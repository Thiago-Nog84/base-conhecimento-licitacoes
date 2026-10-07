"""Preenche as secoes vazias dos boletins 06, 07 e 08/2026 no consolidado Guia Lici 2026 (etapa 12).
Texto: OCR (tesseract, 400 dpi) revisado manualmente contra a imagem dos PDFs.
Seguranca: confere o MD5 esperado da versao atual, faz backup e so substitui secoes vazias.
Grava na mestra e no clone (que precisam estar identicos antes).
"""
import hashlib, os, shutil, datetime, sys

REL = r'02_Jurisprudencia_e_Orientacoes\Informativos_Guia_Lici\Boletim Guia Lici - Consolidado Anual 2026.md'
MESTRA = os.path.join(r'C:\Users\thiagonogueira\OneDrive - mppi.mp.br\CLC\01_Processos_e_Aquisicoes\Base de Conhecimento - Thiago', REL)
CLONE = os.path.join(r'C:\Users\thiagonogueira\Dev\base-conhecimento-licitacoes', REL)
BACKUP = r'C:\Users\thiagonogueira\Claude\backup_md'
MD5_ESPERADO = '54709dd95f476dbbab0b975a69f3b941'
NOTA = '> Transcrição revisada: OCR do PDF-imagem conferido manualmente com a imagem original em 04/10/2026.'


def lp(p):
    return '\\\\?\\' + os.path.normpath(p)


def md5(p):
    return hashlib.md5(open(lp(p), 'rb').read()).hexdigest()


B06 = NOTA + '''

**BOLETIM INFORMATIVO Nº 06/2026 — COORDENADORIA DE LICITAÇÕES E CONTRATOS**

📝 **Tema Principal:** O que é a data do orçamento estimado?

🎯 **Objetivo**

Evitar confusões sobre a **data-base para reajustes contratuais**, garantindo que ela seja corretamente identificada e documentada para preservar o **equilíbrio econômico-financeiro do contrato**.

📌 **Definição**

A **data do orçamento estimado** é o **momento oficial em que a Administração consolida a pesquisa de preços** para definir o valor estimado da contratação, servindo como **referência temporal para reajustes contratuais** (Lei 14.133/2021, art. 92, §3º).

⚖️ **Base legal essencial**

- **Lei nº 14.133/2021, art. 25, §7º:** o edital deve prever índice de reajustamento com **data-base vinculada à data do orçamento estimado.**
- **Art. 92, §3º:** o reajuste segue a **data do orçamento estimado pela Administração**, iniciando a contagem anual.
- **IN SEGES/ME nº 65/2021 e jurisprudência TCU:** materialização da pesquisa de preços em documento oficial na fase preparatória **(art. 18)**.

🔎 **O que deve ser observado**

- A data é o momento da **consolidação oficial da pesquisa de mercado** (ex.: ata ou relatório de preços).
- **No MP/PI, consideramos especificamente a data da última assinatura do mapa comparativo de preços** como data do orçamento estimado.
- Vincula **índices de reajuste**, não a data da proposta ou assinatura do contrato.
- Em inexigibilidade ou obras, pode ser a data da assinatura da planilha orçamentária ou proposta exclusiva.

⚠️ **Erros frequentes**

- Confundir com **data da proposta vencedora ou assinatura do contrato**.
- **Não documentar explicitamente nos autos do processo**.
- Ignorar em reajustes, levando a **contagens erradas de periodicidade**.
- Omitir no Termo de Referência **(TR)**, deixando indefinida para o contrato.

✅ **Boas práticas**

- No Estudo Técnico Preliminar **(ETP)**, planeje a pesquisa e registre a data prevista.
- No **TR**, justifique a **data-base (no MP/PI: última assinatura do mapa comparativo)** e junte comprovantes (Painel de Preços, cotações).
- Teste compatibilidade de preços e informe explicitamente nos artefatos preparatórios da contratação.
- Diferencie de repactuação em serviços com **dedicação exclusiva.**

📎 **Lembrete final:** A data inadequada compromete reajustes, **atrai questionamentos do TCU** e distorce a execução contratual. **No MP/PI, sempre utilize a data da última assinatura do mapa comparativo de preços**, documente e vincule ao orçamento estimado para **conformidade legal.**

📢 "A boa gestão das contratações públicas depende da atualização contínua sobre jurisprudência e boas práticas."

✍️ Elaborado por: Assessoria para Gerenciamento de Licitações/CLC/MPPI.'''

B07 = NOTA + '''

**BOLETIM INFORMATIVO Nº 07/2026 — COORDENADORIA DE LICITAÇÕES E CONTRATOS**

📝 **Tema Principal:** Matriz de Riscos Genérica

🎯 **Objetivo**

Orientar sobre o uso adequado da matriz de riscos genérica na fase preparatória das licitações, destacando limites, riscos e boas práticas.

❓ **Definição**

A **matriz de riscos** é cláusula contratual que distribui responsabilidades por eventos futuros que possam afetar o equilíbrio econômico-financeiro do contrato.

A **matriz genérica** é um modelo padronizado, aplicável a contratações simples, desde que adaptado ao caso concreto.

⚖️ **Base legal essencial**

- Lei nº 14.133/2021: arts. 6º, XXVII; 18, X; 22; 103, §§ 4º a 6º
- Obrigatória em:
  - Obras e serviços de grande vulto
  - Contratação integrada e semi-integrada

🔎 **Mapa × Matriz de Riscos**

O **Mapa de riscos (ETP/TR):** identifica e analisa riscos (planejamento), enquanto a **matriz de riscos (edital/contrato):** distribui responsabilidades (cláusula vinculante).

📊 **Estrutura básica**

- Risco identificado
- Responsável (Administração/contratado/compartilhado)
- Medidas preventivas e mitigadoras
- Impacto econômico-financeiro

⚠️ **Riscos da matriz genérica**

- Não refletir o objeto específico
- Gerar sobrepreço ou licitação deserta
- Comprometer o reequilíbrio contratual
- Desconexão com ETP, TR e orçamento
- Possível irregularidade em casos obrigatórios

🏛️ **Diretriz do TCU**

A matriz deve:

- Ser específica para o contrato
- Ser compatível com projeto e orçamento
- Considerar a capacidade de gestão de cada parte
- Evitar uso automático de modelos

✅ **Boas práticas**

- Adaptar modelos ao caso concreto
- Integrar com ETP e TR
- Considerar contratações anteriores
- Prever medidas reais de mitigação

📎 **Lembrete final**

A matriz de riscos não é formalidade. Seu uso genérico, sem adaptação, pode comprometer a contratação e gerar prejuízos à Administração.

📢 "A boa gestão das contratações públicas depende da atualização contínua sobre jurisprudência e boas práticas."

✍️ Elaborado por: Assessoria para Gerenciamento de Licitações/CLC/MPPI.'''

B08 = NOTA + '''

**BOLETIM INFORMATIVO Nº 08/2026 — COORDENADORIA DE LICITAÇÕES E CONTRATOS**

📝 **Tema Principal:** Esclarecimentos Vinculam a Administração - Cuidado na resposta a pedidos de esclarecimento e impugnações

⚖️ **Base normativa**

- A **IN SEGES/ME nº 73/2022**, em seu art. 16, prevê que qualquer pessoa pode impugnar o edital ou solicitar esclarecimentos sobre seus termos. O § 1º dispõe que o agente de contratação poderá requisitar subsídios formais aos responsáveis pela elaboração do edital e dos anexos. Já o § 4º é expresso ao estabelecer que as respostas aos pedidos de esclarecimentos e impugnações vinculam os participantes e a Administração.
- No mesmo sentido, o **Acórdão nº 799/2026 – Plenário/TCU** reafirmou que os esclarecimentos oficiais passam a integrar o instrumento convocatório, não sendo admissível, na fase de habilitação ou julgamento, interpretação diversa da que foi formalmente prestada.

🎯 **O que isso significa na prática?**

- Quando a equipe de planejamento elabora ou subsidia resposta a esclarecimento ou impugnação, ela não está apenas prestando informação complementar: ela pode estar **definindo o sentido oficial do edital, do TR e dos anexos.**
- Por isso, a resposta dada **obriga a Administração** e deverá ser observada por todos na análise posterior.

🧭 **Cuidados essenciais da equipe de planejamento**

- Revisar previamente o ETP, o TR e os anexos antes de responder;
- Garantir que a resposta seja clara, precisa e completa, sem lacunas ou ambiguidades;
- Ter atenção redobrada em temas como **qualificação técnica, prazos, quantitativos, critérios de julgamento e requisitos de habilitação;**
- Evitar respostas apressadas ou genéricas, que possam alterar a compreensão do edital sem a devida cautela;
- Quando a inconsistência for relevante, avaliar a necessidade de **retificação formal do edital ou de seus anexos.**

❌ **Erros que devem ser evitados**

- Responder sem conferir a redação original do TR e dos anexos;
- Dar resposta lacônica a dúvida complexa;
- Tentar aplicar, depois, interpretação mais restritiva ou diferente da resposta oficial;
- Tratar o esclarecimento como ato informal, sem efeito vinculante.

📎 **Lembrete final**

- Esclarecimentos e respostas a impugnações **integram as regras do certame.** Assim, respostas imprecisas, contraditórias ou incompletas podem gerar **inabilitações indevidas, violação ao instrumento convocatório, retorno de fase, anulação de atos, atraso no certame e prejuízo à competitividade.** Planejar bem também é responder com responsabilidade.

📢 "A boa gestão das contratações públicas depende da atualização contínua sobre jurisprudência e boas práticas."

✍️ Elaborado por: Assessoria para Gerenciamento de Licitações/CLC/MPPI.'''

for p in (MESTRA, CLONE):
    if md5(p) != MD5_ESPERADO:
        sys.exit(f'MD5 inesperado (arquivo mudou?), nada alterado: {p}')

t = open(lp(MESTRA), encoding='utf-8', newline='').read()
crlf = t.count('\r\n')
if crlf and crlf != t.count('\n'):
    sys.exit('fins de linha mistos (CRLF e LF), nada alterado')
eol = '\r\n' if crlf else '\n'
t = t.replace('\r\n', '\n')
trocas = [
    ('## Boletim informativo 07 2026 1\n\n\n\n---', '## Boletim informativo 07 2026 1\n\n' + B07 + '\n\n---'),
    ('## Boletim informativo 082026\n\n\n\n---', '## Boletim informativo 082026\n\n' + B08 + '\n\n---'),
]
for velho, novo in trocas:
    if t.count(velho) != 1:
        sys.exit('secao vazia nao encontrada exatamente 1 vez, nada alterado: ' + velho.splitlines()[0])
    t = t.replace(velho, novo)
cab06 = '## Boletim_informativo_06_2026'
i = t.find(cab06)
if i < 0 or t[i + len(cab06):].strip():
    sys.exit('secao 06 nao esta vazia no fim do arquivo, nada alterado')
t = (t[:i] + cab06 + '\n\n' + B06 + '\n').replace('\n', eol)

stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
bk = os.path.join(BACKUP, f'{stamp}_Boletim Guia Lici - Consolidado Anual 2026.md')
shutil.copy2(lp(MESTRA), lp(bk))
assert md5(bk) == MD5_ESPERADO
for p in (MESTRA, CLONE):
    open(lp(p), 'w', encoding='utf-8', newline='').write(t)
print('backup:', bk)
print('novo md5 mestra:', md5(MESTRA), '| clone:', md5(CLONE))
