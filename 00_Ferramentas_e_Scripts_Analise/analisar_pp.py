#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════╗
║  Analisador de PP — ASSCOMPRAS / MPPI                     v1.0      ║
║  Pesquisa de Preços e Mapa Comparativo de Preços                     ║
╚══════════════════════════════════════════════════════════════════════╝

Analisa a Pesquisa de Preços (PP) e o respectivo Mapa Comparativo
exportados do SEI (PDF ou HTML) e gera automaticamente:

  1. Arquivo JSON com achados de conformidade (achados_PP_*.json)
  2. Relatório resumido no terminal
  3. Ofício ASSCOMPRAS (.docx), se solicitado com --oficio

Base normativa dos quesitos:
  · Lei nº 14.133/2021 — arts. 6º, XXIII, 'i'; 18, § 1º, VI; 23; 72, II e VII
  · Decreto Estadual (PI) nº 21.872/2023 — arts. 44 a 47 e 159, II
  · IN SEGES/ME nº 65/2021 — arts. 3º a 10
  · IN SEGES/MP nº 5/2017 — Anexo VII-D (planilha de custos)
  · Decreto Federal nº 7.983/2013 — obras e serviços de engenharia
  · Roteiro de Quesitos ASSCOMPRAS/MPPI — grupo "Pesquisa de Preços" (Q119–Q147)
  · Lista de Verificação CNMP — Pesquisa de Preços

Requisitos (instale uma única vez):
    pip install pdfplumber beautifulsoup4 lxml python-docx

Uso:
    python analisar_pp.py "caminho\\para\\pesquisa_precos.pdf"
    python analisar_pp.py "caminho\\para\\pesquisa_precos.html" --oficio

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

# Nº mínimo de fontes/propostas recomendado pela IN SEGES/ME nº 65/2021
MIN_FONTES_ESPERADO = 3


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
class PP:
    texto_completo: str = ""
    num_processo: str = ""
    objeto_descricao: str = ""
    unidade_requisitante: str = ""

    # Classificação
    is_tic:              bool = False
    is_servico_mao_obra: bool = False
    is_obra_engenharia:  bool = False
    is_contratacao_direta: bool = False

    # Métricas
    num_fontes_detectadas:      int = 0
    num_cnpj_detectados:        int = 0

    # Grupo 1 — Elementos obrigatórios (art. 44 do Decreto 21.872/2023)
    tem_descricao_objeto:        bool = False   # art. 44, I
    tem_identificacao_agentes:   bool = False   # art. 44, II
    tem_caracterizacao_fontes:   bool = False   # art. 44, III
    tem_serie_precos:            bool = False   # art. 44, IV
    tem_metodo_estatistico:      bool = False   # art. 44, V
    tem_justificativa_metodologia: bool = False # art. 44, VI
    tem_memoria_calculo:         bool = False   # art. 44, VII
    tem_justificativa_fornecedores: bool = False # art. 44, VIII

    # Grupo 2 — Condições comerciais (art. 45)
    tem_condicoes_comerciais: bool = False
    tem_taxa_risco:           bool = False

    # Grupo 3 — Parâmetros de pesquisa (art. 46)
    tem_painel_precos:        bool = False   # art. 46, I
    tem_contratacoes_similares: bool = False # art. 46, II
    tem_midia_especializada:  bool = False   # art. 46, III
    tem_notas_fiscais:        bool = False   # art. 46, IV
    tem_pesquisa_direta:      bool = False   # art. 46, V
    tem_priorizacao_oficiais: bool = False
    tem_dados_completos_proposta: bool = False
    tem_prazo_validade:       bool = False
    tem_registro_nao_respondentes: bool = False

    # Grupo 4 — Tratamento estatístico (art. 47)
    tem_mapa_comparativo:       bool = False
    tem_desconsideracao_valores: bool = False
    tem_analise_critica:        bool = False
    tem_valor_estimado:         bool = False

    # Grupo 5 — Situações específicas
    tem_planilha_custos:      bool = False   # serviços com mão de obra
    tem_catalogo_tic:         bool = False   # catálogo SGD de TIC
    tem_criterios_engenharia: bool = False   # Decreto 7.983/2013
    tem_orcamento_sigiloso:   bool = False
    tem_aprovacao_demandante: bool = False

    # Grupo 6 — Encerramento
    tem_assinatura: bool = False
    tem_data:       bool = False


# ─────────────────────────────────────────────────────────────────────
#  EXTRAÇÃO DE TEXTO
# ─────────────────────────────────────────────────────────────────────

def _erro(msg: str):
    print(f"\n❌ ERRO: {msg}\n", file=sys.stderr)
    sys.exit(1)


def _caminho_seguro(caminho: str) -> str:
    import shutil, tempfile
    ext = Path(caminho).suffix.lower()
    dest = os.path.join(tempfile.gettempdir(), f"pp_temp{ext}")
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
#  PARSING DA PESQUISA DE PREÇOS
# ─────────────────────────────────────────────────────────────────────

def parse_pp(texto: str) -> PP:
    pp = PP()
    pp.texto_completo = texto

    # Número do processo SEI
    m = re.search(r"\b(\d{2}\.\d{2}\.\d{4}\.\d{7}/\d{4}-\d{2})\b", texto)
    if m:
        pp.num_processo = m.group(1)

    # Objeto
    m = re.search(
        r"(?:OBJETO|DESCRI[ÇC][AÃ]O\s+DO\s+OBJETO|ITEM\s+PESQUISADO)"
        r"[:\s]+(.{20,400}?)(?:\n[A-Z\d]|\Z)",
        texto, re.DOTALL | re.IGNORECASE)
    if m:
        pp.objeto_descricao = m.group(1).strip()[:300]

    pp.tem_descricao_objeto = bool(pp.objeto_descricao) or bool(re.search(
        r"descri[çc][aã]o\s+do\s+objeto|objeto\s+(?:pesquisado|a\s+ser\s+contratado)"
        r"|especifica[çc][aã]o\s+(?:do\s+item|t[eé]cnica)|item\s+\d+.*(?:unidade|und|qtd)",
        texto, re.IGNORECASE))

    # Unidade requisitante
    for pat in [
        r"(?:Unidade\s+Requisitante|[Áa]rea\s+Requisitante|Unidade\s+Demandante"
        r"|Setor\s+Requisitante|Setor\s+Solicitante)[:\s]+([^\n]{4,80})",
        r"(?:Coordenadoria|Assessoria|Diretoria|Secretaria|Gerência)\s+de\s+[^\n]{4,60}",
    ]:
        m = re.search(pat, texto[:4000], re.IGNORECASE)
        if m:
            pp.unidade_requisitante = m.group(0).strip()[:80]
            break

    # ── Classificação ────────────────────────────────────────────────
    pp.is_tic = bool(re.search(
        r"\bTIC\b|tecnologia\s+da\s+informa[çc][aã]o|software|hardware"
        r"|licen[çc]a\s+de\s+uso|solu[çc][aã]o\s+de\s+TI|cat[áa]logo.*(?:SGD|TIC)",
        texto, re.IGNORECASE))

    pp.is_servico_mao_obra = bool(re.search(
        r"m[aã]o\s+de\s+obra\s+exclusiva|dedica[çc][aã]o\s+exclusiva\s+de\s+m[aã]o\s+de\s+obra"
        r"|posto\s+de\s+(?:trabalho|servi[çc]o)|conven[çc][aã]o\s+coletiva|\bCCT\b"
        r"|planilha\s+de\s+custos\s+e\s+forma[çc][aã]o\s+de\s+pre[çc]os",
        texto, re.IGNORECASE))

    pp.is_obra_engenharia = bool(re.search(
        r"obra[s]?\s+(?:e\s+servi[çc]os?\s+)?de\s+engenharia|servi[çc]o\s+de\s+engenharia"
        r"|\bSINAPI\b|\bSICRO\b|Decreto\s+n[º°]?\s*7\.983|or[çc]amento\s+anal[íi]tico"
        r"|BDI\b|composi[çc][aã]o\s+de\s+custos\s+unit[áa]rios",
        texto, re.IGNORECASE))

    pp.is_contratacao_direta = bool(re.search(
        r"dispensa\s+de\s+licita[çc][aã]o|inexigibilidade|contrata[çc][aã]o\s+direta"
        r"|art\.?\s*7[45]\b",
        texto, re.IGNORECASE))

    # ── Grupo 1 — Elementos obrigatórios (art. 44) ───────────────────
    pp.tem_identificacao_agentes = bool(re.search(
        r"respons[áa]vel\s+pela\s+pesquisa|agente[s]?\s+respons[áa]ve"
        r"|pesquisa\s+realizada\s+por|equipe\s+de\s+planejamento"
        r"|elaborad[ao]\s+por|matr[íi]cula\s*n?[º°]?\s*[\d\.]+",
        texto, re.IGNORECASE))

    pp.tem_caracterizacao_fontes = bool(re.search(
        r"fonte[s]?\s+(?:consultada|de\s+pesquisa|utilizada)"
        r"|caracteriza[çc][aã]o\s+das?\s+fontes?|par[aâ]metro[s]?\s+(?:utilizado|de\s+pesquisa)"
        r"|origem\s+d[oa]s?\s+(?:pre[çc]o|dado)",
        texto, re.IGNORECASE))

    pp.tem_serie_precos = bool(re.search(
        r"s[ée]rie\s+de\s+pre[çc]os|pre[çc]os?\s+coletad|valores?\s+coletad"
        r"|R\$\s*[\d\.]+,\d{2}.*R\$\s*[\d\.]+,\d{2}"
        r"|tabela\s+(?:de\s+)?(?:pre[çc]os|valores)|quadro\s+comparativo",
        texto, re.IGNORECASE | re.DOTALL))

    pp.tem_metodo_estatistico = bool(re.search(
        r"m[ée]dia\s+(?:aritm[ée]tica|dos?\s+(?:pre[çc]o|valor))|mediana|moda\b"
        r"|menor\s+(?:pre[çc]o|valor)\s+(?:obtido|coletado|dentre)"
        r"|m[ée]todo\s+estat[íi]stico|crit[ée]rio\s+(?:estat[íi]stico|de\s+c[áa]lculo)"
        r"|desvio\s+padr[aã]o|coeficiente\s+de\s+varia[çc][aã]o",
        texto, re.IGNORECASE))

    pp.tem_justificativa_metodologia = bool(re.search(
        r"justificativa.*(?:metodologia|m[ée]todo|crit[ée]rio)"
        r"|metodologia.*(?:justific|adotad|utilizad)"
        r"|adotou-se|optou-se\s+(?:pela|pelo)|foi\s+(?:adotad|utilizad)[oa].*(?:por|em\s+raz[aã]o)"
        r"|justifica-se\s+(?:a|o)\s+(?:ado[çc][aã]o|uso|escolha)",
        texto, re.IGNORECASE))

    pp.tem_memoria_calculo = bool(re.search(
        r"mem[oó]ria\s+de\s+c[áa]lculo|planilha\s+de\s+c[áa]lculo"
        r"|c[áa]lculo\s+do\s+valor\s+estimado|demonstrativo\s+de\s+c[áa]lculo"
        r"|f[oó]rmula\s+(?:utilizada|aplicada)|[\(\[].*[\+\-\*/].*[\)\]]\s*[/÷]\s*\d",
        texto, re.IGNORECASE))

    pp.tem_justificativa_fornecedores = bool(re.search(
        r"justificativa.*(?:escolha|sele[çc][aã]o).*fornecedor"
        r"|fornecedor(?:es)?.*(?:escolhid|selecionad).*(?:por|em\s+raz[aã]o|crit[ée]rio)"
        r"|crit[ée]rio[s]?\s+(?:de\s+)?(?:escolha|sele[çc][aã]o)\s+d[oe]s?\s+fornecedor"
        r"|empresas?\s+(?:do\s+ramo|atuantes?\s+no\s+mercado)",
        texto, re.IGNORECASE))

    # ── Grupo 2 — Condições comerciais (art. 45) ─────────────────────
    pp.tem_condicoes_comerciais = bool(re.search(
        r"condi[çc][oõ]es\s+comerciais|prazo\s+(?:de\s+)?entrega|local\s+de\s+entrega"
        r"|frete|garantia\s+(?:do\s+produto|exigida|m[íi]nima)"
        r"|instala[çc][aã]o\s+e\s+montagem|forma\s+de\s+pagamento|prazo\s+de\s+pagamento",
        texto, re.IGNORECASE))

    pp.tem_taxa_risco = bool(re.search(
        r"taxa\s+de\s+risco|matriz\s+de\s+aloca[çc][aã]o\s+de\s+riscos?"
        r"|risco.*(?:compat[íi]vel|atribu[íi]do).*contratad",
        texto, re.IGNORECASE))

    # ── Grupo 3 — Parâmetros de pesquisa (art. 46) ───────────────────
    pp.tem_painel_precos = bool(re.search(
        r"painel\s+de\s+pre[çc]os|painel\.compras|banco\s+de\s+pre[çc]os\s+em\s+sa[úu]de"
        r"|sistema[s]?\s+oficia(?:l|is)\s+de\s+governo|\bPNCP\b|comprasnet"
        r"|compras\.gov\.br",
        texto, re.IGNORECASE))

    pp.tem_contratacoes_similares = bool(re.search(
        r"contrata[çc][oõ]es?\s+similar|contrato[s]?\s+similar"
        r"|ata\s+de\s+registro\s+de\s+pre[çc]os|\bARP\b"
        r"|contrata[çc][aã]o\s+(?:anterior|de\s+outro\s+[óo]rg[aã]o)"
        r"|preg[aã]o\s+n[º°]?\s*\d+.*(?:\d{4})",
        texto, re.IGNORECASE))

    pp.tem_midia_especializada = bool(re.search(
        r"m[íi]dia\s+especializada|s[íi]tio[s]?\s+especializado|tabela\s+de\s+refer[êe]ncia"
        r"|revista\s+especializada|publica[çc][aã]o\s+especializada"
        r"|\bwww\.|https?://|dom[íi]nio\s+amplo|data\s+e\s+hora\s+de\s+acesso",
        texto, re.IGNORECASE))

    pp.tem_notas_fiscais = bool(re.search(
        r"nota[s]?\s+fiscal(?:is|)\s*(?:eletr[oô]nica|emitida|n[º°])"
        r"|base\s+oficial\s+de\s+notas\s+fiscais|\bNF-?e\b",
        texto, re.IGNORECASE))

    pp.tem_pesquisa_direta = bool(re.search(
        r"pesquisa\s+direta|consulta\s+direta.*fornecedor|solicita[çc][aã]o\s+(?:formal\s+)?de\s+cota[çc][aã]o"
        r"|proposta[s]?\s+(?:comercia(?:l|is)|de\s+pre[çc]os?)|or[çc]amento[s]?\s+(?:apresentad|recebid)"
        r"|cota[çc][oõ]es?\s+(?:recebida|obtida)",
        texto, re.IGNORECASE))

    pp.tem_priorizacao_oficiais = pp.tem_painel_precos or pp.tem_contratacoes_similares or bool(re.search(
        r"prioriza(?:ndo|[çc][aã]o).*(?:sistema|painel|oficial)"
        r"|impossibilidade.*(?:painel|sistema\s+oficial|contrata[çc][oõ]es\s+similar)"
        r"|n[aã]o\s+(?:foi|foram)\s+(?:localizad|encontrad).*(?:painel|sistema\s+oficial)",
        texto, re.IGNORECASE))

    # Contagem de CNPJ (proxy do nº de fornecedores consultados)
    cnpjs = set(re.findall(r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b", texto))
    cnpjs |= set(re.findall(r"\bCNPJ\s*n?[º°]?\s*:?\s*([\d\.\-/]{14,20})", texto, re.IGNORECASE))
    pp.num_cnpj_detectados = len(cnpjs)

    # Contagem aproximada de fontes efetivamente utilizadas
    fontes = [
        pp.tem_painel_precos,
        pp.tem_contratacoes_similares,
        pp.tem_midia_especializada,
        pp.tem_notas_fiscais,
        pp.tem_pesquisa_direta,
    ]
    pp.num_fontes_detectadas = sum(1 for f in fontes if f)

    pp.tem_dados_completos_proposta = bool(re.search(
        r"\bCNPJ\b", texto, re.IGNORECASE)) and bool(re.search(
        r"endere[çc]o|telefone|e-?mail|raz[aã]o\s+social", texto, re.IGNORECASE))

    pp.tem_prazo_validade = bool(re.search(
        r"prazo\s+de\s+validade|validade\s+d[ao]\s+(?:proposta|or[çc]amento|cota[çc][aã]o)"
        r"|v[áa]lid[ao]\s+(?:por|at[ée])|data\s+de\s+emiss[aã]o"
        r"|(?:6|seis)\s*\(?(?:seis)?\)?\s*meses",
        texto, re.IGNORECASE))

    pp.tem_registro_nao_respondentes = bool(re.search(
        r"n[aã]o\s+(?:responder|enviar|retornar)|sem\s+resposta|n[aã]o\s+houve\s+retorno"
        r"|empresas?\s+consultada[s]?\s+que\s+n[aã]o|deixaram\s+de\s+(?:responder|apresentar)"
        r"|relação\s+de\s+fornecedores\s+consultados",
        texto, re.IGNORECASE))

    # ── Grupo 4 — Tratamento estatístico (art. 47) ───────────────────
    pp.tem_mapa_comparativo = bool(re.search(
        r"mapa\s+comparativo|quadro\s+comparativo|planilha\s+comparativa"
        r"|comparativo\s+de\s+pre[çc]os|tabela\s+comparativa",
        texto, re.IGNORECASE))

    pp.tem_desconsideracao_valores = bool(re.search(
        r"desconsiderad|desclassificad|exclu[íi]d[oa].*(?:valor|pre[çc]o|proposta)"
        r"|inexequ[íi]ve|inconsistent|excessivamente\s+elevad"
        r"|discrepant|outlier|fora\s+da\s+(?:m[ée]dia|curva)",
        texto, re.IGNORECASE))

    pp.tem_analise_critica = bool(re.search(
        r"an[áa]lise\s+cr[íi]tica|avalia[çc][aã]o\s+cr[íi]tica|analisad[oa]s?\s+criticamente"
        r"|varia[çc][aã]o\s+(?:entre|dos?)\s+(?:os\s+)?(?:valor|pre[çc]o)"
        r"|grande\s+varia[çc][aã]o|dispers[aã]o\s+dos?\s+(?:pre[çc]o|valor)"
        r"|amplitude\s+(?:dos?\s+)?(?:pre[çc]o|valor)",
        texto, re.IGNORECASE))

    pp.tem_valor_estimado = bool(re.search(
        r"valor\s+(?:total\s+)?estimad|pre[çc]o\s+estimad|valor\s+de\s+refer[êe]ncia"
        r"|valor\s+m[áa]ximo\s+(?:aceit[áa]vel|admitid)"
        r"|estimativa\s+(?:total\s+)?d[oe]\s+(?:valor|contrata[çc][aã]o)",
        texto, re.IGNORECASE))

    # ── Grupo 5 — Situações específicas ──────────────────────────────
    pp.tem_planilha_custos = bool(re.search(
        r"planilha\s+de\s+custos\s+e\s+forma[çc][aã]o\s+de\s+pre[çc]os"
        r"|Anexo\s+VII-?D|conven[çc][aã]o\s+coletiva|\bCCT\b"
        r"|m[oó]dulo\s+[1-6]|encargos\s+sociais.*percentual",
        texto, re.IGNORECASE))

    pp.tem_catalogo_tic = bool(re.search(
        r"cat[áa]logo\s+de\s+solu[çc][oõ]es\s+de\s+TIC|condi[çc][oõ]es\s+padronizadas"
        r"|Secretaria\s+de\s+Governo\s+Digital|\bSGD\b|IN\s+SGD/ME\s+n[º°]?\s*94",
        texto, re.IGNORECASE))

    pp.tem_criterios_engenharia = bool(re.search(
        r"Decreto\s+n[º°]?\s*7\.983|\bSINAPI\b|\bSICRO\b|\bBDI\b"
        r"|composi[çc][aã]o\s+de\s+custos\s+unit[áa]rios|or[çc]amento\s+anal[íi]tico"
        r"|IN\s+SEGES/ME\s+n[º°]?\s*91",
        texto, re.IGNORECASE))

    pp.tem_orcamento_sigiloso = bool(re.search(
        r"or[çc]amento\s+sigiloso|car[áa]ter\s+sigiloso|sigilo\s+d[oa]\s+(?:or[çc]amento|estimativa)"
        r"|art\.?\s*24.*14\.133|anexo\s+classificado",
        texto, re.IGNORECASE))

    pp.tem_aprovacao_demandante = bool(re.search(
        r"aprova[çc][aã]o\s+d[ao]\s+(?:unidade|[áa]rea|setor)\s+(?:demandante|requisitante)"
        r"|submetid[oa].*(?:aprova[çc][aã]o|exame).*(?:demandante|requisitante)"
        r"|ci[êe]ncia\s+d[ao]\s+(?:unidade|setor)\s+(?:demandante|requisitante)"
        r"|autoridade\s+competente.*aprov",
        texto, re.IGNORECASE))

    # ── Grupo 6 — Encerramento ───────────────────────────────────────
    pp.tem_assinatura = bool(re.search(
        r"assinad[oa]\s+eletronicamente|assinatura\s+eletr[oô]nica|documento\s+assinado"
        r"|matr[íi]cula|cargo/fun[çc][aã]o|equipe\s+de\s+planejamento"
        r"|respons[áa]vel\s+pela\s+pesquisa",
        texto[-5000:], re.IGNORECASE))

    pp.tem_data = bool(re.search(
        r"\b\d{2}/\d{2}/\d{4}\b|data\s+da\s+(?:pesquisa|consulta|coleta)"
        r"|realizada\s+em\s+\d{2}",
        texto, re.IGNORECASE))

    return pp


# ─────────────────────────────────────────────────────────────────────
#  CHECKLIST DE CONFORMIDADE
# ─────────────────────────────────────────────────────────────────────

def _add(achados: list, **kwargs) -> None:
    kwargs["numero"] = len(achados) + 1
    achados.append(Achado(**kwargs))


def checar_elementos_obrigatorios(pp: PP, achados: list) -> None:
    """Grupo 1 — Elementos obrigatórios do art. 44 do Decreto (PI) 21.872/2023."""

    if not pp.tem_descricao_objeto:
        _add(achados,
            titulo="Pesquisa de Preços sem Descrição do Objeto Pesquisado (Art. 44, I)",
            tipo="Vício Formal",
            localizacao="Preâmbulo / cabeçalho da Pesquisa de Preços",
            inconsistencia=(
                "A Pesquisa de Preços não apresenta a descrição do objeto pesquisado. "
                "A descrição é elemento obrigatório do documento e condição para "
                "verificar a aderência dos preços coletados às características "
                "efetivamente especificadas no Termo de Referência — pesquisa realizada "
                "sobre objeto diverso do que será licitado não serve como parâmetro "
                "válido de estimativa."
            ),
            fundamentacao=(
                "Art. 6º, XXIII, 'i', e art. 23, caput, da Lei nº 14.133/2021; art. 44, "
                "I, do Decreto Estadual (PI) nº 21.872/2023; art. 3º, I, da IN SEGES/ME "
                "nº 65/2021."
            ),
            acao=(
                "Inserir na Pesquisa de Preços a descrição completa de cada item "
                "pesquisado, com especificação técnica, unidade de medida e quantidade, "
                "rigorosamente coincidente com o Termo de Referência."
            ),
            sugestao=(
                "[Estruturar tabela: 'Item | Descrição/Especificação técnica | Unidade | "
                "Quantidade', com descrição idêntica à do TR (doc. SEI nº [ID]).']"
            ),
        )

    if not pp.tem_identificacao_agentes:
        _add(achados,
            titulo="Pesquisa de Preços sem Identificação dos Agentes Responsáveis (Art. 44, II)",
            tipo="Vício Formal",
            localizacao="Preâmbulo ou fecho da Pesquisa de Preços",
            inconsistencia=(
                "A Pesquisa de Preços não identifica o agente ou a equipe responsável "
                "pela sua realização. A identificação é elemento obrigatório do "
                "documento e pressuposto de responsabilização funcional pelos valores "
                "apurados, além de permitir a verificação da observância da segregação "
                "de funções."
            ),
            fundamentacao=(
                "Art. 44, II, do Decreto Estadual (PI) nº 21.872/2023; art. 3º, II, da "
                "IN SEGES/ME nº 65/2021; art. 7º, § 1º, da Lei nº 14.133/2021."
            ),
            acao=(
                "Identificar no documento o(s) agente(s) responsável(is) pela pesquisa, "
                "com nome completo, cargo/função e matrícula, ou indicar a Equipe de "
                "Planejamento da Contratação designada."
            ),
            sugestao=(
                "[Ex: 'A presente pesquisa de preços foi realizada por [Nome completo], "
                "[cargo/função], matrícula nº [XXXX], integrante da Equipe de "
                "Planejamento da Contratação designada nos autos.']"
            ),
        )

    if not pp.tem_caracterizacao_fontes:
        _add(achados,
            titulo="Pesquisa de Preços sem Caracterização das Fontes Consultadas (Art. 44, III)",
            tipo="Vício Material",
            localizacao="Corpo da Pesquisa de Preços",
            inconsistencia=(
                "A Pesquisa de Preços não caracteriza as fontes consultadas. A norma "
                "exige a identificação precisa de cada fonte — sistema oficial, "
                "contratação similar, mídia especializada, nota fiscal ou fornecedor "
                "consultado —, com os respectivos elementos de rastreabilidade. Sem a "
                "caracterização, os valores apresentados não são verificáveis nem "
                "auditáveis."
            ),
            fundamentacao=(
                "Art. 23, § 1º, da Lei nº 14.133/2021; art. 44, III, e art. 46 do "
                "Decreto Estadual (PI) nº 21.872/2023; art. 3º, III, e art. 5º da "
                "IN SEGES/ME nº 65/2021."
            ),
            acao=(
                "Caracterizar cada fonte utilizada: (a) Painel de Preços — indicar "
                "filtros, período e data de acesso; (b) contratações similares — "
                "indicar órgão, número do contrato/ARP e data; (c) mídia especializada "
                "— indicar URL, data e hora de acesso; (d) fornecedores — indicar razão "
                "social e CNPJ."
            ),
            sugestao=(
                "[Estruturar tabela: 'Fonte | Tipo (art. 46, inciso) | Identificação "
                "(órgão / URL / CNPJ) | Data de consulta | Valor unitário obtido'.]"
            ),
        )

    if not pp.tem_serie_precos:
        _add(achados,
            titulo="Pesquisa de Preços sem Apresentação da Série de Preços Coletados (Art. 44, IV)",
            tipo="Vício Material",
            localizacao="Corpo da Pesquisa de Preços",
            inconsistencia=(
                "A Pesquisa de Preços não apresenta a série completa dos preços "
                "coletados. A norma exige a exibição de todos os valores obtidos — "
                "inclusive os posteriormente desconsiderados —, de modo a permitir a "
                "verificação da dispersão dos preços e a aferição da razoabilidade do "
                "valor estimado final."
            ),
            fundamentacao=(
                "Art. 23, caput, da Lei nº 14.133/2021; art. 44, IV, e art. 47, § 3º, "
                "do Decreto Estadual (PI) nº 21.872/2023; art. 3º, IV, e art. 6º, § 3º, "
                "da IN SEGES/ME nº 65/2021."
            ),
            acao=(
                "Apresentar tabela contendo todos os preços coletados por item, com "
                "identificação da fonte e do valor unitário, destacando expressamente "
                "aqueles que foram desconsiderados e o respectivo motivo."
            ),
            sugestao=(
                "[Estruturar Mapa Comparativo: 'Item | Fonte 1 (R$) | Fonte 2 (R$) | "
                "Fonte 3 (R$) | ... | Valor Estimado (R$)', com nota de rodapé "
                "identificando os valores desconsiderados e o motivo.]"
            ),
        )

    if not pp.tem_metodo_estatistico:
        _add(achados,
            titulo="Pesquisa de Preços sem Aplicação de Método Estatístico Explícito (Art. 44, V)",
            tipo="Vício Material",
            localizacao="Seção de apuração do valor estimado",
            inconsistencia=(
                "A Pesquisa de Preços não explicita o método estatístico aplicado para "
                "a definição do valor estimado. A norma admite a média, a mediana ou o "
                "menor dos valores obtidos, incidindo o cálculo sobre conjunto de três "
                "ou mais preços. A ausência de indicação do método impede verificar a "
                "consistência da estimativa e a sua aderência ao regulamento."
            ),
            fundamentacao=(
                "Art. 23, § 2º, da Lei nº 14.133/2021; art. 44, V, e art. 47, caput, do "
                "Decreto Estadual (PI) nº 21.872/2023; art. 3º, V e VI, e art. 6º da "
                "IN SEGES/ME nº 65/2021."
            ),
            acao=(
                "Indicar expressamente o método estatístico aplicado (média, mediana ou "
                "menor valor) e demonstrar que o cálculo incidiu sobre conjunto de, no "
                "mínimo, três preços válidos, desconsiderados os inexequíveis, "
                "inconsistentes e excessivamente elevados."
            ),
            sugestao=(
                "[Ex: 'O valor estimado foi apurado pela MÉDIA ARITMÉTICA dos preços "
                "válidos coletados, incidindo o cálculo sobre [N] valores, após a "
                "desconsideração de [X] valores classificados como excessivamente "
                "elevados, nos termos do art. 47, caput e § 3º, do Decreto Estadual "
                "(PI) nº 21.872/2023.']"
            ),
        )

    if not pp.tem_justificativa_metodologia:
        _add(achados,
            titulo="Pesquisa de Preços sem Justificativa da Metodologia Adotada (Art. 44, VI)",
            tipo="Vício Formal",
            localizacao="Seção metodológica da Pesquisa de Preços",
            inconsistencia=(
                "A Pesquisa de Preços não justifica a metodologia utilizada — "
                "especialmente quanto à escolha entre média, mediana ou menor valor e "
                "quanto aos critérios de desconsideração de valores inconsistentes. A "
                "justificativa é elemento obrigatório e materializa o dever de motivação "
                "das escolhas técnicas."
            ),
            fundamentacao=(
                "Art. 44, VI, e art. 47, § 1º e § 3º, do Decreto Estadual (PI) nº "
                "21.872/2023; art. 3º, VI, e art. 6º, § 3º, da IN SEGES/ME nº 65/2021; "
                "art. 50 da Lei nº 9.784/1999."
            ),
            acao=(
                "Inserir seção justificando a metodologia adotada, explicando por que "
                "o método escolhido é o mais adequado ao caso concreto e quais critérios "
                "objetivos orientaram eventual desconsideração de valores."
            ),
            sugestao=(
                "[Ex: 'Optou-se pela MEDIANA em razão da elevada dispersão entre os "
                "valores coletados (amplitude de [X]%), o que tornaria a média "
                "aritmética suscetível à distorção pelos valores extremos. Foram "
                "desconsiderados os valores que se afastaram em mais de [Y]% da mediana "
                "preliminar, por serem considerados inconsistentes.']"
            ),
        )

    if not pp.tem_memoria_calculo:
        _add(achados,
            titulo="Pesquisa de Preços sem Memória de Cálculo do Valor Estimado (Art. 44, VII)",
            tipo="Vício Material",
            localizacao="Seção de apuração do valor estimado",
            inconsistencia=(
                "A Pesquisa de Preços não apresenta a memória de cálculo do valor "
                "estimado nem os documentos comprobatórios que lhe dão suporte. A "
                "memória de cálculo é elemento obrigatório e expressamente exigido pela "
                "Lei nº 14.133/2021 — sua ausência impede a verificação aritmética da "
                "estimativa e compromete a instrução do processo."
            ),
            fundamentacao=(
                "Art. 6º, XXIII, 'i', art. 18, § 1º, VI, e art. 23 da Lei nº 14.133/2021; "
                "art. 44, VII, do Decreto Estadual (PI) nº 21.872/2023; art. 3º, VII, da "
                "IN SEGES/ME nº 65/2021."
            ),
            acao=(
                "Acrescentar a memória de cálculo detalhada, demonstrando a operação "
                "aritmética que conduziu ao valor estimado unitário e global, e anexar "
                "os documentos comprobatórios (prints do Painel de Preços, propostas, "
                "atas, notas fiscais)."
            ),
            sugestao=(
                "[Ex: 'MEMÓRIA DE CÁLCULO — Item 01: Valores válidos coletados: "
                "R$ [A]; R$ [B]; R$ [C]. Média = (A + B + C) / 3 = R$ [X] (valor "
                "unitário estimado). Valor global = R$ [X] × [Q] unidades = R$ [Total]. "
                "Documentos comprobatórios no Anexo [Y].']"
            ),
        )


def checar_parametros_pesquisa(pp: PP, achados: list) -> None:
    """Grupo 2/3 — Parâmetros de pesquisa e condições comerciais (arts. 45 e 46)."""

    if pp.num_fontes_detectadas == 0:
        _add(achados,
            titulo="Pesquisa de Preços sem Utilização de Qualquer Parâmetro Legal Reconhecido",
            tipo="Vício Material",
            localizacao="Corpo da Pesquisa de Preços",
            inconsistencia=(
                "Não foi identificada, no documento, a utilização de nenhum dos "
                "parâmetros de pesquisa previstos no art. 46 do Decreto Estadual (PI) "
                "nº 21.872/2023 — sistemas oficiais, contratações similares, mídia "
                "especializada, notas fiscais ou pesquisa direta com fornecedores. A "
                "estimativa de valor deve necessariamente apoiar-se em pelo menos um "
                "desses parâmetros."
            ),
            fundamentacao=(
                "Art. 23, § 1º, I a V, da Lei nº 14.133/2021; art. 46, caput e incisos "
                "I a V, do Decreto Estadual (PI) nº 21.872/2023; art. 5º da IN SEGES/ME "
                "nº 65/2021."
            ),
            acao=(
                "Refazer a pesquisa de preços utilizando, de forma combinada ou não, os "
                "parâmetros do art. 46, priorizando os sistemas oficiais (Painel de "
                "Preços) e as contratações similares da Administração Pública."
            ),
            sugestao=(
                "[Ex: 'A pesquisa utilizou os seguintes parâmetros do art. 46 do "
                "Decreto Estadual (PI) nº 21.872/2023: (I) Painel de Preços "
                "(painel.compras.gov.br), consulta em [data]; (II) Ata de Registro de "
                "Preços nº [XX/AAAA] do [órgão]; (V) pesquisa direta com [N] "
                "fornecedores.']"
            ),
        )
    elif pp.num_fontes_detectadas == 1 and pp.tem_pesquisa_direta \
            and not pp.tem_priorizacao_oficiais:
        _add(achados,
            titulo=(
                "Estimativa Derivada Exclusivamente de Propostas de Fornecedores sem "
                "Justificativa para a Não Utilização dos Sistemas Oficiais"
            ),
            tipo="Vício Material",
            localizacao="Seção metodológica da Pesquisa de Preços",
            inconsistencia=(
                "A estimativa de valor apoia-se exclusivamente em propostas obtidas por "
                "consulta direta a fornecedores, sem que se apresente justificativa "
                "fundamentada para a não utilização dos parâmetros prioritários — "
                "sistemas oficiais de governo (Painel de Preços) e contratações "
                "similares da Administração Pública. A norma estabelece ordem de "
                "preferência entre os parâmetros e a inversão exige motivação expressa."
            ),
            fundamentacao=(
                "Art. 23, § 1º, IV, da Lei nº 14.133/2021; art. 46, I, II e V, do "
                "Decreto Estadual (PI) nº 21.872/2023; art. 5º, § 1º, da IN SEGES/ME "
                "nº 65/2021; art. 20, § 3º, da IN SEGES/ME nº 81/2022."
            ),
            acao=(
                "Complementar a pesquisa com consulta ao Painel de Preços e a "
                "contratações similares da Administração Pública. Não sendo possível, "
                "registrar expressamente a tentativa de consulta e a justificativa "
                "fundamentada para a impossibilidade (ex.: inexistência de item "
                "equivalente cadastrado, ausência de contratações similares no período)."
            ),
            sugestao=(
                "[Ex: 'Foi realizada consulta ao Painel de Preços em [data], sem que se "
                "localizassem registros de contratações do objeto nos últimos 12 meses, "
                "conforme comprovante juntado (doc. SEI nº [ID]). Igualmente, não foram "
                "identificadas contratações similares por outros órgãos. Por essa razão, "
                "a estimativa apoiou-se exclusivamente em propostas obtidas por consulta "
                "direta a [N] fornecedores do ramo, nos termos do art. 46, V, do Decreto "
                "Estadual (PI) nº 21.872/2023.']"
            ),
        )

    if pp.tem_pesquisa_direta and pp.num_cnpj_detectados < MIN_FONTES_ESPERADO:
        _add(achados,
            titulo=(
                f"Pesquisa Direta com Quantitativo Insuficiente de Fornecedores "
                f"({pp.num_cnpj_detectados} CNPJ identificado(s))"
            ),
            tipo="Vício Material",
            localizacao="Corpo da Pesquisa de Preços — propostas de fornecedores",
            inconsistencia=(
                f"Foram identificados apenas {pp.num_cnpj_detectados} CNPJ(s) distinto(s) "
                "no documento, quantitativo inferior ao mínimo de 3 (três) fornecedores "
                "exigido para a pesquisa direta. A norma estabelece esse patamar mínimo "
                "para conferir consistência estatística à estimativa; quantitativo "
                "inferior exige justificativa expressa e aprovação da autoridade "
                "competente."
            ),
            fundamentacao=(
                "Art. 23, § 1º, IV, da Lei nº 14.133/2021; art. 46, V, e art. 47, § 5º, "
                "do Decreto Estadual (PI) nº 21.872/2023; art. 6º, § 5º, da IN SEGES/ME "
                "nº 65/2021."
            ),
            acao=(
                "Complementar a pesquisa até atingir, no mínimo, 3 (três) propostas de "
                "fornecedores com CNPJ distintos e sem relacionamento societário entre "
                "si. Não sendo possível, apresentar justificativa fundamentada nos autos "
                "e submetê-la à aprovação da autoridade competente."
            ),
            sugestao=(
                "[Ex: 'Foram consultadas [N] empresas do ramo, das quais [M] "
                "apresentaram proposta. A obtenção de quantitativo inferior a três "
                "propostas decorre de [justificativa — ex.: restrição do mercado local, "
                "objeto de nicho especializado], o que se submete à aprovação da "
                "autoridade competente nos termos do art. 47, § 5º, do Decreto Estadual "
                "(PI) nº 21.872/2023.']"
            ),
        )

    if not pp.tem_condicoes_comerciais:
        _add(achados,
            titulo="Pesquisa de Preços sem Observância das Condições Comerciais Praticadas (Art. 45)",
            tipo="Vício Formal",
            localizacao="Corpo da Pesquisa de Preços",
            inconsistencia=(
                "A Pesquisa de Preços não registra a observância das condições "
                "comerciais praticadas — prazos e locais de entrega, instalação e "
                "montagem, quantidade contratada, formas e prazos de pagamento, fretes "
                "e garantias exigidas. Preços coletados sob condições comerciais "
                "diversas das que serão contratadas não são comparáveis e distorcem a "
                "estimativa."
            ),
            fundamentacao=(
                "Art. 23, caput, da Lei nº 14.133/2021; art. 45, caput, do Decreto "
                "Estadual (PI) nº 21.872/2023; art. 4º da IN SEGES/ME nº 65/2021."
            ),
            acao=(
                "Registrar na Pesquisa de Preços que as condições comerciais do TR "
                "foram informadas aos fornecedores consultados e consideradas na "
                "análise das fontes, especificando: prazo e local de entrega, "
                "quantidade, forma e prazo de pagamento, frete e garantia exigida."
            ),
            sugestao=(
                "[Ex: 'As solicitações de cotação informaram expressamente as seguintes "
                "condições comerciais, coincidentes com o Termo de Referência: entrega "
                "em [local], no prazo de [X] dias; quantidade de [Q] unidades; "
                "pagamento em até 30 dias após o recebimento definitivo; frete CIF; "
                "garantia mínima de [Y] meses.']"
            ),
        )

    if pp.tem_pesquisa_direta and not pp.tem_dados_completos_proposta:
        _add(achados,
            titulo="Propostas de Fornecedores sem os Dados Identificadores Obrigatórios",
            tipo="Vício Formal",
            localizacao="Anexos / propostas de fornecedores",
            inconsistencia=(
                "As propostas obtidas por consulta direta não contêm todos os dados "
                "identificadores exigidos: razão social, CNPJ, endereço físico e "
                "eletrônico, telefone de contato, data de emissão, nome completo e "
                "identificação do responsável pela cotação. A completude desses dados é "
                "condição de idoneidade da proposta como fonte de pesquisa e permite a "
                "verificação da inexistência de relacionamento societário entre os "
                "consultados."
            ),
            fundamentacao=(
                "Art. 6º, XXIII, 'i', e art. 18, § 1º, VI, da Lei nº 14.133/2021; "
                "art. 46, V, do Decreto Estadual (PI) nº 21.872/2023; art. 5º, § 2º, da "
                "IN SEGES/ME nº 65/2021; art. 26, § 1º, da Portaria TCU nº 121/2023."
            ),
            acao=(
                "Solicitar aos fornecedores a reapresentação das propostas com todos os "
                "dados identificadores, e verificar nos autos que os CNPJs são distintos "
                "e que não há sócios ou endereços em comum entre as empresas consultadas."
            ),
            sugestao=(
                "[Exigir em cada proposta: 'Razão social; CNPJ; endereço completo; "
                "telefone; e-mail; data de emissão; prazo de validade; nome completo, "
                "cargo e assinatura do responsável.' Registrar nos autos: 'Verificou-se "
                "que as empresas consultadas possuem CNPJs distintos e não apresentam "
                "sócios ou endereços em comum.']"
            ),
        )

    if not pp.tem_prazo_validade:
        _add(achados,
            titulo="Pesquisa de Preços sem Registro da Data de Emissão e do Prazo de Validade das Cotações",
            tipo="Vício Formal",
            localizacao="Corpo da Pesquisa de Preços / propostas anexadas",
            inconsistencia=(
                "A Pesquisa de Preços não registra a data de emissão e o prazo de "
                "validade das cotações obtidas. A norma veda a utilização de orçamentos "
                "obtidos com mais de 6 (seis) meses de antecedência da data de "
                "divulgação do edital, salvo justificativa expressa com aplicação de "
                "índice de atualização — o controle desse prazo depende do registro das "
                "datas."
            ),
            fundamentacao=(
                "Art. 23, § 1º, da Lei nº 14.133/2021; art. 46, V, e art. 46, § 1º, do "
                "Decreto Estadual (PI) nº 21.872/2023; art. 5º, § 2º, da IN SEGES/ME "
                "nº 65/2021."
            ),
            acao=(
                "Registrar a data de emissão de cada cotação e a data de realização da "
                "pesquisa, atestando que os orçamentos observam o prazo máximo de 6 "
                "(seis) meses. Excedido o prazo, aplicar índice oficial de atualização "
                "com a devida justificativa."
            ),
            sugestao=(
                "[Ex: 'Todas as cotações foram obtidas entre [data inicial] e [data "
                "final], observado o prazo máximo de 6 (seis) meses previsto no art. 46, "
                "V, do Decreto Estadual (PI) nº 21.872/2023.']"
            ),
        )

    if pp.tem_pesquisa_direta and not pp.tem_registro_nao_respondentes:
        _add(achados,
            titulo="Ausência de Registro dos Fornecedores Consultados que Não Apresentaram Proposta",
            tipo="Sugestão de Melhoria",
            localizacao="Corpo da Pesquisa de Preços",
            inconsistencia=(
                "A Pesquisa de Preços não registra a relação de fornecedores que foram "
                "consultados mas não enviaram propostas. Esse registro é boa prática "
                "expressamente recomendada pela norma: demonstra o esforço efetivo de "
                "ampliação da amostra, afasta a suspeita de consulta direcionada e "
                "explica a eventual insuficiência de propostas obtidas."
            ),
            fundamentacao=(
                "Art. 23, § 1º, IV, da Lei nº 14.133/2021; art. 46, § 3º, do Decreto "
                "Estadual (PI) nº 21.872/2023; art. 5º, § 2º, da IN SEGES/ME nº 65/2021; "
                "art. 28, § 4º, II a IV, da Portaria TCU nº 121/2023."
            ),
            acao=(
                "Incluir na Pesquisa de Preços quadro relacionando todas as empresas "
                "consultadas, com indicação de quais responderam e quais não "
                "responderam, bem como a data e o meio das comunicações realizadas."
            ),
            sugestao=(
                "[Estruturar quadro: 'Empresa | CNPJ | Data da solicitação | Meio "
                "(e-mail/ofício) | Resposta (Sim/Não)'. Ex: 'Foram consultadas 6 (seis) "
                "empresas, das quais 3 (três) apresentaram proposta e 3 (três) não "
                "responderam à solicitação, conforme comprovantes de envio juntados aos "
                "autos.']"
            ),
        )


def checar_tratamento_estatistico(pp: PP, achados: list) -> None:
    """Grupo 4 — Mapa Comparativo e tratamento estatístico (art. 47)."""

    if not pp.tem_mapa_comparativo:
        _add(achados,
            titulo="Ausência de Mapa Comparativo de Preços Consolidando as Fontes",
            tipo="Vício Formal",
            localizacao="Documento de Pesquisa de Preços",
            inconsistencia=(
                "Não foi identificado Mapa Comparativo de Preços consolidando, em "
                "quadro único, todos os valores obtidos nas diferentes fontes. O Mapa "
                "Comparativo é o instrumento que materializa a série de preços "
                "coletados e viabiliza a análise crítica da dispersão — deve compor "
                "todos os valores obtidos e somente então indicar os desclassificados."
            ),
            fundamentacao=(
                "Art. 23, caput, da Lei nº 14.133/2021; art. 44, IV, e art. 47, caput e "
                "§ 3º, do Decreto Estadual (PI) nº 21.872/2023; art. 2º, I, art. 3º, VI, "
                "e art. 6º, § 3º, da IN SEGES/ME nº 65/2021."
            ),
            acao=(
                "Elaborar Mapa Comparativo de Preços em formato tabular, com uma linha "
                "por item e uma coluna por fonte consultada, exibindo todos os valores "
                "obtidos, os valores desconsiderados (destacados), o método aplicado e "
                "o valor estimado final."
            ),
            sugestao=(
                "[Estruturar: 'Item | Descrição | Qtd | Fonte 1 | Fonte 2 | Fonte 3 | "
                "Fonte 4 | Valores desconsiderados | Método | Valor unitário estimado | "
                "Valor global'. Totalizar ao final com o valor global estimado da "
                "contratação.]"
            ),
        )

    if pp.tem_desconsideracao_valores and not pp.tem_justificativa_metodologia:
        _add(achados,
            titulo="Desconsideração de Valores sem Critério Fundamentado e Descrito nos Autos",
            tipo="Vício Material",
            localizacao="Seção de tratamento dos preços coletados",
            inconsistencia=(
                "O documento indica a desconsideração de valores coletados sem "
                "descrever o critério objetivo que fundamentou a exclusão. A norma exige "
                "que os critérios de desconsideração de valores inexequíveis, "
                "inconsistentes ou excessivamente elevados sejam fundamentados e "
                "descritos no processo administrativo — a exclusão discricionária de "
                "valores pode distorcer artificialmente a estimativa."
            ),
            fundamentacao=(
                "Art. 23, § 2º, da Lei nº 14.133/2021; art. 44, VI, e art. 47, § 3º, do "
                "Decreto Estadual (PI) nº 21.872/2023; art. 6º, § 3º, da IN SEGES/ME "
                "nº 65/2021."
            ),
            acao=(
                "Descrever o critério objetivo aplicado para a desconsideração de "
                "valores (ex.: desvio percentual em relação à média ou mediana "
                "preliminar) e justificar individualmente cada exclusão realizada."
            ),
            sugestao=(
                "[Ex: 'CRITÉRIO DE DESCONSIDERAÇÃO: foram excluídos os valores que se "
                "afastaram em mais de 25% (vinte e cinco por cento), para mais ou para "
                "menos, da mediana preliminar do conjunto. Com base nesse critério, foi "
                "desconsiderado o valor de R$ [X] (fonte: [identificação]), por "
                "representar [Y]% acima da mediana, sendo classificado como "
                "excessivamente elevado.']"
            ),
        )

    if not pp.tem_analise_critica:
        _add(achados,
            titulo="Pesquisa de Preços sem Análise Crítica dos Valores Coletados (Art. 47, § 4º)",
            tipo="Sugestão de Melhoria",
            localizacao="Seção de apuração do valor estimado",
            inconsistencia=(
                "A Pesquisa de Preços não apresenta análise crítica dos preços "
                "coletados, especialmente quanto à variação entre os valores obtidos. A "
                "norma exige análise crítica sempre que houver grande dispersão — "
                "amplitude elevada pode indicar especificação ambígua, cotações sobre "
                "objetos distintos ou preço inexequível, e a mera aplicação mecânica de "
                "média sobre valores dispersos produz estimativa inconsistente."
            ),
            fundamentacao=(
                "Art. 23, caput e § 2º, da Lei nº 14.133/2021; art. 47, § 4º, do "
                "Decreto Estadual (PI) nº 21.872/2023; art. 6º da IN SEGES/ME "
                "nº 65/2021; art. 21, parágrafo único, da Portaria TCU nº 121/2023."
            ),
            acao=(
                "Inserir seção de análise crítica avaliando a dispersão dos valores "
                "coletados (amplitude, desvio em relação à média), justificando as "
                "variações relevantes e atestando a razoabilidade do valor estimado "
                "final frente aos preços praticados no mercado."
            ),
            sugestao=(
                "[Ex: 'ANÁLISE CRÍTICA: Os valores coletados variaram entre R$ [mín] e "
                "R$ [máx], correspondendo a amplitude de [X]%. A variação é compatível "
                "com as diferenças de [porte do fornecedor / prazo de entrega / "
                "localização], não se identificando indício de inexequibilidade ou "
                "sobrepreço. O valor estimado de R$ [Y] mostra-se compatível com os "
                "preços praticados no mercado.']"
            ),
        )

    if not pp.tem_valor_estimado:
        _add(achados,
            titulo="Pesquisa de Preços sem Apresentação Consolidada do Valor Estimado da Contratação",
            tipo="Vício Material",
            localizacao="Conclusão da Pesquisa de Preços",
            inconsistencia=(
                "A Pesquisa de Preços não apresenta, de forma consolidada e conclusiva, "
                "o valor estimado unitário e global da contratação. A conclusão "
                "explícita é o produto útil do documento — é esse valor que instrui o "
                "TR, fundamenta a reserva orçamentária e define o parâmetro máximo "
                "aceitável no certame."
            ),
            fundamentacao=(
                "Art. 6º, XXIII, 'i', art. 18, § 1º, VI, e art. 23, caput, da Lei nº "
                "14.133/2021; art. 36, IX, e art. 47 do Decreto Estadual (PI) nº "
                "21.872/2023."
            ),
            acao=(
                "Inserir seção conclusiva apresentando o valor unitário estimado por "
                "item e o valor global da contratação, por extenso, e indicando a data "
                "de referência da estimativa."
            ),
            sugestao=(
                "[Ex: 'CONCLUSÃO: O valor total estimado da contratação é de "
                "R$ [X.XXX,XX] ([valor por extenso]), na data-base de [mês/ano], "
                "conforme detalhamento por item constante do Mapa Comparativo anexo.']"
            ),
        )


def checar_situacoes_especificas(pp: PP, achados: list) -> None:
    """Grupo 5 — Regras específicas por natureza do objeto."""

    if pp.is_servico_mao_obra and not pp.tem_planilha_custos:
        _add(achados,
            titulo="[Mão de Obra] Ausência de Planilha de Custos e Formação de Preços",
            tipo="Vício Material",
            localizacao="Documento de Pesquisa de Preços",
            inconsistencia=(
                "Tratando-se de contratação de serviços com dedicação exclusiva de mão "
                "de obra, a Pesquisa de Preços não apresenta a Planilha de Custos e "
                "Formação de Preços elaborada pela Administração. Nessas contratações, "
                "a estimativa não pode apoiar-se apenas em cotações globais: exige "
                "planilha analítica construída a partir da Convenção Coletiva de "
                "Trabalho vigente da categoria, com notas explicativas."
            ),
            fundamentacao=(
                "Art. 23, § 1º, da Lei nº 14.133/2021; art. 9º da IN SEGES/ME nº "
                "65/2021; Anexo VII-D da IN SEGES/MP nº 5/2017; art. 30 da Portaria TCU "
                "nº 121/2023."
            ),
            acao=(
                "Elaborar Planilha de Custos e Formação de Preços conforme modelo "
                "padronizado (Anexo VII-D da IN SEGES/MP nº 5/2017), preenchida pela "
                "Administração com base na CCT vigente da categoria, acompanhada de "
                "notas explicativas de cada módulo."
            ),
            sugestao=(
                "[Ex: 'A estimativa foi elaborada mediante Planilha de Custos e "
                "Formação de Preços (Anexo [X]), construída com base na Convenção "
                "Coletiva de Trabalho [nº de registro MTE], vigente de [período], "
                "compreendendo: Módulo 1 (composição da remuneração), Módulo 2 "
                "(encargos e benefícios), Módulo 3 (provisão para rescisão), Módulo 4 "
                "(reposição do profissional ausente), Módulo 5 (insumos diversos) e "
                "Módulo 6 (custos indiretos, tributos e lucro).']"
            ),
        )

    if pp.is_obra_engenharia and not pp.tem_criterios_engenharia:
        _add(achados,
            titulo="[Engenharia] Pesquisa de Preços sem Observância dos Critérios Específicos de Obras e Serviços de Engenharia",
            tipo="Vício Material",
            localizacao="Documento de Pesquisa de Preços",
            inconsistencia=(
                "Tratando-se de obra ou serviço de engenharia, a Pesquisa de Preços não "
                "demonstra a observância dos critérios específicos aplicáveis. Nesses "
                "objetos, a estimativa deve basear-se em orçamento analítico com "
                "composição de custos unitários referenciados em sistemas oficiais "
                "(SINAPI, SICRO ou equivalentes) e explicitar o BDI adotado."
            ),
            fundamentacao=(
                "Art. 23, § 2º, da Lei nº 14.133/2021; Decreto Federal nº 7.983/2013; "
                "IN SEGES/ME nº 91/2022; art. 31 da Portaria TCU nº 121/2023; Acórdão "
                "TCU nº 2.622/2013-Plenário (BDI referencial)."
            ),
            acao=(
                "Substituir ou complementar a estimativa por orçamento analítico com "
                "composição de custos unitários referenciada no SINAPI ou SICRO, "
                "explicitando a data-base das tabelas, os itens sem referência oficial "
                "(com a respectiva justificativa de composição) e a memória de cálculo "
                "do BDI."
            ),
            sugestao=(
                "[Ex: 'O orçamento estimativo foi elaborado com base no SINAPI "
                "[Estado/PI], data-base [mês/ano], com composição analítica por item. "
                "Os itens não constantes do sistema oficial ([relacionar]) foram "
                "compostos a partir de [fonte], conforme justificado no Anexo [X]. O "
                "BDI adotado é de [Y]%, conforme memória de cálculo do Anexo [Z], "
                "situando-se dentro dos parâmetros do Acórdão TCU nº 2.622/2013-Plenário.']"
            ),
        )

    if pp.tem_orcamento_sigiloso and not pp.tem_justificativa_metodologia:
        _add(achados,
            titulo="Adoção de Orçamento Sigiloso sem Motivação Expressa nos Autos",
            tipo="Vício Formal",
            localizacao="Seção de classificação do orçamento",
            inconsistencia=(
                "O documento indica a adoção de orçamento sigiloso sem apresentar "
                "motivação expressa quanto à necessidade do sigilo e ao momento de sua "
                "divulgação. O sigilo do orçamento é exceção ao princípio da "
                "publicidade e depende de motivação específica, devendo o valor ser "
                "disponibilizado aos órgãos de controle a qualquer tempo."
            ),
            fundamentacao=(
                "Art. 24 e art. 18, § 1º, VI, da Lei nº 14.133/2021; art. 10 da IN "
                "SEGES/ME nº 65/2021; art. 36, X, do Decreto Estadual (PI) nº 21.872/2023."
            ),
            acao=(
                "Inserir motivação expressa sobre a adoção do orçamento sigiloso e "
                "sobre o momento de sua divulgação, registrando que o valor permanecerá "
                "acessível aos órgãos de controle interno e externo."
            ),
            sugestao=(
                "[Ex: 'O orçamento estimado tem caráter sigiloso, nos termos do art. 24 "
                "da Lei nº 14.133/2021, tendo em vista [justificativa — ex.: o risco de "
                "nivelamento das propostas ao valor máximo]. O valor será divulgado "
                "imediatamente após o encerramento da fase de lances, permanecendo "
                "acessível aos órgãos de controle a qualquer tempo.']"
            ),
        )

    if not pp.tem_aprovacao_demandante:
        _add(achados,
            titulo="Ausência de Submissão dos Preços Encontrados ao Exame da Unidade Demandante",
            tipo="Sugestão de Melhoria",
            localizacao="Seção conclusiva da Pesquisa de Preços",
            inconsistencia=(
                "Não há registro de que os preços apurados tenham sido submetidos ao "
                "exame e à aprovação da unidade de atuação demandante. Trata-se de "
                "procedimento de gestão de riscos recomendado pelos normativos e pelos "
                "órgãos de controle: a unidade demandante, por conhecer tecnicamente o "
                "objeto, é quem melhor pode atestar a compatibilidade dos valores com "
                "a realidade do mercado do segmento."
            ),
            fundamentacao=(
                "Art. 169, I, da Lei nº 14.133/2021; art. 24, caput e § 1º, VI, da IN "
                "SEGES/MP nº 5/2017; art. 17 do Decreto Federal nº 9.203/2017; art. 21, "
                "parágrafo único, da Portaria TCU nº 121/2023; Enunciado CJF nº 54/2023."
            ),
            acao=(
                "Submeter formalmente o resultado da pesquisa à unidade demandante para "
                "manifestação sobre a adequação dos preços, e juntar aos autos o "
                "respectivo pronunciamento antes do prosseguimento do feito."
            ),
            sugestao=(
                "[Ex: 'Os preços apurados foram submetidos ao exame da unidade "
                "demandante, que se manifestou pela sua compatibilidade com os valores "
                "praticados no mercado do segmento, conforme despacho constante dos "
                "autos (doc. SEI nº [ID]).']"
            ),
        )


def checar_encerramento(pp: PP, achados: list) -> None:
    """Grupo 6 — Data e assinatura."""

    if not pp.tem_data:
        _add(achados,
            titulo="Pesquisa de Preços sem Indicação da Data de Realização",
            tipo="Vício Formal",
            localizacao="Cabeçalho ou fecho da Pesquisa de Preços",
            inconsistencia=(
                "A Pesquisa de Preços não indica a data em que foi realizada. A data é "
                "elemento essencial para aferir a atualidade da estimativa e a "
                "observância dos prazos de validade dos parâmetros utilizados "
                "(12 meses para contratações similares, 6 meses para cotações diretas)."
            ),
            fundamentacao=(
                "Art. 23, § 1º, da Lei nº 14.133/2021; art. 46, II e V, do Decreto "
                "Estadual (PI) nº 21.872/2023; art. 5º, § 2º, da IN SEGES/ME nº 65/2021."
            ),
            acao=(
                "Registrar no documento a data de realização da pesquisa e a data-base "
                "de referência do valor estimado."
            ),
            sugestao=(
                "[Ex: 'Pesquisa realizada no período de [data inicial] a [data final]. "
                "Data-base do valor estimado: [mês/ano].']"
            ),
        )

    if not pp.tem_assinatura:
        _add(achados,
            titulo="Pesquisa de Preços sem Evidência de Assinatura do Agente Responsável",
            tipo="Vício Formal",
            localizacao="Fecho da Pesquisa de Preços",
            inconsistencia=(
                "A Pesquisa de Preços não apresenta evidência de assinatura pelo agente "
                "responsável por sua elaboração. A assinatura é condição de validade "
                "formal do documento e materializa a assunção de responsabilidade "
                "funcional pelos valores apurados."
            ),
            fundamentacao=(
                "Art. 7º, caput, e art. 12, VI, da Lei nº 14.133/2021; art. 44, II, do "
                "Decreto Estadual (PI) nº 21.872/2023; art. 3º, II, da IN SEGES/ME "
                "nº 65/2021."
            ),
            acao=(
                "Assinar eletronicamente a Pesquisa de Preços no SEI, com identificação "
                "do agente responsável (nome, cargo/função e matrícula) ou dos "
                "integrantes da Equipe de Planejamento da Contratação."
            ),
            sugestao=(
                "[Ex fecho: 'Teresina (PI), na data da assinatura eletrônica. "
                "[Nome completo] — [Cargo/função] — Matrícula nº [XXXX] — Responsável "
                "pela pesquisa de preços.']"
            ),
        )


def checar_quesitos_json(pp: PP, achados: list) -> None:
    """Verifica quesitos declarativos definidos em quesitos_PP.json."""
    import json
    caminho_json = BASE_DIR / "quesitos_PP.json"
    if not caminho_json.exists():
        return
    try:
        with open(caminho_json, encoding="utf-8") as f:
            dados = json.load(f)
    except Exception:
        return
    texto = pp.texto_completo
    for q in dados.get("quesitos", []):
        if q.get("is_tic_only") and not pp.is_tic:
            continue
        if q.get("is_direta_only") and not pp.is_contratacao_direta:
            continue
        if q.get("is_servico_only") and not pp.is_servico_mao_obra:
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

def salvar_achados_json(pp: PP, achados: list, caminho_origem: str) -> str:
    """Salva os achados em JSON para consolidação posterior no Ofício final."""
    import json
    base = Path(caminho_origem).stem
    pasta = Path(caminho_origem).parent
    caminho_json = str(pasta / f"achados_PP_{base}.json")

    dados = {
        "artefato": "PP",
        "num_processo": pp.num_processo or "",
        "objeto": pp.objeto_descricao or "",
        "unidade": pp.unidade_requisitante or "",
        "is_tic": pp.is_tic,
        "data_analise": DATA_ANALISE,
        "arquivo_origem": Path(caminho_origem).name,
        "fontes_detectadas": pp.num_fontes_detectadas,
        "cnpj_detectados": pp.num_cnpj_detectados,
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


def gerar_oficio_word(pp: PP, achados: list, caminho_saida: str):
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

    unidade  = pp.unidade_requisitante or "[Unidade Requisitante]"
    processo = pp.num_processo         or "[nº do processo SEI]"

    p = doc.add_paragraph()
    p.add_run(f"À {unidade}").bold = True
    p = doc.add_paragraph()
    p.add_run(
        f"Assunto: Devolução de Autos para Saneamento — "
        f"Análise da Pesquisa de Preços e do Mapa Comparativo — "
        f"Processo SEI nº {processo}."
    ).bold = True

    doc.add_paragraph()
    doc.add_paragraph().add_run("Senhor(a) Coordenador(a),")
    doc.add_paragraph()

    abertura = [
        (
            "Cumprimentando-o cordialmente, registro que a equipe desta Assessoria "
            "analisou a Pesquisa de Preços e o respectivo Mapa Comparativo juntados "
            "aos autos do processo em referência, verificando a conformidade dos "
            "documentos com os normativos aplicáveis: Lei nº 14.133/2021, Decreto "
            "Estadual (PI) nº 21.872/2023 (arts. 44 a 47), IN SEGES/ME nº 65/2021 e "
            "Atos PGJ/MPPI nº 1.381 e 1.382/2024."
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
    p.add_run("1. ARTEFATO: PESQUISA DE PREÇOS E MAPA COMPARATIVO DE PREÇOS (PP)").bold = True
    doc.add_paragraph()

    if not achados:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(1)
        p.add_run(
            "Nenhuma inconsistência identificada. Pesquisa de Preços em conformidade "
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
        "Salientamos que a consistência da pesquisa de preços é determinante para a "
        "economicidade da contratação: estimativas subdimensionadas conduzem a "
        "certames fracassados, ao passo que estimativas superdimensionadas expõem a "
        "Administração ao risco de sobrepreço e à responsabilização perante os órgãos "
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

def imprimir_relatorio(pp: PP, achados: list):
    sep = "─" * 68
    print(f"\n{'═' * 68}")
    print(f"  ANÁLISE DE CONFORMIDADE — PESQUISA DE PREÇOS  (v{VERSION})")
    print(f"{'═' * 68}")
    print(f"  Processo: {pp.num_processo or '(não identificado)'}")
    print(f"  Unidade : {pp.unidade_requisitante or '(não identificada)'}")
    print(f"  Objeto  : {(pp.objeto_descricao or '(não identificado)')[:70]}...")
    flags_cls = []
    if pp.is_tic:               flags_cls.append("TIC")
    if pp.is_servico_mao_obra:  flags_cls.append("Mão de obra exclusiva")
    if pp.is_obra_engenharia:   flags_cls.append("Obra/Engenharia")
    if pp.is_contratacao_direta: flags_cls.append("Contratação direta")
    print(f"  Tipo    : {', '.join(flags_cls) or '(não classificado)'}")
    print(f"  Fontes  : {pp.num_fontes_detectadas} parâmetro(s) do art. 46 identificado(s)")
    print(f"  CNPJs   : {pp.num_cnpj_detectados} fornecedor(es) identificado(s)")
    print(f"  Data    : {DATA_ANALISE}")
    print(sep)

    checks = [
        ("Descrição do objeto (art. 44, I)",        pp.tem_descricao_objeto),
        ("Agentes responsáveis (art. 44, II)",      pp.tem_identificacao_agentes),
        ("Caracterização das fontes (art. 44, III)", pp.tem_caracterizacao_fontes),
        ("Série de preços (art. 44, IV)",           pp.tem_serie_precos),
        ("Método estatístico (art. 44, V)",         pp.tem_metodo_estatistico),
        ("Justificativa metodologia (art. 44, VI)", pp.tem_justificativa_metodologia),
        ("Memória de cálculo (art. 44, VII)",       pp.tem_memoria_calculo),
        ("Justificativa fornecedores (art. 44, VIII)", pp.tem_justificativa_fornecedores),
        ("Condições comerciais (art. 45)",          pp.tem_condicoes_comerciais),
        ("Painel de Preços (art. 46, I)",           pp.tem_painel_precos),
        ("Contratações similares (art. 46, II)",    pp.tem_contratacoes_similares),
        ("Mídia especializada (art. 46, III)",      pp.tem_midia_especializada),
        ("Notas fiscais (art. 46, IV)",             pp.tem_notas_fiscais),
        ("Pesquisa direta (art. 46, V)",            pp.tem_pesquisa_direta),
        ("Dados completos das propostas",           pp.tem_dados_completos_proposta),
        ("Prazo de validade das cotações",          pp.tem_prazo_validade),
        ("Registro de não respondentes",            pp.tem_registro_nao_respondentes),
        ("Mapa Comparativo",                        pp.tem_mapa_comparativo),
        ("Análise crítica (art. 47, § 4º)",         pp.tem_analise_critica),
        ("Valor estimado consolidado",              pp.tem_valor_estimado),
        ("Aprovação da unidade demandante",         pp.tem_aprovacao_demandante),
        ("Assinatura",                              pp.tem_assinatura),
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

    pp = parse_pp(texto)
    achados: list = []

    checar_elementos_obrigatorios(pp, achados)
    checar_parametros_pesquisa(pp, achados)
    checar_tratamento_estatistico(pp, achados)
    checar_situacoes_especificas(pp, achados)
    checar_encerramento(pp, achados)
    checar_quesitos_json(pp, achados)

    print(f"      {len(achados)} achado(s) identificado(s)")
    imprimir_relatorio(pp, achados)

    salvar_achados_json(pp, achados, caminho)

    if "--oficio" in sys.argv:
        base = Path(caminho).stem
        saida = str(Path(caminho).parent / f"Oficio_ASSCOMPRAS_PP_{base}.docx")
        gerar_oficio_word(pp, achados, saida)
    else:
        print("ℹ  Para gerar o Ofício Word desta análise isolada, use: --oficio")
        print("ℹ  Para consolidar todos os artefatos do processo, use: gerar_oficio_processo.py\n")


if __name__ == "__main__":
    main()
