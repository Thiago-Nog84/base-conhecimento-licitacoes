# Gera o indice por fase da contratacao a partir de mapa_indice.py.
# Uso:  python gerar_indice_por_fase.py             -> so confere (relatorio)
#       python gerar_indice_por_fase.py --lista     -> confere e lista os caminhos resolvidos
#       python gerar_indice_por_fase.py --escrever  -> grava o RASCUNHO fora da base (so se nao houver pendencias)
#       python gerar_indice_por_fase.py --aplicar   -> grava o indice vigente na RAIZ DA MESTRA; recusa se ja existir
#       python gerar_indice_por_fase.py --aplicar --substituir -> troca na mestra E no clone, cada um com backup (so com autorizacao)
# Cada padrao do mapa precisa casar com exatamente um .md do clone (versionado ou so local)
# e o arquivo precisa existir na pasta mestra e no clone; senao, nada e gravado.
# O indice vai primeiro para a mestra e chega ao clone por ferramentas/carregar_repo.py.
import sys, os, subprocess, unicodedata, shutil, datetime
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from mapa_indice import GRUPOS, SECOES, TRANSVERSAL, POR_OBJETO

MESTRA = Path(r"C:\Users\thiagonogueira\OneDrive - mppi.mp.br\CLC\01_Processos_e_Aquisicoes\Base de Conhecimento - Thiago")
CLONE = AQUI.parents[2]
NOME_INDICE = "00_Indice_por_Fase_da_Contratacao.md"
RASCUNHO = Path(r"C:\Users\thiagonogueira\Claude\proposta_indice_por_fase.md")
BACKUP = Path(r"C:\Users\thiagonogueira\Claude\backup_md\indice")
# Os links sao relativos a raiz da mestra, onde o indice fica
DATA = "2026-10-05"
APLICAR = "--aplicar" in sys.argv
SUBSTITUIR = "--substituir" in sys.argv
ESCREVER = "--escrever" in sys.argv or APLICAR

def nfc(s): return unicodedata.normalize("NFC", s)
def lp(p): return chr(92) * 2 + "?" + chr(92) + str(p)

def git_lista(*args):
    r = subprocess.run(["git", "-c", "core.quotepath=false", *args], cwd=CLONE,
                       capture_output=True, text=True, encoding="utf-8", check=True)
    return [nfc(l.strip()) for l in r.stdout.splitlines() if l.strip()]

versionados = git_lista("ls-files", "*.md")
locais = git_lista("ls-files", "--others", "--ignored", "--exclude-standard", "*.md")
TODOS = versionados + locais
SO_LOCAL = set(locais)

problemas, faltando, usados, contagem, out = [], [], {}, {}, []

def resolver(padrao, contexto):
    achados = [c for c in TODOS if nfc(padrao) in c]
    if len(achados) != 1:
        problemas.append((contexto, padrao, achados))
        return None
    usados.setdefault(achados[0], []).append(contexto)
    return achados[0]

def existe(raiz, rel):
    return os.path.exists(lp(raiz / rel.replace("/", "\\")))

def link(padrao, desc, contexto):
    c = resolver(padrao, contexto)
    if c is None:
        return None
    for nome, raiz in (("mestra", MESTRA), ("clone", CLONE)):
        if not existe(raiz, c):
            faltando.append((nome, c))
    marca = " *(só local)*" if c in SO_LOCAL else ""
    return f"- [{desc}](<@@{c}>){marca}"

def bloco(titulo, itens, contexto, nivel="###"):
    linhas = [l for l in (link(p, d, contexto) for p, d in itens) if l]
    if linhas:
        out.extend([f"{nivel} {titulo}\n", *linhas, ""])
    return len(linhas)

for s in SECOES:
    ctx = f"seção {s['id']}"
    out.append(f'<a id="fase-{s["id"]}"></a>\n\n## {s["id"]}. {s["titulo"]}\n')
    out.append(f"**Lei 14.133:** {s['artigos']}\n")
    n = 0
    for g in "NMDJ":
        n += bloco(GRUPOS[g], s["itens"].get(g, []), ctx)
        if g == "N" and s.get("transicao"):
            n += bloco("Regras de transição (Piauí)", s["transicao"], ctx, "####")
        if g == "M" and s.get("pge"):
            n += bloco("Listas de verificação da PGE-PI", s["pge"], ctx, "####")
    if s["lacunas"]:
        out.append("> **Lacunas:** " + " ".join(s["lacunas"]) + "\n")
    contagem[s["id"]] = n

for sec in (TRANSVERSAL, POR_OBJETO):
    out.append(f"## {sec['titulo']}\n")
    for nome, itens in sec["blocos"]:
        contagem[f"{sec['titulo']} / {nome}"] = bloco(nome, itens, sec["titulo"])

# ---------- relatorio ----------
print(f"Arquivos distintos ligados: {len(usados)} (só locais: {len(SO_LOCAL & set(usados))})")
for ctx, pad, ach in problemas:
    print(f"[{'SEM CASAMENTO' if not ach else 'AMBÍGUO'}] {ctx} :: {pad}")
    for a in ach[:8]:
        print("     ", a)
for onde, c in faltando:
    print(f"[NÃO EXISTE NA {onde.upper()}] {c}")
for c, v in usados.items():
    if len(v) > 1:
        print(f"[REPETIDO] {c} <- {v}")
for k, n in contagem.items():
    print(f"  {n:3d}  {k}")
if "--lista" in sys.argv:
    for c in sorted(usados):
        print("L|", c)
if not ESCREVER:
    sys.exit(0)
if problemas or faltando:
    print("Há pendências; nada foi gravado.")
    sys.exit(1)

# ---------- documento ----------
n_local = len(SO_LOCAL & set(usados))
tabela = ["| Seção | Lei 14.133 | Links |", "|---|---|---|"]
for s in SECOES:
    tabela.append(f"| [{s['id']}. {s['titulo']}](#fase-{s['id']}) | {s['artigos'].split(';')[0]} | {contagem[s['id']]} |")
n_transv = len(TRANSVERSAL["blocos"]); n_obj = len(POR_OBJETO["blocos"])

if APLICAR:
    topo = f"""---
titulo: "Índice por fase da contratação"
tipo: "Índice"
assunto: "Mapa dos arquivos da base por fase da contratação, com a Lei 14.133/2021 como eixo"
status: "vigente"
gerado_em: {DATA}
gerado_por: "docs/controle/indice/gerar_indice_por_fase.py"
tags: [indice, fases, navegacao]
---

# Índice por fase da contratação

> Este arquivo é gerado por script. Para mudá-lo, corrija o `mapa_indice.py` (em `docs/controle/indice/`) e gere de novo, em vez de editar aqui. Os links são relativos à raiz da base.
"""
else:
    topo = f"""---
titulo: "Índice por fase da contratação"
status: "PROPOSTA — não aplicada à base"
gerado_em: {DATA}
gerado_por: "docs/controle/indice/gerar_indice_por_fase.py"
---

# Índice por fase da contratação — PROPOSTA

> **Rascunho para aprovação.** O índice ainda não foi aplicado à base. O local proposto é `{NOME_INDICE}`, na raiz da pasta mestra. Este arquivo é gerado por script: corrija o `mapa_indice.py` e gere de novo, em vez de editar aqui.
"""

cab = f"""{topo}
## Como usar

- Ache a fase em que o processo está e consulte, nesta ordem: **normas, modelos e roteiros, manuais, jurisprudência**.
- A **base legal comum** (seção 0) vale para todas as fases e não se repete nelas.
- Cada arquivo aparece numa só seção, a do uso principal. O Ato PGJ 1.382/2024, por exemplo, está na seção 0, mas rege todas as fases.
- *(só local)* marca uma obra licenciada: o `.md` existe na pasta mestra e no clone, mas não vai para o GitHub.
- Cada descrição foi conferida no **corpo** do arquivo, não no front-matter, que tem erros conhecidos (Apêndice A).
- Arquivos com conteúdo trocado, duplicados ou fora do escopo ficaram de fora de propósito (Apêndices A e C).

**Números:** {len(usados)} arquivos ligados ({n_local} só locais), em {len(SECOES)} seções por fase, {n_transv} temas transversais e {n_obj} tipos de objeto.

## Mapa rápido

{chr(10).join(tabela)}

Mais: [Temas transversais](#temas-transversais) · [Por tipo de objeto](#por-tipo-de-objeto) · [Apêndices](#apêndice-a--pontos-de-atenção-na-base)

"""
apendices = (AQUI / "apendices_proposta.md").read_text(encoding="utf-8")
if APLICAR:
    # o Apêndice D (decisões para aprovar) é só da proposta
    apendices = apendices.split("\n## Apêndice D")[0].rstrip("\n") + "\n"
corpo = "\n".join(out)
texto = (cab + corpo + "\n" + apendices).replace("<@@", "<")

if APLICAR:
    destino = MESTRA / NOME_INDICE
    no_clone = CLONE / NOME_INDICE
    if os.path.exists(lp(destino)) and not SUBSTITUIR:
        print(f"{destino} já existe; nada foi gravado. Use --substituir (com autorização) para trocar, com backup.")
        sys.exit(1)
    selo = f"{datetime.datetime.now():%Y%m%d_%H%M%S}"
    # A carga (carregar_repo.py) nao sobrescreve; por isso, na troca, grava-se na mestra e no clone, cada um com backup
    alvos = [destino] + ([no_clone] if SUBSTITUIR and os.path.exists(lp(no_clone)) else [])
    for alvo in alvos:
        if os.path.exists(lp(alvo)):
            BACKUP.mkdir(parents=True, exist_ok=True)
            onde = "mestra" if alvo == destino else "clone"
            copia = BACKUP / f"{selo}_{onde}_{NOME_INDICE}"
            shutil.copy2(lp(alvo), lp(copia))
            print(f"Backup: {copia}")
        with open(lp(alvo), "w", encoding="utf-8", newline="\n") as f:
            f.write(texto)
        print(f"Gravado: {alvo} ({os.path.getsize(lp(alvo))} bytes)")
    if len(alvos) == 1:
        print("Falta levar ao clone: rode ferramentas/carregar_repo.py.")
else:
    with open(RASCUNHO, "w", encoding="utf-8", newline="\n") as f:
        f.write(texto)
    print(f"Gravado: {RASCUNHO} ({RASCUNHO.stat().st_size} bytes)")
