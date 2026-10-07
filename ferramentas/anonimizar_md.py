"""Substitui dados pessoais por marcadores nos .md de um lote (o original docx/pdf fica intacto).
Uso: python anonimizar_md.py <log_lote.csv> <regras.py> [--front-matter]
--front-matter: aplica as regras tambem ao front-matter (so para .md autorais, cujo cabecalho e conteudo,
ex.: "elaboracao: <nome>"; nos convertidos o cabecalho tem so dados tecnicos e fica intacto).
regras.py define REGRAS = [(rotulo, regex, substituicao), ...]. O rotulo vai para o log; o texto removido nao.
Backup de cada .md alterado em backup_md\\anonimizacao\\<data>\\ antes de gravar. Idempotente.
Log: log_anonimizacao.csv (quando, md, rotulo, ocorrencias, backup).
"""
import csv, os, re, sys, shutil, datetime, runpy

BASE = r'C:\Users\thiagonogueira\Claude'
LOG = os.path.join(BASE, 'log_anonimizacao.csv')


def lp(p):
    p = os.path.normpath(p)
    return p if p.startswith('\\\\?\\') else '\\\\?\\' + p


regras = runpy.run_path(sys.argv[2])['REGRAS']
hoje = datetime.date.today().isoformat()
bdir = os.path.join(BASE, 'backup_md', 'anonimizacao', hoje)
os.makedirs(bdir, exist_ok=True)
novo = not os.path.exists(LOG)
lg = open(LOG, 'a', encoding='utf-8-sig', newline='')
w = csv.writer(lg)
if novo:
    w.writerow(['quando', 'md', 'rotulo', 'ocorrencias', 'backup'])
total = 0
for r in csv.DictReader(open(sys.argv[1], encoding='utf-8-sig')):
    if r['status'] != 'OK':
        continue
    md = r['md']
    txt = open(lp(md), encoding='utf-8').read()
    # o front-matter (caminhos do original) nao e alterado
    m = re.match(r'^---\n.*?\n---\n', txt, re.S)
    cab, corpo = (m.group(0), txt[m.end():]) if m and '--front-matter' not in sys.argv else ('', txt)
    contagem = []
    for rot, rx, sub in regras:
        corpo, n = re.subn(rx, sub, corpo)
        if n:
            contagem.append((rot, n))
    if not contagem:
        continue
    bk = os.path.join(bdir, os.path.basename(md))
    if not os.path.exists(lp(bk)):
        shutil.copy2(lp(md), lp(bk))
    with open(lp(md), 'w', encoding='utf-8', newline='\n') as f:
        f.write(cab + corpo)
    agora = datetime.datetime.now().isoformat(timespec='seconds')
    for rot, n in contagem:
        w.writerow([agora, md, rot, n, bk])
        total += n
    print(os.path.basename(md)[:60], contagem)
lg.close()
print('substituicoes:', total)
