#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════╗
║  Analisador de DFD — ASSCOMPRAS / MPPI                  v1.0        ║
║  Coordenadoria de Licitações e Contratos                             ║
╚══════════════════════════════════════════════════════════════════════╝

Analisa o Documento de Formalização da Demanda (DFD) exportado do
SEI (PDF ou HTML) e gera automaticamente:

  1. Ofício ASSCOMPRAS com achados de conformidade (.docx)
  2. Relatório resumido no terminal

Requisitos (instale uma única vez):
    pip install pdfplumber beautifulsoup4 lxml python-docx

Uso:
    python analisar_dfd.py "caminho\\para\\dfd.pdf"
    python analisar_dfd.py "caminho\\para\\dfd.html"

Exemplos:
    python analisar_dfd.py "DFD - Contratação de Software.pdf"
    python analisar_dfd.py "SEI_1234567_DFD.html"

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
    """Representa um achado de conformidade no DFD."""
    numero: int
    titulo: str
    tipo: str = "Vício Formal"
    localizacao: str = ""
    inconsistencia: str = ""
    fundamentacao: str = ""
    acao: str = ""
    sugestao: str = ""


@dataclass
class DFD:
    """Campos extraídos do DFD."""
    # Identificação geral
    num_processo: str = ""
    texto_completo: str = ""

    # Seção 2 — Unidade Requisitante
    unidade_requisitante: str = ""
    responsavel: str = ""
    matricula_responsavel: str = ""   # novo
    email_responsavel: str = ""

    # Seção 3 — Informações Gerais
    unidade_orcamentaria: str = ""
    tipo_objeto: str = ""
    objeto_descricao: str = ""
    providencias_previas: str = ""    # "sim" | "nao" | ""
    detalhe_providencias: str = ""    # novo — texto do "SE SIM, QUAL?"
    grau_prioridade: str = ""
    data_inicio: str = ""
    data_termino: str = ""

    # Seção 4 — Equipe de Planejamento
    equipe: list = field(default_factory=list)
    # [{"nome": str, "funcao": str, "email": str}]
    equipe_tem_email: bool = False     # novo — há e-mail na tabela de equipe?

    # Seção 5 — Fiscalização
    fiscais: list = field(default_factory=list)
    # [{"matricula": str, "tem_email": bool, "perfis": list}]
    fiscal_tem_matricula_real: bool = False  # novo — matrícula ≥ 5 dígitos (não ramal)

    # Seção 6 — Identificação da Demanda
    catmat_catser: str = ""
    quantidade: str = ""
    valor_estimado: str = ""
    num_arp: str = ""
    via_licitacao: str = ""  # "licitacao", "arp", ou ""
    tem_memoria_calculo: bool = False  # novo — texto indica origem do quantitativo

    # Seção 7 — Unidade Beneficiária
    unidade_beneficiaria: str = ""

    # Seção 8 — Alinhamento Estratégico
    objetivos_pca: str = ""
    codigo_pca: str = ""
    alinhamento_pdtic: str = ""
    tem_pei: bool = False              # novo — menciona PEI ou Plano Estratégico

    # Seção 9 — Fundamentação
    necessidade: str = ""
    motivacao: str = ""

    # Seção 10 — Resultados
    objetivo_resultado: str = ""
    meta: str = ""
    indicador: str = ""

    # Seção 11/12 — Assinaturas
    responsavel_preenchimento: str = ""
    ordenador_despesas: str = ""
    tem_assinatura_titular: bool = False  # novo — seção de assinatura preenchida


# ─────────────────────────────────────────────────────────────────────
#  EXTRAÇÃO DE TEXTO
# ─────────────────────────────────────────────────────────────────────

def _caminho_seguro(caminho: str) -> str:
    """
    Copia o arquivo para C:\\Temp com nome simples, contornando
    limitações do Windows com caminhos longos ou com acentos.
    Retorna o caminho temporário criado.
    """
    import shutil, tempfile
    temp_dir = "C:\\Temp"
    os.makedirs(temp_dir, exist_ok=True)
    ext = Path(caminho).suffix.lower()
    dest = os.path.join(temp_dir, f"dfd_temp{ext}")
    shutil.copy2(caminho, dest)
    return dest


def extrair_texto_pdf(caminho: str) -> str:
    """Extrai texto de PDF usando pdfplumber."""
    try:
        import pdfplumber
    except ImportError:
        _erro("pdfplumber não instalado. Execute: pip install pdfplumber")

    # Copia para caminho seguro (sem acentos, sem espaços problemáticos)
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
    """Extrai texto de HTML (exportação do SEI)."""
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        _erro("beautifulsoup4 não instalado. Execute: pip install beautifulsoup4 lxml")

    caminho = _caminho_seguro(caminho)

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
#  PARSING DO DFD
# ─────────────────────────────────────────────────────────────────────

def _secao(texto: str, ini: int, fim: int = None) -> str:
    """Extrai o texto entre a seção 'ini' e a seção 'fim'."""
    # Padrões de início de seção numerada
    pat_ini = rf"(?:^|\n)\s*{ini}[\s\.\-–]"
    pat_fim = rf"(?:^|\n)\s*{fim}[\s\.\-–]" if fim else None

    m = re.search(pat_ini, texto, re.IGNORECASE | re.MULTILINE)
    if not m:
        return ""
    start = m.start()

    if pat_fim:
        m2 = re.search(pat_fim, texto[start + 5:], re.IGNORECASE | re.MULTILINE)
        end = (start + 5 + m2.start()) if m2 else len(texto)
    else:
        end = len(texto)

    return texto[start:end].strip()


def _primeiro_email(texto: str) -> str:
    m = re.search(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", texto)
    return m.group(0) if m else ""


def _primeiro_valor(texto: str) -> str:
    m = re.search(r"R\$\s*[\d.,]+", texto)
    return m.group(0) if m else ""


def _datas(texto: str) -> list:
    return re.findall(r"\b\d{2}/\d{2}/\d{4}\b", texto)


def parse_dfd(texto: str) -> DFD:
    dfd = DFD()
    dfd.texto_completo = texto

    # Número do processo SEI
    m = re.search(r"\b(\d{2}\.\d{2}\.\d{4}\.\d{7}/\d{4}-\d{2})\b", texto)
    if m:
        dfd.num_processo = m.group(1)

    # ─── Seção 2: Unidade Requisitante ───────────────────────────────
    s2 = _secao(texto, 2, 3)
    if s2:
        # Nome da unidade
        for pat in [r"(?:Unidade Requisitante|Nome da Unidade)[:\s]+([^\n]{5,80})",
                    r"(?:Unidade)[:\s]+([A-ZÁÉÍÓÚ][^\n]{4,60})"]:
            m = re.search(pat, s2, re.IGNORECASE)
            if m:
                dfd.unidade_requisitante = m.group(1).strip()
                break

        # Responsável
        for pat in [r"(?:Responsável|Nome do Responsável)[:\s]+([^\n]{5,80})",
                    r"Resp[.\s]*:[:\s]+([A-ZÁÉÍÓÚ][^\n]{4,60})"]:
            m = re.search(pat, s2, re.IGNORECASE)
            if m:
                dfd.responsavel = m.group(1).strip()
                break

        dfd.email_responsavel = _primeiro_email(s2)

        # Matrícula do responsável (pelo menos 5 dígitos)
        m = re.search(r"matr[íi]cula[:\s#nº°.]*(\d{5,8})", s2, re.IGNORECASE)
        if m:
            dfd.matricula_responsavel = m.group(1)

    # ─── Seção 3: Informações Gerais ─────────────────────────────────
    s3 = _secao(texto, 3, 4)
    if s3:
        # Unidade orçamentária — procura checkbox marcado antes do nome da UO
        # O SEI usa formatos como: "( X ) PGJ", "(X ) PGJ", "( X) PGJ"
        _cb = r"\(\s*[Xx]\s*\)"  # padrão de checkbox marcado
        for uo in ["PGJ", "FMMPI", "FPROCON"]:
            if re.search(_cb + r"[^\n]*" + uo, s3) or re.search(uo + r"[^\n]*" + _cb, s3):
                dfd.unidade_orcamentaria = uo
                break
        if not dfd.unidade_orcamentaria:
            for uo in ["PGJ", "FMMPI", "FPROCON"]:
                if uo in s3:
                    dfd.unidade_orcamentaria = uo
                    break

        # Tipo de objeto — detectar o checkbox marcado antes de cada opção
        tipos_obj = [
            (r"SERVI[Ç]OS N[ÃA]O CONTINUADOS", "Serviços Não Continuados"),
            (r"SERVI[Ç]OS CONTINUADOS SEM DEDICA[ÇC][ÃA]O", "Serviços Continuados sem Dedicação de MO"),
            (r"SERVI[Ç]OS CONTINUADOS COM DEDICA[ÇC][ÃA]O", "Serviços Continuados com Dedicação de MO"),
            (r"FORNECIMENTO CONTINUADO", "Fornecimento Continuado"),
            (r"FORNECIMENTO N[ÃA]O CONTINUADO", "Fornecimento Não Continuado"),
            (r"OBRAS E SERVI[ÇC]OS DE ENGENHARIA", "Obras e Serviços de Engenharia"),
            (r"AQUISI[ÇC][ÃA]O DE SOLU[ÇC][ÃA]O DE TECNOLOGIA", "TIC"),
        ]
        for pat, descr in tipos_obj:
            # Aceita checkbox antes ou depois do label
            if re.search(_cb + r"[^\n]{0,5}" + pat, s3, re.IGNORECASE) or \
               re.search(pat + r"[^\n]{0,5}" + _cb, s3, re.IGNORECASE):
                dfd.tipo_objeto = descr
                break

        # Grau de prioridade — checkbox marcado
        if re.search(_cb + r"[^\n]{0,5}ALTO|ALTO[^\n]{0,5}" + _cb, s3, re.IGNORECASE):
            dfd.grau_prioridade = "Alto"
        elif re.search(_cb + r"[^\n]{0,5}M[EÉ]DIO|M[EÉ]DIO[^\n]{0,5}" + _cb, s3, re.IGNORECASE):
            dfd.grau_prioridade = "Médio"
        elif re.search(_cb + r"[^\n]{0,5}BAIXO|BAIXO[^\n]{0,5}" + _cb, s3, re.IGNORECASE):
            dfd.grau_prioridade = "Baixo"
        else:
            # Fallback: texto livre
            m = re.search(r"(?:grau|prioridade)[:\s]*(alto|m[eé]dio|baixo)", s3, re.IGNORECASE)
            if m:
                dfd.grau_prioridade = m.group(1).capitalize()

        # Providências prévias
        if re.search(r"\(\s*[Xx]\s*\)[^\n]*SIM|SIM[^\n]*\(\s*[Xx]\s*\)", s3, re.IGNORECASE):
            dfd.providencias_previas = "sim"
            # Detalhe: linha após "SE SIM, QUAL?"
            m_det = re.search(r"SE SIM[,\s]+QUAL\??[:\s]*\n([^\n]{5,})", s3, re.IGNORECASE)
            if m_det:
                dfd.detalhe_providencias = m_det.group(1).strip()
        elif re.search(r"\(\s*[Xx]\s*\)[^\n]*N[ÃA]O|N[ÃA]O[^\n]*\(\s*[Xx]\s*\)", s3, re.IGNORECASE):
            dfd.providencias_previas = "nao"

        # Datas
        datas = _datas(s3)
        if datas:
            dfd.data_inicio = datas[0]
            if len(datas) > 1:
                dfd.data_termino = datas[-1]

        # Objeto (usar bloco maior de texto)
        m = re.search(r"(?:objeto|descri[çc][ãa]o do objeto)[:\s]+(.{20,500}?)(?:\n[A-Z]|\Z)",
                      s3, re.IGNORECASE | re.DOTALL)
        if m:
            dfd.objeto_descricao = m.group(1).strip()[:400]

    # ─── Seção 4: Equipe de Planejamento ─────────────────────────────
    s4 = _secao(texto, 4, 5)
    if s4:
        # No HTML do SEI, nomes e funções ficam em linhas separadas (células de tabela).
        # Estratégia: coletar nomes (linhas com padrão SOBRENOME NOME em maiúsculas),
        # depois verificar quais funções aparecem marcadas (checkbox) na seção.

        # Funções com checkbox marcado
        funcoes_marcadas = []
        if re.search(r"\(\s*[Xx]\s*\)[^\n]*[Cc]oordenador", s4):
            funcoes_marcadas.append("Coordenador da Equipe")
        if re.search(r"\(\s*[Xx]\s*\)[^\n]*[Rr]equisitante|[Rr]equisitante[^\n]*\(\s*[Xx]\s*\)", s4):
            funcoes_marcadas.append("Integrante Requisitante")
        if re.search(r"\(\s*[Xx]\s*\)[^\n]*[Tt][eé]cnico|[Tt][eé]cnico[^\n]*\(\s*[Xx]\s*\)", s4):
            funcoes_marcadas.append("Integrante Técnico")
        if re.search(r"\(\s*[Xx]\s*\)[^\n]*[Aa]dministrativo|[Aa]dministrativo[^\n]*\(\s*[Xx]\s*\)", s4):
            funcoes_marcadas.append("Integrante Administrativo")

        # Guardar as funções marcadas no campo equipe para uso nas verificações
        # (simplificado: registrar só as funções detectadas)
        dfd.equipe = [{"nome": "", "funcao": f, "email": ""} for f in funcoes_marcadas]

        # Emails da equipe
        emails_s4 = re.findall(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", s4)
        for i, e in enumerate(emails_s4):
            if i < len(dfd.equipe):
                dfd.equipe[i]["email"] = e
        dfd.equipe_tem_email = len(emails_s4) > 0

    # ─── Seção 5: Fiscalização ────────────────────────────────────────
    s5 = _secao(texto, 5, 6)
    if s5:
        # Extração de matrículas — o HTML do SEI exporta tabelas em linhas separadas,
        # por isso não há "matrícula: NNN" na mesma linha.
        # Estratégia: coletar todos os números isolados na seção e filtrar ramais.
        # Formatos aceitos: "173" (3 dígitos), "20269" (5 dígitos), "20.269" (com ponto).
        # Ramais típicos do MPPI: 4 dígitos começando com 8 (ex: 8025, 8039).
        numeros_s5 = re.findall(r"\b(\d{2,3}\.\d{3}|\d{2,8})\b", s5)
        matriculas = []
        for n in numeros_s5:
            digitos = n.replace(".", "")
            # Excluir ramais (4 dígitos começando com 8)
            if len(digitos) == 4 and digitos.startswith("8"):
                continue
            # Excluir anos (4 dígitos ≥ 2020)
            if len(digitos) == 4 and int(digitos) >= 2020:
                continue
            # Manter qualquer outro número de 2–8 dígitos
            matriculas.append(n)

        tem_email_fiscal = bool(_primeiro_email(s5))

        # Detectar perfis marcados — usa padrão simples sem acento para evitar
        # incompatibilidade entre maiúsculas acentuadas (TÉCNICO) e regex [eé]
        _cb5 = r"\(\s*[Xx]\s*\)"
        perfis = []
        for trecho in re.findall(_cb5 + r"[^\n]*", s5):
            t = trecho.upper()
            if "CNICO" in t:          # TÉCNICO / TECNICO
                perfis.append("Técnico")
            elif "MINISTRATIVO" in t:  # ADMINISTRATIVO
                perfis.append("Administrativo")
            elif "SETORIAL" in t:
                perfis.append("Setorial")

        # Considera matrícula real se encontrou ao menos um número válido
        matricula_real = matriculas[0] if matriculas else ""
        dfd.fiscal_tem_matricula_real = bool(matricula_real)
        dfd.fiscais = [{
            "matricula": matricula_real,
            "tem_email": tem_email_fiscal,
            "perfis": perfis,
        }]

    # ─── Seção 6: Identificação da Demanda ───────────────────────────
    s6 = _secao(texto, 6, 7)
    if s6:
        # Via de contratação
        if re.search(r"\bARP\b|Ata de Registro", s6, re.IGNORECASE):
            dfd.via_licitacao = "arp"
            m = re.search(r"(?:ARP|Ata)[:\s]*n[oº]?\s*([\d\./\-]+)", s6, re.IGNORECASE)
            if m:
                dfd.num_arp = m.group(1).strip()
        else:
            dfd.via_licitacao = "licitacao"

        # CATMAT / CATSER — o SEI coloca o código na mesma linha ou na linha seguinte
        # ao cabeçalho "CATMAT/CATSER". Procura sequência de 5-8 dígitos após o cabeçalho.
        m = re.search(r"(?:CATMAT|CATSER)[/\s]*(?:CATMAT|CATSER)?[:\s\n]*(\d{5,8})", s6, re.IGNORECASE)
        if m:
            dfd.catmat_catser = m.group(1)
        else:
            # Fallback: tabela de itens — padrão: ordem(01) + descrição + código + qtd + valor
            # Ex: "01\nDescrição\n18651\n06\nR$ 16.140,00"
            m = re.search(r"\b0*[1-9]\b[^\n]*\n[^\n]+\n(\d{5,8})\n(\d[\d.,]*)\n(R\$[^\n]+)", s6)
            if m:
                dfd.catmat_catser = m.group(1)
                dfd.quantidade = m.group(2)
                dfd.valor_estimado = m.group(3).strip()

        # Quantidade (se não extraída acima)
        if not dfd.quantidade:
            m = re.search(r"(?:quantidade|qtd?)[:\s]*([\d.,]+)", s6, re.IGNORECASE)
            if m:
                dfd.quantidade = m.group(1).strip()

        # Valor estimado (se não extraído acima)
        if not dfd.valor_estimado:
            dfd.valor_estimado = _primeiro_valor(s6)

        # Memória de cálculo / justificativa do quantitativo
        dfd.tem_memoria_calculo = bool(re.search(
            r"hist[oó]rico|consumo|demanda.{0,20}anterior|exerc[ií]cio.{0,20}anterior|"
            r"m[eé]dia.{0,20}anual|levantamento|m[eé]moria de c[áa]lculo|série hist[oó]rica|"
            r"per capita|consumo m[eé]dio",
            s6, re.IGNORECASE
        ))

    # ─── Seção 7: Unidade Beneficiária ───────────────────────────────
    s7 = _secao(texto, 7, 8)
    dfd.unidade_beneficiaria = s7.strip()

    # ─── Seção 8: Alinhamento Estratégico ────────────────────────────
    s8 = _secao(texto, 8, 9)
    if s8:
        dfd.objetivos_pca = s8[:500]
        # Código PCA (ex: CCS-03, A185, C001, IT-12)
        m = re.search(r"\b([A-Z]{1,5}-?\d{2,4}|[A-Z]\d{3,4})\b", s8)
        if m:
            dfd.codigo_pca = m.group(1)
        dfd.alinhamento_pdtic = "pdti" if re.search(r"\bPDTI\b", s8) else ""
        # PEI — Plano Estratégico Institucional
        dfd.tem_pei = bool(re.search(
            r"\bPEI\b|Plano Estrat[eé]gico Institucional|Objetivo Estrat[eé]gico",
            s8, re.IGNORECASE
        ))

    # ─── Seção 9: Fundamentação ───────────────────────────────────────
    s9 = _secao(texto, 9, 10)
    if s9:
        m91 = re.search(r"9[\.\s]*1[.\s]+(.+?)(?=9[\.\s]*2|$)", s9, re.IGNORECASE | re.DOTALL)
        if m91:
            dfd.necessidade = m91.group(1).strip()[:600]
        m92 = re.search(r"9[\.\s]*2[.\s]+(.+?)$", s9, re.IGNORECASE | re.DOTALL)
        if m92:
            dfd.motivacao = m92.group(1).strip()[:600]
        # Fallback: se não achou 9.1/9.2 explícitos, usa tudo
        if not dfd.necessidade and len(s9) > 50:
            dfd.necessidade = s9[:600]

    # ─── Seção 10: Resultados ─────────────────────────────────────────
    s10 = _secao(texto, 10, 11)
    if s10:
        dfd.objetivo_resultado = s10[:600]

        # O DFD do SEI usa perguntas numeradas como cabeçalhos de subitem:
        #   "1 Qual o objetivo..." / "2 Qual a meta..." / "3 Qual o indicador..."
        # Tentativa 1: padrão de perguntas numeradas (formato SEI)
        _pat_obj = (
            r"(?:1[\s.\-–]*)?[Qq]ual\s+o\s+objetivo[\s\S]*?"
            r"(?=(?:2[\s.\-–]*)?[Qq]ual\s+a\s+meta|$)"
        )
        _pat_meta = (
            r"(?:2[\s.\-–]*)?[Qq]ual\s+a\s+meta[\s\S]*?"
            r"(?=(?:3[\s.\-–]*)?[Qq]ual\s+o\s+indicador|$)"
        )
        _pat_ind = (
            r"(?:3[\s.\-–]*)?[Qq]ual\s+o\s+indicador[\s\S]*$"
        )

        m_obj  = re.search(_pat_obj,  s10)
        m_meta = re.search(_pat_meta, s10)
        m_ind  = re.search(_pat_ind,  s10)

        # Tentativa 2: fallback — palavras-chave simples (caso o formato seja diferente)
        if not m_obj:
            m_obj = re.search(r"[Oo]bjetivo[\s\S]*?(?=[Mm]eta|[Ii]ndicador|$)", s10)
        if not m_meta:
            m_meta = re.search(r"[Mm]eta[\s\S]*?(?=[Ii]ndicador|$)", s10)
        if not m_ind:
            m_ind = re.search(r"[Ii]ndicador[\s\S]*$", s10)

        if m_obj:
            dfd.objetivo_resultado = m_obj.group(0).strip()[:400]
        if m_meta:
            # Remove o próprio cabeçalho de pergunta, mantendo só o valor
            meta_raw = m_meta.group(0).strip()
            meta_val = re.sub(
                r"^(?:\d[\s.\-–]*)?[Qq]ual\s+a\s+meta[^?\n]*\??\s*",
                "", meta_raw
            ).strip()
            dfd.meta = meta_val[:300]
        if m_ind:
            ind_raw = m_ind.group(0).strip()
            ind_val = re.sub(
                r"^(?:\d[\s.\-–]*)?[Qq]ual\s+o\s+indicador[^?\n]*\??\s*",
                "", ind_raw
            ).strip()
            dfd.indicador = ind_val[:300]

    return dfd


# ─────────────────────────────────────────────────────────────────────
#  CHECKLIST DE CONFORMIDADE
# ─────────────────────────────────────────────────────────────────────

def _add(achados: list, **kwargs) -> None:
    kwargs["numero"] = len(achados) + 1
    achados.append(Achado(**kwargs))


def checar_secao2(dfd: DFD, achados: list) -> None:
    """Seção 2 — Identificação da Unidade Requisitante."""

    # 2a. Responsável ausente
    if not dfd.responsavel or len(dfd.responsavel) < 5:
        _add(achados,
            titulo="Omissão na Identificação do Responsável pela Demanda",
            tipo="Vício Formal",
            localizacao="Item 2 (Identificação da Unidade Requisitante) — campo Responsável pela Demanda",
            inconsistencia=(
                "O campo 'Responsável pela demanda' não foi preenchido ou está incompleto. "
                "O responsável formal deve ser o chefe da unidade ou seu substituto legal "
                "formalmente designado, não podendo ser um servidor sem atribuição de chefia, "
                "salvo expressa delegação."
            ),
            fundamentacao=(
                "Art. 12, inciso VII, da Lei nº 14.133/2021; art. 9º do Decreto Estadual "
                "(PI) nº 21.872/2023; Ato PGJ/PI nº 1.381/2024."
            ),
            acao=(
                "Preencher o campo com o nome completo do responsável formal pela unidade. "
                "Caso seja substituto, mencionar expressamente a portaria de substituição."
            ),
            sugestao="[Nome completo do chefe da unidade ou substituto legal — ex: Fulano de Tal, Portaria nº XX/XXXX]",
        )

    # 2b. E-mail ausente
    if not dfd.email_responsavel:
        _add(achados,
            titulo="Ausência de E-mail do Responsável pela Demanda",
            tipo="Vício Formal",
            localizacao="Item 2 (Identificação da Unidade Requisitante) — campo E-mail",
            inconsistencia=(
                "O campo de e-mail institucional do responsável não foi preenchido, "
                "impossibilitando contato formal sobre o processo e o rastreio de "
                "comunicações nos sistemas de controle."
            ),
            fundamentacao=(
                "Art. 5º (Princípios da Transparência e Eficiência) e art. 12, inciso VII, "
                "da Lei nº 14.133/2021."
            ),
            acao="Incluir o endereço de e-mail institucional (@mppi.mp.br) do responsável pela demanda.",
            sugestao="[nome.sobrenome]@mppi.mp.br",
        )

    # 2c. Matrícula do responsável ausente
    if not dfd.matricula_responsavel:
        _add(achados,
            titulo="Ausência de Matrícula do Responsável pela Demanda",
            tipo="Vício Formal",
            localizacao="Item 2 (Identificação da Unidade Requisitante) — campo Responsável",
            inconsistencia=(
                "O número de matrícula funcional do responsável pela demanda não "
                "consta no DFD. A matrícula é essencial para a rastreabilidade "
                "do agente público subscritor do ato e para a geração de portarias "
                "de designação nos sistemas de controle (TCE-PI, PNCP)."
            ),
            fundamentacao=(
                "Art. 7º e art. 11, § 1º, da Lei nº 14.133/2021 (princípios da "
                "segregação de funções, transparência e responsabilização); art. 20 "
                "do Decreto Estadual (PI) nº 21.872/2023 (identificação formal do "
                "agente público subscritor)."
            ),
            acao=(
                "Incluir no campo do Responsável a matrícula funcional completa, "
                "no formato: [Nome Completo] — Matrícula nº [XXXXX]."
            ),
            sugestao="[Nome do Responsável] — Matrícula nº [XXXXX]",
        )


def checar_secao3(dfd: DFD, achados: list) -> None:
    """Seção 3 — Informações Gerais."""
    texto = dfd.texto_completo
    s3 = _secao(texto, 3, 4)

    # 3a. Texto genérico do modelo não removido
    tem_modelo = bool(re.search(
        r"licitação própria.{0,30}ou.{0,30}contratação direta|"
        r"\[indicar o tipo de objeto\]|"
        r"a ser processada por meio de|"
        r"\[descreva aqui\]|"
        r"inserir (?:objeto|descrição)",
        s3, re.IGNORECASE
    ))
    if tem_modelo:
        _add(achados,
            titulo="Refinamento na Descrição do Objeto (Remoção de Trechos Genéricos do Modelo)",
            tipo="Sugestão de Melhoria",
            localizacao="Item 3 (Informações Gerais da Contratação) — campo Objeto Detalhado",
            inconsistencia=(
                "A descrição do objeto conserva trechos genéricos do modelo padrão — "
                "como a expressão 'a ser processada por meio de licitação própria (ou "
                "contratação direta)' — que não foram substituídos pela via de contratação "
                "efetivamente adotada. Tal omissão compromete a clareza e a unicidade do "
                "documento."
            ),
            fundamentacao=(
                "Princípios do Planejamento, da Transparência e da Clareza, previstos no "
                "art. 5º da Lei nº 14.133/2021, c/c art. 12, inciso VII, da mesma Lei."
            ),
            acao=(
                "Expurgar as expressões genéricas do modelo e indicar expressamente a via "
                "de contratação a ser adotada (Contratação Direta — Dispensa, Pregão "
                "Eletrônico, Carona em ARP, etc.)."
            ),
            sugestao=(
                "[Descrever o objeto de forma específica e clara, com a via de contratação "
                "definida — ex: 'Contratação direta, por dispensa de licitação nos termos "
                "do art. 75, II, da Lei nº 14.133/2021, para fornecimento de...']"
            ),
        )

    # 3b. Providências prévias marcadas SIM mas sem detalhamento
    if dfd.providencias_previas == "sim" and not dfd.detalhe_providencias:
        _add(achados,
            titulo="Providências Prévias Indicadas como Necessárias sem Identificação do Objeto Correlato",
            tipo="Vício Formal",
            localizacao="Item 3 (Informações Gerais) — campo Providências Prévias / SE SIM, QUAL?",
            inconsistencia=(
                "O campo 'Há necessidade de contratação correlata (providências prévias)?' "
                "foi marcado como SIM, mas o campo subsequente 'SE SIM, QUAL?' não foi "
                "preenchido. A omissão impede a instrução das contratações correlatas e "
                "pode acarretar paralisação do objeto principal por falta de infraestrutura "
                "de suporte."
            ),
            fundamentacao=(
                "Art. 18, § 1º, incisos IV e XI, da Lei nº 14.133/2021 (mapeamento de "
                "interdependências e providências prévias de adaptação); art. 20 do "
                "Decreto Estadual (PI) nº 21.872/2023."
            ),
            acao=(
                "Preencher o campo 'SE SIM, QUAL?' com a identificação clara da "
                "contratação correlata ou providência prévia necessária, incluindo, "
                "se aplicável, o número do processo SEI correspondente."
            ),
            sugestao=(
                "[Descrever a contratação correlata necessária — ex: 'Adequação da "
                "rede elétrica (Processo SEI nº XX.XX.XXXX.XXXXXXX/XXXX-XX)' ou "
                "'Instalação de infraestrutura de cabeamento estruturado']"
            ),
        )

    # 3d. Grau de prioridade PCA ausente
    if not dfd.grau_prioridade:
        _add(achados,
            titulo="Omissão do Grau de Prioridade no PCA",
            tipo="Vício Formal",
            localizacao="Item 3 (Informações Gerais da Contratação) — campo Grau de Prioridade PCA",
            inconsistencia=(
                "O campo de Grau de Prioridade no Plano de Contratações Anual (PCA) "
                "não foi preenchido. Esse dado é essencial para demonstrar o alinhamento "
                "da demanda com o planejamento institucional e subsidiar decisões "
                "gerenciais sobre a ordem de tramitação dos processos."
            ),
            fundamentacao=(
                "Art. 12, inciso VII, da Lei nº 14.133/2021 c/c art. 7º, § 1º, do "
                "Decreto Estadual (PI) nº 21.872/2023."
            ),
            acao=(
                "Preencher o campo com o grau de prioridade correspondente ao item no "
                "PCA aprovado: Alto, Médio ou Baixo."
            ),
            sugestao="Alto / Médio / Baixo [conforme classificação definida no PCA aprovado para o exercício]",
        )

    # 3e. Unidade orçamentária ausente
    if not dfd.unidade_orcamentaria:
        _add(achados,
            titulo="Ausência da Unidade Gestora/Orçamentária Responsável pelo Custeio",
            tipo="Vício Formal",
            localizacao="Item 3 (Informações Gerais da Contratação) — campo Unidade Orçamentária / Fonte de Recursos",
            inconsistencia=(
                "Não foi identificada nos autos a indicação da unidade gestora (UG) "
                "responsável pelo custeio da contratação — PGJ (UG 250101), FMMPI "
                "(UG 250102) ou FPROCON (UG 250103). A identificação da fonte de "
                "recursos é obrigatória para a verificação da adequação orçamentária "
                "e financeira, para a reserva de dotação e para a emissão do empenho."
            ),
            fundamentacao=(
                "Art. 72, inciso IV, da Lei nº 14.133/2021 (indicação dos recursos "
                "orçamentários como elemento obrigatório da instrução do processo); "
                "art. 18, § 1º, inciso IX, da mesma Lei; art. 20 do Decreto Estadual "
                "(PI) nº 21.872/2023; Decreto Estadual (PI) nº 21.938/2023, art. 13."
            ),
            acao=(
                "Identificar e preencher no DFD a unidade gestora responsável pelo "
                "custeio: PGJ (UG 250101), FMMPI (UG 250102) ou FPROCON (UG 250103), "
                "conforme a dotação orçamentária aprovada para o exercício."
            ),
            sugestao=(
                "[Unidade Gestora: PGJ — Procuradoria Geral de Justiça (UG 250101)] "
                "ou [FMMPI — Fundo de Modernização do MPPI (UG 250102)] "
                "ou [FPROCON (UG 250103)]"
            ),
        )

    # 3c. Data de início no passado
    if dfd.data_inicio:
        try:
            data_ini = datetime.strptime(dfd.data_inicio, "%d/%m/%Y")
            hoje = datetime.now()
            if data_ini < hoje:
                _add(achados,
                    titulo="Adequação do Cronograma de Execução — Data de Início Retroativa",
                    tipo="Sugestão de Melhoria",
                    localizacao=(
                        "Item 3 (Informações Gerais da Contratação) "
                        "— campo Previsão de Início da Execução"
                    ),
                    inconsistencia=(
                        f"A data prevista para início da execução ({dfd.data_inicio}) "
                        "já se encontra no passado ou é incompatível com o tempo "
                        "mínimo necessário para concluir o rito processual (análise "
                        "orçamentária, publicação do aviso de contratação direta por "
                        "3 dias úteis, assinatura do instrumento e execução da despesa)."
                    ),
                    fundamentacao=(
                        "Princípios do Planejamento, da Eficiência e da Razoabilidade, "
                        "preconizados no art. 5º da Lei Federal nº 14.133/2021, c/c "
                        "a diretriz de governança do art. 11, parágrafo único."
                    ),
                    acao=(
                        "Retificar a data prevista para o início da execução, "
                        "dilatando o prazo para um cenário compatível com o trâmite "
                        "interno. Ajustar, por consequência, a data de término para "
                        "manter o prazo de vigência inicialmente planejado."
                    ),
                    sugestao=(
                        f"[Projetar data de início compatível com o trâmite processual "
                        f"restante — recomenda-se ao menos 30 a 60 dias a partir de "
                        f"{hoje.strftime('%d/%m/%Y')}]"
                    ),
                )
        except ValueError:
            pass


def checar_secao4(dfd: DFD, achados: list) -> None:
    """Seção 4 — Equipe de Planejamento."""
    s4 = _secao(dfd.texto_completo, 4, 5)

    funcoes_lower = [m.get("funcao", "").lower() for m in dfd.equipe]
    tem_requisitante = any("requisitante" in f for f in funcoes_lower)
    tem_tecnico = any("técnico" in f or "tecnico" in f for f in funcoes_lower)
    tem_administrativo = any("administrativo" in f for f in funcoes_lower)

    # 4a. Composição incompleta
    if dfd.equipe and not (tem_requisitante and tem_tecnico and tem_administrativo):
        papeis_faltantes = []
        if not tem_requisitante:
            papeis_faltantes.append("Integrante Requisitante")
        if not tem_tecnico:
            papeis_faltantes.append("Integrante Técnico")
        if not tem_administrativo:
            papeis_faltantes.append("Integrante Administrativo")

        _add(achados,
            titulo="Composição Incompleta da Equipe de Planejamento da Contratação",
            tipo="Vício Formal",
            localizacao="Item 4 (Equipe de Planejamento da Contratação)",
            inconsistencia=(
                f"A equipe de planejamento não apresenta todos os perfis obrigatórios. "
                f"Ausência identificada: {', '.join(papeis_faltantes)}. "
                "A governança das contratações exige, no mínimo, a presença de "
                "Integrante Requisitante, Integrante Técnico e Integrante Administrativo, "
                "com a devida segregação de funções entre os membros."
            ),
            fundamentacao=(
                "Art. 7º, § 1º, da Lei nº 14.133/2021; art. 9º, incisos I a III, do "
                "Decreto Estadual (PI) nº 21.872/2023; Ato PGJ/PI nº 1.381/2024."
            ),
            acao=(
                "Complementar a equipe com todos os perfis exigidos, garantindo que os "
                "membros designados constem formalmente na Portaria de Planejamento da "
                "unidade vigente."
            ),
            sugestao=(
                "[Integrante Requisitante — nome completo] | "
                "[Integrante Técnico — nome completo] | "
                "[Integrante Administrativo — nome completo]"
            ),
        )

    # 4b. Segregação de funções — mesmo servidor em papéis incompatíveis
    nomes_funcoes: dict[str, list] = {}
    for m in dfd.equipe:
        nome = m.get("nome", "").strip().lower()
        funcao = m.get("funcao", "").lower()
        if nome and funcao:
            nomes_funcoes.setdefault(nome, []).append(funcao)

    for nome, funcoes in nomes_funcoes.items():
        req = any("requisitante" in f for f in funcoes)
        adm = any("administrativo" in f for f in funcoes)
        tec = any("técnico" in f or "tecnico" in f for f in funcoes)
        if req and tec and not adm:
            # Requisitante + Técnico no mesmo servidor — padrão identificado no Ofício 142
            _add(achados,
                titulo="Violação da Segregação de Funções — Integrante Requisitante e Técnico Acumulados pelo Mesmo Servidor",
                tipo="Vício Formal",
                localizacao="Item 4 (Equipe de Planejamento da Contratação)",
                inconsistencia=(
                    "O mesmo servidor acumula simultaneamente as funções de Integrante "
                    "Requisitante e Integrante Técnico na equipe de planejamento. Essa "
                    "acumulação viola o princípio da segregação de funções: o Requisitante "
                    "expressa a necessidade da unidade, enquanto o Técnico deve avaliá-la "
                    "com independência. Quando um único agente exerce os dois papéis, "
                    "suprime-se o controle cruzado que a norma visa assegurar."
                ),
                fundamentacao=(
                    "Art. 7º, § 1º, da Lei nº 14.133/2021 c/c art. 9º, incisos I e II, "
                    "do Decreto Estadual (PI) nº 21.872/2023; Resolução CNMP nº 283/2024, "
                    "art. 10 (vedação de acúmulo de papéis incompatíveis na fase de "
                    "planejamento da contratação)."
                ),
                acao=(
                    "Designar servidores distintos para as funções de Integrante Requisitante "
                    "e Integrante Técnico. O Requisitante deve ser o servidor da área com a "
                    "necessidade; o Técnico deve ser servidor com capacidade de avaliar "
                    "independentemente os aspectos técnicos da contratação."
                ),
                sugestao=(
                    "[Integrante Requisitante — Nome Completo, servidor da área demandante] | "
                    "[Integrante Técnico — Nome Completo, servidor distinto com competência "
                    "técnica para avaliação independente]"
                ),
            )
            break
        elif (req and adm) or (req and tec and adm):
            _add(achados,
                titulo="Violação da Segregação de Funções — Acúmulo de Papéis Incompatíveis",
                tipo="Vício Formal",
                localizacao="Item 4 (Equipe de Planejamento da Contratação)",
                inconsistencia=(
                    "Um mesmo servidor foi designado simultaneamente para funções "
                    "incompatíveis na equipe de planejamento. A acumulação viola "
                    "a segregação de funções prevista na lei e fragiliza a "
                    "integridade da análise técnica e administrativa do processo."
                ),
                fundamentacao=(
                    "Art. 7º, § 1º, da Lei nº 14.133/2021; Portaria PGJ/PI nº 4.335/2024 "
                    "(para contratações de TIC) c/c Resolução CNMP nº 283/2024."
                ),
                acao=(
                    "Redistribuir as funções entre servidores distintos, garantindo a "
                    "segregação entre Integrante Requisitante, Técnico e Administrativo."
                ),
                sugestao="[Designar servidores diferentes para cada função na equipe de planejamento]",
            )
            break  # apenas um achado por esse tipo

    # 4c. E-mail dos integrantes ausente na tabela da equipe
    if dfd.equipe and not dfd.equipe_tem_email:
        _add(achados,
            titulo="Ausência de E-mail Institucional dos Integrantes da Equipe de Planejamento",
            tipo="Vício Formal",
            localizacao="Item 4 (Equipe de Planejamento da Contratação) — coluna E-mail",
            inconsistencia=(
                "A tabela da Equipe de Planejamento não contém o endereço de e-mail "
                "institucional dos integrantes. O e-mail é dado obrigatório de "
                "identificação dos agentes e serve como canal de comunicação formal "
                "e rastreabilidade durante toda a fase de planejamento."
            ),
            fundamentacao=(
                "Art. 7º da Lei nº 14.133/2021; art. 20 do Decreto Estadual (PI) "
                "nº 21.872/2023 (identificação completa de cada integrante: nome, "
                "matrícula, e-mail e telefone); Resolução CNMP nº 283/2024."
            ),
            acao=(
                "Preencher a coluna E-mail da tabela para cada integrante da equipe, "
                "utilizando exclusivamente o endereço institucional @mppi.mp.br."
            ),
            sugestao=(
                "[Inserir e-mail institucional de cada integrante — "
                "ex: nome.sobrenome@mppi.mp.br]"
            ),
        )

    # 4d. Equipe não identificada (seção em branco)
    if not dfd.equipe and s4 and len(s4) < 80:
        _add(achados,
            titulo="Ausência de Identificação da Equipe de Planejamento",
            tipo="Vício Formal",
            localizacao="Item 4 (Equipe de Planejamento da Contratação)",
            inconsistencia=(
                "O quadro da equipe de planejamento está em branco ou sem identificação "
                "nominal dos membros e suas respectivas funções. A designação formal e "
                "expressa de cada integrante é condição de validade do processo."
            ),
            fundamentacao=(
                "Art. 7º, § 1º, da Lei nº 14.133/2021; art. 9º do Decreto Estadual "
                "(PI) nº 21.872/2023; Ato PGJ/PI nº 1.381/2024."
            ),
            acao=(
                "Preencher o quadro com o nome completo, e-mail institucional e função "
                "de cada membro, verificando que todos constem na Portaria de designação "
                "vigente da unidade."
            ),
            sugestao=(
                "Nome: [Nome Completo] | E-mail: nome@mppi.mp.br | "
                "Função: [Coordenador / Integrante Requisitante / Integrante Técnico / "
                "Integrante Administrativo] | Ramal: [XXXX]"
            ),
        )


def checar_secao5(dfd: DFD, achados: list) -> None:
    """Seção 5 — Fiscalização do Objeto."""
    s5 = _secao(dfd.texto_completo, 5, 6)
    if not s5 or len(s5) < 30:
        return

    # Usa fiscal_tem_matricula_real (≥5 dígitos) para evitar falso positivo com ramal (4 dígitos)
    tem_matricula = dfd.fiscal_tem_matricula_real
    tem_perfil = bool(re.search(r"t[eé]cnico|administrativo|setorial", s5, re.IGNORECASE))
    tem_email = bool(_primeiro_email(s5))

    # 5a. Matrícula ausente (real, ≥5 dígitos — não confundir com ramal)
    if not tem_matricula:
        _add(achados,
            titulo="Ausência de Matrícula na Identificação da Equipe de Fiscalização",
            tipo="Vício Formal",
            localizacao="Item 5 (Fiscalização do Objeto da Contratação) — campo Matrícula",
            inconsistencia=(
                "O quadro de indicação da fiscalização omitiu o número de matrícula "
                "funcional dos servidores indicados. A matrícula é essencial para a "
                "correta identificação nos sistemas de controle interno e externo "
                "(TCE-PI e PNCP), evitando homonímias e agilizando a futura emissão "
                "da Portaria de designação dos fiscais."
            ),
            fundamentacao=(
                "Art. 5º (Princípios da Transparência e Impessoalidade) e art. 7º, "
                "inciso I, da Lei nº 14.133/2021."
            ),
            acao=(
                "Retificar o quadro do Item 5 para incluir o número de matrícula "
                "funcional respectivo junto ao nome de cada fiscal indicado."
            ),
            sugestao=(
                "[Nome do Fiscal] — Matrícula nº [XXXXX] — "
                "[Perfil: Técnico / Administrativo / Setorial] — "
                "[e-mail]@mppi.mp.br"
            ),
        )

    # 5b. Perfil do fiscal ausente
    if not tem_perfil:
        _add(achados,
            titulo="Ausência do Perfil da Fiscalização",
            tipo="Vício Formal",
            localizacao="Item 5 (Fiscalização do Objeto da Contratação) — campo Perfil",
            inconsistencia=(
                "O perfil da fiscalização (Técnico, Administrativo ou Setorial) não foi "
                "especificado. A definição do perfil orienta a Portaria de designação e "
                "determina as atribuições específicas de cada fiscal no monitoramento "
                "da execução contratual."
            ),
            fundamentacao=(
                "Art. 117 da Lei nº 14.133/2021 c/c art. 9º do Decreto Estadual "
                "(PI) nº 21.872/2023."
            ),
            acao=(
                "Indicar expressamente o perfil de cada fiscal: Técnico (acompanha "
                "aspectos técnicos), Administrativo (controla aspectos burocráticos "
                "e financeiros) ou Setorial (vinculado à unidade beneficiária)."
            ),
            sugestao="Perfil: [Técnico / Administrativo / Setorial]",
        )


def checar_secao6(dfd: DFD, achados: list) -> None:
    """Seção 6 — Identificação da Demanda."""
    s6 = _secao(dfd.texto_completo, 6, 7)

    # 6a. CATMAT/CATSER ausente (apenas para licitação/CD, não para ARP pura)
    if dfd.via_licitacao != "arp" and not dfd.catmat_catser:
        _add(achados,
            titulo="Ausência do Código CATMAT/CATSER",
            tipo="Vício Formal",
            localizacao="Item 6.1 (Identificação da Demanda — Licitação/Contratação Direta) — campo Código",
            inconsistencia=(
                "O código CATMAT (para bens e materiais) ou CATSER (para serviços) "
                "não foi informado. Esse código é obrigatório para catalogação no "
                "Portal Nacional de Contratações Públicas (PNCP) e para a correta "
                "classificação do objeto nos sistemas de planejamento e controle "
                "das compras governamentais."
            ),
            fundamentacao=(
                "Art. 7º, § 3º, da Lei nº 14.133/2021; art. 26, § 1º, do Decreto "
                "Estadual (PI) nº 21.872/2023."
            ),
            acao=(
                "Pesquisar e inserir o código CATMAT ou CATSER correspondente ao "
                "objeto na plataforma compras.gov.br (Pesquisa de Materiais/Serviços)."
            ),
            sugestao=(
                "[Inserir código CATMAT ou CATSER — consultar em "
                "compras.gov.br > Consultas > Materiais e Serviços]"
            ),
        )

    # 6b. Valor estimado ausente
    if not dfd.valor_estimado:
        _add(achados,
            titulo="Ausência do Valor Total Estimado da Contratação",
            tipo="Vício Formal",
            localizacao="Item 6.1 (Identificação da Demanda) — campo Valor Total Estimado",
            inconsistencia=(
                "O campo 'Valor Total Estimado' não foi preenchido. "
                "Essa informação é indispensável para verificar o enquadramento "
                "legal (limites de dispensa), autorizar a adequação orçamentária "
                "e dimensionar o impacto financeiro da contratação."
            ),
            fundamentacao=(
                "Art. 18, § 1º, inciso IV, da Lei nº 14.133/2021; art. 26, "
                "inciso II, do Decreto Estadual (PI) nº 21.872/2023."
            ),
            acao=(
                "Preencher o campo com o valor total estimado, obtido a partir da "
                "pesquisa de preços formalizada nos autos."
            ),
            sugestao="R$ [Inserir valor com base na pesquisa de preços — dois decimais]",
        )

    # 6c. Quantidade ausente
    if not dfd.quantidade:
        _add(achados,
            titulo="Ausência da Quantidade Demandada",
            tipo="Vício Formal",
            localizacao="Item 6.1 (Identificação da Demanda) — campo Quantidade",
            inconsistencia=(
                "A quantidade demandada não foi especificada. Esse dado é essencial "
                "para a pesquisa de preços, para o dimensionamento orçamentário e "
                "para a definição do objeto do contrato."
            ),
            fundamentacao=(
                "Art. 18, § 1º, inciso III, da Lei nº 14.133/2021; art. 26, inciso I, "
                "do Decreto Estadual (PI) nº 21.872/2023."
            ),
            acao=(
                "Preencher o campo com a quantidade total demandada, especificando "
                "a unidade de medida (unidade, mês, lote, licença, etc.)."
            ),
            sugestao="[Inserir quantidade e unidade de medida — ex: 12 meses / 1 lote / 50 unidades]",
        )

    # 6d. Quantitativo sem memória de cálculo / justificativa de origem
    if dfd.quantidade and not dfd.tem_memoria_calculo:
        _add(achados,
            titulo="Quantitativo sem Memória de Cálculo ou Justificativa de Origem",
            tipo="Sugestão de Melhoria",
            localizacao="Item 6 (Identificação da Demanda) — campo Quantidade",
            inconsistencia=(
                "O quantitativo demandado foi informado, porém o DFD não apresenta "
                "a memória de cálculo ou a justificativa que fundamenta esse número "
                "(e.g., histórico de consumo, série histórica, levantamento por unidade "
                "beneficiária ou per capita). A ausência desse dado fragiliza a "
                "contratação frente a questionamentos dos órgãos de controle sobre "
                "superdimensionamento ou subdimensionamento."
            ),
            fundamentacao=(
                "Art. 18, § 1º, inciso IV, da Lei nº 14.133/2021 (estimativas de "
                "quantidades acompanhadas das memórias de cálculo que as embasam); "
                "art. 20, inciso III, do Decreto Estadual (PI) nº 21.872/2023; "
                "PEI 2022-2029, Ação 19 (alinhar aquisições ao histórico logístico)."
            ),
            acao=(
                "Acrescentar, no campo Quantidade ou em nota de rodapé, a memória "
                "de cálculo que justifique o quantitativo, utilizando pelo menos uma "
                "das seguintes bases: (a) histórico de consumo dos últimos 12 meses; "
                "(b) número de usuários/servidores beneficiados; (c) previsão do PCA."
            ),
            sugestao=(
                "[Justificativa — ex: 'Quantidade definida com base no histórico de "
                "consumo do exercício anterior (X unidades em 12 meses) e na "
                "previsão de crescimento de Y%. Média mensal: Z unidades.']"
            ),
        )


def checar_secao7(dfd: DFD, achados: list) -> None:
    """Seção 7 — Unidade Beneficiária."""
    s7 = dfd.unidade_beneficiaria

    # Verificar se é genérico: apenas números ou muito curto
    tem_texto = bool(re.search(r"[a-zA-ZÀ-ü]{5,}", s7))
    somente_numero = bool(re.match(r"^\s*[\d\s]+\s*$", s7[:80])) if s7 else True

    if not tem_texto or somente_numero or len(s7.strip()) < 30:
        _add(achados,
            titulo="Detalhamento Insuficiente das Unidades Beneficiárias",
            tipo="Erro Material",
            localizacao="Item 7 (Identificação da Unidade Beneficiária)",
            inconsistencia=(
                "O quadro foi preenchido de forma excessivamente sintética — "
                "constando apenas numerais, traços ou campos em branco. "
                "O preenchimento adequado é fundamental para demonstrar ao "
                "ordenador de despesas e aos órgãos de controle o impacto "
                "financeiro da demanda e a destinação dos recursos."
            ),
            fundamentacao=(
                "Art. 5º (Princípios do Planejamento e Transparência) e art. 12, "
                "inciso VII, da Lei nº 14.133/2021; art. 20 do Decreto Estadual "
                "(PI) nº 21.872/2023."
            ),
            acao=(
                "Retificar o quadro do Item 7 para incluir: nome da unidade "
                "beneficiária, objeto recebido, quantidade e valor estimado."
            ),
            sugestao=(
                f"Unidade Beneficiária: [{dfd.unidade_requisitante or 'Nome da Unidade'}] | "
                f"Objeto: [Descrição do objeto] | Quantidade: [Lote Único] | "
                f"Valor Estimado: [{dfd.valor_estimado or 'R$ X.XXX,XX'}]"
            ),
        )


def checar_secao8(dfd: DFD, achados: list) -> None:
    """Seção 8 — Alinhamento Estratégico."""
    s8 = dfd.objetivos_pca

    # 8a. Referência a PDTI em vez de PDTIC
    if dfd.alinhamento_pdtic == "pdti":
        _add(achados,
            titulo="Referência a PDTI Inexistente no Alinhamento Estratégico",
            tipo="Erro Material",
            localizacao="Item 8 (Alinhamento Estratégico) — campo Alinhamento PDTIC",
            inconsistencia=(
                "O documento referencia um Plano Diretor de Tecnologia da Informação "
                "(PDTI) no alinhamento estratégico. O MPPI não dispõe de PDTI vigente "
                "e formalizado; o instrumento correto para contratações de TIC é o "
                "PDTIC (Plano Diretor de Tecnologia da Informação e Comunicação) "
                "e/ou o Plano de Contratações Anual (PCA) do exercício."
            ),
            fundamentacao=(
                "Art. 18, § 1º, inciso II, da Lei nº 14.133/2021; Tópico 2.1.6 do "
                "Manual de Orientações Técnicas (MOTec/CNMP); Resolução CNMP nº 283/2024."
            ),
            acao=(
                "Retificar o campo, substituindo 'PDTI' pela sigla correta 'PDTIC' e/ou "
                "'PCA [ano]', conforme o instrumento efetivamente vigente no MPPI."
            ),
            sugestao=(
                "[Substituir referência ao PDTI pela referência ao PCA e ao PDTIC "
                "efetivamente vigente — verificar com a área de TIC do MPPI qual "
                "é o instrumento atual]"
            ),
        )

    # 8b. Código PCA ausente
    if not dfd.codigo_pca:
        _add(achados,
            titulo="Ausência do Código/Item do PCA no Alinhamento Estratégico",
            tipo="Vício Formal",
            localizacao="Item 8 (Alinhamento Estratégico) — campo Itens PCA",
            inconsistencia=(
                "O código identificador do item correspondente no Plano de "
                "Contratações Anual (PCA) não foi informado. A rastreabilidade ao "
                "PCA aprovado é obrigatória e demonstra que a demanda nasceu de "
                "forma planejada, organizada e devidamente prevista pelo gestor."
            ),
            fundamentacao=(
                "Art. 18, § 1º, inciso II, da Lei nº 14.133/2021; art. 17, inciso I, "
                "do Decreto Estadual (PI) nº 21.872/2023."
            ),
            acao=(
                "Inserir o código exato do item no PCA aprovado para o exercício "
                "vigente, garantindo a correspondência com o documento de planejamento "
                "institucional."
            ),
            sugestao=(
                "[Inserir código do item PCA — ex: CCS-03, C185, IT-12 — "
                "conforme o PCA aprovado para o exercício vigente]"
            ),
        )

    # 8c. PCA não mencionado em absoluto
    if not re.search(r"\bPCA\b|Plano de Contrata[çc][õo]es Anual", dfd.texto_completo, re.IGNORECASE):
        _add(achados,
            titulo="Ausência de Referência ao Plano de Contratações Anual (PCA)",
            tipo="Vício Formal",
            localizacao="Item 3 (Informações Gerais) e/ou Item 8 (Alinhamento Estratégico)",
            inconsistencia=(
                "O documento não contém nenhuma referência expressa ao Plano de "
                "Contratações Anual (PCA) vigente, nem identifica o item "
                "correspondente à demanda. A comprovação de que a contratação estava "
                "prevista no PCA é requisito legal obrigatório desde a edição da "
                "Lei nº 14.133/2021."
            ),
            fundamentacao=(
                "Art. 18, § 1º, inciso II, c/c art. 12, inciso VII, da Lei nº "
                "14.133/2021; art. 17, inciso I, do Decreto Estadual (PI) nº 21.872/2023."
            ),
            acao=(
                "Incluir referência expressa ao PCA vigente, com o código do item "
                "correspondente, nos campos pertinentes do DFD (Item 3 e Item 8)."
            ),
            sugestao=(
                "[Identificar e inserir o código do item PCA correspondente — "
                "verificar no PCA aprovado para o exercício]"
            ),
        )

    # 8d. Alinhamento ao PEI ausente
    if not dfd.tem_pei:
        _add(achados,
            titulo="Ausência de Alinhamento Explícito ao Plano Estratégico Institucional (PEI)",
            tipo="Sugestão de Melhoria",
            localizacao="Item 8 (Alinhamento Estratégico) — campo Objetivos Estratégicos",
            inconsistencia=(
                "O DFD não indica expressamente o ID e a descrição do Objetivo "
                "Estratégico do Plano Estratégico Institucional (PEI 2022-2029) ao "
                "qual a demanda se vincula. O alinhamento ao PEI demonstra que a "
                "contratação contribui para as metas institucionais e facilita a "
                "avaliação de desempenho pela Administração Superior."
            ),
            fundamentacao=(
                "Art. 11, § 2º, da Lei nº 14.133/2021 (responsabilidade da alta "
                "administração pelo alinhamento das contratações aos macro-objetivos "
                "estratégicos); art. 6º do Decreto Estadual (PI) nº 21.872/2023 "
                "(governança e submissão aos planos estratégicos); PEI 2022-2029, "
                "Eixo Gestão Administrativa, Ação 19."
            ),
            acao=(
                "Acrescentar no Item 8, no campo de objetivos estratégicos, o ID e "
                "a descrição do Objetivo Estratégico do PEI 2022-2029 ao qual a "
                "demanda se vincula."
            ),
            sugestao=(
                "[Ex: Objetivo Estratégico 3.2 — 'Estabelecer a gestão administrativa "
                "compartilhada e padronizada com foco na motivação clara dos gastos "
                "logísticos' | PEI 2022-2029, Eixo Gestão Administrativa]"
            ),
        )


def checar_secao9(dfd: DFD, achados: list) -> None:
    """Seção 9 — Fundamentação da Contratação."""

    # 9a. Necessidade ausente ou insuficiente
    if not dfd.necessidade or len(dfd.necessidade.strip()) < 80:
        _add(achados,
            titulo="Ausência ou Insuficiência na Descrição da Necessidade (Item 9.1)",
            tipo="Vício Formal",
            localizacao="Item 9.1 (Fundamentação da Contratação — Necessidade da contratação)",
            inconsistencia=(
                "O campo destinado à descrição da necessidade da contratação está "
                "em branco ou contém texto insuficiente para demonstrar a carência "
                "administrativa que justifica o pedido. A necessidade deve ser "
                "descrita de forma objetiva, clara e fundamentada."
            ),
            fundamentacao=(
                "Art. 18, § 1º, inciso I, da Lei nº 14.133/2021; art. 20, inciso I, "
                "do Decreto Estadual (PI) nº 21.872/2023."
            ),
            acao=(
                "Preencher o campo 9.1 com a descrição clara e objetiva da "
                "necessidade administrativa, enfocando o PROBLEMA a ser resolvido, "
                "não a solução (contratação) em si."
            ),
            sugestao=(
                "[Descrever o problema ou carência que justifica a contratação — "
                "ex: 'A necessidade decorre da ausência de [bem/serviço] em quantidade "
                "e qualidade adequadas para [objetivo institucional], o que compromete "
                "[impacto negativo identificado]']"
            ),
        )
    else:
        # 9b. Necessidade descreve solução em vez de problema
        palavras_solucao = [
            "contratar", "contratação de empresa", "empresa especializada",
            "aquisição de", "adquirir", "fornecimento de", "compra de",
            "locação de", "serviço de"
        ]
        inicio = dfd.necessidade[:300].lower()
        foco_em_solucao = sum(1 for p in palavras_solucao if p in inicio) >= 2

        if foco_em_solucao:
            _add(achados,
                titulo="Aprimoramento na Descrição da Necessidade — Foco no Problema, não na Solução (Item 9.1)",
                tipo="Sugestão de Melhoria",
                localizacao="Item 9.1 (Fundamentação da Contratação — Necessidade da contratação)",
                inconsistencia=(
                    "O texto do item 9.1 descreve a solução pretendida (contratação/aquisição) "
                    "em vez do problema que gerou o pedido. Na boa governança das contratações, "
                    "o foco do item de necessidade deve recair sobre a carência administrativa, "
                    "ou seja, o problema concreto que a Administração precisa resolver, e não "
                    "sobre a resposta que ela cogita adotar."
                ),
                fundamentacao=(
                    "Art. 18, § 1º, inciso I, da Lei nº 14.133/2021 — que exige evidenciar "
                    "o problema a ser resolvido sob a perspectiva do interesse público — c/c "
                    "art. 20, inciso I, do Decreto Estadual (PI) nº 21.872/2023."
                ),
                acao=(
                    "Reescrever o campo 9.1 deslocando o foco conceitual da 'contratação' "
                    "(solução) para a 'carência concreta da unidade' (necessidade administrativa). "
                    "A solução pode ser mencionada, mas apenas como consequência lógica do problema."
                ),
                sugestao=(
                    "[Iniciar com a descrição do problema — ex: 'A unidade [X] enfrenta [problema], "
                    "o que impede/compromete [consequência para o interesse público]. "
                    "Para sanar essa carência, faz-se necessária a contratação de...']"
                ),
            )

    # 9c. Motivação/Justificativa ausente ou sem economicidade
    if dfd.motivacao and len(dfd.motivacao.strip()) > 50:
        has_economicidade = bool(re.search(
            r"economi|custo|efici[eê]ncia|menor custo|vantaj|relação custo.bene|benefício",
            dfd.motivacao, re.IGNORECASE
        ))
        if not has_economicidade:
            _add(achados,
                titulo="Aprimoramento da Justificativa com Foco na Economicidade (Item 9.2)",
                tipo="Sugestão de Melhoria",
                localizacao="Item 9.2 (Fundamentação da Contratação — Motivação e Justificativa)",
                inconsistencia=(
                    "A justificativa descreve adequadamente a utilidade da contratação, "
                    "mas não demonstra a vantagem econômica da solução escolhida em "
                    "relação a alternativas. A economicidade deve ser evidenciada para "
                    "respaldar a opção pela melhor relação custo-benefício."
                ),
                fundamentacao=(
                    "Princípios da Eficiência e da Economicidade (art. 5º da Lei nº "
                    "14.133/2021) c/c art. 18, § 1º (avaliação da melhor solução) da "
                    "mesma Lei; art. 20, inciso III, do Decreto Estadual (PI) nº 21.872/2023."
                ),
                acao=(
                    "Complementar a redação do item 9.2 com um parágrafo que evidencie "
                    "as vantagens econômicas da solução escolhida em detrimento de "
                    "alternativas disponíveis."
                ),
                sugestao=(
                    "[Adicionar parágrafo — ex: 'A opção pela [locação/serviço/aquisição] "
                    "justifica-se pela economicidade, uma vez que exime a Administração dos "
                    "custos fixos de [manutenção/armazenamento/pessoal especializado], "
                    "representando uma relação custo-benefício mais favorável ao erário...']"
                ),
            )
    elif not dfd.motivacao or len(dfd.motivacao.strip()) < 50:
        _add(achados,
            titulo="Ausência ou Insuficiência da Motivação/Justificativa (Item 9.2)",
            tipo="Vício Formal",
            localizacao="Item 9.2 (Fundamentação da Contratação — Motivação e Justificativa)",
            inconsistencia=(
                "O campo destinado à motivação e justificativa da contratação está "
                "em branco ou contém texto insuficiente. A justificativa deve "
                "demonstrar a adequação da solução ao interesse público, incluindo "
                "análise de alternativas e evidências de economicidade."
            ),
            fundamentacao=(
                "Art. 18, § 1º, incisos I a IV, da Lei nº 14.133/2021; art. 20, "
                "incisos II e III, do Decreto Estadual (PI) nº 21.872/2023."
            ),
            acao=(
                "Preencher o campo 9.2 com justificativa substantiva que inclua: "
                "(a) adequação da solução ao interesse público; "
                "(b) análise de alternativas disponíveis; "
                "(c) demonstração de economicidade."
            ),
            sugestao=(
                "[Justificar a escolha da solução, incluindo análise de alternativas "
                "e evidências de economicidade — fundamentar com dados concretos]"
            ),
        )

    # 9d. Inexigibilidade sem elementos obrigatórios de justificação
    # Quando o tipo_objeto ou motivacao indica inexigibilidade, verificar se constam
    # as expressões que amparam o art. 74 III 'f' (capacitação) ou art. 74 I/II/III
    tipo_lower = dfd.tipo_objeto.lower()
    motiv_lower = (dfd.motivacao or "").lower()
    neces_lower = (dfd.necessidade or "").lower()
    texto_s9 = (neces_lower + " " + motiv_lower)

    is_inexigibilidade = bool(re.search(
        r"inexigib|art[\.\s]*74|notória\s+especializ|inviabilidade\s+de\s+competi",
        tipo_lower + " " + texto_s9, re.IGNORECASE
    ))

    if is_inexigibilidade:
        tem_inviabilidade = bool(re.search(
            r"inviabilidade\s+de\s+competi[çc]",
            texto_s9, re.IGNORECASE
        ))
        tem_singularidade = bool(re.search(
            r"singular(idade)?|[úu]nico\s+no\s+mercado|exclusiv(idade)?",
            texto_s9, re.IGNORECASE
        ))
        tem_notoria = bool(re.search(
            r"not[oó]ria\s+especializ|reconhecido\s+pela\s+[aá]rea|renome\s+acad[eê]mico",
            texto_s9, re.IGNORECASE
        ))

        elementos_faltantes = []
        if not tem_inviabilidade:
            elementos_faltantes.append("inviabilidade de competição")
        if not tem_singularidade:
            elementos_faltantes.append("singularidade do objeto/fornecedor")
        if not tem_notoria:
            elementos_faltantes.append("notória especialização")

        if elementos_faltantes:
            _add(achados,
                titulo="Fundamentação de Inexigibilidade Incompleta — Ausência de Elementos Essenciais (Item 9)",
                tipo="Vício Formal",
                localizacao="Item 9 (Fundamentação da Contratação) — modalidade Inexigibilidade",
                inconsistencia=(
                    "O DFD indica modalidade de Inexigibilidade de Licitação, porém a "
                    "fundamentação dos itens 9.1 e 9.2 não demonstra expressamente todos "
                    "os elementos que a lei exige para afastar a competição. "
                    f"Elementos ausentes ou insuficientemente demonstrados: "
                    f"{'; '.join(elementos_faltantes)}. "
                    "Sem esses elementos, a opção pela inexigibilidade carece de lastro "
                    "jurídico e fica vulnerável à impugnação pelos órgãos de controle."
                ),
                fundamentacao=(
                    "Art. 74, caput e § 3º, da Lei nº 14.133/2021 — para a inexigibilidade "
                    "por serviços técnicos especializados de natureza predominantemente "
                    "intelectual (inc. III, 'f'), exige-se demonstração de: (i) inviabilidade "
                    "de competição; (ii) singularidade do serviço; e (iii) notória especialização "
                    "do contratado. Para capacitações (art. 74, inc. III, 'f'), exige-se "
                    "demonstrar que o credenciado/fornecedor detém exclusividade reconhecida "
                    "pelo mercado ou pelos órgãos reguladores da área."
                ),
                acao=(
                    "Complementar os itens 9.1 e 9.2 do DFD com a demonstração expressa de: "
                    "(a) inviabilidade de competição — por que não há outros fornecedores "
                    "aptos no mercado; "
                    "(b) singularidade do objeto ou do fornecedor — características únicas "
                    "que o diferenciam de outros prestadores; "
                    "(c) notória especialização — reconhecimento técnico/acadêmico do "
                    "contratado comprovado por documentação pertinente."
                ),
                sugestao=(
                    "[9.1 — Necessidade: 'A contratação é inviável por competição em razão "
                    "de [descrever singularidade do objeto ou do fornecedor]. Não foram "
                    "identificados outros prestadores no mercado com as mesmas qualificações, "
                    "comprovadas por [certificação/acreditação/publicações/premiações].'] | "
                    "[9.2 — Motivação: 'A escolha pelo fornecedor [Nome] justifica-se pela "
                    "sua notória especialização, reconhecida por [entidade/publicação], "
                    "bem como pela singularidade do [curso/serviço], que não encontra "
                    "equivalente no mercado capaz de atender à necessidade da unidade.']"
                ),
            )

    # ── 9e. Necessidade de capacitação com foco equivocado ──────────────
    # Padrão Ofício 142 Achado 04: texto de 9.1 menciona "processos de contratação"
    # em vez da lacuna operacional concreta (ex: retenções na fonte, liquidação).
    is_capacitacao = bool(re.search(
        r"capacita[çc][aã]o|treinamento|curso|workshop|qualifica[çc][aã]o"
        r"|atualiza[çc][aã]o.{0,20}t[eé]cnica|desenvolvimento.{0,20}servidor",
        (dfd.tipo_objeto + " " + (dfd.necessidade or "") + " " + (dfd.motivacao or "")).lower()
    ))

    if is_capacitacao and dfd.necessidade and len(dfd.necessidade.strip()) > 80:
        nes_lower = dfd.necessidade.lower()
        foco_em_proc_contratacao = bool(re.search(
            r"processos?\s+de\s+contrata[çc][aã]o"
            r"|atividades?\s+de\s+(?:licita[çc][aã]o|contrata[çc][aã]o)"
            r"|fases?\s+de\s+(?:licita[çc][aã]o|contrata[çc][aã]o)"
            r"|procedimentos?\s+licitat[oó]rios?",
            nes_lower
        ))
        if foco_em_proc_contratacao:
            _add(achados,
                titulo=(
                    "Foco Equivocado na Necessidade de Capacitação — "
                    "Descrição de Processo Licitatório em Vez da Lacuna Técnica Operacional (Item 9.1)"
                ),
                tipo="Erro Material",
                localizacao="Item 9.1 (Fundamentação da Contratação — Necessidade da contratação)",
                inconsistencia=(
                    "O campo 9.1 destina-se a descrever a lacuna técnica ou operacional "
                    "concreta da unidade requisitante — o problema real que a capacitação "
                    "visa sanar. Contudo, o texto atual desvia-se desse propósito ao "
                    "enquadrar a necessidade como uma questão ligada aos 'processos de "
                    "contratação', linguagem própria da instrução processual, e não da "
                    "carência técnica da unidade. A descrição deve focar nas atribuições "
                    "funcionais da equipe (ex.: liquidação de despesa, retenções na fonte, "
                    "obrigações acessórias) e na lacuna de conhecimento gerada pelas "
                    "inovações normativas, demonstrando por que a capacitação é uma "
                    "medida preventiva necessária — não apenas a descrição do curso."
                ),
                fundamentacao=(
                    "Art. 18, § 1º, inciso I, da Lei nº 14.133/2021 — a necessidade deve "
                    "ser descrita sob a perspectiva do interesse público e do problema "
                    "concreto a resolver, não da solução (o curso em si); art. 20, inciso "
                    "I, do Decreto Estadual (PI) nº 21.872/2023."
                ),
                acao=(
                    "Reescrever o campo 9.1 com foco na lacuna técnica-operacional: "
                    "(a) identificar quais atribuições da unidade são impactadas pela "
                    "mudança normativa; (b) descrever a lacuna de conhecimento resultante; "
                    "(c) apontar o risco concreto para a Administração se a capacitação "
                    "não ocorrer (ex.: risco de autuação fiscal, passivo, recolhimento "
                    "indevido ou omissão de obrigações acessórias)."
                ),
                sugestao=(
                    "[Ex: 'A necessidade decorre da urgente lacuna técnica dos servidores "
                    "da [unidade] frente às inovações trazidas pela [Lei/EC], que impõem "
                    "novas obrigações de [retenção na fonte / liquidação / escrituração]. "
                    "Sem a devida atualização, a unidade fica exposta ao risco de "
                    "[descrever consequência concreta: autuação, recolhimento indevido, "
                    "descumprimento de obrigação acessória], comprometendo a conformidade "
                    "legal e a governança institucional do MPPI.']"
                ),
            )

    # ── 9f. Erros gramaticais/formais comuns em 9.1 e 9.2 ──────────────
    # Detecta padrões recorrentes identificados no Ofício 142 (Achado 04 e 05)
    texto_s9_full = (dfd.necessidade or "") + " " + (dfd.motivacao or "")
    erros_detectados = []

    # "bem com" em vez de "bem como"
    if re.search(r"\bbem\s+com\s+(?!a\b|o\b|os\b|as\b|isso\b|ele\b|ela\b|eles\b|elas\b|que\b)",
                 texto_s9_full, re.IGNORECASE):
        erros_detectados.append("'bem com' (provavelmente 'bem como')")

    # Artigo feminino plural antes de substantivo no singular ("nas Legislação", "nas Lei")
    if re.search(r"\bnas\s+[A-ZÁÉÍÓÚÂÊÎÔÛÃÕ][a-záéíóúâêîôûãõ]*[çc][aã]o\b",
                 texto_s9_full):
        erros_detectados.append(
            "concordância 'nas [Substantivo singular]' — artigo plural com substantivo no singular"
        )

    # Ausência de pontuação em construção tipo "... Reforma Tributária O Novo ..."
    if re.search(r"[a-záéíóúâêîôûãõ]\s+[A-ZÁÉÍÓÚÂÊÎÔÛÃÕ][a-záéíóúâêîôûãõ]+\s+[A-ZÁÉÍÓÚÂÊÎÔÛÃÕ]",
                 texto_s9_full):
        # Heurística conservadora: maiúscula logo após minúscula sem pontuação intermediária
        if re.search(
            r"[a-záéíóúâêîôûãõ]\s+(?:O|A|Os|As|Um|Uma)\s+[A-ZÁÉÍÓÚÂÊÎÔÛÃÕ]",
            texto_s9_full
        ):
            erros_detectados.append(
                "possível ausência de pontuação entre frases "
                "(artigo definido após palavra em minúscula sem vírgula ou ponto)"
            )

    # "alterações ocorridos" (concordância de gênero: alterações = feminino, ocorridos = masculino)
    if re.search(r"altera[çc][oõ]es\s+ocorridos?", texto_s9_full, re.IGNORECASE):
        erros_detectados.append("'alterações ocorridos' — erro de concordância (deveria ser 'ocorridas')")

    if erros_detectados and len(texto_s9_full.strip()) > 50:
        erros_str = "; ".join(erros_detectados)
        _add(achados,
            titulo="Incorreções Gramaticais/Formais nos Campos de Fundamentação (Itens 9.1 e/ou 9.2)",
            tipo="Erro Material",
            localizacao="Item 9 (Fundamentação da Contratação) — Itens 9.1 e/ou 9.2",
            inconsistencia=(
                "Foram identificados indícios de incorreções gramaticais ou formais no "
                "texto dos campos de fundamentação, que comprometem a clareza e a "
                "formalidade exigidas em instrução processual de contratação pública. "
                f"Padrões detectados: {erros_str}. "
                "Documentos oficiais devem observar rigorosamente a norma culta da "
                "língua portuguesa, especialmente em atos que integram processos "
                "administrativos sujeitos à revisão pelos órgãos de controle."
            ),
            fundamentacao=(
                "Princípios da Clareza, da Motivação e da Formalidade dos atos "
                "administrativos (art. 5º da Lei nº 14.133/2021) c/c art. 20 do "
                "Decreto Estadual (PI) nº 21.872/2023."
            ),
            acao=(
                "Revisar integralmente o texto dos itens 9.1 e 9.2 quanto à "
                "gramática, concordância nominal e verbal, pontuação e ortografia, "
                "substituindo os trechos com vícios identificados por redação "
                "gramaticalmente escorreita e formal."
            ),
            sugestao=(
                "[Revisar: concordâncias, uso de 'bem como' (não 'bem com'), "
                "pontuação entre períodos, maiúsculas indevidas em substantivos comuns "
                "como 'Seletivo', e estruturas frasais coesas no último parágrafo.]"
            ),
        )


def checar_secao10(dfd: DFD, achados: list) -> None:
    """Seção 10 — Resultados a Serem Alcançados."""
    s10 = dfd.objetivo_resultado

    if not s10 or len(s10.strip()) < 30:
        _add(achados,
            titulo="Ausência ou Insuficiência nos Resultados Esperados (Item 10)",
            tipo="Vício Formal",
            localizacao="Item 10 (Resultados a Serem Alcançados)",
            inconsistencia=(
                "O quadro de resultados esperados está em branco ou insuficientemente "
                "preenchido. A definição clara de objetivo, meta e indicador é "
                "essencial para o monitoramento e a avaliação da contratação."
            ),
            fundamentacao=(
                "Art. 11, caput e inciso I, da Lei nº 14.133/2021; art. 22, inciso IV, "
                "do Decreto Estadual (PI) nº 21.872/2023."
            ),
            acao=(
                "Preencher o quadro com: Objetivo (resultado a alcançar), "
                "Meta (expressão quantitativa/temporal) e Indicador (forma de medir)."
            ),
            sugestao=(
                "Objetivo: [Resultado concreto em linguagem de gestão por resultados — "
                "ex: 'Assegurar a disponibilidade de [bem/serviço] para as unidades do MPPI'] | "
                "Meta: [Expressão mensurável — ex: '100% dos pedidos atendidos em até X dias'] | "
                "Indicador: [Forma de medir — ex: 'Taxa de atendimento de pedidos']"
            ),
        )
    else:
        obj_lower = s10.lower()

        # 10a. Objetivo confundido com ementa do curso (conteúdo programático)
        # Padrão do Ofício 142: objetivo lista tópicos do curso em vez da finalidade administrativa
        palavras_ementa = [
            "ibs", "cbs", "imposto seletivo", "lei complementar 214",
            "lei complementar nº 214", "reforma tributária", "tributário",
            "cenário atual", "impacto para", "imposto sobre bens",
            "contribuição sobre bens", "módulo", "unidade didática",
            "carga horária", "ementa", "conteúdo programático",
        ]
        # Detecta se o objetivo parece listar tópicos (ementa) ao invés de resultado
        qtd_ementa = sum(1 for p in palavras_ementa if p in obj_lower)
        # Heurística: 2+ termos de ementa OU presença de ":" seguida de lista temática
        parece_ementa = (qtd_ementa >= 2) or bool(re.search(
            r"(?:abordando|aborda|incluindo|temas?\s+como|módulos?:)\s+[\w\s,]+",
            obj_lower
        ))

        verbos_meio = [
            "contratar", "adquirir", "comprar", "disponibilizar",
            "fornecer", "realizar", "executar"
        ]
        verbos_resultado = [
            "assegurar", "garantir", "promover", "fortalecer", "alcançar",
            "manter", "elevar", "reduzir", "ampliar", "melhorar", "capacitar",
            "habilitar", "desenvolver", "qualificar"
        ]
        is_meio = any(v in obj_lower for v in verbos_meio)
        is_resultado = any(v in obj_lower for v in verbos_resultado)

        if parece_ementa:
            _add(achados,
                titulo="Objetivo Confundido com Ementa do Curso — Ausência de Finalidade Administrativa (Item 10.1)",
                tipo="Erro Material",
                localizacao="Item 10 (Resultados a Serem Alcançados) — campo Objetivo da Contratação",
                inconsistencia=(
                    "O campo 'Objetivo da Contratação' descreve o conteúdo programático "
                    "ou ementa do curso (tópicos, módulos, temas abordados) em vez de "
                    "declarar a finalidade administrativa que a contratação visa alcançar. "
                    "O objetivo deve responder à pergunta 'qual resultado institucional se "
                    "pretende com essa capacitação?', não 'o que o curso vai ensinar?'. "
                    "A ementa é parte do Termo de Referência, não do DFD."
                ),
                fundamentacao=(
                    "Art. 18, § 1º, inciso I, da Lei nº 14.133/2021 — o DFD deve demonstrar "
                    "o resultado a ser alcançado sob a perspectiva do interesse público, não "
                    "a solução técnica ou o conteúdo do objeto; art. 11, inciso I, da mesma "
                    "Lei; art. 22, inciso IV, do Decreto Estadual (PI) nº 21.872/2023."
                ),
                acao=(
                    "Substituir o conteúdo do campo 'Objetivo' por uma declaração de "
                    "finalidade administrativa: qual competência institucional será "
                    "desenvolvida, qual lacuna de conhecimento será suprida e como isso "
                    "contribui para os resultados do MPPI. O conteúdo programático deve "
                    "ser detalhado no Termo de Referência."
                ),
                sugestao=(
                    "[Ex: 'Capacitar os servidores da [unidade] para o correto cumprimento "
                    "das obrigações decorrentes da Reforma Tributária (LC 214/2025), "
                    "habilitando-os a [ação concreta — ex: aplicar os novos procedimentos "
                    "de apuração, prestar assessoramento técnico às unidades de origem, "
                    "adaptar os fluxos internos de controle], reduzindo o risco de "
                    "autuação e passivo fiscal para a instituição.']"
                ),
            )
        elif is_meio and not is_resultado:
            _add(achados,
                titulo="Aprimoramento do Objetivo da Contratação — Foco no Resultado, não no Meio (Item 10.1)",
                tipo="Sugestão de Melhoria",
                localizacao="Item 10 (Resultados a Serem Alcançados) — campo Objetivo da Contratação",
                inconsistencia=(
                    "A redação do objetivo foca na ação (o meio) em vez do resultado "
                    "final pretendido pela Administração. Sob a ótica da gestão por "
                    "resultados, o objetivo deve evidenciar o impacto prático da "
                    "contratação, não apenas a atividade a ser realizada."
                ),
                fundamentacao=(
                    "Art. 11, caput e inciso I, da Lei nº 14.133/2021, que estipula "
                    "como objetivo das contratações assegurar o resultado mais vantajoso "
                    "para a Administração."
                ),
                acao=(
                    "Ajustar a redação para que o objetivo evidencie o resultado final "
                    "almejado e o interesse público atendido, usando verbos de resultado."
                ),
                sugestao=(
                    "[Substituir verbos de ação por verbos de resultado — "
                    "ex: em vez de 'contratar empresa para X', usar "
                    "'Assegurar [resultado concreto] para [benefício ao interesse público]']"
                ),
            )

        # 10b. Meta sem parametrização mensurável
        meta_texto = dfd.meta or s10  # fallback para s10 se meta não foi extraída separadamente
        meta_lower = meta_texto.lower()
        tem_quantificador = bool(re.search(
            r"\b\d+\s*%|\b\d+\s*vag|\b\d+\s*servidor|\b\d+\s*participante"
            r"|\b\d+\s*pessoa|\b\d+\s*servidor|\b\d+\s*unidade"
            r"|100%|todos os|todas as|\d+\s*(?:dias?|meses?|horas?)"
            r"|até\s+\d|no\s+m[ií]nimo\s+\d|ao\s+menos\s+\d",
            meta_lower
        ))

        if dfd.meta and len(dfd.meta.strip()) > 10 and not tem_quantificador:
            _add(achados,
                titulo="Meta sem Parametrização Mensurável — Ausência de Quantificador (Item 10.2)",
                tipo="Erro Material",
                localizacao="Item 10 (Resultados a Serem Alcançados) — campo Meta",
                inconsistencia=(
                    "A meta declarada no Item 10 não apresenta parâmetro mensurável — "
                    "ausência de percentual, quantidade de beneficiários, prazo ou outro "
                    "quantificador que permita verificar objetivamente se foi atingida. "
                    "Uma meta sem quantificação não cumpre sua função de instrumento de "
                    "acompanhamento e avaliação da execução contratual."
                ),
                fundamentacao=(
                    "Art. 11, inciso I, da Lei nº 14.133/2021 (gestão por resultados e "
                    "seleção da proposta mais vantajosa); art. 22, inciso IV, do Decreto "
                    "Estadual (PI) nº 21.872/2023; Guia Prático SEGES/MGI — Documento de "
                    "Formalização da Demanda (item 'Meta': expressão quantitativa e temporal)."
                ),
                acao=(
                    "Reescrever o campo Meta incluindo: (a) quantidade de servidores/vagas "
                    "a serem capacitados ou unidades a serem atendidas; (b) percentual de "
                    "execução ou aprovação esperado; (c) prazo de realização."
                ),
                sugestao=(
                    "[Ex: 'Capacitar [N] servidores até [mês/ano], com aproveitamento "
                    "mínimo de [X]% dos participantes' — ou — 'Realizar [N] turmas com "
                    "carga horária de [X]h cada, atendendo à totalidade dos servidores "
                    "da [unidade] indicados pela chefia imediata.']"
                ),
            )

        # 10c. Indicador sem métrica documental (KPI verificável)
        ind_lower = (dfd.indicador or "").lower()
        if dfd.indicador and len(dfd.indicador.strip()) > 10:
            tem_metrica_doc = bool(re.search(
                r"certificad|taxa\s+de|n[uú]mero\s+de|percentual|relat[oó]rio"
                r"|lista\s+de\s+presença|ata\s+de|comprova[çc][aã]o|declara[çc][aã]o"
                r"|nota\s+(?:fiscal|de\s+aproveit)|avalia[çc][aã]o\s+de\s+reação"
                r"|índice\s+de|grau\s+de|quantidade\s+de",
                ind_lower
            ))
            if not tem_metrica_doc:
                _add(achados,
                    titulo="Indicador sem Métrica Documental Verificável (Item 10.3)",
                    tipo="Erro Material",
                    localizacao="Item 10 (Resultados a Serem Alcançados) — campo Indicador",
                    inconsistencia=(
                        "O indicador declarado no Item 10 não especifica uma métrica "
                        "documental verificável — não há referência a certificado de "
                        "conclusão, taxa de aproveitamento, lista de presença, relatório "
                        "de execução ou outro documento/KPI que permita ao fiscal aferir "
                        "objetivamente o cumprimento do objeto. Sem isso, o indicador "
                        "não atende à sua finalidade de instrumento de fiscalização."
                    ),
                    fundamentacao=(
                        "Art. 117 da Lei nº 14.133/2021 (fiscalização da execução "
                        "contratual); art. 11, inciso I, da mesma Lei; art. 22, inciso "
                        "IV, do Decreto Estadual (PI) nº 21.872/2023; Guia Prático "
                        "SEGES/MGI — DFD (campo 'Indicador': deve ser mensurável e "
                        "baseado em documentação gerada pela execução do contrato)."
                    ),
                    acao=(
                        "Reformular o indicador especificando o documento ou KPI que será "
                        "utilizado para mensurar o resultado: certificado de conclusão, "
                        "taxa de aprovação, lista de presença assinada, relatório de "
                        "execução do fornecedor, avaliação de reação dos participantes, etc."
                    ),
                    sugestao=(
                        "[Ex: 'Taxa de conclusão — percentual de servidores que obtiveram "
                        "certificado de conclusão em relação ao total de inscritos.' — ou — "
                        "'Número de servidores certificados: lista nominal emitida pelo "
                        "contratado ao final de cada turma, conferida com a lista de "
                        "inscrição da unidade demandante.']"
                    ),
                )


def checar_secao11(dfd: DFD, achados: list) -> None:
    """Seção 11/12 — Assinaturas e aprovação pelo titular."""
    texto = dfd.texto_completo

    # Verificar se há seção de assinatura com conteúdo (nome/matrícula/cargo)
    s11 = _secao(texto, 11, None)
    s12 = _secao(texto, 12, None) if not s11 else ""
    bloco_assin = s11 or s12 or ""

    # Procurar padrões de assinatura: nome em maiúsculas + cargo/matrícula
    tem_assinatura = bool(re.search(
        r"[A-ZÁÉÍÓÚÂÊÎÔÛÃÕÀÜ]{3,}\s+[A-ZÁÉÍÓÚÂÊÎÔÛÃÕÀÜ]{3,}|"  # nome maiúsculo
        r"assin[ao]|rubric|data[:\s]+\d{2}/\d{2}|titular|ordenador",
        bloco_assin, re.IGNORECASE
    ))

    if not tem_assinatura:
        _add(achados,
            titulo="DFD sem Evidência de Assinatura/Aprovação pelo Titular da Unidade Requisitante",
            tipo="Vício Formal",
            localizacao="Item 11 (Assinaturas) — Assinatura do Titular da Área Requisitante",
            inconsistencia=(
                "O DFD não apresenta evidência de que foi formalmente datado e "
                "assinado pelo titular da unidade requisitante antes do encaminhamento "
                "à ASSCOMPRAS. A ausência de assinatura do ordenador/titular retira "
                "a validade formal do ato e impede a abertura regular do processo "
                "administrativo no SEI."
            ),
            fundamentacao=(
                "Art. 20, caput, do Decreto Estadual (PI) nº 21.872/2023 "
                "(regularidade formal e validação hierárquica do ato); art. 7º da "
                "Lei nº 14.133/2021; Ato PGJ/PI nº 1.381/2024 (competência para "
                "abertura de processos de planejamento de contratação)."
            ),
            acao=(
                "Garantir que o DFD seja datado e assinado eletronicamente no SEI "
                "pelo titular da unidade requisitante (ou substituto formalmente "
                "designado) antes do encaminhamento à ASSCOMPRAS."
            ),
            sugestao=(
                "[Assinar o DFD eletronicamente no SEI — acesse o processo, "
                "localize o documento DFD e clique em 'Assinar Documento'. "
                "A assinatura deve constar antes do despacho de encaminhamento.]"
            ),
        )


# ─────────────────────────────────────────────────────────────────────
#  VERIFICAÇÃO DE QUESITOS ADICIONAIS (declarativos — quesitos_DFD.json)
# ─────────────────────────────────────────────────────────────────────

def checar_quesitos_json(dfd: DFD, achados: list) -> None:
    """
    Carrega quesitos_DFD.json (mesmo diretório do script) e executa checks
    de regex sobre o texto completo do DFD, gerando achados para quesitos
    não cobertos pelos checks estruturais das seções 2-11.
    """
    import json
    caminho_json = BASE_DIR / "quesitos_DFD.json"
    if not caminho_json.exists():
        return

    try:
        with open(caminho_json, encoding="utf-8") as f:
            dados = json.load(f)
    except Exception:
        return

    texto = dfd.texto_completo
    is_tic = bool(getattr(dfd, "is_tic", False) or
                  re.search(r"\bTIC\b|\bTI\b|tecnologia da informação|informática",
                            texto, re.IGNORECASE))

    for q in dados.get("quesitos", []):
        # Pular quesitos exclusivos de TIC em contratações não-TIC
        if q.get("is_tic_only") and not is_tic:
            continue

        patterns = q.get("patterns", [])
        modo = q.get("modo", "ausente")

        encontrou = any(
            re.search(p, texto, re.IGNORECASE | re.DOTALL)
            for p in patterns
        )

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

def salvar_achados_json(dfd, achados: list, caminho_origem: str) -> str:
    """Salva os achados em JSON para consolidação posterior no Ofício final."""
    import json
    base = Path(caminho_origem).stem
    pasta = Path(caminho_origem).parent
    caminho_json = str(pasta / f"achados_DFD_{base}.json")

    dados = {
        "artefato": "DFD",
        "num_processo": dfd.num_processo or "",
        "objeto": dfd.objeto_descricao or "",
        "unidade": dfd.unidade_requisitante or "",
        "is_tic": getattr(dfd, "is_tic", False),
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
#  GERAÇÃO DO OFÍCIO WORD  (formato Ofício ASSCOMPRAS padrão MPPI)
# ─────────────────────────────────────────────────────────────────────

def _set_font(doc, nome="Times New Roman", tamanho=12):
    from docx.shared import Pt
    style = doc.styles["Normal"]
    style.font.name = nome
    style.font.size = Pt(tamanho)


def gerar_oficio_word(dfd, achados, caminho_saida):
    try:
        from docx import Document
        from docx.shared import Pt, Cm
        from docx.enum.text import WD_ALIGN_PARAGRAPH
    except ImportError:
        print("ERRO: python-docx não instalado. Execute: pip install python-docx")
        import sys; sys.exit(1)

    doc = Document()
    _set_font(doc, "Times New Roman", 12)
    section = doc.sections[0]
    section.top_margin    = Cm(3)
    section.bottom_margin = Cm(2)
    section.left_margin   = Cm(3)
    section.right_margin  = Cm(2)

    unidade = dfd.unidade_requisitante or "[Unidade Requisitante]"
    processo = dfd.num_processo or "[nº do processo SEI]"

    # ── Destinatário ────────────────────────────────────────────────
    p = doc.add_paragraph()
    p.add_run(f"À {unidade}").bold = True
    p = doc.add_paragraph()
    run_sub = p.add_run(
        f"Assunto: Devolução de Autos para Saneamento — "
        f"Processo SEI nº {processo}."
    )
    run_sub.bold = True

    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run("Senhor(a) Coordenador(a),")
    doc.add_paragraph()

    # ── Parágrafos de abertura ───────────────────────────────────────
    abertura = [
        (
            "Cumprimentando-o cordialmente, registro que a equipe desta Assessoria "
            "reconhece o esforço técnico da unidade requisitante na instrução do "
            "processo, notadamente pela elaboração dos artefatos iniciais, o que "
            "demonstra compromisso com a boa governança."
        ),
        (
            "Na qualidade de Agente de Contratação responsável pela análise de "
            "conformidade da fase preparatória, e em cumprimento ao disposto no "
            "art. 53 da Lei nº 14.133/2021, restituo o presente feito para "
            "saneamento de inconsistências formais e/ou materiais identificadas "
            "nos artefatos analisados. Ressalta-se que os apontamentos formulados "
            "possuem o intuito eminentemente colaborativo de aprimorar a instrução "
            "processual, visando conferir segurança jurídica, transparência e "
            "eficiência ao procedimento."
        ),
        (
            "A seguir, apresentamos os achados estruturados por artefato, com a "
            "respectiva ação de saneamento e sugestão de texto para ajuste, quando "
            "aplicável. Cumpre destacar que as redações propostas possuem caráter "
            "meramente exemplificativo e orientativo, competindo estritamente ao "
            "setor requisitante, no exercício de suas atribuições, avaliar a "
            "pertinência, a plausibilidade e a conveniência de sua manutenção ou "
            "adoção frente à realidade técnica e fática da contratação:"
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
    run = p.add_run("1. ARTEFATO: DOCUMENTO DE FORMALIZAÇÃO DA DEMANDA (DFD)")
    run.bold = True
    doc.add_paragraph()

    if not achados:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(1)
        p.add_run("Nenhuma inconsistência identificada.").italic = True
    else:
        for achado in achados:
            # Título do achado
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(1)
            p.paragraph_format.space_before = Pt(6)
            run = p.add_run(f"{achado.numero}. Achado Nº {achado.numero:02d}: {achado.titulo}")
            run.bold = True
            if achado.tipo:
                p.add_run(f" ({achado.tipo})").italic = True

            # Sub-itens numerados
            sub_num = 1
            campos = [
                ("Localização",        achado.localizacao),
                ("A Inconsistência",   achado.inconsistencia),
                ("Fundamentação Legal", achado.fundamentacao),
                ("Ação de Saneamento", achado.acao),
            ]
            for label, conteudo in campos:
                if not conteudo:
                    continue
                p = doc.add_paragraph()
                p.paragraph_format.left_indent = Cm(2)
                p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                run_lbl = p.add_run(f"{sub_num}. {label}: ")
                run_lbl.bold = True
                p.add_run(conteudo)
                sub_num += 1

            if achado.sugestao:
                p = doc.add_paragraph()
                p.paragraph_format.left_indent = Cm(2)
                p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                run_lbl = p.add_run(f"{sub_num}. Sugestão de texto: ")
                run_lbl.bold = True
                run_sug = p.add_run(
                    "(instrução — a unidade deverá adaptar conforme a realidade fática) "
                    + achado.sugestao
                )
                run_sug.italic = True

            doc.add_paragraph()

    # ── Encerramento ─────────────────────────────────────────────────
    p = doc.add_paragraph()
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.first_line_indent = Cm(1.25)
    p.add_run(
        "Dessa forma, com as observações, devolvo os autos à origem, pugnando "
        "pelo saneamento exato e tempestivo dos achados elencados, condição "
        "sine qua non para o prosseguimento hígido do feito e remessa às "
        "instâncias superiores."
    )

    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run("Atenciosamente,")
    doc.add_paragraph()
    doc.add_paragraph()

    p = doc.add_paragraph()
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run("THIAGO NOGUEIRA DE SOUSA MARTINS ALMEIDA").bold = True
    p = doc.add_paragraph()
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run("Assessor de Compras")
    p = doc.add_paragraph()
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run("Coordenadoria de Licitações e Contratos — MPPI")
    p = doc.add_paragraph()
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run(f"Teresina (PI), {DATA_ANALISE}")

    doc.save(caminho_saida)



# ─────────────────────────────────────────────────────────────────────
#  GERAÇÃO DO DFD SANEADO (minuta corrigida)
# ─────────────────────────────────────────────────────────────────────

def gerar_dfd_saneado(dfd, achados, caminho_saida):
    """
    Gera minuta de DFD com todas as seções:
    - Campos sem achados: dados originais (ou indicação de manter original)
    - Campos com achados: correção sugerida em amarelo
    - Campos com pendência de preenchimento manual: indicação em vermelho
    """
    import re as _re
    try:
        from docx import Document
        from docx.shared import Pt, Cm, RGBColor
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        from docx.oxml.ns import qn
        from docx.oxml import OxmlElement
    except ImportError:
        print("ERRO: python-docx não instalado.")
        return

    COR_LABEL = 'D9D9D9'   # cinza - rótulos
    COR_CORR  = 'FFF9C4'   # amarelo - campo corrigido
    COR_INSER = 'FFCDD2'   # rosa - preenchimento manual obrigatório
    MANTER    = "[Manter conforme original]"

    def _set_bg(cell, hex_color):
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'), 'clear')
        shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:fill'), hex_color)
        tcPr.append(shd)

    def _add_row(table, label, value, cor=None, negrito_val=False):
        row = table.add_row()
        # Label
        _set_bg(row.cells[0], COR_LABEL)
        lp = row.cells[0].paragraphs[0]
        lp.paragraph_format.space_before = Pt(2)
        lp.paragraph_format.space_after = Pt(2)
        lr = lp.add_run(label)
        lr.bold = True; lr.font.size = Pt(10)
        # Value
        if cor:
            _set_bg(row.cells[1], cor)
        vp = row.cells[1].paragraphs[0]
        vp.paragraph_format.space_before = Pt(2)
        vp.paragraph_format.space_after = Pt(2)
        vp.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        vr = vp.add_run(str(value or MANTER))
        vr.font.size = Pt(10)
        if negrito_val:
            vr.bold = True
        return row

    def _sec_head(doc, num, titulo, tem_achado=False):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(3)
        txt = f"SEÇÃO {num} — {titulo.upper()}"
        if tem_achado:
            txt += "  [⚠ CORRIGIDA]"
        r = p.add_run(txt)
        r.bold = True; r.font.size = Pt(11)
        if tem_achado:
            r.font.color.rgb = RGBColor(0xB8, 0x46, 0x00)

    def _new_table(doc):
        t = doc.add_table(rows=0, cols=2)
        t.style = 'Table Grid'
        # fixed column widths
        from docx.shared import Cm as C
        for row in t.rows:
            row.cells[0].width = C(5)
            row.cells[1].width = C(11)
        return t

    # Mapeia seções com achados
    secs_com_achado = set()
    for a in achados:
        m = _re.search(r'Item\s+(\d+)', a.localizacao or '')
        if m:
            secs_com_achado.add(int(m.group(1)))

    def _has(n):
        return n in secs_com_achado

    # ── Documento ───────────────────────────────────────────────────
    doc = Document()
    _set_font(doc, "Times New Roman", 11)
    s = doc.sections[0]
    s.top_margin = Cm(2.5); s.bottom_margin = Cm(2)
    s.left_margin = Cm(3);  s.right_margin  = Cm(2)

    # Cabeçalho
    for txt, sz, bold, cor in [
        ("MINISTÉRIO PÚBLICO DO ESTADO DO PIAUÍ", 12, True, None),
        ("DOCUMENTO DE FORMALIZAÇÃO DA DEMANDA — DFD", 14, True, None),
        (f"MINUTA CORRIGIDA — ASSCOMPRAS/CLC  ·  {DATA_ANALISE}", 10, True, RGBColor(0xB8,0x46,0x00)),
    ]:
        p = doc.add_paragraph()
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(txt)
        r.bold = bold; r.font.size = Pt(sz)
        if cor: r.font.color.rgb = cor

    p = doc.add_paragraph()
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(10)
    r = p.add_run(
        "Legenda:  ■ Amarelo = campo corrigido/sugerido (adaptar ao caso concreto)  "
        "■ Vermelho = preenchimento manual obrigatório  "
        "■ Sem cor = manter conforme DFD original"
    )
    r.font.size = Pt(8.5); r.italic = True

    # ── Seção 1 ─────────────────────────────────────────────────────
    _sec_head(doc, 1, "Identificação do Processo")
    t = _new_table(doc)
    _add_row(t, "Número do Processo SEI", dfd.num_processo)
    obj_resumo = dfd.objeto_descricao[:200].strip() if dfd.objeto_descricao else None
    _add_row(t, "Objeto (resumo)", obj_resumo)

    # ── Seção 2 ─────────────────────────────────────────────────────
    _sec_head(doc, 2, "Identificação da Unidade Requisitante e do Responsável", _has(2))
    t = _new_table(doc)

    unid = dfd.unidade_requisitante
    if not unid or 'nome da unidade' in unid.lower():
        unid = None
    _add_row(t, "Unidade Requisitante", unid)

    resp = dfd.responsavel
    if not resp or len(resp.strip()) < 5 or resp.strip().lower() == 'pela demanda':
        resp = None
    _add_row(t, "Responsável pela Demanda", resp)

    if not dfd.matricula_responsavel:
        _add_row(t, "Matrícula do Responsável",
                 "[INSERIR: nº de matrícula funcional do responsável pela demanda]",
                 cor=COR_INSER, negrito_val=True)
    else:
        _add_row(t, "Matrícula do Responsável", dfd.matricula_responsavel)

    _add_row(t, "E-mail do Responsável", dfd.email_responsavel)

    # ── Seção 3 ─────────────────────────────────────────────────────
    _sec_head(doc, 3, "Informações Gerais da Contratação", _has(3))
    t = _new_table(doc)
    _add_row(t, "Tipo de Objeto", dfd.tipo_objeto)
    _add_row(t, "Objeto Detalhado", dfd.objeto_descricao or None)
    _add_row(t, "CATMAT / CATSER", dfd.catmat_catser)
    _add_row(t, "Via de Contratação",
             "Contratação Direta" if dfd.via_licitacao else None)

    from datetime import datetime as _dt
    data_ok = False
    if dfd.data_inicio:
        try:
            dt_ini = _dt.strptime(dfd.data_inicio, "%d/%m/%Y")
            data_ok = dt_ini >= _dt.now()
        except:
            pass
    if not data_ok and dfd.data_inicio:
        _add_row(t, "Previsão de Início da Execução",
                 f"[INSERIR: data futura compatível com o trâmite administrativo "
                 f"(data original '{dfd.data_inicio}' é retroativa)]",
                 cor=COR_INSER, negrito_val=True)
        _add_row(t, "Previsão de Término da Execução",
                 "[INSERIR: data de término compatível com a nova data de início]",
                 cor=COR_INSER, negrito_val=True)
    else:
        _add_row(t, "Previsão de Início da Execução", dfd.data_inicio)
        _add_row(t, "Previsão de Término da Execução", dfd.data_termino)

    # ── Seção 4 ─────────────────────────────────────────────────────
    _sec_head(doc, 4, "Equipe de Planejamento da Contratação", _has(4))
    t = _new_table(doc)
    funcoes = {m.get('funcao','').lower() for m in dfd.equipe}
    tem_adm = any('administrativo' in f for f in funcoes)

    for membro in dfd.equipe:
        funcao = membro.get('funcao', '') or 'Membro'
        nome   = membro.get('nome',  '') or None
        email  = membro.get('email', '') or None
        _add_row(t, f"{funcao} — Nome", nome)
        if not email:
            _add_row(t, f"{funcao} — E-mail",
                     "[INSERIR: e-mail institucional (@mppi.mp.br)]",
                     cor=COR_INSER, negrito_val=True)
        else:
            _add_row(t, f"{funcao} — E-mail", email)

    if not tem_adm:
        _add_row(t, "Integrante Administrativo — Nome",
                 "[INSERIR: nome do servidor designado para o papel administrativo]",
                 cor=COR_INSER, negrito_val=True)
        _add_row(t, "Integrante Administrativo — Matrícula / E-mail",
                 "[INSERIR: matrícula e e-mail institucional (@mppi.mp.br)]",
                 cor=COR_INSER, negrito_val=True)

    # ── Seção 5 ─────────────────────────────────────────────────────
    _sec_head(doc, 5, "Equipe de Fiscalização", _has(5))
    t = _new_table(doc)
    if dfd.fiscais:
        for i, fiscal in enumerate(dfd.fiscais, 1):
            perfis = ', '.join(fiscal.get('perfis', [])) or None
            _add_row(t, f"Fiscal {i} — Perfil(is)", perfis)
            mat = fiscal.get('matricula', '') or ''
            if not dfd.fiscal_tem_matricula_real:
                _add_row(t, f"Fiscal {i} — Matrícula",
                         "[INSERIR: nº de matrícula funcional do fiscal "
                         "(≥ 5 dígitos — não confundir com ramal telefônico)]",
                         cor=COR_INSER, negrito_val=True)
            else:
                _add_row(t, f"Fiscal {i} — Matrícula", mat)
            _add_row(t, f"Fiscal {i} — E-mail",
                     "[Manter conforme original]" if fiscal.get('tem_email') else
                     "[INSERIR: e-mail institucional do fiscal]")
    else:
        _add_row(t, "Fiscal", None)

    # ── Seção 6 ─────────────────────────────────────────────────────
    _sec_head(doc, 6, "Quantitativo Estimado da Demanda", _has(6))
    t = _new_table(doc)
    _add_row(t, "Quantidade Estimada", dfd.quantidade)
    if not dfd.tem_memoria_calculo:
        _add_row(t, "Memória de Cálculo / Metodologia",
                 ("O quantitativo de "
                  + (dfd.quantidade or "N/A")
                  + " unidades foi definido com base no número de servidores da unidade "
                  "diretamente impactados pela demanda, considerando a capacidade de "
                  "atendimento do objeto contratado e o histórico de demandas similares.\n\n"
                  "[ADAPTAR: substitua pelo critério real adotado — ex.: levantamento "
                  "de necessidades, série histórica de consumo, demanda prospectiva etc.]"),
                 cor=COR_CORR)
    else:
        _add_row(t, "Memória de Cálculo / Metodologia", MANTER)

    # ── Seção 7 ─────────────────────────────────────────────────────
    _sec_head(doc, 7, "Identificação da Unidade Beneficiária e Valor Estimado")
    t = _new_table(doc)
    _add_row(t, "Unidade Beneficiária", None)
    _add_row(t, "Valor Estimado Total", dfd.valor_estimado)

    # ── Seção 8 ─────────────────────────────────────────────────────
    _sec_head(doc, 8, "Alinhamento Estratégico", _has(8))
    t = _new_table(doc)
    _add_row(t, "Grau de Prioridade (PCA)", dfd.grau_prioridade)
    if not dfd.codigo_pca:
        _add_row(t, "Código / Item do PCA Vigente",
                 "[INSERIR: número do item do PCA vigente do MPPI "
                 "correspondente a esta contratação]",
                 cor=COR_INSER, negrito_val=True)
    else:
        _add_row(t, "Código / Item do PCA Vigente", dfd.codigo_pca)
    _add_row(t, "Objetivos Estratégicos (conforme PCA)", None)
    _add_row(t, "Alinhamento ao PDTIC", None)
    if not dfd.tem_pei:
        _add_row(t, "Alinhamento ao PEI 2022-2029",
                 ("A presente contratação está alinhada ao Plano Estratégico Institucional "
                  "do MPPI (PEI 2022-2029), especificamente ao Objetivo Estratégico de "
                  "Excelência na Gestão Institucional, na medida em que promove a "
                  "qualificação e a atualização técnica dos servidores, fortalecendo a "
                  "capacidade operacional e a conformidade da unidade às novas exigências "
                  "legais decorrentes da Reforma Tributária.\n\n"
                  "[ADAPTAR: consulte o PEI 2022-2029 e cite o objetivo estratégico e "
                  "a meta institucional correspondentes à área desta contratação.]"),
                 cor=COR_CORR)
    else:
        _add_row(t, "Alinhamento ao PEI 2022-2029", MANTER)

    # ── Seção 9 ─────────────────────────────────────────────────────
    _sec_head(doc, 9, "Fundamentação da Contratação", _has(9))
    t = _new_table(doc)

    nec = dfd.necessidade or ''
    if nec.startswith("QUAL A NECESSIDADE"):
        nec = nec.split('\n', 1)[1].strip() if '\n' in nec else nec
    _add_row(t, "9.1 Necessidade da Contratação", nec or None)

    mot = dfd.motivacao or ''
    if mot.startswith("POR QUE FAZER"):
        mot = mot.split('\n', 1)[1].strip() if '\n' in mot else mot

    if _has(9):
        mot_corr = (
            (mot + "\n\n" if mot else "") +
            "[COMPLEMENTAR — Achado 09: incluir análise de economicidade que demonstre "
            "a vantajosidade da contratação. Exemplos: comparativo de custos x "
            "benefícios esperados, referência a contratações similares em outros "
            "órgãos públicos, impacto positivo na eficiência operacional da unidade.]"
        )
        _add_row(t, "9.2 Motivação e Justificativa", mot_corr, cor=COR_CORR)
    else:
        _add_row(t, "9.2 Motivação e Justificativa", mot or None)

    # ── Seção 10 ─────────────────────────────────────────────────────
    _sec_head(doc, 10, "Resultados a Serem Alcançados")
    t = _new_table(doc)
    obj = dfd.objetivo_resultado or ''
    obj = _re.sub(r'^10\.\s*RESULTADO[^\n]*\n', '', obj, flags=_re.DOTALL, count=1).strip()
    _add_row(t, "Objetivos e Resultados Esperados", obj or None)

    # ── Seção 11 ─────────────────────────────────────────────────────
    _sec_head(doc, 11, "Providências Anteriores e Assinaturas", _has(11))
    t = _new_table(doc)

    prov = dfd.providencias_previas
    if prov == 'sim':
        _add_row(t, "Providências Prévias", "( X ) SIM")
        _add_row(t, "Detalhamento das Providências",
                 dfd.detalhe_providencias or
                 "[INSERIR: descrição das providências já adotadas]")
    elif prov == 'nao':
        _add_row(t, "Providências Prévias", "( X ) NÃO")
    else:
        _add_row(t, "Providências Prévias", None)

    _add_row(t, "Responsável pelo Preenchimento",
             dfd.responsavel_preenchimento or None)

    if not dfd.tem_assinatura_titular:
        _add_row(t, "Assinatura do Titular da Unidade Requisitante",
                 "[AÇÃO OBRIGATÓRIA: assinar o DFD eletronicamente no SEI antes do "
                 "encaminhamento à ASSCOMPRAS — acesse o processo, localize o "
                 "documento DFD e clique em 'Assinar Documento'.]",
                 cor=COR_INSER, negrito_val=True)
    else:
        _add_row(t, "Assinatura do Titular da Unidade Requisitante", MANTER)

    # Nota de rodapé
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    r = p.add_run(
        f"NOTA: Minuta gerada automaticamente pelo sistema ASSCOMPRAS "
        f"({len(achados)} achado(s) identificado(s)). "
        "Campos em AMARELO são sugestões orientativas — o setor requisitante deve "
        "avaliar e adaptar ao caso concreto antes de adotar. "
        "Campos em VERMELHO exigem preenchimento obrigatório. "
        "O DFD deve ser editado e assinado diretamente no sistema SEI."
    )
    r.italic = True; r.font.size = Pt(9)

    doc.save(caminho_saida)
# ─────────────────────────────────────────────────────────────────────
#  UTILITÁRIOS E MAIN
# ─────────────────────────────────────────────────────────────────────

def _erro(msg):
    print(f"\nERRO: {msg}\n")
    import sys; sys.exit(1)


def _banner():
    print()
    print("=" * 62)
    print(f"  Analisador de DFD - ASSCOMPRAS / MPPI  v{VERSION}")
    print("=" * 62)


def _resumo_terminal(dfd, achados):
    print("\nDADOS EXTRAÍDOS DO DFD:")
    for label, val in [
        ("Processo SEI",          dfd.num_processo),
        ("Unidade Requisitante",  dfd.unidade_requisitante),
        ("Responsável",           dfd.responsavel),
        ("Matrícula Responsável", dfd.matricula_responsavel),
        ("E-mail",                dfd.email_responsavel),
        ("Tipo de Objeto",        dfd.tipo_objeto),
        ("Grau Prioridade PCA",   dfd.grau_prioridade),
        ("Data Início",           dfd.data_inicio),
        ("CATMAT/CATSER",         dfd.catmat_catser),
        ("Valor Estimado",        dfd.valor_estimado),
        ("Quantidade",            dfd.quantidade),
        ("Código PCA",            dfd.codigo_pca),
    ]:
        status = "OK" if val else "??"
        print(f"  [{status}] {label:28s} {val or '(não identificado)'}")

    print(f"\nACHADOS: {len(achados)}")
    for a in achados:
        print(f"  {a.numero:02d}. [{a.tipo}] {a.titulo[:70]}")
    print()



def _validar_achados(achados: list) -> list:
    """
    Exibe cada achado e solicita confirmacao interativa.
    Retorna apenas os achados mantidos pelo analista.
    """
    SEP  = "-" * 62
    DSEP = "=" * 62
    mantidos   = []
    descartados = []

    print(f"\n{DSEP}")
    print(f"  VALIDACAO DE ACHADOS  --  {len(achados)} identificado(s)")
    print( "  Revise cada achado e confirme se deve constar no Oficio.")
    print( "  [S/Enter] Manter     [N] Descartar")
    print(f"{DSEP}")

    for idx, a in enumerate(achados, 1):
        print(f"\n{SEP}")
        print(f"  Achado {idx:02d}/{len(achados):02d}  [{a.tipo}]")
        print(f"  Titulo:    {a.titulo}")
        print(f"  Local:     {a.localizacao}")
        print(SEP)
        incons = a.inconsistencia.replace("\n", " ")
        if len(incons) > 280:
            incons = incons[:277] + "..."
        print(f"  Inconsistencia: {incons}")
        print()
        while True:
            resp = input("  Manter este achado? [S/n]: ").strip().lower()
            if resp in ("", "s", "sim", "y", "yes"):
                mantidos.append(a)
                print("  OK - Mantido.")
                break
            elif resp in ("n", "nao", "no"):
                descartados.append(a)
                print("  -- Descartado.")
                break
            else:
                print("  Digite S para manter ou N para descartar.")

    for i, a in enumerate(mantidos, 1):
        a.numero = i

    print(f"\n{DSEP}")
    print(f"  Resultado: {len(mantidos)} mantido(s), {len(descartados)} descartado(s).")
    print(DSEP)
    return mantidos


def main():
    _banner()
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    caminho_dfd = sys.argv[1]
    if not os.path.exists(caminho_dfd):
        _erro(f"Arquivo nao encontrado: {caminho_dfd}")

    print(f"\nArquivo: {Path(caminho_dfd).name}")
    print("\n[1/5] Extraindo texto...")
    texto = extrair_texto(caminho_dfd)
    print(f"      {len(texto):,} caracteres")

    print("\n[2/5] Analisando secoes...")
    dfd = parse_dfd(texto)

    print("\n[3/5] Aplicando checklist...")
    achados = []
    checar_secao2(dfd, achados)
    checar_secao3(dfd, achados)
    checar_secao4(dfd, achados)
    checar_secao5(dfd, achados)
    checar_secao6(dfd, achados)
    checar_secao7(dfd, achados)
    checar_secao8(dfd, achados)
    checar_secao9(dfd, achados)
    checar_secao10(dfd, achados)
    checar_secao11(dfd, achados)
    checar_quesitos_json(dfd, achados)
    print(f"      {len(achados)} achado(s) identificado(s)")

    print("\n[4/5] Validando achados...")
    achados = _validar_achados(achados)
    if not achados:
        print("\n  Nenhum achado mantido. Nenhum documento sera gerado.")
        sys.exit(0)

    print(f"\n[5/5] Salvando achados ({len(achados)} achado(s))...")
    nome_base = Path(caminho_dfd).stem
    salvar_achados_json(dfd, achados, caminho_dfd)

    _resumo_terminal(dfd, achados)

    # Gerar documentos Word apenas se solicitado explicitamente (flag --oficio)
    if "--oficio" in sys.argv:
        data_str = datetime.now().strftime("%Y%m%d_%H%M")
        caminho_saida = str(BASE_DIR / f"Oficio ASSCOMPRAS - {nome_base} - {data_str}.docx")
        gerar_oficio_word(dfd, achados, caminho_saida)
        caminho_saneado = str(BASE_DIR / f"DFD Saneado - {nome_base} - {data_str}.docx")
        gerar_dfd_saneado(dfd, achados, caminho_saneado)
        print(f"Oficio gerado:    {Path(caminho_saida).name}")
        print(f"DFD Saneado:      {Path(caminho_saneado).name}")
        print(f"Pasta: {BASE_DIR}")
    else:
        print("ℹ  Para gerar o Ofício Word desta análise isolada, use: --oficio")
        print("ℹ  Para consolidar todos os artefatos do processo, use: gerar_oficio_processo.py\n")


if __name__ == "__main__":
    main()
