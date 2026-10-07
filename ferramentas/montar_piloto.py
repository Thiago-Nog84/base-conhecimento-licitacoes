import csv, os, collections

BASE = r'C:\Users\thiagonogueira\Claude'
rows = [r for r in csv.DictReader(open(os.path.join(BASE, 'comparacao_conteudo_pdf_md.csv'), encoding='utf-8-sig'))
        if r['Classe'] == 'DISTINTO' and r['Tipo'] == 'TEXTO' and r['OCR'] == 'nao']
por_pasta = collections.defaultdict(list)
for r in rows:
    por_pasta[r['Pasta']].append(r)
sel = []
while len(sel) < 20 and any(por_pasta.values()):
    for p in list(por_pasta):
        if por_pasta[p] and len(sel) < 20:
            sel.append(por_pasta[p].pop(0))
with open(os.path.join(BASE, 'lista_piloto.csv'), 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(sel[0]))
    w.writeheader()
    w.writerows(sel)
print(len(sel), 'PDFs;', len(por_pasta), 'pastas')
for r in sel:
    print(r['Paginas'], '|', r['Pasta'][-35:], '|', r['PDF'][:60])
