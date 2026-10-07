---
tipo: "Manual Operacional de Sistema"
numero: "3.5.0"
ano: 2026
orgao: "Governo Federal / MGI / Contratos.gov.br"
status: "Vigente / Manual Operacional"
assunto: "Guia técnico para fornecedores contratados sobre acesso, envio de notas fiscais, acompanhamento de atestes e tramitação no Contratos.gov.br"
tags: ["contratos-gov", "fornecedor", "nota-fiscal", "ateste", "manual-operacional"]
---

# Manual Operacional - Contratos.gov.br - Perfil Fornecedor

> **Síntese / Ementa Institucional:**  
> Guia técnico para fornecedores contratados sobre acesso, envio de notas fiscais, acompanhamento de atestes e tramitação no Contratos.gov.br  
> **Órgão Responsável:** Governo Federal / MGI / Contratos.gov.br | **Ano de Referência:** 2026

---

## Conteúdo Integral

<!-- Página 1 -->

VERSÃO 3.5.0 - AGOSTO/2026

---

<!-- Página 2 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
2 | 4 7
VOLTAR AO COMEÇO
Ministério da Gestão e da Inovação em Serviços Públicos – MGI
Ministra: Esther Dweck
Secretaria de Gestão e Inovação – Seges
Secretário: Roberto Pojo
Secretária-adjunta: Regina Lemos de Andrade
Diretoria de Normas e Sistemas de Logística – Delog
Diretor: Everton Batista dos Santos
Coordenação-Geral dos Sistemas de Contratos e Patrimônio – CGCON
Coordenadora-Geral: Anne Camila Knoll
Coordenador do Sistema de Contratos: Edher Garrido Lombardi
Equipe:
Alice Bressanelli Azevedo
Brunno dos Passos Alves
Cleiton Lucas Sampaio Pontes
Fernanda Vieira Klein Teixeira
Gildete Mamede Sales
Kelson Soares Brito
Lucas Borges Kappel
Marcela Rocha Brum
Patrícia Mattar
Ricardo Arruda Sowek
Rochanna Argenta Betto Barreto
Sandra Regina Sousa Santos
Projeto gráfico:
André Siqueira de Azevedo
VERSÃO 3.2.0 – MAR/2024

---

<!-- Página 3 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
3 | 4 7
VOLTAR AO COMEÇO
Histórico de Versões
DATA
VERSÃO
DESCRIÇÃO
15/08/2026
3.5.0
-
Importação de arquivo XML da NF-e
10/08/2026
3.4.0
-
Vincular
TRD
ao
Instrumento
de
Cobrança.
01/07/2026
3.3.0
-
Possibilidade de incluir documentos do
Plano de Fiscalização na entrega.
14/05/2026
3.2.0
-
Possibilidade de realização de entregas
sem vínculo com OS/F;
-
Possibilidade de download do(s) TRP(s)
e TRD(s) relacionados à entrega.
01/04/2026
3.1.0
- Indicação de Preposto para seus contratos
- Acompanhamento e Análise (aceite ou
recusa) de Solicitações de Adesão às Atas de
Registros de Preço
-
Registro
e
acompanhamento
de
Instrumentos de Cobrança
09/09/2024
3.0.0
- Manual técnico operacional do perfil
fornecedor no sistema Contratos.gov.br

---

<!-- Página 4 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
4 | 4 7
VOLTAR AO COMEÇO
Sumário
1.
Apresentação .......................................................................................................................................................................... 5
2.
Grupo de usuários ............................................................................................................................................................... 6
2.1.
Atribuição de perfis ........................................................................................................................................... 6
3.
Tela de autenticação do sistema .......................................................................................................................... 9
4.
Início .............................................................................................................................................................................................. 10
5.
Menu de acesso rápido ................................................................................................................................................. 11
6.
Menu Lateral ......................................................................................................................................................................... 12
7.
Menu Contratos .................................................................................................................................................................. 12
7.1.
Visualizar Contrato .................................................................................................................................................14
7.2.
Ordens de Serviço/Fornecimento .......................................................................................................... 16
7.2.1.
Visualizar Ordem de Serviço/Fornecimento ............................................................................ 18
7.2.2.
Assinar Ordem de Serviço/Fornecimento .................................................................................. 19
7.3.
Entregas........................................................................................................................................................................ 20
7.3.1.
Comunicar Entrega ......................................................................................................................................... 22
7.3.2.
Acompanhamento do recebimento da entrega ..................................................................... 27
7.3.3.
Duplicar entrega .............................................................................................................................................. 28
7.4.
Prepostos..................................................................................................................................................................... 28
7.4.1.
Indicar Prepostos ............................................................................................................................................ 29
8.
Menu Ordem de Serviço/Fornecimento .................................................................................................... 30
9.
Instrumentos de Cobrança .......................................................................................................................................32
9.1.
Cadastro do Instrumento de Cobrança ...............................................................................................32
9.2.
Listagem dos instrumentos de cobrança e ordem cronológica de pagamento .....
.............................................................................................................................................................................................. 40
9.3.
Importação do arquivo XML da NF-e .....................................................................................................41
10. Menu Atas de Registro de Preços .......................................................................................................................41
10.1.
Visualizar Atas de Registro de Preços .................................................................................................. 43
11. Menu Analisar Adesão .................................................................................................................................................. 44
11.1.
Analisar solicitação de anuência da adesão ....................................................................................46

---

<!-- Página 5 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
5 | 4 7
VOLTAR AO COMEÇO
Apresentação
Com a criação do Módulo Fornecedor dentro do Sistema Contratos.gov.br pela
primeira vez o fornecedor de produtos e/ou serviços ao Governo Federal terá uma
interface para realizar a gestão contratual de todos os contratos e atas de registro
de preços que possui com os órgãos usuários do sistema.
O usuário fornecedor realizará as primeiras interações com os órgãos
contratantes, como assinar as ordens de serviços e/ou fornecimento relacionadas
aos contratos existentes e informar entregas a elas relacionadas. Por meio do
sistema de alerta, o fornecedor será notificado sobre a necessidade de assinatura
de documentos, bem como acompanhamento da evolução das entregas
realizadas.
Com isso, o fornecedor passa a ter acesso centralizado às informações
relacionadas aos contratos e atas de registro de preços, podendo fazer extrações,
consultas diversas, realizar o efetivo acompanhamento contratual e praticar atos
relacionados à execução dos contratos e atas vigentes.
Também estão previstas evoluções futuras que possibilitarão ao fornecedor a
assinatura de contratos e seus termos, inserção de documentos relacionados às
etapas de recebimento do objeto, inclusão de notas fiscais e demais instrumentos
de cobrança, acompanhamento de ocorrências, manifestação de anuência para a
adesão em atas de registro de preços, entre outras ações.
A disponibilização desse módulo é apenas a primeira etapa de uma série de
melhorias que proporcionarão ao fornecedor executar diversas ações e interagir
com a equipe de gestão e fiscalização do contrato diretamente no sistema.
Quem pode utilizar:
Qualquer representante de empresa que tenha contrato firmado com órgãos
públicos usuários do sistema Contratos.gov.br.
Modelo de oferta do módulo:
Disponibilizado de forma centralizada como parte do Contratos.gov.br, evitando a
manutenção de outros sistemas afins, de forma isolada, estabelecendo medidas
de eficiência organizacional para o aprimoramento da administração pública.

---

<!-- Página 6 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
6 | 4 7
VOLTAR AO COMEÇO
1. Grupo de usuários
TIPO
DESCRIÇÃO
Administrador
de Contratos
Tem permissão para visualizar todos os contratos em que o
fornecedor figura como contratado, assinar Ordens de
Serviço/Fornecimento, comunicar entregas e acompanhar o
status do seu recebimento até a elaboração do Termo de
Recebimento Definitivo por parte do órgão contratante. Pode,
ainda, visualizar todas as atas de registro de preços e realizar
outras consultas e extrações de dados relacionadas aos
instrumentos de cobrança, ordens de serviço/fornecimento,
contratos e atas de registro de preços cadastrados no Sistema.
Preposto
de
Contratos
Tem as mesmas permissões do Administrador de Contratos,
mas restrito aos contratos em que foi cadastrado como
preposto pelo Setor Contratos.
Responsável
por contratos
Tem permissão para visualizar todos os contratos do
fornecedor, assinar Ordens de Serviço / Fornecimento, realizar
entregas e acompanhar o status do recebimento das entregas
realizadas até a elaboração do Termo de Recebimento
Definitivo por parte do órgão contratante. Também pode
visualizar todas as atas de registro de preços que o fornecedor
tem com os órgãos usuários do sistema e realizar outras
consultas e extrações de dados relacionadas aos instrumentos
de cobrança, ordens de serviço/fornecimento, contratos e atas
de registro de preços.
1.1. Atribuição de perfis
A atribuição de perfis é realizada pelo próprio fornecedor através do sistema
Compras.com.br. Não sendo exigida nenhuma nova senha pois o usuário utilizará
o mesmo acesso que já possui ao sistema de compras.

---

<!-- Página 7 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
7 | 4 7
VOLTAR AO COMEÇO
Figura 1 – Tela de login do sistema Compras.gov.br
Dentro da tela inicial do sistema Compras.gov.br, o usuário deverá acessar o menu
“Dados Cadastrais” e em seguida “Controle de Usuários e Opção por Serviços”.
Figura 2 – Tela inicial do sistema Compras.gov.br
Nesta tela, serão exibidos os usuários já cadastrados, permitindo a alteração de
seus perfis, bem como inclusão de novos usuários. Para realizar alteração de perfil
e incluir a permissão para acesso ao Sistema Contratos.gov.br, deve-se clicar
sobre o perfil do usuário que deseja alterar, conforme imagem abaixo.

---

<!-- Página 8 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
8 | 4 7
VOLTAR AO COMEÇO
Figura 3 – Acesso aos perfis no sistema Compras.gov.br.
Com isso, será aberta a janela em que poderá ser selecionados os serviços
disponíveis para serem concedidos aos usuários.
Para que o usuário possa acessar o sistema Contratos.gov.br, deve(m) ser
selecionada(s) a(s) opção(ões) “Administrador de Contratos” ou “Preposto de
Contratos, de acordo com as definições que o próprio fornecedor achar mais
adequada.
Figura 4 – Seleção das opções para acesso ao Contratos.gov.br.

---

<!-- Página 9 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
9 | 4 7
VOLTAR AO COMEÇO
2. Tela de autenticação do sistema
Para acessar à área do fornecedor no Sistema Contratos, efetuar o login no
Sistema Compras.gov.br e selecionar a opção “Contratos”, escolhendo se deseja
acessar como “Administrador de Contratos” ou “Preposto de Contratos”, conforme
o perfil atribuído ao usuário como explicado no item 2.1 deste manual.
Figura 5 – Acesso ao sistema Contratos.gov.br
No primeiro acesso ao sistema, será solicitado ao usuário logado que informe o
melhor e-mail e telefone para contato para fins de atualização na base de dados
do sistema Contratos.gov.br.
Figura 6 – Tela de confirmação dos dados.

---

<!-- Página 10 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
10 | 4 7
VOLTAR AO COMEÇO
Atenção: Esses dados são importantes, pois é por meio do e-mail informado que
serão feitas eventuais notificações existentes das atualizações relacionadas aos
contratos ou atas de registro de preços e comunicação a ser realizada com o
fornecedor.
3. Início
Abaixo, o detalhamento de todos os componentes da página inicial do
fornecedor.
Figura 7 – Tela inicial do fornecedor – Identificação, menus de acesso rápido e acompanhamento de
vencimentos
Figura 8 – Tela inicial do fornecedor – Gráficos de distribuição e valores dos contratos e atas de registro de
preços

---

<!-- Página 11 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
11 | 4 7
VOLTAR AO COMEÇO
Figura 9 – Tela inicial do fornecedor – listagem de contratos e atas de registro de preços
4. Menu de acesso rápido
Na tela inicial, o fornecedor visualizará os ícones de acesso rápido, que levará à
funcionalidade
desejada:
Contratos,
Ordem
de
Serviço/Fornecimento,
Instrumentos Cobrança e as Atas de Registro de Preços.
Figura 10 – Menu de Acesso Rápido

---

<!-- Página 12 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
12 | 4 7
VOLTAR AO COMEÇO
5. Menu Lateral
O usuário também tem a opção de acesso às funcionalidades do sistema por meio
do menu localizado na lateral superior esquerda da tela, representado pelo ícone
“
”.
Figura 11 – Menu Lateral
Além das opções mencionadas para o acesso rápido, no menu lateral é possível acessar
os ambientes de transparência do sistema Contratos.gov.br, com informações públicas
disponibilizadas
pelo
sistema.
6. Menu Contratos
A relação de contratos do fornecedor pode ser acessada pelo menu lateral ou
pelo menu de acesso rápido.
Serão apresentados os contratos que o fornecedor figure como contratado, caso
tenha sido escolhida a opção de visualização pelo Administrador de Contratos, ou
os contratos em que o órgão realizou o cadastro do preposto, caso tenha sido
escolhida esta opção, sendo possível configurar as colunas apresentadas, por
meio do botão
, além de possibilitar a extração dos dados
através de exportação de arquivos do tipo Excel, CSV, PDF ou mesmo imprimir
diretamente da tela.

---

<!-- Página 13 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
13 | 4 7
VOLTAR AO COMEÇO
Figura 12 – Tipos de acesso do Fornecedor e opções de exportação e visibilidade das colunas apresentadas
Na coluna “Ações”, o fornecedor tem as opções específicas por contrato, como a
visualização
do
seu
detalhamento
(
),
acesso
às
Ordens
de
Serviço/Fornecimento (
), consulta aos instrumentos de cobrança cadastrados (
) e visualização da publicação do contrato no PNCP (
) para contratos
decorrentes da Lei 14.133/2021.

---

<!-- Página 14 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
14 | 4 7
VOLTAR AO COMEÇO
Figura 13  – Contratos do fornecedor
É importante destacar que o fornecedor, que tenha acessado com o perfil
“Preposto de Contratos”, consiga visualizar os contratos, o órgão contratante
precisa ter realizado previamente o cadastro do preposto no contrato dentro do
sistema Contratos.gov.br.
Já se o login for realizado utilizando o perfil “Administrador de Contratos”, o
fornecedor terá acesso a todos os contratos registrados no sistema
Contratos.gov.br do fornecedor logado, de todos os órgãos públicos que utilizam
o sistema.
6.1. Visualizar Contrato
Acessando a listagem de contratos e clicando no ícone
, o usuário terá acesso
à tela de detalhamento deste contrato, como seu número, unidade gestora,
amparo legal, vigência início e fim, valor global, histórico, empenhos, faturas,
prepostos, responsáveis, entre outros. Também terá acesso à página de
instrumentos de cobrança detalhados, os terceirizados cadastrados e os arquivos
vinculados que podem ser baixados.

---

<!-- Página 15 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
15 | 4 7
VOLTAR AO COMEÇO

---

<!-- Página 16 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
16 | 4 7
VOLTAR AO COMEÇO
Figura 14 – Visualização de um contrato
6.2. Ordens de Serviço/Fornecimento
Ainda na listagem de contratos, existe a funcionalidade para acesso às Ordens de
Serviço/Fornecimento (OS/F) daquele contrato emitidas pelo órgão contratante,
disponível no ícone “
”, contendo sua situação, os status da evolução de sua
execução e outras ações que explicaremos a seguir.

---

<!-- Página 17 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
17 | 4 7
VOLTAR AO COMEÇO
Figura 15  – Ordens de serviço/fornecimento do contrato
Na coluna “Situação” o usuário pode acompanhar a fase de cada Ordem de
Serviço/Fornecimento, sendo elas: “Aguardando Assinatura” – quando tem
assinatura pendente, “Em Execução” – quando iniciou o prazo de vigência previsto
na OS/F; ou “Concluído” – quando o prazo de vigência foi finalizado.
Figura 16 – Situação da Ordem de Serviço / Fornecimento

---

<!-- Página 18 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
18 | 4 7
VOLTAR AO COMEÇO
A coluna “Evolução” apresenta graficamente o percentual de evolução da
execução da Ordem de Serviço/Fornecimento, sendo possível acompanhar o
quanto foi executado, auxiliando o acompanhamento principalmente de entregas
parceladas do objeto. O percentual aumenta conforme as entregas relacionadas
àquela OS/F são informadas no sistema.
Figura 17 – Coluna Evolução da Ordem de Serviço/Fornecimento
6.2.1. Visualizar Ordem de Serviço/Fornecimento
Dentre as opções da coluna “Ações” existe a opção “visualizar”, representada pelo
ícone “
”. Ao clicar nesse ícone o usuário tem acesso às informações detalhadas
da OS/F, opção de download de arquivos anexados, além da versão assinada em
formato PDF.

---

<!-- Página 19 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
19 | 4 7
VOLTAR AO COMEÇO
Figura 18 – Tela Visualizar Ordem de Serviço / Fornecimento
6.2.2. Assinar Ordem de Serviço/Fornecimento
A opção “assinar”, representada pelo ícone “
”, ficará disponível caso o gestor ou
fiscal do contrato, ao criar a Ordem de Serviço/Fornecimento pelo Sistema, tenha
identificado o fornecedor como preposto do contrato ou tenha sido feita a opção
de login com o perfil de Administrador de Contratos.

---

<!-- Página 20 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
20 | 4 7
VOLTAR AO COMEÇO
Ao clicar no ícone, o usuário tem acesso à página com o PDF da Ordem de
Serviço/Fornecimento, podendo fazer a análise do texto e assiná-la digitalmente
através do serviço Gov.br, sendo necessário o nível da conta prata ou ouro. Para
mais informações em como aumentar o nível da conta ou criação de uma,
consultar a página do Gov.br <Conta gov.br — Governo Digital (www.gov.br)>.
Figura 19 – PDF para Assinatura de Ordem de Serviço
6.3. Entregas
A comunicação da entrega do objeto contratado pode ser realizada de duas
formas, dependendo da existência de uma Ordem de Serviço ou Fornecimento
(OS/F):
1. Entregas vinculadas a uma OS/F: Podem ser realizadas através do menu
de Ordens de Serviço, utilizando o ícone
(Entrega) ou na tela de consulta
“Meus Contratos direto no ícone
(Entrega).
2. Entregas sem OS/F: O registro da entrega é possível exclusivamente
através da tela “Meus Contratos”, acionando o botão “Entrega”.
Esta ação dará início à contagem dos prazos informados pelo Setor de Contratos
no cadastro do contrato para o Recebimento Provisório e o Recebimento
Definitivo do objeto, conforme previsto no contrato, edital, aviso de contratação
direta ou outro normativo pertinente.

---

<!-- Página 21 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
21 | 4 7
VOLTAR AO COMEÇO
Figura 20 – Cadastrar Entrega
Se o prazo não tiver sido cadastrado ou estiver em desconformidade com o que
foi estabelecido contratualmente pelas partes, o fornecedor pode solicitar que o
Setor Contratos ou Gestor do contrato realize a correção das informações contidas
no sistema, a fim de facilitar o melhor gerenciamento desse contrato.
Nessa página estão relacionadas todas as entregas de materiais e/ou serviços
realizadas pelo fornecedor, sejam elas informadas pelo próprio representante do
fornecedor ou pela equipe de fiscalização do órgão contratante.
Dentre as informações disponíveis, além dos dados do contrato, tem a situação
em que se encontram no fluxo de recebimento por parte do órgão, ou seja, é
possível identificar se a entrega informada já foi analisada pelo órgão contratante,
se já teve o Termo de Recebimento Provisório ou o Definitivo emitidos, bem como
fazer o download dos documentos assinados.
Também é possível, com base na data de realização da entrega, ter a previsão
para a conclusão de cada etapa do fluxo de recebimento, trazendo assim mais
previsibilidade para o fornecedor, desde que os parâmetros tenham sido
informados pelo Setor Contratos no respectivo contrato. Caso contrário, os prazos
ficarão em branco, semelhante à entrega com situação “em elaboração” na figura
abaixo.

---

<!-- Página 22 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
22 | 4 7
VOLTAR AO COMEÇO
Figura 21 – Tela de entregas
6.3.1. Comunicar Entrega
Dentro do sistema, o usuário fornecedor tem a possibilidade de comunicar a
realização da entrega do objeto do contrato, que poderá ser integral ou parcial.
A comunicação da entrega, total ou parcial, do objeto pelo fornecedor dá início ao
fluxo de recebimento por parte do órgão contratante e passará pelas etapas de
análise da entrega, elaboração do Termo de Recebimento Provisório e elaboração
do Termo de Recebimento Definitivo.
Para iniciar a comunicação de uma entrega de um produto e/ou serviço, o
fornecedor deve acessar a Ordem de Serviço/Fornecimento correspondente,
acessar a opção Entregas, ou acessar o ícone ‘Entregas’ na coluna ‘ações da
listagem de Contratos, conforme orientado no Item 7.2.3. e em seguida clicar no
botão “+ Adicionar Entrega”.

---

<!-- Página 23 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
23 | 4 7
VOLTAR AO COMEÇO
Figura 22 – Comunicar Entrega
Após clicar em Adicionar entrega, o fornecedor terá acesso aos dados do contrato,
os dados da OS/F ou itens e logo abaixo o campo para que seja incluída a
quantidade do(s) item(ns) entregue(s).

---

<!-- Página 24 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
24 | 4 7
VOLTAR AO COMEÇO
Figura 23 – Comunicar entrega pelo Fornecedor
O usuário deve selecionar a(s) linha(s) do(s) item(ns) entregue(s), preencher a
quantidade informada na entrega e conferir o seu valor total. É possível incluir mais
de um item em cada entrega. No entanto, quando vinculado a OS/F, só é possível
selecionar uma única OS/F por entrega.
Em cada linha do item, consta à direita uma barra de evolução das entregas
daquele item, que aumenta seu percentual conforme as entregas dos itens vão
sendo realizadas, possibilitando ao fornecedor acompanhar sua evolução e o
quanto ainda falta ou pode ser executado dentro do que foi estabelecido na
respectiva OS/F ou dentro do que foi contratado. A barra de evolução muda de
cor, demonstrando a proximidade do máximo permitido a ser executado.

---

<!-- Página 25 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
25 | 4 7
VOLTAR AO COMEÇO
Figura 24 – Itens Entregues
Ao posicionar o cursor sobre o símbolo “,
” localizado ao lado da barra de
evolução das entregas, é exibido o seu detalhamento, sendo possível verificar a
situação de entregas anteriores.
Na figura abaixo podemos ver o exemplo de uma entrega que está em
preenchimento com o quantitativo de 1 unidade.
A linha 1 do quadro mostra o quantitativo total de unidades solicitadas naquela
Ordem de Serviço/Fornecimento.
A linha 2 exibe a quantidade que foi informada naquela entrega.
A linha 3 mostra a quantidade já entregue em ocasiões anteriores.
Por fim, a linha 4 mostra a quantidade ainda pendente de entrega, considerando
as quantidades já informadas no sistema.
Figura 25 – Tabela Quadro Resumo das Entregas de um item
Em seguida o fornecedor deverá preencher o campo de informações
complementares, caso deseje.

---

<!-- Página 26 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
26 | 4 7
VOLTAR AO COMEÇO
Deve ainda selecionar o Mês/Ano de Referência, e preencher os campos “Período
início da entrega” e “Período fim da entrega”. O campo “Data efetiva da entrega”
vem pré-preenchido com a data de criação da entrega, e com base nesta data são
calculados os campos “Data prevista para o recebimento provisório” e “Data
prevista para o recebimento definitivo”.
O fornecedor também tem a possibilidade de inclusão de arquivos relacionados
ao Plano de Fiscalização, personalizado pela equipe de gestão/fiscalização do
contrato, limitado ao tamanho de 30Mb.
Figura 26 – Preenchimento da entrega
Por fim, após o preenchimento, o fornecedor tem 3 opções:
1 - “Cancelar” - cancela o que foi preenchido e volta para a tela anterior sem
registrar os dados;
2 - “Salvar Rascunho” – cria uma entrega, porém com o status “em elaboração”, ou
seja, que ainda não foi enviada para análise do órgão contratante e,
consequentemente, ainda não gera os efeitos de início de contagem de prazo para
o recebimento provisório e definitivo; e
3 – “Registrar Entrega” – envia efetivamente a entrega para análise do órgão
contratante e passa a ter início os prazos para o recebimento provisório e definitivo
dos itens entregues.
Figura 27 – Botões da página Comunicar Entrega

---

<!-- Página 27 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
27 | 4 7
VOLTAR AO COMEÇO
6.3.2. Acompanhamento do recebimento da entrega
Após a realização da comunicação da entrega, o sistema retorna para a tela
listagem das entregas já realizadas e a coluna “Situação” apresenta os respectivos
status, conforme figura abaixo.
Figura 28 – Situação das entregas
As situações possíveis em para os status das entregas são:
• Em Elaboração – Quando foi iniciada a elaboração de uma entrega e salva
em rascunho. Nessa situação a entrega ainda não está em análise pelo
órgão, sendo possível sua edição ou exclusão. Nesse caso ainda não se
inicia a contagem de prazos para o recebimento provisório e definitivo.
• Recusada – Quando o fiscal ou gestor do contrato no órgão contratante
recusa a entrega justificadamente. Nessa situação, os prazos para
recebimento provisório e definitivo são interrompidos e o fornecedor pode
editar a entrega, para corrigi-la.
• Em Análise – Situação quando a entrega foi enviada pelo fornecedor, mas
ainda não foi analisada pelo fiscal do contrato no órgão contratante. Os
prazos para recebimento provisório e definitivo nesse caso já passam a ser
contados.
•
Em Execução – Indica que a entrega está em processamento pelo órgão
contratante. Nesta fase, os Termos de Recebimento Provisório (TRP) e

---

<!-- Página 28 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
28 | 4 7
VOLTAR AO COMEÇO
Definitivo (TRD) podem ou não ter sido emitidos. Para identificar o status de
cada termo, observe a cor dos botões na coluna de ações: se estiverem
azuis, o documento já foi emitido e está disponível para download; se
estiverem cinzas, o documento ainda não foi gerado ou está em fase de
elaboração interna.
• Cancelada – Esta situação indica o encerramento do ciclo da entrega no
sistema. Ela ocorre automaticamente em duas situações: quando o fiscal ou
gestor, ao emitir o Termo de Recebimento Definitivo (TRD), indica que
aquela entrega finaliza a Ordem de Serviço (OS), ou quando a OS é finalizada
diretamente pelo gestor no sistema.
6.3.3. Duplicar entrega
Caso o fornecedor deseje realizar uma nova entrega e precise reaproveitar
informações incluídas em uma entrega anterior dentro da mesma Ordem de
Serviço/Fornecimento, existe a opção para duplicar uma entrega já realizada. Para
isso, deve-se utilizar o ícone “
” na coluna “Ações”. O sistema criará uma entrega
com a situação “Em Elaboração” com os mesmos dados da anterior, devendo
clicar no ícone “
” para realizar a edição, alterando os dados necessários e
aproveitando dados já existentes na entrega originária.
6.4. Prepostos
A indicação do preposto deve ser feita pelo Administrados acionando o ícone “
”
na coluna Ações. Será exibida uma nova janela onde é possível pelo acionamento
dos botões: “Voltar” a listagem dos Contratos, assim fechando a atual janela;
verificar o “Histórico” dos prepostos que já atuaram no contrato em questão, sendo
possível tomas algumas ações quanto a situação desses; e por Fim “Indicar
Preposto”, dessa firma designando uma pessoa para assumir como preposto do
contrato
em
questão.

---

<!-- Página 29 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
29 | 4 7
VOLTAR AO COMEÇO
Figura 29 – Menu preposto
6.4.1. Indicar Prepostos
Acionando o botão “Indicar Preposto” será redirecionado para a tela de cadastro
do preposto:
Figura 30 – Indicar Preposto

---

<!-- Página 30 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
30 | 4 7
VOLTAR AO COMEÇO
1. Dados para Indicação do Preposto
• CPF: número do CPF
• Nome completo
• E-mail
• Telefone fixo
• Celular
• Documento de Formalização: Por exemplo, ofício ou declaração
• Titularidade: se o preposto é o Titular ou Substituto
• Informações
Complementares:
Demais
informações
ou
observações que julgar necessário
• Anexo: documentação relativa à indicação do preposto.
Após a indicação será necessário o Fiscal/Gestor do contrato avaliar e aprovar.
7. Menu Ordem de Serviço/Fornecimento
O menu Ordem de Serviço / Fornecimento pode ser acessado tanto acesso rápido
na parte superior da página principal ou pelo menu lateral.
Figura 31 – Acesso OS/F via Acesso Rápido

---

<!-- Página 31 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
31 | 4 7
VOLTAR AO COMEÇO
Figura 32 – Acesso OS/F via menu lateral
O usuário tem acesso a todas as Ordens de Serviço / Fornecimento obedecendo
a seguinte lógica:
• Preposto de contratos: visualiza as Ordens de Serviço / Fornecimento em
que foi designado.
• Administrador de Contratos: Visualiza todas as Ordens de Serviço /
Fornecimento do fornecedor.
Na página da relação de Ordens de Serviço / Fornecimento do Fornecedor são
apresentadas todas as OS/F, independente do contrato ao qual ela está vinculada,
tendo as mesmas colunas e ações descritos no item 7.2 deste manual.

---

<!-- Página 32 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
32 | 4 7
VOLTAR AO COMEÇO
Figura 33 – Ordens de Serviço / Fornecimento do Fornecedor
8. Instrumentos de Cobrança
8.1. Cadastro do Instrumento de Cobrança
O cadastro do Instrumento de Cobrança (IC) pode ser realizado por dois acessos:
1. Pelo Acesso Rápido:
 Clique no ícone “Instrumentos de Cobrança” e, em seguida,
 Clique em “Cadastrar instrumento de cobrança”
Pelo Acesso Rápido é possível consultar os instrumentos de cobrança já
cadastrados, clicando no ícone visualizar
da coluna “Ações” na listagem inicial
ao entrar pelo ícone.

---

<!-- Página 33 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
33 | 4 7
VOLTAR AO COMEÇO
Figura 34 – Instrumentos de Cobrança via Acesso Rápido
Após clicar em “Cadastrar instrumento de cobrança”, aparecerá uma tela para
seleção do contrato que deseja cadastrar o IC, podendo pesquisar pelo
número/ano do contrato ou pela unidade ou clicando no contrato/unidade da
listagem.
Figura 35 – Pesquisa do contrato que deseja cadastrar instrumento de cobrança

---

<!-- Página 34 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
34 | 4 7
VOLTAR AO COMEÇO
2. Pelo Menu Lateral:
 Acesse “Gestão Contratual” e, depois
 Acesse “Contratos”, e na tela seguinte,
 Na coluna “Ações” clique no ícone “Instrumento de cobrança” e, em
seguida, clique em “Cadastrar instrumento de cobrança”
Figura 36 – Instrumentos de Cobrança via Menu Lateral
Após a escolha de acesso ao cadastro do instrumento de cobrança (acesso rápido
ou menu lateral), preencher os campos do IC. A tela de cadastro é composta de

---

<!-- Página 35 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
35 | 4 7
VOLTAR AO COMEÇO
quatro: Dados do Instrumento de Cobrança; Itens Instrumento de Cobrança,
Termo Receb. Definitivo e Outras Informações.
1. Aba - Dados do Instrumento de Cobrança
• Dados do Contrato: cabeçalho com as informações do contrato,
pode ser ocultado os dados pela seta na lateral direita.
• Fornecedor Subcontratado: caso o IC seja de outro fornecedor
diferente do contrato e que esteja indicado como subcontratado no
contrato.
• Consulta SICAF: consulta das certidões do fornecedor por integração
com o SICAF.
• Unidade: unidade na qual o contrato está cadastrado (pré-
preenchido), podendo selecionar uma unidade descentralizada do
contrato.
• Número do Processo Sei: número do processo indicado no contrato
(pré-preenchido).
• Tipo Lista: selecionar a que se refere o instrumento de cobrança
(prestação de serviços, fornecimento de bens etc.).
• Tipo de Instrumento de Cobrança: selecionar qual o tipo do IC (NFe,
Nota fiscal, fatura, recibo etc.).
• Data de emissão: informar a data de emissão do IC.
• Número: informar o número do IC.
• Série: informar o número da série, se houver.
• Chave NFe: informar a chave em caso da seleção de NFe em tipo do
IC, observando que a chave pode conter de 44 a 50 dígitos.
• Arquivo de Instrumento de Cobrança: inserir o documento de IC.
Dica: Após seleção e preenchimento dos campos da aba, clique na seta na parte
inferior da tela
ou clique na próxima aba na parte superior.

---

<!-- Página 36 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
36 | 4 7
VOLTAR AO COMEÇO
Figura 37 – Dados do Instrumento de Cobrança

---

<!-- Página 37 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
37 | 4 7
VOLTAR AO COMEÇO
Aba - Itens Instrumento de Cobrança
• Dados do contrato: a partir da segunda aba, os dados ficam ocultados,
podendo ser expandidos clicando na seta.
• Glosa: colocar o valor, se houver, podendo ser descontado do valor total
ou não. Se descontar do valor total, marcar a opção “sim” após
preenchimento.
• Juros/Multa: colocar o valor, se houver. O valor informado aumenta o
valor líquido do IC.
• Histórico do Contrato: escolher o contrato ou seus termos, podendo
escolher mais de um.
• Itens do histórico: escolher um ou todos os itens do contrato ou termo
selecionado
• Valor unitário e quantidade: valores pré-preenchidos podendo ser
editados.
• País de fabricação: escolher o país de fabricação quando se tratar de
fornecimento de bens.
Outras funcionalidades: além do preenchimento dos campos, a tela permite
expandir a visualização ao clicar no ícone
. Também é possível excluir um ou
mais itens, ou ainda todos de uma vez, utilizando o ícone de lixeira; para exclusões
em lote, o usuário pode selecionar todos os itens e desmarcar aqueles que não
deseja excluir antes de confirmar a ação. Adicionalmente, há a funcionalidade de
replicar itens, disponível por meio do ícone
, que permite duplicar rapidamente
as informações já inseridas.
Após seleção e preenchimento dos campos da aba, clique na seta na parte inferior
da tela ou clique na próxima aba no canto superior.

---

<!-- Página 38 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
38 | 4 7
VOLTAR AO COMEÇO
Figura 38– Itens Instrumento de Cobrança
2. Aba – Termo Receb. Definitivo
Selecionar o(s) termo(s) de recebimento definitivo para vincular ao
instrumento de cobrança. A soma dos termos vinculados deve ser
equivalente ao valor do Instrumento de Cobrança indicado na aba Itens
Instrumento de Cobrança.
• Situação do termo de recebimento definitivo: são listados apenas os
termos na situação “Aguard. Inst. Cobrança”.
• Número do termo de recebimento definitivo
• Valor do termo de recebimento definitivo
• Valor considerado no Inst. de cobrança: informar o valor correspondente
ao termo (pode haver mais de um termo).
• Consumo: informa o % do valor informado em relação ao valor do termo de
recebimento definitivo.
• Ações: opção de visualizar o termo de recebimento definitivo
Figura 39 – Vincular Termo de Recebimento Definitivo ao Instrumento de Cobrança

---

<!-- Página 39 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
39 | 4 7
VOLTAR AO COMEÇO
3. Aba - Outras informações:
• Mês e Ano de Referência: selecionar o mês e ano de referência do IC.
• Valor: informar o valor líquido da aba anterior.
• Informações complementares: preencher, se houver.
• Arquivo Complementar: inserir documento complementar, se houver.
Após preenchimentos das abas, clicar em “Criar Instrumento de Cobrança” para
registrar o IC.
Figura 40– Outras Informações
Após cadastro do Instrumento de cobrança, volta para tela de listagem dos ICs
pertencentes ao contrato selecionado no momento inicial do registro. O
Instrumento de cobrança fica na situação “Aguardando Fiscal”, pois se encontra
em fase de análise do fiscal do órgão contratante.
Figura 41 – Instrumento de Cobrança  situação aguardando fiscal

---

<!-- Página 40 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
40 | 4 7
VOLTAR AO COMEÇO
Após análise do fiscal, o documento pode ser recusado¹ ou aceito². Se for
recusado, sua situação é alterada para recusado com uma mensagem de alerta e
o motivo da recusa, podendo ser corrigido pela edição
ou cancelado clicando
no ícone
, registrando um novo IC. Se o IC for aceito pelo órgão contratante, a
situação fica “Pendente”, indicando que o documento está pendente de
pagamento, não sendo possível mais a sua edição
Figura 42 – Aceite ou recusa do instrumento de cobrança
No ícone visualizar
verifica-se as principais informações do IC, inclusive o
histórico das ações: inclusão, edição, recusa.
8.2. Listagem dos instrumentos de cobrança e ordem cronológica de pagamento
O instrumento de cobrança é listado por sua ordem cronológica de pagamento,
seguindo as regras da Instrução Normativa nº 77 de novembro de 2022. Além
disso, é possível pesquisar o instrumento de cobrança pelo nº do contrato,
situação, número etc., utilizando os filtros, e pelo campo pesquisar digitando o nº
do IC ou contrato.
Observando que a edição do IC só é permitida na situação “Aguardando Fiscal”.
Figura 43 – Listagem dos instrumentos de cobrança.

---

<!-- Página 41 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
41 | 4 7
VOLTAR AO COMEÇO
8.3. Importação do arquivo XML da NF-e
A partir da parametrização realizada pelo órgão contratante, fica disponível a
funcionalidade de importação do XML da Nota Fiscal Eletrônica (NF-e) para
preenchimento automático dos campos no cadastro do Instrumento de Cobrança
(IC).
Para realizar a importação, clique no ícone “Importar XML NF-e”, selecione a
parametrização previamente cadastrada e, em seguida, anexe o arquivo XML da
NF-e que deseja importar.
Os campos preenchidos automaticamente pela importação são:
• Tipo Lista (Bens ou Serviço)
• Tipo de IC (NF-e ou Nota Fiscal)
• Data de Emissão
• Número
• Série (se houver)
• Chave da NF-e (se houver)
• Itens – podem estar diferentes da NF-e, sendo necessário verificar se estão
corretos ou selecionar os itens correspondentes a partir da seleção
disponível.
• Valor Unitário do Item
• Quantidade do Item
• Informações Complementares.
Observação: todos os campos são editáveis para ajuste, se necessário, exceto
data de emissão e número da NF-e.
9.   Menu Atas de Registro de Preços
O Menu Atas de Registro de Preços, assim como os demais menus, pode ser
acessado via menu de acesso rápido na parte superior da página inicial e no menu
lateral, conforme figuras abaixo.

---

<!-- Página 42 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
42 | 4 7
VOLTAR AO COMEÇO
Figura 44 – Atas de Registro de Preços via menu de Acesso Rápido
Figura 45 – Atas de Registro de Preços via menu lateral
Ao acessar a listagem de atas de registro de preços, o sistema apresentará todas
as atas em que o fornecedor é integrante, de todos os órgãos que utilizam o
sistema Contratos.gov.br, independentemente do perfil que tenha sido
selecionado pelo fornecedor (Administrador de Contratos ou Preposto).
Na relação será exibida a situação da Ata, número, vigência inicial e final, unidade
gerenciadora da ata e valor total.

---

<!-- Página 43 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
43 | 4 7
VOLTAR AO COMEÇO
Na coluna “Ações” estão disponíveis os ícones “
”, para visualizar o conteúdo da
ata de registro de preços, assim como o ícone “
”, que acessa a publicação da ata
de registro de preços no Portal Nacional de Contratações Públicas (PNCP).
Figura 46 – Listagem de Atas de Registro de Preços
No final da página com a listagem das atas de registro de preços, o fornecedor
tem a opção de extrair dados em forma de arquivos do tipo Excel, CSV e PDF
através do botão
ou a opção de impressão diretamente da página.
9.1. Visualizar Atas de Registro de Preços
A visualização dos dados da ata de registro de preços pode ser realizada através
do ícone “
” disponível na coluna “Ações”, onde encontrará informações mais
detalhadas como número da ata, situação, vigência inicial e final, itens, unidades

---

<!-- Página 44 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
44 | 4 7
VOLTAR AO COMEÇO
participantes, entre outras.
Figura 47 – Visualização Atas de Registro de Preços
10. Menu Analisar Adesão
O Menu Analisar Adesão está disponível no acesso rápido na parte superior da
página inicial.

---

<!-- Página 45 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
45 | 4 7
VOLTAR AO COMEÇO
Figura 48 – Analisar Adesão via menu de Acesso Rápido
Ao acessar a listagem de Solicitações de anuência da adesão, o sistema
apresentará todas as solicitações de adesão que o fornecedor recebeu, de todos
os órgãos que utilizam o sistema Contratos.gov.br.
Na relação será exibida a situação da Solicitação, número, número da ata de
registro de preço, unidade gerenciadora e unidade solicitante.
Na coluna “Ações” estão disponíveis os ícones “
”, para visualizar o conteúdo da
solicitação de adesão. Caso a situação esteja como “Em análise pelo Fornecedor”
aparecerá o ícone “
” para realizar a análise, ou seja, aceitar o rejeitar a solicitação;
caso a situação esteja como “Aceita” aparecerá também o ícone “
” para cancelar
a Adesão.

---

<!-- Página 46 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
46 | 4 7
VOLTAR AO COMEÇO
Figura 49 – Listagem de Solicitações de Anuência de Adesão
10.1.
Analisar solicitação de anuência da adesão
A análise das solicitações de anuência de adesão é realizada através do ícone “
” disponível na coluna “Ações”, onde encontrará informações mais detalhadas
como o responsável pela solicitação e seu e-mail, justificativa, demonstração de
valores compatíveis. Bem como os itens solicitado, a vigência, quantidade
disponível para adesão e a quantidade solicitada. Para cada item 3 ações são
Possíveis, selecionando a ação desejada na coluna “Analisar”:
• Aceitar
• Negar: necessário preencher a justificativa para a negativa
• Aceitar Parcialmente: necessário indicar a quantidade a ser fornecida e a
justificativa do porquê ser parcial.

---

<!-- Página 47 -->

M A N U A L T É C N I C O O P E R A C I O N A L – C O N T R A T O S . G O V . B R I F O R N E C E D O R
47 | 4 7
VOLTAR AO COMEÇO
Figura 50 – Ações para analisar a solicitação de adesão
É possível, pelo acionamento do botão “Salvar Rascunho” salvar as análises já
realizadas para finalizar mais tarde. Caso tenha concluído todas as análises, acionar
o botão “Finalizar análise”. Então a solicitação irá para análise da Unidade Gestora.
