---
arquivo_original: "Slides - IA Aplicada nas Licitações.pdf"
hash_pdf_md5: eb84209b45572d33769fb413d51b9efc
paginas: 33
metodo: "OCR tesseract por"
convertido_em: 2026-10-03T17:19:55
fonte: Base de Conhecimento CLC
---

<!-- pagina 1 (OCR) -->
. Licitadores.
com

.“

aplicada nas licitações

<!-- pagina 2 (OCR) -->
o Conceitos Introdutórios

0 e Principais Riscos

e Principais Ferramentas de IA Generativa

<!-- pagina 3 (OCR) -->
Led.O . que.é IAGenerativa?

A Inteligência Artificial Generativa se refere a um ramo da |A capaz de criar ou sintetizar conteúdo novo a
partir de um conjunto de dados existentes ou de instruções fornecidas pelo usuário (por exemplo, um
comando de texto conhecido como “prompt”). Em vez de apenas analisar dados, a IA generativa pode
produzir textos, imagens, vídeos, sons ou até códigos de programação.

Exemplo simples: Um sistema de IA generativa pode elaborar um rascunho de Termo de Referência para
uma licitação usando modelos de linguagem capazes de entender e reproduzir a estrutura típica de

documentos de compras públicas.

Essa vertente da IA vem ganhando destaque por possibilitar a criação de propostas de documentos e
soluções automatizadas, algo especialmente útil para quem trabalha em ambientes de alta demanda

burocrática, como as contratações no setor público.

CONCEITOS INTRODUTÓRIOS <& Licitadores.

<!-- pagina 4 (OCR) -->
1.2 Relevância da IA Generativa
para Compras Públicas

No contexto das compras governamentais, várias etapas — como d
elaboração de editais, a escolha de fornecedores e a pesquisa de
preços — exigem grande volume de documentos e de análise.

AIA generativa pode:

* —Aceleraraescrita de minutas, editais e contratos.

* —Facilitara verificação de cláusulas ou termos que não podem
faltar nos documentos de contratação.

* —Apoiar a produção de relatórios e de estimativas de custo de
forma mais ágil, desde que seja cuidadosamente treinada ou
orientada via prompts adequados.

Por outro lado, também levanta preocupações quanto a risco de

vazamento de dados, inclusão de informações equivocadas e

excesso de confiança na máquina, temas que serão explorados

adiante (Tópico 2).

<!-- pagina 5 (OCR) -->
E AAAA A .

Para facilitar a compreensão dos próximos capítulos, seguem alguns termos que aparecerão

frequentemente:

Algoritimo

Conjunto de instruções ou
regras que determinam como
um problema será resolvido. Na
IA, algoritmos são usados para

processar dados e tomar

decisões ou gerar conteúdo.

Aprendizado de Máquina

(Machine Learning)

Técnica na qual o sistema “aprende" a partir de
exemplos (dados) e cria modelos que generalizam
esses padrões. Pode ser supervisionado (quando há
rotulagem de dados) ou não supervisionado (quando

o modelo detecta padrões por conta própria).

Aprendizado Profundo (Deep Learning)

Subconjunto de aprendizado de máquina que utiliza redes neurais

complexas para identificar padrões em grandes quantidades de dados. É a

base de muitos sistemas de |lA generativa.

ConcEITOS INTRODUTÓRIOS — «& Licitadores.

<!-- pagina 6 (OCR) -->
Prompt

Instrução textual (ou de outro formato) fornecida pelo usuário a um modelo de IA. Em geral, a IA "lê”

o prompt e gera uma resposta (texto, imagem etc.). No contexto de compras, um prompt pode

descrever o tipo de documento ou análise que se deseja criar.

Grandes Modelos de Linguagem
(Large Language Models)

Modelos treinados em imensas bases de texto
capazes de compreender e gerar linguagem
natural de forma contextualizada. Exemplos incluem
ChatGPT, Claude e outros.

Viês (Bias)

Tendência de um modelo de |A em
produzir resultados desbalanceados
ou discriminatórios caso tenha sido

treinado em dados que já possuíam

algum tipo de distorção.

Dados Sensíveis Redes Neurais

Informações cujo uso indevido pode Arquiteturas computacionais inspiradas no
causar prejuízos às pessoas ou às funcionamento do cérebro humano. São
instituições (por exemplo, dados formadas por camadas de "neurônios" que
pessoais, informações sigilosas sobre processam informações e aprendem por meio
licitações etc.). de exemplos.

ConcEITOS INTRODUTÓRIOS — « Licitadores.

<!-- pagina 7 (OCR) -->
+ Modelos de Linguagem

São sistemas treinados para compreender e gerar texto.

Contam com bilhões de parâmetros que aprendem

probabilisticamente a prever a próxima palavra ou frase.

Exemplos de utilização:

* Geração de Documentos: Minutas para termos de
referência, pareceres, notas técnicas, impugnações e
recursos, por exemplo.

* Auxílio na Revisão: Indicação de ajustes ou melhorias
em cláusulas contratuais, análise de planilhas, etc.

Quanto mais dados consistentes e variados o modelo de

linguagem recebe durante seu desenvolvimento, maior a

Cchance de oferecer respostas coerentes e adaptáveis a

diferentes contextos do setor público.

' EIToí

V

CONC

<!-- pagina 8 (OCR) -->
+ Redes Neurais

Embora também sustentem os modelos de linguagem, redes neurais podem ser aplicadas a diversos fins,
como análise deimagem, previsões de séries históricas e classificação de dados. No contexto de compras
públicas, costumam ser usadas "por trás dos panos ' em sistemas que:

* Identificam anomalias em propostas de fornecedores.

* Classificam grandes volumes de documentos para facilitar a localização de informações.

As redes neurais profundas (Deep Learning) são versões mais complexas que envolvem múltiplas
camadas e permitem que o sistema “aprenda” nuances e padrões mais complexos, como é o caso dos
robôs de controle do TCU: ALICE (Análise de Licitações e Editais), SOFIA (Sistema de Orientação sobre Fatos
e Indícios para o Auditor), ADELE (Análise de Dlsputa em Licitações Eletrônicas), MARINA (Mapa de Riscos

nas Aquisições), dentre outros.

. Licitadores.
com

n
O
a
f
()
Z
Q
O

<!-- pagina 9 (OCR) -->
2.1 Vazamento.de.Dacdos

Por que é um risco? Em ferramentas de |A generativa, geralmente
fornecemos prompts que contêm informações contextudais.
Quando esses dados são sensíveis ou confidenciais (por
exemplo, identificação de servidores, detalhes de contratos ou
estratégias de compra), podem ocorrer vazamentos se a
ferramenta estiver conectada à internet ou se não houver
mecanismos adequados de segurança. Além disso,
dependendo da natureza do dado vazado, a instituição pode
enfrentar processos administrativos ou até sofrer sanções.
Exemplo prático: Um servidor copia trechos de documento com
identificação de servidores e insere em um chatbot público para
verificar possíveis melhorias na redação de um relatório. Se a
plataforma não tiver uma política de privacidade robusta, há
risco de que o conteúdo se torne acessível a outros usuários,
mesmo que involuntariamente.

Se um usuário insere trechos inteiros de um Termo de Referência
confidencial em uma plataforma aberta de I1A, corre o risco de
expor estratégias de contratação ou informações que não

deveriam ser divulgadas.

PRINCIPAIS RISCOS <& Licitadores

<!-- pagina 10 (OCR) -->
2.2 Enviescamentos.ísios)

Por que é um risco? Modelos de IA são treinados em grandes bases
de dados, que podem conter padrões discriminatórios ou
desequilibrados. Mesmo que a ferramenta informe que são
apenas dados sem censura, isso pode afetar a objetividade em
sugerir textos de editais ou na avaliação de fornecedores.

Exemplo prático: O algoritmo pode sugerir frases que excluem
determinadas modalidades de participação ou grupos de
fornecedores, reproduzindo preconceitos presentes no conjunto
de dados de treinamento.

2.3,confiabilidade.cdas,Respostas

Por que é um risco? O sistema gera conteúdo com base em
probabilidades, não em certezas. Ele pode "alucinar" (como se diz
no jargão) e produzir informações incorretas, ainda que expressas
com aparente firmeza.

Exemplo prático: Um modelo de IA gera cláusulas contratuais com
boas intenções, mas omite pontos obrigatórios por força de lei,
induzindo ao erro quem não revisar cuidadosamente o conteúdo.

PRINCIPAIS RISCOS <& Licitadores

<!-- pagina 11 (OCR) -->
2.A Excesso.deAutomeação

* Porqueéumrisco? Confiar cegamente no modelo de lA pode levar a
decisões automatizadas sem revisão humana. O "viés de
automação" ocorre quando assumimos que a máquina está
sempre certa.

* Exemplo prático: Utilizar o output de IA para avaliar a melhor
proposta de fornecedor, sem que um servidor verifique a coerência
das condições ou o histórico de atendimento daquela empresa em
outras contratações, ou mesmo se a legislação utilizada como base
está correta.

2.9,Usonão adequado das ferramentas

adcres.

* —Por que é um risco? Algumas plataformas externas não são

-

=
Ácn
)

autorizadas para uso institucional, conforme a política de
segurança de informações da entidade. Mesmo uma simples
consulta informal pode ferir regras de sigilo ou compliance.

* —Exemplo prático: Fornecedores inserirem dados estratégicos
(como margens de lucro ou planos de expansão) em uma

ferramenta pública de 1A, e essa informação ficar disponível ou ser

)
o
O
&
a
2)
&
o
<
a
[e

rastreável por concorrentes.

<!-- pagina 12 (OCR) -->
2.2 Boaus.Práticas.Gerais

para Servidores e Fornecedores

Validação humana constante +

Mesmo que a 1A ofereça um "rascunho” ou

sugestão de texto, a revisão por um profissional é

obrigatória. Nenhuma ferramenta substitui a

capacidade humana de interpretar nuances legais

e contextuais.

* Dica: Crie um fluxo de trabalho onde todo
documento gerado pela IA passe por do menos

um revisor que verifique coerência, adequação

u

legal e aderência à política institucional.

+ Não inserir dados sensíveis em plataformas externas

Ferramentas públicas, como ChatGPT, Gemini, Claude e similares, armazenam dados para aprimorar
seus modelos. Caso seja necessário trabalhar com informações restritas, busque soluções aprovadas ou
homologadas pela instituição, conforme recomenda o “Guia de uso de IA generativa no TCU”.

* Dica: Se for indispensável usar uma IA não corporativa, faça a anonimização ou produza versões

simplificadas dos dados, de modo a protegerinformações sigilosas.

PRINCIPAIS RISCOs & Licitadores.

<!-- pagina 13 (OCR) -->
+ Transparência nos processos

Mantenha um registro de quais partes do documento foram geradas pela IA e quais foram revisadas ou
acrescentadas manualmente. A rastreabilidade facilita eventuais auditorias e assegura
responsabilização adequada:.

* Dica:Inclua notas no arquivo (ex: "Seção X foi gerada por A; verificada em [data] por [responsável]").

Diversidade de dados e testes +

Para mitigar o risco de viés, recomendar-se que alA seja testada com conjuntos de dados diversos ou com
cenários que representem a pluralidade de fornecedores e situações. Assim, é possível identificar se o
modelo tem preferências injustificadas ou omissões relevantes. Importante ressaltar que vieses sempre
existirão, pois toda ferramenta é produzida e revisada por humanos, carregando consigo seus vieses.

Dica: Conduza testes de uso 'às cegas”, comparando propostas geradas pela |A e por pessoas diferentes,

para ver se há disparidades notáveis.

+ Definição de políticas e treinamentos internos

Políticas Internas: Elabore normas claras sobre em quais casos a IA pode (ou não) ser usada, e quais
etapas exigem revisão humana obrigatória.
Treinamentos: Ofereça capacitações para servidores e fornecedores, explicando os riscos de se confiar

cegamente na tecnologia e como proceder na prática.

PRINCIPAIS RISCOs & Licitadores.

<!-- pagina 14 (OCR) -->
2.3,Orientações inspiradas.em guias .oficiais

O "Guia de uso de |A generativa no TCU" traz recomendações específicas para uso responsável de IA em

órgãos públicos, entre elas:

* Validaçãohumana de todo conteúdo gerado e responsabilidade do autor, mesmo no uso de lA.

* Cauteladgoinserir informações confidenciais em soluções de terceiros, bem como uso preferencial de
soluções aprovadas pela própria instituição.

* Evitardecisões automatizadas sem supervisão, pois o 'viés de automação'" e possíveis 'alucinações' da

IA podem induzir a erros difíceis de rastrear.
* Esses princípios podem ser adaptados para cada realidade, mas servem de norte no momento de

regulamentar ou promover o uso de ferramentas de |A generativa.

PRINCIPAIS RISCOS <& Licitadores

<!-- pagina 15 (OCR) -->
Principais ferramentas de IA generativa

Neste capítulo, analisaremos algumas das
ferramentas de IA generativa mais conhecidas do
mercado, apresentando suas funcionalidades, du $%
vantagens, desvantagens e a existência de
versões gratuitas ou pagas. Também discutiremos
como essas ferramentas podem ser aplicadas
para otimizar processos de compras públicas, e
que tipo de cuidado se deve ter ao utilizá-las para

finsinstitucionais.

Licitadores:

com

”

Existem muitas outras, para geração de imagens,

músicas, vídeos e muito mais. No entanto, neste

ANBAVA

momento vamos nos ater à produção e análise de
documentos com as ferramentas que hoje são as

mais interessantes.

PRINCIPAIS FERRAMENTAS DE IA GENER

<!-- pagina 16 (OCR) -->
+ ChatGPT

&

O Chat6GPT é um modelo de linguagem desenvolvido pela OpenAl, amplamente utilizado para gerar

respostas a perguntas, criar textos e resumir informações. Ele funciona por meio de um chat interativo, em

que o usuário insere um prompte recebe respostas sequentciais.

Vantagens

* —Interfaceconversacionalintuitiva.

* — Versatilidadenageração de conteúdos.

* — Suporte para upload de documentos e
acesso àdinternet.

* — Recursos avançados de voz e vídeo na
versão Plus.

* —Opçãogratuitaeversãopagacom mais
funcionalidades.

* —Personalização com GPTs treinados
(versão Plus).

* Tarefas semiautomatizadas (versão

Plus) e agentes próprios (versão Pro).

Desvantagens:
* —“Riscodeexposição de dados sensíveis.
* — Possibilidade de gerar informações erradas, especialmente sobre|eis.

* —Dependênciados servidores da OpenAl, podendo haver instabilidades.

Planos/ Versões

* — Gratuito: acesso sujeito a sobrecarga e com funcionalidades reduzidas;
limite de uso diário relativamente baixo para produção de documentos.

* — Pago (ChatGPT Plus): prioridade de acesso e eventuais melhorias de
modelo, acesso ao Sora para geração de vídeo, limites extendidos de
uso e acesso dos modelos o03- mini, o3-mini-high, and ol.

* — Pago (ChatGPT Pro): o melhor que a ferramenta tem, acesso a todos os

modelos, inclusive o Operator (apenas nos EUA).

Aplicações em Compras Públicas
* — Geraçãodeminutas de editais, termos de referência, justificação de preços, análise de documentos

de concorrentes, busca de falhas ou incoerências em propostas, etc.

* —Consultarápidadeideias preliminares

PRINCIPAIS FERRAMENTAS DE IA GENERATIVA <& Licitadores.

<!-- pagina 17 (OCR) -->
Gemini :
G |

De

senvolvido pela Google DeepMind, o Gemini reúne modelos de linguagem de alta performance para

múltiplas tarefas de |A. Integra vários serviços do ecossistema Google.

Vantagens Desvantagens:
Forte integração com Google Workspace, Drive, Cloud etc. Ainda em desenvolvimento, comete muitos erros de

Infraestrutura sólida de pesquisa, prometendo alto compreensão do contexto e do que se pede no prompt.
desempenho, principalmente em cálculos. excesso de proibições em suas políticas.

Pode processar grandes volumes de dados, útil em Dependência do Google Cloud e possíveis custos para
projetos robustos de compras públicas. integrações avançadas.

Pode acessar a internet em temporeal. Assim como outros modelos, não há garantia de

respostas 100% corretas.

Planos/ Versões

* Versãogratuita (limitada) e versão paga, que custa 99 reais por mês e inclui o Goo One, armazenamento na nuvem e outras
vantagens..

* —Integração empresarial exige assinatura de serviços Google Cloud.

Aplicações em Compras Públicas

* —Análisesavançadas de editais e documentos com auxílio do Google Cloud.

* —Traduçãoesumarização de conteúdos internacionais para parcerias e projetos.

. Licitadores

com

PRINCIPAIS FERRAMENTAS DE IA GENERATIVA

<!-- pagina 18 (OCR) -->
+ Claude

é Claude

Claude é o assistente de IA da Anthropic, com foco em segurança e alinhamento ético, projetado para

minimizar riscos associados a modelos de linguagem. É o que possui a escrita mais fluida, muito

interessante para produção de relatórios, Termo de Referência, ETPs e pareceres.

Vantagens
* — Priorizasegurança e alinhamento ético, fundamental em entes governamentais.
* —Interação porlinguagem natural, com atualizações frequentes de segurança.

* —Preocupação em reduzir enviesamentos e respostas indevidas.

Desvantagens:

* — Paracálculos, existem opções mais interessantes.

* —Podeterlimitações em certos idiomas ou domínios jurídicos locais.

* — Necessita supervisão humana permanente para uso em processos críticos, pois

"se cansa rápido" e começa a produzir “'mais do mesmo”.

Planos/ Versões

* —Gratuito com restrição no
número de acessos.

* — PlanoPro custa 110 reais por
mês e permite 5x mais uso
que a versão gratuita, além
de acesso a modelos mais
avançados.

* —PlanoTeam custa 135 reais
por membro e tem maior
quantidade de uso
disponível

Aplicações em Compras Públicas

* — Geraçãoderelatóriosetextos com menorrisco de conteúdo duvidoso.

* — Acompanhamento de legislação e normas, com verificação local posterior.

PRINCIPAIS FERRAMENTAS DE IA GENERATIVA <& Licitadores.

<!-- pagina 19 (OCR) -->
Brok Ã/l

Menos famoso que outros modelos, foi criado pelo grupo de Elon Musk e está conextado dao X (antigo
Twitter). É focado em análise de dados e suporte à tomada de decisão e gera excelentes respostas, com
menos censura que as demais plataformas.Tem ênfase em resumir grandes bases textuais e encontrar

padrões.

Vantagens Planos/Versões
* —Idealpara quemlida com volume alto de dados históricos de * Ofertas Enterprise com preços mais elevados

compras ou fornecedores. voltadas para grandes organizações.
Geração de insights e relatórios executivos para a tomada versão beta está disponível para usuários do X

de decisão. gratuitamente, por enquanto.
Oferta de segurança empresarial, útil para órgãos públicos.

Desvantagens:

Menor reconhecimento no mercado e comunidade mais reduzida, até por ser muito recente.
App só está disponível para Apple, em breve estará disponível no Android.

Possíveis limitações de funcionalidades em certos idiomas ou termos técnicos.

Integração com sistemas internos pode exigir acordos específicos ou implementação custosa.

Aplicações em Compras Públicas

* —Análisedefornecedores, simulação de cenários de custo, projeções de demanda.

* — Produção derelatórios para comissões de licitação, consolidando dados.

* —Perguntastécnicas.

. Licitadores

com

PRINCIPAIS FERRAMENTAS DE IA GENERATIVA

<!-- pagina 20 (OCR) -->
+ DeepSeek

Q' deepseelk

O DeepSeek combina busca semântica avançada e IA generativa, auxiliando tanto na localização de

documentos quanto na criação de sínteses. É uma ferramenta Open Source desenvolvida na China.

Vantagens
* —“Rapidezaofiltrareindexar documentos
* Integração potencial com sistemas de gestão documental (via APIs).

Desvantagens:
* —Configuraçãocomplexa paraindexar grandes repositórios internos.
* Naanálisedeleisbrasileiras da área de licitações se mostrou péssimoa.

* —Ajustedeidioma e terminologias jurídicas pode demorar para ser satisfatório.

* — Podereduzirtempo de preparação de minutas ao reunir informações de várias fontes.

Planos/ Versões

* —Gratuito (opensource)

AMENTAS DE IA GENERATIVA <& Licitadores.

<!-- pagina 21 (OCR) -->
Perplexity

1) perplexity

Conhecido como "“buscador inteligente”, o Perplexity oferece respostas rápidas e curtas, muitas vezes

indicando as fontes originais de onde extraiu a informação. Quando você se acostumar com ele, vai largar

o Goodle.

Vantagens

* —Informaasfontes consultadas, permitindo
verificação de confiabilidade.
Facilidade de uso, como se fosse um
buscador em linguagem natural.
Bom para consultas pontuais de temas
específicos ou estatísticas rápidas.
Sugere perguntas e dá prosseguimento a
uma pesquisa mais apurada.
Mostra as fontes imediatamente.

Desvantagens:
Pode não apresentar profundidade necessária para gerar minutas

complexas.
Depende de dados da web, que podem estar incompletos ou

desatualizados.

Planos/ Versões
* Em geral, você consegue fazer quase tudo na versão gratuita, mas na
versão Pro você tem acesso a pesquisas mais apuradas. Se tiver o plano

da Vivo, consegue acessar a versão Pro gratuitamente..

Aplicações em Compras Públicas

* —Quicksearch de dúvidas sobre requisitos legais, verificando referências oferecidas.

* — Pesquisas preliminares de mercado, embora sem garantias de profundidade ou atualidade

total.

Licitadores
WV com

PRINCIPAIS FERRAMENTAS DE IA GENERATIVA

<!-- pagina 22 (OCR) -->
3.L-Critérios.de escolha-da-ferramenta

Ao decidir por uma das plataformas, não esqueça de avaliar:

* Segurançae Privacidade (adequação a leis e normas internas).
* SuporteeEstabilidade (SLA, atualizações, comunidade ativa).
* Compeatibilidade (APIs, formatos de arquivo, infraestrutura local).

* IdiomaeContexto (ferramenta está preparada para o português e para textos jurídicos?).

* “Custo-Benefício (planos pagos versus limitações de versões gratuitas).

PRINCIPAIS FERRAMENTAS DE 1A GENERATIVA — & Licitadores.

<!-- pagina 23 (OCR) -->
4.1 o que é um prompt?

Um prompt é a instrução ou pedido inicial que o usuário
faz a uma IA generativa. Em compras públicas, pode
assumir diferentes formas: solicitação de rascunho de
documento, pesquisa sobre legislação ou até sugestões
para estrutura de editais. Quanto mais claro e
contextualizado for o prompt, maior a chance de a
resposta ser útil e coerente.

AA generativa utiliza esse prompt como ponto de partida
para "imaginar" a resposta. Isso se dá por meio de
modelos de linguagem que analisam padrões extraídos
de bilhões de dados de texto, oferecendo um resultado
que combina lógica probabilística com capacidades de
síntese. Embora o mecanismo interno seja complexo, para
o usuário o prompt funciona como uma simples linha de

comando ou texto inserido em uma caixa de diálogo.

"
()
dm
o
)
2E
co
—O

<!-- pagina 24 (OCR) -->
4.2 Engenharia.de.Prompt

A engenharia de prompt é a prática de elaborar, testar e refinar
esses pedidos iniciais, de modo que a IA produza respostas cada
vez mais aderentes às necessidades do usuário. Isso envolve
tanto aspectos técnicos (uso de termos-chave, estrutura do
texto) quanto de contexto (proporcionar detalhes sobre o objetivo
ourestrições da tarefa).

Alguns princípios podem orientar a criação de prompts eficazes:

* — Abertura com objetivo claro.

* Especificação de formato ou nível de detalhamento.

* Contextualização com dados essenciais (prazos, legislações,
escopos).

* Solicitaçãode exemplos ou simulações, quando necessário.

Licitadores
&V com

PROMPTS

<!-- pagina 25 (OCR) -->
4.2 Engenharia.de.Prompt

Para compras públicas, a boa engenharia de prompt possibilita a

geração de minutas iniciais de documentos, guias de conduta

para fornecedores e até apoio em pesquisas de mercado.

Contudo, é indispensável a revisão humana posterior, evitando

uso automático de respostas potencialmente equivocadas.

A construção de um bom prompt varia conforme a ferramenta

que você está usando e conforme o objetivo que se pretende

atingir, mas no caso de elaboração de ETPs, TR, pareceres,
impugnações e recursos, o ideal é que você utilize a seguinte
estrutura:

* Definiçãode Contexto: Descreva a situação e o problema a ser
enfrentado.

* —“Objetivos: Descreva com algum detalhe os objetivos a serem
atingidos (busque ter poucos objetivos, para não confundir a
máquina.

* Meta:Oquevocê espera da ferramenta de 1A que está usando.

* Fonte: Apresente as possíveis fontes de busca e solicite que as
fontes que a 1A utilizou além das indicadas por você sejam
adequadamente referenciadas.

(
o
A
3
)
ZE
.2o
nO

PROMPTS

<!-- pagina 26 (OCR) -->
+ Exemplo de Prompt

í í Em um município brasileiro, a prefeitura de LINDESAS DO SUL abriu uma licitação para a compra de
móveis de escritório para suprir as necessidades dos prédios administrativos e educacionais da
cidade. O processo segue as diretrizes da Lei nº 14.133/202], que trata das regras para licitações e
contratos na administração pública. No entanto, surgiram questionamentos sobre a
conformidade do processo licitatório, especialmente em relação à escolha inadequada de uma
modalidade de licitação e à possível restritividade dos itens presentes no edital. É necessário que
um parecer jurídico seja elaborado para esclarecer esses pontos.

Me ajude a Analisar o Processo Licitatório, considerando minimamente o seguinte:
l. — Examinar a modalidade de licitação escolhida.

2. —Avaliara conformidade do edital em relação à legislação vigente.

3. Identificar possíveis cláusulas restritivas ou ilegais no edital.

Vocêdeve:

1. — Sugerir ajustes necessários no edital para assegurar a legalidade do processo.

2. Orientarsobre procedimentos corretivos adequados.

3. —Fornecer uma análise jurídica detalhada sobre a validade e transparência do
processo.

4. Indicar os riscos potenciais do prosseguimento do processo licitatório nos
termos atuais.

<!-- pagina 27 (OCR) -->
í í Quero que você faça uma análise minuciosa, juridicamente embasada e detalhada de cada

aspecto do edital e do processo licitatório. A Lei 14.133/202] deve ser seguida e você deve me

ajudar garantir um processo mais justo e transparente.

Caso utilize decisões de Tribunais de Contas ou doutrinas especializadas em seu trabalho, cite a

fonte e o link para conferência.

Veja que este prompt foi completo, com tudo o que citei anteriormente. Você pode fazer desta forma ou

passo a passo, o que não pode é fazer prompts ruins, como o daimagem a seguir:

Hoje

As mensagens são geradas pos 1À Algumas respostas podem ser
Incorrétas ou mudequadas Saibo mais

consegue gerar uma imagem do homem aranha
bananeira?

plantando

1024 H

Neste exemplo, por mais que possa
parecer que a IA errou, ela fez um
trabalho perfeito. QUem errou aqui
foi o usuário que pediu à IA para
gerar uma imagem do Homem
Aranha plantando bananeira, sem
explicar o que vem a ser isso.
Lembre-se de que "plantar
bananeira" é uma gíria brasileira, e
essas ferramentas, em sua maioria,
são estrangeiras e podem não
entender a linguagem coloquial em
alguns casos.

. Licitadores.
com

PROMPTS

<!-- pagina 28 (OCR) -->
4.3,.ITrêsmocdelos.de Prompt para fornecedores

A seguir, veremos três modelos ilustrativos, com objetivos específicos, que podem ser usados por
fornecedores do interagirem com IA generativa na preparação de documentos ou estratégias de
participação em licitações. Cada um pode ser adaptado conforme o contexto do órgão público, objeto da

licitação ou legislação local.

Prompt1- Redaçãoinicial de proposta comercial

"Preciso elaborar uma proposta comercial para participar de uma licitação de [nome do objeto]. A
proposta deve destacar diferenciais técnicos e evidenciar minha capacidade de entrega no
prazo. O formato de texto preferido é o XYZ, os tópicos relevantes (qualificações, histórico de
entregas semelhantes, garantias) estão no documento em anexo. A proposta deve conter
também os dados da minha empresa e forma de pagamento”".

Este prompt deixa claro o objetivo (elaboração de uma proposta), especifica o tema (licitação de
um objeto) e pede tópicos relevantes (qualificações e garantias), viabilizando um rascunho que o

fornecedor possa refinar.

. Licitadores

com

<!-- pagina 29 (OCR) -->
Prompt 2 — Pesquisa prévia de preços e
referências

"Quero levantar informações de mercado
sobre [produto/serviço específico] para
embasar minha proposta em uma
licitação pública. Liste fontes possíveis de
pesquisa de preços, aspectos de
qualidade e principais riscos que eu,
enquanto fornecedor, devo considerar ao
demonstrar competitividade e solidez.'
Com esse prompt, o fornecedor obtém
um panorama de fontes de pesquisa e
boas práticas para sua proposta, usando

a IA como ponto de partida. Cabe dao

fornecedor validar cada item sugerido.

Prompt 3 - Análise de cláusulas
contratuais comuns

"Pretendo participar de licitações na área de
[setor X] e quero conhecer as cláusulas
contratuais mais frequentes nesse tipo de
contrato público. Pesquise no PNCP e em
outras fontes e me apresente exemplos
reais de editais de órgãos federais,
estaduais e municipais. Após, resuma as
principais cláusulas que geralmente
aparecem e explique o objetivo de cada
cláusula e como meu negócio pode se
preparar para atender a essas exigências.'
O foco aqui é educar o fornecedor,
oferecendo uma visão geral das cláusulas
obrigatórias ou recorrentes. A 1A listará
exemplos, mas o fornecedor deve checar se

refletem a legislação e o contexto regional.

. Licitadores.
com

PROMPTS

<!-- pagina 30 (OCR) -->
4.4 Três modelos de Prompt para planejamento
da contratação e seleção do fornecedor

Agora, três exemplos de prompts que podem ser usados por servidores ou equipes responsáveis pelo

planejamento e pela seleção de fornecedores, cada um direcionado a uma etapa específica do processo.

Prompt1- Elaboração de Termo de Referência

"Preciso elaborar um Termo de Referência para aquisição
de [descrever objeto] em uma autarquia federal. O TR
deve conter minimamente:

a) Definição do objeto: natureza, quantitativos, prazo do
contrato e possibilidade de prorrogação.

b) Fundamentação: referência a estudos técnicos
preliminares ou extrato das partes não sigilosas.

c) Descrição da solução: abrangendo todo o ciclo de
vida do objeto.

d) Requisitos da contratação.

e) Modelo de execução: definição de como o
contrato produzirá os resultados esperados.

f) Modelo de gestão: acompanhamento e
fiscalização da execução.

g) Critérios de medição e pagamento.

h) Critérios de seleção do fornecedor.

i) Estimativa do valor: preços unitários referenciais,
memórias de cálculo e parâmetros utilizados.

j) Adequação orçamentária.

O documento deve seguir a estrutura da Lei
14.133/202]. A IA pode gerar um rascunho para

revisão e complementação, agilizando o processo.

. Licitadores

com

<!-- pagina 31 (OCR) -->
Prompt 2- Análisederiscos

«"Estou planejando uma licitação para contratação de serviços de [tipo de serviço]. Liste os principais riscos que
podem ocorrer (operacionais, financeiros, jurídicos) e sugira formas de mitigação, considerando legislações e boas
práticas de órgãos de controle no Brasil. Peço exemplos específicos de cláusulas preventivas que podem ser incluídas
no edital ou contrato.»

Aqui, a IA tende a apresentar uma visão ampliada de riscos e cláusulas, ajudando no planejamento do processo. Ainda

assim, cabe dao servidor verificar se as sugestões estão alinhadas às regras do próprio órgão e às exigências locais.

Prompt3- Análise deriscos

"Preciso estruturar critérios de habilitação e julgamento para selecionar o melhor fornecedor em um processo de
compra de [produto/serviço]. Explique como equilibrar requisitos técnicos, experiência prévia, saúde financeira e
ofertas de preço. Traga exemplos de pontuação ou metodologia de julgamento que atenda aos princípios da Lei X
(caso exista uma lei específica).»

O resultado desse prompt pode auxiliar o servidor a delinear metodologias de pontuação, contemplando aspectos
técnicos e de preço. Ao final, a equipe deve adaptar o que foi sugerido às normas e à realidade orçamentária.

e.

Licitadores
á com

<!-- pagina 32 -->
O uso de prompts bem elaborados é decisivo para 
extrair o melhor das ferramentas de IA generativa. 
Para fornecedores, eles ajudam na preparação de 
propostas, estudos de mercado e conhecimento 
de cláusulas comuns. Para os servidores, apoiam 
a criação de documentos como Termos de 
Referência, matrizes de risco e critérios de seleção. 
Ainda assim, a aplicação prática exige validação 
humana e respeito às normas institucionais de 
segurança e privacidade.
www.rafaelmota.pro
rafaelmota.pro
rafaelmotapro
contato@rafaelmota.pro

<!-- pagina 33 (OCR) -->
O futuro é
