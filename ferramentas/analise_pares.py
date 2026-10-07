import csv, re, unicodedata, sys, os, collections
import pymupdf

SRC = r'C:\Users\thiagonogueira\Claude\mapa_pares_pdf_md.csv'
OUT = r'C:\Users\thiagonogueira\Claude\mapa_pares_pdf_md_v2.csv'
STOP = set('de da do das dos e a o as os em para por com na no nas nos um uma ao aos pdf md ocred ocr federal estadual tce tjpi cnmp mppi n no nº'.split())

def toks(name):
    name = os.path.splitext(name)[0].lower()
    name = unicodedata.normalize('NFKD', name)
    name = ''.join(c for c in name if not unicodedata.combining(c))
    t = re.findall(r'[a-z0-9]+', name)
    return {x for x in t if x not in STOP and len(x) > 1}

rows = list(csv.DictReader(open(SRC, encoding='utf-8-sig')))
pdfs = [r for r in rows if r['Status'] == 'PDF_SEM_MD']
mds = [r for r in rows if r['Status'] == 'MD_SEM_PDF']
md_t = [(m, toks(m['MD'])) for m in mds]

def top(r):
    return r['Pasta'].split('\\')[1] if '\\' in r['Pasta'] else ''

res = []
for p in pdfs:
    pt = toks(p['PDF'])
    best, bs = None, 0
    for m, mt in md_t:
        if not pt or not mt:
            continue
        s = len(pt & mt) / len(pt | mt)
        if s > bs:
            best, bs = m, s
    p['MatchScore'] = round(bs, 2)
    p['MatchMD'] = best['MD'] if best else ''
    p['MatchMDPasta'] = best['Pasta'] if best else ''

    # texto ou escaneado
    try:
        d = pymupdf.open(p['CaminhoPDF'])
        n = d.page_count
        sample = [i for i in range(n)][:5]
        chars = sum(len(d[i].get_text().strip()) for i in sample)
        p['Paginas'] = n
        p['CharsPorPag_Amostra'] = round(chars / max(1, len(sample)))
        p['Tipo'] = 'TEXTO' if chars / max(1, len(sample)) > 200 else 'ESCANEADO_OU_POUCO_TEXTO'
        if d.needs_pass:
            p['Tipo'] = 'PROTEGIDO'
        d.close()
    except Exception as e:
        p['Paginas'] = ''
        p['CharsPorPag_Amostra'] = ''
        p['Tipo'] = 'ERRO_ABERTURA'
    res.append(p)

cols = ['Status','Pasta','PDF','TamanhoPDF_KB','Paginas','Tipo','CharsPorPag_Amostra','MatchScore','MatchMD','MatchMDPasta','CaminhoPDF']
with open(OUT, 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore')
    w.writeheader()
    w.writerows(res)

c = collections.Counter(r['Tipo'] for r in res)
print('PDFs analisados:', len(res), dict(c))
print('Paginas totais:', sum(r['Paginas'] for r in res if r['Paginas'] != ''))
hi = [r for r in res if r['MatchScore'] >= 0.6]
mid = [r for r in res if 0.4 <= r['MatchScore'] < 0.6]
print('pares provaveis (score>=0.6):', len(hi), ' duvidosos (0.4-0.6):', len(mid))
for r in sorted(hi, key=lambda x: -x['MatchScore'])[:12]:
    print(f"  {r['MatchScore']}  {r['PDF'][:60]}  <->  {r['MatchMD'][:60]}")
byf = collections.Counter((top(r), r['Tipo']) for r in res)
for k, v in sorted(byf.items()):
    print(k, v)
