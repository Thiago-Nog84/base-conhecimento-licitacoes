"""Confere a qualidade dos .md convertidos (log_conversao.csv) contra o texto do PDF."""
import csv, os, re, sys, collections, unicodedata
import pymupdf

BASE = r'C:\Users\thiagonogueira\Claude'
LOG = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, 'log_conversao.csv')
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(BASE, 'qa_conversao.csv')


def lp(p):
    p = os.path.normpath(p)
    return p if p.startswith('\\\\?\\') else '\\\\?\\' + p


def words(t):
    t = unicodedata.normalize('NFKD', t.lower())
    t = ''.join(c for c in t if not unicodedata.combining(c))
    return re.findall(r'[a-z0-9]{3,}', t)


res = []
for r in csv.DictReader(open(LOG, encoding='utf-8-sig')):
    if r['status'] != 'OK' or not r['pdf'].lower().endswith('.pdf'):
        continue  # docx/xlsx: usar qa_office.py
    md = open(lp(r['md']), encoding='utf-8').read()
    corpo = re.sub(r'^---\n.*?\n---\n', '', md, count=1, flags=re.S)
    doc = pymupdf.open(lp(r['pdf']))
    pdf_txt = ''.join(p.get_text() for p in doc)
    sem_texto = sum(1 for p in doc if len(p.get_text().strip()) < 100)
    doc.close()
    wp, wm = collections.Counter(words(pdf_txt)), collections.Counter(words(corpo))
    total = sum(wp.values()) or 1
    cobertura = sum(min(c, wm[w]) for w, c in wp.items()) / total
    linhas = [l.strip() for l in corpo.splitlines() if l.strip()]
    rep = collections.Counter(l for l in linhas if len(l) > 15)
    repetidas = sum(c for l, c in rep.items() if c >= 3)
    res.append({
        'arquivo': os.path.basename(r['md'])[:70],
        'metodo': r['metodo'],
        'paginas': r['paginas'],
        'pag_sem_texto': sem_texto,
        'cobertura_palavras': round(cobertura, 3),
        'chars_md': len(corpo),
        'chars_pdf': len(pdf_txt),
        'negrito_quebrado': len(re.findall(r'\*\*\S{1,2}\*\*', corpo)),
        'caractere_invalido': corpo.count('\ufffd'),
        'linhas_repetidas_3x': repetidas,
        'tabelas_md': corpo.count('|---'),
        'titulos': len(re.findall(r'^#{1,6} ', corpo, re.M)),
        'linhas_espacadas': sum(1 for l in corpo.splitlines() if re.match(r'^ {8,}\S', l)),
        'md': r['md'],
    })

with open(OUT, 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(res[0]))
    w.writeheader()
    w.writerows(res)
for x in res:
    print(f"{x['cobertura_palavras']:.3f} | neg {x['negrito_quebrado']:3} | inv {x['caractere_invalido']:3} | rep {x['linhas_repetidas_3x']:4} | tab {x['tabelas_md']:3} | tit {x['titulos']:3} | esp {x['linhas_espacadas']:4} | {x['paginas']:>3}p sem{x['pag_sem_texto']} | {x['metodo'][:22]:22} | {x['arquivo'][:50]}")
