import csv, re, os, sys, unicodedata, collections, io
import pymupdf, pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = os.path.expandvars(r'%LOCALAPPDATA%\Programs\Tesseract-OCR\tesseract.exe')
ROOT = r'C:\Users\thiagonogueira\OneDrive - mppi.mp.br\CLC\01_Processos_e_Aquisicoes\Base de Conhecimento - Thiago'
V2 = r'C:\Users\thiagonogueira\Claude\mapa_pares_pdf_md_v2.csv'
OUT = r'C:\Users\thiagonogueira\Claude\comparacao_conteudo_pdf_md.csv'
MAXPAGES = 8   # paginas lidas por PDF
MAXOCR = 3     # paginas com OCR por PDF
K = 4          # tamanho do shingle (palavras)
COLS = ['Classe', 'Score', 'Pasta', 'PDF', 'MelhorMD', 'Paginas', 'OCR', 'Tipo', 'TamanhoPDF_KB', 'CaminhoPDF']


def lp(p):
    p = os.path.normpath(p)
    return p if p.startswith('\\\\?\\') else '\\\\?\\' + p


def norm_words(t):
    t = unicodedata.normalize('NFKD', t.lower())
    t = ''.join(c for c in t if not unicodedata.combining(c))
    return re.findall(r'[a-z0-9]{2,}', t)


def shingles(w):
    return {hash(tuple(w[i:i + K])) for i in range(max(0, len(w) - K + 1))}


def strip_fm(t):
    if t.startswith('---'):
        m = re.match(r'---\s*\n.*?\n---\s*\n', t, re.S)
        if m:
            return t[m.end():]
    return t


# ---- MDs da mestra (exceto quarentena) com indice invertido
mds = []
inv = collections.defaultdict(list)
for dp, dn, fn in os.walk(lp(ROOT)):
    if '_DUPLICADOS_para_arquivar' in dp or '.vscode' in dp or '__pycache__' in dp:
        continue
    for f in fn:
        if f.lower().endswith('.md'):
            path = os.path.join(dp, f)
            try:
                txt = strip_fm(open(path, encoding='utf-8', errors='ignore').read())
            except Exception:
                continue
            sh = shingles(norm_words(txt))
            idx = len(mds)
            mds.append({'path': path.replace('\\\\?\\', ''), 'name': f})
            for h in sh:
                inv[h].append(idx)
print('MDs lidos:', len(mds), flush=True)

rows = list(csv.DictReader(open(V2, encoding='utf-8-sig')))


def pdf_text(path):
    d = pymupdf.open(lp(path))
    n = d.page_count
    txt = ''
    ocr_n = 0
    for i in range(min(n, MAXPAGES)):
        t = d[i].get_text()
        if len(t.strip()) < 100 and ocr_n < MAXOCR:
            ocr_n += 1
            pix = d[i].get_pixmap(dpi=200)
            img = Image.open(io.BytesIO(pix.tobytes('png')))
            t = pytesseract.image_to_string(img, lang='por')
        txt += '\n' + t
    d.close()
    return txt, n, ocr_n > 0


f_out = open(OUT, 'w', encoding='utf-8-sig', newline='')
wr = csv.DictWriter(f_out, fieldnames=COLS, extrasaction='ignore')
wr.writeheader()
res = []
for k, r in enumerate(rows):
    try:
        txt, n, ocr = pdf_text(r['CaminhoPDF'])
    except Exception as e:
        row = {**r, 'Paginas': '', 'OCR': '', 'Classe': 'ERRO_LEITURA', 'Score': 0, 'MelhorMD': str(e)[:60]}
        res.append(row); wr.writerow(row); f_out.flush()
        continue
    sh = shingles(norm_words(txt))
    best, bc = None, 0.0
    if len(sh) >= 20:
        cnt = collections.Counter()
        for h in sh:
            for idx in inv.get(h, ()):
                cnt[idx] += 1
        if cnt:
            idx, inter = cnt.most_common(1)[0]
            best, bc = mds[idx], inter / len(sh)
    if len(sh) < 20:
        cl = 'SEM_TEXTO_SUFICIENTE'
    elif bc >= 0.60:
        cl = 'IGUAL'
    elif bc >= 0.25:
        cl = 'PROVAVEL_REVISAR'
    else:
        cl = 'DISTINTO'
    row = {**r, 'Paginas': n, 'OCR': 'sim' if ocr else 'nao', 'Classe': cl, 'Score': round(bc, 2),
           'MelhorMD': (best['path'].replace(ROOT, 'mestra') if best else '')}
    res.append(row); wr.writerow(row); f_out.flush()
    if (k + 1) % 20 == 0:
        print('PDFs processados', k + 1, flush=True)

f_out.close()
print(collections.Counter(r['Classe'] for r in res))
print('OCR usado em', sum(1 for r in res if r['OCR'] == 'sim'), 'PDFs')
