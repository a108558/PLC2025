import json
from datetime import date
from maq_lex import lexer

FICHEIRO_STOCK = "stock.json"

MOEDAS_VALIDAS = {
    "2e": 200, "1e": 100, "50c": 50, "20c": 20, "10c": 10, "5c": 5, "2c": 2, "1c": 1
}

def carregar_stock():
    try:
        with open(FICHEIRO_STOCK, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def gravar_stock(stock):
    with open(FICHEIRO_STOCK, "w", encoding="utf-8") as f:
        json.dump(stock, f, ensure_ascii=False, indent=4)

def listar_stock(stock):
    print("maq:\ncod | nome | quantidade | preço")
    print("---------------------------------")
    for item in stock:
        print(f"{item['cod']:3} {item['nome']:20} {item['quant']:5} {item['preco']:>5.2f}")

def calcular_troco(valor):
    troco = {}
    for m, v in MOEDAS_VALIDAS.items():
        if valor >= v:
            qtd = valor // v
            valor -= qtd * v
            troco[m] = qtd
    return troco

def mostrar_troco(troco):
    partes = [f"{v}x {k}" for k, v in troco.items() if v > 0]
    print("maq: Pode retirar o troco:", ", ".join(partes))

def main():
    stock = carregar_stock()
    saldo = 0

    print(f"maq: {date.today()}, Stock carregado, Estado atualizado.")
    print("maq: Bom dia. Estou disponível para atender o seu pedido.")

    while True:
        linha = input(">> ")
        lexer.input(linha)
        tokens = [tok for tok in lexer] 

        if not tokens:
            continue

        t0 = tokens[0]

        if t0.type == "LISTAR":
            listar_stock(stock)

        elif t0.type == "MOEDA":
            total = 0
            for tok in tokens[1:]:
                if tok.type == "VALOR":
                    total += MOEDAS_VALIDAS[tok.value]
                else:
                    print(f"maq: moeda inválida: {tok.value}")
            saldo += total
            print(f"maq: Saldo = {saldo//100}e{saldo%100:02d}c")

        elif t0.type == "SELECIONAR":
            if len(tokens) < 2:
                print("maq: Indique o código do produto.")
                continue
            cod = tokens[1].value
            produto = next((p for p in stock if p["cod"] == cod), None)

            if not produto:
                print("maq: Produto inexistente.")
            elif produto["quant"] <= 0:
                print("maq: Produto esgotado.")
            elif saldo < int(produto["preco"] * 100):
                falta = int(produto["preco"] * 100) - saldo
                print(f"maq: Saldo insuficiente ({saldo//100}e{saldo%100:02d}c); Falta {falta//100}e{falta%100:02d}c.")
            else:
                saldo -= int(produto["preco"] * 100)
                produto["quant"] -= 1
                print(f'maq: Pode retirar o produto "{produto["nome"]}"')
                print(f"maq: Saldo = {saldo//100}e{saldo%100:02d}c")

        elif t0.type == "SAIR":
            if saldo > 0:
                troco = calcular_troco(saldo)
                mostrar_troco(troco)
            gravar_stock(stock)
            print("maq: Até à próxima")
            break

        else:
            print("maq: Comando não reconhecido.")

if __name__ == "__main__":
    main()
