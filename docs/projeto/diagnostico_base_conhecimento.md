# Diagnóstico da Base de Conhecimento — CLC (02/09/2026)

Levantamento da árvore completa da pasta `CLC` (que engloba tanto a "Base Legal CLC" quanto a pasta do processo "Manutenção Predial - Lote III" já conectadas à sessão). Objetivo: identificar o que está inflando o volume de dados que preciso varrer/ler, e o que pode ser removido, movido ou convertido para formato mais leve.

## Panorama geral

- **5.730 arquivos**, **623 pastas**, **8,54 GB** de tamanho lógico total.
- Curiosidade: `du -sh` (espaço realmente ocupado em disco) acusa só **1,3 GB**. A diferença (~7,2 GB) é típica de arquivos do OneDrive marcados como "somente online" (placeholders, não baixados localmente) — não é um problema em si, mas mostra que boa parte do que está "catalogado" na pasta nem está disponível localmente agora.

## Achado #1 — Pasta "Instaladores": 4,74 GB que não são base de conhecimento

`CLC/Instaladores` contém **17 arquivos executáveis** somando **4,74 GB** — mais da metade (55%) de todo o peso lógico da pasta CLC. São instaladores de programas, não documentos:

| Arquivo | Tamanho |
|---|---|
| OllamaSetup.exe | 1.829 MB |
| Docker Desktop Installer.exe | 630 MB |
| FoxitPDFReader...Setup...exe | 376 MB |
| postgresql-16.14-2-windows-x64.exe | 349 MB |
| GoogleDriveSetup.exe | 306 MB |
| Antigravity.exe / Antigravity IDE.exe | 234 + 218 MB |
| jdk-26_windows-x64_bin.exe | 189 MB |
| GitHubDesktopSetup-x64.exe | 181 MB |
| VSCodeUserSetup-x64.exe | 133 MB |
| + Git, node, python-manager, etc. | ~150 MB |

**Ação recomendada:** mover essa pasta inteira para fora da árvore do OneDrive/CLC (ex.: `C:\Instaladores` na raiz do usuário, fora de qualquer pasta sincronizada). Ganho imediato: -4,74 GB, risco zero (são apenas instaladores, facilmente redownloadáveis se precisar).

## Achado #2 — .zip duplicando pastas já extraídas: ~301 MB redundantes

Dos 39 arquivos `.zip` (382,5 MB no total), **301,5 MB já têm uma pasta irmã com exatamente o mesmo nome contendo os arquivos extraídos** — ou seja, o conteúdo existe duas vezes: compactado e descompactado, lado a lado.

Exemplos:
- `Pedido Rescisão - L N CASTAGNARO LTDA/SEI_19.21.0016.0030965_2025_22.zip` (97,7 MB) + pasta `SEI_19.21.0016.0030965_2025_22/` já extraída
- `Locação Leste .../SEI_19.21.0438.0028275_2025_71.zip` (67,4 MB) + pasta extraída homônima
- `Coleta de Lixo/Processo antigo/SEI_19.21.0010.0007609_2021_42.zip` (28,7 MB) + pasta extraída

**Ação recomendada:** conferir rapidamente 2-3 casos e, confirmando que a pasta extraída tem o mesmo conteúdo, apagar o `.zip` (mantendo só a pasta com os arquivos soltos, que é o formato mais útil para consulta).

## Achado #3 — 591 grupos de arquivos duplicados exatos (mesmo nome + mesmo tamanho): ~179 MB

Padrão mais comum: dentro da pasta de um processo, os anexos do SEI aparecem **soltos** na pasta principal *e de novo* dentro de uma subpasta `SEI_xxxxxxxx/` (aparentemente um export completo do processo feito depois que os anexos já tinham sido baixados individualmente). Casos recorrentes: "Locação Leste" (7+ arquivos duplicados), "Serpro - BCadastro" (5+ arquivos), "Conectores RJ-45 e Alicates EZ Crimp" (2 arquivos ~15 MB).

Caso à parte, mais estrutural: o modelo **`modelo-de-termo-de-referencia-servicos-e-obras-lei-no-14-133-dez-25.docx`** está copiado manualmente em **7 processos diferentes** (Coleta de Lixo, Aluguel de Decoração, Hospedagem, Media Training, e também em Base Legal/Modelos). Isso é sintoma de um problema maior que só espaço em disco: se esse modelo for atualizado, as 6 cópias "esquecidas" nos processos ficam desatualizadas sem ninguém perceber.

**Ação recomendada:** gero um script que lista os 591 grupos com os caminhos completos para você revisar antes de apagar (não vou apagar nada sem confirmação). Para o modelo de TR: manter 1 cópia canônica em `Base Legal/Modelos` e, nos processos, referenciar por link/atalho em vez de copiar.

## Achado #4 — "_ARQUIVAR" (762 MB) e "Dev_Arquivado" (90 MB): já sinalizados como não-ativos, mas ainda dentro da árvore ativa

- `Base Legal CLC - Atualizada Maio.2026/_ARQUIVAR` — 762 MB, majoritariamente manuais/apostilas em PDF (o próprio nome já diz "para arquivar"). Se não é consultado no dia a dia, mantê-lo fora do escopo ativo da Base Legal reduz bastante o que preciso varrer quando você pede algo como "veja o que temos sobre X na Base Legal".
- `Dev_Arquivado/` — 90 MB, incluindo um projeto de código legado (`pca-mppi-legado`, React + Supabase). Não é conteúdo jurídico/administrativo — é resíduo de desenvolvimento e não deveria estar dentro da pasta de processos do CLC.

**Ação recomendada:** mover ambos para uma pasta separada fora do escopo "ativo" (ex.: `CLC_Arquivo_Historico` fora da árvore principal, ou pelo menos fora das pastas conectadas à sessão do Claude).

## Achado #5 — Resíduo de teste de desenvolvimento dentro de um processo real: 1.904 arquivos

Dentro de `Assessoria de Compras/PGEAs/Inexigibilidades/Curso Reforma Tributária -19.21.0012.0021262_2026_63 -/Teste/`, há uma instalação completa de `node_modules` (biblioteca `pdf-parse` e dependências) — **1.904 arquivos**, ou seja, **33% de todos os arquivos da pasta CLC inteira estão concentrados nesse resíduo de teste**, dentro da pasta de um processo de licitação real. Tamanho em bytes é pequeno, mas o volume de arquivos por si só torna qualquer varredura da pasta de Inexigibilidades muito mais pesada do que precisa ser.

**Ação recomendada:** apagar a subpasta `Teste/` inteira (é claramente um experimento esquecido, não faz parte do processo).

## Achado #6 — PDFs escaneados sem texto pesquisável: os mais caros de eu processar

Testei os 19 maiores PDFs da base com `pdftotext`/`pdfinfo`: **12 não têm nenhum texto extraível** — são digitalizações puras (imagem), sem OCR. Isso inclui:

- Um manual de **1.042 páginas, 33,6 MB**, sem texto algum (`_ARQUIVAR/Manuais.../...`)
- Vários PDFs de 30-200 MB reportados como "1 página" (provavelmente um único objeto de imagem gigante por página do SEI)

Isso é o achado mais diretamente ligado ao seu consumo de tokens: um PDF nativo em texto custa uma fração do que custa um PDF escaneado, porque eu preciso "olhar" cada página como imagem em vez de ler o texto. Os PDFs "com texto extraível" da amostra (normativos, boletins de jurisprudência TCE-PI, manual TCU) já estão em bom formato.

**Ação recomendada:** rodar OCR (ex.: `ocrmypdf`) nos PDFs de referência que você consulta com frequência — normativos, manuais, boletins — para adicionar uma camada de texto pesquisável sem perder a imagem original. Não vale a pena fazer isso em autos de processo (esses eu leio pontualmente, não geram custo recorrente).

## Por extensão (visão geral)

| Extensão | Arquivos | Tamanho |
|---|---|---|
| .exe | 17 | 4.556 MB |
| .pdf | 2.269 | 2.960 MB |
| .zip | 39 | 382 MB |
| .pptx | 10 | 97 MB |
| .html | 765 | 85 MB |
| .docx | 243 | 38 MB |
| .xlsx | 51 | 20 MB |
| .js/.ts/.tsx/.json/.bcmap/.properties (resíduo dev) | ~1.700 | ~22 MB |

(727 dos 765 `.html` estão em `Assessoria de Compras/PGEAs` — em geral e-mails/páginas do SEI exportadas junto com os processos; volume aceitável, baixa prioridade.)

## Plano de ação priorizado

1. **Mover `Instaladores/` para fora do OneDrive/CLC** → -4,74 GB, risco zero.
2. **Apagar a pasta `Teste/` (resíduo de node_modules)** dentro de "Curso Reforma Tributária" → -1.904 arquivos, risco zero.
3. **Apagar os `.zip` que já têm pasta extraída homônima** (conferir 2-3 antes) → -301 MB.
4. **Mover `_ARQUIVAR` (762 MB) e `Dev_Arquivado` (90 MB)** para fora do escopo ativo/conectado → reduz superfície de varredura da Base Legal.
5. **Revisar os 591 grupos de duplicata exata** (~179 MB) com uma lista que posso gerar para você aprovar antes de apagar.
6. **Consolidar o modelo de TR duplicado em 7 processos** → 1 cópia canônica em Base Legal/Modelos.
7. **OCR nos PDFs de referência sem texto** (não nos autos de processo) → reduz custo de leitura recorrente.

Se os passos 1, 2 e 3 forem feitos, o volume lógico cai de 8,54 GB para cerca de 2,7 GB (~-68%) removendo essencialmente só lixo — nenhum conteúdo jurídico é tocado.

---
*Gerado a partir de varredura da pasta `CLC` em 02/09/2026. Nenhum arquivo foi apagado ou movido — este documento é só o diagnóstico.*
