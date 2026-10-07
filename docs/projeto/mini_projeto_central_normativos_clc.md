# Mini Projeto: Central de Normativos e Orientações Processuais da CLC

**Subtítulo:** Complementação da página institucional da Coordenadoria de Licitações e Contratos (CLC) no portal do MPPI

---

## 1. Identificação do Projeto

| Campo | Informação |
|---|---|
| Unidade proponente | Assessoria de Compras — Coordenadoria de Licitações e Contratos (CLC/MPPI) |
| Responsável técnico | [nome do servidor] (Chefe da Assessoria de Compras) |
| Ambiente de publicação | Portal institucional MPPI (`www.mppi.mp.br/internet`) |
| Página-base existente | `/internet/coordenadoria-de-licitacoes-e-contratos/legislacoes/` |
| Data de elaboração | 10/09/2026 |
| Unidade gestora do CMS/publicação | *[INFORMAÇÃO NÃO CONSTANTE NOS AUTOS]* — a confirmar junto à Coordenadoria de Comunicação Social/CTI, responsável usual pela publicação de conteúdo no portal institucional |

---

## 2. Contexto e Diagnóstico da Situação Atual

O portal institucional do MPPI é construído em **WordPress**, com um modelo de página padronizado para unidades administrativas: cabeçalho comum, menu principal (*Institucional · Áreas de Atuação · Serviços · Contato*), **menu lateral próprio de cada Coordenadoria** e conteúdo publicado em blocos de artigo.

A CLC já possui menu lateral estruturado em quatro grupos temáticos:

| Grupo do menu lateral | Itens publicados | URL base |
|---|---|---|
| Institucional e Contato | Apresentação · Equipe · Fale Conosco | `/apresentacao/` `/equipe/` `/contatos-2/` |
| Processos e Planejamento | Processos–Fluxos CLC · Plano Anual de Contratação · Manifestação Jurídica Referencial (MJR) | `/processos-fluxos-clc/` `/…plano-anual-de-contratacao/` `/mjr/` |
| Contratações e Aquisições | Contratações Diretas · Licitações · Contratos e Equivalentes · Compras e ACT's | `/contratacoes-diretas/` `/` `/contratos-e-equivalentes/` `/?page_id=183564` |
| Suporte e Informações | Informativos · **Normativos sobre Licitações e Contratos** · Modelos | `/informativos-clc/` `/legislacoes/` `/modelos/` |

### 2.1. Achado central — lacuna de conteúdo

A página **"Normativos sobre Licitações e Contratos"** (`/legislacoes/`) já está estruturada em três blocos: *Legislação Federal*, *Legislação Estadual* e *Normativos MPPI*. Os dois primeiros estão povoados (tabela "Normativo | Descrição | Acesso" seguida de lista expandida com ementa e link). **O bloco "Normativos MPPI" está publicado apenas como título de seção, sem nenhum conteúdo abaixo.** É exatamente essa lacuna que a presente iniciativa propõe preencher.

Adicionalmente, não existe hoje nenhuma página ou seção consolidada de *orientações sobre como instruir os processos*. O conteúdo mais próximo está disperso em:

- **"Processos–Fluxos CLC"** — lista apenas as quatro assessorias da CLC (ASSGERLICT, ASSPROCLI, ASSCOMPRAS, ASSGECONT), sem conteúdo orientativo visível associado;
- **"MJR" (Manifestação Jurídica Referencial)** — pareceres-modelo organizados por hipótese (*Dispensa*, *Prorrogação de Vigência ARP*, *Adesão–Carona*, *Pagamento por Indenização*, *Troca de Marca*);
- **"Modelos"** — links para os modelos padrão AGU adotados pelo **Ato PGJ/PI nº 1382/2024**, mais a obra *"Licitações & Contratos: Orientações e Jurisprudência do TCU"*.

### 2.2. Inconsistências técnicas identificadas na página atual

| Nº | Inconsistência | Localização | Evidência |
|---|---|---|---|
| 1 | Todos os botões "▶" de acesso da tabela de Legislação Federal apontam para a mesma URL (Decreto 10.818/2021), independentemente da linha (ex.: Lei 8.666/1993 e Lei 14.133/2021 levam ao mesmo link) | `/legislacoes/` — tabela "Legislação Federal" | Verificado por leitura da árvore de acessibilidade da página |
| 2 | Erro de digitação recorrente "licit ação" (espaço interno indevido) | `/legislacoes/` — descrições da tabela | Idem |
| 3 | Referência normativa com erro de dígito: "Ato PGJ/PI n°. 1382/**2**2024" | `/modelos/` | Idem |
| 4 | Descrição do Decreto Estadual nº 21.872/2023 truncada ("Regulamenta a Lei Federal nº , de 1º de Abril de 2021…"), com o número da lei federal deslocado para um link solto na sequência | `/legislacoes/` — bloco "Legislação Estadual" | Idem |
| 5 | Seção "Normativos MPPI" publicada sem conteúdo | `/legislacoes/` | Idem |

*Estes achados devem ser tratados como débito técnico a sanar no mesmo ciclo de publicação, e não apenas como preenchimento de conteúdo novo — ver seção 9 (Alerta de Conformidade).*

---

## 3. Justificativa

A ausência de compilação acessível dos normativos internos do MPPI sobre licitações e contratações, e a dispersão das orientações de instrução processual em páginas sem conexão navegacional entre si, geram dois riscos operacionais: *(i)* dificuldade de localização de base normativa vigente por parte de requisitantes e da própria equipe da CLC, aumentando o risco de instrução processual desalinhada com os normativos internos; *(ii)* uso de canais informais (e-mail, WhatsApp, repositórios pessoais) para disseminação de modelos e orientações, o que compromete a rastreabilidade e a atualização única da informação — um dos pilares da governança documental exigida pela **Lei nº 14.133/2021** e pelo princípio da publicidade.

---

## 4. Objetivos

**Objetivo geral:** completar a arquitetura de informação já existente na página da CLC, transformando-a em referência única e confiável de normativos e orientações para instrução de processos de contratação no MPPI.

**Objetivos específicos:**

1. Preencher o bloco "Normativos MPPI" da página `/legislacoes/` com os Atos PGJ, Portarias e demais normativos internos aplicáveis a licitações e contratações;
2. Consolidar, em ponto único de acesso, a navegação entre "Processos–Fluxos CLC", "MJR" e "Modelos", hoje desconectados entre si;
3. Corrigir as cinco inconsistências técnicas identificadas na Seção 2.2;
4. Estabelecer rotina de atualização e responsável formal pela manutenção do conteúdo publicado.

---

## 5. Escopo

| Em escopo | Fora de escopo |
|---|---|
| Preenchimento do bloco "Normativos MPPI" em `/legislacoes/` | Criação de conteúdo didático inédito (tutoriais passo a passo) — *decisão registrada: consolidar o que já existe, não criar guia novo* |
| Criação de bloco/seção de navegação consolidada entre Fluxos CLC, MJR e Modelos | Alteração do template visual/CSS do portal (fora de governança da CLC) |
| Correção das 5 inconsistências técnicas mapeadas | Abertura de acesso público/externo — *decisão registrada: público interno* |
| Definição de fluxo de atualização periódica do conteúdo | Migração de plataforma (WordPress) |

---

## 6. Arquitetura de Informação Proposta

Mantém-se a estrutura de menu lateral já consolidada pelo usuário do site, com uma inclusão pontual:

| Grupo | Situação atual | Proposta |
|---|---|---|
| Suporte e Informações | Informativos · Normativos sobre Licitações e Contratos · Modelos | Sem alteração de rótulos — **conteúdo interno** de "Normativos sobre Licitações e Contratos" passa a incluir o bloco "Normativos MPPI" completo |
| Processos e Planejamento | Processos–Fluxos CLC · Plano Anual de Contratação · MJR | "Processos–Fluxos CLC" passa a incluir, junto à lista das 4 assessorias, links diretos para as peças correspondentes do MJR e dos Modelos aplicáveis a cada fluxo |

> *Observação:* a opção por reaproveitar a arquitetura existente (em vez de criar itens novos no menu) evita fragmentar ainda mais a navegação — problema que o próprio diagnóstico da Seção 2 evidenciou.

---

## 7. Especificação de Conteúdo por Seção

### 7.1. Bloco "Normativos MPPI" (em `/legislacoes/`)

Deve seguir o **mesmo modelo tabular já usado** nos blocos de Legislação Federal e Estadual, garantindo uniformidade visual:

| Coluna | Conteúdo esperado |
|---|---|
| Normativo | Tipo e número (ex.: *Ato PGJ/PI nº 1382/2024*) |
| Descrição | Ementa resumida, sem truncamento (corrigindo o padrão observado no achado nº 4) |
| Acesso | Link individual e correto para cada documento (corrigindo o achado nº 1) |

*Fonte de dados sugerida:* pasta local conectada **"Base Legal CLC – Atualizada Maio.2026"** e o levantamento já em andamento de *Atos PGJ* (ver memória de projeto, atualização iniciada em 10/09/2026). Cabe validar quais atos dessa base são de publicidade externa obrigatória antes da inclusão.

### 7.2. Consolidação de navegação (Fluxos CLC · MJR · Modelos)

Não se propõe conteúdo textual novo, e sim **pontes de navegação** entre páginas já existentes, por assessoria/hipótese:

| Assessoria (Fluxos CLC) | MJR relacionada | Modelos relacionados |
|---|---|---|
| ASSGERLICT — Gerenciamento de Licitações | *Dado não disponível — mapear caso a caso* | Modelos para pregão e concorrência |
| ASSPROCLI — Pareceres em Processos Licitatórios | *Dado não disponível — mapear caso a caso* | Modelos para pregão e concorrência (obras) |
| ASSCOMPRAS — Assessoria de Compras | Dispensa · Adesão–Carona · Pagamento por Indenização · Troca de Marca | Modelos para Contratação Direta |
| ASSGECONT — Gestão de Contratos | Prorrogação de Vigência ARP | Modelos para Termos Aditivos |

*O mapeamento acima é uma hipótese de trabalho baseada na natureza de cada assessoria; deve ser validado com os titulares de cada uma antes da publicação.*

---

## 8. Papéis e Responsabilidades

| Papel | Responsável | Observação |
|---|---|---|
| Levantamento e curadoria do conteúdo normativo | Assessoria de Compras (CLC) | Já em andamento (atualização de Atos PGJ desde 10/09/2026) |
| Validação jurídica da compilação | *Dado não disponível* | A definir se caberá à CONINT ou à própria CLC |
| Publicação/edição no CMS do portal | *Dado não disponível* | Normalmente atribuição da Coordenadoria de Comunicação Social/CTI — confirmar fluxo de solicitação |
| Atualização periódica | Assessoria de Compras (CLC) | Sugere-se periodicidade mínima semestral ou por evento normativo |

---

## 9. Alerta de Conformidade

- *A publicação de compilação normativa em página institucional gera, perante terceiros e órgãos de controle, presunção de que a informação está vigente e correta.* A manutenção do bloco "Normativos MPPI" vazio, ou a persistência de links incorretos (achado nº 1) e descrições truncadas (achado nº 4), representa risco de **informação oficial incompleta ou equivocada** veiculada em canal público do órgão, com potencial repercussão perante a Lei de Acesso à Informação (Lei nº 12.527/2011) e o princípio constitucional da publicidade (**art. 37, *caput*, CF/88**).
- Recomenda-se que a correção das inconsistências técnicas (Seção 2.2) seja tratada como **pré-requisito** de publicação do novo conteúdo, e não como ajuste posterior — publicar conteúdo novo sobre uma base já com erros de referenciação normativa amplia o risco em vez de mitigá-lo.
- A responsabilidade formal pela publicação/edição do CMS e pela validação jurídica da compilação normativa **não está confirmada** nesta análise (marcada como *Dado não disponível* nas Seções 1 e 8). Recomenda-se formalizar essas definições, preferencialmente por despacho ou expediente interno, antes do início da execução.
- O mapeamento de correspondência entre Assessorias, hipóteses de MJR e Modelos (Seção 7.2) é uma **hipótese de trabalho** e não deve ser publicado sem validação dos titulares de cada assessoria, sob risco de direcionar servidores a peças processuais inaplicáveis ao caso concreto.
- Recomenda-se estabelecer rotina formal de revisão periódica do conteúdo normativo publicado (Seção 8), evitando a repetição do cenário hoje observado (seção publicada e posteriormente deixada incompleta).

---

## 10. Próximos Passos Sugeridos

1. Validar este mini projeto com a chefia da CLC;
2. Levantar, na pasta "Base Legal CLC", a lista definitiva de Atos PGJ/normativos internos a compilar no bloco "Normativos MPPI";
3. Corrigir os 5 achados técnicos junto à unidade responsável pelo CMS;
4. Validar o mapeamento Assessoria × MJR × Modelos com os titulares de cada assessoria;
5. Solicitar formalmente à unidade gestora do portal a publicação do conteúdo consolidado.
