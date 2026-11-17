"""
Script de Correção de Downloads — Base Legal CLC / MPPI
========================================================
Executa após o baixar_normativos.py para:
  1. Apagar arquivos inválidos (JSON de erro 404 disfarçados de PDF)
  2. Apagar INs Federais com conteúdo duplicado/genérico
  3. Baixar MJRs via Google Docs (extrai URL direta do PDF)
  4. Baixar leis/decretos do Planalto como HTML
  5. Gerar relatório de pendências manuais

Uso:
    python corrigir_downloads.py
"""

import os, re, hashlib, time
import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HEADERS  = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0"}
TIMEOUT  = 30

# ── 1. Arquivos inválidos (0.4 KB / JSON de erro) ────────────────────────────

INVALIDOS = [
    r"Normativos Estado do Piauí\DECRETO - n22.237 - 2023.pdf",
    r"Normativos Estado do Piauí\Decreto Estadual - n17.083032017 - 2017.pdf",
    r"Normativos Estado do Piauí\Decreto Estadual - n21.864062023 - 2023.pdf",
    r"Normativos Estado do Piauí\Decreto Estadual - n21.909172023 - 2023.pdf",
    r"Normativos Estado do Piauí\Decreto Estadual - n22.008242023 - 2023.pdf",
    r"Normativos Estado do Piauí\Decreto Estadual - n22.033282023 - 2023.pdf",
    r"Normativos Estado do Piauí\Decreto Estadual - n23.649122025 - 2025.pdf",
    r"Normativos Estado do Piauí\Decreto Estadual - n23.865022025 - 2025.pdf",
    r"Normativos Estado do Piauí\Lei Estadual - n6.782282016 - 2016.pdf",
]

# ── 2. INs Federais com conteúdo duplicado/genérico ──────────────────────────

INS_DUPLICADAS = [
    r"Normativos Federais\Instrução Normativa Federal - n5.0 - 2017.pdf",
    r"Normativos Federais\Instrução Normativa Federal - n58.0 - 2022.pdf",
    r"Normativos Federais\Instrução Normativa Federal - n65.0 - 2021.pdf",
    r"Normativos Federais\Instrução Normativa Federal - n67.0 - 2021.pdf",
    r"Normativos Federais\Instrução Normativa Federal - n75.0 - 2021.pdf",
    r"Normativos Federais\Instrução Normativa Federal - n81.0 - 2022.pdf",
    r"Normativos Federais\Instrução Normativa Federal - n91.0 - 2022.pdf",
    r"Normativos Federais\Instrução Normativa Federal - n103.0 - 2022.pdf",
]

# ── 3. Downloads corrigíveis ──────────────────────────────────────────────────

# MJRs via Google Docs Viewer → extrai URL direta do PDF
GOOGLE_DOCS = [
    {
        "gdocs_url": "https://docs.google.com/viewer?url=https://www.mppi.mp.br/internet/wp-content/uploads/2024/12/MANIFESTACAO-JURIDICA-REFERENCIAL-No-92-2024-CLC-APPL.pdf",
        "destino": r"Normativos MPPI\Manifestação Jurídico Referencial - MJR - n92 - 2024.pdf",
    },
    {
        "gdocs_url": "https://docs.google.com/viewer?url=https://www.mppi.mp.br/internet/wp-content/uploads/2025/09/MANIFESTACAO-JURIDICA-REFERENCIAL-No-86-2025-CLC-APPL-CONTRATACAO-POR-ADESAO.pdf",
        "destino": r"Normativos MPPI\Manifestação Jurídico Referencial - MJR - n86 - 2025.pdf",
    },
]

# Leis e Decretos do Planalto → salvar como HTML
PLANALTO_HTML = [
    {
        "url": "https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2021/lei/l14133.htm",
        "destino": r"Normativos Federais\Lei Federal - n14133 - 2021.html",
    },
    {
        "url": "https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp123.htm",
        "destino": r"Normativos Federais\Lei Complementar - n123 - 2006.html",
    },
    {
        "url": "https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2023/decreto/d11462.htm",
        "destino": r"Normativos Federais\Decreto Federal - n11462 - 2023.html",
    },
    {
        "url": "https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2021/decreto/d10818.htm",
        "destino": r"Normativos Federais\Decreto Federal - n10818 - 2021.html",
    },
    {
        "url": "https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2024/decreto/d12343.htm",
        "destino": r"Normativos Federais\Decreto Federal - n12343 - 2024.html",
    },
]

# ── 4. Pendências manuais (não automatizáveis) ────────────────────────────────

MANUAIS = [
    {
        "item": "Súmula TCU nº 247",
        "motivo": "Página de busca dinâmica — não tem PDF direto",
        "acao": "Acesse https://pesquisa.apps.tcu.gov.br e baixe manualmente",
    },
    {
        "item": "MJR nº 56/2025/CLC/APPL",
        "motivo": "HTTP 404 — arquivo removido do servidor do MPPI",
        "acao": "Solicite ao MPPI ou verifique se existe versão atualizada",
    },
    {
        "item": "INs Federais (65, 58, 67, 91, 75, 81, 103, 5, Portaria 8678)",
        "motivo": "compras.gov.br requer JavaScript para exibir o PDF real",
        "acao": "Acesse cada link do índice no navegador e baixe manualmente para a pasta 'Normativos Federais'",
    },
    {
        "item": "Decretos Estaduais do Piauí com erro 404 (9 arquivos)",
        "motivo": "Documentos removidos do Alfresco/PGE-PI",
        "acao": "Verifique se há versão atualizada no Diário Oficial do Piauí (www.diariooficial.pi.gov.br)",
    },
]


# ── Funções ───────────────────────────────────────────────────────────────────

def apagar(relativo: str, motivo: str):
    caminho = os.path.join(BASE_DIR, relativo)
    if os.path.exists(caminho):
        os.remove(caminho)
        print(f"  🗑  Apagado: {os.path.basename(caminho)}")
    else:
        print(f"  –  Não encontrado (já apagado?): {os.path.basename(caminho)}")


def extrair_url_google_docs(gdocs_url: str) -> str | None:
    """Extrai a URL real do PDF embutida no link do Google Docs Viewer."""
    m = re.search(r"[?&]url=([^&]+)", gdocs_url)
    if m:
        from urllib.parse import unquote
        return unquote(m.group(1))
    return None


def baixar_pdf(url: str, destino_rel: str, session: requests.Session) -> bool:
    destino = os.path.join(BASE_DIR, destino_rel)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    try:
        r = session.get(url, headers=HEADERS, timeout=TIMEOUT, stream=True)
        r.raise_for_status()
        with open(destino, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
        kb = os.path.getsize(destino) / 1024
        print(f"  ✓  Salvo ({kb:.1f} KB): {os.path.basename(destino)}")
        return True
    except Exception as e:
        print(f"  ✗  Falha: {e}")
        return False


def baixar_html(url: str, destino_rel: str, session: requests.Session) -> bool:
    destino = os.path.join(BASE_DIR, destino_rel)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    try:
        r = session.get(url, headers=HEADERS, timeout=TIMEOUT)
        r.raise_for_status()
        r.encoding = r.apparent_encoding or "utf-8"
        with open(destino, "w", encoding="utf-8") as f:
            f.write(r.text)
        kb = os.path.getsize(destino) / 1024
        print(f"  ✓  Salvo ({kb:.1f} KB): {os.path.basename(destino)}")
        return True
    except Exception as e:
        print(f"  ✗  Falha: {e}")
        return False


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    session = requests.Session()

    print("=" * 60)
    print("  Correção de Downloads — Base Legal CLC / MPPI")
    print("=" * 60)

    # 1. Apagar arquivos inválidos (JSON 404)
    print("\n[1/4] Apagando arquivos inválidos (erro 404 do servidor)...")
    for rel in INVALIDOS:
        apagar(rel, "JSON de erro 404")

    # 2. Apagar INs duplicadas/genéricas
    print("\n[2/4] Apagando INs Federais com conteúdo genérico...")
    for rel in INS_DUPLICADAS:
        apagar(rel, "Conteúdo genérico do portal")

    # 3. Baixar MJRs via URL direta extraída do Google Docs
    print("\n[3/4] Baixando MJRs (extraindo URL direta do Google Docs)...")
    for item in GOOGLE_DOCS:
        url_direta = extrair_url_google_docs(item["gdocs_url"])
        if url_direta:
            print(f"  → {os.path.basename(item['destino'])}")
            baixar_pdf(url_direta, item["destino"], session)
        else:
            print(f"  ✗  Não foi possível extrair URL: {item['gdocs_url']}")
        time.sleep(1.5)

    # 4. Baixar leis/decretos do Planalto como HTML
    print("\n[4/4] Baixando leis/decretos do Planalto como HTML...")
    for item in PLANALTO_HTML:
        print(f"  → {os.path.basename(item['destino'])}")
        baixar_html(item["url"], item["destino"], session)
        time.sleep(1.5)

    # 5. Relatório de pendências manuais
    print("\n" + "=" * 60)
    print("  ⚠  PENDÊNCIAS MANUAIS (requerem ação sua)")
    print("=" * 60)
    for p in MANUAIS:
        print(f"\n• {p['item']}")
        print(f"  Motivo: {p['motivo']}")
        print(f"  Ação:   {p['acao']}")

    print("\n" + "=" * 60)
    print("  Correção concluída.")
    print("=" * 60)


if __name__ == "__main__":
    main()
