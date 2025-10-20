import ply.lex as lex

tokens = (
    'LISTAR',
    'MOEDA',
    'SELECIONAR',
    'SAIR',
    'ADICIONAR',
    'VALOR',
    'COD',
    'NUM',
    'NOME',
    'PRECO'
)

t_LISTAR     = r'LISTAR'
t_MOEDA      = r'MOEDA'
t_SELECIONAR = r'SELECIONAR'
t_SAIR       = r'SAIR'
t_ADICIONAR  = r'ADICIONAR'
t_COD        = r'[A-Z]\d{2}'
t_NOME       = r'[A-Za-zÁÉÍÓÚáéíóúçÇ0-9_]+'
t_PRECO      = r'\d+(\.\d+)?'
t_NUM        = r'\d+'

# moedas: 1e, 2e, 10c, 50c, etc.
t_VALOR = r'(1e|2e|50c|20c|10c|5c|2c|1c)'

t_ignore = ' \t\n'

def t_error(t):
    print(f"Caractere inválido: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()