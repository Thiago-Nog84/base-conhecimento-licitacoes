# Pendências (em ordem)

Situação em 2026-10-03 (fim do dia): dos 486 PDFs que estavam sem .md, **439 já têm**:
- 155 receberam cópia de um .md equivalente;
- 20 foram convertidos no piloto;
- 264 foram convertidos nos lotes.

Faltam 47: os 46 infográficos, excluídos por decisão do usuário, e 1 PDF corrompido. Esse PDF, a Portaria Nº 106/2025, foi para a Lixeira em 2026-10-05, a pedido do usuário, por estar fora do escopo da base (HISTORICO, etapa 17).

Depois disso, o `MJR n56 - 2025 - Substituição de Marca` (um dos 20 do piloto) foi excluído a pedido do usuário, com o PDF e o .md, porque continha uma escala de plantonistas e não uma MJR. As 4 cópias idênticas no `E:` também foram apagadas. Depois, o histórico do Git foi reescrito para tirar esse .md e o Livro "ETP e TR com ChatGPT" de todos os commits. Ver HISTORICO, etapas 10 e 11.

Em 2026-10-04, o grupo A dos `Downloads` (21 arquivos) foi movido para a mestra. Os 8 normativos do grupo foram convertidos no lote 07, e os boletins Guia Lici 06 a 08/2026 foram preenchidos no consolidado. Ver HISTORICO, etapa 12.

Em 2026-10-05, os 24 arquivos do grupo B dos `Downloads` (material de trabalho da CLC) foram movidos para a mestra. No lote 08, foram convertidos 26 arquivos, entre eles o primeiro conjunto de .docx e .xlsx da base, que passou por anonimização e enriquecimento antes de ir para o clone. Ver HISTORICO, etapa 13.

Ainda em 2026-10-05, 40 arquivos do grupo C dos `Downloads` foram movidos para a mestra: dossiê de Suprimento de Fundos, curso Zênite, material didático e documentos do projeto. Também foram gerados 2 modelos de ARP a partir de peças do SEI. O lote 09 converteu 39 arquivos, dos quais 15 ficam fora do GitHub por serem obras comerciais. As 5 cópias da escala de plantonistas (grupo E) foram para a Lixeira. Ver HISTORICO, etapa 14.

## 1. Conversão em lote (concluída)
`montar_lotes.py` separou **265 PDFs em 6 lotes**. Ficaram fora 46 infográficos (`lotes\fora_dos_lotes.csv`).
| Lote | PDFs | Páginas | Situação |
|---|---|---|---|
| 01 | 50 | — | **concluído**: 50/50 OK (commit `60a6cfd`) |
| 02 | 50 | — | **concluído**: 50/50 OK (commit `597be85`) |
| 03 | 50 | — | **concluído**: 50/50 OK (commit `72a2b7f`) |
| 04 | 50 | 450 | **concluído**: 49/50 OK; 1 PDF corrompido, excluído depois (etapa 17) (commit `965edc9`) |
| 05 | 50 | ≈10.260 | **concluído**: 50/50 OK, com OCR total ou parcial (commit `aa60a61`) |
| 06 | 15 | ≈1.060 | **concluído**: 15/15 OK |
| 07 | 8 | — | **concluído**: 8/8 OK; normativos do grupo A dos Downloads, enriquecidos com ementa (etapa 12) |
| 08 | 26 | — | **concluído**: 26/26 OK; grupo B dos Downloads (22 .docx, 2 .xlsx e 2 PDFs), anonimizados e enriquecidos (etapa 13) |
| 09 | 39 | — | **concluído**: 39/39 OK; grupo C dos Downloads (31 PDFs, 6 de Office, 1 .doc, 1 .md), anonimizados e enriquecidos; 15 só no clone local (etapa 14) |
| 10 | 2 | — | **concluído**: 2/2 OK; Atos PGJ 1.106/2021 e 1.480/2025, enriquecidos. O .md do 1.480 substituiu, com backup, o .md que misturava trechos de DOE (etapa 20) |
| 11 | 1 | — | **concluído**: 1/1 OK; Ato PGJ 1.471/2025 (PDF baixado do SEI pelo usuário), enriquecido. Substituiu, com backup, o .md antigo sem PDF (etapa 24) |
| 12 | 2 | — | **concluído**: 2/2 OK; Atos PGJ 462/2013 (PDF incluído pelo usuário; o .md tinha lixo binário) e 1.383/2024 (o .md era a página do DOE com quatro atos), enriquecidos. Substituíram, com backup, os .md antigos (etapa 25) |

Quatro obras comerciais dos lotes 05 e 06, todas com "proibida a reprodução", foram convertidas normalmente, mas o `.gitignore` as deixa fora do GitHub: Storytelling com Dados, Manual de Contratação de TIC (Editora Fórum), A Nova Lei de Licitações Esquematizada e a apostila do curso Zênite de Habilitação. A varredura que as encontrou está em `controle/lotes/varredura_licenciados.csv`. No lote 09, a mesma regra valeu para os 11 arquivos do curso Zênite "Imersão em Contratações Diretas" e para 4 obras sobre suprimento de fundos e custo de licitação (MPF 2ª ed., Negócios Públicos e Sollicita).

Procedimento usado em cada lote, que vale também para PDFs novos: `python rodar_lote.py NN`, conferir `lotes\qa_lote_NN.csv` (abaixo de 0,90 de cobertura, olhar as palavras ausentes), verificar que `git status` não lista PDFs e fazer commit/push.

**Próximo passo sugerido:** uma revisão por amostragem dos .md convertidos, feita pelo usuário (por exemplo, 1 por pasta), antes de usar a base em treino.

## 2. Decisões do usuário em aberto
- Os 15 pares `SCORE_BAIXO_CONFERIR`: confirmar quais são o mesmo documento (prováveis: Decreto 11.320/2004, Portaria PGJ 5644/2025, Lista de Verificação SGC TJPI, `merged 2024.pdf`). Já foram resolvidos o par do Ato PGJ 1.480/2025 (etapa 20) e os dos Atos PGJ 1.383/2024 e 1.449/2024 (etapa 25).
- **Origens da etapa 5 que ficaram na mestra:** os .md copiados para o nome do PDF em 03/10 (`log_copia_md.csv`) continuam também no lugar de origem, só na mestra (≈170; `carregar_repo.py` os pula, e o índice não os liga). Exemplo: `Biblioteca_Manuais_e_Cursos/Portaria SEGES-ME 8678.2021 - Governanca das Contratacoes Publicas Federais.md`. Proposta: gerar a lista pelo log, conferir que cada origem ainda é idêntica à cópia (separar as que mudaram), mostrar ao usuário e, com aprovação, mandar as idênticas para a Lixeira com registro.
- PDFs duplicados entre si: `SEI_TJPI_-_6640734_-_Provimento.pdf` e `SEI_TJPI - 6640734 - Provimento 13.2025...pdf`; PCA 2026 v2.0 × v3.0.
- `Federal - CF - 88_2.md` e `Federal - Lei 14133.2021_2.md` têm conteúdo diferente do arquivo de mesmo nome sem `_2`.
- 11 arquivos soltos em `03_MPPI` e 1 em `05_TCE_PI`; pastas antigas possivelmente vazias na mestra.
- Os .md consolidados do TCE-PI (`01_..._TCE_PI.md` a `08_..._TCE_PI.md`): manter junto com os .md individuais das sessões?
- **Materiais dos Downloads (retomar aqui):**
  - Os grupos A, B, C e E estão concluídos (etapas 12 a 14). Resta o **grupo D** ("não integrar"), com a análise em `C:\Users\thiagonogueira\Claude\recomendacao_downloads.md`. Nada dele entra na base. Falta só o usuário decidir o que fazer, no próprio Downloads, com os arquivos que têm dados pessoais e com os resíduos de páginas salvas.
  - Falta o usuário confirmar até onde vai a anonimização do lote 08: além do próprio nome, foram trocados o nome de um colega, os fiscais de um roteiro e uma empresa (etapa 13). Para reverter, use os backups em `backup_md\anonimizacao\2026-10-05\`.
  - Ficaram no Downloads, por decisão da etapa 14: o Ato PGJ 350/2013 (revogado), a cópia `cbc,+XXIICongresso_artigo_0312.pdf`, as peças originais do C5, a planilha do C6 e os 8 arquivos do C2 que já estavam na base. Se o usuário quiser o PDF ao lado de algum desses 8 .md, dá para levá-lo à mestra com o mesmo procedimento.
- A pasta `01_Normativos_Vigentes/04_CNMP/POP's Contratação Direta` guarda POPs do MPPI (códigos POP-CLC-xx), não do CNMP. Mudar a pasta de lugar? Os 3 POPs do grupo B também foram para essa pasta, por decisão do usuário, até que essa mudança seja decidida.
- **Bundles com o histórico antigo:** `C:\Users\thiagonogueira\Claude\backup_git_antes_recomeco_2026-10-07.bundle` (etapa 27) guarda os 42 commits anteriores, com o nome do usuário e de servidores nas versões antigas. Falta decidir até quando guardá-lo. O pedido de coleta de lixo ao Suporte do GitHub, para apagar os commits antigos do cache, é com o usuário.
- **Modelos de TAPPC para TIC e engenharia:** a Assessoria para Pareceres recomendou avaliar checklists próprios para esses objetos (etapa 28). Decidir se vale fazer, a partir do TAPPC ASSGERLICT e dos modelos AGU de TIC.
- `C:\Users\thiagonogueira\Claude\backup_git_antes_reescrita.bundle` ainda contém o MJR n56 e o Livro. Falta decidir se vai para a Lixeira. O pedido de coleta de lixo ao Suporte do GitHub é com o usuário (etapa 11).

- **Índice por fase (aplicado em 2026-10-05):** `00_Indice_por_Fase_da_Contratacao.md` está na raiz da mestra e do clone (452 links, 5 só locais), gerado por `docs/controle/indice/gerar_indice_por_fase.py` a partir do mapa curado. README, AGENTS e PIPELINE foram atualizados. Em aberto, por decisão do usuário:
  - campo `fases:` no front-matter, para gerar o índice a partir dos próprios arquivos (mexe em centenas de .md; exige autorização e backup);
  - auditoria do front-matter dos enriquecidos, cujos erros de `assunto` e ementa estão no Apêndice A.2 do índice;
  - tratamento dos arquivos com conteúdo trocado ou duplicados (Apêndices A.1 e C): renomear, retirar ou refazer o OCR, e mover para pastas os 5 arquivos soltos na raiz. Do A.1, já estão resolvidos os Atos PGJ 1.228/2022 (etapa 19) e 1.480/2025 (etapa 20), o infográfico com nome de Portaria 8.678 (etapa 21), o Manual IRB/Ibraop com nome de Resolução TCE-PI 19/2024 (etapa 22), o Acórdão TCE-PI 300/2025, que estava como "n3001" com o DOE inteiro (etapa 23), e o Ato PGJ 1.471/2025, que estava como "Regulamenta Suprimento de Fundos" e na verdade altera o Ato 823/2018 (etapa 24, PDF obtido); faltam 3. Do Apêndice C, os duplicados dos Atos PGJ 1.382, 1.383, 1.413 e 1.449/2024 e do Ato 479/2014 foram resolvidos na etapa 25. Obter o Regimento Interno do TCE-PI, Resolução 13/2011 (lacuna do Apêndice B). Decidir se o histórico do git deve ser reescrito para tirar o .md antigo do "n3001" (DOE TCE-PI 152/2025 inteiro, com nomes de aposentados e pensionistas, publicado desde a carga inicial `70aa07e`), como na reescrita de 03/10;
  - lacunas do Apêndice B: modelo do MPPI de decisão de recurso e de termo de homologação, regulamento de sanções, manual de riscos, caderno de logística 2024, IN SGD 94/2022 e lei federal da LGPD.
  - A cada lote, acrescentar ao `mapa_indice.py` os arquivos que cabem numa fase e regerar o índice (`--aplicar --substituir`, com autorização).

## 3. Fora do escopo atual (decidir depois)
- ≈1.825 PDFs de processos SEI em `CLC\Assessoria de Compras` (podem conter dados pessoais; não versionar).
- ≈12 mil PDFs em `E:\Thiago\Dev\...\Mapeamento TCE\downloads`.
- 252 itens "DECIDIR" que ficaram fora da mestra.
- A duplicação manual para o `E:` pode ser substituída por um `git clone` deste repositório.
