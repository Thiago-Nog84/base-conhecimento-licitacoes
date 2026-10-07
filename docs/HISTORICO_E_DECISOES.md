# Histórico e decisões

Registro cronológico do trabalho, com as decisões do usuário. Os CSVs citados estão em [`controle/`](controle/).

## Etapa 1 — Mapeamento (2026-10-03)
- Pastas de origem: `C:\Users\thiagonogueira\OneDrive - mppi.mp.br` (≈2.304 PDFs) e `E:\Thiago\Dev` (≈12,9 mil PDFs, quase todos em `Mapeamento TCE\downloads`).
- Ideia do usuário: concentrar tudo numa **pasta mestra** e depois duplicar manualmente.
- Pasta mestra definida: `OneDrive - mppi.mp.br\CLC\01_Processos_e_Aquisicoes\Base de Conhecimento - Thiago`, organizada **por tipo de normativo e por esfera**.

## Etapa 2 — Movimentação para a mestra
Plano em `plano_movimentacao.csv` / `plano_movimentacao_resumo.md`. Decisões do usuário:
- Mover os arquivos novos e reorganizar os existentes por tipo: **sim**.
- Duplicados (por hash) vão para `_DUPLICADOS_para_arquivar`, sem apagar: **sim**.
- Arquivos do `E:` são **copiados**; originais ficam lá: **sim**.
- 252 itens "DECIDIR" (Planejamento, Cursos, Projetos, POPs, IA, Annona) ficam onde estão: **sim**.
- Conflitos de nome recebem sufixo `_2`: **sim**.

Resultado (`log_movimentacao.csv`): 154 reorganizados, 298 copiados do `E:` (0 divergências de hash), 208 duplicados em quarentena, 9 ignorados.

## Etapa 3 — Pareamento PDF ↔ MD
- Por nome (`mapa_pares_pdf_md.csv`): só 9 pares na mesma pasta; **486 PDFs sem .md**; 510 .md sem PDF.
- `mapa_pares_pdf_md_v2.csv`: os 486 com tipo (405 texto, 56 escaneados, 25 com caminho > 260 caracteres).
- Ferramentas instaladas: `pymupdf4llm` e Tesseract 5.4 (eng, osd, **por**) em `%LOCALAPPDATA%\Programs\Tesseract-OCR`.

## Etapa 4 — Comparação por conteúdo
Pedido do usuário: "ler o conteúdo dos PDFs e .md para identificar quais são iguais".
- Método (`ferramentas/comparar_conteudo.py`): até 8 páginas por PDF (OCR em até 3 páginas sem texto), *shingles* de 4 palavras normalizadas, índice invertido sobre todos os .md da mestra. Score = fração do PDF contida no melhor .md.
- Resultado (`comparacao_conteudo_pdf_md.csv`): **260 IGUAL** (≥ 0,60), **98 PROVAVEL_REVISAR** (0,25–0,60), **120 DISTINTO**, **8 SEM_TEXTO_SUFICIENTE**.
- Nenhum par IGUAL tinha o mesmo nome. Por isso o pareamento por nome falhava.

## Etapa 5 — Cópia dos .md equivalentes
Filtro (`plano_copia_md_pares_iguais.csv`): score ≥ 0,90 **e** .md usado por um único PDF → **155 OK**.
Ficaram de fora 105:
- 90 em `MD_USADO_POR_VARIOS_PDFS`: sessões do TCE-PI que caem em .md consolidados (`0X_..._TCE_PI.md`), além de PDFs duplicados (Provimento TJPI 13/2025, PCA 2026 v2/v3, Manual TJPI).
- 15 em `SCORE_BAIXO_CONFERIR` (0,67–0,89), com falsos positivos claros: `PCA 2026.pdf` → `PCA 2025.md`; `Portaria PGJ 3315/2025` → `Portaria PGJ 1040/2025`.

Decisão do usuário: **copiar os 155** (não renomear). O .md de origem foi preservado. Log: `log_copia_md.csv`, 155/155 com hash conferido.

## Etapa 6 — Repositório GitHub
Ideia do usuário: um repositório para usar a base em todos os projetos. Decisões:
- Repositório **privado** `Thiago-Nog84/base-conhecimento-licitacoes`; clone em `C:\Users\thiagonogueira\Dev\base-conhecimento-licitacoes`.
- **Opção A**: o clone espelha a estrutura da mestra com PDFs e MDs lado a lado, mas `*.pdf` está no `.gitignore`. Só os .md vão para o GitHub.
- **Copiar** (não mover) da mestra; originais permanecem no OneDrive.
- Escopo da carga: todos os .md da mestra (exceto quarentena e exceto os 155 .md de origem já copiados com o nome do PDF, para não duplicar) e os PDFs com .md equivalente.

Carga inicial (`ferramentas/carregar_repo.py`, log `log_carga_repo.csv`): 519 .md + 164 PDFs locais. Commit `70aa07e`.

## Etapa 7 — Piloto de conversão
- 20 PDFs DISTINTOS com texto, de 15 pastas diferentes (`lista_piloto.csv`, gerada por `ferramentas/montar_piloto.py`).
- `ferramentas/converter_pdf_md.py`: 20/20 OK (`log_conversao.csv`). Métodos: `pymupdf4llm` em 14; texto simples em 6 (o markdown tinha artefatos de negrito); OCR complementar em 4.
- Achado: `MJR n56 - 2025 - Substituição de Marca.pdf` contém uma escala de plantonistas (junho/2026), não uma MJR. O PDF parece estar com o nome errado, e o usuário precisa conferir.
- **Aguardando validação da qualidade pelo usuário** antes do lote completo.

## Etapa 8 — Conferência de qualidade e conversor v2
A pedido do usuário ("confira o trabalho apresentado"), os 20 .md foram auditados com `ferramentas/qa_conversao.py`, que compara as palavras do .md com as do PDF e procura artefatos.
- Cobertura de 0,93 a 1,00 em todos: nenhuma perda de conteúdo, UTF-8 correto, front-matter completo.
- Problemas da v1, todos corrigidos na v2 de `converter_pdf_md.py`:
  1. Páginas com OCR eram anexadas **no fim** do .md. Agora ficam na posição original (`page_chunks=True`).
  2. Cabeçalhos e rodapés repetidos (marca d'água do livro 132×, carimbos do DOE, timbres). Agora uma linha com mais de 15 caracteres, fora de tabela, que aparece em pelo menos 40% das páginas é mantida só na primeira ocorrência. Os rótulos curtos de formulário são preservados.
  3. O modo "texto simples" mantinha recuos e espaços de diagramação (1.805 linhas recuadas no guia da AGU). Agora os espaços são colapsados.
  4. Páginas com 5 ou mais glifos sem mapeamento Unicode (`�`) passam a ir para OCR. Caracteres ilegíveis restantes são informados no campo `metodo`.
  5. Páginas muito altas (acima de 32.767 px) têm OCR feito em faixas.
- A v2 foi testada nos mesmos 20 PDFs, numa pasta temporária: 20/20 OK. A cobertura cai para 0,90–0,96 só nos arquivos com cabeçalhos removidos; a lista das linhas removidas foi conferida uma a uma.
- Decisão do usuário: **ignorar os infográficos** (páginas únicas muito altas do Compras.gov e a pasta `Infograficos_Zenite`).
- Achados para o usuário: `MJR n56 - 2025 - Substituição de Marca.pdf` contém uma escala de plantonistas; o Livro "ETP e TR com ChatGPT" é obra licenciada com o e-mail do usuário em cada página. Foi sugerido retirá-lo do GitHub.

## Etapa 9 — Aplicação da v2 e lotes
Decisões do usuário: (1) substituir o piloto pela v2: **sim**; (2) converter os demais em lotes: **sim**; (3) tirar o Livro do GitHub: **sim**.
- `substituir_piloto_v2.py`: 17 .md trocados na mestra e no clone, com hash conferido. Os v1 foram guardados em `C:\Users\thiagonogueira\Claude\backup_piloto_v1\`. Os 3 infográficos ficaram como estavam. Commit `d453b35`.
- O Livro "ETP e TR com ChatGPT" saiu do índice do Git (`git rm --cached`) e entrou no `.gitignore`; o .md continua no clone e na mestra. Ele continuou no histórico até a etapa 11, quando o histórico foi reescrito.
- `montar_lotes.py`: 265 PDFs em 6 lotes; 46 infográficos fora (45 Zênite e 1 tutorial do Compras.gov).
- **Lote 01:** 50/50 OK. O QA mostrou que a remoção de cabeçalhos da v2 apagava conteúdo real em pautas curtas do TCE-PI: "SECRETARIA DE CULTURA DO ESTADO DO PIAUÍ (EXERCÍCIO DE 2024)" e "Interessados: ..." repetidos em várias páginas. **Conversor v2.1:** passou a considerar só as linhas na borda da página e a exigir 75% das páginas em documentos com menos de 10. O teste no piloto e no lote 01 confirmou que todos os cabeçalhos verdadeiros continuam sendo removidos e que nenhuma pauta perde conteúdo.
- Os 18 .md do lote 01 afetados pela mudança foram reconvertidos e substituídos (`substituir_md.py`), com backup em `C:\Users\thiagonogueira\Claude\backup_lote01_regra_antiga\` e log `lotes/log_substituicao_lote01.csv`. O piloto não foi refeito: lá a v2 removeu apenas cabeçalhos verdadeiros, conferidos um a um.
- **Lote 02:** 50/50 OK, cobertura mediana de 0,993. As menores coberturas (0,85–0,90) são das Listas de Verificação da SEFAZ-PI, que perderam só o cabeçalho repetido ("Comissão de Gestão por Resultados…"), o carimbo do DOE e ligaduras tipográficas normalizadas.
- **Lote 03:** 50/50 OK, cobertura mediana de 0,995. As menores coberturas vêm das Listas de Verificação da SEFAZ-PI (cabeçalho e carimbo do DOE) e da Portaria PGJ 3315/2025, onde só sumiu a URL de impressão do SEI no cabeçalho e no rodapé. Os PCAs têm muitas linhas repetidas por causa das linhas de tabela que se repetem; o texto foi preservado.
- **Lote 04:** 49/50 OK, cobertura mediana de 1,00. Os pontos baixos são de novo Listas de Verificação da SEFAZ-PI, com o mesmo cabeçalho removido. Um erro: `2. Portaria Nº 106, de 27 de março de 2025.pdf` está truncado (7 MiB exatos, sem `%%EOF`), e a origem no `E:` também, pois foi copiada com o hash conferido. O caso ficou registrado em PENDENCIAS para o usuário obter uma cópia íntegra.
- **Lote 05:** 50/50 OK, cobertura mediana de 0,981. Notas do QA:
  - **Cobertura 0,0** nos 8 PDFs totalmente escaneados: é esperado, porque o PDF não tem camada de texto para comparar. Todos geraram texto por OCR, de 1,8 mil a 124 mil caracteres.
  - **QDD 2026** (0,79–0,82) e **"50 Erros"** (0,87): só perderam o cabeçalho repetido.
  - **"Compras.gov.br – Novo divulgação… Evento de alteração"** (0,53): a camada de texto do PDF está duplicada e fragmentada ("oeda", "escrição"…), e as palavras inteiras estão todas no .md.
  - **Métrica:** a cobertura do QA conta palavras repetidas e fragmentos. Por isso, cada caso abaixo de 0,90 foi conferido pelas palavras ausentes.
- **Lote 06:** 15/15 OK, todos com cobertura de 0,90 ou mais.
- **Resultado final dos lotes:** 264 de 265 convertidos. Dos 486 PDFs que estavam sem .md, 439 já têm .md. Ficam de fora 46 infográficos, por decisão do usuário, e 1 PDF corrompido.
- **Obras comerciais:** uma varredura dos lotes buscou ISBN, "direitos reservados", licença em nome do usuário e CPF (`lotes/varredura_licenciados.csv`). Pelo mesmo critério já aprovado para o Livro "ETP e TR com ChatGPT", quatro obras com reprodução proibida entraram no `.gitignore`: Storytelling com Dados, Manual de Contratação de TIC (Editora Fórum), NLLC Esquematizada e a apostila Zênite de Habilitação. Continuam versionados o Compilado de Leis da Zênite (distribuição gratuita autorizada), as publicações públicas com ISBN (IPEA, CSJT, CGU, MROSC), os manuais do Banco de Preços e os slides de cursos e palestras, que não trazem nenhuma restrição explícita.

## Etapa 10 — Exclusão do MJR n56 (2026-10-03)
Decisão do usuário: apagar o `MJR n56 - 2025 - Substituição de Marca`, que continha uma escala de plantonistas e não uma MJR, e tirá-lo do GitHub.
- Foram para a Lixeira do Windows (recuperáveis), com MD5 registrado em `C:\Users\thiagonogueira\Claude\log_exclusoes.csv`: o PDF e o .md da mestra, o PDF e o .md do clone e o .md v1 em `backup_piloto_v1\`.
- O .md saiu do GitHub com `git rm` e, na etapa 11, também do histórico.
- Os CSVs de controle continuam citando o caminho do arquivo. Não foram alterados, porque guardam só metadados e são o registro do que foi feito.
- No `E:` (`...\Base Legal CLC - Atualizada Maio.2026\Normativos MPPI\`), o original e mais 4 PDFs idênticos a ele (mesmo MD5 `bab3cfbb…`, todos com a escala de plantonistas) tinham nome de MJR: `MJR n56`, `n66`, `n86`, `n92` e `n95`. A pedido do usuário, os 5 foram para a Lixeira do `E:`, e o MD5 de cada um foi conferido antes da exclusão e registrado no log. Os outros 4 nunca chegaram à mestra. As MJRs 56, 66, 86, 92 e 95 verdadeiras estão nas pastas `MJR nº …APPL`, no `E:` e na mestra, e não foram tocadas.

## Etapa 11 — Reescrita do histórico do Git (2026-10-03)
Decisão do usuário: reescrever o histórico para apagar de vez o .md do MJR n56 e o Livro "ETP e TR com ChatGPT".
- Antes da reescrita, o repositório inteiro foi salvo em `C:\Users\thiagonogueira\Claude\backup_git_antes_reescrita.bundle`. Esse backup ainda contém os dois arquivos.
- `git filter-branch --index-filter "git rm --cached --ignore-unmatch ..."` no `main`. Conferido commit a commit: só esses dois arquivos saíram, nada foi acrescentado, as mensagens ficaram iguais e o conteúdo final é idêntico ao de antes. As outras obras comerciais nunca chegaram a ser versionadas.
- **Todos os códigos de commit mudaram**, exceto o primeiro (`70aa07e`). Os documentos foram atualizados com os códigos novos; a correspondência entre antigos e novos está em `controle/mapa_commits_reescrita.csv`.
- Depois veio o *force push* para o GitHub, além da limpeza local (`refs/original`, reflog e `git gc --prune=now`). Qualquer outro clone feito antes disso precisa ser descartado e clonado de novo.
- Conferência: no clone, os 3 blobs (as duas versões do .md do MJR n56 e o Livro) não existem mais, e nenhum commit cita esses caminhos. No GitHub, o `main` tem só o histórico novo. Mesmo assim, o GitHub continua respondendo pelos commits antigos a quem tiver o código exato, até fazer a própria coleta de lixo. O repositório é privado e não tem forks. Para apagá-los de vez, o dono pode pedir ao Suporte do GitHub ("remove cached views / run garbage collection"), informando os códigos antigos do mapa.

## Etapa 12 — Integração do grupo A dos Downloads (2026-10-04)
Os materiais da pasta `Downloads` do usuário foram analisados e separados em grupos, que o usuário aprova um por um. A análise não foi versionada, porque lista arquivos pessoais. O grupo A (normativos e jurisprudência ausentes da base) foi aprovado com a instrução de **mover** os arquivos para a mestra, já com o nome no padrão da base, e conferir o MD5.
- **Movimentação:** `mover_downloads.py` primeiro checa o plano inteiro (a origem existe, o destino não existe, a pasta de destino existe) e só então move. Em cada arquivo, compara o MD5 antes e depois. Os 21 arquivos foram movidos, todos com status OK e MD5 idêntico. O plano está em `controle/plano_mover_grupoA.csv` e o log, em `controle/log_movimentacao_downloads.csv`, com origem e destino, o que permite reverter.
  - A1 e A2: Resolução TCE-PI 41/2023 (compilada com a Res. 02/2026) e Resolução TCE-PI 02/2026, em `05_TCE_PI/Resolucoes`.
  - A3: Acórdão TCE-PI 394-A/2026, consulta do MPPI sobre prorrogação e renovação de quantitativos de ARP, em `05_TCE_PI/Acordaos_Pareceres_Orientacoes`.
  - A4: Parecer Referencial 00003/2025/CONJUR-EB/CGU/AGU, sobre inexigibilidade para cursos e pós-graduação, em `01_Federal/Acordaos_Pareceres_Orientacoes`.
  - A5: Resolução TCE-PI 08/2026, Sistema de Integridade, em `05_TCE_PI/Resolucoes`.
  - A6 e A7: Lei 4.320/1964 e LC 101/2000 (LRF), em `01_Federal/Leis`.
  - A8: Ato PGJ 823/2018 com alterações (Diretor de Sede), em `03_MPPI/Atos`.
  - A9: os 13 PDFs dos boletins Guia Lici 2026 (01 a 13), em `02_Jurisprudencia_e_Orientacoes/Informativos_Guia_Lici/2026`. Mantêm **os nomes originais**, porque o consolidado anual já os cita assim.
- **Lote 07:** os 8 PDFs de A1 a A8 foram convertidos com `converter_pdf_md.py`, todos OK no QA (`controle/lotes/log_lote_07.csv`, `qa_lote_07.csv`). As linhas foram acrescentadas a `log_conversao.csv` por `registrar_lote.py`, sem duplicar.
- **Enriquecimento:** `enriquecer_md.py` acrescentou ao front-matter dos 8 .md os campos semânticos (tipo, número, ano, órgão, âmbito, assunto, status, tags), mais o título e o bloco de ementa, com backup prévio em `backup_md\enriquecimento\`. As ementas foram escritas a partir do texto de cada documento (`controle/lotes/meta_lote_07.py`). A ementa da Res. 08/2026 foi corrigida antes da gravação para seguir o parágrafo único do art. 1º.
- **Boletins Guia Lici 06, 07 e 08/2026:** no consolidado anual, essas seções existiam, mas estavam vazias, porque os PDFs são só imagem. O texto saiu de OCR (Tesseract, 400 dpi) e foi revisado manualmente contra a imagem de cada boletim. Cada seção traz uma nota que indica isso. `preencher_guialici_2026.py` só grava se o MD5 da versão anterior bater (`54709dd9…`, mestra e clone idênticos), preserva o fim de linha CRLF e faz backup (`backup_md\20261004_224742_Boletim Guia Lici - Consolidado Anual 2026.md`). Os boletins "Guia Lici" são produzidos pela própria CLC/MPPI (Assessoria para Gerenciamento de Licitações), por isso não há restrição para versioná-los.
- **Carga do clone:** `carregar_repo.py` copiou 8 .md e 8 PDFs (os PDFs ficam fora do Git pelo `.gitignore`). Ele informa `ORIGEM_NAO_ENCONTRADA` para o PDF do MJR n56, o que é esperado: o arquivo foi apagado na etapa 10, mas a linha continua em `log_conversao.csv`, que não foi alterado.
- **Conferências:** uma varredura de dados pessoais nos 8 .md achou só um CPF que o próprio TCE-PI já publica mascarado no Acórdão 394-A. Nenhum script ou CSV de controle novo contém e-mail.

## Etapa 13 — Integração do grupo B dos Downloads (2026-10-05)
O grupo B reúne o material de trabalho da CLC: POPs, roteiros, prompts, checklists e modelos. O usuário o aprovou com quatro ajustes:
- nomes dos POPs no padrão dos que já estão na base;
- POPs novos na pasta atual (`04_CNMP/POP's Contratação Direta`);
- roteiros em arquivos separados;
- no .md do prompt do Notebook LM, o nome completo do usuário trocado por `[nome do servidor]`, com o .docx original intacto.

Os arquivos foram **movidos**, não copiados.
- **Movimentação:** `mover_downloads.py` executou `controle/plano_mover_grupoB.csv`. Os 24 arquivos ficaram com status OK e MD5 idêntico antes e depois. O log está em `controle/log_movimentacao_downloads.csv`, grupos B1 a B10. Destinos:
  - 3 POPs (POP-CLC-02, 05 e 08): `01_Normativos_Vigentes/04_CNMP/POP's Contratação Direta`;
  - 8 roteiros: `03_Modelos_e_Minutas/Modelos_MPPI_CLC/Roteiros_CLC`;
  - nota técnica e diagnóstico do TAPP-D, mais o glossário de mensagens da sessão pública de pregão: `03_Modelos_e_Minutas/Modelos_MPPI_CLC`;
  - 7 prompts e o checklist de TR (rascunho): `00_Ferramentas_e_Scripts_Analise/Banco_de_Prompts`;
  - 2 TAPPs do MPPE: `03_Modelos_e_Minutas/Modelos_MPPE`.
  - Duas planilhas que já estavam na mestra ganharam .md: o Checklist padronizado do MPPE (v2.0) e o Mapa de Riscos do CNMP/CCAF.
- **Conversor de Office (novo):** `converter_office_md.py` converte dois formatos e grava o mesmo log dos PDFs. A coluna `pdf` guarda o original em qualquer formato, o que permite reaproveitar `registrar_lote.py` e `enriquecer_md.py`.
  - **.docx:** lê o XML com `zipfile` + `lxml`. Parágrafos e tabelas saem na ordem do documento, os títulos vêm do estilo e a numeração das listas é calculada. Caixas de seleção viram `- [ ]`, as notas de rodapé vão para o fim e as imagens são marcadas como *[imagem]*.
  - **.xlsx:** usa `openpyxl`, com uma seção por planilha e os valores calculados.
- **Lote 08:** 26 arquivos (22 .docx, 2 .xlsx e 2 PDFs), todos OK (`controle/lotes/log_lote_08.csv`).
  - `qa_office.py` (novo) deu cobertura de palavras 1,0 nos 24 arquivos de Office (`qa_lote_08_office.csv`).
  - `qa_conversao.py` deu 0,999 e 0,997 nos 2 PDFs (`qa_lote_08.csv`). O script passou a pular os originais que não são PDF.
- **Anonimização (regra nova):** antes da carga no clone, `anonimizar_md.py` aplicou 13 substituições em 7 .md, só no corpo; o front-matter não muda. Houve backup prévio em `backup_md\anonimizacao\2026-10-05\`.
  - Foram trocados por marcadores:
    - o nome e a matrícula do usuário (`[nome do servidor]`, `Mat. [matrícula]`);
    - o nome de um colega nos POPs e na nota técnica;
    - nomes e matrículas de três fiscais de contrato num roteiro (`[nome do fiscal]`);
    - a razão social de uma empresa citada num prompt baseado em caso real (`[nome da empresa]`).
  - As regras (`lotes\anon_lote_08.py`) e o log (`log_anonimizacao.csv`) ficam só no computador local, porque contêm ou apontam os dados removidos.
  - Os originais .docx e PDF não foram alterados.
  - Pelo precedente das MJRs, ficaram mantidos: signatários e gestores nos documentos do MPPE, signatários de MJR, números de processos SEI/PGA e e-mails institucionais.
- **Enriquecimento:** `enriquecer_md.py` usou `controle/lotes/meta_lote_08.py`, com 26 ementas escritas a partir do texto de cada documento. Tipos novos: Nota Técnica, Procedimento Operacional Padrão (POP), Roteiro de Procedimento, Modelo de Mensagens, Prompt de IA, Lista de Verificação (Checklist), Modelo de Análise Preliminar (TAPP) e Documento de Estudo / Planejamento.
- **Proteções:** o `.gitignore` passou a bloquear `*.docx` e `*.xlsx`, porque os originais ficam só no OneDrive. `carregar_repo.py` só leva para o clone os originais .pdf do `log_conversao.csv`.
- **Carga do clone:** 26 .md e 2 PDFs; os PDFs ficam fora do Git. O `ORIGEM_NAO_ENCONTRADA` do MJR n56 continua, como na etapa 12.

## Etapa 14 — Integração do grupo C dos Downloads (2026-10-05)
Antes desta etapa, o usuário fez uma limpeza manual no `Downloads`. O inventário foi refeito: saíram 58 arquivos da raiz, e a mestra não foi tocada. O grupo C, que exigia decisão item a item, foi aprovado "conforme recomendado", junto com a exclusão do grupo E.
- **Decisões por item:**
  - **C1** (`ASSGERLICT.zip`, editais de 2026): encerrado, porque o arquivo saiu na limpeza.
  - **C2** (dossiê de Suprimento de Fundos, 29 arquivos): 20 foram integrados.
    - Oito já estavam na base.
    - O Ato PGJ 350/2013 ficou de fora, porque foi revogado expressamente pelo Ato PGJ 1.228/2022.
    - O `cbc,+XXIICongresso_artigo_0312.pdf` é cópia do `CONGRESSO CUSTOS 2015.pdf` e também ficou no Downloads.
  - **C3** (curso Zênite "Imersão em Contratações Diretas", 11 PDFs): integrado só no clone local, como as demais obras comerciais.
  - **C4** (material didático do usuário, 6 arquivos): integrado em `Biblioteca_Manuais_e_Cursos/Material_Didatico_CLC`.
  - **C5** (peças de processos SEI): nenhuma peça entrou na base. Da manifestação do ordenador sobre adesão à ARP e do ofício ao órgão aderente saíram **dois modelos anonimizados**. Os originais ficaram no Downloads.
  - **C6** (planilha de saldo de adesões da ARP 42/2025): não integrada, porque é controle operacional e envelhece rápido.
  - **C7** (3 documentos do próprio projeto): levados para [`docs/projeto/`](projeto/).
  - **Grupo E:** as 5 cópias da escala de plantonistas (MD5 `bab3cfbb…`) foram para a Lixeira, com registro em `log_exclusoes.csv`.
- **Movimentação:** `mover_downloads.py` executou `controle/plano_mover_grupoC.csv`. Os 40 arquivos (C2: 20, C3: 11, C4: 6, C7: 3) ficaram com status OK e MD5 idêntico antes e depois (`controle/log_movimentacao_downloads.csv`). Destinos:
  - pasta nova `05_Doutrina_e_Biblioteca/Suprimento_de_Fundos`: guias da CGU, do MP-BA, MPES, MPMG, MPRJ e MPPR; estudos sobre o custo de uma licitação; dois trabalhos acadêmicos; a IN CCI 001/2011 de Herval d'Oeste (SC);
  - `01_Normativos_Vigentes/02_Estadual_PI/Leis`: LC 13/1994 (Estatuto dos Servidores Civis do PI);
  - `01_Normativos_Vigentes/03_MPPI`: Informativo da Controladoria Interna sobre suprimento de fundos (maio/2024);
  - pasta nova `05_Doutrina_e_Biblioteca/Biblioteca_Manuais_e_Cursos/Curso_Imersao_Contratacoes_Diretas`: o curso Zênite.
- **Ferramentas alteradas:**
  - `converter_pdf_md.py`: **DPI adaptativo** no OCR. O Informativo tem páginas de cerca de 5.000 × 5.000 pt, que a 250 dpi passavam do limite de pixels do Pillow (`DecompressionBombError`). O DPI agora desce de 10 em 10 até a imagem caber.
  - `converter_office_md.py`: passou a ler **.doc** (Word 97-2003) com `olefile`, pela tabela de peças do documento. Sai só o texto corrido, sem títulos nem listas. A IN CCI 001/2011 foi o primeiro caso.
  - `anonimizar_md.py`: nova opção `--front-matter`, para .md autorais cujo cabeçalho tem conteúdo (por exemplo, o nome de quem elaborou). Nos convertidos, o front-matter continua intacto.
  - `modelo_docx.py` (novo): gera um modelo .docx a partir de um documento real. Troca os dados do caso por marcadores no XML, preserva a formatação e apaga autor e "modificado por" dos metadados. As regras de cada modelo (`lotes\modelo_*.py`) ficam fora do Git, porque contêm os dados originais. Foram gerados os 2 modelos de ARP do C5, em `03_Modelos_e_Minutas/Modelos_MPPI_CLC`.
- **Lote 09:** 39 arquivos, todos OK (`controle/lotes/log_lote_09.csv`): 31 PDFs (2 com OCR total, o Informativo e o laboratório do curso Zênite, e 12 com OCR em algumas páginas), 6 de Office, o .doc e o `Roteiro_Video_PCA_MPPI.md`, que já era Markdown e só recebeu front-matter.
  - QA (`qa_lote_09.csv`, `qa_lote_09_office.csv`): tudo OK. O Informativo tem nota 0 porque o PDF não tem camada de texto para comparar; o OCR foi conferido por amostragem.
  - Os 3 .md do C7 têm log próprio (`log_lote_09_docs.csv`), só para a anonimização.
- **Anonimização:** 10 substituições no lote 09 (nome e matrícula do usuário, nome de um colega) e 3 nos documentos do C7, estes com `--front-matter`. Uma varredura posterior achou só e-mails de autores acadêmicos e contatos institucionais, mantidos pela regra 9.
- **Enriquecimento:** `controle/lotes/meta_lote_09.py`, com 39 ementas escritas a partir do texto. Observações registradas nas ementas:
  - o guia do MPRJ trata de curatela, não de suprimento de fundos;
  - no RT 12, a fonte do dado de custo (FIA/USP) é provável, não confirmada;
  - os 11 arquivos do curso Zênite têm o status "material de curso comercial".
- **Obras fora do GitHub (`.gitignore`):** além das 2 previstas na análise (`34_suprimento_de_fundos_2ed`, do MPF, com todos os direitos reservados, e `Você sabe quanto custa uma licitação_`), entraram outras 2 que a leitura mostrou serem comerciais: `32-Custos de uma licitação - NP` e `QUANTO CUSTA UMA LICITAÇÃO - 2014`, ambas da Negócios Públicos. Entrou também a pasta inteira do curso Zênite. O `.gitignore` passou a bloquear ainda `*.doc`.
- **Carga do clone:** 39 .md e 31 PDFs. Com o `.gitignore`, 15 desses .md ficam só locais, e 24 são versionados.
- **Achado:** na base, o arquivo `01_Normativos_Vigentes/03_MPPI/Atos/Ato PGJ 0228.2022 - Suprimento de Fundos.md` tem no cabeçalho "ATO PGJ Nº 1.228/2022": o nome do arquivo parece ter um erro de digitação. Ver PENDENCIAS.

## Etapa 15 — Índice por fase da contratação (2026-10-05)
- **Origem:** a comparação com o repositório público de um colega de trabalho mostrou que ele organiza os artefatos por fase da contratação. A taxonomia da base é por órgão e tipo, e faltava uma porta de entrada por fase. Do repositório do colega só a ideia foi aproveitada: nenhum arquivo nem código foi integrado.
- **Mapa curado** (`docs/controle/indice/mapa_indice.py`): 17 seções por fase (da base legal comum até liquidação, pagamento e suprimento de fundos), 5 temas transversais e 8 tipos de objeto. Cada fase traz os artigos da Lei 14.133 e, em ordem, normas, modelos e roteiros, manuais e jurisprudência.
  - 450 arquivos ligados, 5 deles só locais (obras licenciadas), cada um **uma vez só**, na seção do uso principal.
  - Cada descrição foi lida no **corpo** do arquivo. O front-matter enriquecido mostrou erros de assunto e ementa em pelo menos 11 arquivos.
- **Gerador** (`gerar_indice_por_fase.py`): confere que cada padrão do mapa casa com um único .md, presente na mestra e no clone, e só grava sem pendências. Modos: conferir, `--lista`, `--escrever` (rascunho fora da base), `--aplicar` (mestra; recusa sobrescrever) e `--substituir` (mestra e clone, cada um com backup em `backup_md\indice\`).
- **Proposta e aprovação:** o rascunho foi gerado fora da base e apresentado com os achados. O usuário aprovou as decisões 1 a 3: **local** na raiz da mestra (`00_Indice_por_Fase_da_Contratacao.md`), **arquivo único** e marca *(só local)* nas obras licenciadas.
- **Aplicação:** o índice foi gravado na mestra e levado ao clone por `carregar_repo.py` (1 .md copiado, MD5 `037beacf…` igual nos dois lados; a simulação prévia mostrou que nada mais seria carregado). Os 450 links foram conferidos de forma independente na mestra e no clone, e as âncoras do mapa rápido também. README, AGENTS e PIPELINE foram atualizados. O README estava desatualizado: dizia que só PDFs ficam fora do Git e não falava das obras só locais.
- **Achados registrados nos apêndices do índice:**
  - 9 arquivos com conteúdo diferente do nome (por exemplo, a "Portaria 8.678" é uma tela do Compras.gov.br), deixados de fora do índice;
  - 11 arquivos com `assunto` ou ementa errados no front-matter;
  - muitos duplicados (PCA 2026 em 3 lugares, Provimento TJPI 13/2025 em 3 arquivos, manuais repetidos) e 5 arquivos na raiz que pertencem a pastas;
  - lacunas: a fase 10 (recursos e homologação) é a mais fraca, e faltam modelo do MPPI de decisão de recurso, regulamento de sanções, manual de riscos, caderno de logística 2024, IN SGD 94/2022 e a lei federal da LGPD.
- **Não feito (depende de decisão):** campo `fases:` no front-matter, auditoria do front-matter, tratamento dos arquivos dos apêndices A.1 e C. Ver PENDENCIAS.

## Etapa 16 — Roteiro de credenciamento (2026-10-05)
- **Pedido:** levar para a mestra o `Roteiro - Credenciamento.md`, que tinha aparecido no clone fora do fluxo (`03_Modelos_e_Minutas/Modelos_MPPI_CLC/Roteiros_CLC/`).
- **Conferência:** o arquivo já estava na mestra, idêntico ao do clone (MD5 `08209994…`, 13.240 bytes, mesma data de modificação, 10:27). Nada foi copiado. A carga da etapa 15 já o tinha registrado como `IGNORADO_JA_EXISTE`. A origem continua desconhecida.
- **Conteúdo:** roteiro técnico da CLC/MPPI para o credenciamento (art. 79 da Lei 14.133, Decreto Federal 11.878/2024, Decreto Estadual 21.872/2023), em 8 fases, da demanda à gestão do rol de credenciados. Não tem nome de pessoa, matrícula nem empresa. Não é obra licenciada, então foi versionado.
- **Diferenças em relação aos outros roteiros da pasta:** não tem .docx ao lado; no front-matter, `hash_arquivo_md5` está vazio e `arquivo_original` aponta para o próprio .md.
- **Índice:** a pedido do usuário, o roteiro entrou na seção 12, ao lado dos outros roteiros da CLC (uma linha no `mapa_indice.py`). O índice foi regerado com `--aplicar --substituir`, com backup dos dois lados em `backup_md\indice\` (selo `20261005_145142`). O MD5 é igual na mestra e no clone (`8f3ee7e0…`), e os 451 links foram conferidos nos dois lugares.

## Etapa 17 — Exclusão da Portaria Nº 106/2025 (2026-10-05)
- **Antes:** o PDF da mestra estava cortado em 7 MiB, e nenhum leitor o abria. Reconstruído o índice interno numa cópia fora da base, 6 das 10 páginas voltaram. O documento é a Portaria Conjunta SSP-PI/SEAD/SIA/ETIPI/FADEX que institui a Política Pública do Ambiente de Inovação do Estado do Piauí. O texto está desenhado como curvas, sem camada de texto. Não trata de licitações e contratos.
- **Pedido:** o usuário mandou excluir a portaria, por não ser relevante para a base.
- **Feito:** o PDF da mestra foi para a Lixeira (MD5 `dfd021de…`, registro em `log_exclusoes.csv`). Não havia .md nem link no índice. A cópia reconstruída para leitura também foi apagada.
- **Cópia do `E:`:** a pedido do usuário, a cópia idêntica na pasta de origem do `E:` (`Normativos Estado do Piauí`) também foi para a Lixeira, para não voltar à base numa cópia futura (mesmo MD5, registro em `log_exclusoes.csv`).
- **Fica:** os registros antigos de controle (lotes, movimentação, mapas de pares) continuam citando o arquivo, como histórico.

## Etapa 18 — Nome do Ato PGJ 1.228/2022 (2026-10-05)
- **Pedido:** corrigir o nome `Ato PGJ 0228.2022 - Suprimento de Fundos.md` (pasta `01_Normativos_Vigentes/03_MPPI/Atos/`), cujo texto começa com "ATO PGJ Nº 1.228/2022" (achado da etapa 14).
- **Feito:** o arquivo passou a se chamar `Ato PGJ 1228.2022 - Suprimento de Fundos.md`, na mestra e no clone (`git mv`). O nome segue o padrão da pasta (`Ato PGJ NNNN.AAAA - Descrição`), sem o ponto de milhar, porque o ponto ali separa o número do ano. O conteúdo não mudou (MD5 `a33dc4fe…` antes e depois). Backup em `backup_md\renomeacao\`; registro em `docs/controle/log_renomeacao.csv`.
- **Índice:** a linha do Apêndice A.1 (em `apendices_proposta.md`) passou a citar o nome novo, e o índice foi regerado com `--aplicar --substituir`: segue com 451 links, sem link quebrado. O arquivo não tem PDF ao lado e não é linkado no corpo do índice; a seção 16 liga o compilado (`03_MPPI/Ato PGJ 1228.2022 - Suprimento de Fundos (Compilado).md`), que não muda.
- **Fica:** os registros antigos de controle continuam citando o nome antigo, como histórico. O que fazer com a duplicação em relação ao compilado foi decidido na etapa 19.

## Etapa 19 — Ato PGJ 1.228/2022: texto original marcado como histórico (2026-10-05)
- **Conferência:** comparado palavra a palavra com o compilado (`03_MPPI/Ato PGJ 1228.2022 - Suprimento de Fundos (Compilado).md`), o arquivo de `Atos/` não é uma duplicata: é a redação original, assinada em 15/09/2022, sem as alterações dos Atos PGJ 1251/2022 e 1252/2022 (≈95% do texto em comum). Só o compilado tem, entre outros, o limite de aplicação até 25 de novembro, a regra de transição para suprimentos pendentes e o art. 23 (pessoa física). Os Atos 1251 e 1252/2022 não estão na base como arquivos próprios.
- **Decisão do usuário:** manter o arquivo, que é a única cópia da redação e da assinatura originais, mas deixar claro que não é a versão em vigor, para a IA não citar regra antiga.
- **Feito, na mestra e no clone (mesmo conteúdo):**
  - front-matter com `status: "Histórico (texto original de 15/09/2022, sem as alterações dos Atos PGJ 1251/2022 e 1252/2022; ver o compilado)"`, no padrão já usado para o roteiro de dispensa de 2024;
  - título, ementa e um aviso que aponta para o compilado. O corpo original continua intacto, logo abaixo do cabeçalho;
  - nome novo: `Ato PGJ 1228.2022 - Suprimento de Fundos (Texto Original).md`.
- **Controle:** MD5 `a33dc4fe…` antes e `d9491c3f…` depois. Backup em `backup_md\renomeacao\2026-10-05_antes_front-matter_…`; renomeação registrada em `docs/controle/log_renomeacao.csv`.
- **Índice:** a linha do Apêndice A.1 passou a dar o caso como resolvido, e a abertura do Apêndice A deixou de dizer que nenhum arquivo foi alterado. Índice regerado com `--aplicar --substituir`: 451 links, nenhum quebrado. O corpo do índice continua ligando só o compilado (seção 16).

## Etapa 20 — Atos PGJ 1.106/2021 e 1.480/2025 (2026-10-05)
- **Antes:** o `Ato PGJ 1480.2025 - Retira CONINT da Fase Interna.md` (Apêndice A.1) não tinha PDF ao lado e misturava trechos de duas edições do DOE MPPI: a 985/2021 (Portaria PGJ 2980/2021 e Ato 1.106/2021) e a 1730/2025 (Ato 1.480/2025 e outros atos). O texto oficial do Ato 1.480/2025 estava no par `Ato PGJMPPI - n1480.0 - 2025` (PDF e .md), que era o linkado no índice.
- **Arquivos novos:** o usuário pôs três PDFs no clone, em `01_Normativos_Vigentes/03_MPPI/Atos/`: `Ato PGJ 1106.2021 - Novo Fluxo da Controladoria Interna.pdf`, `2021-11-ato-pgj-no-1106-2021.pdf` (cópia idêntica do primeiro, MD5 `727a75c5…`) e `Ato PGJ 1480.2025 - Retira CONINT da Fase Interna.pdf` (o mesmo PDF do par `n1480`, MD5 `d382b1bb…`).
- **Decisão do usuário:** seguir com o Ato 1.106 e, para o 1.480, com a saída A: fica o par de nome descritivo, o .md misturado é trocado pela conversão do PDF oficial e o par `n1480` sai.
- **Feito:**
  - os dois PDFs de nome descritivo foram copiados do clone para a mestra, com conferência de MD5 (`docs/controle/log_movimentacao.csv`);
  - lote 10: os dois PDFs passaram por `converter_pdf_md.py`, `qa_conversao.py`, `enriquecer_md.py` (`docs/controle/lotes/meta_lote_10.py`) e `registrar_lote.py`. O Ato 1.106/2021 saiu com `status: "Vigente com alterações (alterado pelo Ato PGJ 1480/2025)"` e com um aviso na ementa: o Ato 1.480 deu nova redação às alíneas h e k e acrescentou os §§ 4º e 5º, e o aviso aponta para o .md dele;
  - o .md do 1.106 chegou ao clone por `carregar_repo.py`;
  - o .md misturado do 1.480 foi trocado, com autorização e backup, pela conversão do PDF oficial. Como o conversor não sobrescreve, a conversão foi feita com `--saida-dir` numa pasta temporária e enriquecida lá. A troca, na mestra e no clone, usou arquivo temporário + `os.replace`, porque o .md da mestra tinha hard links em caches do app. MD5 `23bcf692…` antes e `0b307b61…` depois. Backup em `backup_md\substituicao\`; registro em `docs/controle/log_substituicao_md.csv` (novo);
  - foram para a Lixeira, com conferência de MD5 e registro em `log_exclusoes.csv`: a cópia `2021-11-ato-pgj-no-1106-2021.pdf` do clone e o par `Ato PGJMPPI - n1480.0 - 2025` (PDF e .md), na mestra e no clone.
- **Índice:** no `mapa_indice.py`, a seção 4 (gestão de riscos) passou a ligar o 1.480 pelo nome descritivo e ganhou o 1.106. A linha do Apêndice A.1 dá o caso como resolvido. Índice regerado com `--aplicar --substituir` (backup `20261005_161440`): 452 links, nenhum quebrado na mestra nem no clone; MD5 `7613b5e9…` nos dois.
- **Fica:** a cópia do .md antigo em `_DUPLICADOS_para_arquivar/`, na mestra, como estava. Os registros antigos de controle continuam citando o `n1480`, como histórico.

## Etapa 21 — Infográfico com nome de Portaria 8.678/2021 (2026-10-06)
- **Conferência:** o par `01_Federal/Portarias/Portaria Fedral - n8678.0 - 2021` (Apêndice A.1) não era a portaria. O próprio PDF é um infográfico de 1 página do Compras.gov.br, "Como vender para o Governo" (Canva, 2023), que ensina o fornecedor a criar a conta gov.br, credenciar-se no Sicaf e entrar no pregão eletrônico. O .md trazia esse texto com front-matter, título e ementa da Portaria 8.678, o que enganaria uma IA. Ele tinha sido copiado na etapa 5 de `Federal - Portaria 8678.2021 - Governanca de Contratacoes Publicas.md`, cópia idêntica que só existia na mestra.
- **A portaria de verdade** (Portaria SEGES/ME 8.678/2021, texto integral) já está em `05_Doutrina_e_Biblioteca/Biblioteca_Manuais_e_Cursos/Manuais/`, em PDF e .md, e é a que o índice liga.
- **Decisão do usuário (saída B):** retirar o infográfico da base, por estar fora do escopo.
- **Feito:** foram para a Lixeira, com conferência de MD5 e registro em `log_exclusoes.csv`: o PDF (`230fbfb7…`) e o .md (`1d51db4b…`) na mestra e no clone, e a cópia de origem do .md na mestra.
- **Índice:** a linha do Apêndice A.1 dá o caso como resolvido. Índice regerado com `--aplicar --substituir` (backup `20261006_073339`): 452 links, nenhum quebrado na mestra nem no clone; MD5 `7e3687b4…` nos dois.
- **Fica:** a cópia do .md antigo em `_DUPLICADOS_para_arquivar/` e a cópia idêntica do .md da portaria verdadeira solta em `Biblioteca_Manuais_e_Cursos/` (`Portaria SEGES-ME 8678.2021 - Governanca das Contratacoes Publicas Federais.md`, só na mestra), à espera de decisão.

## Etapa 22 — Manual IRB/Ibraop com nome de Resolução TCE-PI 19/2024 (2026-10-06)
- **Conferência:** o par `05_TCE_PI/Resolucoes/Resolução TCE - n19.0 - 2024` (Apêndice A.1) não era a Resolução 19/2024 (Regimento Interno do TCE-PI). O próprio PDF (114 páginas, MD5 `c610f8e9…`) é o Manual de Auditoria de Obras Públicas e Serviços de Engenharia do IRB e do Ibraop, de 18/10/2018. A conversão do .md estava boa; só o front-matter, o título e a ementa diziam "Regimento Interno do TCE-PI", o que enganaria uma IA. Ele tinha sido copiado na etapa 5 de `Resolucao TCE-PI nº 19.2024 - Regimento Interno do TCE-PI.md`, cópia idêntica que só existia na mestra.
- **Decisão do usuário (saída A, com inclusão no índice):** manter o manual como referência técnica, com nome e cabeçalho corretos.
- **Feito:**
  - o par foi renomeado para `Manual IRB-Ibraop - Auditoria de Obras Publicas e Servicos de Engenharia (2018)` e movido para `05_Doutrina_e_Biblioteca/Biblioteca_Manuais_e_Cursos/Manuais/`, na mestra e no clone, com conferência de MD5 (`docs/controle/log_renomeacao.csv`);
  - o cabeçalho do .md foi trocado, com autorização e backup (`backup_md\renomeacao\`), pelo do manual: tipo "Manual", órgão IRB/Ibraop, ano 2018, status "Referência técnica (anterior à Lei 14.133/2021)" e aviso de que se apoia na Lei 8.666/1993. O corpo ficou intacto. Troca por arquivo temporário + `os.replace`, mantendo o CRLF; MD5 `2869d76b…` antes e `60f71e4c…` depois (`docs/controle/log_substituicao_md.csv`);
  - a cópia de origem com o nome errado foi para a Lixeira (MD5 conferido, registro em `log_exclusoes.csv`).
- **Índice:** o `mapa_indice.py` passou a ligar o manual na seção 13 (fiscalização do contrato, grupo D). A linha do Apêndice A.1 dá o caso como resolvido, e o Apêndice B ganhou a lacuna "Regimento Interno do TCE-PI", que não existe na base. Índice regerado com `--aplicar --substituir` (backup `20261006_075832`): 453 links, nenhum quebrado na mestra nem no clone; MD5 `1e05ee03…` nos dois.
- **Fica:** a cópia do .md antigo em `_DUPLICADOS_para_arquivar/Analise_de_processos_04_Normativos_Relacionados/`, na mestra, como estava.

## Etapa 23 — Acórdão TCE-PI 300/2025, que estava como "n3001" com o DOE inteiro (2026-10-06)
- **Conferência:** o par `02_Jurisprudencia_e_Orientacoes/Acordaos_TCE_PI/Acórdão TCE - n3001 - 2025` (Apêndice A.1) não era um acórdão "3001". O PDF (MD5 `1a7acd9a…`) é a edição inteira do Diário Oficial Eletrônico do TCE-PI nº 152/2025, de 15/08/2025, com 41 páginas e assinatura digital. O acórdão que interessa é o 300/2025 – 1ª Câmara (TC/012945/2024, inspeção na Prefeitura de Flores do Piauí: adesão a ARP de medicamentos, sobrepreço, falta de suplente do fiscal e de PCA), nas páginas 10 e 11, seguido do 300-A/2025, do mesmo processo, nas páginas 11 e 12. O .md convertia o diário inteiro, inclusive cerca de 30 páginas de decisões de aposentadoria e pensão com nomes de servidores e pensionistas, e estava no GitHub com o cabeçalho do Acórdão 300. Ele tinha sido copiado na etapa 5 de `05_TCE_PI/Acordaos_Pareceres_Orientacoes/Acordao TCE-PI 300.2025 - Primeira Camara - Irregularidades Pregao e Adesao ARP.md`, cópia idêntica que só existia na mestra.
- **Decisão do usuário (saída A, com inclusão no índice):** manter o PDF oficial inteiro e reduzir o .md aos dois acórdãos.
- **Feito:**
  - o par foi renomeado para `Acordao TCE-PI 300.2025 - 1a Camara - Irregularidades Pregao e Adesao ARP (DOE 152.2025)`, na mesma pasta, na mestra e no clone, com conferência de MD5 (`docs/controle/log_renomeacao.csv`);
  - o .md foi trocado, com autorização e backup (`backup_md\substituicao\`), por um com só os Acórdãos 300 e 300-A/2025, tirados da conversão anterior (sem os rodapés do diário), e cabeçalho novo que avisa que o PDF ao lado é o DOE inteiro e indica as páginas 10 a 12. Troca por arquivo temporário + `os.replace`, em CRLF; MD5 `afba84f7…` (183 KB) antes e `cc295973…` (14 KB) depois (`docs/controle/log_substituicao_md.csv`);
  - a cópia de origem foi para a Lixeira (MD5 conferido, registro em `log_exclusoes.csv`).
- **Índice:** o `mapa_indice.py` passou a ligar os acórdãos na seção 13, grupo J (jurisprudência), que estava vazio. A linha do Apêndice A.1 dá o caso como resolvido. A lacuna do Regimento Interno no Apêndice B agora diz que é a Resolução TCE/PI 13/2011, como cita o próprio acórdão. Índice regerado com `--aplicar --substituir`: 454 links, nenhum quebrado na mestra nem no clone.
- **Fica:** a cópia do .md antigo em `_DUPLICADOS_para_arquivar/Analise_de_processos_04_Normativos_Relacionados/`, na mestra; e o .md antigo, com o diário inteiro, no histórico do git (ver PENDENCIAS).

## Etapa 24 — Ato PGJ 1.471/2025, que estava como "Regulamenta Suprimento de Fundos" (2026-10-06)
- **Conferência:** o .md `01_Normativos_Vigentes/03_MPPI/Ato PGJ 1471.2025 - Regulamenta Suprimento de Fundos MPPI.md` (Apêndice A.1) não tinha PDF, e o nome e o cabeçalho diziam que o ato regulamenta o suprimento de fundos. Na verdade, o Ato PGJ 1.471/2025, de 16/01/2025, só altera o Ato PGJ 823/2018: acrescenta ao art. 3º o inciso XXV, que dá ao Diretor de Sede a função de agente suprido, nos termos do Ato PGJ 1.228/2022. A compilação do Ato 823 que está na base (alterações dos Atos 940/2019 e 1004/2020) não traz esse inciso.
- **Decisão do usuário:** o usuário baixou o PDF oficial do SEI (1 página, MD5 `48d96e80…`), e o par foi montado em `03_MPPI/Atos/`.
- **Feito:**
  - o PDF foi renomeado no clone para `Ato PGJ 1471.2025 - Altera Ato 823.2018 - Diretor de Sede como Agente Suprido.pdf` e copiado para a mestra, com conferência de MD5 (`log_renomeacao.csv` e `log_movimentacao.csv`);
  - lote 11: `converter_pdf_md.py` com `--saida-dir` numa pasta temporária, `qa_conversao.py` (cobertura 1,0), `enriquecer_md.py` (`docs/controle/lotes/meta_lote_11.py`, status "Vigente", ementa que remete ao Ato 1.228 compilado e ao Ato 823) e `registrar_lote.py`;
  - o .md antigo foi movido para `Atos/`, com o nome do PDF (no clone, com `git mv`), e trocado, com autorização e backup (`backup_md\substituicao\`), pela conversão. Troca por arquivo temporário + `os.replace`, na mestra e no clone; MD5 `1b9ba3fe…` antes e `1ab5abb6…` depois (`docs/controle/log_substituicao_md.csv`);
  - o .md do Ato 823/2018 ganhou, na ementa, um aviso de que o Ato 1.471/2025 acrescentou o inciso XXV e de que a compilação não o traz. O status não mudou. Backup em `backup_md\substituicao\`; MD5 `9bda8e7b…` antes e `830bf8a8…` depois.
- **Índice:** a descrição no `mapa_indice.py` (seção 16) passou a ser "Diretor de Sede como agente suprido", e a linha do Apêndice A.1 dá o caso como resolvido. Índice regerado com `--aplicar --substituir`: 454 links, nenhum quebrado na mestra nem no clone.
- **Fica:** a cópia do .md antigo em `_DUPLICADOS_para_arquivar/Analise_de_processos_04_Normativos_Relacionados/`, na mestra.

## Etapa 25 — PDFs incluídos pelo usuário em `03_MPPI/Atos` (2026-10-06)
- **Origem:** o usuário pôs 13 PDFs em `01_Normativos_Vigentes/03_MPPI/Atos/` no clone. Doze tinham .md sem PDF na base (o 13º era o 1.471, da etapa 24). Todos têm texto, sem precisar de OCR. Os PDFs dos Atos 462/2013 e 479/2014 foram gerados pelo LibreOffice a partir de arquivos de texto; não são a versão assinada do SEI.
- **Decisão do usuário:** aprovar os quatro blocos propostos.
- **Bloco 1 (só PDF):** 10 pares já estavam completos e os .md não mudaram (Atos 939/2019, 1.079/2021, 1.180/2022, 1.228/2022 Texto Original, 1.382/2024, 1.413/2024, 1.441/2024, 1.449/2024, 1.538/2025 e 1.599/2025; cobertura de 0,81 a 1,0, e a diferença vem do cabeçalho de impressão do SEI). Os PDFs foram copiados para a mestra, com conferência de MD5 (`log_movimentacao.csv`). Os PDFs dos Atos 462 e 1.383 também foram copiados.
- **Bloco 2 (Ato 479/2014):**
  - o PDF `2014-06-ato-pgj-no-4792014.pdf` foi renomeado no clone para `Ato PGJ 0479.2014 - Estrutura e Organizacao Administrativa do MPPI.pdf` e copiado para a mestra (`log_renomeacao.csv`);
  - o status do .md passou a citar os três atos que o alteram: "Vigente com alterações (alterado pelos Atos PGJ 1106/2021, 1180/2022 e 1480/2025)". Backup e MD5 `d6336fa7…` → `ab9944ce…` (`log_substituicao_md.csv`);
  - a duplicata `Ato PGJ 0479.2013 - Dispoe sobre a organizacao administrativa do MPPI.md`, sem front-matter e com o ano errado, foi para a Lixeira na mestra e no clone. A Nota Técnica do TAPP-D cita esse nome antigo, como registro do que conferiu; o texto não foi mudado;
  - o 479 entrou no índice, seção 1 (Governança).
- **Bloco 3 (lote 12):** conversão dos PDFs dos Atos 462/2013 (13 páginas, cobertura 0,997, uma página em branco por OCR) e 1.383/2024 (cobertura 1,0) numa pasta temporária, `qa_conversao.py`, `enriquecer_md.py` (`docs/controle/lotes/meta_lote_12.py`) e `registrar_lote.py`. Os .md foram trocados com backup (`backup_md\substituicao\`), por arquivo temporário + `os.replace`, na mestra e no clone:
  - Ato 462: o .md com lixo binário (.doc lido como texto; MD5 `9688711a…`) virou `1831b850…`. Status "Vigente (anterior à Lei 14.133/2021; sem revogação expressa)"; a ementa cita os Anexos I a IV, a base na Lei 8.666 e remete aos arts. 117 e 140 da Lei 14.133;
  - Ato 1.383: o .md era a página do DOE MPPI nº 1493, de 23/02/2024, com o fim do Ato 1.381, os Atos 1.382 e 1.383 e o começo do 1.384 (MD5 `63aaec35…`). Virou a conversão do PDF do SEI (`ce8786da…`), status "Vigente".
  - `registrar_lote.py` gravou em `log_conversao.csv` o caminho temporário do .md; as duas linhas foram corrigidas para o destino na mestra, como o log e o QA do lote em `docs/controle/lotes/`.
- **Bloco 4 (Lixeira):** os pares `Ato PGJMPPI - n1382.0`, `n1383.0`, `n1413.0` e `n1449.0 - 2024`, cujo PDF tem o mesmo MD5 do PDF nomeado e cujo .md não estava no índice, foram para a Lixeira, PDF e .md, na mestra e no clone, como o n1480 na etapa 20. São 18 arquivos ao todo, com a duplicata do 479, registrados em `Claude\log_exclusoes.csv`. Ficam os pares `n...` sem versão nomeada (n1381, n1414, n1415, n1448 e n1456).
- **Índice:** `mapa_indice.py` com o 479 na seção 1; Apêndice C dá como resolvidos os duplicados dos Atos 1.382, 1.383, 1.413, 1.449 e 479. Índice regerado com `--aplicar --substituir`: 455 links, nenhum quebrado na mestra nem no clone.
- **Achado:** 53 .md versionados trazem o primeiro nome do usuário em notas de fonte (ver PENDENCIAS, item 2).

## Etapa 26 — Nome do usuário fora das notas de fonte (2026-10-06)
- **Pedido do usuário:** anonimizar os .md versionados que trazem seu nome (achado da etapa 25).
- **O que mudou:** em 52 .md (51 de conteúdo e o AGENTS.md), o primeiro nome do usuário virou o marcador `[nome do usuário]` (regra 9):
  - "Fonte: PDF fornecido pelo [nome do usuário] (Downloads\Nova pasta)…" (41 arquivos);
  - "fornecido diretamente por [nome do usuário] (anexo no chat)" e variantes (7);
  - "chefiada por [nome do usuário] — Assessor de Compras" (3 roadmaps em `06_Paineis_e_Contratos_Historicos`);
  - "mantida por [nome do usuário] (CLC/MPPI)" (AGENTS.md).
- **Como:** backup em `Claude\backup_md\anonimizacao\2026-10-06\`, arquivo temporário + `os.replace`, na mestra e no clone (103 gravações; o AGENTS.md só existe no clone); mestra e clone eram idênticos antes da troca. MD5 antes e depois em `docs/controle/log_substituicao_md.csv`. A contagem de 53 da etapa 25 estava errada; são 52.
- **Nome completo e matrícula (2ª parte, também a pedido do usuário):** em 8 .md, o nome completo virou `[nome do usuário]` e a matrícula, `[matrícula]`: Portarias PGJ 4337/2024, 5644/2025 (os dois .md), 3447/2024 e 3448/2024 (nas tabelas de designação), POP Contratação Direta art. 75, IX ("Elaborado por"), `Oficio_Devolucao_Saneamento_ETP_TR.md` (assinatura) e `Roteiro_Pedagogico_Aula_Contratos_Planejamento.md` (apresentador). Mesmo procedimento: backup, mestra e clone (16 gravações), `log_substituicao_md.csv`. Os outros servidores citados nesses atos e no ofício não foram tocados, porque o pedido foi só sobre o nome do usuário.
- **Demais servidores (3ª parte, também a pedido do usuário):** nos mesmos atos e no ofício, os nomes dos outros servidores viraram `[nome do servidor]` e as matrículas, `[matrícula]`: Anexo Único das Portarias PGJ 4337/2024 (17) e 5644/2025 (24 em cada um dos dois .md, incluídos os três nomes partidos em duas linhas pelo PDF), Portarias 3447/2024 (3) e 3448/2024 (32). No ofício, como o achado compara as funções de duas servidoras, os marcadores são numerados: `[nome do servidor 1]` e `[nome do servidor 2]`, para manter o sentido. Membros do MPPI (Procuradores-Gerais que assinam e Promotores designados) não foram tocados. Mesmo procedimento: backup em `backup_md\anonimizacao\2026-10-06\servidores\`, mestra e clone (12 gravações), `log_substituicao_md.csv`.
- **Atos oficiais × documentos internos (4ª parte, decisão do usuário):** os mesmos servidores apareciam em outros 22 .md, a maioria portarias de equipe de planejamento já publicadas. Decisão: atos oficiais publicados (portarias, PCA, atas assinadas) mantêm os nomes de servidores, e só o nome do usuário vai como marcador; documentos internos e modelos são anonimizados. Assim: (a) as 5 portarias da 3ª parte (4337/2024, 5644/2025 nos dois .md, 3447/2024 e 3448/2024) voltaram à versão da 2ª parte, a partir do backup `servidores\`; (b) 8 docs internos foram anonimizados: seis POPs de contratação direta ("Elaborado por"), `Modelo de DFD - TIC.md` (nome, assinatura e e-mail pessoal, este como `[e-mail do servidor]`) e `Roteiro_Falas_Sessao_Publica_Pregao_Eletronico.md` (pregoeira); (c) o ofício continua anonimizado, por ser documento interno de processo SEI; (d) as 12 portarias, os PCAs 2025/2026 e a ARP SEI_0978996 ficaram como estavam. Regra 9 do AGENTS atualizada com a exceção. Backup em `backup_md\anonimizacao\2026-10-06\internos\`, mestra e clone (26 gravações), `log_substituicao_md.csv`.
- **Nomes de arquivo (5ª parte, a pedido do usuário):** três arquivos perderam o nome do usuário, que vinha como prefixo ou sufixo: o modelo de TAAP, agora `TAAP - TERMO DE ANÁLISE PRELIMINAR DO PLANEJAMENTO DA CONTRATAÇÃO.md`, e o documento modelo do TAPP-DIMPLANC, agora `TAPP_DIMPLANC_000_202X-X_Documento_modelo.md` (mestra e clone), e a planilha de quesitos, agora `Roteiro Quesitos (Google).xlsx` (só na mestra). O `assunto:` do TAAP também mudou (backup em `backup_md\anonimizacao\2026-10-06\nomes_arquivo\`). Junto: padrão do TAAP no `mapa_indice.py`, índice regerado com `--aplicar --substituir` (só os dois links mudaram), duas citações da planilha no `Roteiro_Analise_Pasta_CLC_Scripts_Artefatos.md` e regra 9 do AGENTS (nomes de arquivo sem o nome do usuário). Logs: `log_renomeacao.csv` (5 renomeações) e `log_substituicao_md.csv`. Ficaram: o Laboratório do Professor Thiago Zagatto (outra pessoa), os logs antigos e o nome da pasta mestra.
- **Histórico do git:** recomeçado na etapa 27. Outras pessoas com o mesmo prenome do usuário (advogados, autores) não foram tocadas.

## Etapa 27 — Histórico do git recomeçado do zero (2026-10-07)
- **Decisão do usuário:** em vez de trocar o texto commit a commit (cerca de 70 arquivos tiveram nomes em algum momento), recomeçar o histórico: um commit novo com a árvore atual substitui os 42 commits anteriores, que guardavam nas versões antigas o nome e a matrícula do usuário, os nomes de servidores e os nomes antigos de arquivo.
- **Backup:** o repositório inteiro foi salvo antes em `C:\Users\thiagonogueira\Claude\backup_git_antes_recomeco_2026-10-07.bundle` (verificado). Esse backup ainda contém as versões antigas e fica fora do Git.
- **Códigos de commit:** os citados nestes documentos (etapas 1 a 26 e tabela de lotes em PENDENCIAS) são do histórico antigo e só existem no bundle; a lista completa, com data e mensagem, está em `docs/controle/commits_antes_recomeco.csv`. Para consultar: `git clone <bundle> pasta`.
- **Como:** branch órfão com a mesma árvore do último commit (conferido pelo código da árvore), troca do `main` e *force push*; depois, limpeza local (reflog e `git gc --prune=now`). Qualquer outro clone feito antes precisa ser descartado e clonado de novo.
- **E-mail do autor:** por decisão do usuário, os commits continuam com o e-mail atual.
- **Fica com o usuário:** o GitHub pode guardar por um tempo os commits antigos em cache; para apagá-los de vez, o pedido de coleta de lixo é ao Suporte do GitHub (como na etapa 11).
