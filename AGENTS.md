# Instruções para agentes de IA

Este repositório é uma **base de conhecimento em Markdown sobre licitações e contratos públicos** (Lei 14.133/2021, normas do Piauí, MPPI, CNMP, TCE-PI, TJPI), mantida por [nome do usuário] (CLC/MPPI). Qualquer IA que continue o trabalho deve ler este arquivo primeiro e, em seguida:

1. [`docs/HISTORICO_E_DECISOES.md`](docs/HISTORICO_E_DECISOES.md): o que já foi feito e por quê.
2. [`docs/PENDENCIAS.md`](docs/PENDENCIAS.md): o que falta, em ordem.
3. [`docs/PIPELINE.md`](docs/PIPELINE.md): como rodar os scripts de `ferramentas/`.
4. [`00_Indice_por_Fase_da_Contratacao.md`](00_Indice_por_Fase_da_Contratacao.md): mapa dos arquivos por fase da contratação. É a melhor porta de entrada para consultar a base.

## Objetivo
- Cada PDF de interesse deve ter um `.md` correspondente (mesmo nome, mesma pasta), para uso por IA.
- Os PDFs continuam existindo porque são anexados em processos no SEI.

## Onde as coisas ficam
| Local | Papel |
|---|---|
| `C:\Users\thiagonogueira\OneDrive - mppi.mp.br\CLC\01_Processos_e_Aquisicoes\Base de Conhecimento - Thiago` | **Pasta mestra** (fonte da verdade: PDFs + MDs) |
| `D:\00_ATIVO\Dev\base-conhecimento-licitacoes` | Clone deste repositório (MDs versionados + PDFs locais, ignorados pelo Git), na SSD portátil desde 2026-10-07. A letra da SSD pode mudar em outro PC |
| `https://github.com/Thiago-Nog84/base-conhecimento-licitacoes` | Repositório **privado** (só `.md` e documentação) |
| `C:\Users\thiagonogueira\Claude` | Pasta de trabalho: scripts originais e CSVs de controle (cópias em `ferramentas/` e `docs/controle/`) |

**Consultar no clone, alimentar pela mestra.** Todo arquivo novo ou corrigido entra primeiro na mestra e chega ao clone por `carregar_repo.py`, que copia num sentido só e não sobrescreve. Não crie nem edite `.md` de conteúdo direto no clone: a mestra ficaria sem ele, e uma correção feita só no clone se perde. Se for preciso corrigir um `.md` já carregado, corrija nos dois lugares, com backup. Os documentos do próprio projeto ficam em [`docs/projeto/`](docs/projeto/).

## Regras invioláveis
1. **Nunca apagar nem renomear PDFs.** Apenas criar `.md` ou copiar/mover com log reversível (CSV origem → destino).
2. **Listar e pedir autorização ao usuário** antes de qualquer movimentação ou ação em lote nova. O usuário responde item a item.
3. **Nunca sobrescrever um `.md` existente.** A única exceção é com autorização explícita do usuário e backup prévio, como na substituição do piloto v1 → v2 (`log_substituicao_piloto_v2.csv`) e na troca do .md do Ato PGJ 1.480/2025 (`docs/controle/log_substituicao_md.csv`).
4. **PDFs, .doc, .docx e .xlsx não vão para o GitHub** (o `.gitignore` bloqueia esses formatos; só o `.md` ao lado é versionado). Não versionar documentos de processos SEI nem arquivos com dados pessoais.
5. Copiar (não mover) a partir do `E:\Thiago\Dev`; conferir cópias por hash MD5.
6. O clone fica **fora do OneDrive** (o OneDrive corrompe a pasta `.git`).
7. **Obras licenciadas ou comerciais** (livros com licença de uso individual, material de cursos pagos, publicações com "todos os direitos reservados") ficam só no clone local: o `.md` é listado no `.gitignore` **antes** de `carregar_repo.py`. Na dúvida, pergunte ao usuário antes do commit.
8. **Infográficos não são convertidos.** São eles a pasta `Infograficos_Zenite` e os PDFs de uma página com altura maior que 3× a largura.
9. **Anonimizar o material de trabalho antes de versionar.**
   - No `.md`, nomes e matrículas de servidores e fiscais, e empresas ligadas a casos concretos, viram marcadores: `[nome do servidor]`, `[matrícula]`, `[nome do fiscal]`, `[nome da empresa]`.
   - A troca é feita com `anonimizar_md.py`, com backup. O original não é alterado.
   - O arquivo de regras e o log de anonimização ficam fora do Git.
   - Signatários de atos oficiais, números de processo e e-mails institucionais de setor são mantidos, pelo precedente das MJRs.
   - Exceção: atos oficiais publicados (portarias, PCA, atas assinadas) mantêm os nomes de servidores; o nome do usuário vai como marcador (`[nome do usuário]`, `[matrícula]`). Documentos internos e modelos (POPs, DFDs, roteiros, ofícios de processo SEI) são anonimizados, inclusive o e-mail pessoal do servidor (`[e-mail do servidor]`).
   - Nomes de arquivo também não levam o nome do usuário (a pasta mestra, fora do Git, é a exceção).
   - Na dúvida, pergunte ao usuário.

## Convenções
- **Índice por fase:** `00_Indice_por_Fase_da_Contratacao.md` (raiz) é **gerado** por `docs/controle/indice/gerar_indice_por_fase.py` a partir do mapa curado `mapa_indice.py`. Não edite o índice à mão. Arquivo novo só aparece nele se for incluído no mapa, com a descrição lida no corpo (o front-matter enriquecido tem erros de `assunto` e ementa). Para trocar o índice, use `--aplicar --substituir`, com autorização: o script faz backup e grava na mestra e no clone.
- Front-matter dos `.md` convertidos de PDF: `arquivo_original`, `hash_pdf_md5`, `paginas`, `metodo`, `convertido_em`, `fonte`.
- De .docx/.xlsx/.doc: `arquivo_original`, `hash_arquivo_md5`, `formato`, `planilhas` (só .xlsx), `metodo`, `convertido_em`, `fonte`.
- Os enriquecidos (lotes 07 em diante) recebem também `tipo`, `numero`, `ano`, `orgao`, `ambito`, `assunto`, `status`, `tags`, o título e o bloco "Ementa / Síntese".
- Fim de linha LF (`.gitattributes`); `core.longpaths=true` no clone (há nomes de arquivo muito longos).
- Taxonomia: `01_Normativos_Vigentes/{01_Federal,02_Estadual_PI,03_MPPI,04_CNMP,05_TCE_PI,06_TJPI}/<tipo>`, com tipos `Constituicao, Leis, Decretos, Instrucoes_Normativas, Resolucoes, Portarias, Acordaos_Pareceres_Orientacoes, Atos, Manuais_e_Guias_Tecnicos, Outros_Normativos`. Demais pastas: `02_Jurisprudencia_e_Orientacoes`, `03_Modelos_e_Minutas`, `04_Sistemas_e_Catalogos`, `05_Doutrina_e_Biblioteca`, `06_Paineis_e_Contratos_Historicos`, `SIte_PGE_PI`. Na mestra existe ainda `_DUPLICADOS_para_arquivar` (quarentena, nunca copiada para cá).

## Cuidados técnicos (Windows)
- Caminhos com mais de 260 caracteres: usar o prefixo `\\?\` (os scripts têm a função `lp()`). O prefixo não resolve nomes curtos 8.3, como `THIAGO~1`; use sempre o caminho completo.
- PowerShell 5.1: `LP` é alias (não usar como nome de função); variáveis não diferenciam maiúsculas.
- Arquivos do OneDrive podem ser placeholders: ler dispara download.
- Ao editar scripts, use um editor ou ferramenta de escrita de arquivo; *heredocs* no Bash removem barras invertidas e já corromperam scripts.
- Idioma de trabalho: português do Brasil.
