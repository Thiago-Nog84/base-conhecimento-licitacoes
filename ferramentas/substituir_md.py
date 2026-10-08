"""Substitui .md ja convertidos por uma nova conversao (gerada com --saida-dir em pasta temporaria).
Uso: python substituir_md.py <log_da_nova_conversao.csv> <pasta_backup> <log_saida.csv>
Para cada linha OK: guarda o .md atual da mestra em <pasta_backup> (mesma estrutura), copia o novo
para a mestra e para o clone. Hash conferido. So usar com autorizacao do usuario (AGENTS.md, regra 3).
"""
import csv, os, sys, shutil, hashlib, datetime

ROOT = r'C:\Users\thiagonogueira\OneDrive - mppi.mp.br\CLC\01_Processos_e_Aquisicoes\Base de Conhecimento - Thiago'
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # raiz do clone (pasta acima de ferramentas)


def lp(p):
    p = os.path.normpath(p)
    return p if p.startswith('\\\\?\\') else '\\\\?\\' + p


def md5(p):
    h = hashlib.md5()
    with open(lp(p), 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def copiar(o, d):
    os.makedirs(lp(os.path.dirname(d)), exist_ok=True)
    shutil.copy2(lp(o), lp(d))
    return md5(o) == md5(d)


log_novo, backup, saida = sys.argv[1:4]
with open(saida, 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(['quando', 'status', 'md_mestra', 'backup', 'md_novo', 'md_repo'])
    for r in csv.DictReader(open(log_novo, encoding='utf-8-sig')):
        if r['status'] != 'OK':
            continue
        mestra = os.path.join(os.path.dirname(r['pdf']), os.path.splitext(os.path.basename(r['pdf']))[0] + '.md')
        rel = os.path.relpath(mestra, ROOT)
        bkp, repo = os.path.join(backup, rel), os.path.join(REPO, rel)
        try:
            if not os.path.exists(lp(mestra)):
                st = 'SEM_MD_NA_MESTRA'
            elif not copiar(mestra, bkp):
                st = 'ERRO_HASH_BACKUP'
            elif not copiar(r['md'], mestra):
                st = 'ERRO_HASH_MESTRA'
            elif not copiar(r['md'], repo):
                st = 'ERRO_HASH_REPO'
            else:
                st = 'OK'
        except Exception as e:
            st = 'ERRO: ' + str(e)[:80]
        w.writerow([datetime.datetime.now().isoformat(timespec='seconds'), st, mestra, bkp, r['md'], repo])
        print(st, '|', os.path.basename(mestra)[:80])
