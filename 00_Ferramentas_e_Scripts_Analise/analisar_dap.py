#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════╗
║  Analisador de DAP — ASSCOMPRAS / MPPI                    v1.0      ║
║  Despacho de Abertura de Procedimento                                ║
╚══════════════════════════════════════════════════════════════════════╝

Analisa o Despacho de Abertura de Procedimento (DAP) exportado do SEI
(PDF ou HTML) e gera automaticamente:

  1. Arquivo JSON com achados de conformidade (achados_DAP_*.json)
  2. Relatório resumido no terminal
  3. Ofício ASSCOMPRAS (.docx), se solicitado com --oficio

Base normativa dos quesitos:
  · Lei nº 14.133/2021 — arts. 7º, 8º, 12, 18, 28, 72, 74, 75 e 105
  · Decreto Estadual (PI) nº 21.872/2023 — arts. 18, 19 e 159
  · Lei nº 9.784/1999 — art. 2º, VIII (formalização processual)
  · Roteiro de Quesitos ASSCOMPRAS/MPPI — grupo "Verificação Comum"
  · Lista de Verificação CNMP — Contratação Direta

Requisitos (instale uma única vez):
    pip install pdfplumber beautifulsoup4 lxml python-docx

Uso:
    python analisar_dap.py "caminho\\para\\dap.pdf"
    python analisar_dap.py "caminho\\para\\dap.html" --oficio

⚠ IMPORTANTE: Revise e complemente os achados gerados. A análise
  automática identifica achados comuns mas não substitui a avaliação
  jurídica e técnica do Agente de Contratação.
"""

import sys
import os
import re
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass

VERSION = "1.0.0"
BASE_DIR = Path(__file__).parent
DATA_ANALISE = datetime.now().strftime("%d/%m/%Y")


# ─────────────────────────────────────────────────────────────────────
#  ESTRUTURAS DE DADOS
# ─────────────────────────────────────────────────────────────────────

@dataclass
class Achado:
    numero: int
    titulo: str
    tipo: str = "Vício Formal"
    localizacao: str = ""
    inconsistencia: str = ""
    fundamentacao: str = ""
    acao: str = ""
    sugestao: str = ""


@dataclass
class DAP:
    texto_completo: str = ""
    num_processo: str = ""
    objeto_descricao: str = ""
    unidade_requisitante: str = ""
    unidade_gestora: str = ""

    # Classificação do procedimento
    is_tic:              bool = False
    is_licitacao:        bool = False
    is_dispensa:         bool = False
    is_inexigibilidade:  bool = False
    is_adesao_arp:       bool = False

    # Grupo 1 — Formalização do processo
    tem_num_processo:        bool = False
    tem_objeto:              bool = False
    tem_unidade_requisitante: bool = False

    # Grupo 2 — Autorização e competência
    tem_autorizacao_autoridade: bool = False
    tem_ordenador_despesas:     bool = False

    # Grupo 3 — Designação de agentes
    tem_designacao_agente:   bool = False
    tem_equipe_apoio:        bool = False
    tem_substitutos:         bool = False
    tem_segregacao_funcoes:  bool = False

    # Grupo 4 — Orçamento e planejamento
    tem_unidade_gestora:  bool = False
    tem_fonte_recursos:   bool = False
    tem_referencia_pca:   bool = False

    # Grupo 5 — Enquadramento legal
    tem_enquadramento_legal:  bool = False
    tem_fundamento_dispensa:  bool = False
    tem_fundamento_inexig:    bool = False
    tem_modalidade:           bool = False

    # Grupo 6 — Artefatos referenciados
    tem_referencia_dfd:  bool = False
    tem_referencia_etp:  bool = False
    tem_referencia_tr:   bool = False
    tem_referencia_mr:   bool = False
    tem_referencia_pp:   bool = False

    # Grupo 7 — Determinações e encerramento
    tem_determinacao_providencias: bool = False
    tem_parecer_juridico:          bool = False
    tem_assinatura:                bool = False
    tem_data:                      bool = False
    tem_pncp:                      bool = False


# ─────────────────────────────────────────────────────────────────────
#  EXTRAÇÃO DE TEXTO
# ─────────────────────────────────────────────────────────────────────

def _erro(msg: str):
    print(f"\n❌ ERRO: {msg}\n", file=sys.stderr)
    sys.exit(1)


def _caminho_seguro(caminho: str) -> str:
    import shutil, tempfile
    ext = Path(caminho).suffix.lower()
    dest = os.path.join(tempfile.gettempdir(), f"dap_temp{ext}")
    shutil.copy2(caminho, dest)
    return dest


def extrair_texto_pdf(caminho: str) -> str:
    try:
        import pdfplumber
    except ImportError:
        _erro("pdfplumber não instalado. Execute: pip install pdfplumber")
    caminho_temp = _caminho_seguro(caminho)
    try:
        paginas = []
        with pdfplumber.open(caminho_temp) as pdf:
            for i, page in enumerate(pdf.pages, 1):
                texto = page.extract_text(x_tolerance=3, y_tolerance=3)
                if texto:
                    paginas.append(f"[PÁGINA {i}]\n{texto}")
        return "\n\n".join(paginas)
    except Exception as e:
        _erro(f"Falha ao ler PDF: {e}")
    finally:
        try:
            os.remove(caminho_temp)
        except Exception:
            pass


def extrair_texto_html(caminho: str) -> str:
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        _erro("beautifulsoup4 não instalado. Execute: pip install beautifulsoup4 lxml")
    try:
        with open(caminho, "r", encoding="utf-8", errors="replace") as f:
            conteudo = f.read()
        soup = BeautifulSoup(conteudo, "lxml")
        for tag in soup(["script", "style", "head"]):
            tag.decompose()
        linhas = []
        for elem in soup.find_all(string=True):
            texto = elem.get_text(strip=True)
            if texto:
                linhas.append(texto)
        return "\n".join(linhas)
    except Exception as e:
        _erro(f"Falha ao ler HTML: {e}")


def extrair_texto(caminho: str) -> str:
    ext = Path(caminho).suffix.lower()
    if ext == ".pdf":
        return extrair_texto_pdf(caminho)
    elif ext in (".html", ".htm"):
        return extrair_texto_html(caminho)
    else:
        _erro(f"Formato não suportado: '{ext}'. Use PDF ou HTML exportado do SEI.")


# ─────────────────────────────────────────────────────────────────────
#  PARSING DO DAP
# ─────────────────────────────────────────────────────────────────────

def parse_dap(texto: str) -> DAP:
    dap = DAP()
    dap.texto_completo = texto

    # Número do processo SEI
    m = re.search(r"\b(\d{2}\.\d{2}\.\d{4}\.\d{7}/\d{4}-\d{2})\b", texto)
    if m:
        dap.num_processo = m.group(1)
        dap.tem_num_processo = True
    else:
        dap.tem_num_processo = bool(re.search(
            r"processo\s+(?:SEI\s+)?n[º°]?\s*[\d\.\-/]{8,}", texto, re.IGNORECASE))

    # Objeto
    m = re.search(
        r"(?:OBJETO(?:\s+DA\s+CONTRATA[ÇC][AÃ]O)?)[:\s]+(.{20,400}?)(?:\n[A-Z\d]|\Z)",
        texto, re.DOTALL | re.IGNORECASE)
    if m:
        dap.objeto_descricao = m.group(1).strip()[:300]
    dap.tem_objeto = bool(dap.objeto_descricao) or bool(re.search(
        r"\bobjeto\b.{0,40}(?:contrata[çc][aã]o|aquisi[çc][aã]o|presta[çc][aã]o|fornecimento)",
        texto, re.IGNORECASE))

    # Unidade requisitante
    for pat in [
        r"(?:Unidade\s+Requisitante|[Áa]rea\s+Requisitante|[Óo]rg[aã]o\s+Requisitante"
        r"|Setor\s+Requisitante|Unidade\s+Demandante)[:\s]+([^\n]{4,80})",
        r"(?:Coordenadoria|Assessoria|Diretoria|Secretaria|Gerência)\s+de\s+([^\n]{4,60})",
    ]:
        m = re.search(pat, texto[:4000], re.IGNORECASE)
        if m:
            dap.unidade_requisitante = m.group(0).strip()[:80]
            break
    dap.tem_unidade_requisitante = bool(dap.unidade_requisitante)

    # ── Classificação do procedimento ────────────────────────────────
    dap.is_tic = bool(re.search(
        r"\bTIC\b|tecnologia\s+da\s+informa[çc][aã]o|software|hardware"
        r"|solu[çc][aã]o\s+de\s+TI|CNMP\s+n[º°]?\s*283|MOTec|CTI\b",
        texto, re.IGNORECASE))

    dap.is_dispensa = bool(re.search(
        r"dispensa\s+de\s+licita[çc][aã]o|dispensa\s+eletr[oô]nica"
        r"|art\.?\s*75\b|artigo\s+75\b|contrata[çc][aã]o\s+direta.*dispensa",
        texto, re.IGNORECASE))

    dap.is_inexigibilidade = bool(re.search(
        r"inexigibilidade|art\.?\s*74\b|artigo\s+74\b|invi[aá]bil.*competi[çc][aã]o",
        texto, re.IGNORECASE))

    dap.is_adesao_arp = bool(re.search(
        r"ades[aã]o.*(?:ata|registro\s+de\s+pre[çc]os)|carona"
        r"|ata\s+de\s+registro\s+de\s+pre[çc]os\s+n[º°]",
        texto, re.IGNORECASE))

    dap.is_licitacao = bool(re.search(
        r"preg[aã]o\s+(?:eletr[oô]nico|presencial)|concorr[eê]ncia"
        r"|concurso\b|leil[aã]o\b|di[aá]logo\s+competitivo",
        texto, re.IGNORECASE))

    # ── Grupo 2 — Autorização e competência ──────────────────────────
    dap.tem_autorizacao_autoridade = bool(re.search(
        r"\bAUTORIZO\b|autorizo\s+a\s+(?:abertura|contrata[çc][aã]o|deflagra[çc][aã]o)"
        r"|determino\s+a\s+abertura|fica\s+autorizad|autoriza[çc][aã]o\s+da\s+autoridade"
        r"|\bAPROVO\b|autoridade\s+competente.*autoriz",
        texto, re.IGNORECASE))

    dap.tem_ordenador_despesas = bool(re.search(
        r"ordenador\s+de\s+despesas?|Procurador[a]?-?Geral\s+de\s+Justi[çc]a"
        r"|Chefe\s+de\s+Gabinete|Gestor\s+do\s+F(?:MMPI|PROCON)"
        r"|Coordenador\s+Geral\s+do\s+PROCON",
        texto, re.IGNORECASE))

    # ── Grupo 3 — Designação de agentes ──────────────────────────────
    dap.tem_designacao_agente = bool(re.search(
        r"agente\s+de\s+contrata[çc][aã]o|pregoeir[oa]|comiss[aã]o\s+de\s+contrata[çc][aã]o"
        r"|designo.*(?:agente|pregoeiro|comiss[aã]o)|designa[çc][aã]o.*agente",
        texto, re.IGNORECASE))

    dap.tem_equipe_apoio = bool(re.search(
        r"equipe\s+de\s+apoio|equipe\s+de\s+planejamento",
        texto, re.IGNORECASE))

    dap.tem_substitutos = bool(re.search(
        r"substitut[oa]s?|suplente|em\s+seus?\s+impedimentos?"
        r"|nas\s+aus[eê]ncias|impedimentos\s+legais",
        texto, re.IGNORECASE))

    dap.tem_segregacao_funcoes = bool(re.search(
        r"segrega[çc][aã]o\s+de\s+fun[çc][oõ]es|art\.?\s*7[º°]?,?\s*§\s*1"
        r"|separa[çc][aã]o.*(?:fun[çc][oõ]es|atribui[çc][oõ]es)",
        texto, re.IGNORECASE))

    # ── Grupo 4 — Orçamento e planejamento ───────────────────────────
    m = re.search(
        r"\b(PGJ|FMMPI|FMMPPI|FPROCON|FPDC)\b|unidade\s+gestora[:\s]+([^\n]{3,60})"
        r"|UG\s*(\d{6})",
        texto, re.IGNORECASE)
    if m:
        dap.unidade_gestora = (m.group(0) or "").strip()[:60]
    dap.tem_unidade_gestora = bool(dap.unidade_gestora)

    dap.tem_fonte_recursos = bool(re.search(
        r"elemento\s+de\s+despesa|fonte\s+de\s+recurso|dota[çc][aã]o\s+or[çc]ament[áa]ria"
        r"|classifica[çc][aã]o\s+or[çc]ament[áa]ria|cr[eé]dito\s+or[çc]ament[áa]rio"
        r"|reserva\s+de\s+dota[çc][aã]o|disponibilidade\s+or[çc]ament[áa]ria"
        r"|unidade\s+or[çc]ament[áa]ria",
        texto, re.IGNORECASE))

    dap.tem_referencia_pca = bool(re.search(
        r"\bPCA\b|Plano\s+de\s+Contrata[çc][oõ]es\s+Anual"
        r"|plano\s+anual\s+de\s+contrata[çc][oõ]es",
        texto, re.IGNORECASE))

    # ── Grupo 5 — Enquadramento legal ────────────────────────────────
    dap.tem_fundamento_dispensa = bool(re.search(
        r"art(?:igo)?\.?\s*75\s*,?\s*(?:inciso\s*)?[IVX]+|art\.?\s*75\s*,\s*[IVX]",
        texto, re.IGNORECASE))

    dap.tem_fundamento_inexig = bool(re.search(
        r"art(?:igo)?\.?\s*74\s*,?\s*(?:inciso\s*)?[IVX]+|art\.?\s*74\s*,\s*[IVX]",
        texto, re.IGNORECASE))

    dap.tem_modalidade = bool(re.search(
        r"preg[aã]o\s+eletr[oô]nico|preg[aã]o\s+presencial|concorr[eê]ncia"
        r"|modalidade\s+de\s+licita[çc][aã]o|di[aá]logo\s+competitivo"
        r"|dispensa\s+eletr[oô]nica|inexigibilidade\s+de\s+licita[çc][aã]o",
        texto, re.IGNORECASE))

    dap.tem_enquadramento_legal = (
        dap.tem_fundamento_dispensa
        or dap.tem_fundamento_inexig
        or dap.tem_modalidade
        or bool(re.search(r"Lei\s+n[º°]?\s*14\.133", texto, re.IGNORECASE))
    )

    # ── Grupo 6 — Artefatos referenciados ────────────────────────────
    dap.tem_referencia_dfd = bool(re.search(
        r"\bDFD\b|Documento\s+de\s+Formaliza[çc][aã]o\s+d[ae]\s+Demanda",
        texto, re.IGNORECASE))

    dap.tem_referencia_etp = bool(re.search(
        r"\bETP\b|Estudo\s+T[eé]cnico\s+Preliminar",
        texto, re.IGNORECASE))

    dap.tem_referencia_tr = bool(re.search(
        r"\bTR\b|Termo\s+de\s+Refer[eê]ncia|Projeto\s+B[áa]sico|Projeto\s+Executivo",
        texto, re.IGNORECASE))

    dap.tem_referencia_mr = bool(re.search(
        r"Mapa\s+de\s+Risco|Matriz\s+de\s+Risco|An[áa]lise\s+de\s+Riscos?"
        r"|gerenciamento\s+de\s+riscos",
        texto, re.IGNORECASE))

    dap.tem_referencia_pp = bool(re.search(
        r"pesquisa\s+de\s+pre[çc]os?|or[çc]amento\s+estimado"
        r"|mapa\s+comparativo\s+de\s+pre[çc]os?|estimativa\s+de\s+(?:valor|pre[çc]o)",
        texto, re.IGNORECASE))

    # ── Grupo 7 — Determinações e encerramento ───────────────────────
    dap.tem_determinacao_providencias = bool(re.search(
        r"encaminhe-se|remetam?-se|dê-se\s+ci[eê]ncia|providencie-se"
        r"|determino\s+(?:o|a|que)|encaminhamento\s+dos?\s+autos"
        r"|remessa\s+dos?\s+autos|[àa]\s+(?:CLC|ASSCOMPRAS|CONINT|Assessoria)",
        texto, re.IGNORECASE))

    dap.tem_parecer_juridico = bool(re.search(
        r"parecer\s+jur[íi]dico|manifesta[çc][aã]o\s+jur[íi]dica"
        r"|Manifesta[çc][aã]o\s+Jur[íi]dica\s+Referencial|assessoria\s+jur[íi]dica"
        r"|art\.?\s*53.*14\.133|dispensa.*an[áa]lise\s+jur[íi]dica",
        texto, re.IGNORECASE))

    dap.tem_assinatura = bool(re.search(
        r"assinad[oa]\s+eletronicamente|assinatura\s+eletr[oô]nica"
        r"|documento\s+assinado|Promotor\s+de\s+Justi[çc]a|Procurador[a]?\s+de\s+Justi[çc]a"
        r"|Dr[a]?\.\s+[A-ZÁÉÍÓÚ]",
        texto[-4000:], re.IGNORECASE))

    dap.tem_data = bool(re.search(
        r"\b\d{2}/\d{2}/\d{4}\b|\bde\s+\d{4}\b"
        r"|na\s+data\s+da\s+assinatura\s+eletr[oô]nica"
        r"|Teresina.{0,40}\d{4}",
        texto, re.IGNORECASE))

    dap.tem_pncp = bool(re.search(
        r"\bPNCP\b|Portal\s+Nacional\s+de\s+Contrata[çc][oõ]es\s+P[úu]blicas"
        r"|Portal\s+Nacional\s+de\s+Compras\s+P[úu]blicas",
        texto, re.IGNORECASE))

    return dap


# ─────────────────────────────────────────────────────────────────────
#  CHECKLIST DE CONFORMIDADE
# ─────────────────────────────────────────────────────────────────────

def _add(achados: list, **kwargs) -> None:
    kwargs["numero"] = len(achados) + 1
    achados.append(Achado(**kwargs))


def checar_formalizacao(dap: DAP, achados: list) -> None:
    """Grupo 1 — Formalização e identificação do procedimento."""

    if not dap.tem_num_processo:
        _add(achados,
            titulo="DAP sem Identificação do Número do Processo Administrativo",
            tipo="Vício Formal",
            localizacao="Cabeçalho / preâmbulo do Despacho",
            inconsistencia=(
                "O Despacho de Abertura de Procedimento não identifica o número do "
                "processo administrativo SEI a que se refere. A identificação do "
                "processo devidamente autuado, protocolado e numerado é requisito "
                "elementar da formalização processual administrativa e condição de "
                "rastreabilidade de todos os atos subsequentes."
            ),
            fundamentacao=(
                "Art. 2º, parágrafo único, VIII, da Lei nº 9.784/1999; art. 12, I, e "
                "art. 72, caput, da Lei nº 14.133/2021; art. 159 do Decreto Estadual "
                "(PI) nº 21.872/2023."
            ),
            acao=(
                "Inserir no cabeçalho do Despacho o número integral do processo SEI, "
                "no formato NN.NN.NNNN.NNNNNNN/AAAA-NN."
            ),
            sugestao=(
                "[Ex: 'PROCESSO SEI Nº: 19.21.0967.0010077/2026-14']"
            ),
        )

    if not dap.tem_objeto:
        _add(achados,
            titulo="DAP sem Descrição do Objeto da Contratação",
            tipo="Vício Formal",
            localizacao="Preâmbulo do Despacho",
            inconsistencia=(
                "O Despacho não descreve o objeto da contratação a ser autorizada. "
                "A descrição do objeto é elemento indispensável do ato autorizativo: "
                "sem ela não é possível delimitar o alcance da autorização concedida "
                "pela autoridade competente."
            ),
            fundamentacao=(
                "Art. 6º, XXIII, 'a', e art. 72, caput, da Lei nº 14.133/2021; "
                "art. 18 do Decreto Estadual (PI) nº 21.872/2023."
            ),
            acao=(
                "Inserir no Despacho a descrição sucinta e precisa do objeto, "
                "coincidente com a descrição constante do DFD e do TR."
            ),
            sugestao=(
                "[Ex: 'OBJETO DA CONTRATAÇÃO: Contratação de empresa especializada "
                "na prestação de serviços de [descrição], conforme especificações "
                "do Termo de Referência (doc. SEI nº [ID]).']"
            ),
        )

    if not dap.tem_unidade_requisitante:
        _add(achados,
            titulo="DAP sem Identificação da Unidade Requisitante",
            tipo="Vício Formal",
            localizacao="Preâmbulo / dados gerais do Despacho",
            inconsistencia=(
                "O Despacho não identifica de forma expressa a unidade requisitante "
                "da contratação. A identificação é necessária para verificar a "
                "observância da segregação de funções — a solicitação de compra deve "
                "partir da unidade demandante do bem ou serviço, e não da equipe de "
                "licitação — e para definir os responsáveis pela futura fiscalização."
            ),
            fundamentacao=(
                "Art. 5º e art. 7º, § 1º, da Lei nº 14.133/2021; art. 19 do Decreto "
                "Estadual (PI) nº 21.872/2023; art. 8º da IN SEGES/ME nº 58/2022; "
                "art. 12 do Decreto Federal nº 11.246/2022."
            ),
            acao=(
                "Indicar expressamente no Despacho a unidade requisitante, "
                "identificando o setor e o respectivo Coordenador responsável."
            ),
            sugestao=(
                "[Ex: 'UNIDADE REQUISITANTE: Coordenadoria de [nome], sob a "
                "responsabilidade de [Nome do Coordenador], conforme DFD "
                "(doc. SEI nº [ID]).']"
            ),
        )


def checar_autorizacao(dap: DAP, achados: list) -> None:
    """Grupo 2 — Autorização da autoridade competente."""

    if not dap.tem_autorizacao_autoridade:
        _add(achados,
            titulo="DAP sem Ato Expresso de Autorização da Autoridade Competente",
            tipo="Vício Material",
            localizacao="Parte dispositiva do Despacho",
            inconsistencia=(
                "O Despacho não contém manifestação expressa e inequívoca da "
                "autoridade competente autorizando a abertura do procedimento e a "
                "deflagração da contratação. A autorização da autoridade competente é "
                "requisito legal expresso do processo de contratação — sua ausência "
                "compromete a validade dos atos praticados a partir desse marco."
            ),
            fundamentacao=(
                "Art. 72, VIII, e art. 18, caput, da Lei nº 14.133/2021; art. 18 do "
                "Decreto Estadual (PI) nº 21.872/2023."
            ),
            acao=(
                "Inserir na parte dispositiva do Despacho manifestação expressa da "
                "autoridade competente, com os verbos APROVO e AUTORIZO, referindo-se "
                "aos artefatos de planejamento e à deflagração da fase externa."
            ),
            sugestao=(
                "[Ex: 'CONSIDERANDO os artefatos de planejamento constantes dos autos; "
                "CONSIDERANDO o Parecer Jurídico nº [XXX]; APROVO os artefatos "
                "supramencionados e AUTORIZO a contratação, inclusive a deflagração "
                "da fase externa da licitação/contratação direta.']"
            ),
        )

    if not dap.tem_ordenador_despesas:
        _add(achados,
            titulo="DAP sem Identificação do Ordenador de Despesas Signatário",
            tipo="Vício Formal",
            localizacao="Fecho / assinatura do Despacho",
            inconsistencia=(
                "O Despacho não identifica o cargo do signatário como Ordenador de "
                "Despesas da unidade gestora responsável. A autorização de despesa é "
                "competência privativa do ordenador — a ausência da qualificação "
                "funcional impede verificar a competência do agente que praticou o ato."
            ),
            fundamentacao=(
                "Art. 72, VIII, e art. 105 da Lei nº 14.133/2021; art. 80, § 1º, do "
                "Decreto-Lei nº 200/1967; Ato PGJ/MPPI de delegação de competência "
                "para ordenação de despesas."
            ),
            acao=(
                "Qualificar o signatário no fecho do Despacho, indicando nome, cargo "
                "e a condição de Ordenador de Despesas da unidade gestora "
                "correspondente (PGJ, FMMPI ou FPROCON)."
            ),
            sugestao=(
                "[Ex: 'Dr. [Nome] — Promotor de Justiça / Chefe de Gabinete / "
                "Ordenador de Despesas' ou 'Dr(a). [Nome] — Coordenador(a) Geral do "
                "PROCON / Gestor(a) do FPROCON'.]"
            ),
        )


def checar_designacao_agentes(dap: DAP, achados: list) -> None:
    """Grupo 3 — Designação de agentes e segregação de funções."""

    if not dap.tem_designacao_agente:
        _add(achados,
            titulo="DAP sem Designação Formal do Agente de Contratação ou Comissão",
            tipo="Vício Formal",
            localizacao="Parte dispositiva do Despacho",
            inconsistencia=(
                "O Despacho não designa formalmente o Agente de Contratação, o "
                "Pregoeiro ou a Comissão de Contratação responsável pela condução do "
                "certame. A designação formal é requisito legal e pressuposto de "
                "validade dos atos de condução do procedimento."
            ),
            fundamentacao=(
                "Art. 7º, caput, e art. 8º, caput e § 1º, da Lei nº 14.133/2021; "
                "arts. 3º, 4º e 10, § 3º, do Decreto Federal nº 11.246/2022; art. 19 "
                "do Decreto Estadual (PI) nº 21.872/2023."
            ),
            acao=(
                "Inserir no Despacho a designação nominal do Agente de Contratação "
                "(ou Comissão de Contratação, nos casos de licitação de bens e "
                "serviços especiais), ou referenciar a Portaria PGJ de designação já "
                "publicada."
            ),
            sugestao=(
                "[Ex: 'DESIGNO como Agente de Contratação o servidor [Nome], "
                "matrícula [nº], nos termos do art. 8º da Lei nº 14.133/2021.' ou "
                "'A condução do certame caberá ao Agente de Contratação designado "
                "pela Portaria PGJ/PI nº [XXXX], publicada no DOEMP/PI de [data].']"
            ),
        )

    if dap.tem_designacao_agente and not dap.tem_substitutos:
        _add(achados,
            titulo="DAP sem Indicação dos Substitutos dos Agentes Designados",
            tipo="Sugestão de Melhoria",
            localizacao="Parte dispositiva do Despacho",
            inconsistencia=(
                "O Despacho designa os agentes responsáveis mas não indica seus "
                "substitutos imediatos. A designação de substitutos é exigência "
                "expressa do regulamento e previne a paralisação do procedimento em "
                "caso de afastamento, férias ou impedimento do titular."
            ),
            fundamentacao=(
                "Art. 8º, § 1º, da Lei nº 14.133/2021; art. 10, § 3º, do Decreto "
                "Federal nº 11.246/2022; art. 19 do Decreto Estadual (PI) nº 21.872/2023."
            ),
            acao=(
                "Indicar no Despacho, ou na Portaria referenciada, os substitutos "
                "imediatos do Agente de Contratação e dos integrantes da equipe de apoio."
            ),
            sugestao=(
                "[Ex: 'Nos impedimentos e afastamentos legais do Agente de Contratação "
                "designado, atuará como substituto(a) o(a) servidor(a) [Nome], "
                "matrícula [nº].']"
            ),
        )

    if not dap.tem_segregacao_funcoes:
        _add(achados,
            titulo="Ausência de Registro sobre a Observância da Segregação de Funções",
            tipo="Sugestão de Melhoria",
            localizacao="Considerandos do Despacho",
            inconsistencia=(
                "O Despacho não registra a observância do princípio da segregação de "
                "funções na condução do procedimento. Trata-se de controle interno "
                "expressamente exigido pela Lei nº 14.133/2021: as funções de "
                "requisitar, planejar, conduzir o certame, fiscalizar e ordenar a "
                "despesa devem recair sobre agentes distintos, salvo justificativa."
            ),
            fundamentacao=(
                "Art. 5º e art. 7º, § 1º, da Lei nº 14.133/2021; art. 12 do Decreto "
                "Federal nº 11.246/2022; art. 8º da IN SEGES/ME nº 58/2022."
            ),
            acao=(
                "Acrescentar considerando registrando que a distribuição das funções "
                "observou a segregação exigida pelo art. 7º, § 1º, da Lei nº 14.133/2021, "
                "ou justificar a acumulação quando inevitável em razão do quantitativo "
                "de servidores da unidade."
            ),
            sugestao=(
                "[Ex: 'CONSIDERANDO que a distribuição das atribuições entre a unidade "
                "requisitante, a equipe de planejamento, o Agente de Contratação e o "
                "Ordenador de Despesas observa o princípio da segregação de funções "
                "previsto no art. 7º, § 1º, da Lei nº 14.133/2021;']"
            ),
        )


def checar_orcamento(dap: DAP, achados: list) -> None:
    """Grupo 4 — Adequação orçamentária e planejamento."""

    if not (dap.tem_unidade_gestora or dap.tem_fonte_recursos):
        _add(achados,
            titulo="DAP sem Demonstração da Adequação Orçamentária da Despesa",
            tipo="Vício Material",
            localizacao="Considerandos ou parte dispositiva do Despacho",
            inconsistencia=(
                "O Despacho não indica a unidade gestora responsável nem demonstra a "
                "compatibilidade da previsão de recursos orçamentários com o "
                "compromisso a ser assumido. Essa demonstração é requisito legal "
                "expresso do processo de contratação e pressuposto para a reserva de "
                "dotação e posterior emissão de empenho."
            ),
            fundamentacao=(
                "Art. 72, IV, e art. 105 da Lei nº 14.133/2021; art. 16 da Lei "
                "Complementar nº 101/2000 (LRF); art. 52, § 1º, do Decreto Estadual "
                "(PI) nº 21.872/2023."
            ),
            acao=(
                "Indicar no Despacho a unidade gestora onerada (PGJ, FMMPI ou FPROCON), "
                "o elemento de despesa e a dotação orçamentária, ou referenciar a "
                "declaração de adequação orçamentária juntada aos autos."
            ),
            sugestao=(
                "[Ex: 'UNIDADE ORÇAMENTÁRIA: ( X ) PGJ – Procuradoria-Geral de Justiça "
                "( ) FMMPI – Fundo de Modernização do MPPI ( ) FPROCON – Fundo "
                "Estadual de Proteção e Defesa do Consumidor. CONSIDERANDO a "
                "declaração de adequação orçamentária e financeira (doc. SEI nº [ID]), "
                "que atesta a existência de dotação no elemento de despesa [código];']"
            ),
        )

    if not dap.tem_referencia_pca:
        _add(achados,
            titulo="DAP sem Demonstração da Previsão da Contratação no PCA",
            tipo="Vício Formal",
            localizacao="Considerandos do Despacho",
            inconsistencia=(
                "O Despacho não demonstra a previsão da contratação no Plano de "
                "Contratações Anual (PCA), tampouco justifica a sua ausência. A "
                "demonstração do alinhamento com o PCA é requisito legal que comprova "
                "o planejamento prévio da despesa, ressalvadas apenas as hipóteses "
                "legais de dispensa dessa demonstração."
            ),
            fundamentacao=(
                "Art. 12, VII e § 1º, e art. 18, caput e § 1º, II, da Lei nº 14.133/2021; "
                "art. 7º do Decreto Federal nº 10.947/2022; art. 17, I, do Decreto "
                "Estadual (PI) nº 21.872/2023."
            ),
            acao=(
                "Inserir considerando indicando o item do PCA em que a contratação "
                "está prevista, ou apresentar justificativa formal para a sua ausência "
                "e o ato de inclusão excepcional."
            ),
            sugestao=(
                "[Ex: 'CONSIDERANDO que a presente contratação encontra-se prevista no "
                "Plano de Contratações Anual do MPPI para o exercício de [XXXX], item "
                "nº [código];' | Se ausente: 'CONSIDERANDO a justificativa apresentada "
                "para a inclusão excepcional da demanda no PCA (doc. SEI nº [ID]) e a "
                "respectiva autorização;']"
            ),
        )


def checar_enquadramento(dap: DAP, achados: list) -> None:
    """Grupo 5 — Enquadramento legal do procedimento."""

    if not dap.tem_enquadramento_legal:
        _add(achados,
            titulo="DAP sem Enquadramento Legal do Procedimento de Contratação",
            tipo="Vício Material",
            localizacao="Considerandos ou parte dispositiva do Despacho",
            inconsistencia=(
                "O Despacho não indica o enquadramento legal do procedimento — nem a "
                "modalidade licitatória a ser adotada, nem a hipótese legal de "
                "contratação direta. O enquadramento define o rito procedimental "
                "aplicável e é elemento essencial à motivação do ato administrativo."
            ),
            fundamentacao=(
                "Art. 28, art. 72, caput, art. 74 e art. 75 da Lei nº 14.133/2021; "
                "art. 50 da Lei nº 9.784/1999 (motivação); art. 18 do Decreto Estadual "
                "(PI) nº 21.872/2023."
            ),
            acao=(
                "Indicar expressamente no Despacho: (a) se licitação, a modalidade, o "
                "critério de julgamento e o modo de disputa; (b) se contratação direta, "
                "o dispositivo legal específico (art. 74 ou art. 75, com o inciso)."
            ),
            sugestao=(
                "[Ex LICITAÇÃO: 'AUTORIZO a deflagração de PREGÃO ELETRÔNICO, critério "
                "de julgamento MENOR PREÇO, modo de disputa ABERTO, nos termos do "
                "art. 28, I, e art. 34 da Lei nº 14.133/2021.' | Ex DIRETA: "
                "'AUTORIZO a contratação direta por DISPENSA DE LICITAÇÃO, com "
                "fundamento no art. 75, II, da Lei nº 14.133/2021.']"
            ),
        )

    if dap.is_dispensa and not dap.tem_fundamento_dispensa:
        _add(achados,
            titulo="DAP sem Indicação do Inciso Específico do Art. 75 que Fundamenta a Dispensa",
            tipo="Vício Material",
            localizacao="Considerandos / parte dispositiva do Despacho",
            inconsistencia=(
                "O Despacho refere-se a contratação por dispensa de licitação mas não "
                "indica o inciso específico do art. 75 da Lei nº 14.133/2021 em que a "
                "hipótese se enquadra. As hipóteses de dispensa são taxativas e de "
                "interpretação restritiva — a menção genérica ao artigo não satisfaz "
                "o dever de motivação."
            ),
            fundamentacao=(
                "Art. 72, caput, e art. 75 da Lei nº 14.133/2021; art. 50, I e IV, da "
                "Lei nº 9.784/1999; Ato PGJ/MPPI nº 1.383/2024."
            ),
            acao=(
                "Indicar o inciso específico do art. 75 e demonstrar o preenchimento "
                "dos respectivos requisitos. Tratando-se de dispensa por valor "
                "(incisos I e II), demonstrar o respeito ao limite considerando o "
                "somatório com outros objetos de mesma natureza contratados pela mesma "
                "unidade gestora no exercício."
            ),
            sugestao=(
                "[Ex: 'AUTORIZO a contratação direta por dispensa de licitação, com "
                "fundamento no art. 75, inciso II, da Lei nº 14.133/2021, considerando "
                "que o valor estimado de R$ [X] não supera o limite legal atualizado, "
                "observado o somatório dos objetos de mesma natureza contratados no "
                "exercício, conforme demonstrativo constante dos autos (doc. SEI nº [ID]).']"
            ),
        )

    if dap.is_inexigibilidade and not dap.tem_fundamento_inexig:
        _add(achados,
            titulo="DAP sem Indicação do Inciso Específico do Art. 74 que Fundamenta a Inexigibilidade",
            tipo="Vício Material",
            localizacao="Considerandos / parte dispositiva do Despacho",
            inconsistencia=(
                "O Despacho refere-se a contratação por inexigibilidade mas não indica "
                "o inciso específico do art. 74 da Lei nº 14.133/2021, tampouco "
                "demonstra a inviabilidade de competição. A inviabilidade de competição "
                "é o pressuposto material da inexigibilidade e deve ser demonstrada nos "
                "autos por manifestação técnica."
            ),
            fundamentacao=(
                "Art. 72, caput, e art. 74 da Lei nº 14.133/2021; art. 7º, § 3º, da "
                "IN SEGES/ME nº 65/2021; art. 50, I e IV, da Lei nº 9.784/1999."
            ),
            acao=(
                "Indicar o inciso específico do art. 74 e referenciar a manifestação "
                "técnica que demonstra a inviabilidade de competição, bem como o "
                "documento comprobatório da exclusividade (quando aplicável)."
            ),
            sugestao=(
                "[Ex: 'AUTORIZO a contratação direta por inexigibilidade de licitação, "
                "com fundamento no art. 74, inciso I, da Lei nº 14.133/2021, tendo em "
                "vista o atestado de exclusividade (doc. SEI nº [ID]) e a manifestação "
                "técnica que demonstra a inviabilidade de competição (doc. SEI nº [ID]).']"
            ),
        )


def checar_artefatos_referenciados(dap: DAP, achados: list) -> None:
    """Grupo 6 — Artefatos de planejamento referenciados e aprovados."""

    ausentes = []
    if not dap.tem_referencia_dfd:
        ausentes.append("DFD")
    if not dap.tem_referencia_etp:
        ausentes.append("ETP")
    if not dap.tem_referencia_tr:
        ausentes.append("TR / Projeto Básico")
    if not dap.tem_referencia_mr:
        ausentes.append("Mapa de Riscos")
    if not dap.tem_referencia_pp:
        ausentes.append("Pesquisa de Preços")

    if ausentes:
        _add(achados,
            titulo=(
                "DAP sem Referência Expressa aos Artefatos de Planejamento: "
                + ", ".join(ausentes)
            ),
            tipo="Vício Formal",
            localizacao="Considerandos / seção de especificação dos artefatos",
            inconsistencia=(
                "O Despacho de Abertura, na qualidade de ato de aprovação dos artefatos "
                "da fase preparatória, não referencia expressamente o(s) seguinte(s) "
                f"documento(s): {', '.join(ausentes)}. A aprovação da autoridade "
                "superior deve recair sobre artefatos individualizados e identificados "
                "pelo respectivo número SEI — ou, quando o artefato for legalmente "
                "dispensado, deve constar a justificativa da dispensa."
            ),
            fundamentacao=(
                "Art. 18 e art. 72, I, da Lei nº 14.133/2021; art. 18 e art. 159, I, "
                "do Decreto Estadual (PI) nº 21.872/2023; art. 14, I e II, da "
                "IN SEGES/ME nº 58/2022."
            ),
            acao=(
                "Complementar o Despacho relacionando cada artefato de planejamento "
                "com o respectivo número de documento SEI e link de acesso. Quando o "
                "artefato for dispensado, registrar a hipótese legal da dispensa "
                "(ex.: art. 28, § 2º, do Decreto Estadual nº 21.872/2023 para o ETP; "
                "art. 34, XXII, do mesmo Decreto para a matriz de riscos)."
            ),
            sugestao=(
                "[Estruturar tabela: '1. DFD — doc. SEI nº [ID]; 2. ETP — doc. SEI nº "
                "[ID] ou ( ) não foi elaborado ETP, pois é dispensado nos termos do "
                "art. 28, § 2º, do Decreto Estadual nº 21.872/2023; 3. Mapa de Riscos "
                "— doc. SEI nº [ID]; 4. TR — doc. SEI nº [ID]; 5. Pesquisa de Preços "
                "— doc. SEI nº [ID].']"
            ),
        )

    if not dap.tem_parecer_juridico:
        _add(achados,
            titulo="DAP sem Referência ao Parecer Jurídico ou à sua Dispensa",
            tipo="Vício Formal",
            localizacao="Considerandos do Despacho",
            inconsistencia=(
                "O Despacho não referencia o Parecer Jurídico, a Manifestação Jurídica "
                "Referencial, nem registra a hipótese de dispensa da análise jurídica. "
                "O controle prévio de legalidade é etapa obrigatória do processo de "
                "contratação, salvo nas hipóteses de dispensa autorizadas por ato da "
                "autoridade máxima."
            ),
            fundamentacao=(
                "Art. 53, caput, § 4º e § 5º, e art. 72, III, da Lei nº 14.133/2021; "
                "Atos PGJ/MPPI nº 1.383/2024 e nº 1.480/2025 (hipóteses de dispensa "
                "de Parecer Jurídico)."
            ),
            acao=(
                "Referenciar no Despacho o Parecer Jurídico ou a Manifestação Jurídica "
                "Referencial aplicável, com o número do documento SEI. Se a análise "
                "jurídica for dispensada, indicar expressamente a hipótese normativa "
                "(baixo valor, baixa complexidade, entrega imediata ou utilização de "
                "minutas padronizadas)."
            ),
            sugestao=(
                "[Ex: 'CONSIDERANDO o Parecer Jurídico nº [XXX] (doc. SEI nº [ID]), "
                "que opinou pela regularidade da contratação;' | Se dispensado: "
                "'CONSIDERANDO que a presente contratação enquadra-se na hipótese de "
                "dispensa de análise jurídica prevista no art. 53, § 5º, da Lei nº "
                "14.133/2021 e no Ato PGJ nº 1.383/2024, por se tratar de contratação "
                "de baixo valor com utilização de minuta padronizada;']"
            ),
        )


def checar_encerramento(dap: DAP, achados: list) -> None:
    """Grupo 7 — Determinações, publicidade e assinatura."""

    if not dap.tem_determinacao_providencias:
        _add(achados,
            titulo="DAP sem Determinação Expressa das Providências Subsequentes",
            tipo="Sugestão de Melhoria",
            localizacao="Parte dispositiva final do Despacho",
            inconsistencia=(
                "O Despacho não determina expressamente as providências subsequentes "
                "nem o encaminhamento dos autos à unidade responsável pela condução da "
                "fase externa. A ausência de comando processual claro gera indefinição "
                "quanto ao próximo responsável pelo feito e pode acarretar paralisação "
                "injustificada do processo."
            ),
            fundamentacao=(
                "Art. 5º (princípio da eficiência) e art. 12, I, da Lei nº 14.133/2021; "
                "art. 2º, parágrafo único, IX e XII, da Lei nº 9.784/1999."
            ),
            acao=(
                "Acrescentar ao final do Despacho determinação expressa de "
                "encaminhamento dos autos, indicando a unidade destinatária e a "
                "providência esperada."
            ),
            sugestao=(
                "[Ex: 'Encaminhem-se os autos à Coordenadoria de Licitações e Contratos "
                "— CLC, para as providências relativas à deflagração da fase externa "
                "do certame e publicação do instrumento convocatório no PNCP.']"
            ),
        )

    if (dap.is_dispensa or dap.is_inexigibilidade) and not dap.tem_pncp:
        _add(achados,
            titulo="DAP sem Determinação de Divulgação do Ato de Contratação Direta no PNCP",
            tipo="Vício Formal",
            localizacao="Parte dispositiva final do Despacho",
            inconsistencia=(
                "Tratando-se de contratação direta, o Despacho não determina a "
                "divulgação do ato que autoriza a contratação no Portal Nacional de "
                "Contratações Públicas (PNCP). A publicação é condição de eficácia do "
                "ato de contratação direta e requisito de transparência ativa."
            ),
            fundamentacao=(
                "Art. 72, parágrafo único, e art. 174, § 2º, III e V, da Lei nº "
                "14.133/2021; art. 94 da Lei nº 14.133/2021; art. 93 do Decreto "
                "Estadual (PI) nº 21.872/2023."
            ),
            acao=(
                "Inserir determinação expressa de divulgação do ato autorizativo da "
                "contratação direta no PNCP e no sítio eletrônico oficial do MPPI, "
                "como condição de eficácia."
            ),
            sugestao=(
                "[Ex: 'Determino a divulgação do presente ato de autorização da "
                "contratação direta no Portal Nacional de Contratações Públicas (PNCP) "
                "e no sítio eletrônico oficial do MPPI, nos termos do art. 72, "
                "parágrafo único, da Lei nº 14.133/2021.']"
            ),
        )

    if not dap.tem_assinatura:
        _add(achados,
            titulo="DAP sem Evidência de Assinatura Eletrônica",
            tipo="Vício Formal",
            localizacao="Fecho do Despacho",
            inconsistencia=(
                "O Despacho não apresenta evidência de assinatura eletrônica pela "
                "autoridade competente. A assinatura é condição de existência e "
                "validade do ato administrativo autorizativo."
            ),
            fundamentacao=(
                "Art. 12, VI, da Lei nº 14.133/2021; art. 22, § 1º, da Lei nº "
                "9.784/1999; Ato PGJ/MPPI que disciplina o uso do SEI."
            ),
            acao=(
                "Assinar eletronicamente o Despacho no SEI, na qualidade de autoridade "
                "competente / Ordenador de Despesas, antes do encaminhamento dos autos."
            ),
            sugestao=(
                "[Ex fecho: 'Teresina (PI), na data da assinatura eletrônica. "
                "[Nome] — Promotor de Justiça / Chefe de Gabinete / Ordenador de "
                "Despesas'.]"
            ),
        )


def checar_quesitos_json(dap: DAP, achados: list) -> None:
    """Verifica quesitos declarativos definidos em quesitos_DAP.json."""
    import json
    caminho_json = BASE_DIR / "quesitos_DAP.json"
    if not caminho_json.exists():
        return
    try:
        with open(caminho_json, encoding="utf-8") as f:
            dados = json.load(f)
    except Exception:
        return
    texto = dap.texto_completo
    is_tic = dap.is_tic
    for q in dados.get("quesitos", []):
        if q.get("is_tic_only") and not is_tic:
            continue
        if q.get("is_direta_only") and not (dap.is_dispensa or dap.is_inexigibilidade):
            continue
        patterns = q.get("patterns", [])
        modo = q.get("modo", "ausente")
        encontrou = any(re.search(p, texto, re.IGNORECASE | re.DOTALL) for p in patterns)
        gerar_achado = (modo == "ausente" and not encontrou) or \
                       (modo == "presente" and encontrou)
        if gerar_achado:
            _add(achados,
                titulo=q.get("titulo", ""),
                tipo=q.get("tipo", "Vício Formal"),
                localizacao=q.get("localizacao", "Documento completo"),
                inconsistencia=q.get("inconsistencia", ""),
                fundamentacao=q.get("fundamentacao", ""),
                acao=q.get("acao", ""),
                sugestao=q.get("sugestao", ""),
            )


# ─────────────────────────────────────────────────────────────────────
#  PERSISTÊNCIA DE ACHADOS EM JSON
# ─────────────────────────────────────────────────────────────────────

def salvar_achados_json(dap: DAP, achados: list, caminho_origem: str) -> str:
    """Salva os achados em JSON para consolidação posterior no Ofício final."""
    import json
    base = Path(caminho_origem).stem
    pasta = Path(caminho_origem).parent
    caminho_json = str(pasta / f"achados_DAP_{base}.json")

    dados = {
        "artefato": "DAP",
        "num_processo": dap.num_processo or "",
        "objeto": dap.objeto_descricao or "",
        "unidade": dap.unidade_requisitante or "",
        "is_tic": dap.is_tic,
        "data_analise": DATA_ANALISE,
        "arquivo_origem": Path(caminho_origem).name,
        "achados": [
            {
                "numero": a.numero,
                "titulo": a.titulo,
                "tipo": a.tipo,
                "localizacao": a.localizacao,
                "inconsistencia": a.inconsistencia,
                "fundamentacao": a.fundamentacao,
                "acao": a.acao,
                "sugestao": a.sugestao,
            }
            for a in achados
        ],
    }
    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    print(f"\n💾 Achados salvos em: {caminho_json}")
    return caminho_json


# ─────────────────────────────────────────────────────────────────────
#  GERAÇÃO DO OFÍCIO WORD
# ─────────────────────────────────────────────────────────────────────

def _set_font(doc, nome="Times New Roman", tamanho=12):
    from docx.shared import Pt
    style = doc.styles["Normal"]
    style.font.name = nome
    style.font.size = Pt(tamanho)


def gerar_oficio_word(dap: DAP, achados: list, caminho_saida: str):
    try:
        from docx import Document
        from docx.shared import Pt, Cm
        from docx.enum.text import WD_ALIGN_PARAGRAPH
    except ImportError:
        print("ERRO: python-docx não instalado. Execute: pip install python-docx")
        sys.exit(1)

    doc = Document()
    _set_font(doc, "Times New Roman", 12)
    section = doc.sections[0]
    section.top_margin    = Cm(3)
    section.bottom_margin = Cm(2)
    section.left_margin   = Cm(3)
    section.right_margin  = Cm(2)

    unidade  = dap.unidade_requisitante or "[Unidade Requisitante]"
    processo = dap.num_processo         or "[nº do processo SEI]"

    p = doc.add_paragraph()
    p.add_run(f"À {unidade}").bold = True
    p = doc.add_paragraph()
    p.add_run(
        f"Assunto: Devolução de Autos para Saneamento — "
        f"Análise do Despacho de Abertura de Procedimento — "
        f"Processo SEI nº {processo}."
    ).bold = True

    doc.add_paragraph()
    doc.add_paragraph().add_run("Senhor(a) Coordenador(a),")
    doc.add_paragraph()

    abertura = [
        (
            "Cumprimentando-o cordialmente, registro que a equipe desta Assessoria "
            "analisou o Despacho de Abertura de Procedimento (DAP) juntado aos autos "
            "do processo em referência, verificando a conformidade do documento com "
            "os normativos aplicáveis: Lei nº 14.133/2021, Lei nº 9.784/1999, Decreto "
            "Estadual (PI) nº 21.872/2023 e Atos PGJ/MPPI nº 1.381 e 1.382/2024."
        ),
        (
            "Na qualidade de Agente de Contratação responsável pela análise de "
            "conformidade da fase preparatória, e em cumprimento ao disposto no "
            "art. 53 da Lei nº 14.133/2021, restituo o presente feito para saneamento "
            "das inconsistências identificadas no DAP. Os apontamentos possuem caráter "
            "eminentemente colaborativo, visando conferir segurança jurídica, "
            "transparência e eficiência ao procedimento."
        ),
        (
            "A seguir, apresentam-se os achados estruturados, com a respectiva "
            "fundamentação legal, ação de saneamento e sugestão de texto, quando "
            "aplicável. As redações sugeridas têm caráter meramente exemplificativo "
            "e orientativo:"
        ),
    ]
    for txt in abertura:
        p = doc.add_paragraph()
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.first_line_indent = Cm(1.25)
        p.add_run(txt)

    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run("1. ARTEFATO: DESPACHO DE ABERTURA DE PROCEDIMENTO (DAP)").bold = True
    doc.add_paragraph()

    if not achados:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(1)
        p.add_run(
            "Nenhuma inconsistência identificada. DAP em conformidade com os "
            "normativos aplicáveis."
        ).italic = True
    else:
        for achado in achados:
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(1)
            p.paragraph_format.space_before = Pt(6)
            p.add_run(f"{achado.numero}. Achado Nº {achado.numero:02d}: {achado.titulo}").bold = True
            if achado.tipo:
                p.add_run(f" ({achado.tipo})").italic = True

            campos = [
                ("Localização",         achado.localizacao),
                ("A Inconsistência",    achado.inconsistencia),
                ("Fundamentação Legal", achado.fundamentacao),
                ("Ação de Saneamento",  achado.acao),
            ]
            for sub, (label, conteudo) in enumerate(campos, 1):
                if not conteudo:
                    continue
                p = doc.add_paragraph()
                p.paragraph_format.left_indent = Cm(1.5)
                p.add_run(f"{achado.numero}.{sub}. {label}: ").bold = True
                p.add_run(conteudo)

            if achado.sugestao:
                p = doc.add_paragraph()
                p.paragraph_format.left_indent = Cm(1.5)
                p.add_run(f"{achado.numero}.5. Sugestão de Texto: ").bold = True
                p.add_run(achado.sugestao).italic = True

            doc.add_paragraph()

    doc.add_paragraph()
    p = doc.add_paragraph()
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.first_line_indent = Cm(1.25)
    p.add_run(
        "Salientamos que o cumprimento das recomendações acima, além de conferir "
        "maior segurança jurídica ao procedimento, contribuirá para a regularidade "
        "da instrução processual e para a prevenção de questionamentos dos órgãos "
        "de controle."
    )

    doc.add_paragraph()
    p = doc.add_paragraph()
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run(f"Teresina (PI), {DATA_ANALISE}.")

    doc.add_paragraph()
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run("Agente de Contratação / Assessoria de Compras e Contratos — ASSCOMPRAS").bold = True
    p = doc.add_paragraph()
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run("Ministério Público do Estado do Piauí — MPPI")

    doc.save(caminho_saida)
    print(f"\n✅ Ofício gerado: {caminho_saida}\n")


# ─────────────────────────────────────────────────────────────────────
#  RELATÓRIO NO TERMINAL
# ─────────────────────────────────────────────────────────────────────

def imprimir_relatorio(dap: DAP, achados: list):
    sep = "─" * 68
    print(f"\n{'═' * 68}")
    print(f"  ANÁLISE DE CONFORMIDADE — DAP  (v{VERSION})")
    print(f"{'═' * 68}")
    print(f"  Processo: {dap.num_processo or '(não identificado)'}")
    print(f"  Unidade : {dap.unidade_requisitante or '(não identificada)'}")
    print(f"  Objeto  : {(dap.objeto_descricao or '(não identificado)')[:70]}...")
    flags_cls = []
    if dap.is_tic:             flags_cls.append("TIC")
    if dap.is_licitacao:       flags_cls.append("Licitação")
    if dap.is_dispensa:        flags_cls.append("Dispensa")
    if dap.is_inexigibilidade: flags_cls.append("Inexigibilidade")
    if dap.is_adesao_arp:      flags_cls.append("Adesão a ARP")
    print(f"  Tipo    : {', '.join(flags_cls) or '(não classificado)'}")
    print(f"  Data    : {DATA_ANALISE}")
    print(sep)

    checks = [
        ("Nº do processo",              dap.tem_num_processo),
        ("Objeto descrito",             dap.tem_objeto),
        ("Unidade requisitante",        dap.tem_unidade_requisitante),
        ("Autorização da autoridade",   dap.tem_autorizacao_autoridade),
        ("Ordenador de Despesas",       dap.tem_ordenador_despesas),
        ("Designação do Agente",        dap.tem_designacao_agente),
        ("Substitutos indicados",       dap.tem_substitutos),
        ("Segregação de funções",       dap.tem_segregacao_funcoes),
        ("Unidade gestora",             dap.tem_unidade_gestora),
        ("Fonte de recursos",           dap.tem_fonte_recursos),
        ("Referência ao PCA",           dap.tem_referencia_pca),
        ("Enquadramento legal",         dap.tem_enquadramento_legal),
        ("Referência ao DFD",           dap.tem_referencia_dfd),
        ("Referência ao ETP",           dap.tem_referencia_etp),
        ("Referência ao Mapa de Riscos", dap.tem_referencia_mr),
        ("Referência ao TR",            dap.tem_referencia_tr),
        ("Referência à Pesquisa de Preços", dap.tem_referencia_pp),
        ("Parecer Jurídico",            dap.tem_parecer_juridico),
        ("Determinação de providências", dap.tem_determinacao_providencias),
        ("Referência ao PNCP",          dap.tem_pncp),
        ("Assinatura",                  dap.tem_assinatura),
    ]
    print("  VERIFICAÇÕES:")
    for label, flag in checks:
        status = "✓" if flag else "✗"
        print(f"    [{status}] {label}")

    print(sep)
    if not achados:
        print("  ✅ Nenhuma inconsistência identificada.")
    else:
        print(f"  ⚠ {len(achados)} achado(s) identificado(s):\n")
        for a in achados:
            print(f"    {a.numero:02d}. [{a.tipo}] {a.titulo}")
    print(f"{'═' * 68}\n")


# ─────────────────────────────────────────────────────────────────────
#  PONTO DE ENTRADA
# ─────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    caminho = sys.argv[1]
    if not os.path.isfile(caminho):
        _erro(f"Arquivo não encontrado: '{caminho}'")

    print(f"\n🔍 Lendo arquivo: {caminho}")
    texto = extrair_texto(caminho)
    print(f"   {len(texto):,} caracteres extraídos.")

    dap = parse_dap(texto)
    achados: list = []

    checar_formalizacao(dap, achados)
    checar_autorizacao(dap, achados)
    checar_designacao_agentes(dap, achados)
    checar_orcamento(dap, achados)
    checar_enquadramento(dap, achados)
    checar_artefatos_referenciados(dap, achados)
    checar_encerramento(dap, achados)
    checar_quesitos_json(dap, achados)

    print(f"      {len(achados)} achado(s) identificado(s)")
    imprimir_relatorio(dap, achados)

    salvar_achados_json(dap, achados, caminho)

    if "--oficio" in sys.argv:
        base = Path(caminho).stem
        saida = str(Path(caminho).parent / f"Oficio_ASSCOMPRAS_DAP_{base}.docx")
        gerar_oficio_word(dap, achados, saida)
    else:
        print("ℹ  Para gerar o Ofício Word desta análise isolada, use: --oficio")
        print("ℹ  Para consolidar todos os artefatos do processo, use: gerar_oficio_processo.py\n")


if __name__ == "__main__":
    main()
