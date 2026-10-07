import csv, os, collections

ROOT = r'C:\Users\thiagonogueira\OneDrive - mppi.mp.br\CLC\01_Processos_e_Aquisicoes\Base de Conhecimento - Thiago'
BASE = r'C:\Users\thiagonogueira\Claude'


def lp(p):
    p = os.path.normpath(p)
    return p if p.startswith('\\\\?\\') else '\\\\?\\' + p


r = [x for x in csv.DictReader(open(os.path.join(BASE, 'comparacao_conteudo_pdf_md.csv'), encoding='utf-8-sig'))
     if x['Classe'] == 'IGUAL']
uso = collections.Counter(x['MelhorMD'] for x in r)
out = []
for x in r:
    md = x['MelhorMD'].replace('mestra', ROOT, 1)
    dest = os.path.splitext(x['CaminhoPDF'])[0] + '.md'
    if os.path.exists(lp(dest)):
        st = 'DESTINO_JA_EXISTE'
    elif not os.path.exists(lp(md)):
        st = 'MD_ORIGEM_NAO_ENCONTRADO'
    elif uso[x['MelhorMD']] > 1:
        st = 'MD_USADO_POR_VARIOS_PDFS'
    elif float(x['Score']) < 0.9:
        st = 'SCORE_BAIXO_CONFERIR'
    else:
        st = 'OK'
    out.append({'Status': st, 'Score': x['Score'], 'PDF': x['PDF'], 'MD_Origem': md, 'MD_Destino': dest})

with open(os.path.join(BASE, 'plano_copia_md_pares_iguais.csv'), 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0]))
    w.writeheader()
    w.writerows(out)
print(collections.Counter(o['Status'] for o in out))
for o in out:
    if o['Status'] != 'OK':
        print(o['Status'], o['Score'], o['PDF'][:55], '->', os.path.basename(o['MD_Origem'])[:55])
