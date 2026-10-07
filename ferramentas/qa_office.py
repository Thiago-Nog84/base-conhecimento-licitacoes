"""Confere os .md gerados por converter_office_md.py contra o texto do original (.docx/.xlsx).
Uso: python qa_office.py <log_lote.csv> <saida_qa.csv>
Referencia independente do conversor: docx = todo <w:t> do corpo, notas e cabecalhos (XML bruto);
xlsx = todos os valores das celulas. cobertura = fracao das palavras distintas do original presentes no .md.
Linhas de PDF no log sao ignoradas (usar qa_conversao.py).
"""
import csv, os, re, sys, zipfile, unicodedata, html
import openpyxl


def lp(p):
    p = os.path.normpath(p)
    return p if p.startswith('\\\\?\\') else '\\\\?\\' + p


def words(t):
    t = unicodedata.normalize('NFKD', t.lower())
    t = ''.join(c for c in t if not unicodedata.combining(c))
    return set(re.findall(r'[a-z0-9]{3,}', t))


def ref_docx(p):
    z = zipfile.ZipFile(lp(p))
    partes = [n for n in z.namelist() if re.match(r'word/(document|footnotes|header\d*)\.xml$', n)]
    # junta os <w:t> de cada paragrafo (palavras quebradas entre runs ficam inteiras)
    txt = []
    for n in partes:
        x = z.read(n).decode('utf8')
        for par in re.findall(r'<w:p[ >].*?</w:p>', x, re.S):
            txt.append(''.join(re.findall(r'<w:t(?: [^>]*)?>([^<]*)</w:t>', par)))
    return html.unescape(' '.join(txt))


def ref_xlsx(p):
    wb = openpyxl.load_workbook(lp(p), data_only=True)
    t = ' '.join(str(v) for ws in wb.worksheets for r in ws.iter_rows(values_only=True) for v in r if v is not None)
    wb.close()
    return t


res = []
for r in csv.DictReader(open(sys.argv[1], encoding='utf-8-sig')):
    ext = os.path.splitext(r['pdf'])[1].lower()
    if r['status'] != 'OK' or ext not in ('.docx', '.xlsx'):
        continue
    md = open(lp(r['md']), encoding='utf-8').read()
    corpo = re.sub(r'^---\n.*?\n---\n', '', md, count=1, flags=re.S)
    ref = words(ref_docx(r['pdf']) if ext == '.docx' else ref_xlsx(r['pdf']))
    wm = words(corpo)
    faltam = sorted(ref - wm)
    res.append({
        'arquivo': os.path.basename(r['md'])[:70],
        'formato': ext[1:],
        'cobertura_palavras': round(len(ref & wm) / (len(ref) or 1), 3),
        'palavras_distintas_original': len(ref),
        'ausentes_exemplo': ' '.join(faltam[:12]),
        'chars_md': len(corpo),
        'tabelas_md': corpo.count('|---'),
        'titulos': len(re.findall(r'^#{1,6} ', corpo, re.M)),
        'itens_lista': len(re.findall(r'^\s*- ', corpo, re.M)),
        'imagens': corpo.count('*[imagem]*'),
        'notas': len(re.findall(r'^\[\^\d+\]:', corpo, re.M)),
        'md': r['md'],
    })

with open(sys.argv[2], 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(res[0]))
    w.writeheader()
    w.writerows(res)
for x in res:
    print(f"{x['cobertura_palavras']:.3f} | tab {x['tabelas_md']:3} | tit {x['titulos']:3} | lis {x['itens_lista']:3} | img {x['imagens']} | not {x['notas']} | {x['arquivo'][:55]:55} | {x['ausentes_exemplo'][:60]}")
