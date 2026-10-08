# Pipeline e ferramentas

Scripts em [`../ferramentas/`](../ferramentas/), cópias dos originais em `C:\Users\thiagonogueira\Claude\scripts`. Os caminhos (`ROOT`, `BASE`, `REPO`) estão no topo de cada script, e os CSVs de entrada e saída ficam em `C:\Users\thiagonogueira\Claude`. As cópias desses CSVs estão em [`controle/`](controle/).

## Requisitos
- Python 3 com `pymupdf`, `pymupdf4llm`, `pytesseract`, `Pillow`, além de `lxml` e `openpyxl`, usados na conversão de .docx/.xlsx, e `olefile`, usado na de .doc.
- Tesseract 5.4 com o idioma `por` em `%LOCALAPPDATA%\Programs\Tesseract-OCR\tesseract.exe`.
- `git` (com `core.longpaths=true`) e `gh` autenticado como `Thiago-Nog84`.

## Fluxo
| # | Script | Entrada | Saída | Função |
|---|---|---|---|---|
| 1 | `analise_pares.py` | `mapa_pares_pdf_md.csv` | `mapa_pares_pdf_md_v2.csv` | Classifica os PDFs sem .md (texto/escaneado) e faz o *match* por nome |
| 2 | `comparar_conteudo.py` | v2 + todos os .md da mestra | `comparacao_conteudo_pdf_md.csv` | Similaridade por conteúdo (*shingles* + índice invertido) |
| 3 | `plano_copia_md.py` | comparação | `plano_copia_md_pares_iguais.csv` | Seleciona pares seguros (≥ 0,90, .md único) |
| 4 | `executar_copia_md.py` | plano (status OK) | `log_copia_md.csv` | Copia o .md para o nome do PDF; confere o hash |
| 5 | `montar_piloto.py` | comparação | `lista_piloto.csv` | 20 PDFs DISTINTOS de pastas variadas |
| 6 | `converter_pdf_md.py <lista.csv> [--saida-dir DIR] [--log CSV]` | qualquer CSV com a coluna `CaminhoPDF` | `.md` ao lado do PDF + `log_conversao.csv` | Conversão PDF → MD |
| 7 | `qa_conversao.py` | `log_conversao.csv` (ou outro log) | `qa_conversao.csv` | Audita os .md: cobertura de palavras, `�`, negrito quebrado, linhas repetidas, recuos (só originais PDF) |
| 8 | `carregar_repo.py` | logs acima | clone + `log_carga_repo.csv` | Copia .md e PDFs pareados da mestra para o clone (não sobrescreve; .doc/.docx/.xlsx nunca vão) |
| 9 | `substituir_piloto_v2.py` | `log_conversao.csv` + log da v2 | `backup_piloto_v1\` + `log_substituicao_piloto_v2.csv` | Uso único: trocou os .md do piloto pela v2, com backup |
| 10 | `montar_lotes.py` | comparação + plano + `log_conversao.csv` | `lotes\lista_completa.csv`, `lotes\lote_NN.csv`, `lotes\fora_dos_lotes.csv` | PDFs ainda sem .md, menos infográficos, em lotes de 50 (com texto primeiro, depois OCR) |
| 11 | `rodar_lote.py NN` | `lotes\lote_NN.csv` | `lotes\log_lote_NN.csv`, `lotes\qa_lote_NN.csv` | Converte, audita, acrescenta as linhas OK em `log_conversao.csv` e roda `carregar_repo.py` |
| 12 | `substituir_md.py` | log de uma reconversão feita com `--saida-dir` | backup + log | Troca .md já convertidos pelos reconvertidos, com backup e hash (só com autorização) |
| 13 | `mover_downloads.py <plano.csv>` | plano com as colunas `grupo`, `origem`, `destino` | `log_movimentacao_downloads.csv` | Move arquivos aprovados para a mestra com o nome novo. Checa o plano inteiro antes (origem existe, destino livre, pasta existe) e confere o MD5 antes e depois |
| 14 | `registrar_lote.py <log_lote.csv>` | log de um lote | `log_conversao.csv` | Acrescenta as linhas OK ao log mestre sem duplicar (para lotes convertidos fora do `rodar_lote.py`) |
| 15 | `enriquecer_md.py <log_lote.csv> <meta.py>` | log do lote + dicionário `META` (ementas verificadas) | .md enriquecido + `backup_md\enriquecimento\` | Acrescenta o front-matter semântico, o título e a ementa. Pula o .md que já tem `tipo:` |
| 16 | `preencher_guialici_2026.py` | consolidado Guia Lici 2026 (MD5 esperado) | mestra + clone + backup | Uso único: preencheu as seções vazias dos boletins 06 a 08/2026 com a transcrição revisada |
| 17 | `converter_office_md.py <lista.csv> [--log CSV] [--saida-dir DIR]` | CSV com a coluna `CaminhoArquivo` | `.md` ao lado do original + log no formato de `log_conversao.csv` | Conversão .docx/.xlsx/.doc → MD (ver abaixo). Ignora outros formatos e nunca sobrescreve |
| 18 | `qa_office.py <log_lote.csv> <saida.csv>` | log de um lote de Office | `lotes\qa_lote_NN_office.csv` | Cobertura de palavras contra o texto do original, além de tabelas, títulos, listas, imagens e notas |
| 19 | `anonimizar_md.py <log_lote.csv> <regras.py> [--front-matter]` | log do lote + `REGRAS = [(rotulo, regex, substituicao)]` | .md anonimizado + `backup_md\anonimizacao\<data>\` + `log_anonimizacao.csv` | Troca dados pessoais por marcadores só no corpo (front-matter intacto). Com `--front-matter`, aplica também ao cabeçalho, para .md autorais cujo cabeçalho tem conteúdo. Idempotente. O arquivo de regras e o log **não** são versionados |
| 20 | `modelo_docx.py <original.docx> <modelo.docx> <regras.py>` | documento real + `REGRAS` (mesmo formato) | modelo .docx com marcadores | Troca os dados do caso por marcadores no XML (corpo, cabeçalhos, rodapés, notas), preservando a formatação. Apaga autor e "modificado por" dos metadados. Nunca sobrescreve. As regras (`lotes\modelo_*.py`) **não** são versionadas |
| 21 | `gerar_indice_por_fase.py` (opções `--lista`, `--escrever`, `--aplicar`, `--substituir`) | `mapa_indice.py` (mapa curado) + `apendices_proposta.md` + .md do clone | `00_Indice_por_Fase_da_Contratacao.md` na raiz da mestra (e do clone, na troca) + `backup_md\indice\` | Gera o índice por fase da contratação. Confere que cada padrão do mapa casa com um só .md, presente na mestra e no clone, e só grava sem pendências. `--escrever` faz o rascunho fora da base; `--aplicar` grava na mestra e recusa sobrescrever; `--substituir` troca na mestra **e no clone**, cada um com backup (só com autorização). Os arquivos ficam em `docs/controle/indice/` |

Uso do conversor:
```
python converter_pdf_md.py <lista.csv> [--saida-dir DIR] [--limite N] [--log CSV]
python qa_conversao.py [log.csv] [saida.csv]
```
Lógica do conversor (v2):
1. Uma página vai para OCR se tiver menos de 100 caracteres de texto ou 5 ou mais `�` (glifos sem mapeamento Unicode).
2. Se até 20% das páginas precisam de OCR, a conversão usa `pymupdf4llm.to_markdown(page_chunks=True)`, e o OCR é feito só nessas páginas, **na posição original**. Acima de 20%, faz OCR em todas as páginas.
3. Se o markdown tiver mais de 15 ocorrências de `**x**` (letras isoladas em negrito), a conversão troca para `get_text(sort=True)` e colapsa os espaços de diagramação.
4. Cabeçalhos e rodapés (v2.1): uma linha com mais de 15 caracteres, fora de tabela, que aparece **na borda** da página (entre as 4 primeiras ou as 4 últimas linhas não vazias) em pelo menos 40% das páginas é mantida só na primeira ocorrência. Em documentos com menos de 10 páginas, o limite sobe para 75%. Mínimo de 3 páginas; não se aplica a documentos com menos de 4 páginas. As ocorrências no meio do texto são preservadas. Isso evita apagar conteúdo que se repete de verdade, como o nome do órgão ou a situação "RETIRADO DE PAUTA" nas pautas do TCE-PI.
5. Páginas com mais de 8.000 px de altura passam por OCR em faixas, porque o limite do Tesseract é 32.767 px. O DPI do OCR é adaptativo: parte de 250 e desce de 10 em 10 (mínimo de 72) enquanto a largura passar de 8.000 px ou a área passar de 150 milhões de pixels. Isso evita o `DecompressionBombError` do Pillow em páginas gigantes.
6. Cada página começa com o marcador `<!-- pagina N -->`, ou `<!-- pagina N (OCR) -->`. `�` restantes são informados no campo `metodo` do front-matter.
7. O conversor nunca sobrescreve um .md existente.

Conversão de Office (`converter_office_md.py`):
- **.docx:** o script lê o XML (`zipfile` + `lxml`). Parágrafos e tabelas saem na ordem do documento, e os títulos vêm do estilo. A numeração das listas é calculada, e as caixas de seleção viram `- [ ]`. Controles de conteúdo e caixas de texto entram no texto, e o texto do cabeçalho vai no início. As imagens são marcadas como *[imagem]* e as notas de rodapé vão para o fim. O texto excluído em revisão é ignorado.
- **.xlsx:** uma seção por planilha, com uma tabela markdown de valores calculados, sem as linhas e colunas vazias.
- **.doc (Word 97-2003):** o script lê o arquivo OLE com `olefile` e extrai o texto do corpo pela tabela de peças (CLX), sem precisar do Word nem do antiword. Sai um parágrafo por linha; dos campos fica só o resultado. Títulos e listas não são reconhecidos. Documentos criptografados dão erro.
- **Front-matter:** `arquivo_original`, `hash_arquivo_md5`, `formato`, `planilhas` (só .xlsx), `metodo`, `convertido_em`, `fonte`.
- Sequência usada nos lotes 08 e 09:
  1. `converter_office_md.py` (e `converter_pdf_md.py` para os PDFs do mesmo lote);
  2. `qa_office.py` e `qa_conversao.py`;
  3. `anonimizar_md.py`;
  4. `enriquecer_md.py`;
  5. `registrar_lote.py`;
  6. `carregar_repo.py`;
  7. se o lote trouxe arquivo que cabe numa fase da contratação, acrescentá-lo ao `mapa_indice.py` e regerar o índice com `gerar_indice_por_fase.py --aplicar --substituir` (com autorização).

  Anonimizar e enriquecer **antes** da carga é obrigatório, porque `carregar_repo.py` não sobrescreve o que já está no clone. Pelo mesmo motivo, as obras comerciais entram no `.gitignore` antes da carga, para nunca aparecerem como arquivos novos no `git add`.

Troca de um .md existente pela conversão do PDF (só com autorização do usuário; usada nos lotes 10, 11 e 12, etapas 20, 24 e 25):
  1. converter com `--saida-dir` numa pasta temporária, porque o conversor não sobrescreve, e enriquecer lá;
  2. fazer backup do .md antigo em `backup_md\substituicao\`;
  3. trocar na mestra e no clone por arquivo temporário + `os.replace`, nunca gravando por cima, porque o .md pode ter hard links em caches do app;
  4. registrar MD5 antes e depois em `docs/controle/log_substituicao_md.csv`;
  5. corrigir o caminho do .md (da pasta temporária para o destino na mestra) no log e no QA do lote e nas linhas que `registrar_lote.py` acrescentou a `log_conversao.csv`. Passe a `--saida-dir` um caminho absoluto: com caminho relativo, o conversor falha.

**Infográficos ficam fora** da lista de conversão (decisão do usuário): a pasta `Infograficos_Zenite` e os PDFs de uma página com altura maior que 3× a largura.

## Publicação
```
cd D:\00_ATIVO\Dev\base-conhecimento-licitacoes
git add -A
git status --short | findstr /I ".pdf"   # deve sair vazio
git commit -m "..."
git push
```

## Classes da comparação
`IGUAL` ≥ 0,60 · `PROVAVEL_REVISAR` 0,25–0,60 · `DISTINTO` < 0,25 · `SEM_TEXTO_SUFICIENTE` (menos de 20 *shingles*) · `ERRO_LEITURA`.
