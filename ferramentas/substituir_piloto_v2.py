"""Substitui os .md do piloto (conversor v1) pelos da v2, na mestra e no clone.
Antes, guarda o .md v1 em backup_piloto_v1/ (mesma estrutura de pastas). Infograficos ficam como estao.
Verificacao por hash. Log em log_substituicao_piloto_v2.csv.
"""
import csv, os, shutil, hashlib, datetime
import pymupdf

BASE = r'C:\Users\thiagonogueira\Claude'
ROOT = r'C:\Users\thiagonogueira\OneDrive - mppi.mp.br\CLC\01_Processos_e_Aquisicoes\Base de Conhecimento - Thiago'
REPO = r'C:\Users\thiagonogueira\Dev\base-conhecimento-licitacoes'
BACKUP = os.path.join(BASE, 'backup_piloto_v1')
V2_LOG = r'C:\Users\thiagonogueira\AppData\Local\Temp\claude\C--Users-thiagonogueira-Claude\768e0e83-5666-4657-904e-3362959700b5\scratchpad\log_piloto_v2.csv'


def lp(p):
    p = os.path.normpath(p)
    return p if p.startswith('\\\\?\\') else '\\\\?\\' + p


def md5(p):
    h = hashlib.md5()
    with open(lp(p), 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def eh_infografico(pdf):
    if 'infograficos_zenite' in pdf.lower():
        return True
    doc = pymupdf.open(lp(pdf))
    r = doc[0].rect if doc.page_count == 1 else None
    doc.close()
    return bool(r) and r.height > 3 * r.width


def copiar(o, d):
    os.makedirs(lp(os.path.dirname(d)), exist_ok=True)
    shutil.copy2(lp(o), lp(d))
    return md5(o) == md5(d)


v1 = [r for r in csv.DictReader(open(os.path.join(BASE, 'log_conversao.csv'), encoding='utf-8-sig')) if r['status'] == 'OK']
v2 = {os.path.normpath(r['pdf']).lower(): r for r in csv.DictReader(open(V2_LOG, encoding='utf-8-sig')) if r['status'] == 'OK'}

with open(os.path.join(BASE, 'log_substituicao_piloto_v2.csv'), 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(['quando', 'status', 'md_mestra', 'backup_v1', 'md_v2', 'md_repo'])
    for r in v1:
        quando = datetime.datetime.now().isoformat(timespec='seconds')
        mestra = os.path.normpath(r['md'])
        rel = os.path.relpath(mestra, ROOT)
        bkp, repo = os.path.join(BACKUP, rel), os.path.join(REPO, rel)
        novo = v2.get(os.path.normpath(r['pdf']).lower())
        try:
            if eh_infografico(r['pdf']):
                st = 'MANTIDO_INFOGRAFICO'
            elif not novo:
                st = 'SEM_V2'
            elif not copiar(mestra, bkp):
                st = 'ERRO_HASH_BACKUP'
            elif not copiar(novo['md'], mestra):
                st = 'ERRO_HASH_MESTRA'
            elif not copiar(novo['md'], repo):
                st = 'ERRO_HASH_REPO'
            else:
                st = 'OK'
        except Exception as e:
            st = 'ERRO: ' + str(e)[:80]
        w.writerow([quando, st, mestra, bkp, novo['md'] if novo else '', repo])
        print(st, '|', os.path.basename(mestra)[:80])
