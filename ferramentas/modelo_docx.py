"""Gera um modelo .docx a partir de um documento real, trocando dados do caso por marcadores.
Uso: python modelo_docx.py <original.docx> <modelo.docx> <regras.py>
regras.py define REGRAS = [(rotulo, regex, substituicao), ...] (mesmo formato de anonimizar_md.py).
A troca e feita no XML (document, cabecalhos, rodapes, notas), por paragrafo: um trecho dividido em varios
runs e substituido no primeiro run e removido dos demais, preservando a formatacao do restante.
Autor e "modificado por" dos metadados (docProps/core.xml) sao apagados. O original nao e alterado.
Nunca sobrescreve o modelo. Imprime as contagens por regra e os padroes que nao foram encontrados.
"""
import os, re, sys, zipfile, runpy
from lxml import etree

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
XS = '{http://www.w3.org/XML/1998/namespace}space'


def lp(p):
    p = os.path.normpath(p)
    return p if p.startswith('\\\\?\\') else '\\\\?\\' + p


def substituir(p, regras, cont):
    ts = list(p.iter('{%s}t' % W))
    if not ts:
        return
    for rot, rx, sub in regras:
        desde = 0
        while True:
            texto = ''.join(t.text or '' for t in ts)
            m = re.compile(rx).search(texto, desde)
            if not m:
                break
            novo, (a, b) = m.expand(sub), m.span()
            pos, feito = 0, False
            for t in ts:
                s = t.text or ''
                t0, t1 = pos, pos + len(s)
                pos = t1
                if t1 <= a or t0 >= b:
                    continue
                lo, hi = max(a, t0) - t0, min(b, t1) - t0
                t.text = s[:lo] + (novo if not feito else '') + s[hi:]
                t.set(XS, 'preserve')
                feito = True
            desde = a + len(novo)
            cont[rot] = cont.get(rot, 0) + 1


def main():
    orig, dest, regras_py = sys.argv[1:4]
    regras = runpy.run_path(regras_py)['REGRAS']
    if os.path.exists(lp(dest)):
        sys.exit('modelo ja existe: ' + dest)
    cont = {}
    zin = zipfile.ZipFile(lp(orig))
    with zipfile.ZipFile(lp(dest), 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            dados = zin.read(item.filename)
            if re.match(r'word/(document|header\d*|footer\d*|footnotes|endnotes)\.xml$', item.filename):
                raiz = etree.fromstring(dados)
                for p in raiz.iter('{%s}p' % W):
                    substituir(p, regras, cont)
                dados = etree.tostring(raiz, xml_declaration=True, encoding='UTF-8', standalone=True)
            elif item.filename == 'docProps/core.xml':
                raiz = etree.fromstring(dados)
                for el in raiz:
                    if etree.QName(el).localname in ('creator', 'lastModifiedBy'):
                        el.text = ''
                dados = etree.tostring(raiz, xml_declaration=True, encoding='UTF-8', standalone=True)
            zout.writestr(item, dados)
    zin.close()
    for rot, rx, sub in regras:
        print('%3d  %s' % (cont.get(rot, 0), rot))
    faltando = [rot for rot, rx, sub in regras if not cont.get(rot)]
    if faltando:
        print('SEM OCORRENCIA:', faltando)


if __name__ == '__main__':
    main()
