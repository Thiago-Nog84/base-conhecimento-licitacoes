"""
Script de Download - Base Legal CLC / MPPI
===========================================
Baixa automaticamente os normativos catalogados no Levantamento de Normativos.xlsx
que ainda não possuem arquivo local na pasta da Base Legal.

Requisitos:
    pip install requests openpyxl

Uso:
    python baixar_normativos.py

Os arquivos serão salvos nas subpastas correspondentes da Base Legal.
"""

import os
import re
import time
import requests
from openpyxl import load_workbook

# ── Configuração ──────────────────────────────────────────────────────────────

# Pasta raiz da Base Legal (ajuste se necessário)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

EXCEL_PATH = os.path.join(BASE_DIR, "Levantamento de Normativos.xlsx")

# Mapeamento de âmbito → subpasta existente
PASTA_POR_AMBITO = {
    "federal":        "Normativos Federais",
    "estadual":       "Normativos Estado do Piauí",
    "estado do piauí":"Normativos Estado do Piauí",
    "mppi":           "Normativos MPPI",
    "tce/pi":         "Boletins de Jurisprudência TCE-PI",
    "tcepi":          "Boletins de Jurisprudência TCE-PI",
    "cnmp":           "Normativos CNMP",
    "tjpi":           "Normativos TJPI",
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

TIMEOUT = 30  # segundos por requisição
PAUSA   = 1.5 # segundos entre downloads (evita bloqueio)


# ── Funções auxiliares ────────────────────────────────────────────────────────

def sanitizar(texto: str) -> str:
    """Remove caracteres inválidos para nomes de arquivo."""
    texto = re.sub(r'[\\/*?:"<>|]', '', texto)
    return texto.strip()


def pasta_destino(ambito: str) -> str:
    """Retorna o caminho da subpasta de destino com base no âmbito."""
    chave = ambito.lower().strip()
    for k, v in PASTA_POR_AMBITO.items():
        if k in chave:
            pasta = os.path.join(BASE_DIR, v)
            os.makedirs(pasta, exist_ok=True)
            return pasta
    # Âmbito desconhecido → pasta genérica
    pasta = os.path.join(BASE_DIR, "Outros Normativos")
    os.makedirs(pasta, exist_ok=True)
    return pasta


def nome_arquivo(tipo: str, num: str, ano: str, url: str) -> str:
    """Gera nome de arquivo padronizado."""
    num_limpo = re.sub(r'[^\d.]', '', num) if num else ''
    partes = [sanitizar(tipo)]
    if num_limpo:
        partes.append(f"n{num_limpo}")
    if ano:
        partes.append(ano)
    nome_base = " - ".join(partes)

    # Extensão a partir da URL ou padrão PDF
    ext = ".pdf"
    url_lower = url.lower().split("?")[0]
    for possivel_ext in [".pdf", ".docx", ".doc", ".html", ".htm"]:
        if url_lower.endswith(possivel_ext):
            ext = possivel_ext
            break

    return nome_base + ext


def arquivo_ja_existe(pasta: str, tipo: str, num: str, ano: str) -> bool:
    """Verifica se já existe um arquivo com tipo+número+ano na pasta."""
    num_limpo = re.sub(r'[^\d]', '', num) if num else ''
    if not num_limpo or not ano:
        return False
    for arq in os.listdir(pasta):
        arq_c = re.sub(r'[.\-_/ ]', '', arq.lower())
        if num_limpo in arq_c and ano in arq_c:
            return True
    return False


def extrair_pdf_da_pagina(url: str, session: requests.Session) -> str | None:
    """
    Para URLs que são páginas HTML (não PDF direto), tenta encontrar
    um link de PDF dentro da página.
    """
    try:
        r = session.get(url, headers=HEADERS, timeout=TIMEOUT)
        if "text/html" not in r.headers.get("Content-Type", ""):
            return None
        # Procura links .pdf no HTML
        pdfs = re.findall(r'href=["\']([^"\']+\.pdf)["\']', r.text, re.IGNORECASE)
        if pdfs:
            candidato = pdfs[0]
            if candidato.startswith("http"):
                return candidato
            # URL relativa → montar absoluta
            from urllib.parse import urljoin
            return urljoin(url, candidato)
    except Exception:
        pass
    return None


def baixar(url: str, destino: str, session: requests.Session) -> bool:
    """Baixa um arquivo e salva em destino. Retorna True se bem-sucedido."""
    try:
        r = session.get(url, headers=HEADERS, timeout=TIMEOUT, stream=True)
        r.raise_for_status()

        content_type = r.headers.get("Content-Type", "")

        # Se retornou HTML em vez de PDF, tenta extrair link de PDF
        if "text/html" in content_type:
            pdf_url = extrair_pdf_da_pagina(url, session)
            if pdf_url:
                return baixar(pdf_url, destino, session)
            else:
                print(f"    ⚠  Página HTML sem PDF encontrado: {url}")
                return False

        with open(destino, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        return True

    except requests.exceptions.HTTPError as e:
        print(f"    ✗  HTTP {e.response.status_code}: {url}")
    except requests.exceptions.ConnectionError:
        print(f"    ✗  Falha de conexão: {url}")
    except requests.exceptions.Timeout:
        print(f"    ✗  Timeout: {url}")
    except Exception as e:
        print(f"    ✗  Erro inesperado: {e}")
    return False


# ── Leitura do Excel ──────────────────────────────────────────────────────────

def carregar_normativos() -> list[dict]:
    wb = load_workbook(EXCEL_PATH)
    normativos = []

    # Página1: A=Tipo, B=Âmbito, C=Nº, D=Ano, E=Descrição, F=Link
    ws1 = wb["Página1"]
    for row in ws1.iter_rows(min_row=2):
        tipo   = row[0].value
        ambito = row[1].value
        num    = row[2].value
        ano    = row[3].value
        cell_link = row[5]
        url = cell_link.hyperlink.target if cell_link.hyperlink else None
        if tipo and url:
            normativos.append({
                "tipo":   str(tipo).strip(),
                "ambito": str(ambito).strip() if ambito else "Federal",
                "num":    str(num).strip() if num else "",
                "ano":    str(int(float(ano))) if ano and str(ano) not in ("", "nan") else "",
                "url":    url,
            })

    # Página2: A=Tipo, B=Identificacao, C=Pub, D=Descrição, E=Tema, F=Link
    ws2 = wb["Página2"]
    for row in ws2.iter_rows(min_row=2):
        tipo  = row[0].value
        ident = row[1].value
        cell_link = row[5]
        url = cell_link.hyperlink.target if cell_link.hyperlink else None
        if tipo and url and ident:
            nums = re.search(r"(\d[\d.]*)", str(ident))
            anos = re.findall(r"\b((?:19|20)\d{2})\b", str(ident))
            normativos.append({
                "tipo":   str(tipo).strip(),
                "ambito": "Estado do Piauí",
                "num":    nums.group(1) if nums else "",
                "ano":    anos[-1] if anos else "",
                "url":    url,
            })

    return normativos


# ── Execução principal ────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  Download de Normativos — Base Legal CLC / MPPI")
    print("=" * 60)

    normativos = carregar_normativos()
    print(f"\n📋 {len(normativos)} normativos encontrados no índice.\n")

    session = requests.Session()
    session.headers.update(HEADERS)

    baixados  = 0
    ignorados = 0
    falhas    = 0

    for i, norm in enumerate(normativos, 1):
        pasta = pasta_destino(norm["ambito"])

        # Pula se já existe arquivo local
        if arquivo_ja_existe(pasta, norm["tipo"], norm["num"], norm["ano"]):
            ignorados += 1
            continue

        nome = nome_arquivo(norm["tipo"], norm["num"], norm["ano"], norm["url"])
        destino = os.path.join(pasta, nome)

        print(f"[{i:03d}/{len(normativos)}] {norm['tipo']} nº {norm['num']} ({norm['ano']})")
        print(f"        → {nome}")

        ok = baixar(norm["url"], destino, session)

        if ok:
            tamanho = os.path.getsize(destino) / 1024
            print(f"    ✓  Salvo ({tamanho:.1f} KB)")
            baixados += 1
        else:
            falhas += 1

        time.sleep(PAUSA)

    print("\n" + "=" * 60)
    print(f"  ✓  Baixados:  {baixados}")
    print(f"  –  Já existiam: {ignorados}")
    print(f"  ✗  Falhas:    {falhas}")
    print("=" * 60)


if __name__ == "__main__":
    main()
