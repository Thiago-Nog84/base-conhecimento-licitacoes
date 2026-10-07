"""Converte PDFs em .md (ao lado do PDF, mesmo nome) com front-matter.

Uso:
  python converter_pdf_md.py <lista.csv> [--saida-dir DIR] [--limite N]
A lista CSV precisa da coluna CaminhoPDF. Sem --saida-dir, grava ao lado do PDF.
Nunca sobrescreve .md existente. Registra tudo em log_conversao.csv.
"""
import csv, os, sys, io, hashlib, datetime, argparse, re, collections
import pymupdf, pymupdf4llm, pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = os.path.expandvars(r'%LOCALAPPDATA%\Programs\Tesseract-OCR\tesseract.exe')
LOG = r'C:\Users\thiagonogueira\Claude\log_conversao.csv'

def lp(p):
    p = os.path.normpath(p)
    return p if p.startswith('\\\\?\\') else '\\\\?\\' + p

def md5(path):
    h = hashlib.md5()
    with open(lp(path), 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()

def ocr_page(page):
    # paginas gigantes (ex.: informativo de 5000x5000 pt) estouram o limite de pixels do PIL: reduz o DPI
    dpi, pol_l, pol_a = 250, page.rect.width / 72, page.rect.height / 72
    while dpi > 72 and (pol_l * dpi > 8000 or pol_l * pol_a * dpi * dpi > 150e6):
        dpi -= 10
    pix = page.get_pixmap(dpi=dpi)
    img = Image.open(io.BytesIO(pix.tobytes('png')))
    # paginas muito altas (infograficos) excedem o limite do Tesseract (32767 px): OCR em faixas
    faixa = 8000
    if img.height <= faixa:
        return pytesseract.image_to_string(img, lang='por')
    return '\n'.join(pytesseract.image_to_string(img.crop((0, y, img.width, min(y + faixa, img.height))), lang='por')
                     for y in range(0, img.height, faixa))

def texto_simples(page):
    # remove recuos e espacos de justificacao/diagramacao
    linhas = [re.sub(r' {2,}', ' ', l).strip() for l in page.get_text(sort=True).splitlines()]
    return '\n'.join(linhas)


BORDA = 4  # cabecalho/rodape: entre as 4 primeiras ou 4 ultimas linhas nao vazias da pagina


def chave(l):
    return re.sub(r'[#*_\s]+', ' ', l).strip()


def remover_repetidas(paginas):
    """Remove cabecalhos/rodapes: linha (fora de tabela, > 15 caracteres) que aparece na borda
    (inicio ou fim) de >= 40% das paginas (75% se < 10 paginas; minimo 3). Mantem a 1a ocorrencia e as ocorrencias
    no meio do texto, para nao apagar conteudo repetido de verdade (ex.: nome do orgao em pautas)."""
    n = len(paginas)
    if n < 4:
        return paginas
    def bordas(p):
        idx = [i for i, l in enumerate(p.splitlines()) if l.strip()]
        return set(idx[:BORDA] + idx[-BORDA:])
    freq = collections.Counter()
    for p in paginas:
        ls, b = p.splitlines(), bordas(p)
        # > 15 caracteres: preserva rotulos curtos de formularios ("Descricao", "Objeto")
        freq.update({chave(ls[i]) for i in b if len(chave(ls[i])) > 15 and not ls[i].lstrip().startswith('|')})
    # documentos curtos (< 10 paginas): exige 75% das paginas, pois pautas repetem situacoes ("RETIRADO DE PAUTA")
    rep = {k for k, c in freq.items() if c >= max(3, n * (0.4 if n >= 10 else 0.75))}
    if not rep:
        return paginas
    vistas, out = set(), []
    for p in paginas:
        ls, b = p.splitlines(), bordas(p)
        linhas = []
        for i, l in enumerate(ls):
            k = chave(l)
            if k in rep and i in b:
                if k in vistas:
                    continue
                vistas.add(k)
            linhas.append(l)
        out.append('\n'.join(linhas))
    return out


def extrair_paginas(pdf):
    doc = pymupdf.open(lp(pdf))
    n = doc.page_count
    textos = [doc[i].get_text() for i in range(n)]
    # OCR: pagina sem texto, ou com muitos glifos sem mapeamento Unicode (U+FFFD)
    ocr = {i for i in range(n) if len(textos[i].strip()) < 100 or textos[i].count('�') >= 5}
    if len(ocr) <= n * 0.2:
        chunks = pymupdf4llm.to_markdown(doc, page_chunks=True, show_progress=False)
        paginas = [c['text'] for c in chunks]
        ocr |= {i for i, p in enumerate(paginas) if p.count('�') >= 5}
        metodo = 'texto (pymupdf4llm)'
        # slides/fontes especiais geram negrito em letras isoladas: usar texto simples
        if len(re.findall(r'\*\*\S{1,2}\*\*', '\n'.join(paginas))) > 15:
            paginas = [texto_simples(doc[i]) for i in range(n)]
            metodo = 'texto (pymupdf simples; markdown tinha artefatos)'
        if ocr:
            metodo += f' + OCR em {len(ocr)} pagina(s)'
    else:
        paginas = [textos[i] for i in range(n)]
        metodo = 'OCR tesseract por'
    # OCR no lugar da propria pagina (preserva a ordem do documento)
    for i in sorted(ocr):
        paginas[i] = ocr_page(doc[i])
    doc.close()
    return paginas, ocr, n, metodo


def converter(pdf):
    paginas, ocr, n, metodo = extrair_paginas(pdf)
    paginas = remover_repetidas(paginas)
    md = '\n\n'.join(f'<!-- pagina {i+1}{" (OCR)" if i in ocr else ""} -->\n' + p.strip() for i, p in enumerate(paginas))
    invalidos = md.count('�')
    if invalidos:
        metodo += f'; {invalidos} caractere(s) ilegivel(is)'
    return md, n, metodo

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('lista'); ap.add_argument('--saida-dir'); ap.add_argument('--limite', type=int)
    ap.add_argument('--log', default=LOG)
    a = ap.parse_args()
    rows = list(csv.DictReader(open(a.lista, encoding='utf-8-sig')))
    if a.limite: rows = rows[:a.limite]
    novo = not os.path.exists(a.log)
    lg = open(a.log, 'a', encoding='utf-8-sig', newline='')
    w = csv.writer(lg)
    if novo: w.writerow(['quando', 'status', 'metodo', 'paginas', 'caracteres', 'pdf', 'md'])
    for r in rows:
        pdf = r['CaminhoPDF']
        base = os.path.splitext(os.path.basename(pdf))[0]
        dest_dir = a.saida_dir or os.path.dirname(pdf)
        dest = os.path.join(dest_dir, base + '.md')
        quando = datetime.datetime.now().isoformat(timespec='seconds')
        try:
            if os.path.exists(lp(dest)):
                w.writerow([quando, 'IGNORADO_MD_JA_EXISTE', '', '', '', pdf, dest]); continue
            md, n, metodo = converter(pdf)
            md = re.sub(r'\n{3,}', '\n\n', md).strip()
            fm = ('---\n'
                  f'arquivo_original: "{os.path.basename(pdf)}"\n'
                  f'hash_pdf_md5: {md5(pdf)}\n'
                  f'paginas: {n}\n'
                  f'metodo: "{metodo}"\n'
                  f'convertido_em: {quando}\n'
                  'fonte: Base de Conhecimento CLC\n'
                  '---\n\n')
            os.makedirs(lp(dest_dir), exist_ok=True)
            with open(lp(dest), 'w', encoding='utf-8', newline='\n') as f:
                f.write(fm + md + '\n')
            w.writerow([quando, 'OK', metodo, n, len(md), pdf, dest])
        except Exception as e:
            w.writerow([quando, 'ERRO: ' + str(e)[:80], '', '', '', pdf, dest])
        lg.flush()
    lg.close()

if __name__ == '__main__':
    main()
