"""Monta os lotes de conversao com os PDFs que ainda nao tem .md.
Exclui: pares ja copiados (plano OK), piloto (log_conversao OK), infograficos e PDFs que ja tem .md ao lado.
Ordem: PDFs com texto primeiro, depois os que precisam de OCR. Saida em lotes\\ (lista_completa.csv e lote_NN.csv).
"""
import csv, os
import pymupdf

BASE = r'C:\Users\thiagonogueira\Claude'
SAIDA = os.path.join(BASE, 'lotes')
TAM = 50
ORDEM = {'DISTINTO': 0, 'PROVAVEL_REVISAR': 1, 'IGUAL': 2, 'SEM_TEXTO_SUFICIENTE': 3}


def lp(p):
    p = os.path.normpath(p)
    return p if p.startswith('\\\\?\\') else '\\\\?\\' + p


def rd(nome):
    return list(csv.DictReader(open(os.path.join(BASE, nome), encoding='utf-8-sig')))


def eh_infografico(pdf):
    if 'infograficos_zenite' in pdf.lower():
        return True
    doc = pymupdf.open(lp(pdf))
    r = doc[0].rect if doc.page_count == 1 else None
    doc.close()
    return bool(r) and r.height > 3 * r.width


norm = lambda p: os.path.normpath(p).lower()
feitos = {norm(r['MD_Destino'][:-2] + 'pdf') for r in rd('plano_copia_md_pares_iguais.csv') if r['Status'] == 'OK'}
feitos |= {norm(r['pdf']) for r in rd('log_conversao.csv') if r['status'] == 'OK'}

sel, fora = [], []
for r in rd('comparacao_conteudo_pdf_md.csv'):
    pdf = r['CaminhoPDF']
    if norm(pdf) in feitos:
        continue
    try:
        if os.path.exists(lp(pdf[:-4] + '.md')):
            fora.append(('JA_TEM_MD', pdf))
        elif eh_infografico(pdf):
            fora.append(('INFOGRAFICO', pdf))
        else:
            sel.append(r)
    except Exception as e:
        fora.append(('ERRO: ' + str(e)[:60], pdf))

sel.sort(key=lambda r: (r['OCR'] == 'sim', ORDEM.get(r['Classe'], 9), r['Pasta'], r['PDF']))
os.makedirs(SAIDA, exist_ok=True)
campos = ['Lote'] + list(sel[0])
for i, r in enumerate(sel):
    r['Lote'] = f'{i // TAM + 1:02d}'
with open(os.path.join(SAIDA, 'lista_completa.csv'), 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=campos)
    w.writeheader()
    w.writerows(sel)
for lote in sorted({r['Lote'] for r in sel}):
    with open(os.path.join(SAIDA, f'lote_{lote}.csv'), 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        w.writerows(r for r in sel if r['Lote'] == lote)
with open(os.path.join(SAIDA, 'fora_dos_lotes.csv'), 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(['motivo', 'pdf'])
    w.writerows(fora)

print(len(sel), 'PDFs em', len({r['Lote'] for r in sel}), 'lotes;', len(fora), 'fora')
for m, p in fora:
    print('  fora:', m, '|', os.path.basename(p)[:80])
for lote in sorted({r['Lote'] for r in sel}):
    g = [r for r in sel if r['Lote'] == lote]
    print(f"lote {lote}: {len(g):3} PDFs, {sum(int(r['Paginas'] or 0) for r in g):5} pags, OCR={sum(r['OCR'] == 'sim' for r in g)}")
