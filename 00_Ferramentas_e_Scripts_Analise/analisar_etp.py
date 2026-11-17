#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════╗
║  Analisador de ETP — ASSCOMPRAS / MPPI                  v1.0        ║
║  Coordenadoria de Licitações e Contratos                             ║
╚══════════════════════════════════════════════════════════════════════╝

Analisa o Estudo Técnico Preliminar (ETP) exportado do SEI (PDF ou HTML)
e gera automaticamente:

  1. Ofício ASSCOMPRAS com achados de conformidade (.docx)
  2. Relatório resumido no terminal

Requisitos (instale uma única vez):
    pip install pdfplumber beautifulsoup4 lxml python-docx

Uso:
    python analisar_etp.py "caminho\\para\\etp.pdf"
    python analisar_etp.py "caminho\\para\\etp.html"

⚠ IMPORTANTE: Revise e complemente o Ofício gerado. A análise
  automática identifica achados comuns mas não substitui a avaliação
  jurídica e técnica do Agente de Contratação.
"""

import sys
import os
import re
import textwrap
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
class ETP:
    texto_completo: str = ""
    num_processo: str = ""
    objeto_descricao: str = ""
    unidade_requisitante: str = ""

    # Flag TIC
    is_tic: bool = False

    # Elemento I — Necessidade (OBRIGATÓRIO)
    elem_I_texto: str = ""
    elem_I_foco_solucao: bool = False   # descreve solução em vez de problema

    # Elemento II — Requisitos
    elem_II_texto: str = ""

    # Elemento III — Levantamento de Mercado
    elem_III_texto: str = ""
    elem_III_tem_alternativas: bool = False
    elem_III_tic_alíneas: bool = False  # verificou alíneas a-g (CNMP 283)

    # Elemento IV — Solução como um todo
    elem_IV_texto: str = ""

    # Elemento V — Estimativa de Quantidades (OBRIGATÓRIO)
    elem_V_texto: str = ""
    elem_V_tem_memoria: bool = False

    # Elemento VI — Estimativa de Valor (OBRIGATÓRIO)
    elem_VI_texto: str = ""
    elem_VI_tem_preco_ref: bool = False
    elem_VI_tem_tco: bool = False       # TIC: mencionou TCO

    # Elemento VII — Parcelamento (OBRIGATÓRIO)
    elem_VII_texto: str = ""

    # Elemento VIII — Correlatas/Interdependentes
    elem_VIII_texto: str = ""

    # Elemento IX — Previsão no PCA
    elem_IX_texto: str = ""

    # Elemento X — Resultados Pretendidos
    elem_X_texto: str = ""

    # Elemento XI — Providências Prévias
    elem_XI_texto: str = ""

    # Elemento XII — Impactos Ambientais
    elem_XII_texto: str = ""

    # Elemento XIII — Posicionamento Conclusivo (OBRIGATÓRIO)
    elem_XIII_texto: str = ""
    elem_XIII_concluiu_viavel: Optional[bool] = None  # True/False/None

    # Assinaturas
    tem_assinatura_equipe: bool = False

    # PCA
    tem_referencia_pca: bool = False
    cod_pca: str = ""


# ─────────────────────────────────────────────────────────────────────
#  EXTRAÇÃO DE TEXTO
# ─────────────────────────────────────────────────────────────────────

def _erro(msg: str):
    print(f"\n❌ ERRO: {msg}\n", file=sys.stderr)
    sys.exit(1)


def _caminho_seguro(caminho: str) -> str:
    import shutil, tempfile
    ext = Path(caminho).suffix.lower()
    temp_dir = tempfile.gettempdir()
    dest = os.path.join(temp_dir, f"etp_temp{ext}")
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
#  PARSING DO ETP
# ─────────────────────────────────────────────────────────────────────

# Padrões de cabeçalho de elemento.
# Prioridade: títulos ALL-CAPS do SEI (linha inteira) → depois romano/numérico.
# ATENÇÃO: o mapeamento de slots segue a lógica das VERIFICAÇÕES do script,
# não necessariamente a numeração da Lei. Ex.: slot VII = parcelamento, que no
# HTML do SEI aparece na seção citada como "inciso VIII da Lei 14.133".
_ELEM_PATS = {
    # I — Descrição da Necessidade
    "I":    [r"^DESCRIÇÃO DA NECESSIDADE\b",
             r"^I\s*[-–.]\s*DESCRIÇÃO DA NECESSIDADE",
             r"\bI\b[\s\.\-–]+descri[çc][aã]o\s+da\s+necessidade",
             r"1[\.\s]+(?:descri[çc][aã]o\s+da\s+necessidade|necessidade)"],
    # II — Requisitos da Contratação
    "II":   [r"^REQUISITOS DA CONTRATA[ÇC][ÃA]O\b",
             r"^II\s*[-–.]\s*REQUISITOS",
             r"\bII\b[\s\.\-–]+requisitos",
             r"2[\.\s]+requisitos"],
    # III — Levantamento de Mercado
    "III":  [r"^LEVANTAMENTO DE MERCADO\b",
             r"^III\s*[-–.]\s*LEVANTAMENTO",
             r"\bIII\b[\s\.\-–]+levantamento",
             r"3[\.\s]+levantamento"],
    # IV — Descrição da Solução como um Todo
    "IV":   [r"^DESCRIÇÃO DA SOLUÇÃO COMO UM TODO\b",
             r"^IV\s*[-–.]\s*DESCRIÇÃO DA SOLUÇÃO",
             r"\bIV\b[\s\.\-–]+descri[çc][aã]o\s+da\s+solu[çc][aã]o",
             r"4[\.\s]+solu[çc][aã]o"],
    # V — Estimativa das Quantidades
    "V":    [r"^ESTIMATIVAS? DAS? QUANTIDADES?\b",
             r"^V\s*[-–.]\s*ESTIMATIVA",
             r"\bV\b[\s\.\-–]+estimativa\s+d[ae]s?\s+quantidades",
             r"estimativa\s+d(?:as|e)\s+quantidades"],
    # VI — Estimativa do Valor da Contratação
    "VI":   [r"^ESTIMATIVA DO VALOR DA CONTRATA[ÇC][ÃA]O\b",
             r"^VI\s*[-–.]\s*ESTIMATIVA DO VALOR",
             r"\bVI\b[\s\.\-–]+estimativa\s+do\s+valor",
             r"estimativa\s+d[oe]\s+valor"],
    # VII — Justificativa para o Parcelamento ou Não
    "VII":  [r"^JUSTIFICATIVA PARA O PARCELAMENTO\b",
             r"^VII\s*[-–.]\s*(?:JUSTIFICATIVA|PARCELAMENTO)",
             r"\bVII\b[\s\.\-–]+parcelamento",
             r"justificativa\s+para\s+o\s+parcelamento"],
    # VIII — Contratações Correlatas e/ou Interdependentes
    "VIII": [r"^CONTRATA[ÇC][ÕO]ES CORRELATAS\b",
             r"^VIII\s*[-–.]",
             r"\bVIII\b[\s\.\-–]+contrata[çc][oõ]es\s+correlatas",
             r"contrata[çc][oõ]es\s+correlatas"],
    # IX — Demonstração da Previsão no PCA
    "IX":   [r"^DEMONSTRAÇÃO DA PREVISÃO DA CONTRATA[ÇC][ÃA]O\b",
             r"^IX\s*[-–.]",
             r"\bIX\b[\s\.\-–]+",
             r"demonstra[çc][aã]o\s+da\s+previs[aã]o|previs[aã]o\s+no\s+pca"],
    # X — Demonstrativo dos Resultados Pretendidos
    "X":    [r"^DEMONSTRATIVO DOS RESULTADOS PRETENDIDOS\b",
             r"^X\s*[-–.]",
             r"\bX\b[\s\.\-–]+(?!I)",
             r"resultados\s+pretendidos"],
    # XI — Providências a serem Adotadas
    "XI":   [r"^PROVIDÊNCIAS A SEREM ADOTADAS\b",
             r"^XI\s*[-–.]",
             r"\bXI\b[\s\.\-–]+",
             r"provid[eê]ncias\s+a\s+serem\s+adotadas"],
    # XII — Impactos Ambientais
    "XII":  [r"^DESCRIÇÃO DE POSS[ÍI]VEIS IMPACTOS AMBIENTAIS\b",
             r"^XII\s*[-–.]",
             r"\bXII\b[\s\.\-–]+",
             r"impactos?\s+ambientais?"],
    # XIII — Posicionamento Conclusivo
    "XIII": [r"^POSICIONAMENTO CONCLUSIVO\b",
             r"^XIII\s*[-–.]",
             r"\bXIII\b[\s\.\-–]+",
             r"posicionamento\s+conclusivo"],
}

def _bloco_elemento(texto: str, elem: str) -> str:
    """Extrai o bloco de texto de um elemento do ETP (entre seu cabeçalho e o próximo)."""
    elem_ordem = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII"]
    idx = elem_ordem.index(elem)

    # Tenta cada padrão de cabeçalho para encontrar o início
    start = -1
    for pat in _ELEM_PATS[elem]:
        m = re.search(pat, texto, re.IGNORECASE | re.MULTILINE)
        if m:
            start = m.start()
            break
    if start == -1:
        return ""

    # Encontra o início do próximo elemento para delimitar o bloco
    end = len(texto)
    for prox_elem in elem_ordem[idx + 1:]:
        for pat in _ELEM_PATS[prox_elem]:
            m2 = re.search(pat, texto[start + 5:], re.IGNORECASE | re.MULTILINE)
            if m2:
                end = min(end, start + 5 + m2.start())
                break
        else:
            continue
        break

    return texto[start:end].strip()


def parse_etp(texto: str) -> ETP:
    etp = ETP()
    etp.texto_completo = texto

    # Número do processo SEI
    m = re.search(r"\b(\d{2}\.\d{2}\.\d{4}\.\d{7}/\d{4}-\d{2})\b", texto)
    if m:
        etp.num_processo = m.group(1)

    # Objeto/descrição — tenta extrair de citação explícita de objeto ou,
    # no formato SEI (HTML), da primeira frase substantiva da Necessidade
    m = re.search(r"(?:objeto[:\s]+)(.{20,300}?)(?:\n[A-Z\d]|\Z)", texto,
                  re.IGNORECASE | re.DOTALL)
    if m:
        etp.objeto_descricao = m.group(1).strip()[:300]
    else:
        # Fallback: primeira frase após "DESCRIÇÃO DA NECESSIDADE" que contenha verbo de ação
        m2 = re.search(r"DESCRIÇÃO DA NECESSIDADE[^\n]*\n(?:[^\n]*\n){0,3}"
                       r"([A-ZA-záéíóúàâêôãõç][^.]{30,300}\.)", texto, re.DOTALL)
        if m2:
            etp.objeto_descricao = m2.group(1).strip()[:300]

    # Unidade requisitante
    for pat in [r"(?:Unidade\s+Requisitante|[Áa]rea\s+Requisitante)[:\s]+([^\n]{5,80})",
                r"(?:Órgão|Institui[çc][aã]o)[:\s]+([A-ZÁÉÍÓÚ][^\n]{4,60})"]:
        m = re.search(pat, texto[:2000], re.IGNORECASE)
        if m:
            etp.unidade_requisitante = m.group(1).strip()
            break

    # Detectar se é TIC
    etp.is_tic = bool(re.search(
        r"\bTIC\b|tecnologia\s+da\s+informa[çc][aã]o|software|hardware|sistema\s+de\s+informa[çc][aã]o"
        r"|solu[çc][aã]o\s+de\s+TI|contrata[çc][aã]o\s+de\s+TI|MOTec|CNMP\s+n[º°]?\s*283",
        texto, re.IGNORECASE
    ))

    # PCA
    etp.tem_referencia_pca = bool(re.search(
        r"\bPCA\b|Plano\s+de\s+Contrata[çc][oõ]es\s+Anual", texto, re.IGNORECASE
    ))
    m_pca = re.search(r"\b([A-Z]{1,5}-?\d{2,4}|[A-Z]\d{3,4})\b", texto)
    if m_pca:
        etp.cod_pca = m_pca.group(1)

    # Assinaturas
    etp.tem_assinatura_equipe = bool(re.search(
        r"equipe\s+de\s+planejamento|integrante\s+(?:requisitante|t[eé]cnico|administrativo)"
        r"|assinado\s+por|data[:\s]+\d{2}/\d{2}",
        texto[-3000:], re.IGNORECASE
    ))

    # ─── Extrair cada elemento ───────────────────────────────────────
    etp.elem_I_texto   = _bloco_elemento(texto, "I")
    etp.elem_II_texto  = _bloco_elemento(texto, "II")
    etp.elem_III_texto = _bloco_elemento(texto, "III")
    etp.elem_IV_texto  = _bloco_elemento(texto, "IV")
    etp.elem_V_texto   = _bloco_elemento(texto, "V")
    etp.elem_VI_texto  = _bloco_elemento(texto, "VI")
    etp.elem_VII_texto = _bloco_elemento(texto, "VII")
    etp.elem_VIII_texto= _bloco_elemento(texto, "VIII")
    etp.elem_IX_texto  = _bloco_elemento(texto, "IX")
    etp.elem_X_texto   = _bloco_elemento(texto, "X")
    etp.elem_XI_texto  = _bloco_elemento(texto, "XI")
    etp.elem_XII_texto = _bloco_elemento(texto, "XII")
    etp.elem_XIII_texto= _bloco_elemento(texto, "XIII")

    # Análises dentro dos elementos
    # I — foco em solução?
    if etp.elem_I_texto:
        palavras_solucao = ["contratar", "contratação de", "aquisição de", "adquirir",
                            "fornecimento de", "compra de", "locação de"]
        inicio = etp.elem_I_texto[:400].lower()
        etp.elem_I_foco_solucao = sum(1 for p in palavras_solucao if p in inicio) >= 2

    # III — alternativas e alíneas TIC
    if etp.elem_III_texto:
        t = etp.elem_III_texto.lower()
        etp.elem_III_tem_alternativas = bool(re.search(
            r"alternativa|solu[çc][aã]o\s+(?:\d+|similar)|outro\s+[oó]rg[aã]o"
            r"|software\s+livre|software\s+p[úu]blico|compara[çc][aã]o",
            t
        ))
        etp.elem_III_tic_alíneas = bool(re.search(
            r"software\s+livre|software\s+p[úu]blico|outro\s+[oó]rg[aã]o"
            r"|modelos?\s+de\s+presta[çc][aã]o|servi[çc]o\s+(?:como|em\s+nuvem|saas)"
            r"|amplia[çc][aã]o\s+da\s+solu[çc][aã]o|substitui[çc][aã]o",
            t
        ))

    # V — memória de cálculo
    if etp.elem_V_texto:
        etp.elem_V_tem_memoria = bool(re.search(
            r"hist[oó]rico|m[eé]moria\s+de\s+c[áa]lculo|s[eé]rie\s+hist[oó]rica"
            r"|consumo\s+(?:m[eé]dio|anterior)|levantamento|projeção|estimativa\s+baseada"
            r"|per\s+capita|demanda\s+anterior|exerc[ií]cio\s+anterior",
            etp.elem_V_texto, re.IGNORECASE
        ))

    # VI — preço referencial e TCO
    if etp.elem_VI_texto:
        etp.elem_VI_tem_preco_ref = bool(re.search(
            r"pre[çc]o\s+(?:unit[áa]rio|referencial|de\s+refer[eê]ncia)"
            r"|pesquisa\s+de\s+pre[çc]o|painel\s+de\s+pre[çc]o|comprasnet"
            r"|ata\s+de\s+registro|contrata[çc][aã]o\s+anterior|banco\s+de\s+pre[çc]o"
            r"|proposta\s+comercial|proposta\s+de\s+pre[çc]o|or[çc]amento"
            r"|IN\s+SEGES.{0,10}65|art\.?\s*7[º°]\s+da\s+IN"
            r"|metodologia\s+de\s+apura[çc][aã]o|justificativa\s+de\s+pre[çc]o"
            r"|verifica[çc][aã]o\s+de\s+compatibilidade|negoci[ao]|desconto",
            etp.elem_VI_texto, re.IGNORECASE
        ))
        etp.elem_VI_tem_tco = bool(re.search(
            r"TCO|total\s+cost\s+of\s+ownership|custo\s+total\s+de\s+propriedade"
            r"|ciclo\s+de\s+vida\s+da\s+solu[çc][aã]o|custos?\s+(?:de\s+aquisi[çc][aã]o"
            r"|\s*de\s+manuten[çc][aã]o|\s*totais)",
            etp.elem_VI_texto, re.IGNORECASE
        ))

    # XIII — conclusão viável/inviável
    if etp.elem_XIII_texto:
        t13 = etp.elem_XIII_texto.lower()
        if re.search(r"vi[aá]vel|viabilidade\s+t[eé]cnica|recomend[ao]\s+a\s+contrata"
                     r"|prosseguir|conclus[aã]o\s+positiva"
                     r"|contrata[çc][aã]o\s+(?:[eé]\s+)?vi[aá]vel", t13):
            etp.elem_XIII_concluiu_viavel = True
        elif re.search(r"invi[aá]vel|n[aã]o\s+(?:[eé]\s+)?vi[aá]vel|recomend[ao]\s+(?:o\s+)?n[aã]o"
                       r"|conclus[aã]o\s+negativa", t13):
            etp.elem_XIII_concluiu_viavel = False

    return etp


# ─────────────────────────────────────────────────────────────────────
#  CHECKLIST DE CONFORMIDADE
# ─────────────────────────────────────────────────────────────────────

def _add(achados: list, **kwargs) -> None:
    kwargs["numero"] = len(achados) + 1
    achados.append(Achado(**kwargs))


def checar_elementos_obrigatorios(etp: ETP, achados: list) -> None:
    """Verifica os 5 elementos obrigatórios: I, V, VI, VII, XIII."""

    fund_base = (
        "Art. 18, § 1º, da Lei nº 14.133/2021; art. 9º, § 1º, da IN SEGES/ME nº 58/2022; "
        "art. 23, § 1º, do Decreto Estadual (PI) nº 21.872/2023."
    )

    obrigatorios = [
        ("I",   "Descrição da Necessidade da Contratação", etp.elem_I_texto),
        ("V",   "Estimativa de Quantidades",               etp.elem_V_texto),
        ("VI",  "Estimativa do Valor da Contratação",      etp.elem_VI_texto),
        ("VII", "Justificativas para o Parcelamento",      etp.elem_VII_texto),
        ("XIII","Posicionamento Conclusivo",                etp.elem_XIII_texto),
    ]

    for roman, nome, texto in obrigatorios:
        if not texto or len(texto.strip()) < 60:
            _add(achados,
                titulo=f"Ausência do Elemento {roman} — {nome} (OBRIGATÓRIO)",
                tipo="Vício Formal",
                localizacao=f"Elemento {roman} do ETP — {nome}",
                inconsistencia=(
                    f"O Elemento {roman} ({nome}) não foi localizado ou está com "
                    "conteúdo insuficiente. Trata-se de elemento de preenchimento "
                    "obrigatório, independentemente do objeto contratado. Sua ausência "
                    "torna o ETP formalmente incompleto e impede o prosseguimento "
                    "regular do processo de contratação."
                ),
                fundamentacao=fund_base,
                acao=(
                    f"Elaborar e inserir o Elemento {roman} ({nome}) no ETP, "
                    "com conteúdo substantivo e fundamentado, conforme as diretrizes "
                    "dos normativos aplicáveis."
                ),
                sugestao=f"[Elaborar o Elemento {roman} — ver art. 9º, {roman}, da IN 58/2022 "
                         f"e art. 23, {roman}, do Decreto PI 21.872/2023 para orientação]",
            )


def checar_elemento_I(etp: ETP, achados: list) -> None:
    """Elemento I — Descrição da Necessidade (foco no problema)."""
    if not etp.elem_I_texto or len(etp.elem_I_texto.strip()) < 60:
        return  # já capturado em checar_elementos_obrigatorios

    if etp.elem_I_foco_solucao:
        _add(achados,
            titulo="Aprimoramento do Elemento I — Necessidade Descrita como Solução em Vez de Problema",
            tipo="Erro Material",
            localizacao="Elemento I do ETP — Descrição da Necessidade da Contratação",
            inconsistencia=(
                "O Elemento I descreve a solução pretendida (contratação/aquisição) "
                "em vez do problema administrativo que originou a demanda. "
                "A necessidade deve responder à pergunta 'qual problema ou carência "
                "a Administração precisa resolver?', não 'o que será contratado?'. "
                "A norma exige que o ETP evidencie o problema 'sob a perspectiva "
                "do interesse público', com foco na lacuna e não na saída."
            ),
            fundamentacao=(
                "Art. 18, § 1º, inciso I, da Lei nº 14.133/2021 — 'descrição da "
                "necessidade da contratação, considerado o problema a ser resolvido "
                "sob a perspectiva do interesse público'; art. 23, I, do Decreto "
                "Estadual (PI) nº 21.872/2023."
            ),
            acao=(
                "Reescrever o Elemento I deslocando o foco para o problema concreto: "
                "(a) qual carência ou risco institucional motiva a contratação; "
                "(b) qual impacto negativo ocorre na ausência do bem/serviço; "
                "(c) como a contratação resolve esse problema. "
                "A solução pode ser mencionada, mas apenas como consequência lógica."
            ),
            sugestao=(
                "[Ex: 'A necessidade decorre de [lacuna/carência concreta]. "
                "A ausência de [bem/serviço] compromete [atividade institucional], "
                "expondo o MPPI a [risco: prejuízo, descumprimento legal, etc.]. "
                "A contratação é a medida necessária para sanar essa carência.']"
            ),
        )

    # Verificar se há referência ao interesse público
    if etp.elem_I_texto and not re.search(
        r"interesse\s+p[úu]blico|atividade\s+(?:fim|institucional|ministerial)"
        r"|servi[çc]o\s+[àa]\s+sociedade|miss[aã]o\s+institucional|objetivo\s+institucional",
        etp.elem_I_texto, re.IGNORECASE
    ):
        _add(achados,
            titulo="Ausência de Vinculação da Necessidade ao Interesse Público (Elemento I)",
            tipo="Sugestão de Melhoria",
            localizacao="Elemento I do ETP — Descrição da Necessidade da Contratação",
            inconsistencia=(
                "A descrição da necessidade não demonstra expressamente a vinculação "
                "da contratação ao interesse público ou às atividades institucionais "
                "do MPPI. A norma exige que o problema seja descrito 'sob a perspectiva "
                "do interesse público', evidenciando que a contratação serve à missão "
                "da instituição e não a conveniências particulares."
            ),
            fundamentacao=(
                "Art. 18, § 1º, inciso I, da Lei nº 14.133/2021; art. 6º, inciso II, "
                "da IN SEGES/ME nº 58/2022 (viabilidade técnica, socioeconômica e ambiental)."
            ),
            acao=(
                "Acrescentar parágrafo ou frase que vincule expressamente a necessidade "
                "à missão institucional do MPPI ou ao interesse público atendido."
            ),
            sugestao=(
                "[Ex: '...comprometendo a continuidade dos serviços prestados à "
                "sociedade pelo Ministério Público do Estado do Piauí, em especial "
                "quanto a [atividade finalística impactada].']"
            ),
        )


def checar_elemento_II(etp: ETP, achados: list) -> None:
    """Elemento II — Requisitos da Contratação."""
    if not etp.elem_II_texto or len(etp.elem_II_texto.strip()) < 40:
        _add(achados,
            titulo="Ausência ou Insuficiência do Elemento II — Requisitos da Contratação",
            tipo="Vício Formal",
            localizacao="Elemento II do ETP — Requisitos da Contratação",
            inconsistencia=(
                "O Elemento II (Requisitos da Contratação) não foi localizado ou "
                "apresenta conteúdo insuficiente. Este elemento deve descrever os "
                "critérios e práticas de sustentabilidade, os padrões mínimos de "
                "qualidade e desempenho, e demais requisitos necessários e suficientes "
                "para a escolha da solução adequada."
            ),
            fundamentacao=(
                "Art. 18, § 1º, inciso III, da Lei nº 14.133/2021; art. 9º, II, da "
                "IN SEGES/ME nº 58/2022; art. 23, II, do Decreto PI nº 21.872/2023."
            ),
            acao="Elaborar o Elemento II descrevendo os requisitos necessários à contratação.",
            sugestao=(
                "[Incluir: critérios de qualidade e desempenho; requisitos de sustentabilidade; "
                "habilitações exigidas; padrões técnicos mínimos aplicáveis ao objeto]"
            ),
        )
        return

    # Verificar TIC: requisitos específicos (art. 17, I, a-s da Res. CNMP 283/2024)
    if etp.is_tic:
        t2 = etp.elem_II_texto.lower()
        requisitos_tic_presentes = sum([
            bool(re.search(r"neg[oó]cio|funcional", t2)),
            bool(re.search(r"capacita[çc][aã]o|treinamento", t2)),
            bool(re.search(r"seguran[çc]a|privacidade|lgpd|dados\s+pessoais", t2)),
            bool(re.search(r"arquitetura\s+tecnol[oó]gica|interoperabilidade|linguagem", t2)),
            bool(re.search(r"implanta[çc][aã]o|ambiente\s+de\s+produ[çc][aã]o", t2)),
        ])
        if requisitos_tic_presentes < 2:
            _add(achados,
                titulo="Insuficiência de Requisitos Específicos de TIC (Elemento II)",
                tipo="Vício Formal",
                localizacao="Elemento II do ETP — Requisitos da Contratação (TIC)",
                inconsistencia=(
                    "Trata-se de contratação de Solução de TIC, mas o Elemento II não "
                    "contempla os requisitos específicos exigidos para essa categoria. "
                    "A Resolução CNMP nº 283/2024 e o MOTec exigem a especificação de "
                    "até 19 tipos de requisitos (a-s): negócio, capacitação, legais, "
                    "manutenção, temporais, segurança e privacidade (LGPD), sociais/"
                    "ambientais, arquitetura tecnológica, projeto/implementação, "
                    "implantação, garantia, capacitação técnica, experiência e formação "
                    "da equipe, metodologia de trabalho, segurança de ativos de TI, "
                    "prova de conceito, reajuste e margens de preferência."
                ),
                fundamentacao=(
                    "Art. 17, inciso I, alíneas a-s, da Resolução CNMP nº 283/2024; "
                    "MOTec (Artefato III, seção 2); art. 9º, II, da IN SEGES/ME nº 58/2022."
                ),
                acao=(
                    "Complementar o Elemento II com os requisitos específicos de TIC "
                    "aplicáveis ao objeto contratado, organizados por tipo (negócio, "
                    "capacitação, legais, segurança/privacidade, arquitetura, etc.)."
                ),
                sugestao=(
                    "[Estruturar os requisitos em seções: 2.1 De Negócio; 2.2 De Capacitação; "
                    "2.3 Legais; 2.4 De Segurança e Privacidade (LGPD); 2.5 De Arquitetura "
                    "Tecnológica; 2.6 De Implantação; 2.7 De Garantia; etc.]"
                ),
            )


def checar_elemento_III(etp: ETP, achados: list) -> None:
    """Elemento III — Levantamento de Mercado."""
    if not etp.elem_III_texto or len(etp.elem_III_texto.strip()) < 60:
        _add(achados,
            titulo="Ausência ou Insuficiência do Elemento III — Levantamento de Mercado",
            tipo="Vício Formal",
            localizacao="Elemento III do ETP — Levantamento de Mercado",
            inconsistencia=(
                "O Elemento III (Levantamento de Mercado) não foi localizado ou "
                "apresenta conteúdo insuficiente. Este elemento deve demonstrar a "
                "análise das alternativas possíveis e a justificativa técnica e "
                "econômica da solução escolhida."
            ),
            fundamentacao=(
                "Art. 18, § 1º, inciso V, da Lei nº 14.133/2021; art. 9º, III, da "
                "IN SEGES/ME nº 58/2022; art. 23, III, do Decreto PI nº 21.872/2023."
            ),
            acao=(
                "Elaborar o Elemento III com: análise de alternativas disponíveis; "
                "consulta a outros órgãos com soluções similares; justificativa técnica "
                "e econômica da escolha."
            ),
            sugestao=(
                "[Descrever as alternativas consideradas, o critério de comparação e a "
                "justificativa para a solução escolhida. Indicar órgãos com contratações "
                "similares pesquisadas.]"
            ),
        )
        return

    if not etp.elem_III_tem_alternativas:
        _add(achados,
            titulo="Levantamento de Mercado sem Análise Comparativa de Alternativas (Elemento III)",
            tipo="Erro Material",
            localizacao="Elemento III do ETP — Levantamento de Mercado",
            inconsistencia=(
                "O Elemento III não apresenta análise comparativa entre alternativas "
                "de solução. O levantamento de mercado deve ir além da descrição da "
                "solução escolhida e demonstrar quais outras opções foram consideradas "
                "(incluindo não contratar, contratar de forma diferente, ou adotar "
                "solução já disponível em outro órgão) e por que foram afastadas."
            ),
            fundamentacao=(
                "Art. 18, § 1º, inciso V, da Lei nº 14.133/2021 — 'análise das "
                "alternativas possíveis, e justificativa técnica e econômica da escolha'; "
                "art. 23, III, a-d, do Decreto PI nº 21.872/2023; art. 12 da IN 58/2022."
            ),
            acao=(
                "Complementar o Elemento III com: (a) identificação e descrição das "
                "alternativas consideradas (mínimo 2-3); (b) critério de comparação "
                "(técnico e econômico); (c) justificativa da escolha; (d) soluções "
                "descartadas e razão do descarte."
            ),
            sugestao=(
                "[Ex: Solução 1: [descrição] — Viável/Inviável por [razão]. "
                "Solução 2: [descrição] — Viável/Inviável por [razão]. "
                "Solução adotada: [descrição] — escolhida por [justificativa técnica e econômica].]"
            ),
        )

    # TIC — verificar alíneas específicas (CNMP 283, art. 10, I, a-g)
    if etp.is_tic and not etp.elem_III_tic_alíneas:
        _add(achados,
            titulo="Levantamento de Mercado para TIC sem Análise das Alíneas Específicas (Elemento III)",
            tipo="Vício Formal",
            localizacao="Elemento III do ETP — Levantamento de Mercado (TIC)",
            inconsistencia=(
                "Para contratações de Soluções de TIC, o levantamento de mercado deve "
                "analisar especificamente: a) disponibilidade de solução similar em "
                "outro órgão; b) existência de software livre ou software público; "
                "c) diferentes modelos de prestação de serviço (SaaS, IaaS, etc.); "
                "d) possibilidade de aquisição como bem ou serviço; "
                "e) ampliação ou substituição da solução já implantada. "
                "Não foram identificadas essas análises no Elemento III."
            ),
            fundamentacao=(
                "Art. 10, inciso I, alíneas a-g, da Resolução CNMP nº 283/2024; "
                "MOTec, seção 4 (Análise de Soluções Possíveis); art. 16 da IN 58/2022."
            ),
            acao=(
                "Complementar o Elemento III verificando e documentando cada alínea: "
                "a) há solução similar disponível em outro órgão do MP ou da Administração? "
                "b) existe software livre ou software público equivalente? "
                "c) quais modelos de prestação estão disponíveis no mercado? "
                "d) é mais vantajoso adquirir como bem ou contratar como serviço? "
                "e) é possível ampliar a solução atual em vez de contratar nova?"
            ),
            sugestao=(
                "[Organizar em subseções: 4.1 Disponibilidade em outros órgãos; "
                "4.2 Software livre/público; 4.3 Modelos de prestação; "
                "4.4 Bens x Serviço; 4.5 Ampliação da solução atual; "
                "4.6 Justificativa da solução escolhida]"
            ),
        )

    # Verificar pesquisa a outros órgãos
    if not re.search(
        r"outro\s+[oó]rg[aã]o|outro\s+MP|outro\s+Minist[eé]rio|TCE|AGU|CNMP"
        r"|painel\s+de\s+pre[çc]o|contratanet|comprasnet",
        etp.elem_III_texto, re.IGNORECASE
    ):
        _add(achados,
            titulo="Ausência de Pesquisa de ETP de Outros Órgãos (Elemento III)",
            tipo="Sugestão de Melhoria",
            localizacao="Elemento III do ETP — Levantamento de Mercado",
            inconsistencia=(
                "O levantamento de mercado não registra a consulta a ETPs de outros "
                "órgãos ou entidades da Administração Pública com soluções similares. "
                "Essa pesquisa é recomendada para identificar soluções já testadas, "
                "evitar retrabalho e assegurar a vantajosidade da solução escolhida."
            ),
            fundamentacao=(
                "Art. 26 do Decreto Estadual (PI) nº 21.872/2023; art. 12 da IN SEGES/ME "
                "nº 58/2022 ('pesquisar o ETP de outras unidades'); art. 13 da Resolução "
                "CNMP nº 283/2024 (uso de ETP de outro órgão como subsídio)."
            ),
            acao=(
                "Registrar no Elemento III a pesquisa realizada junto a outros órgãos "
                "ou entidades, indicando: órgão pesquisado, objeto contratado, resultado "
                "da pesquisa e conclusão sobre a aplicabilidade ao caso concreto."
            ),
            sugestao=(
                "[Ex: 'Foram pesquisados ETPs nos sistemas ComprasNet e PNE-CNMP para "
                "soluções similares. Identificou-se contratação análoga no [órgão X], "
                "conforme [número do processo/ARP]. A solução foi/não foi adotada como "
                "referência por [razão].']"
            ),
        )


def checar_elemento_V(etp: ETP, achados: list) -> None:
    """Elemento V — Estimativa de Quantidades (obrigatório)."""
    if not etp.elem_V_texto or len(etp.elem_V_texto.strip()) < 40:
        return  # já capturado em checar_elementos_obrigatorios

    if not etp.elem_V_tem_memoria:
        _add(achados,
            titulo="Estimativa de Quantidades sem Memória de Cálculo (Elemento V)",
            tipo="Vício Formal",
            localizacao="Elemento V do ETP — Estimativa de Quantidades",
            inconsistencia=(
                "A estimativa de quantidades não apresenta memória de cálculo ou "
                "documentos de suporte que demonstrem a origem dos quantitativos. "
                "A norma exige que as quantidades sejam 'acompanhadas das memórias "
                "de cálculo e dos documentos que lhes dão suporte', sendo insuficiente "
                "informar apenas o número sem explicar como foi obtido."
            ),
            fundamentacao=(
                "Art. 18, § 1º, inciso IV, da Lei nº 14.133/2021 — 'estimativas das "
                "quantidades para a contratação, acompanhadas das memórias de cálculo'; "
                "art. 9º, V, da IN SEGES/ME nº 58/2022; art. 23, V, do Decreto PI."
            ),
            acao=(
                "Complementar o Elemento V com a memória de cálculo dos quantitativos: "
                "(a) base de dados utilizada (histórico de consumo, levantamento por "
                "unidade beneficiária, série histórica, etc.); "
                "(b) fórmula ou método de estimativa; "
                "(c) documentos comprobatórios (planilhas, relatórios, inventários)."
            ),
            sugestao=(
                "[Ex: 'Quantidade apurada com base no histórico de consumo dos "
                "últimos 12 meses ([X] unidades/ano), acrescido de [Y]% de margem "
                "de segurança para atendimento de demandas emergenciais, "
                "totalizando [Z] unidades. Memória de cálculo constante do Anexo I.']"
            ),
        )


def checar_elemento_VI(etp: ETP, achados: list) -> None:
    """Elemento VI — Estimativa do Valor (obrigatório)."""
    if not etp.elem_VI_texto or len(etp.elem_VI_texto.strip()) < 40:
        return  # já capturado

    if not etp.elem_VI_tem_preco_ref:
        _add(achados,
            titulo="Estimativa de Valor sem Indicação de Fonte/Preço Referencial (Elemento VI)",
            tipo="Vício Formal",
            localizacao="Elemento VI do ETP — Estimativa do Valor da Contratação",
            inconsistencia=(
                "A estimativa de valor não indica a fonte dos preços referenciais "
                "utilizados (pesquisa de mercado, painel de preços, ARP, contratação "
                "anterior, etc.). A norma exige que a estimativa seja acompanhada "
                "de 'preços unitários referenciais, memórias de cálculo e documentos "
                "que lhe dão suporte', para permitir a aferição da vantajosidade."
            ),
            fundamentacao=(
                "Art. 18, § 1º, inciso VI, da Lei nº 14.133/2021; art. 9º, VI, da "
                "IN SEGES/ME nº 58/2022; art. 23, VI, do Decreto PI nº 21.872/2023."
            ),
            acao=(
                "Indicar expressamente as fontes utilizadas para a estimativa: "
                "painel de preços do governo federal, pesquisa de mercado com "
                "fornecedores, atas de registro de preços vigentes, contratos "
                "similares de outros órgãos, etc. Anexar ou referenciar as memórias "
                "de cálculo e os documentos de pesquisa."
            ),
            sugestao=(
                "[Ex: 'O valor estimado de R$ X.XXX,XX foi obtido mediante pesquisa "
                "de preços realizada em [data], consultando: (1) Painel de Preços "
                "(painel.compras.gov.br); (2) Ata de Registro de Preços nº XX/XXXX; "
                "(3) Proposta de [Fornecedor X]. Memória de cálculo constante do Anexo II.']"
            ),
        )

    # TIC — TCO
    if etp.is_tic and not etp.elem_VI_tem_tco:
        _add(achados,
            titulo="Estimativa de Valor para TIC sem Análise de Custo Total de Propriedade — TCO (Elemento VI)",
            tipo="Sugestão de Melhoria",
            localizacao="Elemento VI do ETP — Estimativa do Valor da Contratação (TIC)",
            inconsistencia=(
                "Para contratações de Soluções de TIC, a estimativa de valor deve "
                "incluir a comparação de Custos Totais de Propriedade (TCO — Total "
                "Cost Ownership): custos do ciclo de vida de cada solução (aquisição "
                "de ativos, insumos, garantia, manutenção). Não foi identificada essa "
                "análise no Elemento VI."
            ),
            fundamentacao=(
                "Art. 10, inciso II, alínea a, da Resolução CNMP nº 283/2024 "
                "('comparação de custos totais de propriedade — TCO'); "
                "MOTec, seções 4.4 a 4.6."
            ),
            acao=(
                "Complementar o Elemento VI com análise de TCO para cada alternativa "
                "viável: custos de aquisição, licenciamento, manutenção, suporte, "
                "treinamento, migração de dados e descontinuação, ao longo do ciclo "
                "de vida previsto da solução."
            ),
            sugestao=(
                "[Tabela comparativa de TCO: Solução 1 — Custo de aquisição: R$X | "
                "Manutenção anual: R$Y | Suporte: R$Z | TCO (5 anos): R$W. "
                "Solução 2 — [idem]. Solução adotada: menor TCO ou melhor custo-benefício.]"
            ),
        )


def checar_elemento_VII(etp: ETP, achados: list) -> None:
    """Elemento VII — Parcelamento."""
    if not etp.elem_VII_texto or len(etp.elem_VII_texto.strip()) < 40:
        return  # já capturado

    # Verificar se há posição explícita sobre parcelar ou não parcelar
    t7 = etp.elem_VII_texto.lower()
    tem_posicao = bool(re.search(
        r"n[aã]o\s+(?:[eé]\s+)?(?:vi[aá]vel|adequado|conveniente|recomend[aá]vel)?\s*parcelar"
        r"|n[aã]o\s+ser[aá]\s+objeto\s+de\s+parcelamento"
        r"|n[aã]o\s+parcelamento|parcelamento\s+n[aã]o"
        r"|parcelamento\s+(?:n[aã]o\s+[eé]\s+)?(?:vi[aá]vel|adequado|recomend[aá]vel)"
        r"|opt[ao]u.{0,20}parcel|parcel[ao].{0,30}em\s+\d+|lote\s+[úu]nico"
        r"|objeto\s+[eé]\s+(?:uno|[úu]nico|indivisível)|indivisível|adjudicad[ao]\s+em\s+lote",
        t7
    ))
    if not tem_posicao:
        _add(achados,
            titulo="Justificativa de Parcelamento sem Posicionamento Explícito (Elemento VII)",
            tipo="Vício Formal",
            localizacao="Elemento VII do ETP — Justificativas para o Parcelamento",
            inconsistencia=(
                "O Elemento VII não expressa posicionamento claro sobre o parcelamento: "
                "se o objeto será ou não parcelado, e por quê. A norma exige 'justificativas "
                "para o parcelamento ou não parcelamento', portanto é necessário manifestar "
                "uma das duas opções com fundamentação técnica e econômica."
            ),
            fundamentacao=(
                "Art. 18, § 1º, inciso VII, da Lei nº 14.133/2021; art. 9º, VII, da "
                "IN SEGES/ME nº 58/2022; art. 23, VII, do Decreto PI nº 21.872/2023."
            ),
            acao=(
                "Complementar o Elemento VII com posicionamento explícito: "
                "(a) se o objeto será parcelado, indicar os lotes e a justificativa "
                "da divisão (ampliação da competitividade, natureza técnica dos itens); "
                "(b) se não será parcelado, justificar a indivisibilidade técnica ou "
                "inviabilidade econômica do parcelamento."
            ),
            sugestao=(
                "[Ex: 'Optou-se pelo NÃO PARCELAMENTO do objeto em razão de [justificativa: "
                "interdependência técnica entre os itens; necessidade de responsabilidade "
                "única da contratada; inviabilidade econômica de múltiplos contratos]. "
                "O objeto será contratado em lote único.']"
            ),
        )


def checar_elemento_IX(etp: ETP, achados: list) -> None:
    """Elemento IX — Previsão no PCA."""
    if not etp.elem_IX_texto or len(etp.elem_IX_texto.strip()) < 20:
        if not etp.tem_referencia_pca:
            _add(achados,
                titulo="Ausência de Demonstrativo de Previsão no PCA (Elemento IX)",
                tipo="Vício Formal",
                localizacao="Elemento IX do ETP — Demonstrativo da Previsão no PCA",
                inconsistencia=(
                    "O Elemento IX (Previsão no Plano de Contratações Anual) não foi "
                    "localizado e o ETP não contém referência ao PCA vigente. A demonstração "
                    "de que a contratação está prevista no PCA é requisito legal obrigatório, "
                    "evidenciando o alinhamento da demanda com o planejamento institucional."
                ),
                fundamentacao=(
                    "Art. 18, § 1º, inciso IX, da Lei nº 14.133/2021; art. 9º, IX, da "
                    "IN SEGES/ME nº 58/2022; art. 23, IX, do Decreto PI nº 21.872/2023; "
                    "art. 5º da Resolução CNMP nº 283/2024 (contratações de TIC no PCA)."
                ),
                acao=(
                    "Incluir o Elemento IX demonstrando a previsão da contratação no PCA "
                    "aprovado para o exercício, com indicação do código ou número do item."
                ),
                sugestao=(
                    "[Ex: 'A presente contratação está prevista no Plano de Contratações "
                    "Anual do MPPI para o exercício [XXXX], sob o item [código/número], "
                    "aprovado por [ato de aprovação], alinhado ao Planejamento Estratégico "
                    "Institucional (PEI 2022-2029).']"
                ),
            )


def checar_elemento_XI(etp: ETP, achados: list) -> None:
    """Elemento XI — Providências Prévias."""
    if not etp.elem_XI_texto or len(etp.elem_XI_texto.strip()) < 30:
        _add(achados,
            titulo="Ausência ou Insuficiência do Elemento XI — Providências Prévias",
            tipo="Vício Formal",
            localizacao="Elemento XI do ETP — Providências Prévias à Celebração do Contrato",
            inconsistencia=(
                "O Elemento XI (Providências Prévias) não foi localizado ou apresenta "
                "conteúdo insuficiente. Este elemento deve identificar todas as ações "
                "necessárias antes da celebração do contrato: adaptações de ambiente, "
                "obtenção de licenças/autorizações, capacitação de servidores para "
                "fiscalização/gestão contratual."
            ),
            fundamentacao=(
                "Art. 18, § 1º, inciso XI, da Lei nº 14.133/2021; art. 9º, XI, da "
                "IN SEGES/ME nº 58/2022; art. 23, XI, do Decreto PI nº 21.872/2023."
            ),
            acao=(
                "Elaborar o Elemento XI listando todas as providências necessárias antes "
                "da contratação, com responsável e prazo estimado para cada uma."
            ),
            sugestao=(
                "[Ex: Providência 1 — Capacitação dos servidores fiscais (Responsável: "
                "[unidade]; Prazo: antes da assinatura do contrato). "
                "Providência 2 — [outras providências identificadas].']"
            ),
        )
        return

    # TIC — verificar providências específicas (art. 10, III, a-b, CNMP 283)
    if etp.is_tic:
        t11 = etp.elem_XI_texto.lower()
        tem_adequacao_ambiente = bool(re.search(
            r"infraestrutura|ambiente\s+tecnol[oó]gico|espa[çc]o\s+f[íi]sico"
            r"|cabeamento|el[eé]trica|mobili[áa]rio|logística",
            t11
        ))
        tem_rh = bool(re.search(
            r"recursos?\s+humanos?|servidores?\s+(?:necess[áa]rios?|designados?)"
            r"|equipe\s+de\s+(?:gest[aã]o|fiscaliza[çc][aã]o|implanta[çc][aã]o)"
            r"|disponibilidade\s+de\s+tempo",
            t11
        ))
        if not (tem_adequacao_ambiente and tem_rh):
            ausentes = []
            if not tem_adequacao_ambiente:
                ausentes.append("adequação do ambiente (infraestrutura tecnológica, elétrica, logística, espaço físico)")
            if not tem_rh:
                ausentes.append("recursos humanos necessários à implantação, manutenção e fiscalização")
            _add(achados,
                titulo="Providências Prévias para TIC Incompletas — Itens Específicos Ausentes (Elemento XI)",
                tipo="Vício Formal",
                localizacao="Elemento XI do ETP — Providências Prévias (TIC)",
                inconsistencia=(
                    "Para contratações de Soluções de TIC, as providências prévias devem "
                    "avaliar especificamente: (a) adequação do ambiente da instituição "
                    "(infraestrutura tecnológica e elétrica, logística, espaço físico, "
                    "mobiliário); (b) recursos humanos necessários à implantação, "
                    "manutenção, gestão e fiscalização do contrato. "
                    f"Não foram identificados: {'; '.join(ausentes)}."
                ),
                fundamentacao=(
                    "Art. 10, inciso III, alíneas a-b, da Resolução CNMP nº 283/2024; "
                    "MOTec, seção 4.11; art. 9º, XI, da IN SEGES/ME nº 58/2022."
                ),
                acao=(
                    "Complementar o Elemento XI com avaliação dos itens ausentes, "
                    "indicando para cada um: situação atual, necessidade de adaptação "
                    "e responsável pela providência."
                ),
                sugestao=(
                    "[Seção 'Adequação do Ambiente': descrever infraestrutura existente e "
                    "necessidades de adaptação. Seção 'Recursos Humanos': listar servidores "
                    "designados para implantação, gestão e fiscalização, com disponibilidade "
                    "de tempo estimada para cada fase.]"
                ),
            )


def checar_elemento_XIII(etp: ETP, achados: list) -> None:
    """Elemento XIII — Posicionamento Conclusivo."""
    if not etp.elem_XIII_texto or len(etp.elem_XIII_texto.strip()) < 40:
        return  # já capturado

    if etp.elem_XIII_concluiu_viavel is None:
        _add(achados,
            titulo="Posicionamento Conclusivo sem Declaração Explícita de Viabilidade (Elemento XIII)",
            tipo="Erro Material",
            localizacao="Elemento XIII do ETP — Posicionamento Conclusivo",
            inconsistencia=(
                "O Elemento XIII não contém declaração explícita sobre a viabilidade "
                "ou inviabilidade da contratação. A lei exige 'posicionamento conclusivo "
                "sobre a adequação da contratação para o atendimento da necessidade', "
                "o que demanda conclusão clara: a contratação é ou não é viável. "
                "Texto vago ou descritivo sem conclusão não atende ao requisito."
            ),
            fundamentacao=(
                "Art. 18, § 1º, inciso XIII, da Lei nº 14.133/2021; art. 9º, XIII, da "
                "IN SEGES/ME nº 58/2022; art. 23, XIII, do Decreto PI nº 21.872/2023; "
                "art. 16 da Resolução CNMP nº 283/2024 ('somente dará continuidade ao "
                "processo se for concluído que a contratação é adequada e viável')."
            ),
            acao=(
                "Reformular o Elemento XIII para conter: (a) referência expressa à "
                "conclusão de viabilidade técnica e econômica da contratação; "
                "(b) declaração de que a equipe de planejamento recomenda o "
                "prosseguimento (ou não) do processo; (c) data e identificação "
                "dos signatários do ETP."
            ),
            sugestao=(
                "[Ex: 'Diante dos estudos realizados, a Equipe de Planejamento da "
                "Contratação conclui pela VIABILIDADE TÉCNICA E ECONÔMICA da "
                "contratação de [objeto], conforme demonstrado nos Elementos I a XII "
                "deste Estudo Técnico Preliminar. Recomenda-se o prosseguimento do "
                "processo para elaboração do Termo de Referência.']"
            ),
        )


def checar_assinaturas(etp: ETP, achados: list) -> None:
    """Verificar assinatura pelo(s) integrante(s) da equipe de planejamento."""
    if not etp.tem_assinatura_equipe:
        _add(achados,
            titulo="ETP sem Evidência de Assinatura pela Equipe de Planejamento",
            tipo="Vício Formal",
            localizacao="Seção de Assinaturas do ETP",
            inconsistencia=(
                "O ETP não apresenta evidência de que foi assinado pelos integrantes "
                "da Equipe de Planejamento da Contratação. A assinatura de todos os "
                "integrantes é condição de validade do ETP e pressuposto para o "
                "prosseguimento do processo; na ausência de assinatura, o ETP não "
                "tem eficácia jurídica e o processo não pode avançar para a fase "
                "de seleção do fornecedor."
            ),
            fundamentacao=(
                "Art. 18, caput, da Lei nº 14.133/2021; art. 18 do Decreto Estadual "
                "(PI) nº 21.872/2023; art. 16 da Resolução CNMP nº 283/2024 "
                "('o ETP será assinado pelos integrantes da Equipe de Planejamento')."
            ),
            acao=(
                "Assinar o ETP eletronicamente no SEI, com a assinatura de todos os "
                "integrantes designados para a Equipe de Planejamento da Contratação "
                "(Integrante Requisitante, Técnico e Administrativo). A aprovação pela "
                "autoridade competente deve ocorrer na sequência."
            ),
            sugestao=(
                "[Assinar o documento ETP no SEI. Para contratações de TIC, verificar "
                "se todos os integrantes da Equipe de Planejamento (art. 9º da Res. "
                "CNMP 283/2024) assinaram antes do encaminhamento à área de licitações.]"
            ),
        )


def checar_sigilo(etp: ETP, achados: list) -> None:
    """Verificar se o ETP avaliou a necessidade de sigilo."""
    texto = etp.texto_completo
    tem_sigilo = bool(re.search(
        r"sigilo|classificado|restri[çc][aã]o\s+de\s+acesso|reservado"
        r"|orçamento\s+sigiloso|pre[çc]o\s+sigiloso",
        texto, re.IGNORECASE
    ))
    if not tem_sigilo:
        _add(achados,
            titulo="ETP sem Avaliação sobre Necessidade de Classificação Sigilosa",
            tipo="Sugestão de Melhoria",
            localizacao="Elemento XIII do ETP ou seção específica de sigilo",
            inconsistencia=(
                "O ETP não registra avaliação sobre a necessidade de classificar o "
                "documento ou parte de seu conteúdo como sigiloso (em especial a "
                "estimativa de preços). A lei permite que a estimativa de valor "
                "conste de anexo classificado, a critério da Administração, para "
                "preservar a competitividade do certame. Não avaliar esse ponto pode "
                "representar exposição indevida de informação estratégica."
            ),
            fundamentacao=(
                "Art. 18, § 1º, inciso VI, da Lei nº 14.133/2021 (estimativa de valor "
                "'que poderão constar de anexo classificado, se a Administração optar "
                "por preservar o seu sigilo até a conclusão da licitação'); art. 27 do "
                "Decreto PI nº 21.872/2023; art. 13 da IN SEGES/ME nº 58/2022."
            ),
            acao=(
                "Inserir ao final do ETP (preferencialmente no Elemento XIII ou em "
                "seção específica) a avaliação sobre sigilo: se a estimativa de preços "
                "será pública ou classificada, e a justificativa para a decisão adotada."
            ),
            sugestao=(
                "[Ex: 'A Equipe de Planejamento avaliou a necessidade de sigilo do ETP "
                "e concluiu que [o orçamento detalhado será classificado / o ETP será "
                "integralmente público], em razão de [justificativa: preservar "
                "competitividade do certame / natureza pública da estimativa].']"
            ),
        )


def checar_quesitos_json(etp: ETP, achados: list) -> None:
    """Verifica quesitos declarativos definidos em quesitos_ETP.json."""
    import json
    caminho_json = BASE_DIR / "quesitos_ETP.json"
    if not caminho_json.exists():
        return
    try:
        with open(caminho_json, encoding="utf-8") as f:
            dados = json.load(f)
    except Exception:
        return
    texto = etp.texto_completo
    is_tic = etp.is_tic
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

def salvar_achados_json(etp: ETP, achados: list, caminho_origem: str) -> str:
    """Salva os achados em JSON para consolidação posterior no Ofício final."""
    import json
    base = Path(caminho_origem).stem
    pasta = Path(caminho_origem).parent
    caminho_json = str(pasta / f"achados_ETP_{base}.json")

    dados = {
        "artefato": "ETP",
        "num_processo": etp.num_processo or "",
        "objeto": etp.objeto_descricao or "",
        "unidade": etp.unidade_requisitante or "",
        "is_tic": etp.is_tic,
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


def gerar_oficio_word(etp: ETP, achados: list, caminho_saida: str):
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

    unidade  = etp.unidade_requisitante or "[Unidade Requisitante]"
    processo = etp.num_processo         or "[nº do processo SEI]"
    tipo_tag = " — Solução de TIC" if etp.is_tic else ""

    # ── Destinatário ─────────────────────────────────────────────────
    p = doc.add_paragraph()
    p.add_run(f"À {unidade}").bold = True
    p = doc.add_paragraph()
    p.add_run(
        f"Assunto: Devolução de Autos para Saneamento — "
        f"Análise do Estudo Técnico Preliminar{tipo_tag} — "
        f"Processo SEI nº {processo}."
    ).bold = True

    doc.add_paragraph()
    doc.add_paragraph().add_run("Senhor(a) Coordenador(a),")
    doc.add_paragraph()

    # ── Abertura ─────────────────────────────────────────────────────
    abertura = [
        (
            "Cumprimentando-o cordialmente, registro que a equipe desta Assessoria "
            "analisou o Estudo Técnico Preliminar (ETP) juntado aos autos do processo "
            "em referência, verificando a conformidade do documento com os normativos "
            "aplicáveis: Lei nº 14.133/2021, Decreto Estadual (PI) nº 21.872/2023, "
            "IN SEGES/ME nº 58/2022, Atos PGJ/MPPI nº 1.381 e 1.382/2024"
            + (", Resolução CNMP nº 283/2024 e MOTec" if etp.is_tic else "") + "."
        ),
        (
            "Na qualidade de Agente de Contratação responsável pela análise de "
            "conformidade da fase preparatória, e em cumprimento ao disposto no "
            "art. 53 da Lei nº 14.133/2021, restituo o presente feito para "
            "saneamento das inconsistências identificadas no ETP. Os apontamentos "
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
    p.add_run("1. ARTEFATO: ESTUDO TÉCNICO PRELIMINAR (ETP)").bold = True
    doc.add_paragraph()

    if not achados:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(1)
        p.add_run("Nenhuma inconsistência identificada. ETP em conformidade com os normativos aplicáveis.").italic = True
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
        "qualidade do Termo de Referência subsequente e para a boa execução "
        "contratual, prevenindo impugnações, questionamentos dos órgãos de controle "
        "e eventuais nulidades processuais."
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

def imprimir_relatorio(etp: ETP, achados: list):
    sep = "─" * 68
    print(f"\n{'═' * 68}")
    print(f"  ANÁLISE DE CONFORMIDADE — ETP  (v{VERSION})")
    print(f"{'═' * 68}")
    print(f"  Processo: {etp.num_processo or '(não identificado)'}")
    print(f"  Unidade : {etp.unidade_requisitante or '(não identificada)'}")
    print(f"  Objeto  : {(etp.objeto_descricao or '(não identificado)')[:70]}...")
    print(f"  TIC     : {'Sim (CNMP 283/MOTec aplicável)' if etp.is_tic else 'Não'}")
    print(f"  PCA     : {'Referenciado' if etp.tem_referencia_pca else 'NÃO ENCONTRADO'}")
    print(f"  Data    : {DATA_ANALISE}")
    print(sep)

    # Elementos presentes/ausentes
    obrigatorios = {
        "I": etp.elem_I_texto, "V": etp.elem_V_texto,
        "VI": etp.elem_VI_texto, "VII": etp.elem_VII_texto,
        "XIII": etp.elem_XIII_texto,
    }
    todos = {
        "I": etp.elem_I_texto, "II": etp.elem_II_texto, "III": etp.elem_III_texto,
        "IV": etp.elem_IV_texto, "V": etp.elem_V_texto, "VI": etp.elem_VI_texto,
        "VII": etp.elem_VII_texto, "VIII": etp.elem_VIII_texto, "IX": etp.elem_IX_texto,
        "X": etp.elem_X_texto, "XI": etp.elem_XI_texto, "XII": etp.elem_XII_texto,
        "XIII": etp.elem_XIII_texto,
    }
    print("  ELEMENTOS:")
    for elem, texto in todos.items():
        presente = bool(texto and len(texto.strip()) >= 40)
        obrig = " ★" if elem in obrigatorios else "  "
        status = "✓" if presente else "✗"
        print(f"    [{status}] Elemento {elem:>4}{obrig}")

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

    etp = parse_etp(texto)
    achados: list = []

    # Executa verificações em ordem
    checar_elementos_obrigatorios(etp, achados)
    checar_elemento_I(etp, achados)
    checar_elemento_II(etp, achados)
    checar_elemento_III(etp, achados)
    checar_elemento_V(etp, achados)
    checar_elemento_VI(etp, achados)
    checar_elemento_VII(etp, achados)
    checar_elemento_IX(etp, achados)
    checar_elemento_XI(etp, achados)
    checar_elemento_XIII(etp, achados)
    checar_assinaturas(etp, achados)
    checar_sigilo(etp, achados)
    checar_quesitos_json(etp, achados)

    print(f"      {len(achados)} achado(s) identificado(s)")
    imprimir_relatorio(etp, achados)

    # Salvar achados em JSON para consolidação posterior no Ofício final
    salvar_achados_json(etp, achados, caminho)

    # Gerar Ofício Word apenas se solicitado explicitamente (flag --oficio)
    if "--oficio" in sys.argv:
        base = Path(caminho).stem
        saida = str(Path(caminho).parent / f"Oficio_ASSCOMPRAS_ETP_{base}.docx")
        gerar_oficio_word(etp, achados, saida)
    else:
        print("ℹ  Para gerar o Ofício Word desta análise isolada, use: --oficio")
        print("ℹ  Para consolidar todos os artefatos do processo, use: gerar_oficio_processo.py\n")


if __name__ == "__main__":
    main()
