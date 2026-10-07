"""Roda um lote: converte, audita, registra no log mestre e copia para o clone.
Uso: python rodar_lote.py NN   (le lotes/lote_NN.csv)
Saidas: lotes/log_lote_NN.csv, lotes/qa_lote_NN.csv; linhas OK acrescentadas a log_conversao.csv.
O commit/push no repositorio e feito depois, manualmente, apos conferir o QA.
"""
import csv, os, sys, subprocess

BASE = r'C:\Users\thiagonogueira\Claude'
S = os.path.join(BASE, 'scripts')
L = os.path.join(BASE, 'lotes')
n = sys.argv[1].zfill(2)
lista, log, qa = (os.path.join(L, f'{p}_{n}.csv') for p in ('lote', 'log_lote', 'qa_lote'))
mestre = os.path.join(BASE, 'log_conversao.csv')

subprocess.run([sys.executable, os.path.join(S, 'converter_pdf_md.py'), lista, '--log', log], check=True)
subprocess.run([sys.executable, os.path.join(S, 'qa_conversao.py'), log, qa], check=True)

rows = list(csv.DictReader(open(log, encoding='utf-8-sig')))
ja = {r['pdf'].lower() for r in csv.DictReader(open(mestre, encoding='utf-8-sig')) if r['status'] == 'OK'}
with open(mestre, 'a', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    for r in rows:
        if r['status'] == 'OK' and r['pdf'].lower() not in ja:
            w.writerow([r[k] for k in ('quando', 'status', 'metodo', 'paginas', 'caracteres', 'pdf', 'md')])
print('lote', n, ':', sum(r['status'] == 'OK' for r in rows), 'OK de', len(rows),
      '| outros:', [(os.path.basename(r['pdf'])[:50], r['status']) for r in rows if r['status'] != 'OK'])

subprocess.run([sys.executable, os.path.join(S, 'carregar_repo.py')], check=True)
