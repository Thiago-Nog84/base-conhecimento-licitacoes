"""Copia o .md de origem para o nome do PDF (mesma pasta) nos pares com Status OK. Nunca sobrescreve. Log reversivel + verificacao por hash."""
import csv, os, shutil, hashlib, datetime

BASE = r'C:\Users\thiagonogueira\Claude'
LOG = os.path.join(BASE, 'log_copia_md.csv')


def lp(p):
    p = os.path.normpath(p)
    return p if p.startswith('\\\\?\\') else '\\\\?\\' + p


def md5(p):
    h = hashlib.md5()
    with open(lp(p), 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


rows = [r for r in csv.DictReader(open(os.path.join(BASE, 'plano_copia_md_pares_iguais.csv'), encoding='utf-8-sig'))
        if r['Status'] == 'OK']
with open(LOG, 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(['quando', 'status', 'md_origem', 'md_destino'])
    ok = 0
    for r in rows:
        o, d = r['MD_Origem'], r['MD_Destino']
        q = datetime.datetime.now().isoformat(timespec='seconds')
        try:
            if os.path.exists(lp(d)):
                st = 'IGNORADO_DESTINO_EXISTE'
            else:
                shutil.copy2(lp(o), lp(d))
                st = 'OK' if md5(o) == md5(d) else 'ERRO_HASH'
                ok += st == 'OK'
        except Exception as e:
            st = 'ERRO: ' + str(e)[:80]
        w.writerow([q, st, o, d])
print('copiados e verificados:', ok, 'de', len(rows))
