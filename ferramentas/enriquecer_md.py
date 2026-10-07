"""Acrescenta front-matter semantico + titulo + bloco 'Ementa / Sintese' a .md recem-convertidos.
Uso: python enriquecer_md.py <log_lote.csv> <metadados.py>
metadados.py define META = {arquivo_original: dict(tipo, numero, ano, orgao, ambito, assunto, status, tags, titulo, ementa)}.
So mexe em .md cujo front-matter ainda nao tem 'tipo:' (idempotente). Mantem os campos tecnicos intactos.
Backup do .md original em backup_md/enriquecimento/ antes de gravar.
"""
import csv, os, sys, shutil, runpy, datetime

BACKUP = r'C:\Users\thiagonogueira\Claude\backup_md\enriquecimento'


def lp(p):
    p = os.path.normpath(p)
    return p if p.startswith('\\\\?\\') else '\\\\?\\' + p


def q(s):
    return '"' + str(s).replace('"', '\\"') + '"'


META = runpy.run_path(sys.argv[2])['META']
os.makedirs(BACKUP, exist_ok=True)
for r in csv.DictReader(open(sys.argv[1], encoding='utf-8-sig')):
    if r['status'] != 'OK':
        continue
    md = r['md']
    nome = os.path.basename(r['pdf'])
    m = META.get(nome)
    if not m:
        print('SEM_METADADOS', nome)
        continue
    t = open(lp(md), encoding='utf-8').read()
    fim = t.find('\n---', 4)
    fm, corpo = t[:fim], t[fim + 4:]
    if '\ntipo:' in fm:
        print('JA_ENRIQUECIDO', nome)
        continue
    sem = (f'\ntipo: {q(m["tipo"])}\nnumero: {q(m["numero"])}\nano: {m["ano"]}\norgao: {q(m["orgao"])}'
           f'\nambito: {q(m["ambito"])}\nassunto: {q(m["assunto"])}\nstatus: {q(m["status"])}\ntags: {m["tags"]!r}')
    cab = (f'\n\n# {m["titulo"]}\n\n> **Ementa / Síntese:**  \n> {m["ementa"]}  \n'
           f'> **Órgão Emissor:** {m["orgao"]} | **Ano:** {m["ano"]} | **Status:** {m["status"]}\n\n---\n')
    stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    shutil.copy2(lp(md), lp(os.path.join(BACKUP, f'{stamp}_{os.path.basename(md)}')))
    open(lp(md), 'w', encoding='utf-8', newline='\n').write(fm + sem + '\n---' + cab + corpo)
    print('OK', nome)
