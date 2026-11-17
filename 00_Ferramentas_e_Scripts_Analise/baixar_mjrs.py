"""
Download das MJRs — Base Legal CLC / MPPI
==========================================
Acessa cada página das MJRs no site do MPPI, localiza o link do PDF
e salva na pasta Normativos MPPI.

Uso:
    python baixar_mjrs.py
"""

import os, re, time
import requests

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
DEST_DIR  = os.path.join(BASE_DIR, "Normativos MPPI")
os.makedirs(DEST_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Referer": "https://www.mppi.mp.br/",
}

MJRS = [
    {
        "nome": "MJR n92 - 2024 - Contratação Direta (Dispensa Art 75 I e II)",
        "pagina": "https://www.mppi.mp.br/internet/coordenadoria-de-licitacoes-e-contratos/mjr/?sub=dispensa",
    },
    {
        "nome": "MJR n95 - 2025 - Prorrogação de Vigência de ARP",
        "pagina": "https://www.mppi.mp.br/internet/coordenadoria-de-licitacoes-e-contratos/mjr/?sub=prorrogacao-de-vigencia-arp",
    },
    {
        "nome": "MJR n86 - 2025 - Adesão à Ata de Registro de Preços (Carona)",
        "pagina": "https://www.mppi.mp.br/internet/coordenadoria-de-licitacoes-e-contratos/mjr/?sub=adesao-carona",
    },
    {
        "nome": "MJR n66 - 2025 - Pagamento por Indenização (Art 149)",
        "pagina": "https://www.mppi.mp.br/internet/coordenadoria-de-licitacoes-e-contratos/mjr/?sub=pagamento-por-indenizacao",
    },
    {
        "nome": "MJR n56 - 2025 - Substituição de Marca",
        "pagina": "https://www.mppi.mp.br/internet/coordenadoria-de-licitacoes-e-contratos/mjr/?sub=coordenadoria-de-tecnologia-da-informacao-cti",
    },
]


def encontrar_pdf_na_pagina(url: str, session: requests.Session) -> list[str]:
    """Busca links de PDF na página, incluindo dentro de Google Docs viewer."""
    try:
        r = session.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()
        html = r.text

        urls_pdf = []

        # PDFs diretos
        for m in re.finditer(r'href=["\']([^"\']+\.pdf)["\']', html, re.IGNORECASE):
            href = m.group(1)
            if href.startswith("http"):
                urls_pdf.append(href)
            else:
                from urllib.parse import urljoin
                urls_pdf.append(urljoin(url, href))

        # PDFs embutidos em Google Docs viewer
        for m in re.finditer(r'[?&]url=([^&"\']+\.pdf)', html, re.IGNORECASE):
            from urllib.parse import unquote
            urls_pdf.append(unquote(m.group(1)))

        # src de iframes com PDF
        for m in re.finditer(r'src=["\']([^"\']+\.pdf)["\']', html, re.IGNORECASE):
            href = m.group(1)
            if href.startswith("http"):
                urls_pdf.append(href)

        return list(dict.fromkeys(urls_pdf))  # deduplicar mantendo ordem

    except Exception as e:
        print(f"    ✗ Erro ao acessar página: {e}")
        return []


def baixar(url: str, destino: str, session: requests.Session) -> bool:
    try:
        r = session.get(url, headers=HEADERS, timeout=30, stream=True)
        r.raise_for_status()
        ct = r.headers.get("Content-Type", "")
        if "pdf" not in ct.lower() and "octet" not in ct.lower():
            print(f"    ⚠  Não é PDF (Content-Type: {ct}): {url}")
            return False
        with open(destino, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
        kb = os.path.getsize(destino) / 1024
        if kb < 5:
            os.remove(destino)
            print(f"    ⚠  Arquivo muito pequeno ({kb:.1f} KB), ignorado")
            return False
        print(f"    ✓  Salvo ({kb:.1f} KB): {os.path.basename(destino)}")
        return True
    except Exception as e:
        print(f"    ✗  Falha no download: {e}")
        return False


def main():
    print("=" * 60)
    print("  Download das MJRs — CLC / MPPI")
    print("=" * 60)

    session = requests.Session()
    baixados = 0
    falhas   = []

    for mjr in MJRS:
        print(f"\n▶ {mjr['nome']}")
        print(f"  Página: {mjr['pagina']}")

        # Verificar se já existe
        destino = os.path.join(DEST_DIR, mjr["nome"] + ".pdf")
        if os.path.exists(destino) and os.path.getsize(destino) > 5000:
            print(f"  –  Já existe, pulando.")
            continue

        # Buscar PDFs na página
        pdfs = encontrar_pdf_na_pagina(mjr["pagina"], session)

        if not pdfs:
            print(f"  ⚠  Nenhum PDF encontrado na página.")
            print(f"  →  Acesse manualmente: {mjr['pagina']}")
            falhas.append(mjr["nome"])
            time.sleep(1)
            continue

        print(f"  Links PDF encontrados: {len(pdfs)}")
        ok = False
        for url_pdf in pdfs:
            print(f"  Tentando: {url_pdf}")
            if baixar(url_pdf, destino, session):
                baixados += 1
                ok = True
                break
            time.sleep(1)

        if not ok:
            falhas.append(mjr["nome"])

        time.sleep(2)

    print("\n" + "=" * 60)
    print(f"  ✓  Baixados:  {baixados}")
    print(f"  ✗  Falhas:    {len(falhas)}")
    if falhas:
        print("\n  Baixe manualmente acessando as páginas acima:")
        for f in falhas:
            print(f"    • {f}")
        print(f"\n  Salve os PDFs em:")
        print(f"    {DEST_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
