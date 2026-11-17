#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════╗
║  Analisador de MR — ASSCOMPRAS / MPPI                     v1.0      ║
║  Mapa de Riscos / Análise de Riscos da Contratação                   ║
╚══════════════════════════════════════════════════════════════════════╝

Analisa o Mapa de Riscos (MR) exportado do SEI (PDF ou HTML) e gera
automaticamente:

  1. Arquivo JSON com achados de conformidade (achados_MR_*.json)
  2. Relatório resumido no terminal
  3. Ofício ASSCOMPRAS (.docx), se solicitado com --oficio

Base normativa dos quesitos:
  · Lei nº 14.133/2021 — arts. 11 (par. único), 18, X, 22, § 3º, 103 e 169
  · Decreto Estadual (PI) nº 21.872/2023 — arts. 29 a 34 e 159
  · IN SEGES/MP nº 5/2017 — art. 26 e Anexos I (XII), III (3.10, "c") e IV
  · Roteiro de Quesitos ASSCOMPRAS/MPPI — grupo "Análise de Riscos" (Q69–Q83)
  · Lista de Verificação CNMP — Mapa de Riscos

Requisitos (instale uma única vez):
    pip install pdfplumber beautifulsoup4 lxml python-docx

Uso:
    python analisar_mr.py "caminho\\para\\mapa_riscos.pdf"
    python analisar_mr.py "caminho\\para\\mapa_riscos.html" --oficio

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

# Nº mínimo de riscos esperado num Mapa de Riscos minimamente consistente
MIN_RISCOS_ESPERADO = 3


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
class MR:
    texto_completo: str = ""
    num_processo: str = ""
    objeto_descricao: str = ""
    unidade_requisitante: str = ""

    # Classificação
    is_tic:     bool = False
    is_servico: bool = False
    is_obra:    bool = False

    # Métricas
    num_riscos_identificados: int = 0

    # Grupo 1 — Existência e vinculação
    tem_referencia_processo:  bool = False
    tem_descricao_solucao:    bool = False
    tem_referencia_etp:       bool = False

    # Grupo 2 — Estrutura mínima do Mapa de Riscos
    tem_identificacao_riscos: bool = False
    tem_probabilidade:        bool = False
    tem_impacto:              bool = False
    tem_nivel_risco:          bool = False
    tem_escala_criterios:     bool = False

    # Grupo 3 — Tratamento dos riscos
    tem_acoes_preventivas:  bool = False
    tem_acoes_contingencia: bool = False
    tem_responsaveis:       bool = False

    # Grupo 4 — Abrangência (fases do processo)
    tem_riscos_planejamento: bool = False
    tem_riscos_selecao:      bool = False
    tem_riscos_execucao:     bool = False

    # Grupo 5 — Matriz de alocação de riscos (contratual)
    tem_matriz_alocacao:      bool = False
    tem_equilibrio_economico: bool = False

    # Grupo 6 — Monitoramento e governança
    tem_monitoramento:         bool = False
    tem_periodicidade_revisao: bool = False
    tem_referencia_politica:   bool = False

    # Grupo 7 — Encerramento
    tem_assinatura: bool = False


# ─────────────────────────────────────────────────────────────────────
#  EXTRAÇÃO DE TEXTO
# ─────────────────────────────────────────────────────────────────────

def _erro(msg: str):
    print(f"\n❌ ERRO: {msg}\n", file=sys.stderr)
    sys.exit(1)


def _caminho_seguro(caminho: str) -> str:
    import shutil, tempfile
    ext = Path(caminho).suffix.lower()
    dest = os.path.join(tempfile.gettempdir(), f"mr_temp{ext}")
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
#  PARSING DO MAPA DE RISCOS
# ─────────────────────────────────────────────────────────────────────

def parse_mr(texto: str) -> MR:
    mr = MR()
    mr.texto_completo = texto

    # Número do processo SEI
    m = re.search(r"\b(\d{2}\.\d{2}\.\d{4}\.\d{7}/\d{4}-\d{2})\b", texto)
    if m:
        mr.num_processo = m.group(1)
    mr.tem_referencia_processo = bool(m) or bool(re.search(
        r"processo\s+(?:SEI\s+)?n[º°]?\s*[\d\.\-/]{8,}", texto, re.IGNORECASE))

    # Objeto / solução
    m = re.search(
        r"(?:OBJETO|SOLU[ÇC][AÃ]O(?:\s+A\s+SER\s+CONTRATADA)?|DESCRI[ÇC][AÃ]O\s+DA\s+SOLU[ÇC][AÃ]O)"
        r"[:\s]+(.{20,400}?)(?:\n[A-Z\d]|\Z)",
        texto, re.DOTALL | re.IGNORECASE)
    if m:
        mr.objeto_descricao = m.group(1).strip()[:300]

    mr.tem_descricao_solucao = bool(mr.objeto_descricao) or bool(re.search(
        r"descri[çc][aã]o\s+da\s+solu[çc][aã]o|solu[çc][aã]o\s+a\s+ser\s+contratada"
        r"|objeto\s+da\s+contrata[çc][aã]o",
        texto, re.IGNORECASE))

    # Unidade requisitante
    for pat in [
        r"(?:Unidade\s+Requisitante|[Áa]rea\s+Requisitante|Unidade\s+Demandante"
        r"|[Áa]rea\s+Demandante|Setor\s+Requisitante)[:\s]+([^\n]{4,80})",
        r"(?:Coordenadoria|Assessoria|Diretoria|Secretaria|Gerência)\s+de\s+[^\n]{4,60}",
    ]:
        m = re.search(pat, texto[:4000], re.IGNORECASE)
        if m:
            mr.unidade_requisitante = m.group(0).strip()[:80]
            break

    # ── Classificação ────────────────────────────────────────────────
    mr.is_tic = bool(re.search(
        r"\bTIC\b|tecnologia\s+da\s+informa[çc][aã]o|software|hardware"
        r"|solu[çc][aã]o\s+de\s+TI|CNMP\s+n[º°]?\s*283|MOTec"
        r"|seguran[çc]a\s+da\s+informa[çc][aã]o|\bLGPD\b",
        texto, re.IGNORECASE))

    mr.is_servico = bool(re.search(
        r"presta[çc][aã]o\s+de\s+servi[çc]o|contrata[çc][aã]o\s+de\s+servi[çc]o"
        r"|m[aã]o\s+de\s+obra|servi[çc]os?\s+continuad",
        texto, re.IGNORECASE))

    mr.is_obra = bool(re.search(
        r"obra[s]?\s+(?:e\s+servi[çc]os?\s+)?de\s+engenharia|servi[çc]o\s+de\s+engenharia"
        r"|reforma|constru[çc][aã]o|projeto\s+executivo",
        texto, re.IGNORECASE))

    # ── Grupo 1 — Vinculação aos demais artefatos ────────────────────
    mr.tem_referencia_etp = bool(re.search(
        r"\bETP\b|Estudo\s+T[eé]cnico\s+Preliminar|\bDFD\b"
        r"|Documento\s+de\s+Formaliza[çc][aã]o|Termo\s+de\s+Refer[eê]ncia|\bTR\b",
        texto, re.IGNORECASE))

    # ── Grupo 2 — Estrutura mínima ───────────────────────────────────
    mr.tem_identificacao_riscos = bool(re.search(
        r"risco\s+\d|risco\s+n[º°]|evento\s+de\s+risco|identifica[çc][aã]o\s+d[eo]s?\s+riscos?"
        r"|\bR\d{1,2}\b|descri[çc][aã]o\s+do\s+risco|riscos?\s+identificad",
        texto, re.IGNORECASE))

    # Contagem aproximada de riscos catalogados
    padroes_contagem = [
        r"(?:^|\n)\s*(?:risco|evento)\s*(?:n[º°]\s*)?\d{1,2}\b",
        r"(?:^|\n)\s*R\s*[-–]?\s*\d{1,2}\b",
        r"\bID\s*[-–:]?\s*\d{1,2}\b",
    ]
    ocorrencias = set()
    for pat in padroes_contagem:
        for m2 in re.finditer(pat, texto, re.IGNORECASE | re.MULTILINE):
            ocorrencias.add(m2.group(0).strip().lower())
    mr.num_riscos_identificados = len(ocorrencias)

    mr.tem_probabilidade = bool(re.search(
        r"probabilidade|frequ[eê]ncia\s+(?:de\s+)?ocorr[eê]ncia"
        r"|chance\s+de\s+ocorr[eê]ncia|verossimilhan[çc]a",
        texto, re.IGNORECASE))

    mr.tem_impacto = bool(re.search(
        r"\bimpacto\b|consequ[eê]ncia|severidade|gravidade|dano\s+potencial"
        r"|efeito.*(?:ocorr[eê]ncia|materializa)",
        texto, re.IGNORECASE))

    mr.tem_nivel_risco = bool(re.search(
        r"n[íi]vel\s+de\s+risco|criticidade|grau\s+de\s+risco|risco\s+(?:residual|inerente)"
        r"|classifica[çc][aã]o\s+do\s+risco|(?:alt[oa]|m[ée]di[oa]|baix[oa])\s*[/,]\s*(?:alt|m[ée]d|baix)"
        r"|matriz\s+de\s+(?:severidade|criticidade)|P\s*[x×]\s*I\b",
        texto, re.IGNORECASE))

    mr.tem_escala_criterios = bool(re.search(
        r"escala\s+de\s+(?:probabilidade|impacto|risco)|crit[eé]rios?\s+de\s+(?:avalia[çc][aã]o|classifica)"
        r"|(?:1|um)\s*[-–a]\s*(?:5|cinco)|legenda|par[aâ]metros?\s+de\s+(?:avalia[çc][aã]o|pontua)"
        r"|metodologia\s+de\s+(?:an[áa]lise|avalia[çc][aã]o)\s+de\s+riscos?",
        texto, re.IGNORECASE))

    # ── Grupo 3 — Tratamento dos riscos ──────────────────────────────
    mr.tem_acoes_preventivas = bool(re.search(
        r"a[çc][õo]es?\s+preventiva|medida[s]?\s+preventiva|preven[çc][aã]o"
        r"|mitiga[çc][aã]o|a[çc][õo]es?\s+de\s+mitiga|medida[s]?\s+mitigador"
        r"|tratamento\s+do\s+risco|resposta\s+ao\s+risco|controle[s]?\s+preventiv",
        texto, re.IGNORECASE))

    mr.tem_acoes_contingencia = bool(re.search(
        r"conting[eê]ncia|a[çc][õo]es?\s+de\s+conting|plano\s+de\s+conting"
        r"|a[çc][õo]es?\s+corretiva|medida[s]?\s+corretiva|caso\s+(?:o\s+risco\s+)?se\s+concretiz"
        r"|se\s+materializ|controle[s]?\s+corretiv",
        texto, re.IGNORECASE))

    mr.tem_responsaveis = bool(re.search(
        r"respons[áa]vel\s+(?:pela|pelo)|respons[áa]veis|dono\s+do\s+risco"
        r"|\bowner\b|unidade\s+respons[áa]vel|setor\s+respons[áa]vel"
        r"|respons[áa]vel\s+pela\s+(?:a[çc][aã]o|mitiga|implementa|gest[aã]o|monitor)",
        texto, re.IGNORECASE))

    # ── Grupo 4 — Abrangência por fase ───────────────────────────────
    mr.tem_riscos_planejamento = bool(re.search(
        r"fase\s+de\s+planejamento|fase\s+preparat[óo]ria|fase\s+interna"
        r"|risco.*planejamento|planejamento\s+da\s+contrata[çc][aã]o",
        texto, re.IGNORECASE))

    mr.tem_riscos_selecao = bool(re.search(
        r"sele[çc][aã]o\s+do\s+fornecedor|fase\s+externa|fase\s+de\s+sele[çc][aã]o"
        r"|risco.*(?:licita[çc][aã]o|certame)|deserto|fracassad|impugna[çc][aã]o|recurso\s+administrativo",
        texto, re.IGNORECASE))

    mr.tem_riscos_execucao = bool(re.search(
        r"gest[aã]o\s+(?:do\s+)?contratual|execu[çc][aã]o\s+(?:do\s+)?contratual"
        r"|fase\s+de\s+(?:gest[aã]o|execu[çc][aã]o)|risco.*execu[çc][aã]o\s+contratual"
        r"|inadimplemento|atraso\s+na\s+entrega|rescis[aã]o",
        texto, re.IGNORECASE))

    # ── Grupo 5 — Matriz de alocação de riscos ───────────────────────
    mr.tem_matriz_alocacao = bool(re.search(
        r"matriz\s+de\s+(?:aloca[çc][aã]o\s+de\s+)?riscos?|aloca[çc][aã]o\s+de\s+riscos?"
        r"|reparti[çc][aã]o\s+de\s+riscos?|risco.*(?:contratante|contratad[ao])"
        r"|art\.?\s*22.*14\.133|art\.?\s*103.*14\.133",
        texto, re.IGNORECASE))

    mr.tem_equilibrio_economico = bool(re.search(
        r"equil[íi]brio\s+econ[oô]mico|reequil[íi]brio|[áa]lea\s+(?:ordin[áa]ria|extraordin[áa]ria)"
        r"|revis[aã]o\s+(?:contratual|de\s+pre[çc]os)|caso\s+fortuito|for[çc]a\s+maior",
        texto, re.IGNORECASE))

    # ── Grupo 6 — Monitoramento e governança ─────────────────────────
    mr.tem_monitoramento = bool(re.search(
        r"monitoramento|acompanhamento\s+d[eo]s?\s+riscos?|monitorar"
        r"|indicador.*risco|controle\s+cont[íi]nuo|reavalia[çc][aã]o\s+d[eo]s?\s+riscos?",
        texto, re.IGNORECASE))

    mr.tem_periodicidade_revisao = bool(re.search(
        r"periodicidade|revis[aã]o\s+(?:peri[óo]dica|do\s+mapa|semestral|anual|trimestral)"
        r"|atualiza[çc][aã]o\s+(?:peri[óo]dica|semestral|anual|trimestral)"
        r"|(?:a\s+cada|de)\s+\d+\s*(?:meses|dias)|semestralmente|anualmente|trimestralmente",
        texto, re.IGNORECASE))

    mr.tem_referencia_politica = bool(re.search(
        r"pol[íi]tica\s+de\s+gest[aã]o\s+de\s+riscos?|gest[aã]o\s+de\s+riscos?\s+institucional"
        r"|invent[áa]rio\s+de\s+riscos?|metaprocesso|governan[çc]a"
        r"|Decreto\s+n[º°]?\s*9\.203|\bCOSO\b|ISO\s*31000|Resolu[çc][aã]o\s+CNMP",
        texto, re.IGNORECASE))

    # ── Grupo 7 — Encerramento ───────────────────────────────────────
    mr.tem_assinatura = bool(re.search(
        r"equipe\s+de\s+planejamento|integrante\s+requisitante|integrante\s+t[eé]cnico"
        r"|integrante\s+administrativo|assinad[oa]\s+eletronicamente|assinatura\s+eletr[oô]nica"
        r"|matr[íi]cula|cargo/fun[çc][aã]o|documento\s+assinado",
        texto[-5000:], re.IGNORECASE))

    return mr


# ─────────────────────────────────────────────────────────────────────
#  CHECKLIST DE CONFORMIDADE
# ─────────────────────────────────────────────────────────────────────

def _add(achados: list, **kwargs) -> None:
    kwargs["numero"] = len(achados) + 1
    achados.append(Achado(**kwargs))


def checar_vinculacao(mr: MR, achados: list) -> None:
    """Grupo 1 — Existência, vinculação processual e descrição da solução."""

    if not mr.tem_referencia_processo:
        _add(achados,
            titulo="Mapa de Riscos sem Identificação do Processo Administrativo",
            tipo="Vício Formal",
            localizacao="Cabeçalho / preâmbulo do Mapa de Riscos",
            inconsistencia=(
                "O Mapa de Riscos não identifica o número do processo administrativo "
                "SEI a que se refere. A vinculação processual expressa é indispensável "
                "para demonstrar que a análise de riscos foi elaborada especificamente "
                "para a contratação em exame, e não reaproveitada de outro procedimento."
            ),
            fundamentacao=(
                "Art. 12, I, e art. 18, X, da Lei nº 14.133/2021; art. 159, I, do "
                "Decreto Estadual (PI) nº 21.872/2023; art. 2º, parágrafo único, VIII, "
                "da Lei nº 9.784/1999."
            ),
            acao=(
                "Inserir no cabeçalho do Mapa de Riscos o número integral do processo "
                "SEI e a identificação da contratação a que se refere."
            ),
            sugestao=(
                "[Ex: 'MAPA DE RISCOS — Processo SEI nº [NN.NN.NNNN.NNNNNNN/AAAA-NN] "
                "— Objeto: [descrição sucinta].']"
            ),
        )

    if not mr.tem_descricao_solucao:
        _add(achados,
            titulo="Mapa de Riscos sem Descrição da Solução a Ser Contratada",
            tipo="Vício Formal",
            localizacao="Seção introdutória do Mapa de Riscos",
            inconsistencia=(
                "O Mapa de Riscos não descreve a solução a ser contratada. A descrição "
                "do objeto é premissa da análise de riscos: sem delimitar o que será "
                "contratado, não é possível verificar se os riscos catalogados são "
                "pertinentes, suficientes e proporcionais à contratação pretendida."
            ),
            fundamentacao=(
                "Art. 18, X, da Lei nº 14.133/2021; art. 29 do Decreto Estadual (PI) "
                "nº 21.872/2023; art. 26 da IN SEGES/MP nº 5/2017."
            ),
            acao=(
                "Inserir seção inicial descrevendo a solução a ser contratada, "
                "coincidente com a descrição constante do ETP e do TR, incluindo "
                "quantitativos, prazo de vigência e regime de execução."
            ),
            sugestao=(
                "[Ex: '1. DESCRIÇÃO DA SOLUÇÃO A SER CONTRATADA: Contratação de "
                "[objeto], pelo prazo de [X] meses, compreendendo [escopo], conforme "
                "detalhado no Termo de Referência (doc. SEI nº [ID]).']"
            ),
        )

    if not mr.tem_referencia_etp:
        _add(achados,
            titulo="Mapa de Riscos sem Referência aos Demais Artefatos de Planejamento",
            tipo="Sugestão de Melhoria",
            localizacao="Seção introdutória do Mapa de Riscos",
            inconsistencia=(
                "O Mapa de Riscos não referencia o DFD, o ETP ou o Termo de Referência "
                "da contratação. A vinculação expressa entre os artefatos é boa prática "
                "de governança: demonstra a coerência do planejamento e permite ao "
                "órgão de controle verificar que a análise de riscos considerou as "
                "premissas técnicas já estabelecidas."
            ),
            fundamentacao=(
                "Art. 18, caput e X, da Lei nº 14.133/2021; art. 29 do Decreto Estadual "
                "(PI) nº 21.872/2023; art. 14 da IN SEGES/ME nº 58/2022."
            ),
            acao=(
                "Referenciar no Mapa de Riscos os artefatos correlatos (DFD, ETP e TR), "
                "com os respectivos números de documento SEI."
            ),
            sugestao=(
                "[Ex: 'O presente Mapa de Riscos integra o planejamento da contratação "
                "instruída pelo DFD (doc. SEI nº [ID]), pelo ETP (doc. SEI nº [ID]) e "
                "pelo Termo de Referência (doc. SEI nº [ID]).']"
            ),
        )


def checar_estrutura_minima(mr: MR, achados: list) -> None:
    """Grupo 2 — Elementos obrigatórios do Mapa de Riscos."""

    if not mr.tem_identificacao_riscos:
        _add(achados,
            titulo="Mapa de Riscos sem Identificação Individualizada dos Eventos de Risco",
            tipo="Vício Material",
            localizacao="Corpo do Mapa de Riscos",
            inconsistencia=(
                "O Mapa de Riscos não apresenta os eventos de risco identificados de "
                "forma individualizada e catalogada. A identificação dos riscos é o "
                "elemento nuclear do documento — sem ela, o Mapa é apenas uma peça "
                "formal, incapaz de subsidiar decisões de tratamento e de servir como "
                "instrumento efetivo de controle interno."
            ),
            fundamentacao=(
                "Art. 18, X, e art. 169, caput, da Lei nº 14.133/2021; arts. 29 e 30 do "
                "Decreto Estadual (PI) nº 21.872/2023; art. 26 e Anexo IV da IN "
                "SEGES/MP nº 5/2017."
            ),
            acao=(
                "Estruturar o Mapa de Riscos em formato tabular, catalogando cada "
                "evento de risco com identificador único, descrição do evento, causa e "
                "consequência potencial."
            ),
            sugestao=(
                "[Estruturar tabela: 'RISCO 01 — Descrição: [evento]; Causa: [origem]; "
                "Consequência: [efeito sobre a contratação]. RISCO 02 — ...']"
            ),
        )
    elif mr.num_riscos_identificados and mr.num_riscos_identificados < MIN_RISCOS_ESPERADO:
        _add(achados,
            titulo=(
                f"Mapa de Riscos com Quantitativo Reduzido de Riscos Catalogados "
                f"({mr.num_riscos_identificados} identificado(s))"
            ),
            tipo="Sugestão de Melhoria",
            localizacao="Corpo do Mapa de Riscos",
            inconsistencia=(
                f"Foram identificados apenas {mr.num_riscos_identificados} evento(s) de "
                "risco no documento. Um Mapa de Riscos consistente deve contemplar, no "
                "mínimo, riscos relativos às três fases do processo — planejamento, "
                "seleção do fornecedor e gestão contratual —, além dos riscos "
                "específicos do objeto. Quantitativo reduzido pode indicar análise "
                "superficial ou reaproveitamento de modelo genérico."
            ),
            fundamentacao=(
                "Art. 18, X, e art. 169 da Lei nº 14.133/2021; art. 30 do Decreto "
                "Estadual (PI) nº 21.872/2023; Anexo IV da IN SEGES/MP nº 5/2017."
            ),
            acao=(
                "Revisar o Mapa de Riscos, complementando-o com os riscos específicos "
                "do objeto e com os riscos típicos de cada fase da contratação, "
                "utilizando como referência o Inventário de Riscos institucional e as "
                "listas de verificação do CNMP."
            ),
            sugestao=(
                "[Considerar riscos típicos: (i) planejamento — especificação "
                "inadequada, quantitativo superdimensionado, preço estimado "
                "desatualizado; (ii) seleção — licitação deserta ou fracassada, "
                "impugnação do edital, proposta inexequível; (iii) execução — atraso "
                "na entrega, qualidade inferior à contratada, inadimplemento de "
                "obrigações trabalhistas, descontinuidade do serviço.]"
            ),
        )

    if not mr.tem_probabilidade:
        _add(achados,
            titulo="Mapa de Riscos sem Avaliação da Probabilidade de Ocorrência dos Riscos",
            tipo="Vício Material",
            localizacao="Corpo do Mapa de Riscos — coluna de avaliação",
            inconsistencia=(
                "O Mapa de Riscos não atribui probabilidade de ocorrência a cada evento "
                "de risco identificado. A mensuração da probabilidade é elemento "
                "obrigatório da análise de riscos e condição para a priorização do "
                "tratamento — sem ela, todos os riscos aparentam igual relevância."
            ),
            fundamentacao=(
                "Art. 18, X, da Lei nº 14.133/2021; art. 30, II, do Decreto Estadual "
                "(PI) nº 21.872/2023; Anexo IV da IN SEGES/MP nº 5/2017; art. 17 do "
                "Decreto Federal nº 9.203/2017."
            ),
            acao=(
                "Acrescentar, para cada risco catalogado, a avaliação da probabilidade "
                "de ocorrência segundo escala objetiva previamente definida no próprio "
                "documento."
            ),
            sugestao=(
                "[Ex: adotar escala de 1 a 5 — '1 = Raro (improvável nos próximos "
                "5 anos); 2 = Pouco provável; 3 = Provável; 4 = Muito provável; "
                "5 = Praticamente certo'.]"
            ),
        )

    if not mr.tem_impacto:
        _add(achados,
            titulo="Mapa de Riscos sem Avaliação do Impacto Potencial dos Riscos",
            tipo="Vício Material",
            localizacao="Corpo do Mapa de Riscos — coluna de avaliação",
            inconsistencia=(
                "O Mapa de Riscos não avalia o impacto potencial de cada evento de "
                "risco caso este se concretize. A mensuração do impacto, ao lado da "
                "probabilidade, compõe o cálculo do nível de risco e orienta a "
                "alocação dos esforços de controle."
            ),
            fundamentacao=(
                "Art. 18, X, da Lei nº 14.133/2021; art. 30, III, do Decreto Estadual "
                "(PI) nº 21.872/2023; Anexo IV da IN SEGES/MP nº 5/2017."
            ),
            acao=(
                "Acrescentar, para cada risco catalogado, a avaliação do impacto "
                "segundo escala objetiva, considerando dimensões como custo, prazo, "
                "qualidade do serviço, imagem institucional e continuidade das "
                "atividades finalísticas."
            ),
            sugestao=(
                "[Ex: adotar escala de 1 a 5 — '1 = Muito baixo (efeito desprezível); "
                "3 = Moderado (atraso ou custo adicional relevante); 5 = Muito alto "
                "(interrupção de atividade finalística ou dano reputacional grave)'.]"
            ),
        )

    if not mr.tem_nivel_risco:
        _add(achados,
            titulo="Mapa de Riscos sem Classificação do Nível de Risco (Criticidade)",
            tipo="Vício Material",
            localizacao="Corpo do Mapa de Riscos — coluna de classificação",
            inconsistencia=(
                "O Mapa de Riscos não apresenta a classificação do nível de risco "
                "(criticidade) resultante da combinação entre probabilidade e impacto. "
                "A classificação é o que permite priorizar o tratamento e definir quais "
                "riscos exigem ação imediata, quais serão monitorados e quais podem ser "
                "aceitos."
            ),
            fundamentacao=(
                "Art. 18, X, e art. 169, I, da Lei nº 14.133/2021; art. 30, IV, do "
                "Decreto Estadual (PI) nº 21.872/2023; art. 17 do Decreto Federal "
                "nº 9.203/2017; Anexo IV da IN SEGES/MP nº 5/2017."
            ),
            acao=(
                "Calcular e registrar o nível de risco de cada evento (probabilidade × "
                "impacto), classificando-o em faixas objetivas (ex.: baixo, médio, alto, "
                "crítico) e explicitando a matriz de severidade adotada."
            ),
            sugestao=(
                "[Ex: 'Nível de Risco = Probabilidade × Impacto. Faixas: 1–4 = BAIXO "
                "(aceitar e monitorar); 5–9 = MÉDIO (mitigar); 10–16 = ALTO (mitigar "
                "prioritariamente); 17–25 = CRÍTICO (evitar ou transferir).']"
            ),
        )

    if (mr.tem_probabilidade or mr.tem_impacto) and not mr.tem_escala_criterios:
        _add(achados,
            titulo="Mapa de Riscos sem Explicitação da Escala e dos Critérios de Avaliação Adotados",
            tipo="Sugestão de Melhoria",
            localizacao="Seção metodológica do Mapa de Riscos",
            inconsistencia=(
                "O Mapa de Riscos atribui valores de probabilidade e/ou impacto sem "
                "explicitar a escala e os critérios objetivos que fundamentam a "
                "pontuação. Sem a legenda metodológica, as notas atribuídas tornam-se "
                "subjetivas e não auditáveis, comprometendo a reprodutibilidade da "
                "análise."
            ),
            fundamentacao=(
                "Art. 169, I, da Lei nº 14.133/2021; art. 30 do Decreto Estadual (PI) "
                "nº 21.872/2023; art. 17 do Decreto Federal nº 9.203/2017; ABNT NBR "
                "ISO 31000 (gestão de riscos — diretrizes)."
            ),
            acao=(
                "Inserir seção metodológica descrevendo a escala adotada para "
                "probabilidade e impacto, os critérios de enquadramento em cada nível "
                "e a matriz de severidade utilizada para o cálculo do nível de risco."
            ),
            sugestao=(
                "[Ex: 'METODOLOGIA: A avaliação seguiu a metodologia da Política de "
                "Gestão de Riscos do MPPI, com escalas de 1 a 5 para probabilidade e "
                "impacto, conforme legendas abaixo, e cálculo do nível de risco pelo "
                "produto P × I.']"
            ),
        )


def checar_tratamento(mr: MR, achados: list) -> None:
    """Grupo 3 — Tratamento dos riscos e responsáveis."""

    if not mr.tem_acoes_preventivas:
        _add(achados,
            titulo="Mapa de Riscos sem Ações Preventivas ou de Mitigação",
            tipo="Vício Material",
            localizacao="Corpo do Mapa de Riscos — coluna de tratamento",
            inconsistencia=(
                "O Mapa de Riscos identifica eventos de risco mas não define as ações "
                "preventivas ou de mitigação a serem adotadas. A definição do tratamento "
                "é a finalidade prática do documento: sem ela, o Mapa cumpre função "
                "meramente descritiva e não produz efeito útil sobre a gestão da "
                "contratação."
            ),
            fundamentacao=(
                "Art. 18, X, e art. 169, caput e I, da Lei nº 14.133/2021; art. 30, V, "
                "do Decreto Estadual (PI) nº 21.872/2023; art. 26 e Anexo IV da IN "
                "SEGES/MP nº 5/2017."
            ),
            acao=(
                "Definir, para cada risco catalogado, as ações preventivas concretas — "
                "isto é, as medidas a serem adotadas antes da materialização do risco, "
                "voltadas a reduzir sua probabilidade de ocorrência ou seu impacto."
            ),
            sugestao=(
                "[Ex: 'RISCO: Entrega em desacordo com a especificação. AÇÃO "
                "PREVENTIVA: Exigir amostra ou prova de conceito antes da adjudicação; "
                "detalhar as especificações técnicas no TR com parâmetros mensuráveis; "
                "prever recebimento provisório com prazo para verificação técnica.']"
            ),
        )

    if not mr.tem_acoes_contingencia:
        _add(achados,
            titulo="Mapa de Riscos sem Ações de Contingência para Riscos Materializados",
            tipo="Vício Formal",
            localizacao="Corpo do Mapa de Riscos — coluna de contingência",
            inconsistencia=(
                "O Mapa de Riscos não define as ações de contingência a serem adotadas "
                "caso os riscos identificados venham efetivamente a se concretizar. O "
                "planejamento das respostas — distinto das medidas preventivas — é "
                "elemento próprio da análise de riscos e assegura resposta tempestiva "
                "durante a execução contratual."
            ),
            fundamentacao=(
                "Art. 18, X, e art. 169 da Lei nº 14.133/2021; art. 30, VI, do Decreto "
                "Estadual (PI) nº 21.872/2023; Anexo IV da IN SEGES/MP nº 5/2017."
            ),
            acao=(
                "Definir, para cada risco de nível médio ou superior, as ações de "
                "contingência aplicáveis após a materialização do evento, indicando o "
                "procedimento, o prazo de resposta e o responsável pelo acionamento."
            ),
            sugestao=(
                "[Ex: 'RISCO: Inadimplemento da contratada. AÇÃO DE CONTINGÊNCIA: "
                "Notificar formalmente a contratada com prazo de [X] dias para "
                "regularização; não havendo regularização, instaurar processo "
                "sancionatório e avaliar a contratação remanescente nos termos do "
                "art. 90, § 7º, da Lei nº 14.133/2021.']"
            ),
        )

    if not mr.tem_responsaveis:
        _add(achados,
            titulo="Mapa de Riscos sem Indicação dos Responsáveis pelo Tratamento dos Riscos",
            tipo="Vício Material",
            localizacao="Corpo do Mapa de Riscos — coluna de responsáveis",
            inconsistencia=(
                "O Mapa de Riscos não indica os responsáveis pela implementação das "
                "ações de tratamento e pelo monitoramento de cada risco identificado. "
                "A atribuição nominal ou setorial de responsabilidade é requisito de "
                "efetividade do documento — ações sem responsável designado tendem a "
                "não ser executadas."
            ),
            fundamentacao=(
                "Art. 18, X, e art. 169, § 1º, da Lei nº 14.133/2021; art. 30, VII, do "
                "Decreto Estadual (PI) nº 21.872/2023; art. 17 do Decreto Federal "
                "nº 9.203/2017."
            ),
            acao=(
                "Indicar, para cada risco, a unidade ou o agente responsável pela "
                "implementação da ação preventiva, pela ação de contingência e pelo "
                "monitoramento contínuo."
            ),
            sugestao=(
                "[Ex: acrescentar colunas 'Responsável pela Ação Preventiva' e "
                "'Responsável pelo Monitoramento', preenchidas com a unidade "
                "(ex.: Coordenadoria requisitante, CLC/ASSCOMPRAS, Fiscal do Contrato) "
                "ou o cargo do agente designado.]"
            ),
        )


def checar_abrangencia(mr: MR, achados: list) -> None:
    """Grupo 4 — Abrangência do Mapa quanto às fases do processo."""

    fases_ausentes = []
    if not mr.tem_riscos_planejamento:
        fases_ausentes.append("planejamento da contratação")
    if not mr.tem_riscos_selecao:
        fases_ausentes.append("seleção do fornecedor")
    if not mr.tem_riscos_execucao:
        fases_ausentes.append("gestão do contrato")

    if fases_ausentes:
        _add(achados,
            titulo=(
                "Mapa de Riscos sem Cobertura das Fases: "
                + ", ".join(fases_ausentes)
            ),
            tipo="Vício Formal",
            localizacao="Corpo do Mapa de Riscos",
            inconsistencia=(
                "O Mapa de Riscos não contempla riscos relativos à(s) seguinte(s) "
                f"fase(s) do processo de contratação: {', '.join(fases_ausentes)}. A "
                "análise de riscos deve abranger o metaprocesso de contratação em sua "
                "integralidade — do planejamento à gestão contratual —, sob pena de "
                "deixar descobertas etapas críticas do ciclo."
            ),
            fundamentacao=(
                "Art. 18, X, e art. 169, caput, da Lei nº 14.133/2021; art. 29 e "
                "art. 30 do Decreto Estadual (PI) nº 21.872/2023; art. 26 e Anexo IV "
                "da IN SEGES/MP nº 5/2017 (riscos do processo de contratação e da "
                "gestão contratual)."
            ),
            acao=(
                "Complementar o Mapa de Riscos com eventos relativos a todas as fases "
                "do processo, organizando o documento por fase para facilitar a "
                "verificação da cobertura integral."
            ),
            sugestao=(
                "[Estruturar em três blocos: 'A. RISCOS DA FASE DE PLANEJAMENTO' "
                "(ex.: especificação inadequada, quantitativo mal dimensionado, preço "
                "estimado desatualizado); 'B. RISCOS DA FASE DE SELEÇÃO DO FORNECEDOR' "
                "(ex.: certame deserto ou fracassado, impugnação, proposta inexequível); "
                "'C. RISCOS DA GESTÃO CONTRATUAL' (ex.: atraso na entrega, qualidade "
                "inferior, inadimplemento trabalhista, descontinuidade do serviço).]"
            ),
        )


def checar_matriz_alocacao(mr: MR, achados: list) -> None:
    """Grupo 5 — Matriz de alocação de riscos entre contratante e contratado."""

    if not mr.tem_matriz_alocacao:
        _add(achados,
            titulo="Ausência de Matriz de Alocação de Riscos entre Contratante e Contratado",
            tipo="Sugestão de Melhoria",
            localizacao="Seção final do Mapa de Riscos",
            inconsistencia=(
                "O documento não apresenta matriz de alocação de riscos definindo a "
                "responsabilidade de cada parte — contratante e contratado — sobre os "
                "riscos contratuais. A matriz é obrigatória nas contratações de valor "
                "estimado superior a 2% do limite do art. 6º, XXII, da Lei nº "
                "14.133/2021, nos termos do art. 34 do Decreto Estadual (PI) nº "
                "21.872/2023, e recomendável nas demais, por delimitar previamente as "
                "hipóteses de reequilíbrio econômico-financeiro."
            ),
            fundamentacao=(
                "Art. 22, caput e § 3º, art. 103 e art. 124, II, 'd', da Lei nº "
                "14.133/2021; art. 34 do Decreto Estadual (PI) nº 21.872/2023."
            ),
            acao=(
                "Verificar se a contratação supera o limite do art. 34 do Decreto "
                "Estadual nº 21.872/2023. Em caso positivo, elaborar matriz de alocação "
                "de riscos, alocando cada risco relevante à parte com melhor condição "
                "de geri-lo e definindo as consequências contratuais. Em caso negativo, "
                "registrar expressamente a hipótese de dispensa."
            ),
            sugestao=(
                "[Ex MATRIZ: tabela com colunas 'Risco | Alocado a (Contratante / "
                "Contratado) | Consequência contratual | Enseja reequilíbrio? (Sim/Não)'. "
                "| Ex DISPENSA: 'Não foi elaborada matriz de alocação de riscos, pois "
                "o valor estimado da contratação (R$ [X]) não supera o limite previsto "
                "no art. 34 do Decreto Estadual (PI) nº 21.872/2023, e a contratação "
                "não apresenta riscos relevantes com impacto sobre o equilíbrio "
                "econômico-financeiro do contrato.']"
            ),
        )


def checar_monitoramento(mr: MR, achados: list) -> None:
    """Grupo 6 — Monitoramento, revisão e alinhamento à governança."""

    if not mr.tem_monitoramento:
        _add(achados,
            titulo="Mapa de Riscos sem Mecanismos de Monitoramento Contínuo",
            tipo="Vício Formal",
            localizacao="Seção final do Mapa de Riscos",
            inconsistencia=(
                "O Mapa de Riscos não estabelece mecanismos de monitoramento contínuo "
                "dos riscos identificados. A gestão de riscos é processo dinâmico: sem "
                "previsão de acompanhamento, o Mapa cristaliza uma fotografia do "
                "momento do planejamento e perde utilidade ao longo da execução "
                "contratual."
            ),
            fundamentacao=(
                "Art. 169, caput e §§ 1º e 3º, da Lei nº 14.133/2021; art. 33 do "
                "Decreto Estadual (PI) nº 21.872/2023; art. 17 do Decreto Federal "
                "nº 9.203/2017."
            ),
            acao=(
                "Inserir seção definindo como os riscos serão monitorados durante a "
                "execução contratual, indicando o instrumento de registro (relatório "
                "de fiscalização, check-list, sistema) e o agente responsável."
            ),
            sugestao=(
                "[Ex: 'MONITORAMENTO: Os riscos catalogados serão monitorados pelo "
                "fiscal do contrato, que registrará em relatório mensal de "
                "fiscalização a ocorrência ou iminência de qualquer dos eventos "
                "mapeados, comunicando de imediato ao gestor do contrato os riscos de "
                "nível alto ou crítico.']"
            ),
        )

    if not mr.tem_periodicidade_revisao:
        _add(achados,
            titulo="Mapa de Riscos sem Previsão de Periodicidade para Revisão e Atualização",
            tipo="Sugestão de Melhoria",
            localizacao="Seção final do Mapa de Riscos",
            inconsistencia=(
                "O Mapa de Riscos não estabelece periodicidade para a sua revisão e "
                "atualização. A definição de um ciclo de revisão assegura que o "
                "documento acompanhe as mudanças de contexto — alteração de "
                "quantitativos, prorrogações contratuais, novas exigências normativas "
                "ou riscos emergentes não previstos no planejamento inicial."
            ),
            fundamentacao=(
                "Art. 169, § 1º, da Lei nº 14.133/2021; art. 33 do Decreto Estadual "
                "(PI) nº 21.872/2023; ABNT NBR ISO 31000."
            ),
            acao=(
                "Definir no Mapa de Riscos a periodicidade de revisão e os eventos que "
                "disparam revisão extraordinária (prorrogação, aditivo quantitativo, "
                "materialização de risco crítico), bem como o responsável pela "
                "atualização."
            ),
            sugestao=(
                "[Ex: 'REVISÃO: O presente Mapa de Riscos será revisado semestralmente "
                "pela equipe de fiscalização e, extraordinariamente, sempre que houver "
                "prorrogação contratual, celebração de termo aditivo ou materialização "
                "de risco classificado como alto ou crítico.']"
            ),
        )

    if not mr.tem_referencia_politica:
        _add(achados,
            titulo="Mapa de Riscos sem Referência às Diretrizes Institucionais de Gestão de Riscos",
            tipo="Sugestão de Melhoria",
            localizacao="Seção introdutória / metodológica do Mapa de Riscos",
            inconsistencia=(
                "O Mapa de Riscos não referencia a Política de Gestão de Riscos "
                "institucional, o Inventário de Riscos do metaprocesso de contratações "
                "ou metodologia de referência reconhecida. O alinhamento às diretrizes "
                "institucionais assegura uniformidade metodológica entre os processos "
                "e permite a consolidação dos riscos em nível organizacional."
            ),
            fundamentacao=(
                "Art. 11, parágrafo único, e art. 169, caput, da Lei nº 14.133/2021; "
                "art. 29 do Decreto Estadual (PI) nº 21.872/2023; art. 17 do Decreto "
                "Federal nº 9.203/2017; Resolução CNMP sobre gestão de riscos; "
                "ABNT NBR ISO 31000."
            ),
            acao=(
                "Referenciar na introdução do Mapa a Política de Gestão de Riscos do "
                "MPPI (ou, na sua ausência, a metodologia adotada) e registrar se os "
                "riscos catalogados no Inventário de Riscos do metaprocesso de "
                "contratações foram considerados."
            ),
            sugestao=(
                "[Ex: 'A presente Análise de Riscos foi elaborada em conformidade com "
                "a Política de Gestão de Riscos do MPPI e considerou, além dos riscos "
                "específicos desta contratação, os riscos catalogados no Inventário de "
                "Riscos do metaprocesso de contratações públicas.']"
            ),
        )


def checar_assinatura(mr: MR, achados: list) -> None:
    """Grupo 7 — Assinatura pela Equipe de Planejamento."""

    if not mr.tem_assinatura:
        _add(achados,
            titulo="Mapa de Riscos sem Evidência de Assinatura pela Equipe de Planejamento",
            tipo="Vício Formal",
            localizacao="Seção de assinaturas do Mapa de Riscos",
            inconsistencia=(
                "O Mapa de Riscos não apresenta evidência de assinatura pelos "
                "integrantes da Equipe de Planejamento da Contratação. A subscrição do "
                "documento pelos mesmos servidores que elaboraram o DFD e o ETP é "
                "condição de validade formal e demonstra a assunção de responsabilidade "
                "técnica sobre a análise realizada."
            ),
            fundamentacao=(
                "Art. 7º, caput, e art. 18, X, da Lei nº 14.133/2021; art. 19 do "
                "Decreto Estadual (PI) nº 21.872/2023; art. 8º da IN SEGES/ME nº 81/2022."
            ),
            acao=(
                "Assinar eletronicamente o Mapa de Riscos no SEI, com a subscrição de "
                "todos os integrantes designados para a Equipe de Planejamento da "
                "Contratação, antes da submissão à autoridade competente."
            ),
            sugestao=(
                "[Assinar o documento no SEI com os três integrantes: Integrante "
                "Requisitante (área demandante), Integrante Técnico (área técnica) e "
                "Integrante Administrativo (ASSCOMPRAS/CLC), qualificando nome, "
                "cargo/função e matrícula.]"
            ),
        )


def checar_quesitos_json(mr: MR, achados: list) -> None:
    """Verifica quesitos declarativos definidos em quesitos_MR.json."""
    import json
    caminho_json = BASE_DIR / "quesitos_MR.json"
    if not caminho_json.exists():
        return
    try:
        with open(caminho_json, encoding="utf-8") as f:
            dados = json.load(f)
    except Exception:
        return
    texto = mr.texto_completo
    is_tic = mr.is_tic
    for q in dados.get("quesitos", []):
        if q.get("is_tic_only") and not is_tic:
            continue
        if q.get("is_servico_only") and not mr.is_servico:
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

def salvar_achados_json(mr: MR, achados: list, caminho_origem: str) -> str:
    """Salva os achados em JSON para consolidação posterior no Ofício final."""
    import json
    base = Path(caminho_origem).stem
    pasta = Path(caminho_origem).parent
    caminho_json = str(pasta / f"achados_MR_{base}.json")

    dados = {
        "artefato": "MR",
        "num_processo": mr.num_processo or "",
        "objeto": mr.objeto_descricao or "",
        "unidade": mr.unidade_requisitante or "",
        "is_tic": mr.is_tic,
        "data_analise": DATA_ANALISE,
        "arquivo_origem": Path(caminho_origem).name,
        "riscos_identificados": mr.num_riscos_identificados,
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


def gerar_oficio_word(mr: MR, achados: list, caminho_saida: str):
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

    unidade  = mr.unidade_requisitante or "[Unidade Requisitante]"
    processo = mr.num_processo         or "[nº do processo SEI]"
    tipo_tag = " — Solução de TIC" if mr.is_tic else ""

    p = doc.add_paragraph()
    p.add_run(f"À {unidade}").bold = True
    p = doc.add_paragraph()
    p.add_run(
        f"Assunto: Devolução de Autos para Saneamento — "
        f"Análise do Mapa de Riscos{tipo_tag} — "
        f"Processo SEI nº {processo}."
    ).bold = True

    doc.add_paragraph()
    doc.add_paragraph().add_run("Senhor(a) Coordenador(a),")
    doc.add_paragraph()

    abertura = [
        (
            "Cumprimentando-o cordialmente, registro que a equipe desta Assessoria "
            "analisou o Mapa de Riscos juntado aos autos do processo em referência, "
            "verificando a conformidade do documento com os normativos aplicáveis: "
            "Lei nº 14.133/2021, Decreto Estadual (PI) nº 21.872/2023, IN SEGES/MP "
            "nº 5/2017, Decreto Federal nº 9.203/2017 e Atos PGJ/MPPI nº 1.381 e "
            "1.382/2024"
            + (", Resolução CNMP nº 283/2024 e MOTec" if mr.is_tic else "") + "."
        ),
        (
            "Na qualidade de Agente de Contratação responsável pela análise de "
            "conformidade da fase preparatória, e em cumprimento ao disposto no "
            "art. 53 da Lei nº 14.133/2021, restituo o presente feito para saneamento "
            "das inconsistências identificadas. Os apontamentos possuem caráter "
            "eminentemente colaborativo, visando conferir segurança jurídica, "
            "transparência e eficiência ao procedimento."
        ),
        (
            "A seguir, apresentam-se os achados estruturados, com a respectiva "
            "fundamentação legal, ação de saneamento e sugestão de texto, quando "
            "aplicável. As redações sugeridas têm caráter meramente exemplificativo "
            "e orientativo, competindo à equipe de planejamento avaliar sua "
            "pertinência frente à realidade técnica e fática do objeto:"
        ),
    ]
    for txt in abertura:
        p = doc.add_paragraph()
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.first_line_indent = Cm(1.25)
        p.add_run(txt)

    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run("1. ARTEFATO: MAPA DE RISCOS (MR)").bold = True
    doc.add_paragraph()

    if not achados:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(1)
        p.add_run(
            "Nenhuma inconsistência identificada. Mapa de Riscos em conformidade "
            "com os normativos aplicáveis."
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
        "Salientamos que um Mapa de Riscos consistente não apenas atende a exigência "
        "formal da legislação, como fornece aos fiscais e gestores instrumento "
        "concreto de antecipação de problemas durante a execução contratual, "
        "prevenindo prejuízos ao erário e questionamentos dos órgãos de controle."
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

def imprimir_relatorio(mr: MR, achados: list):
    sep = "─" * 68
    print(f"\n{'═' * 68}")
    print(f"  ANÁLISE DE CONFORMIDADE — MAPA DE RISCOS  (v{VERSION})")
    print(f"{'═' * 68}")
    print(f"  Processo: {mr.num_processo or '(não identificado)'}")
    print(f"  Unidade : {mr.unidade_requisitante or '(não identificada)'}")
    print(f"  Objeto  : {(mr.objeto_descricao or '(não identificado)')[:70]}...")
    flags_cls = []
    if mr.is_tic:     flags_cls.append("TIC")
    if mr.is_servico: flags_cls.append("Serviço")
    if mr.is_obra:    flags_cls.append("Obra/Engenharia")
    print(f"  Tipo    : {', '.join(flags_cls) or '(não classificado)'}")
    print(f"  Riscos  : ~{mr.num_riscos_identificados} evento(s) catalogado(s)")
    print(f"  Data    : {DATA_ANALISE}")
    print(sep)

    checks = [
        ("Referência ao processo",      mr.tem_referencia_processo),
        ("Descrição da solução",        mr.tem_descricao_solucao),
        ("Referência a DFD/ETP/TR",     mr.tem_referencia_etp),
        ("Riscos identificados",        mr.tem_identificacao_riscos),
        ("Probabilidade",               mr.tem_probabilidade),
        ("Impacto",                     mr.tem_impacto),
        ("Nível de risco / criticidade", mr.tem_nivel_risco),
        ("Escala e critérios",          mr.tem_escala_criterios),
        ("Ações preventivas",           mr.tem_acoes_preventivas),
        ("Ações de contingência",       mr.tem_acoes_contingencia),
        ("Responsáveis indicados",      mr.tem_responsaveis),
        ("Riscos do planejamento",      mr.tem_riscos_planejamento),
        ("Riscos da seleção",           mr.tem_riscos_selecao),
        ("Riscos da execução",          mr.tem_riscos_execucao),
        ("Matriz de alocação",          mr.tem_matriz_alocacao),
        ("Monitoramento",               mr.tem_monitoramento),
        ("Periodicidade de revisão",    mr.tem_periodicidade_revisao),
        ("Política/metodologia",        mr.tem_referencia_politica),
        ("Assinatura",                  mr.tem_assinatura),
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

    mr = parse_mr(texto)
    achados: list = []

    checar_vinculacao(mr, achados)
    checar_estrutura_minima(mr, achados)
    checar_tratamento(mr, achados)
    checar_abrangencia(mr, achados)
    checar_matriz_alocacao(mr, achados)
    checar_monitoramento(mr, achados)
    checar_assinatura(mr, achados)
    checar_quesitos_json(mr, achados)

    print(f"      {len(achados)} achado(s) identificado(s)")
    imprimir_relatorio(mr, achados)

    salvar_achados_json(mr, achados, caminho)

    if "--oficio" in sys.argv:
        base = Path(caminho).stem
        saida = str(Path(caminho).parent / f"Oficio_ASSCOMPRAS_MR_{base}.docx")
        gerar_oficio_word(mr, achados, saida)
    else:
        print("ℹ  Para gerar o Ofício Word desta análise isolada, use: --oficio")
        print("ℹ  Para consolidar todos os artefatos do processo, use: gerar_oficio_processo.py\n")


if __name__ == "__main__":
    main()
