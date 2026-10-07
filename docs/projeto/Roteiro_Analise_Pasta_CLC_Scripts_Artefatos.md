---
tipo: Roteiro Técnico de Análise de Acervo
orgao: Assessoria de Compras / CLC - MPPI
assunto: Roteiro para análise completa da pasta CLC com vistas à criação de scripts de análise de artefatos de contratação
versao: 1.0
data: 30/09/2026
elaboracao: [nome do servidor] - Técnico Ministerial, Mat. [matrícula] - Chefe da Assessoria de Compras
tags: [roteiro, scripts, quesitos, DFD, ETP, TR, PP, MR, DAP, automacao]
---

# ROTEIRO DE ANÁLISE COMPLETA DA PASTA CLC — BASE PARA OS SCRIPTS DE ANÁLISE DE ARTEFATOS

> **Pasta analisada:** `C:\Users\thiagonogueira\OneDrive - mppi.mp.br\CLC`
> **Data do diagnóstico:** 30/09/2026
> **Produto final visado:** conjunto de scripts de análise automatizada dos artefatos da fase preparatória (DFD, DAP, ETP, Mapa de Riscos, TR, Pesquisa de Preços, Mapa Comparativo de Preços e documentos correlatos), com geração de achados no padrão do Ofício ASSCOMPRAS de Devolução para Saneamento.

---

## 1. OBJETIVO E PREMISSAS

1. **Objetivo.** Estruturar, em fases sucessivas e verificáveis, o estudo integral do acervo da pasta CLC, de modo a:
    1.1. identificar todos os pontos analisados e quesitos já formulados pela Assessoria de Compras e por fontes externas (CNMP, AGU, MPPE, SINCIN, TCE-PI);
        1.1.1. consolidá-los em uma *matriz única de quesitos*, sem duplicidade e com rastreabilidade à fonte;
        1.1.2. vincular cada quesito ao dispositivo normativo vigente.
    1.2. extrair, dos ofícios de devolução efetivamente expedidos, a *tipologia real de achados*, para calibrar e testar os scripts;
    1.3. refatorar e ampliar os scripts já existentes (`analisar_*.py`), em vez de reescrevê-los do zero.
2. **Premissas.**
    2.1. A análise automatizada é *instrumento de triagem*; não substitui o juízo do Agente de Contratação (art. 53 da **Lei nº 14.133/2021**).
    2.2. O escopo dos scripts é conformidade **formal, legal e matemática**; o mérito administrativo (conveniência e oportunidade) permanece fora do alcance da automação.
    2.3. Nenhum valor legal atualizável (art. 182 da **Lei nº 14.133/2021**) deve ser fixado no código; os valores vigentes devem ser lidos de arquivo de configuração normativa.
    2.4. Todo achado sem evidência no texto do artefato deve ser reportado como "Dado não disponível" ou "[INFORMAÇÃO NÃO CONSTANTE NOS AUTOS]", nunca inferido.

---

## 2. DIAGNÓSTICO DO ACERVO (INVENTÁRIO DE 30/09/2026)

### 2.1. Volume por diretório

| Diretório | Arquivos | Tamanho | Conteúdo predominante | Relevância para os scripts |
|---|---:|---:|---|---|
| `01_Processos_e_Aquisicoes/Assessoria de Compras/PGEAs` | 3.091 | ≈ 3,4 GB | Processos reais exportados do SEI (PDF/HTML), ofícios de devolução, análises | **Crítica** — corpus de teste e fonte de achados reais |
| `01_Processos_e_Aquisicoes/Base de Conhecimento - Thiago` | 838 | — | Scripts, checklists, normativos em `.md`, MJRs, modelos AGU/MPPE/MPPI | **Crítica** — motor atual e base normativa |
| `02_Modelos_POPs_e_Roteiros` | 94 | 27 MB | Quesitos, roteiros-checkbox, POPs, TAPP-D, notas técnicas | **Crítica** — fonte primária de quesitos |
| `03_IA_e_Automacao` | 54 | 2,2 MB | Banco de prompts revisores, SKILL.md, n8n, painel | **Alta** — regras já formuladas em linguagem natural |
| `04_Arquivo_e_Duplicados` | 162 | 138 MB | Duplicatas arquivadas, diagnósticos | Baixa — excluir do corpus |
| `Base Legal CLC - Atualizada Maio.2026` (subpasta de CLC) | 0 | 0 | *Pasta vazia* | Ver Sugestão S-14 |
| **Total** | **4.258** | **3,8 GB** | 382 diretórios | — |

### 2.2. Distribuição por formato

| Formato | Qtde. | Tratamento previsto na extração |
|---|---:|---|
| PDF | 2.349 | `pdfplumber` → *fallback* OCR (`tesseract`, disponível no equipamento) para PDFs digitalizados |
| HTML | 821 | `BeautifulSoup` (exportação nativa do SEI — melhor fidelidade de tabelas) |
| MD | 598 | Leitura direta (normativos, checklists e modelos já convertidos) |
| DOCX / DOC / ODT | 237 | `python-docx` / conversão prévia |
| XLSX / ODS / CSV | 96 | `openpyxl` / `pandas` (mapas comparativos, quesitos, listas de verificação) |
| Outros (PNG, ZIP, JSON, PY etc.) | 157 | Triagem manual |

### 2.3. Corpus de artefatos reais disponível nos PGEAs

Classificação obtida pelo padrão de nome de exportação do SEI (`[NN]-IDSEI_Tipo.html|pdf`):

| Tipo documental (nome SEI) | Ocorrências | Script correspondente |
|---|---:|---|
| Documento de Formalização da Demanda (DFD) | 78 (+11 DFD TIC) | `analisar_dfd.py` |
| Termo de Referência | 77 | `analisar_tr.py` |
| Mapa Comparativo de Preços | 56 | `analisar_pp.py` (parcial) |
| Estudo Técnico Preliminar | 40 | `analisar_etp.py` |
| Mapa de Risco e Matriz de Risco da Contratação | 39 | `analisar_mr.py` |
| Despacho de Abertura de Procedimento | 33 | `analisar_dap.py` |
| Solicitação de Parecer Orçamentário e Financeiro | 25 | **Inexistente** |
| Autorização de Empenho | 24 | **Inexistente** |
| Aprovação de Artefatos – 14.133 | 16 | **Inexistente** |
| Justificativa (dispensa de ETP, contratação direta etc.) | 16 | **Inexistente** |
| Memória de Cálculo | 15 | **Inexistente** |
| Pesquisa de Preços | 12 | `analisar_pp.py` |
| Enquadramento da Contratação | 12 | **Inexistente** |
| Parecer Jurídico / Parecer CONINT | 18 / 11 | Fora do escopo (documento de controle) |
| Anexo (listas de verificação, propostas, certidões etc.) | 247 | **Requer classificação por conteúdo** |

> *Alerta:* os 247 "Anexos" concentram peças decisivas (Lista de Verificação da MJR, propostas, certidões, Termo de Anuência). Sem classificador por conteúdo, esses documentos permanecem invisíveis aos scripts.

---

## 3. ATIVOS JÁ EXISTENTES (O QUE NÃO PRECISA SER CRIADO DO ZERO)

### 3.1. Scripts de análise (`Base de Conhecimento - Thiago/00_Ferramentas_e_Scripts_Analise`)

| Script | Linhas | Checagens estruturais (títulos distintos) | Quesitos JSON | Saída | Observação técnica |
|---|---:|---:|---:|---|---|
| `analisar_dfd.py` | 2.663 | 37 | 4 | JSON + Ofício `.docx` + DFD saneado | Único com `_validar_achados`; parser por seções 2 a 11 do modelo MPPI |
| `analisar_dap.py` | 1.287 | 18 | 6 | JSON + Ofício (`--oficio`) | Blocos: formalização, autorização, agentes, orçamento, enquadramento, artefatos, encerramento |
| `analisar_etp.py` | 1.463 | 19 | 6 | JSON + Ofício | Elementos I a XIII do art. 18, § 1º; assinaturas; sigilo |
| `analisar_mr.py` | 1.277 | 18 | 6 | JSON + Ofício (`--oficio`) | Vinculação, estrutura mínima, tratamento, abrangência, matriz de alocação, monitoramento |
| `analisar_tr.py` | 1.389 | 20 | 8 | JSON + Ofício (`--oficio`) | Referencia 21 quesitos do `Quesitos TR.xlsx` (Q1–Q70) |
| `analisar_pp.py` | 1.568 | 24 | 6 | JSON + Ofício (`--oficio`) | Verificação **apenas textual** (regex); não recalcula valores |
| `gerar_oficio_processo.py` | 317 | — | — | Ofício consolidado | Ordem canônica DFD → DAP → ETP → MR → TR → PP |
| `baixar_normativos.py`, `baixar_mjrs.py` | 426 | — | — | Atualização da base normativa | Apoio |

**Modelo de dados do achado** (já adotado nos scripts e nos JSON): `id`, `grupo`, `titulo`, `tipo`, `localizacao`, `inconsistencia`, `fundamentacao`, `acao`, `sugestao`, *flags* `is_tic_only` / `is_direta_only` / `is_servico_only`, `modo` e `patterns` (regex). Esse modelo é compatível com o template obrigatório do Ofício de Devolução e deve ser **preservado**.

### 3.2. Fontes de quesitos identificadas

| Fonte | Localização | Volume | Estrutura | Situação |
|---|---|---:|---|---|
| Roteiro Quesitos (Google) — aba *Planilha1* | `00_Ferramentas.../Roteiro Quesitos (Google).xlsx` | 145 quesitos (90 com quesito condicionante) | Nº, Grupo, Quesito, Condicionante, Resposta, Fundamentação Lei/Decreto PI | **Matriz-mestra de fato**; grupos: Verificação Comum (20), DFD (8), ETP (22), Análise de Riscos (15), TR (35), Pesquisa de Preços (29), Inexigibilidade (7), Bens (5), Serviços (2), Dispensa (2) |
| Idem — aba *Página2* (SINCIN 2, 3 e 4) | mesmo arquivo | 166 perguntas desmembradas | Temática, Pergunta, Roteiro original, Normativo, Fundamentação | Complementar; inclui obras, imóvel (art. 74, V), fornecedor exclusivo (art. 74, I) |
| Quesitos TR | `Checklists_Auditoria/Quesitos TR.xlsx` | 72 quesitos em 11 grupos | Grupo, Quesito Qn, Fundamentação | Parcialmente implementado (21 Q-ids) |
| Lista de Verificação CNMP (arquivo nomeado "MAPA DE RISCOS") | `02.../Quesitos/Anexo_1204260_MAPA_DE_RISCOS...xlsx` (3 cópias) | 12 abas: ETP, TR, Pesquisa de Preços, Licitação, Fase Externa, Contratação Direta, Contrato, Alteração Contratual, Sanções, Fiscalização, Pagamento, Modelo | Linha, Quesito, Conformidade, Setor, Observações, Data | Fonte rica, **nome enganoso** (ver S-12) |
| Verificações CNMP (DOCX "OK - …") | `02.../Quesitos/Quesitos CNMP/` | ETP, TR, Fase Interna, Contratações Diretas | Texto | Convertidas em `.md` nos Checklists de Auditoria |
| Checklists de Auditoria (`.md`) | `00_Ferramentas.../Checklists_Auditoria/` | 391 perguntas (DFD 45; ETP 76; TR 57; Revisão TR 73; Contratações Diretas 37; Fase Interna 53; Lista Fase Interna 50) | Perguntas em prosa | Não estruturadas em dados |
| Checklist ETP MPPI (Padrão) | `Checklists_Auditoria/Checklist_ETP_MPPI (Padrão).xlsx` | 33 itens | Nº, Quesito, Base legal, Conformidade, Setor | Estruturado |
| TAPP-D v4 | `Modelos_MPPI_CLC/TAPP_D_Minuta_Revisada_v4.md` | ≈ 104 marcações SIM/NÃO/NÃO SE APLICA | Seções I a XX + blocos Obras, TIC, Veículos | Checklist de dispensa art. 75, I e II, alinhado à MJR 92/2024 |
| Roteiros-Checkbox | `02.../Roteiros - Checkbox/` | 7 roteiros (Dispensa Eletrônica, Dispensa sem Disputa, Inexigibilidade, ARP, Adesão ARP, Liberação ATA, Dispensa) | Sequência de peças do processo | Base para o *verificador de completude* |
| SKILL.md (Claude - Análises) | `03_IA_e_Automacao/Claude - Análises/SKILL.md` | Roteiro por artefato + classificação de achados | Checklists em Markdown | **Contém valores desatualizados** (ver S-01) |
| Prompts Revisores | `03_IA_e_Automacao/Banco de Prompts/` | DFD, ETP, TR (por artigo e CNMP) | Prompt | Regras qualitativas a converter em quesitos |
| Nota Técnica — Sugestões de Redação | `00_Ferramentas.../Nota_Tecnica_Sugestoes_Redacao_Correcao_Artefatos.md` | Caso passagens aéreas | Localização + texto substitutivo | Modelo para o campo `sugestao` |
| Modelos externos | `03_Modelos_e_Minutas/` (AGU 14.133, MPPE, SEAD-PI, TJ-MA) | Listas de verificação AGU por objeto; checklist MPPE v2.0 | `.md`/`.xlsx` | Referência de completude por tipo de objeto |

### 3.3. Memória de cálculo da cobertura atual

```text
Checagens implementadas (títulos distintos nos scripts):
  DFD 37 + DAP 18 + ETP 19 + MR 18 + TR 20 + PP 24           = 136
Quesitos declarativos JSON:
  DFD 4 + DAP 6 + ETP 6 + MR 6 + TR 8 + PP 6                 = 36
Total de verificações automatizadas                          = 172

Fontes estruturadas de quesitos (sem deduplicação):
  Roteiro Planilha1 145 + Página2 166 + Quesitos TR 72
  + Checklist ETP 33 + Checklists .md 391                    = 807
  (+ Lista CNMP de 12 abas e TAPP-D v4: contagem a apurar na Fase 4)

Cobertura rastreável do TR:
  Q-ids citados em analisar_tr.py = 21 de 72  →  21 / 72 = 29,2 %
Cobertura rastreável dos demais artefatos:
  Dado não disponível — os scripts DFD, DAP, ETP, MR e PP não
  referenciam o Nº do quesito da matriz-mestra (apenas faixas
  genéricas, ex.: "Q69–Q83", "Q119–Q147").
```

> A cobertura real somente poderá ser aferida após a deduplicação da Fase 4. O número bruto de 807 perguntas contém sobreposição elevada entre CNMP, SINCIN e Roteiro próprio.

---

## 4. TIPOLOGIA DOS ACHADOS REAIS (MINERAÇÃO DOS OFÍCIOS DE DEVOLUÇÃO)

Foram lidos os ofícios de devolução dos processos: Recarga de Extintores (SEI 19.21.0010.0024648/2026-45 — 18 achados), Baterias Drones/GAECO (SEI 19.21.0330.0036032/2026-23 — 24 achados), Adesão Passagens Aéreas (SEI 19.21.0850.0035140/2026-11 — 21 achados, 5 versões) e Avaliação de Imóveis/Credenciamento (SEI 19.21.0014.0026458/2026-03 — 29 achados), além da Nota Técnica de Sugestões de Redação.

| Cód. | Categoria de achado | Exemplos reais | Detectado pelos scripts atuais? |
|---|---|---|---|
| T-01 | **Incoerência entre artefatos** (objeto, quantidade, valor, prazo, área requisitante) | Quantidade "1 kit" × "2 kits" no DFD; prazo de 4 × 6 meses entre DFD e ETP; subcontratação divergente ETP × TR; objeto do Mapa de Riscos estranho aos demais artefatos | **Não** (scripts analisam cada artefato isoladamente) |
| T-02 | **Erro aritmético** | Soma das unidades beneficiárias ≠ total do DFD; valor total divergente na conclusão do ETP; arredondamento incorreto em tabela | **Não** |
| T-03 | **Norma revogada, inciso ou parágrafo inexistente** | Portaria PGJ/PI 1318/2026 (revogada pela 2067/2026); Portaria 4337/2024 (revogada pela 5644/2025); parágrafo inexistente do art. 14 da IN SEGES 58/2022; inciso errado do Ato PGJ 1.415/2024 | **Não** (os `patterns` operam apenas no modo "ausente") |
| T-04 | **Texto de modelo não substituído / anotação de trabalho** | "[nome da unidade]" no item 9.1 do DFD; texto-instrução no item VI.6 do Mapa Comparativo; anotação de trabalho no corpo do ETP assinado | Parcial (DFD: "trechos genéricos do modelo") |
| T-05 | **Peça obrigatória ausente nos autos** | DAP ausente; Mapa de Riscos ausente; Análise Preliminar de Conformidade com a MJR; Lista de Verificação preenchida; certidões; portaria de designação; declaração do limite de 50% (adesão) | **Não** (não há verificador de completude do processo) |
| T-06 | **Lista de Verificação atesta o que o artefato não demonstra** | Uso de minuta padronizada do TR "atestado" sem evidência; manifestação sobre não fracionamento inexistente | **Não** |
| T-07 | **Identificação de agentes** | Matrícula divergente entre artefatos; fiscais sem matrícula; função de Integrante Requisitante atribuída indevidamente; falta de declaração de ciência | Parcial (DFD) |
| T-08 | **Pesquisa de preços — qualidade das fontes** | Fontes concentradas no mesmo órgão; edital de terceiro incluído na média; análise crítica prevista no ETP e não realizada; porte empresarial não identificado; numeração de documentos não correspondente | Parcial (apenas presença textual) |
| T-09 | **Numeração e referências cruzadas** | Item "1.5.4" fora de sequência; justificativa referida como "Anexo I" sendo documento SEI autônomo | **Não** |
| T-10 | **Omissões materiais do TR em contratação direta** | ME/EPP (LC 123/2006) sem fundamentação; margem de preferência; bem de luxo; catálogo eletrônico; instrumento substitutivo (art. 95); natureza de despesa incompatível | Parcial |
| T-11 | **Necessidade descrita como solução** | Item 9.1 do DFD; Elemento I do ETP | **Sim** (DFD e ETP) |
| T-12 | **Contradição interna do próprio artefato** | TR afirma natureza contínua e dispensa transição contratual; parágrafo contradiz a tabela anterior | **Não** |

> **Conclusão do diagnóstico:** as categorias de maior incidência real (T-01, T-02, T-03, T-05, T-06) são exatamente as que os scripts atuais **não** cobrem. O ganho marginal de novos regex por artefato é menor do que o ganho de uma camada de *verificação transversal do processo*.

---

## 5. ROTEIRO DE EXECUÇÃO — FASES DA ANÁLISE COMPLETA

### Fase 0 — Saneamento prévio do acervo

1. Definir a *fonte única de verdade* de cada ativo.
    1.1. Scripts e `quesitos_*.json`: manter exclusivamente em `00_Ferramentas_e_Scripts_Analise` (hoje há uma única cópia — preservar).
    1.2. Lista CNMP (`Anexo_1204260_...xlsx`): manter uma cópia e renomear conforme S-12.
        1.2.1. Eliminar as duas cópias remanescentes após conferência de *hash*.
    1.3. Remover do corpus a pasta `04_Arquivo_e_Duplicados` e arquivos temporários `~$*.docx`.
2. Registrar versões múltiplas de um mesmo ofício (ex.: `_v2`, `_1` a `_4`) como *séries* — são valiosas para medir quais achados foram saneados entre devoluções.

### Fase 1 — Inventário automatizado

1. Script `inventario_clc.py` gerando `inventario_clc.csv` com: caminho, extensão, tamanho, data, *hash* MD5, nº SEI extraído do caminho, ID SEI do documento, tipo documental presumido.
2. Critérios de marcação:
    2.1. `duplicado` (mesmo *hash*);
    2.2. `digitalizado` (PDF sem camada de texto);
    2.3. `fora_escopo` (mídia, instaladores, compactados).

### Fase 2 — Extração textual normalizada

1. Módulo único `extracao.py` (substitui as 6 cópias de `extrair_texto_pdf` / `extrair_texto_html`).
    1.1. Prioridade de formato: HTML do SEI > PDF com texto > DOCX > PDF com OCR.
    1.2. Preservar tabelas como estrutura (lista de linhas/células), e não apenas texto corrido — requisito para o motor aritmético.
    1.3. Normalizar: espaços, hifenização, caracteres corrompidos (há nomes com `ý` no acervo), numeração de itens.
2. Saída: `corpus.jsonl` (um registro por documento: metadados + texto + tabelas + seções detectadas).

### Fase 3 — Classificação de artefatos

1. Classificador em duas camadas:
    1.1. **Por nome SEI** (padrão `[NN]-IDSEI_Tipo`), cobrindo DFD, TR, ETP, MR, DAP, Mapa Comparativo, Pesquisa de Preços, Memória de Cálculo, Aprovação de Artefatos, Autorização de Empenho, Parecer Orçamentário, Enquadramento, Justificativa.
    1.2. **Por conteúdo** (impressões digitais textuais), obrigatória para os 247 "Anexos":
        1.2.1. Lista de Verificação da MJR 92/2024 ou 86/2025;
        1.2.2. Proposta comercial / Modelo de Apresentação de Proposta;
        1.2.3. Certidões (CND, FGTS, CNDT, CEIS/CNEP/TCU);
        1.2.4. Termo de Anuência do fornecedor (adesão);
        1.2.5. Justificativa de dispensa de ETP / de Mapa de Riscos.
2. Identificar a **modalidade do processo** (dispensa art. 75, I/II; dispensa eletrônica; inexigibilidade art. 74 e inciso; adesão ARP; aquisição por ARP própria; pregão) e o **tipo de objeto** (bem, serviço, serviço contínuo, serviço com dedicação exclusiva de mão de obra, TIC, obra/engenharia, capacitação, locação de imóvel). Esses dois atributos alimentam as *flags* de aplicabilidade dos quesitos.

### Fase 4 — Consolidação da matriz-mestra de quesitos

1. Unificar todas as fontes da seção 3.2 em `quesitos_master.json` (esquema no Anexo A).
2. Regras de consolidação:
    2.1. Tomar o **Roteiro Quesitos — Planilha1 (145 quesitos)** como espinha dorsal e numeração oficial.
    2.2. Mapear para ela as perguntas equivalentes das demais fontes (campo `fontes_equivalentes`), sem criar novo quesito quando houver equivalência.
    2.3. Criar quesito novo apenas para lacunas efetivas (ex.: T-01 a T-12 da seção 4).
    2.4. Converter os 90 quesitos condicionantes em *árvore de decisão* (`condicao` → `aplica_se_se`).
3. Para cada quesito, classificar a **forma de verificação automatizável**:

| Modo | Descrição | Exemplo |
|---|---|---|
| `ausente` | Tema obrigatório não localizado no texto (modo atual) | Falta de memória de cálculo |
| `presente_proibido` | Texto localizado que não deveria existir | Portaria revogada citada; placeholder "[nome da unidade]" |
| `campo` | Campo estruturado vazio ou inválido | Matrícula, e-mail, CATMAT/CATSER |
| `calculo` | Recomputação aritmética | Soma de itens; média/mediana do mapa |
| `cruzado` | Comparação entre dois ou mais artefatos | Quantidade DFD × TR × PP |
| `completude` | Peça obrigatória ausente nos autos | DAP, Lista de Verificação da MJR |
| `evidencia` | Afirmação de um documento conferida em outro | Lista de Verificação × TR |
| `humano` | Não automatizável; gera ponto de atenção ao Agente | Singularidade do objeto (art. 74, III) |

4. Vincular cada quesito ao dispositivo **vigente**, conferindo a cadeia de alterações na base normativa (`01_Normativos_Vigentes`) antes de fixar a fundamentação.

### Fase 5 — Mineração dos achados históricos (conjunto de referência)

1. Extrair de todos os `Oficio*Devolucao*`, `Analise*Conformidade*` e `Nota_Tecnica*` os campos do template (Artefato, Achado, Localização, Inconsistência, Fundamentação, Ação, Sugestão).
2. Vincular cada achado ao documento SEI analisado (ID SEI citado no campo "Artefato").
3. Rotular cada achado com o quesito da matriz-mestra e com a categoria T-01 a T-12.
4. Produto: `golden_set.jsonl` — gabarito para testes de regressão dos scripts (Fase 10).

### Fase 6 — Pontos de análise por artefato (conteúdo dos scripts)

Os itens abaixo consolidam o que já é verificado (scripts, roteiros, SKILL.md) e o que os ofícios reais demonstram ser necessário. Itens marcados com **[NOVO]** não possuem implementação atual.

#### 6.1. DFD — Documento de Formalização da Demanda

1. Identificação: unidade requisitante, responsável, matrícula, e-mail institucional.
2. Informações gerais: unidade orçamentária/gestora (PGJ, FMMPI, FPROCON), tipo de objeto, providências prévias, grau de prioridade.
    2.1. Previsão de início compatível com a data de elaboração (sem data retroativa) e com a vigência do TR **[NOVO — cruzado]**.
3. Equipe de Planejamento e de Fiscalização.
    3.1. Composição (Integrante Requisitante nativo do Coordenador da unidade; Técnico; Administrativo).
    3.2. Segregação de funções.
    3.3. Portaria de designação vigente **[NOVO — presente_proibido]**.
    3.4. Declaração de ciência das atribuições (**Resolução CNMP nº 283/2024**).
    3.5. Unidade beneficiária relevante integrando a equipe ou registrando ciência **[NOVO]**.
4. Objeto: descrição, CATMAT/CATSER, quantidade, valor total estimado.
    4.1. Soma das parcelas por unidade beneficiária = total declarado **[NOVO — calculo]**.
    4.2. Memória de cálculo do quantitativo.
5. Alinhamento estratégico: item do PCA, PEI 2022-2029, PDTI (somente TIC).
6. Necessidade (9.1) formulada como problema; justificativa (9.2); resultados, metas e indicadores mensuráveis (10.1 a 10.3).
7. Placeholders e textos-modelo remanescentes **[AMPLIAR — presente_proibido]**.
8. Assinatura do titular da unidade requisitante.

#### 6.2. DAP — Despacho de Abertura de Procedimento

1. Conformidade ao modelo oficial da CLC (v1.0) e ao **art. 53 do Decreto Estadual (PI) nº 21.872/2023**.
2. Nº do processo, objeto, unidade requisitante — objeto idêntico ao dos demais artefatos **[NOVO — cruzado]**.
3. Autorização expressa, ordenador de despesas signatário, rito indicado coincidente com o efetivamente instruído **[NOVO — cruzado]** (achado real: autorização de procedimento diverso).
4. Designação de agentes e substitutos; segregação de funções.
5. Adequação orçamentária e previsão no PCA.
6. Enquadramento legal com inciso específico (art. 74 ou art. 75); em adesão a ARP de outro ente, dispositivo estadual próprio **[NOVO]**.
7. Referência aos artefatos, ao parecer jurídico ou à sua dispensa (hipóteses dos Atos PGJ), divulgação no PNCP.
8. Assinatura eletrônica.

#### 6.3. ETP — Estudo Técnico Preliminar (ou Justificativa de sua dispensa)

1. Presença dos elementos do **art. 18, § 1º, da Lei nº 14.133/2021**, com obrigatoriedade mínima dos incisos I, IV, VI, VIII e XIII e justificativa para os demais.
2. Checagens já implementadas, na numeração de "Elementos" adotada por `analisar_etp.py` (que não coincide com a ordem dos incisos da lei): Elemento I (necessidade/problema e interesse público); II (requisitos); III (levantamento de mercado com alternativas e ETPs de outros órgãos); V (quantidades com memória); VI (valor com fonte; TCO em TIC); VII (parcelamento); IX (PCA); XI (providências prévias, incluindo regularidade fiscal); XIII (viabilidade declarada).
    2.1. Na refatoração, adotar como chave a numeração legal do **art. 18, § 1º**, mantendo a do modelo MPPI apenas como rótulo de localização **[AJUSTE]**.
3. Contratações correlatas e interdependentes (**art. 18, § 1º, XI**) — ausência recorrente em achado real **[AMPLIAR]**.
4. Valor total da conclusão = valor do corpo e = valor do mapa comparativo **[NOVO — calculo/cruzado]**.
5. Providências determinadas no ETP efetivamente cumpridas nos artefatos seguintes (ex.: análise crítica no Mapa Comparativo; conteúdo mínimo incorporado ao TR) **[NOVO — evidencia]**.
6. Quando dispensado: justificativa com fundamento correto (**art. 28 do Decreto Estadual nº 21.872/2023**), parágrafo e inciso existentes **[NOVO — presente_proibido]**, limite calculado sobre o valor vigente do decreto federal de atualização.
7. Assinatura de todos os integrantes; avaliação de sigilo.

#### 6.4. Mapa de Riscos / Matriz de Riscos

1. Vinculação ao processo e descrição do objeto **idêntica** à dos demais artefatos **[NOVO — cruzado]**.
2. Riscos individualizados, escala explícita de probabilidade e impacto, nível de risco, ações preventivas e de contingência, responsáveis.
3. Cobertura das fases (planejamento, seleção, gestão contratual) e categorias mínimas: orçamentária/sobrepreço, competitividade, descontinuidade; trabalhista/previdenciária (serviços); segurança da informação/LGPD (TIC).
4. Matriz de alocação contratual quando exigível (valor ou risco — critério parametrizado).
5. Declarações finais coerentes com o processo (ex.: não atribuir responsabilidade por ETP dispensado) **[NOVO — cruzado]**.
6. Quando ausente: justificativa formal de dispensa (recomendável em dispensas por valor).

#### 6.5. TR — Termo de Referência

1. Estrutura mínima do **art. 6º, XXIII, da Lei nº 14.133/2021** e dos incisos I a XX do **art. 36 do Decreto Estadual (PI) nº 21.872/2023** (lista-espelho do TAPP-D v4).
2. Os 72 quesitos do `Quesitos TR.xlsx` (11 grupos), priorizando os ainda não implementados (51 Q-ids).
3. Contratação direta: forma da dispensa (eletrônica/presencial), ME/EPP (**LC nº 123/2006, art. 48**) com fundamentação de eventual afastamento, margem de preferência (**art. 26**), bem de luxo, catálogo eletrônico (**art. 19, § 2º, e art. 40, § 1º**), instrumento substitutivo (**art. 95**) e termo de ciência do fornecedor **[AMPLIAR]**.
4. Natureza de despesa compatível com o objeto **[NOVO — tabela de elementos de despesa]**.
5. Coerência interna: natureza contínua × transição contratual; numeração sequencial; anexos referenciados que existam como tal **[NOVO]**.
6. Coerência externa: prazo, subcontratação, conteúdo mínimo e quantitativos iguais aos do ETP e DFD **[NOVO — cruzado]**.
7. Uso de minuta padronizada AGU (**Ato PGJ/PI nº 1.382/2024**, com a redação dada pelo **Ato PGJ/PI nº 1.413/2024**) demonstrado no próprio TR.

#### 6.6. Pesquisa de Preços e Mapa Comparativo de Preços

1. Elementos do **art. 44 do Decreto Estadual (PI) nº 21.872/2023** (incisos I a VII) e **IN SEGES/ME nº 65/2021** (arts. 3º a 10).
2. Fontes e parâmetros: sistemas oficiais, contratações similares, mídia especializada, pesquisa direta, notas fiscais (contratação direta).
    2.1. Concentração de fontes em um mesmo órgão ou fornecedor **[NOVO]**.
    2.2. Inclusão na série de fonte qualificada como mero parâmetro comparativo **[NOVO]**.
3. **Motor aritmético [NOVO — calculo]**:
    3.1. Recalcular, por item, média, mediana, menor valor, desvio-padrão e coeficiente de variação.
    3.2. Conferir valor total = Σ (quantidade × valor unitário estimado), com a mesma regra de arredondamento declarada.
    3.3. Sinalizar valores fora do critério de aceitabilidade *declarado no próprio mapa* (o script não deve impor critério próprio — apenas conferir a aplicação do critério adotado).
    3.4. Conferir a idade das cotações contra os prazos da norma aplicável, parametrizados em configuração (**[INFORMAÇÃO A CONFIRMAR]** quanto à prevalência entre IN 65/2021 e Decreto PI).
4. Identificação dos fornecedores: CNPJ, porte (ME/EPP), data, validade, responsável; fornecedores consultados sem resposta.
5. Correspondência entre a numeração/ID SEI citados no mapa e os documentos efetivamente juntados **[NOVO — evidencia]**.
6. Competência do responsável pela elaboração; campos-instrução não preenchidos; itens contraditórios **[NOVO]**.
7. Valor final igual ao do TR, ETP e DFD **[NOVO — cruzado]**.

#### 6.7. Outros documentos comuns (novos analisadores)

| Documento | Pontos de análise essenciais | Fonte de referência no acervo |
|---|---|---|
| Lista de Verificação da MJR (92/2024 dispensa; 86/2025 adesão) | Todos os itens respondidos; respostas "Sim" com evidência localizável; portarias citadas vigentes | `reference_mjr86...`; TAPP-D v4 |
| Análise/Declaração Conclusiva de Conformidade | Aderência ao modelo oficial (**Ato PGJ/PI nº 1.456/2024, art. 7º, II e § 3º**) | Modelo oficial registrado |
| Aprovação de Artefatos | Modelo do item 5.1 do POP-CLC-02; artefatos aprovados = artefatos juntados | `Modelos_SEI/Aprovacao_de_Artefatos_14133_*.md` |
| Solicitação de Parecer Orçamentário e Financeiro | Estrutura de 11 itens; valor e natureza de despesa coincidentes com TR/PP | Modelo oficial CLC |
| Autorização de Empenho | Estrutura de campos do modelo validado; Unidade Gestora (PGJ 25101, FMMPI, FPROCON) | Modelo validado SEI |
| Enquadramento da Contratação | Hipótese legal e limite vigente na data | Decreto federal de atualização vigente |
| Justificativa de dispensa de ETP / Mapa de Riscos | Dispositivo existente e vigente; limite de valor | Decreto PI 21.872/2023 |
| Termo de Anuência (adesão) | Quantitativo/teto coincidentes com DFD e ETP; fundamento estadual aplicável | Nota Técnica passagens aéreas |
| Certidões | Validade na data da contratação; CNPJ idêntico ao da proposta | Checklist Habilitação MPPI |
| Proposta comercial | Validade; CNPJ; preço ≤ estimado; aderência ao modelo de proposta | `Modelo Proposta de Precos.md` |

### Fase 7 — Verificações transversais do processo (novo script `analisar_processo.py`)

1. Construir, para cada processo, uma **ficha de atributos** extraída de todos os artefatos: objeto, quantidades por item, valores unitários e totais, prazos, datas, unidade requisitante, equipe (nome/matrícula/função), portarias e normas citadas, modalidade, fundamento legal.
2. Aplicar regras de coerência:

| Regra | Artefatos comparados | Tolerância |
|---|---|---|
| Objeto idêntico (similaridade textual ≥ limiar configurável) | DFD, DAP, ETP, MR, TR, PP | Configurável |
| Quantidade por item idêntica | DFD, ETP, TR, PP | Zero |
| Valor total idêntico | DFD, ETP, TR, PP, Parecer Orçamentário | Diferença de arredondamento ≤ R$ 0,01 por item |
| Prazo de execução/vigência coerente | DFD, ETP, TR, ARP (vigência) | Zero |
| Matrícula por servidor única | Todos | Zero |
| Área requisitante única | Todos | Zero |
| Norma citada vigente | Todos | Consulta ao registro normativo |
| Rito autorizado = rito instruído | DAP × TR × Enquadramento | Zero |

3. Aplicar o **verificador de completude** a partir dos Roteiros-Checkbox (seção 3.2), por modalidade identificada na Fase 3.

### Fase 8 — Registro normativo parametrizado

1. Criar `config/normativos_vigentes.yaml` contendo:
    1.1. valores do art. 75 e demais dispositivos atualizáveis, com decreto de origem e início de vigência;
    1.2. cadeia de revogações de portarias e atos (ex.: Portaria 4337/2024 → 5644/2025; Portaria 1318/2026 → 2067/2026 → retificação posterior);
    1.3. data de expiração de atos com vigência temporária.
2. Os scripts passam a ler exclusivamente esse arquivo; nenhum valor ou número de ato fica fixado no código ou no SKILL.md.

### Fase 9 — Arquitetura-alvo dos scripts

```text
clc_analise/
├── config/
│   ├── normativos_vigentes.yaml
│   └── parametros.yaml            (limiares, tolerâncias, prazos de cotação)
├── quesitos/
│   └── quesitos_master.json       (Fase 4)
├── nucleo/
│   ├── extracao.py                (Fase 2 — substitui 6 cópias)
│   ├── classificador.py           (Fase 3)
│   ├── modelo.py                  (Achado, Artefato, Processo)
│   ├── motor_regras.py            (modos ausente/presente_proibido/campo/calculo/cruzado/evidencia)
│   └── oficio.py                  (template obrigatório de devolução)
├── analisadores/
│   ├── dfd.py  dap.py  etp.py  mr.py  tr.py  pp.py
│   ├── lista_verificacao.py  aprovacao.py  parecer_orcamentario.py
│   └── processo.py                (Fase 7 — transversal)
├── testes/
│   └── golden_set.jsonl           (Fase 5)
└── clc.py                         (CLI única: clc.py analisar <pasta_do_processo> [--oficio])
```

1. Preservar os parsers específicos já maduros (em especial o do DFD, 2.663 linhas) migrando-os para `analisadores/`.
2. CLI única com comportamento uniforme (`--oficio`, `--json`, `--artefato`); corrigir, na migração, os cabeçalhos de `analisar_dfd.py` e `analisar_etp.py`, que descrevem a geração do Ofício como automática, embora o código já a condicione à *flag* `--oficio`.

### Fase 10 — Validação

1. Executar os analisadores sobre o corpus real (Seção 2.3) e comparar com `golden_set.jsonl`.
2. Métricas por quesito:

```text
Precisão   = achados corretos / achados emitidos
Revocação  = achados do gabarito detectados / achados do gabarito
Meta mínima sugerida para entrada em produção: precisão ≥ 0,80 por quesito;
quesitos abaixo da meta operam no modo "ponto de atenção", sem gerar texto de ofício.
```

3. Registrar falsos positivos conhecidos como casos de teste (ex.: DFD-Q03 — "sustentabilidade" confundida com índice de conformidade ambiental; tema tratado em outro artefato do mesmo processo).

### Fase 11 — Governança e manutenção

1. Versionamento semântico dos scripts e da matriz de quesitos, com *changelog*.
2. Revisão trimestral do `normativos_vigentes.yaml` e revisão anual obrigatória em janeiro (decreto federal de atualização).
3. Toda nova devolução expedida alimenta o `golden_set.jsonl`.

---

## 6. SUGESTÕES DE APRIMORAMENTO (PRIORIZADAS)

| ID | Sugestão | Evidência no acervo | Prioridade | Esforço |
|---|---|---|---|---|
| S-01 | **Atualizar imediatamente o SKILL.md**: os limites registrados (R$ 125.451,18 / R$ 62.725,59 e os respectivos 10×) estão superados; vigem R$ 130.984,20 (art. 75, I) e R$ 65.492,11 (art. 75, II) pelo **Decreto nº 12.807/2025**. Substituir por remissão ao decreto vigente | `SKILL.md`, linhas 85 e 228–231; o valor "125.451,18" diverge inclusive do Decreto 12.343/2024 (125.451,15) | **Crítica** | Baixo |
| S-02 | Criar `analisar_processo.py` (verificações transversais — Fase 7) | Categorias T-01, T-02, T-06, T-12: maior incidência nos ofícios reais | **Crítica** | Alto |
| S-03 | Implementar motor aritmético para Mapa Comparativo, DFD e ETP | `analisar_pp.py` só verifica menção textual a "média/mediana" | **Crítica** | Médio |
| S-04 | Criar modo `presente_proibido` (normas revogadas, placeholders, anotações de trabalho) | Achados reais com Portarias 4337/2024 e 1318/2026; "[nome da unidade]" | **Alta** | Baixo |
| S-05 | Registro normativo parametrizado (Fase 8), com alerta de expiração de atos temporários | Portaria PGJ/PI 5644/2025 com vigência de 12 meses a partir de 24/11/2025 | **Alta** | Baixo |
| S-06 | Verificador de completude por modalidade, a partir dos Roteiros-Checkbox | Achados reais T-05 (DAP, MR, Lista de Verificação, certidões ausentes) | **Alta** | Médio |
| S-07 | Refatorar funções duplicadas em núcleo comum | 7 funções repetidas nos 6 scripts (`extrair_texto_pdf`, `extrair_texto_html`, `_caminho_seguro`, `checar_quesitos_json`, `gerar_oficio_word`, `_set_font`, `salvar_achados_json`) | **Alta** | Médio |
| S-08 | Rastreabilidade: cada achado deve citar o Nº do quesito da matriz-mestra | Só o TR cita Q-ids; demais usam faixas genéricas | **Alta** | Baixo |
| S-09 | Unificar a taxonomia de classificação de achados | SKILL.md usa Crítico/Atenção/Conforme; scripts usam Vício Formal/Material/Sugestão; ofícios usam Erro Material, Omissão Relevante, Risco de Nulidade | Média | Baixo |
| S-10 | Classificador por conteúdo para os 247 "Anexos" | Lista de Verificação, Termo de Anuência e certidões estão nesses anexos | Média | Médio |
| S-11 | *Fallback* de OCR para PDFs digitalizados | Nenhum script aciona OCR; `tesseract` está instalado | Média | Baixo |
| S-12 | Renomear arquivos com nome enganoso | `Mapa_Comparativo.xlsx` é planilha do programa "MP Sustentável – Lixo" (2018–2022); `Anexo_1204260_MAPA_DE_RISCOS...xlsx` é Lista de Verificação CNMP de 12 abas (3 cópias) | Média | Baixo |
| S-13 | Estender `_validar_achados` (hoje só no DFD) a todos os analisadores | Evita achados incompletos no ofício | Média | Baixo |
| S-14 | Resolver a subpasta vazia `CLC\Base Legal CLC - Atualizada Maio.2026` e atualizar referências documentais que ainda apontam os JSON de quesitos para essa pasta | Pasta com 0 arquivos; quesitos residem em `00_Ferramentas_e_Scripts_Analise` | Média | Baixo |
| S-15 | Converter os 391 quesitos em prosa dos Checklists de Auditoria para dados estruturados | Hoje não consumíveis pelos scripts | Média | Médio |
| S-16 | Corrigir o *docstring* de `gerar_oficio_processo.py` (menciona apenas DFD, ETP e TR, mas processa 6 artefatos) | Cabeçalho do script | Baixa | Baixo |
| S-17 | Gerar, junto ao ofício, a "Nota Técnica de Sugestões de Redação" (localização literal + texto substitutivo completo) | Modelo validado no processo de passagens aéreas | Baixa | Médio |
| S-18 | Relatório de reincidência: comparar ofícios sucessivos do mesmo processo e listar achados saneados/remanescentes | Séries `_1` a `_4` (passagens) e 1ª a 3ª devolução (drones) | Baixa | Baixo |

---

## 7. CRONOGRAMA REFERENCIAL

| Etapa | Fases | Entregável | Duração estimada |
|---|---|---|---|
| 1 | 0, 1, 8 + S-01, S-12, S-14 | Acervo saneado, inventário, registro normativo | 1 semana |
| 2 | 2, 3 | `corpus.jsonl` classificado | 2 semanas |
| 3 | 4, 5 | `quesitos_master.json` + `golden_set.jsonl` | 3 semanas |
| 4 | 9 (núcleo) + S-04, S-07, S-08, S-11, S-13 | Núcleo refatorado com paridade funcional | 2 semanas |
| 5 | 6.6 (motor aritmético) + 7 | `processo.py` e motor de cálculo | 3 semanas |
| 6 | 6.7 + S-06, S-10 | Novos analisadores e completude | 2 semanas |
| 7 | 10, 11 | Relatório de validação e manual de uso | 1 semana |

> As durações são estimativas de planejamento, dependentes da disponibilidade da equipe; não constituem compromisso de prazo.

---

## ANEXO A — ESQUEMA PROPOSTO PARA `quesitos_master.json`

```json
{
  "id": "PP-017",
  "numero_roteiro": 131,
  "artefato": "PP",
  "grupo": "Pesquisa de Preços",
  "pergunta": "O valor estimado corresponde à aplicação correta do método estatístico declarado?",
  "condicao": { "quesito": "PP-010", "resposta": "SIM" },
  "aplica_se": { "modalidades": ["dispensa", "inexigibilidade", "pregao"], "objetos": ["*"] },
  "modo": "calculo",
  "regra": { "tipo": "recalculo_estatistico", "tolerancia_centavos": 1 },
  "patterns": [],
  "tipo_achado": "Vício Material",
  "fundamentacao": "Art. 23 da Lei nº 14.133/2021; art. 44, VII, do Decreto Estadual (PI) nº 21.872/2023",
  "fontes_equivalentes": ["SINCIN3-P..", "CNMP-PP-..", "TAPP-D-.."],
  "template": { "inconsistencia": "...", "acao": "...", "sugestao": "..." },
  "maturidade": "ponto_de_atencao",
  "versao": "1.0"
}
```

> Os valores de `numero_roteiro`, fundamentação e fontes equivalentes do exemplo são ilustrativos do formato; a vinculação efetiva será apurada na Fase 4.

---

## ALERTA DE CONFORMIDADE

1. **Valores legais desatualizados em instrumento de IA.** O `SKILL.md` em uso contém limites da dispensa superados. Enquanto não corrigido (S-01), qualquer análise conduzida com base nele pode validar enquadramento com parâmetro incorreto — *risco de apontamento pelo TCE-PI/CGE-PI* e de responsabilização (art. 73 da **Lei nº 14.133/2021**).
2. **Vigência iminente de ato de designação.** A **Portaria PGJ/PI nº 5644/2025** (Agentes de Contratação) possui vigência de 12 meses contados de 24/11/2025. Recomenda-se confirmar, antes de 24/11/2026, a edição de ato sucessor e atualizar o registro normativo, sob pena de processos instruídos após essa data citarem designação expirada.
3. **Falsa sensação de cobertura.** Os scripts atuais não verificam coerência entre artefatos nem aritmética; um relatório "sem achados" *não* atesta a higidez do processo nesses aspectos, que respondem pela maior parte das devoluções reais.
4. **Dependência de regex.** Há falsos positivos conhecidos no modo `ausente`; todo achado automatizado deve ser conferido manualmente no trecho do artefato antes de integrar ofício, conforme a prática já adotada.
5. **Prevalência normativa sobre prazos de cotação.** A parametrização do prazo de validade das cotações (IN SEGES/ME nº 65/2021 × Decreto Estadual PI nº 21.872/2023) está marcada como [INFORMAÇÃO A CONFIRMAR] e deve ser validada com a Assessoria Jurídica antes da implementação do motor aritmético.
