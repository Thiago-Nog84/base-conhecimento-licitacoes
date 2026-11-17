#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════╗
║  Gerador de Ofício Consolidado — ASSCOMPRAS / MPPI          v1.0    ║
║  Coordenadoria de Licitações e Contratos                             ║
╚══════════════════════════════════════════════════════════════════════╝

Lê os arquivos JSON de achados gerados pelos scripts de análise
(analisar_dfd.py, analisar_etp.py, analisar_tr.py) e gera um único
Ofício ASSCOMPRAS consolidado com todos os achados do processo.

Ordem canônica dos artefatos no Ofício (fase preparatória):
    1. DFD — Documento de Formalização da Demanda
    2. DAP — Despacho de Abertura de Procedimento
    3. ETP — Estudo Técnico Preliminar
    4. MR  — Mapa de Riscos
    5. TR  — Termo de Referência
    6. PP  — Pesquisa de Preços e Mapa Comparativo de Preços

Uso:
    python gerar_oficio_processo.py achados_DFD_xxx.json achados_ETP_yyy.json
    python gerar_oficio_processo.py pasta/  (processa todos os achados_*.json da pasta)

O Ofício é salvo na mesma pasta do primeiro arquivo JSON informado.
"""

import sys
import os
import json
import re
from datetime import datetime
from pathlib import Path

VERSION = "1.0.0"
DATA_ANALISE = datetime.now().strftime("%d/%m/%Y")

# Ordem canônica de exibição dos artefatos no Ofício
# (sequência cronológica da fase preparatória da contratação)
_ORDEM_ARTEFATOS = ["DFD", "DAP", "ETP", "MR", "TR", "PP"]

# Rótulos amigáveis por artefato
_LABELS = {
    "DFD": "Documento de Formalização da Demanda (DFD)",
    "DAP": "Despacho de Abertura de Procedimento (DAP)",
    "ETP": "Estudo Técnico Preliminar (ETP)",
    "MR":  "Mapa de Riscos (MR)",
    "TR":  "Termo de Referência (TR)",
    "PP":  "Pesquisa de Preços e Mapa Comparativo de Preços (PP)",
}


def _erro(msg: str):
    print(f"\n❌ ERRO: {msg}\n", file=sys.stderr)
    sys.exit(1)


def carregar_jsons(caminhos: list) -> list:
    """Carrega e valida os arquivos JSON de achados."""
    pacotes = []
    for c in caminhos:
        if not os.path.isfile(c):
            _erro(f"Arquivo não encontrado: '{c}'")
        with open(c, encoding="utf-8") as f:
            try:
                dados = json.load(f)
            except json.JSONDecodeError as e:
                _erro(f"JSON inválido em '{c}': {e}")
        if "artefato" not in dados or "achados" not in dados:
            _erro(f"Formato inválido em '{c}'. Esperado: artefato + achados.")
        pacotes.append(dados)
    # Ordenar por ordem canônica de artefatos
    pacotes.sort(key=lambda p: _ORDEM_ARTEFATOS.index(p["artefato"])
                 if p["artefato"] in _ORDEM_ARTEFATOS else 99)
    return pacotes


def descobrir_jsons(pasta: str) -> list:
    """Descobre automaticamente todos os achados_*.json numa pasta."""
    p = Path(pasta)
    jsons = sorted(p.glob("achados_*.json"))
    if not jsons:
        _erro(f"Nenhum arquivo achados_*.json encontrado em '{pasta}'.")
    return [str(j) for j in jsons]


def _set_font(doc, nome="Times New Roman", tamanho=12):
    from docx.shared import Pt
    style = doc.styles["Normal"]
    style.font.name = nome
    style.font.size = Pt(tamanho)


def gerar_oficio_consolidado(pacotes: list, caminho_saida: str):
    try:
        from docx import Document
        from docx.shared import Pt, Cm
        from docx.enum.text import WD_ALIGN_PARAGRAPH
    except ImportError:
        _erro("python-docx não instalado. Execute: pip install python-docx")

    doc = Document()
    _set_font(doc, "Times New Roman", 12)
    section = doc.sections[0]
    section.top_margin    = Cm(3)
    section.bottom_margin = Cm(2)
    section.left_margin   = Cm(3)
    section.right_margin  = Cm(2)

    # Inferir dados do processo do primeiro pacote
    primeiro = pacotes[0]
    num_processo = primeiro.get("num_processo") or "[nº do processo SEI]"
    unidade      = primeiro.get("unidade")      or "[Unidade Requisitante]"
    objeto       = primeiro.get("objeto")       or ""
    is_tic       = any(p.get("is_tic", False) for p in pacotes)

    artefatos_str = ", ".join(
        _LABELS.get(p["artefato"], p["artefato"]) for p in pacotes
    )

    # ── Destinatário ─────────────────────────────────────────────────
    p = doc.add_paragraph()
    p.add_run(f"À {unidade}").bold = True
    p = doc.add_paragraph()
    p.add_run(
        f"Assunto: Devolução de Autos para Saneamento — "
        f"Análise de Conformidade da Fase de Planejamento — "
        f"Processo SEI nº {num_processo}."
    ).bold = True

    doc.add_paragraph()
    doc.add_paragraph().add_run("Senhor(a) Coordenador(a),")
    doc.add_paragraph()

    # ── Abertura ─────────────────────────────────────────────────────
    normativos = (
        "Lei nº 14.133/2021, Decreto Estadual (PI) nº 21.872/2023, "
        "IN SEGES/ME nº 58/2022, Atos PGJ/MPPI nº 1.381 e 1.382/2024"
        + (", Resolução CNMP nº 283/2024 e MOTec" if is_tic else "")
        + "."
    )

    for txt in [
        (
            f"Cumprimentando-o cordialmente, registro que a equipe desta Assessoria "
            f"procedeu à análise dos artefatos de planejamento da contratação juntados "
            f"aos autos do processo em referência ({artefatos_str}), verificando a "
            f"conformidade de cada documento com os normativos aplicáveis: {normativos}"
        ),
        (
            "Na qualidade de Agente de Contratação responsável pela análise de "
            "conformidade da fase preparatória, e em cumprimento ao disposto no "
            "art. 53 da Lei nº 14.133/2021, restituo o presente feito para "
            "saneamento das inconsistências identificadas. Os apontamentos possuem "
            "caráter eminentemente colaborativo, visando conferir segurança jurídica, "
            "transparência e eficiência ao procedimento."
        ),
        (
            "A seguir, apresentam-se os achados por artefato, com a respectiva "
            "fundamentação legal, ação de saneamento e sugestão de texto, quando "
            "aplicável. As redações sugeridas têm caráter meramente exemplificativo "
            "e orientativo, competindo à equipe de planejamento da contratação "
            "avaliar sua pertinência frente à realidade técnica e fática do objeto:"
        ),
    ]:
        par = doc.add_paragraph()
        par.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        par.paragraph_format.first_line_indent = Cm(1.25)
        par.add_run(txt)

    doc.add_paragraph()

    # ── Seção por artefato ───────────────────────────────────────────
    secao_num = 1
    total_achados = 0

    for pacote in pacotes:
        artefato = pacote["artefato"]
        label    = _LABELS.get(artefato, artefato)
        achados  = pacote.get("achados", [])

        p = doc.add_paragraph()
        p.add_run(f"{secao_num}. ARTEFATO: {label.upper()}").bold = True
        doc.add_paragraph()

        if not achados:
            par = doc.add_paragraph()
            par.paragraph_format.left_indent = Cm(1)
            par.add_run(
                f"Nenhuma inconsistência identificada. {label} em conformidade "
                "com os normativos aplicáveis."
            ).italic = True
        else:
            for achado in achados:
                total_achados += 1
                par = doc.add_paragraph()
                par.paragraph_format.left_indent = Cm(1)
                par.paragraph_format.space_before = Pt(6)
                num_global = total_achados
                par.add_run(
                    f"{secao_num}.{achado['numero']}. Achado Nº {num_global:02d}: "
                    f"{achado['titulo']}"
                ).bold = True
                if achado.get("tipo"):
                    par.add_run(f" ({achado['tipo']})").italic = True

                campos = [
                    ("Localização",         achado.get("localizacao", "")),
                    ("A Inconsistência",    achado.get("inconsistencia", "")),
                    ("Fundamentação Legal", achado.get("fundamentacao", "")),
                    ("Ação de Saneamento",  achado.get("acao", "")),
                ]
                for sub, (lbl, conteudo) in enumerate(campos, 1):
                    if not conteudo:
                        continue
                    par2 = doc.add_paragraph()
                    par2.paragraph_format.left_indent = Cm(1.5)
                    par2.add_run(f"{secao_num}.{achado['numero']}.{sub}. {lbl}: ").bold = True
                    par2.add_run(conteudo)

                if achado.get("sugestao"):
                    par2 = doc.add_paragraph()
                    par2.paragraph_format.left_indent = Cm(1.5)
                    par2.add_run(
                        f"{secao_num}.{achado['numero']}.5. Sugestão de Texto: "
                    ).bold = True
                    par2.add_run(achado["sugestao"]).italic = True

                doc.add_paragraph()

        secao_num += 1
        doc.add_paragraph()

    # ── Encerramento ─────────────────────────────────────────────────
    for txt in [
        (
            "Salientamos que o cumprimento das recomendações acima, além de conferir "
            "maior segurança jurídica ao procedimento licitatório, contribuirá para a "
            "qualidade dos artefatos subsequentes e para a boa execução contratual, "
            "prevenindo impugnações, questionamentos dos órgãos de controle e "
            "eventuais nulidades processuais."
        ),
        (
            "Fica a disposição para esclarecimentos adicionais e coloca-se à "
            "disposição para reunião de alinhamento, caso necessário."
        ),
    ]:
        par = doc.add_paragraph()
        par.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        par.paragraph_format.first_line_indent = Cm(1.25)
        par.add_run(txt)

    doc.add_paragraph()
    par = doc.add_paragraph()
    par.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    par.add_run(f"Teresina (PI), {DATA_ANALISE}.")

    doc.add_paragraph()
    doc.add_paragraph()
    par = doc.add_paragraph()
    par.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    par.add_run(
        "Agente de Contratação / Assessoria de Compras e Contratos — ASSCOMPRAS"
    ).bold = True
    par = doc.add_paragraph()
    par.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    par.add_run("Ministério Público do Estado do Piauí — MPPI")

    doc.save(caminho_saida)
    print(f"\n✅ Ofício consolidado gerado ({total_achados} achado(s) de {len(pacotes)} artefato(s)):")
    print(f"   {caminho_saida}\n")


def imprimir_resumo(pacotes: list):
    """Exibe resumo dos achados carregados antes de gerar o Ofício."""
    total = sum(len(p.get("achados", [])) for p in pacotes)
    print(f"\n{'═' * 68}")
    print(f"  RESUMO — OFÍCIO CONSOLIDADO  (v{VERSION})")
    print(f"{'═' * 68}")
    for p in pacotes:
        n = len(p.get("achados", []))
        label = _LABELS.get(p["artefato"], p["artefato"])
        print(f"  {label}: {n} achado(s)")
    print(f"{'─' * 68}")
    print(f"  TOTAL: {total} achado(s) em {len(pacotes)} artefato(s)")
    print(f"{'═' * 68}\n")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    # Detectar se foi passada uma pasta
    if len(args) == 1 and os.path.isdir(args[0]):
        caminhos = descobrir_jsons(args[0])
        pasta_saida = Path(args[0])
    else:
        caminhos = args
        pasta_saida = Path(caminhos[0]).parent

    pacotes = carregar_jsons(caminhos)
    imprimir_resumo(pacotes)

    # Inferir nome do processo para o arquivo de saída
    num = pacotes[0].get("num_processo", "").replace("/", "-").replace(".", "")
    data_str = datetime.now().strftime("%Y%m%d_%H%M")
    nome_saida = f"Oficio_ASSCOMPRAS_{num or data_str}.docx"
    caminho_saida = str(pasta_saida / nome_saida)

    gerar_oficio_consolidado(pacotes, caminho_saida)


if __name__ == "__main__":
    main()
