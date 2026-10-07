# Base de Conhecimento — Licitações e Contratos (CLC)

Normativos, jurisprudência, modelos e manuais sobre licitações e contratos, em **Markdown**, para uso por pessoas e por IA.

> **Para achar um arquivo, comece pelo [Índice por fase da contratação](00_Indice_por_Fase_da_Contratacao.md):** do planejamento à liquidação, com normas, modelos, manuais e jurisprudência de cada fase.

> **Para IAs e colaboradores:** comece por [AGENTS.md](AGENTS.md) (regras), [docs/HISTORICO_E_DECISOES.md](docs/HISTORICO_E_DECISOES.md), [docs/PENDENCIAS.md](docs/PENDENCIAS.md) e [docs/PIPELINE.md](docs/PIPELINE.md). Scripts em `ferramentas/`.

## Convenções
- Cada `.md` tem o **mesmo nome e a mesma pasta** do arquivo de origem (PDF, .docx, .xlsx ou .doc).
- Os **originais não são versionados** (`.gitignore` bloqueia PDF, .docx, .xlsx e .doc): ficam na pasta mestra do OneDrive e são usados para anexar no SEI. Só o `.md` ao lado vai para o Git.
- **Obras licenciadas ou comerciais** têm o `.md` só no clone local (listado no `.gitignore`) e não vão para o GitHub. No índice, aparecem com a marca *(só local)*.
- Arquivos convertidos trazem front-matter com `arquivo_original`, `hash_pdf_md5` (ou `hash_arquivo_md5`), `paginas`, `metodo` e `convertido_em`. Os enriquecidos trazem também `tipo`, `numero`, `ano`, `orgao`, `ambito`, `assunto`, `status` e `tags`.
- O front-matter enriquecido tem erros conhecidos de `assunto` e ementa em alguns arquivos. O índice descreve cada arquivo pelo **corpo**, não pelo cabeçalho.

## Estrutura
- `00_Indice_por_Fase_da_Contratacao.md` (na raiz): mapa por fase da contratação, gerado por script.
- `01_Normativos_Vigentes/{01_Federal,02_Estadual_PI,03_MPPI,04_CNMP,05_TCE_PI,06_TJPI}/<tipo>`
- `02_Jurisprudencia_e_Orientacoes`, `03_Modelos_e_Minutas`, `04_Sistemas_e_Catalogos`
- `05_Doutrina_e_Biblioteca`, `06_Paineis_e_Contratos_Historicos`, `SIte_PGE_PI`
- `00_Ferramentas_e_Scripts_Analise`: prompts e roteiros de análise com IA.

## Fonte
Pasta mestra: `OneDrive - mppi.mp.br\CLC\01_Processos_e_Aquisicoes\Base de Conhecimento - Thiago`.
