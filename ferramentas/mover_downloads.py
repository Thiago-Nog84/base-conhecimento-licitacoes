"""Move arquivos aprovados dos Downloads para a mestra, com o nome novo.
Uso: python mover_downloads.py <plano.csv>   (colunas: grupo, origem, destino)
Confere: origem existe, destino nao existe, pasta de destino existe. MD5 antes e depois.
Log reversivel (acrescenta) em log_movimentacao_downloads.csv: quando, grupo, status, bytes, md5_antes, md5_depois, origem, destino.
"""
import csv, os, sys, shutil, hashlib, datetime

BASE = r'C:\Users\thiagonogueira\Claude'
LOG = os.path.join(BASE, 'log_movimentacao_downloads.csv')


def lp(p):
    p = os.path.normpath(p)
    return p if p.startswith('\\\\?\\') else '\\\\?\\' + p


def md5(p):
    h = hashlib.md5()
    with open(lp(p), 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


plano = list(csv.DictReader(open(sys.argv[1], encoding='utf-8-sig')))
# pre-checagem completa antes de mover qualquer coisa
erros = []
for r in plano:
    if not os.path.isfile(lp(r['origem'])):
        erros.append(('ORIGEM_NAO_ENCONTRADA', r['origem']))
    if os.path.exists(lp(r['destino'])):
        erros.append(('DESTINO_JA_EXISTE', r['destino']))
    if not os.path.isdir(lp(os.path.dirname(r['destino']))):
        erros.append(('PASTA_DESTINO_INEXISTENTE', r['destino']))
if erros:
    for e in erros:
        print(*e)
    sys.exit('nada foi movido')

novo = not os.path.exists(LOG)
with open(LOG, 'a', encoding='utf-8-sig' if novo else 'utf-8', newline='') as f:
    w = csv.writer(f)
    if novo:
        w.writerow(['quando', 'grupo', 'status', 'bytes', 'md5_antes', 'md5_depois', 'origem', 'destino'])
    for r in plano:
        quando = datetime.datetime.now().isoformat(timespec='seconds')
        antes = ''
        try:
            antes = md5(r['origem'])
            tam = os.path.getsize(lp(r['origem']))
            shutil.move(lp(r['origem']), lp(r['destino']))
            depois = md5(r['destino'])
            st = 'OK' if antes == depois and not os.path.exists(lp(r['origem'])) else 'ERRO_HASH'
        except Exception as e:
            depois, tam, st = '', '', 'ERRO: ' + str(e)[:80]
        w.writerow([quando, r['grupo'], st, tam, antes, depois, r['origem'], r['destino']])
        print(st, antes == depois, os.path.basename(r['destino']))
