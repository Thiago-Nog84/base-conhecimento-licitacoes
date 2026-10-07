"""Converte .docx, .xlsx e .doc em .md (ao lado do original, mesmo nome) com front-matter.

Uso:
  python converter_office_md.py <lista.csv> [--log LOG] [--saida-dir DIR]
A lista CSV precisa da coluna CaminhoArquivo. Outros formatos sao ignorados (PDF: usar converter_pdf_md.py).
Nunca sobrescreve .md existente. O log tem as mesmas colunas do log de PDFs (a coluna "pdf" guarda o original),
para servir a enriquecer_md.py e registrar_lote.py.

docx: paragrafos e tabelas na ordem do documento; titulos pelo estilo; listas com a numeracao calculada
(marcador de caixa de selecao vira "- [ ]"); controles de conteudo e caixas de texto incluidos; imagens
marcadas como *[imagem]*; notas de rodape no fim; texto do cabecalho no inicio; texto excluido (revisao) ignorado.
xlsx: uma secao por planilha, tabela markdown com os valores calculados (linhas e colunas vazias removidas).
doc (Word 97-2003): texto corrido do corpo, um paragrafo por linha (olefile; campos ficam so com o resultado).
"""
import csv, os, re, sys, hashlib, datetime, argparse, zipfile, struct
from lxml import etree
import openpyxl
import olefile

LOG = r'C:\Users\thiagonogueira\Claude\log_conversao.csv'
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
MC = 'http://schemas.openxmlformats.org/markup-compatibility/2006'
NS = {'w': W}


def lp(p):
    p = os.path.normpath(p)
    return p if p.startswith('\\\\?\\') else '\\\\?\\' + p


def md5(path):
    h = hashlib.md5()
    with open(lp(path), 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def w(tag):
    return '{%s}%s' % (W, tag)


def attr(el, name):
    return None if el is None else el.get(w(name))


# Marcadores Wingdings/Symbol que representam caixa de selecao vazia
CAIXAS = {'\uf0a8', '\uf06f', '\uf071', '\uf072', '\u2610', '\u25a1', '\u274f', '\u274d'}


def romano(n):
    r = ''
    for v, s in ((1000, 'm'), (900, 'cm'), (500, 'd'), (400, 'cd'), (100, 'c'), (90, 'xc'),
                 (50, 'l'), (40, 'xl'), (10, 'x'), (9, 'ix'), (5, 'v'), (4, 'iv'), (1, 'i')):
        while n >= v:
            r, n = r + s, n - v
    return r


def fmt_num(n, fmt):
    if fmt in ('lowerLetter', 'upperLetter'):
        s = ''
        while n > 0:
            n, k = divmod(n - 1, 26)
            s = chr(97 + k) + s
        return s.upper() if fmt == 'upperLetter' else s
    if fmt in ('lowerRoman', 'upperRoman'):
        return romano(n).upper() if fmt == 'upperRoman' else romano(n)
    if fmt == 'decimalZero':
        return '%02d' % n
    return str(n)


class Docx:
    def __init__(self, path):
        self.z = zipfile.ZipFile(lp(path))
        nomes = self.z.namelist()
        self.imagens, self.refs, self.em_tabela = 0, [], 0
        self.xml =lambda n: etree.fromstring(self.z.read(n)) if n in nomes else None
        self.doc = self.xml('word/document.xml')
        self.estilos = {}  # styleId -> (nome, basedOn, numPr(numId, ilvl), negrito)
        st = self.xml('word/styles.xml')
        if st is not None:
            for s in st.findall('w:style', NS):
                np_ = s.find('w:pPr/w:numPr', NS)
                num = (attr(np_.find('w:numId', NS), 'val'), attr(np_.find('w:ilvl', NS), 'val')) if np_ is not None else None
                self.estilos[attr(s, 'styleId')] = (attr(s.find('w:name', NS), 'val') or '', attr(s.find('w:basedOn', NS), 'val'), num)
        self.num, self.abs = {}, {}
        nb = self.xml('word/numbering.xml')
        if nb is not None:
            for a in nb.findall('w:abstractNum', NS):
                lv = {}
                for l in a.findall('w:lvl', NS):
                    lv[int(attr(l, 'ilvl'))] = (attr(l.find('w:numFmt', NS), 'val') or 'decimal',
                                               attr(l.find('w:lvlText', NS), 'val') or '',
                                               int(attr(l.find('w:start', NS), 'val') or 1))
                self.abs[attr(a, 'abstractNumId')] = lv
            for n in nb.findall('w:num', NS):
                ov = {int(attr(o, 'ilvl')): int(attr(o.find('w:startOverride', NS), 'val'))
                      for o in n.findall('w:lvlOverride', NS) if o.find('w:startOverride', NS) is not None}
                self.num[attr(n, 'numId')] = (attr(n.find('w:abstractNumId', NS), 'val'), ov)
        self.cont = {}
        self.notas = {}
        fn = self.xml('word/footnotes.xml')
        if fn is not None:
            for f in fn.findall('w:footnote', NS):
                # separadores tem w:type; a numeracao pode comecar em 0
                if attr(f, 'type') in (None, 'normal'):
                    self.notas[attr(f, 'id')] = ' '.join(self.texto(p) for p in f.iter(w('p'))).strip()
        self.cabecalho = []
        for n in sorted(x for x in nomes if re.match(r'word/header\d*\.xml$', x)):
            t = ' '.join(self.texto(p) for p in self.xml(n).iter(w('p')) if p.getparent().tag != w('txbxContent')).strip()
            t = re.sub(r'\s+', ' ', t.replace('*[imagem]*', '')).strip()
            if t and t not in self.cabecalho:
                self.cabecalho.append(t)
        self.imagens, self.refs = 0, []  # imagens do cabecalho (logotipos) nao contam

    # ---------- texto de um paragrafo ----------
    def texto(self, el):
        out = []
        self._walk(el, out)
        return re.sub(r'[ \t]+', ' ', ''.join(out)).strip()

    def _walk(self, el, out):
        for ch in el:
            t = ch.tag
            if not isinstance(t, str):
                continue
            if t == '{%s}Fallback' % MC or t in (w('pPr'), w('rPr'), w('sdtPr'), w('del'), w('moveFrom'), w('instrText'), w('delText')):
                continue
            if t == w('t'):
                out.append(ch.text or '')
            elif t == w('tab'):
                out.append(' ')
            elif t in (w('br'), w('cr')):
                out.append(' ')
            elif t == w('sym'):
                c = attr(ch, 'char') or ''
                out.append('☐' if c.upper() in ('F0A8', 'F06F', 'F071') else '☒' if c.upper() in ('F0FE', 'F078') else '✓' if c.upper() == 'F0FC' else '')
            elif t == w('fldChar'):
                cb = ch.find('w:ffData/w:checkBox', NS)
                if cb is not None:
                    v = cb.find('w:checked', NS)
                    if v is None:
                        v = cb.find('w:default', NS)
                    out.append('☒ ' if v is not None and attr(v, 'val') not in ('0', 'false') else '☐ ')
            elif t == w('footnoteReference'):
                i = attr(ch, 'id')
                if i in self.notas:
                    self.refs.append(i)
                    out.append('[^%s]' % i)
            elif t in (w('drawing'), w('pict')):
                if ch.find('.//' + w('txbxContent')) is not None:
                    for p in ch.iter(w('p')):
                        out.append(' ' + self.texto(p) + ' ')
                elif ch.find('.//{http://schemas.openxmlformats.org/drawingml/2006/main}blip') is not None or \
                        ch.find('.//{urn:schemas-microsoft-com:vml}imagedata') is not None:
                    self.imagens += 1
                    out.append(' *[imagem]* ')
            elif t == w('p'):
                out.append(' ' + self.texto(ch) + ' ')
            else:
                self._walk(ch, out)

    # ---------- estrutura ----------
    def estilo(self, p):
        sid = attr(p.find('w:pPr/w:pStyle', NS), 'val')
        nome, num, vistos = '', None, set()
        while sid and sid not in vistos:
            vistos.add(sid)
            e = self.estilos.get(sid)
            if not e:
                break
            nome = nome or e[0]
            num = num or e[2]
            sid = e[1]
        return nome, num

    def rotulo(self, numid, ilvl):
        if numid not in self.num or numid == '0':
            return None
        absid, ov = self.num[numid]
        lv = self.abs.get(absid, {})
        if ilvl not in lv:
            return '- '
        c = self.cont.setdefault(numid, {})
        if ilvl in c:
            c[ilvl] += 1
        else:
            c[ilvl] = ov.get(ilvl, lv[ilvl][2])
        for k in [k for k in c if k > ilvl]:
            del c[k]
        fmt, txt, _ = lv[ilvl]
        if fmt == 'bullet':
            return '- [ ] ' if txt in CAIXAS else '- '
        if fmt == 'none':
            return ''
        def sub(m):
            k = int(m.group(1)) - 1
            n = c.get(k, lv.get(k, ('decimal', '', 1))[2])
            return fmt_num(n, lv.get(k, (fmt,))[0])
        return re.sub(r'%(\d)', sub, txt) + ' '

    def paragrafo(self, p):
        txt = self.texto(p)
        nome, num_est = self.estilo(p)
        np_ = p.find('w:pPr/w:numPr', NS)
        numid, ilvl = None, 0
        if np_ is not None:
            numid = attr(np_.find('w:numId', NS), 'val')
            ilvl = int(attr(np_.find('w:ilvl', NS), 'val') or 0)
        elif num_est:
            numid, ilvl = num_est[0], int(num_est[1] or 0)
        if not txt:
            return ''
        m = re.match(r'(?i)(heading|t[ií]tulo)\s*(\d)', nome)
        ol = attr(p.find('w:pPr/w:outlineLvl', NS), 'val')
        if m or nome.lower() in ('title', 'título', 'titulo') or (ol is not None and ol.isdigit() and int(ol) < 6):
            nivel = int(m.group(2)) if m else (int(ol) + 1 if ol is not None and ol.isdigit() else 1)
            rot = self.rotulo(numid, ilvl) if numid else ''
            t = ((rot or '').replace('- ', '') + txt).strip()
            # dentro de tabela, titulo vira negrito (markdown nao aceita # numa celula)
            return '**' + t.replace('**', '') + '**' if self.em_tabela else '#' * min(nivel + 1, 6) + ' ' + t
        if numid:
            rot = self.rotulo(numid, ilvl)
            if rot is not None:
                return '  ' * ilvl + (rot if rot.startswith('-') else '- ' + rot if rot else '- ') + txt
        runs = [r for r in p.iter(w('r')) if ''.join(x.text or '' for x in r.findall('w:t', NS)).strip()]
        if runs and len(txt) <= 150 and all(
                r.find('w:rPr/w:b', NS) is not None and attr(r.find('w:rPr/w:b', NS), 'val') not in ('0', 'false') for r in runs):
            return '**' + txt.replace('**', '') + '**'
        return txt

    def tabela(self, tbl):
        linhas = []
        self.em_tabela += 1
        for tr in tbl.findall('w:tr', NS):
            cel = []
            for tc in tr.findall('w:tc', NS):
                partes = [x for x in self.blocos(tc) if x.strip()]
                cel.append('<br>'.join(re.sub(r'\s*\n\s*', '<br>', x) for x in partes).replace('|', '\\|'))
            if any(c.strip() for c in cel):
                linhas.append(cel)
        self.em_tabela -= 1
        if not linhas:
            return ''
        n = max(len(l) for l in linhas)
        if n == 1:
            return '\n\n'.join(l[0] for l in linhas)
        linhas = [l + [''] * (n - len(l)) for l in linhas]
        out = ['| ' + ' | '.join(linhas[0]) + ' |', '|' + '---|' * n]
        out += ['| ' + ' | '.join(l) + ' |' for l in linhas[1:]]
        return '\n'.join(out)

    def blocos(self, el):
        out = []
        for ch in el:
            if ch.tag == w('p'):
                out.append(self.paragrafo(ch))
            elif ch.tag == w('tbl'):
                out.append(self.tabela(ch))
            elif ch.tag in (w('sdt'), w('sdtContent'), w('customXml'), w('ins')):
                out += self.blocos(ch.find('w:sdtContent', NS) if ch.tag == w('sdt') else ch)
        return out

    def markdown(self):
        partes = []
        if self.cabecalho:
            partes.append('> **Cabeçalho do original:** ' + ' / '.join(self.cabecalho))
        corpo = [b for b in self.blocos(self.doc.find('w:body', NS)) if b.strip()]
        # itens de lista consecutivos ficam juntos; demais blocos separados por linha em branco
        txt = ''
        for b in corpo:
            lista = b.lstrip().startswith('- ')
            txt += ('\n' if lista and txt.endswith('\x00') else '\n\n') + b + ('\x00' if lista else '')
        partes.append(txt.replace('\x00', '').strip())
        # notas na ordem em que aparecem no texto; as sem referencia no corpo vao por ultimo
        ordem = list(dict.fromkeys(self.refs)) + [i for i in self.notas if i not in self.refs and self.notas[i]]
        if ordem:
            partes.append('\n'.join('[^%s]: %s' % (i, self.notas[i]) for i in ordem))
        return '\n\n'.join(p for p in partes if p)


def doc_texto(path):
    """Texto do corpo de um .doc (Word 97-2003) pela tabela de pecas (CLX) do FIB (sem antiword/Word)."""
    ole = olefile.OleFileIO(lp(path))
    wd = ole.openstream('WordDocument').read()
    flags = struct.unpack_from('<H', wd, 0x0A)[0]
    if flags & 0x0100:
        raise ValueError('documento criptografado')
    tbl = ole.openstream('1Table' if flags & 0x0200 else '0Table').read()
    ccp_text = struct.unpack_from('<i', wd, 0x004C)[0]  # caracteres do corpo principal
    fc_clx, lcb_clx = struct.unpack_from('<II', wd, 0x01A2)
    clx = tbl[fc_clx:fc_clx + lcb_clx]
    i = 0
    while clx[i] == 0x01:  # Prc (propriedades): pular
        i += 3 + struct.unpack_from('<H', clx, i + 1)[0]
    if clx[i] != 0x02:
        raise ValueError('CLX sem Pcdt')
    lcb = struct.unpack_from('<I', clx, i + 1)[0]
    plc = clx[i + 5:i + 5 + lcb]
    n = (lcb - 4) // 12
    cps = struct.unpack_from('<%dI' % (n + 1), plc, 0)
    out = []
    for k in range(n):
        if cps[k] >= ccp_text:
            break
        fc = struct.unpack_from('<I', plc, 4 * (n + 1) + 8 * k + 2)[0]
        nch = min(cps[k + 1], ccp_text) - cps[k]
        if fc & 0x40000000:  # peca comprimida: cp1252, 1 byte por caractere
            ini = (fc & 0x3FFFFFFF) // 2
            out.append(wd[ini:ini + nch].decode('cp1252', 'replace'))
        else:
            out.append(wd[fc:fc + 2 * nch].decode('utf-16-le', 'replace'))
    ole.close()
    t = ''.join(out)
    # campos: \x13 instrucao \x14 resultado \x15 -> fica so o resultado
    t = re.sub(r'\x13[^\x13\x14\x15]*\x14', '', t)
    t = re.sub(r'\x13[^\x13\x14\x15]*\x15', '', t)
    t = t.replace('\x15', '').replace('\x07', '\t')  # \x07: fim de celula/linha de tabela
    t = t.replace('\x0b', '\n').replace('\x0c', '\n').replace('\r', '\n')
    t = re.sub(r'[\x00-\x08\x0e-\x1f]', '', t)
    t = t.replace(' ', ' ').replace(' ', ' ').replace('\xa0', ' ')
    linhas = [re.sub(r'[ \t]+', ' ', l).strip() for l in t.split('\n')]
    return '\n\n'.join(l for l in linhas if l)


def valor(v):
    if v is None:
        return ''
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    if isinstance(v, datetime.datetime):
        v = v.date() if v.time() == datetime.time() else v
    if isinstance(v, (datetime.date, datetime.datetime)):
        v = v.isoformat()
    return re.sub(r'\s*\n\s*', '<br>', str(v).strip()).replace('|', '\\|')


def xlsx_md(path):
    wb = openpyxl.load_workbook(lp(path), data_only=True)
    partes = []
    for ws in wb.worksheets:
        linhas = [[valor(v) for v in r] for r in ws.iter_rows(values_only=True)]
        linhas = [l for l in linhas if any(l)]
        oculta = ' (oculta)' if ws.sheet_state != 'visible' else ''
        if not linhas:
            partes.append(f'## Planilha: {ws.title}{oculta}\n\n*(vazia)*')
            continue
        usadas = [j for j in range(max(len(l) for l in linhas)) if any(j < len(l) and l[j] for l in linhas)]
        linhas = [[l[j] if j < len(l) else '' for j in usadas] for l in linhas]
        n = len(usadas)
        tab = ['| ' + ' | '.join(linhas[0]) + ' |', '|' + '---|' * n] + ['| ' + ' | '.join(l) + ' |' for l in linhas[1:]]
        partes.append(f'## Planilha: {ws.title}{oculta}\n\n' + '\n'.join(tab))
    n = len(wb.worksheets)
    wb.close()
    return '\n\n'.join(partes), n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('lista')
    ap.add_argument('--log', default=LOG)
    ap.add_argument('--saida-dir', help='grava os .md nesta pasta (teste), em vez de ao lado do original')
    a = ap.parse_args()
    rows = list(csv.DictReader(open(a.lista, encoding='utf-8-sig')))
    novo = not os.path.exists(a.log)
    lg = open(a.log, 'a', encoding='utf-8-sig' if novo else 'utf-8', newline='')
    wr = csv.writer(lg)
    if novo:
        wr.writerow(['quando', 'status', 'metodo', 'paginas', 'caracteres', 'pdf', 'md'])
    for r in rows:
        orig = r['CaminhoArquivo']
        ext = os.path.splitext(orig)[1].lower()
        if ext not in ('.docx', '.xlsx', '.doc'):
            continue
        dest = os.path.splitext(orig)[0] + '.md'
        if a.saida_dir:
            dest = os.path.join(a.saida_dir, os.path.basename(dest))
        quando = datetime.datetime.now().isoformat(timespec='seconds')
        try:
            if os.path.exists(lp(dest)):
                wr.writerow([quando, 'IGNORADO_MD_JA_EXISTE', '', '', '', orig, dest])
                continue
            if ext == '.docx':
                d = Docx(orig)
                md = d.markdown()
                metodo = 'docx (python-docx/lxml: paragrafos, tabelas, listas, notas)'
                if d.imagens:
                    metodo += f'; {d.imagens} imagem(ns) sem texto'
                extra = ''
            elif ext == '.doc':
                md = doc_texto(orig)
                metodo = 'doc (olefile: texto da tabela de pecas; sem titulos/listas)'
                extra = ''
            else:
                md, n = xlsx_md(orig)
                metodo = 'xlsx (openpyxl, valores calculados)'
                extra = f'planilhas: {n}\n'
            md = re.sub(r'\n{3,}', '\n\n', md).strip()
            fm = ('---\n'
                  f'arquivo_original: "{os.path.basename(orig)}"\n'
                  f'hash_arquivo_md5: {md5(orig)}\n'
                  f'formato: {ext[1:]}\n' + extra +
                  f'metodo: "{metodo}"\n'
                  f'convertido_em: {quando}\n'
                  'fonte: Base de Conhecimento CLC\n'
                  '---\n\n')
            with open(lp(dest), 'w', encoding='utf-8', newline='\n') as f:
                f.write(fm + md + '\n')
            wr.writerow([quando, 'OK', metodo, '', len(md), orig, dest])
            print('OK', len(md), os.path.basename(dest))
        except Exception as e:
            wr.writerow([quando, 'ERRO: ' + str(e)[:80], '', '', '', orig, dest])
            print('ERRO', e, os.path.basename(orig))
        lg.flush()
    lg.close()


if __name__ == '__main__':
    main()
