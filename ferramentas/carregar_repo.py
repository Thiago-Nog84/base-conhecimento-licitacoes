"""Copia a mestra (OneDrive) para o clone do repositorio, mantendo a estrutura de pastas.
- .md: todos da mestra (exceto _DUPLICADOS_para_arquivar e os .md de origem ja copiados com o nome do PDF)
- .pdf: apenas os que tem .md equivalente (>90% pelo plano de copia + pares por nome)
- .docx/.xlsx convertidos (log_conversao) nao sao copiados: so o .md vai para o clone
Originais permanecem no OneDrive. Verificacao por hash. Log em log_carga_repo.csv.
"""
import csv, os, shutil, hashlib, collections

BASE = r'C:\Users\thiagonogueira\Claude'
ROOT = r'C:\Users\thiagonogueira\OneDrive - mppi.mp.br\CLC\01_Processos_e_Aquisicoes\Base de Conhecimento - Thiago'
REPO = r'C:\Users\thiagonogueira\Dev\base-conhecimento-licitacoes'


def lp(p):
    p = os.path.normpath(p)
    return p if p.startswith('\\\\?\\') else '\\\\?\\' + p


def md5(p):
    h = hashlib.md5()
    with open(lp(p), 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def rd(nome):
    return list(csv.DictReader(open(os.path.join(BASE, nome), encoding='utf-8-sig')))


origens_copiadas = {r['md_origem'].lower() for r in rd('log_copia_md.csv') if r['status'] == 'OK'}
pdf_set = {r['MD_Destino'][:-2] + 'pdf' for r in rd('plano_copia_md_pares_iguais.csv') if r['Status'] == 'OK'}
for r in rd('mapa_pares_pdf_md.csv'):
    if r['Status'] == 'PAR_MESMA_PASTA':
        pdf_set.add(r['CaminhoPDF'])
if os.path.exists(os.path.join(BASE, 'log_conversao.csv')):
    for r in rd('log_conversao.csv'):
        # a coluna 'pdf' guarda o original em qualquer formato; docx/xlsx nao vao para o clone
        if r['status'] == 'OK' and r['pdf'].lower().endswith('.pdf'):
            pdf_set.add(r['pdf'])

itens = []  # (tipo, origem)
for dp, dn, fn in os.walk(lp(ROOT)):
    dn[:] = [d for d in dn if d not in ('_DUPLICADOS_para_arquivar', '.vscode', '__pycache__', '.git')]
    for f in fn:
        p = os.path.join(dp, f).replace('\\\\?\\', '')
        if f.lower().endswith('.md') and p.lower() not in origens_copiadas:
            itens.append(('md', p))
pdf_ok = {os.path.normpath(p).lower() for p in pdf_set}
for p in pdf_set:
    itens.append(('pdf', os.path.normpath(p)))

cont = collections.Counter()
with open(os.path.join(BASE, 'log_carga_repo.csv'), 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.writer(f)
    w.writerow(['status', 'tipo', 'origem', 'destino'])
    for tipo, o in itens:
        rel = os.path.relpath(o, ROOT)
        d = os.path.join(REPO, rel)
        try:
            if not os.path.exists(lp(o)):
                st = 'ORIGEM_NAO_ENCONTRADA'
            elif os.path.exists(lp(d)):
                st = 'IGNORADO_JA_EXISTE'
            else:
                os.makedirs(lp(os.path.dirname(d)), exist_ok=True)
                shutil.copy2(lp(o), lp(d))
                st = 'OK' if md5(o) == md5(d) else 'ERRO_HASH'
        except Exception as e:
            st = 'ERRO: ' + str(e)[:80]
        cont[(tipo, st)] += 1
        w.writerow([st, tipo, o, d])
for k, v in sorted(cont.items()):
    print(k, v)
