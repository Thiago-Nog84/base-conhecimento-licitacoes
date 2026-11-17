#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════╗
║  Analisador de TR — ASSCOMPRAS / MPPI                   v1.0        ║
║  Coordenadoria de Licitações e Contratos                             ║
╚══════════════════════════════════════════════════════════════════════╝

Analisa o Termo de Referência (TR) exportado do SEI (PDF ou HTML)
e gera automaticamente:

  1. Arquivo JSON com achados de conformidade (achados_TR_*.json)
  2. Relatório resumido no terminal
  3. Ofício ASSCOMPRAS (.docx), se solicitado com --oficio

Requisitos (instale uma única vez):
    pip install pdfplumber beautifulsoup4 lxml python-docx

Uso:
    python analisar_tr.py "caminho\\para\\tr.pdf"
    python analisar_tr.py "caminho\\para\\tr.html"
    python analisar_tr.py "caminho\\para\\tr.pdf" --oficio

⚠ IMPORTANTE: Revise e complemente os achados gerados. A análise
  automática identifica achados comuns mas não substitui a avaliação
  jurídica e técnica do Agente de Contratação.
"""

import sys
import os
import re
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

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
class TR:
    texto_completo: str = ""
    num_processo:   str = ""
    objeto_descricao: str = ""
    unidade_requisitante: str = ""

    # Classificação do objeto
    is_tic:      bool = False
    is_servico:  bool = False
    is_bem:      bool = False
    is_continuo: bool = False   # serviço de execução continuada

    # Grupo 1 — Existência e elaboração
    tem_assinatura: bool = False

    # Grupo 2 — Conteúdo essencial
    tem_referencia_etp:              bool = False
    tem_referencia_pca:              bool = False
    tem_justificativa_parcelamento:  bool = False

    # Grupo 3 — Especificação
    tem_indicacao_marca:  bool = False   # flag: marca detectada (checar contexto)
    tem_justif_marca:     bool = False

    # Grupo 4 — Quantitativos e valor
    tem_memoria_calculo:  bool = False
    tem_preco_referencial: bool = False
    tem_fonte_recursos:   bool = False

    # Grupo 5 — Habilitação
    tem_habilitacao:      bool = False

    # Grupo 6 — Sustentabilidade e riscos
    tem_sustentabilidade: bool = False
    tem_mapa_riscos:      bool = False

    # Grupo 8 — Julgamento
    tem_criterio_julgamento: bool = False

    # Grupo 9 — Modelo de execução e recebimento
    tem_modelo_execucao:       bool = False
    tem_recebimento_provisorio: bool = False
    tem_recebimento_definitivo: bool = False

    # Grupo 10 — Gestão do contrato
    tem_modelo_gestao:     bool = False
    tem_condicoes_pagamento: bool = False
    tem_sancoes:           bool = False
    tem_fiscal_gestor:     bool = False

    # Grupo 11 — Disposições finais
    tem_prazo_vigencia:   bool = False
    tem_pncp_referencia:  bool = False


# ─────────────────────────────────────────────────────────────────────
#  EXTRAÇÃO DE TEXTO
# ─────────────────────────────────────────────────────────────────────

def _erro(msg: str):
    print(f"\n❌ ERRO: {msg}\n", file=sys.stderr)
    sys.exit(1)


def _caminho_seguro(caminho: str) -> str:
    import shutil, tempfile
    ext = Path(caminho).suffix.lower()
    dest = os.path.join(tempfile.gettempdir(), f"tr_temp{ext}")
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
#  PARSING DO TR
# ─────────────────────────────────────────────────────────────────────

def parse_tr(texto: str) -> TR:
    tr = TR()
    tr.texto_completo = texto

    # Número do processo SEI
    m = re.search(r"\b(\d{2}\.\d{2}\.\d{4}\.\d{7}/\d{4}-\d{2})\b", texto)
    if m:
        tr.num_processo = m.group(1)

    # Objeto/descrição
    m = re.search(r"(?:objeto[:\s]+|OBJETO[:\s]+)(.{20,400}?)(?:\n[A-Z\d]|\Z)",
                  texto, re.DOTALL)
    if m:
        tr.objeto_descricao = m.group(1).strip()[:300]
    else:
        m2 = re.search(
            r"(?:Contrata[çc][aã]o|Aquisi[çc][aã]o|Presta[çc][aã]o)[^\n]*\n"
            r"([A-ZA-záéíóúàâêôãõç][^.]{30,300}\.)",
            texto, re.DOTALL
        )
        if m2:
            tr.objeto_descricao = m2.group(1).strip()[:300]

    # Unidade requisitante
    for pat in [
        r"(?:Unidade\s+Requisitante|[Áa]rea\s+Requisitante|[Óo]rg[aã]o\s+Requisitante)[:\s]+([^\n]{5,80})",
        r"(?:Órgão|Institui[çc][aã]o)[:\s]+([A-ZÁÉÍÓÚ][^\n]{4,60})",
    ]:
        m = re.search(pat, texto[:3000], re.IGNORECASE)
        if m:
            tr.unidade_requisitante = m.group(1).strip()
            break

    # ── Classificação do objeto ──────────────────────────────────────
    tr.is_tic = bool(re.search(
        r"\bTIC\b|tecnologia\s+da\s+informa[çc][aã]o|software|hardware"
        r"|sistema\s+de\s+informa[çc][aã]o|solu[çc][aã]o\s+de\s+TI"
        r"|contrata[çc][aã]o\s+de\s+TI|CNMP\s+n[º°]?\s*283|MOTec",
        texto, re.IGNORECASE
    ))

    tr.is_servico = bool(re.search(
        r"presta[çc][aã]o\s+de\s+servi[çc]o|contrata[çc][aã]o\s+de\s+servi[çc]o"
        r"|servi[çc]os?\s+de\s+(?:limpeza|vigilância|copa|recepção|informática|manutenção)"
        r"|servi[çc]os?\s+t[eé]cnicos?|execu[çc][aã]o\s+de\s+servi[çc]o",
        texto[:5000], re.IGNORECASE
    ))

    tr.is_bem = bool(re.search(
        r"\baquisi[çc][aã]o\b|\bcompra\b|fornecimento\s+de\s+(?:material|produto|equipamento)"
        r"|material\s+de\s+consumo|material\s+de\s+expediente|bens?\s+(?:m[oó]veis|duráveis)",
        texto[:5000], re.IGNORECASE
    ))

    tr.is_continuo = bool(re.search(
        r"execu[çc][aã]o\s+continuada|servi[çc]o\s+contínuo|natureza\s+continuada"
        r"|servi[çc]os?\s+continuados?|de\s+execu[çc][aã]o\s+continuada"
        r"|prorroga[çc][aã]o.*(?:art\.?\s*107|art\.?\s*106)",
        texto, re.IGNORECASE
    ))

    # ── Grupo 1 — Assinatura ─────────────────────────────────────────
    tr.tem_assinatura = bool(re.search(
        r"equipe\s+de\s+planejamento|integrante\s+requisitante|integrante\s+t[eé]cnico"
        r"|integrante\s+administrativo|assinado\s+por|data[:\s]+\d{2}/\d{2}"
        r"|responsável.*elabora[çc][aã]o",
        texto[-4000:], re.IGNORECASE
    ))

    # ── Grupo 2 — Conteúdo essencial ─────────────────────────────────
    tr.tem_referencia_etp = bool(re.search(
        r"\bETP\b|Estudo\s+T[eé]cnico\s+Preliminar|estudo\s+preliminar.*contrata[çc][aã]o",
        texto, re.IGNORECASE
    ))

    tr.tem_referencia_pca = bool(re.search(
        r"\bPCA\b|Plano\s+de\s+Contrata[çc][oõ]es\s+Anual|plano\s+anual\s+de\s+contrata[çc][oõ]es",
        texto, re.IGNORECASE
    ))

    tr.tem_justificativa_parcelamento = bool(re.search(
        r"parcelamento|n[aã]o\s+parcel|lote\s+[úu]nico|objeto\s+(?:[úu]nico|uno|indivisível)"
        r"|indivisibilidade|n[aã]o\s+ser[aá]\s+parcelado|parcelamento\s+n[aã]o",
        texto, re.IGNORECASE
    ))

    # ── Grupo 3 — Especificação ───────────────────────────────────────
    tr.tem_indicacao_marca = bool(re.search(
        r"\bmarca\b.*(?:específica|referência|padr[aã]o|\w+®)|modelo\s+[A-Z0-9]{3,}"
        r"|fabricante\s+\w+",
        texto, re.IGNORECASE
    ))
    tr.tem_justif_marca = bool(re.search(
        r"justificativa.*(?:marca|modelo)|(?:marca|modelo).*justif"
        r"|padroniza[çc][aã]o.*(?:marca|modelo)|compatibilidade.*(?:existente|instalado)"
        r"|art\.?\s*41.*14\.133",
        texto, re.IGNORECASE
    ))

    # ── Grupo 4 — Quantitativos e valor ──────────────────────────────
    tr.tem_memoria_calculo = bool(re.search(
        r"mem[oó]ria\s+de\s+c[áa]lculo|planilha\s+de\s+c[áa]lculo"
        r"|hist[oó]rico\s+de\s+consumo|consumo\s+(?:m[eé]dio|anterior|registrado)"
        r"|s[eé]rie\s+hist[oó]rica|base\s+de\s+c[áa]lculo|exerc[ií]cio\s+anterior"
        r"|m[eé]dia\s+(?:mensal|anual)|n[uú]mero\s+de\s+usu[áa]rios",
        texto, re.IGNORECASE
    ))

    tr.tem_preco_referencial = bool(re.search(
        r"painel\s+de\s+pre[çc]os?|pesquisa\s+de\s+(?:pre[çc]os?|mercado)"
        r"|comprasnet|ata\s+de\s+registro|proposta\s+comercial|or[çc]amento"
        r"|pre[çc]o\s+referencial|pre[çc]o\s+de\s+refer[eê]ncia"
        r"|pre[çc]o\s+unit[áa]rio|contrata[çc][aã]o\s+similar|banco\s+de\s+pre[çc]os?",
        texto, re.IGNORECASE
    ))

    tr.tem_fonte_recursos = bool(re.search(
        r"elemento\s+de\s+despesa|fonte\s+de\s+recurso|dota[çc][aã]o\s+or[çc]ament[áa]ria"
        r"|unidade\s+gestora|UG\s*250|cr[eé]dito\s+or[çc]ament[áa]rio"
        r"|PGJ|FMMPI|FPROCON",
        texto, re.IGNORECASE
    ))

    # ── Grupo 5 — Habilitação ─────────────────────────────────────────
    tr.tem_habilitacao = bool(re.search(
        r"habilita[çc][aã]o|qualifica[çc][aã]o\s+t[eé]cnica|qualifica[çc][aã]o\s+econ[oô]mico"
        r"|regularidade\s+fiscal|document.*habilita[çc][aã]o|atestado\s+de\s+capacidade",
        texto, re.IGNORECASE
    ))

    # ── Grupo 6 — Sustentabilidade e riscos ──────────────────────────
    tr.tem_sustentabilidade = bool(re.search(
        r"sustentabilidade|crit[eé]rio.*sustent[áa]vel?|ambiental"
        r"|impacto.*ambiental|descarte\s+ecol[oó]gico|logística\s+reversa"
        r"|Guia\s+Nacional.*Sustent|Decreto.*23\.891|efici[eê]ncia\s+energ[eé]tica"
        r"|baixo\s+consumo\s+de\s+energia",
        texto, re.IGNORECASE
    ))

    tr.tem_mapa_riscos = bool(re.search(
        r"mapa\s+de\s+riscos|matriz\s+de\s+riscos|gerenciamento\s+de\s+riscos"
        r"|gest[aã]o\s+de\s+riscos|an[áa]lise\s+de\s+riscos.*contrata[çc][aã]o",
        texto, re.IGNORECASE
    ))

    # ── Grupo 8 — Critério de julgamento ─────────────────────────────
    tr.tem_criterio_julgamento = bool(re.search(
        r"menor\s+pre[çc]o|maior\s+desconto|melhor\s+t[eé]cnica|t[eé]cnica\s+e\s+pre[çc]o"
        r"|crit[eé]rio\s+de\s+julgamento|julgamento.*(?:menor|maior|t[eé]cnica)"
        r"|modalidade.*(?:preg[aã]o|concorr[eê]ncia|dispensa|inexigibilidade)",
        texto, re.IGNORECASE
    ))

    # ── Grupo 9 — Modelo de execução e recebimento ───────────────────
    tr.tem_modelo_execucao = bool(re.search(
        r"modelo\s+de\s+execu[çc][aã]o|cronograma\s+de\s+(?:execu[çc][aã]o|entrega)"
        r"|prazo\s+(?:para\s+)?execu[çc][aã]o|prazo\s+(?:para\s+)?entrega"
        r"|ordem\s+de\s+servi[çc]o|ordem\s+de\s+fornecimento|OS\s*emitida"
        r"|demandas?\s+ser[aã]o\s+formalizadas?|local\s+de\s+(?:execu[çc][aã]o|entrega)",
        texto, re.IGNORECASE
    ))

    tr.tem_recebimento_provisorio = bool(re.search(
        r"recebimento\s+provis[oó]rio",
        texto, re.IGNORECASE
    ))

    tr.tem_recebimento_definitivo = bool(re.search(
        r"recebimento\s+definitivo",
        texto, re.IGNORECASE
    ))

    # ── Grupo 10 — Gestão e fiscalização ─────────────────────────────
    tr.tem_modelo_gestao = bool(re.search(
        r"modelo\s+de\s+gest[aã]o|fiscaliza[çc][aã]o.*contrato"
        r"|gestor.*contrato|fiscal.*contrato"
        r"|acompanhamento.*execu[çc][aã]o|fiscal\s+(?:t[eé]cnico|administrativo)",
        texto, re.IGNORECASE
    ))

    tr.tem_condicoes_pagamento = bool(re.search(
        r"condi[çc][oõ]es\s+de\s+pagamento|prazo\s+(?:para\s+)?pagamento"
        r"|nota\s+fiscal|fatura.*pagamento|pagamento.*ser[aá]\s+efetuado"
        r"|d[íi]as.*pagamento|30\s+(?:\(trinta\)\s+)?dias.*pagamento"
        r"|pagamento.*30.*dias",
        texto, re.IGNORECASE
    ))

    tr.tem_sancoes = bool(re.search(
        r"san[çc][aã]o|san[çc][oõ]es|multa.*contratual|penalidade|infra[çc][aã]o.*contratual"
        r"|penaliza[çc][aã]o|multa.*morat[oó]ria|multa.*compensat[oó]ria"
        r"|art\.?\s*155.*14\.133",
        texto, re.IGNORECASE
    ))

    tr.tem_fiscal_gestor = bool(re.search(
        r"fiscal\s+do\s+contrato|gestor\s+do\s+contrato|designad[ao]\s+(?:como\s+)?fiscal"
        r"|responsável\s+pela\s+fiscaliza[çc][aã]o|fiscal\s+t[eé]cnico\s+do\s+contrato"
        r"|fiscal\s+administrativo\s+do\s+contrato",
        texto, re.IGNORECASE
    ))

    # ── Grupo 11 — Disposições finais ────────────────────────────────
    tr.tem_prazo_vigencia = bool(re.search(
        r"vig[eê]ncia\s+(?:do|de)\s+contrato|prazo\s+de\s+vig[eê]ncia"
        r"|dura[çc][aã]o\s+do\s+contrato|prazo\s+contratual"
        r"|vigência.*(?:meses?|anos?)|(?:\d+\s+\([\w]+\))\s+meses?\s+(?:a\s+partir|de\s+vigência)"
        r"|art\.?\s*106.*14\.133",
        texto, re.IGNORECASE
    ))

    tr.tem_pncp_referencia = bool(re.search(
        r"\bPNCP\b|Portal\s+Nacional\s+de\s+Contrata[çc][oõ]es\s+P[úu]blicas",
        texto, re.IGNORECASE
    ))

    return tr


# ─────────────────────────────────────────────────────────────────────
#  CHECKLIST DE CONFORMIDADE
# ─────────────────────────────────────────────────────────────────────

def _add(achados: list, **kwargs) -> None:
    kwargs["numero"] = len(achados) + 1
    achados.append(Achado(**kwargs))


def checar_existencia_e_elaboracao(tr: TR, achados: list) -> None:
    """Grupo 1 (Q1–Q7) — Existência e Elaboração do TR."""
    if not tr.tem_assinatura:
        _add(achados,
            titulo="TR sem Evidência de Assinatura pela Equipe de Planejamento (Q1/Q5)",
            tipo="Vício Formal",
            localizacao="Seção de assinaturas do TR",
            inconsistencia=(
                "O TR não apresenta evidência de que foi assinado pelos integrantes da "
                "Equipe de Planejamento da Contratação (Requisitante, Técnico e "
                "Administrativo). A assinatura é condição de validade formal do TR e "
                "pressuposto para o prosseguimento regular do processo."
            ),
            fundamentacao=(
                "Art. 7º, caput, e art. 18 da Lei nº 14.133/2021; Art. 18 e art. 19 do "
                "Decreto Estadual (PI) nº 21.872/2023; Art. 8º da IN SEGES/ME nº 81/2022."
            ),
            acao=(
                "Assinar o TR eletronicamente no SEI, com a assinatura de todos os "
                "integrantes designados para a Equipe de Planejamento da Contratação, "
                "antes do envio para análise da ASSCOMPRAS."
            ),
            sugestao=(
                "[Assinar o documento TR no SEI com os três integrantes: Integrante "
                "Requisitante (área demandante), Integrante Técnico (área técnica) e "
                "Integrante Administrativo (ASSCOMPRAS/CLC).]"
            ),
        )


def checar_conteudo_essencial(tr: TR, achados: list) -> None:
    """Grupo 2 (Q8–Q16) — Conteúdo Essencial e Justificativa."""

    if not tr.tem_referencia_etp:
        _add(achados,
            titulo="TR sem Referência Expressa ao Estudo Técnico Preliminar (Q8)",
            tipo="Vício Formal",
            localizacao="Preâmbulo ou seção de justificativa do TR",
            inconsistencia=(
                "O TR não faz referência expressa ao Estudo Técnico Preliminar (ETP) "
                "que fundamenta a escolha da solução contratada. O TR deve referenciar "
                "o ETP ou conter o extrato de suas partes não sigilosas, garantindo a "
                "rastreabilidade entre planejamento e especificação do objeto."
            ),
            fundamentacao=(
                "Art. 6º, XXIII, 'b', da Lei nº 14.133/2021; Art. 36, II, do Decreto "
                "Estadual (PI) nº 21.872/2023; Art. 9º, II, da IN SEGES/ME nº 81/2022."
            ),
            acao=(
                "Inserir no TR referência expressa ao ETP do processo, indicando o "
                "número do documento SEI correspondente, ou incluir no próprio TR o "
                "extrato das partes não sigilosas do ETP (Elementos I, II, III e XIII)."
            ),
            sugestao=(
                "[Ex: 'O presente Termo de Referência tem como fundamento o Estudo "
                "Técnico Preliminar (ETP), constante dos autos do processo SEI nº "
                "[número], elaborado pela Equipe de Planejamento da Contratação em "
                "[data], cujas conclusões principais são: [resumo do Elemento XIII].']"
            ),
        )

    if not tr.tem_referencia_pca:
        _add(achados,
            titulo="TR sem Indicação do Alinhamento com o Plano de Contratações Anual — PCA (Q10)",
            tipo="Vício Formal",
            localizacao="Dados gerais ou seção de justificativa do TR",
            inconsistencia=(
                "O TR não indica expressamente o alinhamento da contratação com o Plano "
                "de Contratações Anual (PCA) vigente. Essa demonstração é requisito legal "
                "que comprova o planejamento prévio da despesa e a compatibilidade com o "
                "instrumento de gestão orçamentária do órgão."
            ),
            fundamentacao=(
                "Art. 12, VII, e art. 18 da Lei nº 14.133/2021; Art. 17, I, do Decreto "
                "Estadual (PI) nº 21.872/2023; Art. 7º da IN SEGES/ME nº 81/2022."
            ),
            acao=(
                "Indicar no TR o item do PCA em que a contratação está prevista, com o "
                "código ou número do item e o exercício financeiro correspondente."
            ),
            sugestao=(
                "[Ex: 'A presente contratação encontra-se prevista no Plano de Contratações "
                "Anual (PCA) do MPPI para o exercício [XXXX], item [código/número], aprovado "
                "por [ato de aprovação], alinhado ao PEI 2022-2029.']"
            ),
        )

    if not tr.tem_justificativa_parcelamento:
        _add(achados,
            titulo="TR sem Justificativa Expressa para o Parcelamento ou Não do Objeto (Q13)",
            tipo="Vício Formal",
            localizacao="Seção de justificativa / parcelamento do TR",
            inconsistencia=(
                "O TR não apresenta posicionamento expresso sobre o parcelamento do "
                "objeto, declarando se o objeto será ou não parcelado e a respectiva "
                "justificativa. O silêncio não atende ao requisito de justificativa "
                "circunstanciada exigida pela Lei nº 14.133/2021."
            ),
            fundamentacao=(
                "Art. 18, § 1º, VIII, e art. 40, § 2º, da Lei nº 14.133/2021; Art. 23, "
                "VII, e art. 36, IV, do Decreto Estadual (PI) nº 21.872/2023."
            ),
            acao=(
                "Inserir no TR item específico sobre parcelamento: (a) se não parcelado, "
                "justificar a indivisibilidade ou inviabilidade econômica; (b) se "
                "parcelado em lotes, descrever os critérios de divisão e a justificativa."
            ),
            sugestao=(
                "[Ex NÃO PARCELAMENTO: 'O objeto não será parcelado em razão de "
                "[interdependência técnica / responsabilidade única / inviabilidade "
                "econômica]. Será contratado em lote único.' | Ex PARCELAMENTO: "
                "'O objeto será dividido em [N] lotes, conforme Anexo I, visando "
                "ampliar a competitividade do certame.']"
            ),
        )


def checar_especificacao_objeto(tr: TR, achados: list) -> None:
    """Grupo 3 (Q17–Q23) — Padronização, Especificação e Artigos de Luxo."""
    if tr.tem_indicacao_marca and not tr.tem_justif_marca:
        _add(achados,
            titulo="Indicação de Marca ou Modelo no TR sem Justificativa Técnica (Q19)",
            tipo="Vício Material",
            localizacao="Descrição do objeto / especificações técnicas do TR",
            inconsistencia=(
                "O TR indica marca ou modelo específico sem apresentar justificativa "
                "técnica baseada em padronização, compatibilidade com o acervo existente "
                "ou exclusividade comprovada. A indicação de marca sem justificativa "
                "restringe indevidamente a competitividade e configura direcionamento "
                "vedado pela Lei nº 14.133/2021."
            ),
            fundamentacao=(
                "Art. 41, I, da Lei nº 14.133/2021; Art. 71, X, 'a', do Decreto Estadual "
                "(PI) nº 21.872/2023."
            ),
            acao=(
                "Reformular a especificação evitando indicação de marca específica, "
                "substituindo-a por características técnicas objetivas equivalentes. "
                "Se necessária a padronização, inserir justificativa técnica formal "
                "com base em: (a) padronização do acervo existente; (b) compatibilidade "
                "com equipamentos já instalados; (c) exclusividade técnica comprovada."
            ),
            sugestao=(
                "[Substituir a marca por especificação técnica: 'capacidade mínima de "
                "[X], compatível com [padrão Y], admitidos equivalentes comprovadamente "
                "compatíveis.' | Se necessária: 'Marca [X] ou equivalente, conforme "
                "justificativa técnica de padronização constante do Processo nº [XXX].']"
            ),
        )


def checar_quantitativos_e_valor(tr: TR, achados: list) -> None:
    """Grupo 4 (Q24–Q27) — Quantitativos, Estimativa de Valor e Fonte de Recursos."""

    if not tr.tem_memoria_calculo:
        _add(achados,
            titulo="TR sem Memória de Cálculo para os Quantitativos Estimados (Q24)",
            tipo="Vício Formal",
            localizacao="Seção de quantitativos / estimativa de quantidades do TR",
            inconsistencia=(
                "O TR apresenta quantitativos estimados sem acompanhar a respectiva "
                "memória de cálculo. A norma exige que as quantidades sejam documentadas "
                "com base em histórico de consumo, levantamento por unidade beneficiária "
                "ou método equivalente — sem o qual não é possível verificar a "
                "racionalidade, proporcionalidade ou adequação dos quantitativos."
            ),
            fundamentacao=(
                "Art. 18, § 1º, IV, e art. 40, III, da Lei nº 14.133/2021; Art. 20, II, "
                "e art. 36, I, do Decreto Estadual (PI) nº 21.872/2023."
            ),
            acao=(
                "Acrescentar ao TR a memória de cálculo dos quantitativos, com base em: "
                "(a) histórico de consumo dos últimos 12–24 meses; (b) número de "
                "usuários/unidades beneficiárias; (c) projeção por capacidade instalada; "
                "(d) parâmetros de contratos similares."
            ),
            sugestao=(
                "[Incluir tabela: 'A estimativa de [X unidades] foi apurada com base: "
                "(i) consumo médio de [Y unidades/mês] nos últimos [N] meses; "
                "(ii) projeção de [Z]% para o período contratado; "
                "(iii) unidades beneficiárias: [N]. Memória de cálculo no Anexo [X].']"
            ),
        )

    if not tr.tem_preco_referencial:
        _add(achados,
            titulo="TR sem Fonte ou Preço Referencial para a Estimativa de Valor (Q25)",
            tipo="Vício Formal",
            localizacao="Seção de estimativa de valor / pesquisa de preços do TR",
            inconsistencia=(
                "O TR não indica as fontes dos preços referenciais utilizados na "
                "estimativa de valor. A estimativa deve ser acompanhada de preços "
                "unitários referenciais e dos documentos de suporte (painel de preços, "
                "pesquisa de mercado, ARP, contratação anterior), para permitir a "
                "verificação da vantajosidade e razoabilidade do valor estimado."
            ),
            fundamentacao=(
                "Art. 6º, XXIII, 'i', e art. 23 da Lei nº 14.133/2021; Art. 44 e "
                "art. 46 do Decreto Estadual (PI) nº 21.872/2023; IN SEGES/ME nº 65/2021."
            ),
            acao=(
                "Indicar expressamente as fontes utilizadas para a estimativa e referenciar "
                "ou anexar os documentos de pesquisa: painel de preços do governo federal, "
                "pesquisa de mercado com fornecedores, atas de registro de preços vigentes, "
                "contratos similares de outros órgãos."
            ),
            sugestao=(
                "[Ex: 'O valor estimado de R$ [X.XXX,XX] foi obtido mediante pesquisa "
                "de preços realizada em [data], com base: (1) Painel de Preços "
                "(painel.compras.gov.br); (2) Ata de Registro de Preços nº XX/XXXX; "
                "(3) Proposta de [Fornecedor X]. Memória de cálculo no Anexo [Y].']"
            ),
        )

    if not tr.tem_fonte_recursos:
        _add(achados,
            titulo="TR sem Identificação da Fonte de Recursos Orçamentários (Q27)",
            tipo="Vício Formal",
            localizacao="Dados gerais ou seção de dotação orçamentária do TR",
            inconsistencia=(
                "O TR não identifica a fonte de recursos orçamentários — elemento de "
                "despesa, unidade gestora (PGJ, FMMPI ou FPROCON) ou dotação orçamentária. "
                "Essa identificação é requisito legal para a regular instrução processual "
                "e condição para a reserva de dotação e emissão de empenho."
            ),
            fundamentacao=(
                "Art. 6º, XXIII, 'j', e art. 150 da Lei nº 14.133/2021; Art. 52, § 1º, "
                "do Decreto Estadual (PI) nº 21.872/2023; Art. 13 do Decreto Estadual "
                "(PI) nº 21.938/2023 (reserva de dotação)."
            ),
            acao=(
                "Inserir no TR a identificação da fonte de recursos: Unidade Gestora "
                "responsável (PGJ/UG 250101, FMMPI/UG 250102 ou FPROCON/UG 250103), "
                "elemento de despesa e dotação orçamentária no exercício vigente."
            ),
            sugestao=(
                "[Ex: 'Os recursos necessários à cobertura da despesa onerarão a dotação "
                "orçamentária da [PGJ / FMMPI / FPROCON], Elemento de Despesa [código], "
                "Fonte [código], no exercício de [Ano].']"
            ),
        )


def checar_habilitacao(tr: TR, achados: list) -> None:
    """Grupo 5 (Q28–Q34) — Requisitos de Habilitação."""
    if not tr.tem_habilitacao:
        _add(achados,
            titulo="TR sem Definição dos Requisitos de Habilitação dos Licitantes (Q28)",
            tipo="Vício Formal",
            localizacao="Seção de habilitação / requisitos dos fornecedores do TR",
            inconsistencia=(
                "O TR não define os documentos de habilitação exigidos dos licitantes — "
                "habilitação jurídica, regularidade fiscal, social e trabalhista, "
                "qualificação técnica e qualificação econômico-financeira. A ausência "
                "dessa definição impede a elaboração do instrumento convocatório "
                "e a avaliação adequada dos proponentes."
            ),
            fundamentacao=(
                "Art. 62, art. 66 e art. 68 da Lei nº 14.133/2021; Art. 36, XVI, do "
                "Decreto Estadual (PI) nº 21.872/2023."
            ),
            acao=(
                "Inserir no TR a relação completa de documentos de habilitação exigidos: "
                "(a) habilitação jurídica; (b) regularidade fiscal, social e trabalhista; "
                "(c) qualificação técnica — atestados de capacidade técnica referentes às "
                "parcelas de maior relevância (≥ 4% do valor estimado); "
                "(d) qualificação econômico-financeira."
            ),
            sugestao=(
                "[Estruturar: '6.1 Habilitação Jurídica; 6.2 Regularidade Fiscal, Social "
                "e Trabalhista; 6.3 Qualificação Técnica (atestados de capacidade técnica, "
                "observados os limites do art. 67, § 1º e § 2º, da Lei nº 14.133/2021); "
                "6.4 Qualificação Econômico-Financeira.']"
            ),
        )


def checar_sustentabilidade_riscos(tr: TR, achados: list) -> None:
    """Grupo 6 (Q35–Q38) — Sustentabilidade Ambiental e Gerenciamento de Riscos."""

    if not tr.tem_sustentabilidade:
        _add(achados,
            titulo="TR sem Critérios de Sustentabilidade Socioambiental ou Justificativa de Dispensa (Q35)",
            tipo="Vício Formal",
            localizacao="Seção de requisitos / sustentabilidade do TR",
            inconsistencia=(
                "O TR não detalha os critérios de sustentabilidade socioambiental e "
                "descarte ecológico aplicáveis ao objeto, tampouco apresenta justificativa "
                "técnica de sua inaplicabilidade. A sustentabilidade é princípio obrigatório "
                "das contratações públicas e o Decreto Estadual (PI) nº 23.891/2025 "
                "estabelece critérios específicos para o Estado do Piauí."
            ),
            fundamentacao=(
                "Art. 11, IV, e art. 18, § 1º, XII, da Lei nº 14.133/2021; Art. 1º e "
                "art. 4º do Decreto Estadual (PI) nº 23.891/2025; Guia Nacional de "
                "Contratações Sustentáveis (CGU/AGU)."
            ),
            acao=(
                "Inserir no TR seção de sustentabilidade com: (i) critérios socioambientais "
                "aplicáveis ao objeto; (ii) requisitos de descarte ecológico ou logística "
                "reversa; (iii) se inaplicáveis, justificativa técnica expressa com "
                "referência ao Guia Nacional de Contratações Sustentáveis."
            ),
            sugestao=(
                "[Aplicável: 'Os critérios de sustentabilidade aplicáveis são: (i) [critério]; "
                "(ii) [critério], conforme Decreto (PI) nº 23.891/2025.' | Inaplicável: "
                "'Considerando a natureza do objeto, não foram identificados critérios "
                "de aplicação obrigatória, conforme consulta ao Guia Nacional de "
                "Contratações Sustentáveis (CGU/AGU).']"
            ),
        )

    if not tr.tem_mapa_riscos:
        _add(achados,
            titulo="Ausência de Referência ao Mapa de Riscos nos Autos (Q38)",
            tipo="Sugestão de Melhoria",
            localizacao="TR completo / seção de gestão e fiscalização",
            inconsistencia=(
                "O TR não faz referência ao Mapa de Riscos da contratação. O Mapa de Riscos "
                "deve ser elaborado na fase preparatória e juntado aos autos até o término "
                "da elaboração do TR. Sua ausência ou falta de referência no TR compromete "
                "a completude da instrução processual e a rastreabilidade do planejamento "
                "de riscos."
            ),
            fundamentacao=(
                "Art. 18, X, da Lei nº 14.133/2021; Art. 31 do Decreto Estadual (PI) "
                "nº 21.872/2023 (Mapa de Riscos como parte integrante do planejamento)."
            ),
            acao=(
                "Verificar se o Mapa de Riscos foi elaborado e juntado aos autos. Caso "
                "não, providenciar sua elaboração. Se já consta nos autos, inserir no TR "
                "referência expressa ao documento e ao número SEI correspondente."
            ),
            sugestao=(
                "[Ex: 'O Mapa de Riscos da presente contratação, elaborado pela Equipe "
                "de Planejamento nos termos do art. 31 do Decreto Estadual nº 21.872/2023, "
                "encontra-se juntado aos autos do processo SEI nº [número], doc. nº [ID].']"
            ),
        )


def checar_julgamento(tr: TR, achados: list) -> None:
    """Grupo 8 (Q46–Q53) — Regras de Julgamento e Participação."""
    if not tr.tem_criterio_julgamento:
        _add(achados,
            titulo="TR sem Definição Motivada do Critério de Julgamento das Propostas (Q46)",
            tipo="Vício Formal",
            localizacao="Seção de critério de julgamento / modalidade licitatória do TR",
            inconsistencia=(
                "O TR não define expressamente a modalidade de licitação, o critério de "
                "julgamento e o modo de disputa a serem adotados. Esses elementos são "
                "requisitos obrigatórios do TR e condicionam toda a estrutura da disputa "
                "concorrencial, devendo ser motivados tecnicamente."
            ),
            fundamentacao=(
                "Art. 6º, XXIII, 'h', e art. 28 da Lei nº 14.133/2021; Art. 36, XIII, "
                "do Decreto Estadual (PI) nº 21.872/2023."
            ),
            acao=(
                "Inserir no TR a definição justificada de: (a) modalidade licitatória "
                "(pregão, concorrência, dispensa, inexigibilidade); (b) critério de "
                "julgamento (menor preço, maior desconto, melhor técnica, técnica e preço); "
                "(c) modo de disputa (aberto, fechado, combinado)."
            ),
            sugestao=(
                "[Ex: 'O critério de julgamento será o MENOR PREÇO, apurado pelo valor "
                "global/unitário, em razão de [objeto é bem/serviço comum passível de "
                "comparação objetiva pelo preço], por meio de disputa no modo ABERTO.']"
            ),
        )


def checar_modelo_execucao(tr: TR, achados: list) -> None:
    """Grupo 9 (Q54–Q58) — Modelo de Execução e Recebimento do Objeto."""

    if not tr.tem_modelo_execucao:
        _add(achados,
            titulo="TR sem Definição do Modelo de Execução da Contratação (Q54)",
            tipo="Vício Formal",
            localizacao="Seção de modelo de execução / rotina de execução do TR",
            inconsistencia=(
                "O TR não detalha o modelo de execução do objeto — cronograma de "
                "entrega/execução, horários de atendimento, responsabilidades de cada "
                "parte e forma de comunicação de demandas (Ordem de Serviço ou Ordem de "
                "Fornecimento). A ausência dessas regras dificulta a fiscalização e o "
                "controle da execução contratual."
            ),
            fundamentacao=(
                "Art. 6º, XXIII, 'e', da Lei nº 14.133/2021; Art. 36, VII, do Decreto "
                "Estadual (PI) nº 21.872/2023; Art. 9º, V, da IN SEGES/ME nº 81/2022."
            ),
            acao=(
                "Inserir seção de modelo de execução contemplando: (a) cronograma ou "
                "prazos de execução/entrega; (b) local e horário; (c) forma de comunicação "
                "de demandas (OS/OF); (d) responsabilidades das partes durante a execução."
            ),
            sugestao=(
                "[Ex: 'As demandas serão formalizadas por Ordem de Serviço/Fornecimento "
                "(OS/OF), emitida pelo fiscal técnico. O prazo para início após emissão "
                "da OS/OF é de [X] dias úteis. A execução deverá observar [local, horário, "
                "condições específicas].']"
            ),
        )

    if not (tr.tem_recebimento_provisorio and tr.tem_recebimento_definitivo):
        ausentes = []
        if not tr.tem_recebimento_provisorio:
            ausentes.append("recebimento provisório")
        if not tr.tem_recebimento_definitivo:
            ausentes.append("recebimento definitivo")
        _add(achados,
            titulo=(
                "TR sem Definição das Condições de "
                + " e ".join(a.title() for a in ausentes)
                + " do Objeto (Q58)"
            ),
            tipo="Vício Formal",
            localizacao="Seção de recebimento do objeto no TR",
            inconsistencia=(
                f"O TR não define as condições de {' e '.join(ausentes)} do objeto "
                "contratado. A lei exige a especificação da forma, local e prazos para "
                "o recebimento provisório e definitivo, como mecanismo de controle da "
                "qualidade da entrega e de apuração de responsabilidades da contratada."
            ),
            fundamentacao=(
                "Art. 6º, XXIII, 'e' e 'g', e art. 140 da Lei nº 14.133/2021; Art. 36, "
                "VII, do Decreto Estadual (PI) nº 21.872/2023; Art. 9º, I, 'c', da "
                "IN SEGES/ME nº 81/2022."
            ),
            acao=(
                "Definir no TR as condições para ambas as modalidades: (a) recebimento "
                "provisório: responsável, prazo e critérios de aceite preliminar; "
                "(b) recebimento definitivo: responsável, prazo, critérios objetivos "
                "de aprovação e consequências em caso de rejeição."
            ),
            sugestao=(
                "[Ex: 'Recebimento Provisório: pelo fiscal técnico, em até [X] dias "
                "úteis da entrega, para verificação de conformidade. Recebimento "
                "Definitivo: em até [Y] dias após o provisório, após verificação de "
                "todos os requisitos técnicos. Em caso de rejeição, a contratada terá "
                "[Z] dias para correção ou substituição.']"
            ),
        )


def checar_gestao_contrato(tr: TR, achados: list) -> None:
    """Grupo 10 (Q59–Q67) — Modelo de Gestão, Fiscalização e Sanções."""

    if not tr.tem_modelo_gestao:
        _add(achados,
            titulo="TR sem Definição do Modelo de Gestão e Fiscalização do Contrato (Q59)",
            tipo="Vício Formal",
            localizacao="Seção de gestão e fiscalização do TR",
            inconsistencia=(
                "O TR não detalha o modelo de gestão do contrato — regras de fiscalização, "
                "critérios de medição, estrutura de controle e atribuições dos fiscais. "
                "Sem essas regras, os fiscais carecem de parâmetros objetivos para avaliar "
                "o desempenho da contratada e acionar as cláusulas sancionatórias."
            ),
            fundamentacao=(
                "Art. 6º, XXIII, 'f', e art. 117 da Lei nº 14.133/2021; Art. 36, XXIV, "
                "do Decreto Estadual (PI) nº 21.872/2023; Art. 9º, VI, da IN SEGES/ME "
                "nº 81/2022."
            ),
            acao=(
                "Inserir seção de modelo de gestão com: (a) atribuições do gestor e dos "
                "fiscais técnico e administrativo; (b) frequência e forma de fiscalização; "
                "(c) instrumentos de medição (IMR/check-list); (d) procedimento de "
                "comunicação de falhas e prazo de correção."
            ),
            sugestao=(
                "[Ex: 'A gestão do contrato será exercida por Gestor e Fiscais formalmente "
                "designados. A fiscalização técnica verificará [critérios]. A medição "
                "utilizará o IMR constante do Anexo [X]. Constatada irregularidade, a "
                "contratada será notificada para correção em [X] dias úteis.']"
            ),
        )

    if not tr.tem_condicoes_pagamento:
        _add(achados,
            titulo="TR sem Definição das Condições de Pagamento (Q62)",
            tipo="Vício Formal",
            localizacao="Seção de pagamento / condições contratuais do TR",
            inconsistencia=(
                "O TR não define as condições de pagamento: prazo após emissão de nota "
                "fiscal/fatura, exigência de nota fiscal eletrônica, regras de reajuste "
                "ou repactuação. A ausência cria insegurança jurídica e pode resultar em "
                "mora no pagamento ou disputas sobre a forma de atualização dos valores."
            ),
            fundamentacao=(
                "Art. 92, V e VI, da Lei nº 14.133/2021; Art. 36, XXV, do Decreto Estadual "
                "(PI) nº 21.872/2023; Art. 9º, VII, da IN SEGES/ME nº 81/2022."
            ),
            acao=(
                "Inserir cláusula de pagamento definindo: (a) prazo para pagamento após "
                "ateste da nota fiscal (máximo 30 dias corridos); (b) exigência de Nota "
                "Fiscal Eletrônica; (c) regras de reajuste/repactuação; (d) glosas "
                "aplicáveis em caso de irregularidade na medição."
            ),
            sugestao=(
                "[Ex: 'O pagamento será efetuado em até 30 (trinta) dias corridos após "
                "o recebimento definitivo e ateste da Nota Fiscal Eletrônica pelo fiscal "
                "administrativo. O valor será reajustado anualmente pelo IPCA, a partir "
                "do 12º mês de vigência, data-base [mês de assinatura].']"
            ),
        )

    if not tr.tem_sancoes:
        _add(achados,
            titulo="TR sem Definição do Rol de Sanções Administrativas e Dosimetria de Multas (Q63)",
            tipo="Vício Material",
            localizacao="Seção de sanções / obrigações contratuais do TR",
            inconsistencia=(
                "O TR não estipula o rol de sanções administrativas com gradação e "
                "dosimetria das multas contratuais. A ausência fragiliza o poder "
                "sancionatório da Administração durante a execução e pode comprometer "
                "a responsabilização da contratada por inadimplementos."
            ),
            fundamentacao=(
                "Art. 92, XIV, e art. 155 da Lei nº 14.133/2021; Art. 14, IV, e art. 36, "
                "XXVI, do Decreto Estadual (PI) nº 21.872/2023; Portaria SEGES/MGI "
                "nº 587/2023 (dosimetria das multas)."
            ),
            acao=(
                "Inserir cláusula de sanções detalhando: (a) condutas puníveis; "
                "(b) tipos de sanção (advertência, multa, suspensão, impedimento, "
                "declaração de inidoneidade); (c) percentuais das multas moratória e "
                "compensatória; (d) procedimento de defesa prévia."
            ),
            sugestao=(
                "[Ex: 'Sanções aplicáveis: (i) advertência; (ii) multa moratória de "
                "[0,5]% ao dia, limitada a [10]% do valor total; (iii) multa "
                "compensatória de [10]% pelo inadimplemento total; (iv) suspensão pelo "
                "prazo de até [3 anos]; (v) declaração de inidoneidade. A aplicação de "
                "sanção é precedida de processo administrativo com ampla defesa.']"
            ),
        )

    if not tr.tem_fiscal_gestor:
        _add(achados,
            titulo="TR sem Previsão Expressa da Designação de Gestor e Fiscais do Contrato (Q65)",
            tipo="Vício Formal",
            localizacao="Seção de gestão e fiscalização do TR",
            inconsistencia=(
                "O TR não prevê expressamente a designação formal de gestor e fiscais "
                "do contrato por ato da autoridade competente, nem menciona seus substitutos "
                "imediatos. Sem previsão no TR, o processo pode avançar sem que os "
                "responsáveis pela fiscalização estejam formalmente designados antes do "
                "início da execução contratual."
            ),
            fundamentacao=(
                "Art. 7º, caput, da Lei nº 14.133/2021; Art. 67 do Decreto Estadual (PI) "
                "nº 21.872/2023."
            ),
            acao=(
                "Inserir no TR exigência de que, até a data de início da execução, a "
                "autoridade máxima emita ato formal designando: (a) gestor do contrato; "
                "(b) fiscal técnico; (c) fiscal administrativo; (d) substitutos imediatos "
                "de cada um."
            ),
            sugestao=(
                "[Ex: 'A gestão e fiscalização do contrato serão exercidas por agentes "
                "formalmente designados por ato do [Procurador-Geral de Justiça / "
                "Ordenador de Despesas], publicado antes do início da execução, nos "
                "termos do art. 7º da Lei nº 14.133/2021 e art. 67 do Decreto "
                "Estadual (PI) nº 21.872/2023.']"
            ),
        )


def checar_disposicoes_finais(tr: TR, achados: list) -> None:
    """Grupo 11 (Q68–Q72) — Disposições Finais, Publicidade e Prazo."""

    if not tr.tem_prazo_vigencia:
        _add(achados,
            titulo="TR sem Definição do Prazo de Vigência do Contrato (Q70)",
            tipo="Vício Formal",
            localizacao="Seção de prazo contratual / disposições gerais do TR",
            inconsistencia=(
                "O TR não define o prazo de vigência do contrato, nem as condições para "
                "eventual prorrogação. O prazo contratual é elemento essencial do TR: "
                "condiciona o dimensionamento do valor estimado, a previsão orçamentária "
                "e os critérios de reajuste aplicáveis."
            ),
            fundamentacao=(
                "Art. 106 da Lei nº 14.133/2021; Art. 36, XVII, do Decreto Estadual (PI) "
                "nº 21.872/2023."
            ),
            acao=(
                "Inserir no TR o prazo de vigência contratual, especificando: (a) prazo "
                "inicial; (b) se serviço contínuo, possibilidade e critérios de prorrogação "
                "até o limite legal de 60 meses; (c) marco inicial de contagem (assinatura, "
                "publicação ou data de início da execução)."
            ),
            sugestao=(
                "[Ex: 'O contrato terá vigência de 12 (doze) meses, contados da data de "
                "sua assinatura, podendo ser prorrogado por períodos sucessivos, até o "
                "limite de 60 (sessenta) meses, desde que demonstrada a vantajosidade e a "
                "manutenção das condições iniciais, nos termos do art. 106, I, da Lei "
                "nº 14.133/2021.']"
            ),
        )

    if not tr.tem_pncp_referencia:
        _add(achados,
            titulo="TR sem Referência à Publicação no PNCP como Anexo do Instrumento Convocatório (Q69)",
            tipo="Sugestão de Melhoria",
            localizacao="Seção de publicidade ou disposições gerais do TR",
            inconsistencia=(
                "O TR não faz referência à obrigatoriedade de sua publicação no Portal "
                "Nacional de Contratações Públicas (PNCP) como anexo do edital ou aviso de "
                "contratação direta. A publicação garante a transparência ativa e o acesso "
                "de potenciais fornecedores às especificações completas do objeto."
            ),
            fundamentacao=(
                "Art. 174, § 2º, III, da Lei nº 14.133/2021; Art. 93 do Decreto Estadual "
                "(PI) nº 21.872/2023; Art. 12 da IN SEGES/ME nº 81/2022."
            ),
            acao=(
                "Inserir ao final do TR referência expressa à sua publicação no PNCP como "
                "anexo do instrumento convocatório (edital ou aviso de contratação direta)."
            ),
            sugestao=(
                "[Ex: 'O presente Termo de Referência será publicado no Portal Nacional de "
                "Contratações Públicas (PNCP), como anexo do [Edital / Aviso de Contratação "
                "Direta], nos termos do art. 174, § 2º, III, da Lei nº 14.133/2021.']"
            ),
        )


def checar_quesitos_json(tr: TR, achados: list) -> None:
    """Verifica quesitos declarativos definidos em quesitos_TR.json."""
    import json
    caminho_json = BASE_DIR / "quesitos_TR.json"
    if not caminho_json.exists():
        return
    try:
        with open(caminho_json, encoding="utf-8") as f:
            dados = json.load(f)
    except Exception:
        return
    texto = tr.texto_completo
    is_tic = tr.is_tic
    for q in dados.get("quesitos", []):
        if q.get("is_tic_only") and not is_tic:
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

def salvar_achados_json(tr: TR, achados: list, caminho_origem: str) -> str:
    """Salva os achados em JSON para consolidação posterior no Ofício final."""
    import json
    base = Path(caminho_origem).stem
    pasta = Path(caminho_origem).parent
    caminho_json = str(pasta / f"achados_TR_{base}.json")

    dados = {
        "artefato": "TR",
        "num_processo": tr.num_processo or "",
        "objeto": tr.objeto_descricao or "",
        "unidade": tr.unidade_requisitante or "",
        "is_tic": tr.is_tic,
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


def gerar_oficio_word(tr: TR, achados: list, caminho_saida: str):
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

    unidade  = tr.unidade_requisitante or "[Unidade Requisitante]"
    processo = tr.num_processo         or "[nº do processo SEI]"
    tipo_tag = " — Solução de TIC" if tr.is_tic else ""

    # ── Destinatário ─────────────────────────────────────────────────
    p = doc.add_paragraph()
    p.add_run(f"À {unidade}").bold = True
    p = doc.add_paragraph()
    p.add_run(
        f"Assunto: Devolução de Autos para Saneamento — "
        f"Análise do Termo de Referência{tipo_tag} — "
        f"Processo SEI nº {processo}."
    ).bold = True

    doc.add_paragraph()
    doc.add_paragraph().add_run("Senhor(a) Coordenador(a),")
    doc.add_paragraph()

    # ── Abertura ─────────────────────────────────────────────────────
    abertura = [
        (
            "Cumprimentando-o cordialmente, registro que a equipe desta Assessoria "
            "analisou o Termo de Referência (TR) juntado aos autos do processo em "
            "referência, verificando a conformidade do documento com os normativos "
            "aplicáveis: Lei nº 14.133/2021, Decreto Estadual (PI) nº 21.872/2023, "
            "IN SEGES/ME nº 81/2022, Atos PGJ/MPPI nº 1.381 e 1.382/2024"
            + (", Resolução CNMP nº 283/2024 e MOTec" if tr.is_tic else "") + "."
        ),
        (
            "Na qualidade de Agente de Contratação responsável pela análise de "
            "conformidade da fase preparatória, e em cumprimento ao disposto no "
            "art. 53 da Lei nº 14.133/2021, restituo o presente feito para "
            "saneamento das inconsistências identificadas no TR. Os apontamentos "
            "possuem caráter eminentemente colaborativo, visando conferir segurança "
            "jurídica, transparência e eficiência ao procedimento."
        ),
        (
            "A seguir, apresentam-se os achados estruturados, com a respectiva "
            "fundamentação legal, ação de saneamento e sugestão de texto, quando "
            "aplicável. As redações sugeridas têm caráter meramente exemplificativo "
            "e orientativo, competindo à equipe de planejamento da contratação "
            "avaliar sua pertinência frente à realidade técnica e fática do objeto:"
        ),
    ]
    for txt in abertura:
        p = doc.add_paragraph()
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.first_line_indent = Cm(1.25)
        p.add_run(txt)

    doc.add_paragraph()

    # ── Cabeçalho do artefato ────────────────────────────────────────
    p = doc.add_paragraph()
    p.add_run("1. ARTEFATO: TERMO DE REFERÊNCIA (TR)").bold = True
    doc.add_paragraph()

    if not achados:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(1)
        p.add_run(
            "Nenhuma inconsistência identificada. TR em conformidade com os normativos aplicáveis."
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

    # ── Encerramento ─────────────────────────────────────────────────
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.first_line_indent = Cm(1.25)
    p.add_run(
        "Salientamos que o cumprimento das recomendações acima, além de conferir "
        "maior segurança jurídica ao procedimento licitatório, contribuirá para a "
        "qualidade do edital subsequente e para a boa execução contratual, "
        "prevenindo impugnações, questionamentos dos órgãos de controle e "
        "eventuais nulidades processuais."
    )

    doc.add_paragraph()
    p = doc.add_paragraph()
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.first_line_indent = Cm(1.25)
    p.add_run(
        "Fica a disposição para esclarecimentos adicionais e coloca-se à "
        "disposição para reunião de alinhamento, caso necessário."
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

def imprimir_relatorio(tr: TR, achados: list):
    sep = "─" * 68
    print(f"\n{'═' * 68}")
    print(f"  ANÁLISE DE CONFORMIDADE — TR  (v{VERSION})")
    print(f"{'═' * 68}")
    print(f"  Processo: {tr.num_processo or '(não identificado)'}")
    print(f"  Unidade : {tr.unidade_requisitante or '(não identificada)'}")
    print(f"  Objeto  : {(tr.objeto_descricao or '(não identificado)')[:70]}...")
    flags_cls = []
    if tr.is_tic:      flags_cls.append("TIC")
    if tr.is_servico:  flags_cls.append("Serviço")
    if tr.is_bem:      flags_cls.append("Bem/Aquisição")
    if tr.is_continuo: flags_cls.append("Execução Continuada")
    print(f"  Tipo    : {', '.join(flags_cls) or '(não classificado)'}")
    print(f"  Data    : {DATA_ANALISE}")
    print(sep)

    checks = [
        ("Assinado",                    tr.tem_assinatura),
        ("Referencia ETP",              tr.tem_referencia_etp),
        ("Referencia PCA",              tr.tem_referencia_pca),
        ("Justif. Parcelamento",        tr.tem_justificativa_parcelamento),
        ("Memória de Cálculo",          tr.tem_memoria_calculo),
        ("Preço Referencial",           tr.tem_preco_referencial),
        ("Fonte de Recursos",           tr.tem_fonte_recursos),
        ("Habilitação definida",        tr.tem_habilitacao),
        ("Sustentabilidade",            tr.tem_sustentabilidade),
        ("Mapa de Riscos",              tr.tem_mapa_riscos),
        ("Critério Julgamento",         tr.tem_criterio_julgamento),
        ("Modelo de Execução",          tr.tem_modelo_execucao),
        ("Recebimento Provisório",      tr.tem_recebimento_provisorio),
        ("Recebimento Definitivo",      tr.tem_recebimento_definitivo),
        ("Modelo de Gestão",            tr.tem_modelo_gestao),
        ("Condições de Pagamento",      tr.tem_condicoes_pagamento),
        ("Sanções",                     tr.tem_sancoes),
        ("Fiscal/Gestor previsto",      tr.tem_fiscal_gestor),
        ("Prazo de Vigência",           tr.tem_prazo_vigencia),
        ("Referência PNCP",             tr.tem_pncp_referencia),
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

    tr = parse_tr(texto)
    achados: list = []

    # Executa verificações em ordem (11 grupos de quesitos)
    checar_existencia_e_elaboracao(tr, achados)
    checar_conteudo_essencial(tr, achados)
    checar_especificacao_objeto(tr, achados)
    checar_quantitativos_e_valor(tr, achados)
    checar_habilitacao(tr, achados)
    checar_sustentabilidade_riscos(tr, achados)
    checar_julgamento(tr, achados)
    checar_modelo_execucao(tr, achados)
    checar_gestao_contrato(tr, achados)
    checar_disposicoes_finais(tr, achados)
    checar_quesitos_json(tr, achados)

    print(f"      {len(achados)} achado(s) identificado(s)")
    imprimir_relatorio(tr, achados)

    # Salvar achados em JSON para consolidação posterior no Ofício final
    salvar_achados_json(tr, achados, caminho)

    # Gerar Ofício Word apenas se solicitado explicitamente (flag --oficio)
    if "--oficio" in sys.argv:
        base = Path(caminho).stem
        saida = str(Path(caminho).parent / f"Oficio_ASSCOMPRAS_TR_{base}.docx")
        gerar_oficio_word(tr, achados, saida)
    else:
        print("ℹ  Para gerar o Ofício Word desta análise isolada, use: --oficio")
        print("ℹ  Para consolidar todos os artefatos do processo, use: gerar_oficio_processo.py\n")


if __name__ == "__main__":
    main()
