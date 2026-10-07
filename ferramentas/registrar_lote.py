"""Acrescenta as linhas OK de um log de lote ao log mestre (log_conversao.csv), sem duplicar.
Uso: python registrar_lote.py <log_lote.csv>
(mesma logica do trecho final de rodar_lote.py, para lotes convertidos em etapas separadas)
"""
import csv, os, sys

mestre = r'C:\Users\thiagonogueira\Claude\log_conversao.csv'
rows = list(csv.DictReader(open(sys.argv[1], encoding='utf-8-sig')))
ja = {r['pdf'].lower() for r in csv.DictReader(open(mestre, encoding='utf-8-sig')) if r['status'] == 'OK'}
n = 0
with open(mestre, 'a', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    for r in rows:
        if r['status'] == 'OK' and r['pdf'].lower() not in ja:
            w.writerow([r[k] for k in ('quando', 'status', 'metodo', 'paginas', 'caracteres', 'pdf', 'md')])
            n += 1
print(n, 'linhas acrescentadas de', len(rows))
