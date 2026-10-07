
## Apêndice A — Pontos de atenção na base

Achados da conferência de conteúdo feita para montar este índice. Salvo o que a própria linha indica como resolvido, nenhum arquivo foi alterado; as correções dependem de autorização.

### A.1 Conteúdo diferente do nome do arquivo (não linkados no índice)

| Arquivo | O que o corpo traz de fato | Sugestão |
|---|---|---|
| `01_Federal/Portarias/Portaria Fedral - n8678.0 - 2021.md` | Infográfico do Compras.gov.br ("Como vender para o Governo"), também no PDF. A Portaria SEGES/ME 8.678/2021 de verdade está em `Biblioteca_Manuais_e_Cursos/Manuais/` | Resolvido em 2026-10-06: PDF e .md foram para a Lixeira, por estarem fora do escopo |
| `03_MPPI/Atos/Ato PGJ 1480.2025 - Retira CONINT da Fase Interna.md` | Trechos dos DOE MPPI 985/2021 (Portaria PGJ 2980/2021, Ato 1.106/2021) e 1730/2025 (Ato 1.480/2025 e outros atos) | Resolvido em 2026-10-05: o .md passou a ser a conversão do PDF oficial do Ato 1.480/2025, e o par `Ato PGJMPPI - n1480.0 - 2025` foi para a Lixeira; o Ato 1.106/2021 ganhou PDF e .md próprios (seção 4) |
| `05_TCE_PI/Resolucoes/Resolução TCE - n19.0 - 2024.md` | Manual de auditoria de obras do IRB/IBRAOP (2018), também no PDF | Resolvido em 2026-10-06: par renomeado para `Manual IRB-Ibraop - Auditoria de Obras Publicas e Servicos de Engenharia (2018)`, movido para `Biblioteca_Manuais_e_Cursos/Manuais/` e com cabeçalho corrigido (seção 13) |
| `02_Jurisprudencia_e_Orientacoes/Acordaos_TCE_PI/Acórdão TCE - n3001 - 2025.md` | Edição do DOE do TCE-PI de 15/08/2025, não o acórdão | Resolvido em 2026-10-06: par renomeado para `Acordao TCE-PI 300.2025 - 1a Camara - Irregularidades Pregao e Adesao ARP (DOE 152.2025)`; o PDF segue sendo o DOE inteiro e o .md traz só os Acórdãos 300 e 300-A/2025 (seção 13) |
| `03_MPPI/Atos/Ato PGJ 1228.2022 - Suprimento de Fundos (Texto Original).md` | Redação original do Ato 1.228/2022 (15/09/2022), sem as alterações dos Atos 1251 e 1252/2022 | Resolvido em 2026-10-05: renomeado (antes `0228.2022`) e marcado como histórico; a versão em vigor é o compilado (seção 16) |
| `03_MPPI/Ato PGJ 1471.2025 - Regulamenta Suprimento...` | Na verdade altera o Ato 823/2018 (Diretor de Sede) | Resolvido em 2026-10-06: PDF oficial obtido; par `Atos/Ato PGJ 1471.2025 - Altera Ato 823.2018 - Diretor de Sede como Agente Suprido`, com o .md convertido do PDF; o Ato 823 ganhou aviso sobre o inciso XXV |
| `Biblioteca_Manuais_e_Cursos/Manual TCU - 2016.md` | OCR ilegível | Refazer o OCR |
| `Biblioteca_Manuais_e_Cursos/Manuais/Nota Técnica N° 18_2026 - Leis.org.md` | Engorda de praia, fora de escopo | Retirar da base |
| `02_Estadual_PI/Leis/Lei Estadual 6782.2016 - Estatuto dos Servidores Publicos do Piaui.md` | Lei 6.782/2016, processo administrativo (o nome e a ementa dizem "servidores") | Duplicata das outras duas versões |

### A.2 Front-matter com assunto ou ementa errados

O índice usa o assunto real, lido no corpo. Arquivos em que o front-matter diverge (assunto real entre colchetes):

- Lei Estadual 7612 "Normas de Gestão e Fiscalização" [gestão de imóveis do Estado]
- Decreto 23.865 "Regulamento de Contratações" [unificação da plataforma de compras]
- Lei Estadual n7.482 [pregão eletrônico e dispensa eletrônica no Piauí]
- Decreto 22.822 [patrocínio]
- IN CGE 01/2013 [obras]; IN CGE 01/2015 [tomada de contas especial]; IN SEFAZ 01/2021 [Nota Patrimonial]
- Portaria n0012024 [Conjunta SEFAZ/SEPLAN, convênios]
- Res. TCE n20/2024 [manual de auditoria financeira do TCU]; Res. TCE n37/2024 [medidas corretivas, duplicata]
- Decreto 20.096 [credenciamento em unidades de saúde]

Sugestão: uma auditoria do front-matter dos arquivos enriquecidos, comparando `assunto` e ementa com o corpo, com backup antes de qualquer alteração.

### A.3 Fora do escopo (não linkados de propósito)

Decreto 15.943/2015 (regime anterior); Res. TCE n10/2020, n9/2025 e 008/2026; Manual de Padronização de Decisões do TCE-PI; manuais da OPA; Transcrição; Roteiro Pedagógico; cursos do BID; Lei Orgânica do MPPI, plano do CEAF, Res. CPJ 08/2025; Portarias de designação 2396, 2864, 2918 e 3172; Atos 0479, 0823, 1079, 1441 e 1599; LC 13.94; Decretos 17031 a 22249 não mapeados; Parecer AGU 00002/2026 (acordos com entidades privadas).

## Apêndice B — Lacunas

- **Fase 4 (riscos):** não há manual de gestão de riscos do MPPI nem do Estado.
- **Fase 5 (pesquisa de preços):** o Caderno de Logística é de 2017; faltam o caderno de 2024 e o manual do STJ.
- **Fase 10 (recursos e homologação):** fase mais fraca; falta modelo do MPPI de decisão de recurso e de termo de homologação.
- **Fase 15 (sanções):** falta regulamento de sanções do MPPI e um manual de sanções.
- **TIC:** falta a IN SGD 94/2022.
- **LGPD:** falta a lei federal (só há o decreto estadual).
- **TCE-PI:** falta o Regimento Interno do TCE-PI (Resolução TCE/PI 13/2011).

## Apêndice C — Duplicados

Não linkados quando há versão canônica; a canônica é a que o índice usa.

- **Atos PGJ 1382, 1383, 1413 e 1449/2024:** resolvido em 2026-10-06: os pares `Ato PGJMPPI - n...`, com PDF idêntico ao do arquivo nomeado, foram para a Lixeira; o mesmo aconteceu com a duplicata `Ato PGJ 0479.2013 - ...` do Ato 479/2014. Nas Portarias 3315 e 5644 ainda existem o arquivo nomeado e o `n...`. (Em alguns casos o índice usa a versão `n...` porque o nome do outro cobre outro assunto; ver cada link.)
- **Decreto 11.320/2004** em duas versões; **INs do TCE-PI** (02/2026, 06/2017 e 07/2021) existem em `02_Estadual_PI` e em `05_TCE_PI` (o índice usa a de `05_TCE_PI`).
- **PCA 2026** em três lugares (`PCA 2026/`, `PCA_2026/` com versões 2.0 e 3.0, e `06_Paineis`); **Provimento TJPI 13/2025** em três arquivos.
- **Lei Estadual 6.782/2016** em três arquivos; **IN 81 (TR 2)**, **Lei 14.133 (_2)** e **CF 88 (_2)** com conteúdo diferente do arquivo sem `_2`.
- **Manuais em duplicata:** Dispensa Eletrônica (versão padrão, (3) e Manual Operacional); TRT-2 (três); Compras públicas para inovação (duas); Zênite 5 Erros (dois); Palestra IA (duas); Contratos.gov (1.39.0, 1.40.0 na raiz, 2.14.0 e `manual-contratos-gov-br-nova-versao` em duas pastas); MPBA Cadastro (dois); PGE-PI Lista de Pequeno Valor (dois); Tutorial de contratações presenciais (dois); Manual TJPI (dois); Custo-Benefício (dois, prováveis); Tutorial PCA 2026 (2) × 2027 (o cabeçalho da versão 2027 diz 2026).
- **Arquivos na raiz que pertencem a uma pasta:** os três "Manual completo", `TEMPORRIO...1.40.0...md` e `SEI_TJPI_-_6640734_-_Provimento.md`.

## Apêndice D — Decisões para aprovar

1. **Local do índice.** Recomendo `00_Indice_por_Fase_da_Contratacao.md` na raiz da pasta mestra, levado ao clone por `carregar_repo.py`. Não crio nada na mestra nem no clone antes de aprovado.
2. **Um arquivo ou um por fase.** Um arquivo só é mais fácil de manter e de dar a uma IA; um por fase (como no repositório do colega) deixa cada leitura mais curta.
3. **Arquivos só locais.** Hoje marcados com *(só local)*. Alternativa: tirá-los do índice versionado, para o GitHub não listar títulos de obras licenciadas.
4. **Campo `fases:` no front-matter** (v2). Permitiria gerar o índice a partir dos arquivos, mas mexe em centenas de .md e exige autorização e backup.
5. **README.** Corrigir (docx, xlsx e doc também não são versionados; obras licenciadas ficam só no local) e linkar o índice.
6. **Documentação.** Atualizar `PIPELINE.md` e `AGENTS.md` para incluir a regeneração do índice a cada lote.
7. **Auditoria do front-matter** (A.2) e **tratamento dos arquivos do A.1** (renomear, retirar ou refazer o OCR).
8. **Itens já em aberto:** Roteiro - Credenciamento (criado direto no clone), anonimização estendida do lote 08, renomear o Ato PGJ 0228.2022 e mover os PDFs dos 8 arquivos do dossiê.
