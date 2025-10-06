# Conversor de MarkDown para HTML

import re

def markdown_to_html(texto_markdown):
    texto_html = []
    in_ol = False

    for linha in texto_markdown.split('\n'):
        
        # Negrito: ente ** **
        linha = re.sub(r'\*\*([^\*]+)\*\*', r'<b>\1</b>', linha)
        
        # Itálico: entre * *
        linha = re.sub(r'\*([^\*]+)\*', r'<i>\1</i>', linha)
        
        # --------------------------------------
        
        # Cabeçalhos
        
        # Se for apenas com # 
        if re.match(r'# (.*)', linha):
            texto_html.append(f"<h1>{re.sub(r'# ', '', linha)}</h1>")
            continue
        
        # Se for com ##
        elif re.match(r'## (.*)', linha):
            texto_html.append(f"<h2>{re.sub(r'## ', '', linha)}</h2>")
            continue
        
        # Se for com ###
        elif re.match(r'### (.*)', linha):
            texto_html.append(f"<h3>{re.sub(r'### ', '', linha)}</h3>")
            continue
        
        
        # --------------------------------------
        
        # Imagens
        linha = re.sub(r'!\[([^\]]+)\]\(([^)]+)\)', r'<img src="\2" alt="\1"/>', linha)
        
        
        # Links
        
        linha = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', linha)
        
        
        # --------------------------------------
        
        # Lista numerada
        
        if re.match(r'\d+\.\s+.*', linha):
            if not in_ol:
                texto_html.append("<ol>")
                in_ol = True
            item = re.sub(r'^\d+\.\s+', '', linha)
            texto_html.append(f"<li>{item}</li>")
            continue
        else:
            if in_ol:
                texto_html.append("</ol>")
                in_ol = False

        texto_html.append(linha)

    if in_ol:
        texto_html.append("</ol>")

    return '\n'.join(texto_html)

# Exemplo de uso:
if __name__ == "__main__":
    md = """
# Exemplo
## Exemplo **de**
### Exemplo de *texto*
Este é um **exemplo** e um *teste*.
1. Primeiro item
2. Segundo item
3. Terceiro item
Como pode ser consultado em [página da UC](http://www.uc.pt)
Como se vê na imagem seguinte: ![imagem dum coelho](http://www.coellho.com)
"""
    print(markdown_to_html(md))