# Extrair tokens de uma Query SPARQL

import sys
import re


def tokenize(input_string):
    reconhecidos = []
    linha = 1
    
    mo = re.finditer(r'(?P<SELECT>\bSELECT\b)|(?P<WHERE>\bWHERE\b)|(?P<VAR>\?[a-zA-Z0-9]+)|(?P<ID>:[a-zA-Z0-9]+)|(?P<PREF>[a-zA-Z0-9]+)|(?P<PA>\{)|(?P<PF>\})|(?P<PONTO>\.)|(?P<SKIP>[ \t])|(?P<NEWLINE>\n)|(?P<ERRO>.)', input_string)    
    for m in mo:
        dic = m.groupdict()
        
        if dic['SELECT']:
            t = ("SELECT", dic['SELECT'], linha, m.span())
        
        elif dic['WHERE']:
            t = ("WHERE", dic['WHERE'], linha, m.span())
        
        elif dic['VAR']:
            t = ("VAR", dic['VAR'], linha, m.span())
        
        elif dic['ID']:
            t = ("ID", dic['ID'], linha, m.span())
        
        elif dic['PREF']:
            t = ("PREF", dic['PREF'], linha, m.span())
        
        elif dic['PA']:
            t = ("PA", dic['PA'], linha, m.span())
        
        elif dic['PF']:
            t = ("PF", dic['PF'], linha, m.span())
        
        elif dic['PONTO']:
            t = ("PONTO", dic['PONTO'], linha, m.span())
        
        elif dic['SKIP']:
            t = ("SKIP", dic['SKIP'], linha, m.span())
        
        elif dic['NEWLINE']:
            t = ("NEWLINE", dic['NEWLINE'], linha, m.span())
            linha +=1
        
        elif dic['ERRO']:
            t = ("ERRO", dic['ERRO'], linha, m.span())
        
        else:
            t = ("UNKNOWN", m.group(), linha, m.span())
        
        if not dic['SKIP'] and t[0] != 'UNKNOWN': reconhecidos.append(t)
    return reconhecidos

    

if __name__ == "__main__":
    query = """SELECT ?a ?b ?c WHERE {
        ?a Rdfitype Pessoa.
        ?a   :temIdade  ?b.
        ?a   :eIrmaDe   ?c.
    }"""
    for tok in tokenize(query):
        print(tok)