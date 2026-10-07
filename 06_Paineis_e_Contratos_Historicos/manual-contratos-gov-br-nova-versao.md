---
arquivo_original: "manual-contratos-gov-br-nova-versao.pdf"
hash_pdf_md5: ba10700a6a960bcb1c652c5d396ef3cc
paginas: 132
metodo: "texto (pymupdf4llm) + OCR em 1 pagina(s)"
convertido_em: 2026-10-03T17:33:24
fonte: Base de Conhecimento CLC
---

<!-- pagina 1 (OCR) -->
© Contratos Gov.br E E E
MANUAL TÉCNICO
OPERACIONAL DO SISTEMA
DE CONTRATOS.GOV.BR
NOVA VERSÃO

Gestão de atas de registro de preços
Fiscalização e gestão de contratos

VERSÃO 2.10.0 — MAIO/2026

<!-- pagina 2 -->
M A N U A L T É C N I C O O P E R A C I O N A L – **C O N T R A T O S . G O V . B R I N O V A V E R S Ã O** 

**Ministério da Gestão e da Inovação em Serviços Públicos – MGI** 

**Ministra:** Esther Dweck 

**Secretaria de Gestão e Inovação – Seges** 

**Secretário:** Roberto Pojo 

**Secretária-adjunta:** Regina Lemos de Andrade 

## **Diretoria de Normas e Sistemas de Logística - Delog** 

**Diretor:** Everton Batista dos Santos 

**Coordenação-Geral dos Sistemas de Contratos e Patrimônio - CGCON** 

**Coordenadora-Geral:** Anne Camila Knoll 

**Coordenador do Sistema de Contratos:** Edher Garrido Lombardi 

**Equipe** : 

Alice Bressanelli Azevedo Brunno dos Passos Alves Cleiton Lucas Sampaio Pontes Gildete Mamede Sales Kelson Soares Brito Lucas Borges Kappel Marcela Rocha Brum Patrícia Mattar Ricardo Arruda Sowek Rochana Argenta Betto Barreto Sandra Regina Sousa Santos 

## **Revisão:** 

Êmili Adami Rossetti 

## **Projeto gráfico:** 

André Siqueira de Azevedo 

2 | 1 3 2 

**<u>VOLTAR AO SUMÁRIO</u>**

<!-- pagina 3 -->
## **Histórico de Versões** 

|**DATA**|**VERSÃO**|**DESCRIÇÃO**|
|---|---|---|
|14/05/2026|2.10.00|-<br>Inclusão da possibilidade de realização de<br>entregas sem OS/F;<br>-<br>Unificação<br>das<br>funcionalidades<br>Comunicar/Informar<br>Recebimento,<br>agora<br>renomeadas para “Adicionar Entrega”|
|01/04/2026|2.9.00|- Inclusão da funcionalidade Instrumento de<br>Cobrança|
|15/12/2025|2.8.00|- Exclusão do campo “Extinguir Ordem de<br>Serviço/Fornecimento” ao alterar OS/F.|
|13/11/2025|2.7.00|- Inclusão de funcionalidade que possibilita<br>renovação de quantitativo por órgãos SISG ao<br>realizar alteração do tipo vigência(prorrogação)|
|11/11/2024|2.6.00|- Inclusão dos campos “Data efetiva da entrega”,<br>“Data prevista para o recebimento provisório” e<br>“Data prevista para recebimento definitivo” na<br>informação das entregas.<br>- Inclusão de Local de Execução nas OS/F,<br>entregas, TRP e TRD.<br>-<br>Adicionar<br>preposto<br>de<br>contrato<br>pelo<br>Fiscal/Gestor.<br>- Inclusão de TRPs e TRDs criados fora do sistema.<br>- Inclusão da situação “Expirada” nas OS/F.<br>- Atualização na forma de login.|
|09/09/2024|2.5.00|- Criação, assinatura e novas ações da Ordem de<br>Serviço/Fornecimento;<br>- Fluxo de Entregas com Termo de Recebimento<br>Provisório e Definitivo;<br>- Revisãogeral.|
|23/08/2024|2.4.00|- Revisão geral;<br>- Alterações decorrentes da Medida Provisória<br>1.221/2024;<br>- Informar dados da Declaração OPM pela<br>Fiscalização;<br>- Correção dos números das versões anteriores no<br>histórico de versões.|
|18/03/2024|2.3.00|- Inclusão do módulo Fiscalização e Gestão<br>Contratual;<br>- Relatório de execução de Ata.|
|07/11/2023|2.2.00|- Inclusão de funcionalidade de Remanejamento<br>deQuantitativos.|
|21/07/2023|2.1.00|- Alterações e melhorias na busca da compra e em<br>campos na solicitação de adesão;<br>- Inclusão do_link_do PNCP no Transparência;|

3 | 1 3 2

<!-- pagina 4 -->
|||- Inclusão da classificação do fornecedor na<br>solicitação de adesão;<br>- Melhoria na inclusão de arquivo;<br>- Inclusão de filtros na consulta de compras;<br>- Melhoria retificar ata;<br>- Inclusão de informações da ata e dos contratos<br>na consulta de Compras;<br>- Inclusão de nova situação para a ata;<br>- Inclusão de justificativa para item isolado na<br>solicitação de adesão; atendimento de exceções de<br>quantitativo;<br>-<br>Inclusão<br>de<br>consulta<br>à<br>Compra<br>no<br>Transparência;<br>- Ação de alterar ata.|
|---|---|---|
|18/05/2023|2.0.00|- Retificar ata;<br>- Atualizações do Transparência;<br>- Inclusão e exclusão de arquivo ao criar ata;<br>- Melhorias na solicitação de adesão;<br>- Inclusão da classificação do fornecedor por item;<br>- Melhorias na busca por compra;<br>- Novos campos ao criar ata;<br>- Situação da ata de registro depreços.|

4 | 1 3 2

<!-- pagina 5 -->
|Sumário||
|---|---|
|1.<br>Apre|sentação .................................................................................................................................. 7|
|2.<br>Gru|po de usuários ........................................................................................................................... 7|
|2.1.|Atribuição de perfis ............................................................................................................ 8|
|2.2.|Órgãos e entidades da Administração Pública federal direta, autárquica e fundacional .. 8|
|2.3.|Órgãos e entidades dos poderes judiciário e legislativo federal ........................................ 8|
|2.4.|Órgãos e entidades das esferas Estadual e Municipal ....................................................... 9|
|3.<br>Tela|de autenticação do sistema .................................................................................................... 9|
|4.<br>Iníci|o .............................................................................................................................................. 12|
|5.<br>Gest|ão contratual ......................................................................................................................... 14|
|6.<br>Com|pras ........................................................................................................................................ 14|
|7.<br>Fisc|alização e Gestão de Contratos............................................................................................... 17|
|7.1.|Ordem de Serviço/Fornecimento ........................................................................................ 20|
|7.1.|1. Informar OS/F ................................................................................................................... 22|
|7.1.|2. Ações na OS/F ................................................................................................................... 25|
|7.1.|3. Criar OS/F ......................................................................................................................... 34|
|7.1.|4. Assinar OS/F ..................................................................................................................... 39|
|7.2.|Informar Declaração Decreto 11.430/2023 ........................................................................ 41|
|7.3.|Entregas ............................................................................................................................... 44|
|7.3.|1. Parametrização automática do Contrato ......................................................................... 44|
|7.3.|2 Entregas cadastradas pelo fornecedor ................................................................................ 46|
|7.3.|3. Adicionar Entrega ................................................................................................................ 46|
|7.3.|3. Termo de Recebimento Provisório (TRP) ............................................................................ 54|
|7.3.|4. Termo de Recebimento Definitivo (TRD) ............................................................................ 64|
|7.4.|Visualizar Preposto do Contrato .......................................................................................... 74|
|7.4.|1. Adicionar Preposto do Contrato ....................................................................................... 75|
|8.<br>Instr|umento de cobrança .............................................................................................................. 75|
|9.<br>Gest|ão de Atas .............................................................................................................................. 83|
|9.1.|Listar Atas de Registro de Preços ........................................................................................ 83|
|9.2.|Cadastro de Ata de Registro de Preços ............................................................................... 85|
|9.3.|Arquivos de Ata de Registro de Preços................................................................................ 92|
|9.4.|Envio de Ata de Registro de Preços para o PNCP ................................................................ 95|
|9.5.|Retificação de Ata de Registro de Preços ............................................................................ 96|
|9.6.|Alteração de Ata de Registro de Preços .............................................................................. 98|
|9.7.|Remanejamento das quantidades registradas na ata de Registro de Preços ................... 106|
|9.8.|Relatório de execução de Ata ............................................................................................ 111|

5 | 1 3 2

<!-- pagina 6 -->
|9.9.|Adesão a Atas .................................................................................................................... 114|
|---|---|
|9.9.1|. Solicitar adesão à ata de registro de preços .................................................................. 115|
|9.9.2|. Analisar solicitação de adesão ........................................................................................ 120|
|10. Trans|parência .............................................................................................................................. 124|
|10.1.|Acesso ao módulo Transparência ...................................................................................... 124|
|10.2.|Transparência – Tela inicial ............................................................................................... 125|
|10.3.|Transparência – Consultar Atas ......................................................................................... 125|
|10.4.|Transparência – Consultar Atas por item .......................................................................... 128|
|10.5.|Transparência – Atas de Registro de Preços ..................................................................... 129|
|10.6.|Transparência – Consultar Compras .................................................................................. 130|

6 | 1 3 2

<!-- pagina 7 -->
## 1. Apresentação 

A Nova Versão é uma solução integrante do sistema Contratos.gov.br, desenvolvida pelo Ministério da Gestão e da Inovação em Serviços Públicos (MGI), com uma tecnologia mais moderna e _design system_ padronizado com os sistemas estruturantes, trazendo novos módulos disponibilizados. 

Embora o Contratos.gov.br possua duas versões - <u>Contratos.gov.br</u> – Versão Original e a <u>Contratos.gov.br</u> - Nova Versão, trata-se do mesmo sistema, cujo cadastro do usuário é o mesmo para acesso em ambas as versões. 

Entre esses módulos, temos o de **Gestão de Atas** , que possibilita aos órgãos e entidades da administração pública direta, autárquica e fundacional, incluindo as empresas estatais, estados e municípios, realizar de forma integrada a gestão das atas de registro de preços com amparo na Lei nº 14.133/2021 e suas derivadas, além de divulgar as informações e suas eventuais alterações no PNCP, em atendimento à citada lei. 

A ferramenta promove a gestão de atas de registro de preços, conectando as unidades, divulgando e agregando transparência às atas de registro de preços e ações relacionadas, aprimorando as condições gerenciais envolvidas. 

Outro módulo disponibilizado é o **Fiscalização e Gestão de Contratos** , que possibilitará ao gestor e fiscal uma atuação mais personalizada e integrada de suas ações, inicialmente trazendo a funcionalidade da Ordem de Serviço/Fornecimento. As antigas funcionalidades (Arquivos, Conta-depósito Vinculada, Empenhos, Instrumento de Cobrança, Terceirizados e Relatório Final) continuam na Versão Original do sistema Contratos.gov.br, devendo ser migradas paulatinamente para a Nova Versão. 

Por fim, existe o módulo do Fornecedor, um ambiente disponível para interação com a Administração Pública, que possui um manual próprio, disponível em <u>Manual Contratos.gov.br - Nova Versão - Perfil Fornecedor.</u> 

## **Quem pode utilizar:** 

Órgãos e entidades da administração pública federal direta, autárquica e fundacional, bem como empresas estatais, estados e municípios – estes últimos apenas para acesso ao módulo gestão de atas. 

**Modelo de oferta do módulo:** disponibilizado de forma centralizada como parte do Contratos.gov.br, evitando a manutenção de outros sistemas afins, de forma isolada, estabelecendo medidas de eficiência organizacional para o aprimoramento da administração pública. 

2. Grupo de usuários 

**TIPO DESCRIÇÃO** 

7 | 1 3 2

<!-- pagina 8 -->
|Gestor de Atas|Tem permissão de acesso ao módulo Gestão de Atas, podendo adicionar,<br>editar e excluir rascunhos de atas de registro de preços, ativar atas,<br>incluir arquivos de atas, solicitar adesão a atas de outras unidades e<br>analisar solicitações de adesão a atas de sua unidade, solicitar<br>remanejamento de outra unidade e analisar remanejamento de sua<br>unidade, realizar cancelamentos de itens, de atas, de adesão e de<br>remanejamentos.|
|---|---|
|Responsável por<br>contratos|Tem permissão para acessar o módulo Fiscalização e Gestão de<br>Contratos, podendo adicionar, editar e excluir rascunhos de ordem de<br>serviço/fornecimento (OS/F) e suas ações.|

## 2.1. Atribuição de perfis 

A atribuição de perfis será realizada no sistema Contratos.gov.br – Versão Original, conforme item 6 do <u>Manual do Contratos.gov.br - Versão Original.</u> 

2.2. Órgãos e entidades da Administração Pública federal direta, autárquica e fundacional 

Para os órgãos e entidades da Administração Pública federal direta, autárquica e fundacional, o grupo Gestor de Atas deve ser atribuído ao usuário pelo administrador de órgão ou administrador de unidade no sistema Contratos.gov.br – Versão Original. 

## 2.3. Órgãos e entidades dos poderes judiciário e legislativo federal 

Os órgãos e entidades dos poderes judiciário e legislativo federal **, que já fizeram adesão ao Sistema Integrado de Administração de Serviços Gerais (Siasg) e já utilizam o Contratos.gov.br** , deverão ter o(s) perfil(is) pertinente(s) ao módulo desejado atribuído(s) aos seus usuários pelo administrador de órgão ou pelo administrador de unidade no <u>Contratos.gov.br – Versão Original.</u> 

Os órgãos e entidades dos poderes judiciário e legislativo federal, **que já fizeram adesão ao Siasg e não utilizam o Contratos.gov.br,** deverão abrir chamado junto à <u>Central de Atendimento, informando os dados de sua unidade e indicando um administrador de órgão.</u> Para indicação do administrador de órgão, deverá ser encaminhado um ofício de indicação assinado por autoridade competente. 

Os órgãos e entidades dos poderes Judiciário e Legislativo federal, que **não fizeram adesão ao Siasg,** deverão fazer a adesão ao Siasg e, após aprovação, deverá abrir chamado junto à <u>Central de Atendimento, informando os dados de sua unidade e indicando um administrador</u> de órgão. Para indicação do administrador de órgão, deverá ser encaminhado um ofício de 

8 | 1 3 2

<!-- pagina 9 -->
indicação do administrador, assinado por autoridade competente, contendo o CPF, nome, e- mail e unidade Siasg do usuário a ser cadastrado. 

## 2.4. Órgãos e entidades das esferas Estadual e Municipal 

Os órgãos e entidades das esferas Estadual e Municipal, que **já fizeram adesão ao Siasg,** terão seu cadastro realizado automaticamente no Contratos.gov.br. Serão cadastrados no Contratos.gov.br os administradores de órgão (perfil equivalente ao cadastrador parcial do Siasg), os administradores de unidade (perfil equivalente ao cadastrador local do Siasg) e os gestores de atas (perfil equivalente ao gestor de atas do Siasg). Esses usuários deverão realizar seu primeiro acesso ao Contratos.gov.br pelo Acesso Gov.br. O perfil de responsável por contratos deverá ser atribuído pelos administradores de unidade. Os administradores de órgãos alteram os usuários que são administradores de unidade e, por sua vez, o administrador de órgão deverá abrir chamado junto à Central de Atendimento para ter seu perfil alterado. 

Os órgãos e entidades das esferas estadual e municipal, que **ainda não fizeram adesão ao** **<u>Siasg,</u>** deverão fazê-la e, após aprovação, deverão abrir chamado junto à <u>Central de Atendimento, informando os dados de sua unidade e indicando um administrador de órgão.</u> Para indicação do administrador de órgão, deverá ser encaminhado um ofício de indicação do administrador, assinado por autoridade competente, contendo o CPF, nome, e-mail e unidade Siasg do usuário a ser cadastrado. Ao administrador de órgão caberá a inclusão e a edição dos administradores de unidade, e a ambos caberão a inclusão e a edição dos demais usuários. Sempre que o administrador de órgão precisar ter seu cadastro alterado, deverá abrir chamado junto à Central de Atendimento. 

## 3. Tela de autenticação do sistema 

Desde 01º de novembro de 2024, o acesso ao sistema de contratos.gov.br no ambiente de produção é realizado exclusivamente por meio de login do Gov.br, com conta nível prata ou ouro, conforme alertado anteriormente em comunicado apresentado até essa data. 

9 | 1 3 2

<!-- pagina 10 -->
_Figura 1 – Mensagem de alerta para nova forma de login no sistema_ 

Ao acessar o sistema Contratos.gov.br, tanto na versão original, quanto na nova versão, será apresentada a nova tela de acesso com a opção de login pelo Gov.br e o acesso ao portal da transparência do sistema, bem como um ícone para acesso ao Portal de Serviços para abertura de chamados em caso de problema com o login. Haverá indicação na tela do ambiente em que o usuário está no canto inferior direito: produção ou treinamento, bem como a indicação de qual versão do sistema está sendo o login, logo abaixo do logo. 

_Figura 2 – Tela de login para acesso ao ambiente de produção na nova versão do sistema_ 

10 | 1 3 2

<!-- pagina 11 -->
_Figura 3 – Tela de login para acesso ao ambiente de produção na versão original do sistema_ 

O ambiente de treinamento também passou por atualização, contudo o login permanece exclusivamente por meio de CPF e senha próprios do sistema nesse ambiente, servindo tanto para a versão original, quanto para nova versão. 

_Figura 4 – Tela de login para acesso ao ambiente de treinamento na nova versão do sistema_ 

11 | 1 3 2

<!-- pagina 12 -->
_Figura 5 – Tela de login para acesso ao ambiente de treinamento na versão original do sistema_ 

**Atenção 1:** Usuários de estados e municípios cadastrados automaticamente no sistema deverão realizar seu primeiro acesso pelo Gov.br. 

**Atenção 2** : Para mais informações sobre como cadastro e aumento de nível da conta no Gov.br, acesse o link <Conta gov.br — Governo Digital (www.gov.br)>. 

4. Início 

Abaixo, imagem com detalhamento de todos os componentes da página inicial do sistema na Nova Versão. 

12 | 1 3 2

<!-- pagina 13 -->
M A N U A L T É C N I C 

O O P E R A C I O N A L – **C O N T R A T O S . G O V . B R I N O V A V E R S Ã O** 

_Figura 6 - Tela inicial do sistema_ 

13 | 1 3 2

<!-- pagina 14 -->
## 5. Gestão contratual 

Ao acessar o menu Gestão Contratual, o usuário é direcionado para a tela de início do sistema Contratos.gov.br – Versão Original, também disponível em: <u>https://contratos.comprasnet.gov.br/login.</u> 

## 6. Compras 

Todos os dados das compras utilizadas para a realização de empenhos, a formalização de contratos e as atas de registro de preços são automaticamente salvos. Ou seja, apenas os dados da compra que tiveram alguma ação do usuário no Sistema do Contratos.gov.br serão apresentados. Caso ainda não tenha sido cadastrada ata de registro de preço, realizado empenho ou cadastrado contrato, mesmo que em rascunho, os dados não serão encontrados, devendo ser consultados diretamente no sistema Compras.gov.br. 

No menu Compras > Visualizar são apresentadas as informações referentes a essas compras. 

Na parte superior da lista, há filtros de unidade origem; unidade sub-rogada; tipo de compra (SISRP ou SISPP); modalidade e lei, para facilitar a localização da compra desejada. 

_Figura 7 - Visualizar Compra_ 

Ao clicar na ação Visualizar , o usuário tem acesso às informações sobre a compra. 

14 | 1 3 2

<!-- pagina 15 -->
M A N U A L T É C N I C O O P E R A C I O N A L – **C O N T R A T O S . G O V . B R I N O V** 

**A V E R S Ã O** 

_Figura 8 - Visualizar compra_ 

Ao clicar na ação Itens , o usuário tem acesso às informações sobre os itens que compõem a compra. 

_Figura 9 - Visualizar itens da compra_ 

Ao clicar na ação Visualizar de cada item, são apresentadas informações do item, abrangendo unidades participantes, fornecedores homologados e sobre a ata de registro de preços do item (se houver, somente as regidas pela Lei nº 14.133/2021). 

15 | 1 3 2

<!-- pagina 16 -->
_Figura 10 - Visualizar itens da compra_ 

Ao clicar na ação Visualizar de cada fornecedor, são apresentadas informações referentes a contratos firmados, empenhos emitidos e suas alterações. 

_Figura 11- Visualizar fornecedores_ 

16 | 1 3 2

<!-- pagina 17 -->
## 7. Fiscalização e Gestão de Contratos 

Módulo direcionado a usuários com perfil “responsável por contrato”, a fim de que exerçam suas atividades de gestão e fiscalização dos contratos ao qual estejam vinculados como responsáveis. 

Inicialmente, será disponibilizada a funcionalidade de cadastro de ordens de serviço/fornecimento nos contratos que estejam sob sua responsabilidade. As funcionalidades já existentes na Versão Original do sistema – disponíveis em Gestão Contratual > Meus Contratos > Mais > Arquivos/Conta-depósito Vinculada/Empenhos/Instrumentos de Cobrança/Ocorrências/Terceirizados/Relatório Final – continuam disponíveis e sendo acessadas pelo mesmo local, sendo migradas paulatinamente para a Nova Versão do sistema. 

O usuário com perfil “responsável por contrato” poderá acessar o novo módulo tanto pela Versão Original quanto pela Nova Versão do sistema, com mesmo _login_ e senha para ambas. Vejamos: 

- Acessando o sistema por meio da Versão Original <u>(https://contratos.comprasnet.gov.br/login), o usuário deverá clicar no submenu Fiscalização</u> e Gestão de Contratos, localizado na barra lateral, sendo direcionado automaticamente para a página Meus Contratos na Nova Versão. 

_Figura 12 – Tela de acesso ao Sistema Contratos.gov.br – Versão Original_ 

17 | 1 3 2

<!-- pagina 18 -->
_Figura 13– Tela de acesso ao Sistema Contratos.gov.br – Versão Original_ 

_Figura 14 – Menu Fiscalização e Gestão de Contratos - Meus Contratos_ 

- Acessando o sistema diretamente pela Nova Versão 

- <u>(https://contratos.sistema.gov.br/login), terá acesso à tela inicial, devendo clicar no menu</u> 

, no lado esquerdo da tela, e acessar a opção Fiscalização e Gestão de Contratos ou pelo ícone de acesso rápido, que levará à página Meus Contratos. 

18 | 1 3 2

<!-- pagina 19 -->
_Figura 15 – Página de acesso ao sistema Contratos.gov.br – Nova Versão_ 

_Figura 16 – Menu lateral para acesso ao módulo Fiscalização e Gestão de Contratos_ 

_Figura 17 - Ícone de acesso rápido ao módulo Fiscalização e Gestão de Contratos_ 

19 | 1 3 2

<!-- pagina 20 -->
L T É C N I C O O P E R A C I O N A L – **C O N T R A T O S . G O V . B R I N O V A V E R S Ã O** 

M A N U A 

_Figura 18 - Menu Fiscalização e Gestão de Contratos - Meus Contratos_ 

Na tela dos Meus Contratos, serão apresentados apenas os contratos em que o usuário Setor Contratos cadastrou na versão original do sistema os respectivos responsáveis por contrato. 

A seguir, serão apresentadas as opções disponíveis dentro das Ações de Meus Contratos na Nova Versão: 

## 7.1. Ordem de Serviço/Fornecimento 

Acessando Fiscalização e Gestão de Contratos > Meus Contratos > Ações > Ordem de Serviço/Fornecimento, o sistema apresenta a tela de cadastro/criação de uma nova ordem de serviço/fornecimento (OS/F) relacionada ao contrato identificado na página anterior, listando as que estão cadastradas/informadas no sistema. 

20 | 1 3 2

<!-- pagina 21 -->
_Figura 19 - Ação Ordem de Serviço/Fornecimento_ 

Nesse momento, clicando em Informar OS/F, o usuário poderá cadastrar uma ordem de serviço/fornecimento que foi registrada em um sistema externo. 

_Figura 20 – Informar Ordens de Serviço/Fornecimento e tela de listagem das já registradas para o contrato selecionado na página anterior_ 

E ao clicar em Criar OS/F, o usuário cadastrará uma nova ordem de serviço e/ou fornecimento diretamente no sistema com suas respectivas assinaturas. 

21 | 1 3 2

<!-- pagina 22 -->
_Figura 21 - Criar Ordens de Serviço/Fornecimento e tela de listagem das já registradas para o contrato selecionado na página anterior_ 

## 7.1.1. Informar OS/F 

Para informar uma OS/F que tem origem em um sistema externo, ou seja, diferente do Contratos.gov.br, o usuário deverá clicar no menu Fiscalização e Gestão de Contratos > Meus Contratos, localizar entre os contratos apresentados na tela aquele em que será informada a OS/F, clicar na ação Ordem de Serviço/Fornecimento e clicar em Informar OS/F. 

_Figura 22 - Informar uma nova ordem de serviço/fornecimento_ 

O sistema apresentará um cabeçalho com os dados do contrato escolhido e, logo abaixo, os campos para preenchimento para identificação da OS/F. Posteriormente, ao se clicar em Adicionar Item, o sistema apresentará uma caixa para seleção dos itens do contrato que comporão essa OS/F. 

22 | 1 3 2

<!-- pagina 23 -->
_Figura 23 - Cabeçalho com informações do contrato e campos de cadastro da OS/F._ 

_Figura 24 - Adicionar item na OS/F._ 

23 | 1 3 2

<!-- pagina 24 -->
Ato contínuo, o usuário, ao clicar em , deverá registrar os campos de identificação para cada item selecionado no passo anterior. 

_Figura 25 - Campos de preenchimento para um item da OS/F_ 

Nesse momento, após o preenchimento das informações anteriores, o usuário poderá: 

- a) Cancelar as informações que foram cadastradas, clicando em Cancelar. Nesse caso, as informações não serão salvas e o sistema retornará para a tela anterior. 

- b) Salvar as informações registradas até o momento para finalização posterior do cadastro, clicando em Salvar Rascunho. 

- c) Finalizar o registro da OS/F, clicando em “Adicionar OS/F”. Nesse caso, a OS/F terá sua situação alterada para “em execução”. 

_Figura 26 - Ações ao informar uma OS/F no sistema_ 

Uma OS/F informada pode ter as seguintes situações: 

- Em elaboração: quando salva em rascunho, não tendo impacto para as demais ações futuras do usuário; 

- Em execução: quando salva definitivamente, estando apta a produzir efeitos assim que iniciar o seu período de vigência inicial; 

- Vigência Expirada: quando o período de vigência da Ordem de Serviço / Fornecimento expira a vigência, mas o saldo dos itens ainda não foi completamente utilizado. 

- Concluído: Quando o saldo dos itens foi totalmente utilizado e o prazo da vigência. 

24 | 1 3 2

<!-- pagina 25 -->
_Figura 27 - Situações e Ações de uma OS/F_ 

## 7.1.2. Ações na OS/F 

Após informar ou criar uma OS/F, os responsáveis pelo contrato podem atuar nelas de acordo com as ações apresentadas a seguir: 

_7.1.2.1 Visualizar_ 

Através do ícone é possível visualizar e acessar as principais informações relacionadas à OS/F, tais como visualizar e fazer download da OS/F assinada ou anexada, acompanhar histórico de execução do(s) item(ns), entre outros. 

25 | 1 3 2

<!-- pagina 26 -->
M A N U A L T É C N I C O O P E R A C I O N A L – **C O N T R A T O S . G O V . B** 

**R I N O V A V E R S Ã O** 

_Figura 28 - Visualizar informações da OS/F_ 

_7.1.2.2. Retificar OS/F_ 

Após a inclusão de uma OS/F com situação ativa, ao perceber alguma informação cadastrada em desacordo, poderá registrar uma retificação do dado cadastrado equivocadamente. 

Para isso será necessário clicar na ação Retificar , adicionar retificação, alterar o(s) campo(s) 

preenchido(s) incorretamente, clicar em Retificar 

_Figura 29 - Retificar uma OS/F_ 

26 | 1 3 2

<!-- pagina 27 -->
_Figura 30 - Campos de registro de uma retificação_ 

_Figura 31 - Salvar uma retificação de OS/F_ 

Importante destacar que o cadastro de uma justificativa é obrigatório para salvar o registro da retificação. 

27 | 1 3 2

<!-- pagina 28 -->
Após o cadastro de uma retificação, o sistema retornará à página anterior, onde é possível cadastrar novas retificações, bem como visualizar as retificações cadastradas. 

_Figura 32 - Registro de uma retificação cadastrada_ 

Nessa página é possível, ainda, clicar na ação Visualizar . O sistema então apresenta uma página com as informações alteradas pela retificação, comparando como eram antes do registro e como ficaram após a retificação cadastrada. 

_Figura 33 - Visualização dos campos retificados_ 

28 | 1 3 2

<!-- pagina 29 -->
## _7.1.2.3. Alterar OS/F_ 

Há também casos em que é preciso alterar o que foi pactuado em uma OS/F. Nesse caso, não se trata de uma informação cadastrada incorretamente, mas de uma nova condição pactuada entre contratante e contratada para a execução de uma determinada OS/F. 

Para alterar uma OS/F, ação permitida apenas para OS/F com situação “Em execução” ou “Vigência Expirada”, o responsável pelo contrato deverá seguir o caminho: localizar o contrato em Meus Contratos > clicar na ação Ordem de Serviço/Fornecimento > localizar a 

OS/F que será alterada > clicar na ação Alterar > clicar em Adicionar Alteração. 

_Figura 34 - Adicionar uma Alteração em uma OS/F_ 

Nesse momento o responsável pelo contrato encontrará duas possibilidades de alteração da OS/F: 

- Vigência: para os casos em que há a necessidade de se antecipar ou prorrogar o prazo de execução da OS/F; 

- Item (Acréscimo/Supressão): quando há a necessidade de incluir algum item do contrato ainda não contemplado na OS/F ou quando se pretende aumentar (acréscimo) ou diminuir (supressão) a quantidade de itens já cadastrados na OS/F. 

29 | 1 3 2

<!-- pagina 30 -->
M A N U A L T É C 

N I C O O P E R A C I O N A L – **C O N T R A T O S . G O V . B R I N O V A V E R S Ã O** 

_Figura 35 - Possibilidades de alteração de uma OS/F_ 

Destacamos que, para o cadastro de uma alteração, é necessário que o responsável preencha os campos obrigatórios Data de início da alteração e Justificativa da Alteração. Após todos os campos preenchidos, clicar em Enviar para Assinatura. 

30 | 1 3 2

<!-- pagina 31 -->
_Figura 36 - Salvar uma alteração de OS/F_ 

Após o cadastro de uma alteração, o sistema retornará à página anterior, onde é possível cadastrar novas alterações, bem como visualizar as alterações cadastradas. 

Nessa página, é possível, ainda, clicar em Visualizar . O sistema, então, apresenta uma página com as informações modificadas, comparando como eram antes do registro e como ficaram após a alteração cadastrada. 

_Figura 37 - Registro de uma alteração cadastrada_ 

31 | 1 3 2

<!-- pagina 32 -->
## _7.1.2.4. Duplicar OS/F_ 

A ação Duplicar  foi desenvolvida com a intenção de facilitar o cadastro de OS/F recorrentes, como é o caso de serviços continuados. 

_Figura 38 - Duplicar uma OS/F já cadastrada_ 

Ao Localizar o contrato em Meus Contratos, clicar na ação Ordem de Serviço/Fornecimento. O ícone Duplicar  aparecerá como opção de ação para todas as OS/F, com exceção daquelas com situação “Em elaboração”. 

Clicando em Duplicar, o sistema apresentará, no topo da lista das OS/F registradas para o contrato identificado anteriormente, uma nova OS/F com situação “Em elaboração”, idêntica à OS/F duplicada. Basta o reponsável clicar na ação Editar e alterar os dados referentes à nova OS/F que precisa ser cadastrada. 

32 | 1 3 2

<!-- pagina 33 -->
_Figura 39 - OS/F duplicada_ 

_7.1.2.5. Visualizar Histórico da OS/F_ 

Neste menu, disponível no ícone , é possível acompanhar o histórico referente às assinaturas do documento, quando houve sua solicitação, recusa ou quando foi assinado. 

_Figura 40 – Ação de visualização de histórico da OS/F_ 

33 | 1 3 2

<!-- pagina 34 -->
_Figura 41 – Histórico de assinaturas de uma OS/F_ 

## 7.1.3. Criar OS/F 

Diferente do Informar OS/F, onde o documento foi elaborado e assinado fora do Sistema, a opção Criar OS/F traz a possibilidade para que o fiscal do contrato inicie o documento e o assine dentro do próprio Sistema, inclusive com a opção de assinatura pelo fornecedor contratado. 

Antes de criar uma OS/F, é importante conferir se o Setor Contratos cadastrou corretamente os responsáveis pelo contrato, sendo obrigatória a indicação de um gestor ou seu substituto., bem como se houve o cadastro do preposto da contratada. 

Para criar uma OS/F, o usuário deverá clicar no menu Fiscalização e Gestão de Contratos > Meus Contratos, localizar entre os contratos apresentados na tela aquele para o qual será criada a OS/F, clicar na ação Ordem de Serviço/Fornecimento e clicar em “Criar OS/F”. 

_Figura 42 - Criar ordem de serviço/fornecimento_ 

O sistema apresentará um cabeçalho com os dados do contrato escolhido e, logo abaixo, os campos para preenchimento da OS/F. Posteriormente, ao se clicar em Adicionar Item, o 

34 | 1 3 2

<!-- pagina 35 -->
sistema apresentará uma caixa para seleção do(s) item(ns) do contrato que comporá(ão) essa OS/F. 

Atenção para data de início de vigência, pois na criação da Ordem de Serviço/Fornecimento esta deve ser igual ou posterior à data em que estiver sendo criada, haja vista que sua assinatura ainda será realizada dentro do Sistema, não sendo possível a criação de uma OS/F com data de vigência retroativa. 

Caso seja indicado um dia anterior ao atual ou a vigência seja alterada, o(s) item(ns) informado(s) precisará(ão) ser reinserido(s). 

_Figura 43 – Cabeçalho com informações do contrato_ 

_Figura 44 – Cadastro de OS/F_ 

35 | 1 3 2

<!-- pagina 36 -->
_Figura 45 - Adicionar item(ns) na OS/F_ 

_Figura 46 – Mensagem de erro quando a data de vigência início é retroativa na criação da OS/F_ 

Observação: Caso o período de vigência indicado para a OS/F que está sendo criada compreenda o período de vigência de mais de um termo do contrato em questão, o item selecionado criará uma linha para cada um dos períodos compreendido na vigência da OS/F. 

_Figura 47 – Detalhamento do mesmo item para períodos de vigência distintos_ 

36 | 1 3 2

<!-- pagina 37 -->
Ato contínuo, o usuário, ao clicar em , deverá registrar os campos de identificação para cada item selecionado no passo anterior. 

_Figura 48 - Campos de preenchimento para um item da OS/F_ 

Ainda é possível ao usuário cadastrar informações complementares referentes ao serviço/bem que está sendo contratado, bem como inserir documentos anexos à OS/F que está sendo cadastrada. 

_Figura 49 – Campos de preenchimento para informações detalhas e anexo de arquivos da OS/F_ 

Nesse momento, após o preenchimento das informações anteriores, o usuário poderá cancelar as informações que foram cadastradas, clicando em “Cancelar” (nesse caso, as informações não serão registradas e o sistema retornará para a tela anterior); salvar as 

37 | 1 3 2

<!-- pagina 38 -->
informações registradas até o momento para finalização posterior do cadastro, clicando em “Salvar Rascunho”; ou enviar a OS/F para assinatura clicando em “Enviar para Assinatura”. 

_Figura 50 - Criar OS/F no sistema – possibilidade de registro_ 

Ao clicar em “Enviar para Assinatura” o sistema abrirá uma caixa para que sejam selecionados os signatários da OS/F que está sendo criada. É obrigatória a seleção de pelo menos um Gestor/gestor substituto do contrato. 

_Figura 51 – Informar os signatários que assinarão a OS/F_ 

Após selecionados os signatários a OS/F, esta será enviada para assinatura, encaminhando um e-mail de notificação para os responsáveis identificados como signatários, que poderão visualizar a ação “Assinar OS/F” no registro que acabou de ser criado. 

38 | 1 3 2

<!-- pagina 39 -->
As ações de retificar, alterar e duplicar OS/F são as mesmas previstas no item 7.1.2. anterior, aplicáveis tanto para informação, quanto para criação de uma OS/F. 

## 7.1.4. Assinar OS/F 

Após a criação de uma OS/F, os signatários escolhidos receberão um e-mail informando que existe uma OS/F pendente de assinatura e também ao acessarem a listagem de OS/F ficará visível a situação como “Aguardando assinatura” e estará habilitado o ícone na coluna ações. 

_Figura 52 – OS/F aguardando assinatura_ 

Ao clicar no ícone , o usuário será direcionado para a página onde será possível verificar o PDF gerado da OS/F, realizar a assinatura dentro do próprio sistema com a ferramenta de assinatura digital do Gov.br, desde que seja de nível prata ou ouro, bem como recusar a assinatura caso exista alguma necessidade de correção. A opção “Cancelar”, fará com que o usuário volte à tela anterior sem realizar qualquer ação. 

A assinatura do gestor ou do gestor substituto fará com que a OS/F mude sua situação para “Em execução”, sendo facultativa a assinatura dos demais integrantes da equipe de fiscalização e do preposto da contratada, quando indicados. 

39 | 1 3 2

<!-- pagina 40 -->
M A N U A L T É C N I C O O P E R A C I O N A L – **C O N T R A T O S . G O V . B R I N** 

**O V A V E R S Ã O** 

_Figura 53 - Assinar OS/F_ 

40 | 1 3 2

<!-- pagina 41 -->
## 7.2. Informar Declaração Decreto 11.430/2023 

Para contratos da categoria mão de obra, que tenha sido informado pelo Setor Contratos no registro do contrato a aplicabilidade do Decreto 11.430/2023, será exibido ao Responsável por contrato nas Ações do módulo Fiscalização e gestão contratual a para adicionar a declaração de atendimento ao respectivo Decreto, por meio do ícone . 

_Figura 54 – Incluir as informações da Declaração OPM_ 

Ao clicar no ícone , serão listadas todas as Declarações eventualmente inseridas naquele contrato com as ações de visualizar, fazer o download ou exclusão. O usuário também pode inserir uma nova declaração clicando no botão “Adicionar declaração”. 

41 | 1 3 2

<!-- pagina 42 -->
_Figura 55 – Listagem de Declarações do contrato e opção para adicionar novo registro_ 

Ao clicar no botão “Adicionar declaração”, o usuário deverá incluir os dados da declaração e anexar o arquivo da declaração emitida pelo órgão responsável, clicando em “Criar Declaração” para que ela seja salva como um Arquivo do Contrato e disponibilizada no ambiente de Transparência da Versão Original do sistema. 

_Figura 56 – Inclusão das informações da Declaração OPM_ 

_Figura 57 – Arquivo salvo automaticamente no contrato após inclusão da Declaração no Sistema_ 

42 | 1 3 2

<!-- pagina 43 -->
_Figura 58 – Consulta ao contrato no ambiente de Transparência da versão original do Sistema_ 

_Figura 59 - Consulta ao contrato no ambiente de Transparência da versão original do Sistema Contratos – continuação – Arquivos da Declaração do Decreto 11.430/2023 salvos e disponibilizados no Transparência_ 

Selecionando a opção “Salvar Rascunho”, o documento será salvo para conclusão posterior, mas sem salvar como arquivo do contrato e nem disponibilização no Transparência. 

43 | 1 3 2

<!-- pagina 44 -->
## 7.3. Entregas 

A funcionalidade **Entregas** é destinada ao registro, acompanhamento e aceite dos bens fornecidos ou serviços prestados pela contratada, garantindo rastreabilidade da execução física do objeto contratual. 

É possível cadastrar entregas relacionadas diretamente aos itens do Contrato (quando não há emissão de OS/F) ou relacionadas aos itens de uma OS/F. No momento do registro da entrega, a seleção dos itens do contrato ou da OS/F dependerá de como o Contrato está parametrizado, conforme detalhado em 7.3.1. 

Independentemente de ser vinculada a uma OS/F ou não, a entrega pode ser realizada de duas formas, de acordo com a execução física do objeto: 

**Entrega Parcial:** Ocorre quando o fornecimento ou prestação de serviço é realizado em parcelas. O sistema permite o registro fracionado de um ou de vários itens, controlando o saldo remanescente até que todo o objeto seja entregue. 

**Entrega Total:** Ocorre quando o registro engloba, em um único evento, todos os itens e a totalidade do quantitativo previsto no contrato ou na respectiva OS/F. 

O registro das entregas não é restrito apenas à Administração. O sistema permite uma gestão colaborativa, onde a entrega pode ser cadastrada por dois perfis distintos: 

**Órgão Contratante:** realizado pelos atores da gestão e fiscalização de contratos vinculados ao processo. 

**Fornecedor:** o próprio fornecedor contratado, por meio de seu **preposto** , possui autonomia para registrar a entrega diretamente no sistema através do **Módulo Fornecedor** . Isso agiliza o fluxo de comunicação e permite que a fiscalização apenas valide o que foi informado pela empresa. 

## 7.3.1. Parametrização automática do Contrato 

A parametrização do contrato pode ser realizada manualmente no módulo Gestão Contratual, através da seleção do contrato > ações > mais > Parâmetros, ou automaticamente no módulo Fiscalização e Gestão Contratual. 

44 | 1 3 2

<!-- pagina 45 -->
_Figura 60 - Cadastro de Parâmetros no módulo Gestão Contratual_ 

A parametrização do contrato define a obrigatoriedade ou não de emissão e Ordens de Serviço/Fornecimento, a obrigatoriedade de assinatura do preposto da OS/F, dentre outros campos. 

No módulo Fiscalização e Gestão e Contratual, a depender da ação do usuário, o contrato será parametrizado automaticamente para a obrigatoriedade ou não de emissão de OS/F e assinatura do preposto. 

Caso a primeira ação do usuário no contrato seja cadastrar uma OS/F, os parâmetros ficam com a seguinte configuração: 

- Obrigatório registro de OS/F: Sim; 

- A assinatura do preposto é obrigatória na OS/F?: Não. 

A parametrização automática se dará assim que o usuário clicar no botão “+ Informar OS/F” ou “+ Criar OS/F”. 

Caso a primeira ação do usuário seja cadastrar uma entrega, os parâmetros ficam com a seguinte configuração: 

- Obrigatório registro de OS/F: Não; 

- A assinatura do preposto é obrigatória na OS/F?: Não. 

Da mesma forma, a parametrização automática se dará assim que o usuário clicar no botão “+ Adicionar Entrega”. 

Além dos parâmetros indicados acima, o sistema também atribuirá o prazo de 10 dias úteis para o Recebimento Provisório e para o Recebimento Definitivo em cada uma das situações. 

Os parâmetros automáticos podem ser visualizados e editados normalmente pelos usuários autorizados, através do menu ações > mais > parâmetros, no módulo Gestão Contratual. 

Registra-se que no momento não é possível que um mesmo contrato possua entregas relacionadas conjuntamente a itens e a OS/Fs. 

Para contratos já existentes, caso o ícone de OS/F não esteja visível, deve-se solicitar a parametrização para o Setor Contratos. 

45 | 1 3 2

<!-- pagina 46 -->
## 7.3.2 Entregas cadastradas pelo fornecedor 

Quando uma entrega é cadastrada diretamente pelo fornecedor no sistema, é criada uma linha com a respectiva entrega que fica com a situação “Em Análise”, significando que a entrega está pendente de análise do órgão contratante, podendo aceitá-la ou recusá-la. No caso de recusa, caso a fiscalização do contrato identifique alguma inconsistência nos dados apontados pelo fornecedor, a entrega muda para a situação “Recusada” e as informações poderão ser corrigidas pelo fornecedor, ficando novamente com a situação “Em Análise” após ser corrigida e reenviada 

Ressaltamos que as entregas recusadas ou aprovadas com valor diferente do informado pelo fornecedor deverão obrigatoriamente ter uma justificativa disposta em campo específico no momento da análise da entrega. 

Caso a entrega seja aceita, já é possível iniciar a elaboração do Termo de Recebimento Provisório diretamente no sistema. 

_Figura_ 61 _- Entregas informadas pelo fornecedor em análise ou recusada_ 

## 7.3.3. Adicionar Entrega 

O registro de entregas no sistema varia conforme a existência de Ordens de Serviço/Fornecimento (OS/F) vinculadas ao contrato. 

No menu “Meus Contratos” do módulo “Fiscalização e Gestão de Contratos”, todos os contratos aparecerão incialmente com o ícone de OS/F ativo na coluna “ações”. 

## _7.3.2.1. Entregas em contratos com OS/F_ 

Em contratos com OS/F emitidas, o cadastro de entrega pode ser realizado por dois caminhos: 

a) Através da lista de contratos > Ações > Mais > Entregas. 

46 | 1 3 2

<!-- pagina 47 -->
_Figura 62 - Acesso às entregas pela lista de contratos_ 

Ao acessar por esse caminho, a tela seguinte exibirá uma lista de todas as entregas já realizadas, além do botão “+ Adicionar Entrega”, para que o usuário possa cadastrar a nova entrega. 

_Figura 63 - Página de entregas acessada pela lista de contratos_ 

Ao clicar no botão “+ Adicionar Entrega”, inicialmente serão exibidos os dados do contrato, seguidos da lista de OS/Fs para seleção. Serão listadas todas as OS/F vinculadas ao contrato, exceto aquelas com situação concluída ou em elaboração. 

Ressalta-se que, quando associadas a uma OS/F, as entregas devem ser vinculadas individualmente a uma única OS/F, admitindo-se, contudo, o cadastro de múltiplas entregas para uma mesma OS/F. 

47 | 1 3 2

<!-- pagina 48 -->
_Figura 64 - Seleção de OS/F no cadastro da entrega_ 

Após selecionar a OS/F, é preciso clicar no botão “+ Adicionar OS/F” e em seguida selecionar o(s) item(ns) da OS/F que farão parte da entrega, para então habilitar os campos quantidade e glosa, quando cabível. 

_Figura 65 - Seleção dos itens da OS/F na entrega_ 

b) Através da lista de OS/Fs > Ações > Entregas. 

48 | 1 3 2

<!-- pagina 49 -->
M A N U A L T É C N I C O O P E R A C I O N A L – **C O N T R A T O S . G O V . B R I N O V A V** 

**E R S Ã O** 

_Figura 66 - Acesso às entregas pela lista de OS/Fs_ 

Ao acessar a funcionalidade entregas através de uma OS/F, a tela seguinte apresentará apenas as entregas já realizadas vinculadas à OS/F selecionada. Isso acontece porque o filtro de OS/F, localizado abaixo do botão “+ Adicionar Entrega” é ativado. 

_Figura 67 - Página de entregas acessada por uma OS/F_ 

Com o filtro de OS/F ativo, ao clicar no botão “+ Adicionar Entrega”, a OS/F filtrada é adicionada automaticamente à entrega, bastando selecionar o(s) item(ns) para habilitar os campos quantidade e glosa. 

49 | 1 3 2

<!-- pagina 50 -->
_Figura 68 - Seleção dos itens na entrega de uma OS/F filtrada._ 

Continuando com o cadastro da entrega, ao final de cada item é apresentada uma barra de evolução que apresenta o percentual de entrega dos itens daquela OS/F. Ao lado da barra, posicionando o mouse sobre o ícone , é apresentado um quadro em que lista a situação das entregas daquele item, bem como o saldo disponível ainda a executar. 

_Figura 69 - Quadro de acompanhamento dos itens executados na Ordem de Serviço / Fornecimento_ 

Mais abaixo, existe um campo para inclusão de informações complementares, seguido de um campo para assinalar a origem da entrega, que pode ser a seguinte: 

**Origem Sistema Contratos** : quando o registro da entrega é realizado inicialmente no próprio sistema Contratos.gov.br; ou 

**Origem Sistema Externo:** quando a entrega já foi registrada em outro sistema, inclusive com a emissão de Termos de Recebimento Provisório e/ou Definitivo, e está sendo apenas informada/cadastrada no sistema Contratos.gov.br. Neste caso, é obrigatório o preenchimento do campo “Número da entrega no sistema externo”. 

50 | 1 3 2

<!-- pagina 51 -->
_Figura 70 - Seleção da origem da entrega_ 

Este campo substitui as ações “Comunicar Recebimento” e “Informar Recebimento” existentes anteriormente. 

Após seleção da origem da entrega, existem os campos para inclusão do local de execução, o mês e ano de referência, período ínicio da entrega, período fim da entrega, data efetiva da entrega, data prevista para o recebimento provisório e a data prevista para o recebimento definitivo. 

Por fim, ao final da página o usuário tem 3 opções: 

- Cancelar: Cancela a inserção dos dados e volta para a página anterior sem salvar; 

- Salvar Rascunho: Salva as informações inseridas, porém na situação “Rascunho”, ficando pendente de conclusão para que o fluxo de recebimento do objeto prossiga, e 

- Registrar Entrega: Valida e estando todos os dados corretos, salva as informações inseridas e a situação da entrega como “Em execução”. 

_Figura 71 - Botões tela de adicionar entrega_ 

_7.3.2.2. Entregas em contratos sem OS/F_ 

Já em contratos sem OS/F emitidas, o cadastro de entrega é realizado diretamente através da lista de contratos > Ações > Mais > Entregas > “+ Adicionar Entrega”. Nesse caso, o formulário de entrega apresentará os itens do contrato para registro das quantidades entregues. 

51 | 1 3 2

<!-- pagina 52 -->
É C N I C O O P E R A C I O N A L – **C O N T R A T O S . G O V . B R I N O V A V E R S Ã O** 

M A N U A L T 

_Figura 72 - Seleção de itens entregues em contrato sem OS/F_ 

Os passos seguintes são semelhantes ao cadastro de entregas com OS/F. 

Após clicar em “Registrar Entrega” e voltar para a tela de listagem das entregas, é possível acompanhar o prazo restante para finalização do fluxo do recebimento provisório e do recebimento definitivo, e outras informações incluindo as colunas na opção “Visibilidade da coluna”. 

Também é possível acessar o passo seguinte, qual seja, a elaboração do Termo de Recebimento Provisório, através do ícone existente na coluna “Ações”. 

52 | 1 3 2

<!-- pagina 53 -->
_Figura 73 - Acesso a informações através do Visibilidade da Coluna e acesos ao TRP._ 

A ação Duplicar  foi desenvolvida com a intenção de facilitar as entregas recorrentes 

Clicando em Duplicar, o sistema apresentará, no topo da lista das entregas registradas, uma nova entrega com situação “Em elaboração”, idêntica à entrega duplicada. Basta o reponsável clicar na ação Editar e alterar os dados referentes à nova entrega que precisa ser cadastrada. 

53 | 1 3 2

<!-- pagina 54 -->
É C N I C O O P E R A C I O N A L – **C O N T R A T O S . G O V . B R I N O V A V E R S Ã O** 

M A N U A 

_Figura 74 - Ação duplicar na listagem de entregas de uma OS/F_ 

## 7.3.3. Termo de Recebimento Provisório (TRP) 

O Termo de Recebimento Provisório é um documento que visa fazer o recebimento de maneira preliminar, na forma prevista no artigo 140 da Lei 14.133/21. Em se tratando de obras e serviços, o documento deverá ser assinado provisoriamente pelo responsável por seu acompanhamento e fiscalização, mediante termo detalhado, quando verificado o cumprimento das exigências de caráter técnico. Em se tratando de compras, o documento deverá ser assinado provisoriamente, de forma sumária, pelo responsável por seu acompanhamento e fiscalização, com verificação posterior da conformidade do material com as exigências contratuais. 

O acesso ao TRP pode ser realizado através da lista de contratos, ou através da listagem de entregas, clicando no ícone da coluna “Ações”. 

54 | 1 3 2

<!-- pagina 55 -->
_Figura 75 - Acesso à funcionalidade Elaborar Termo de Recebimento Provisório pela lista Meus Contratos_ 

_Figura 76 - Acesso à funcionalidade Elaborar Termo de Recebimento Provisório pela lista de entregas_ 

Quando acessado pela lista Meus Contratos, a tela seguinte apresenta a lista de todos os Termos de Recebimento já elaborados. 

55 | 1 3 2

<!-- pagina 56 -->
_Figura 77 - Tela Termo de Recebimento Provisório e lista de TRPs acessada pela lista de Contratos_ 

Quando acessado pela lista de entregas, a página seguinte apresenta a lista de todos os Termos de Recebimento já elaborados relacionados à entrega pelo qual foi encaminhado, ativando os filtros da listagem. 

_Figura 78 - Tela Termo de Recebimento Provisório e lista de TRPs acessada pela lista de entregas, com filtro ativo._ 

Ainda na página do Termo de Recebimento Provisório, o usuário encontra os seguintes botões de ação: 

- + Elaborar Termo Provisório: criação de um Termo de Recebimento Provisório no sistema Contratos.gov.br 

- + Informar Termo Provisório: registro de um Termo de Recebimento Provisório gerado em sistema externo. 

56 | 1 3 2

<!-- pagina 57 -->
_Figura 79 - Botões de ação para elaborar o Termo de Recebimento Provisório_ 

_7.3.3.1. Elaborar o Termo de Recebimento Provisório_ 

Um fiscal técnico ou substituto deve ter sido cadastrado como responsável pelo contrato para que seja vinculado à assinatura do TRP. 

57 | 1 3 2

<!-- pagina 58 -->
_Figura 80 – Um fiscal técnico ou técnico substituto precisa estar vinculado ao contrato para ser assinante do TRP_ 

58 | 1 3 2

<!-- pagina 59 -->
_Figura 81 – Elaborar TRP_ 

Ao iniciar a elaboração do TRP, são apresentados os dados principais do contrato, e campo obrigatório para inserção do texto de introdução quando se tratar de TRP criado no próprio sistema. 

Em seguida, é apresentada a lista de entregas já realizadas, para seleção da(s) entregas(s) que integrará(ão) o TRP. 

59 | 1 3 2

<!-- pagina 60 -->
_Figura 82 - Seleção de entregas do Termo de Recebimento Provisório_ 

Após selecionar as entregas, é preciso clicar no botão “+ Adicionar Entrega” para visualizar os itens entregues. 

Ao clicar no ícone , localizado ao lado esquerdo do item, o sistema apresenta os campos de quantidade, glosa, com as informações inseridas pelo fornecedor ou pelo próprio órgão no momento da entrega, e mais algumas informações facultativas, como competência, número de processo, entre outros, que podem ser inseridas de acordo com a necessidade. É preciso selecionar o item para que os campos sejam habilitados. 

**Atenção:** em contratos com Ordem de Serviço/Fornecimento, só podem ser selecionadas entregas relacionadas a uma mesma OS/F. 

60 | 1 3 2

<!-- pagina 61 -->
_Figura 83 - Campos opcionais para dados complementares referentes ao item_ 

No final do item também é apresentada a barra de evolução do TRP, com a opção de visualização de quadro resumo dos TRPs relacionados àquele item 

_Figura 84 - Quadro de acompanhamento de execução dos itens do contrato no TRP_ 

Continuando a elaboração do TRP, existe o campo para preenchimento de informações complementares. 

Caso o TRP tenha sido gerado em sistema externo, deve ser obrigatoriamente anexado o respectivo documento e preenchida a data de assinatura. 

61 | 1 3 2

<!-- pagina 62 -->
_Figura 85 - Campos TRP informado no sistema_ 

Por fim, ficam disponíveis as opções: 

- Cancelar: Cancela a inserção dos dados e volta para a página anterior sem salvar; 

- Salvar Rascunho: Salva as informações inseridas, porém na situação rascunho, ficando pendente de conclusão do TRP para que o fluxo de recebimento do objeto prossiga; e 

- Criar TRP: Opção para TRPs elaborados inicialmente no sistema Contratos.gov.br. Nesse botão é concluída a elaboração do Termo de Recebimento Provisório, dando prosseguimento na etapa de assinatura do documento gerado no próprio sistema. 

- Informar TRP: Opção para TRPs informados no sistema Contratos.gov.br, ou seja, criados em sistema externo. Nesse botão não é solicitada a assinatura do documento. 

_Figura 86 – Botões de ação de um TRP elaborado no sistema_ 

_Figura 87 - Botões de ação de TRP informado no sistema (gerado em sistema externo)_ 

Ao clicar em “Criar TRP”, o usuário deverá selecionar os signatários que assinarão o documento. É importante ressaltar que é obrigatória a seleção do servidor cadastrado como “Fiscal Técnico” ou seu substituto, podendo ser selecionados outros agentes da fiscalização de forma complementar para a assinatura. Para constar nesta listagem, o Setor Contratos precisa ter cadastrado os fiscais na opção “Responsáveis por Contrato” no módulo de Gestão Contratual na versão original do sistema Contratos.gov.br. 

62 | 1 3 2

<!-- pagina 63 -->
_Figura 88 - Seleção de signatários para assinatura de TRP_ 

## _<u>7.3.3.2. Assinar o Termo de Recebimento Provisório</u>_ 

Após a seleção dos signatários para a assinatura do Termo de Recebimento Provisório, este aparecerá na lista de TRPs elaborados com a situação “Aguardando Assinatura”, sendo possível acessar e fazer o _download_ do documento elaborado ou anexado clicando no ícone 

. Caso o usuário logado seja um dos marcados como signatários do documento, ficará disponível o ícone , que indica que existe um documento pendente de sua assinatura. 

_Figura 89 -  Situação Aguardando Assinatura do Termo de Recebimento Provisório_ 

Ao clicar no ícone , o usuário é levado para a tela de assinatura, sendo apresentado o arquivo PDF do Termo de Recebimento Provisório. Dessa forma, o usuário pode verificar o inteiro teor do documento, com as três opções ao final: 

- Voltar: volta para a tela anterior sem executar qualquer ação, ou seja, o Termo de Recebimento provisório continua na situação “Aguardando Assinatura”; 

- “Ajustar”: retorna à situação de elaboração, retirando a solicitação de assinatura, a fim de que sejam realizadas as correções no teor do documento e, posteriormente, volte a ser colocado para assinatura; 

- “Assinar”: realizará a assinatura do documento, utilizando a ferramenta de assinatura eletrônica da plataforma Gov.br, diretamente dentro do sistema. 

63 | 1 3 2

<!-- pagina 64 -->
_Figura 90 - Assinar Termo de Recebimento Provisório_ 

Após a assinatura a situação do TRP passa a ser “Em Execução” e no botão será possível realizar o _download_ do arquivo assinado, o qual também fica disponível para o fornecedor automaticamente. 

Também é possível seguir para a elaboração do Termo de Recebimento Definitivo, clicando no botão . 

_Figura 91 - Situação TRP Em Execução_ 

7.3.4. Termo de Recebimento Definitivo (TRD) 

O **Termo de Recebimento Definitivo (TRD)** é o documento que atesta a conformidade plena da entrega realizada. Ele representa a validação final da fiscalização, declarando que o objeto (material ou serviço) foi recebido de acordo com as especificações e exigências contratuais. 

64 | 1 3 2

<!-- pagina 65 -->
O acesso ao TRD pode ser realizado através da lista de contratos, ou através da listagem de TRPs, clicando no ícone da coluna “Ações”. 

Quando acessado pela lista Meus Contratos, a tela seguinte apresenta a lista de todos os Termos de Recebimento já elaborados. 

_Figura 92 - Acesso à funcionalidade Elaborar Termo de Recebimento Definitivo pela lista Meus Contratos_ 

_Figura 93 - Lista de todos os TRDs gerados para o Contrato_ 

Quando acessado pela lista de TRPs, a página seguinte apresenta a lista de todos os TRDs já elaborados relacionados à OS/F e ao TRP pelo qual foi encaminhado, ativando os filtros da listagem. 

65 | 1 3 2

<!-- pagina 66 -->
_Figura 94 - Acesso à funcionalidade Elaborar Termo de Recebimento Definitivo pela lista de TRPs_ 

_Figura 95 - Lista de TRDs acessada pela lista de TRPs, com filtro ativo._ 

## _<u>7.3.4.1. Elaborar Termo de Recebimento Definitivo</u>_ 

Com a conclusão do Termo de Recebimento Provisório, o usuário passa a ter acesso ao ícone , onde pode a dar início à elaboração do Termo de Recebimento Definitivo. 

Na página do Termo de Recebimento Definitivo, o usuário encontra duas opções para formalizar o recebimento final, dependendo da origem da documentação: 

- **+ Elaborar Novo TRD:** Esta opção é utilizada para que o próprio sistema gere o documento oficial. Ao selecionar as entregas que já receberam o "Aceite", o sistema compila os dados, itens e valores, criando o TRD digital. Esta funcionalidade é ideal para manter a 

66 | 1 3 2

<!-- pagina 67 -->
padronização documental dentro da plataforma e garantir que todos os cálculos de saldo e execução sejam atualizados automaticamente. 

- + **Informar Termo Definitivo:** Esta opção é utilizada quando o documento de recebimento definitivo já foi emitido fora do sistema (por exemplo, um documento assinado fisicamente ou via SEI). Ao "informar", o fiscal registra no sistema os dados de referência desse documento externo e anexa as informações necessárias para que o histórico do contrato fique completo, permitindo o prosseguimento para a fase de pagamento. 

_Figura 96 - Botões de ação para elaborar o Termo de Recebimento Definitivo_ 

67 | 1 3 2

<!-- pagina 68 -->
_Figura 97 – Elaborar TRD_ 

Ao acessar a página, são apresentados os dados principais do contrato, e campo obrigatório para inserção do texto de introdução do TRD quando se tratar de TRD criado no próprio sistema. 

Em seguida, é apresentada a lista com os TRPs já elaborados, para seleção daquele(s) que integrará(ão) o TRD. 

68 | 1 3 2

<!-- pagina 69 -->
_Figura 98 - Seleção de TRPs do Termo de Recebimento Definitivo_ 

Após selecionar o(s) TRP(s), é preciso clicar no botão “+ Adicionar TRP” para visualizar os itens considerados e selecioná-los. 

O sistema trará preenchidas a quantidade e a glosa indicada no TRP, podendo as informações serem editadas, caso necessário. 

Ao clicar no ícone , localizado ao lado esquerdo do item, o sistema apresenta os campos de quantidade, glosa, com as informações inseridas no TRP, e mais algumas informações facultativas, como mês/ano de referência, número de processo, entre outros, que podem ser inseridas de acordo com a necessidade. É preciso selecionar o item para que os campos sejam habilitados e registrar o TRD. 

Atenção: em contratos com Ordem de Serviço/Fornecimento, só podem ser selecionados TRPs relacionados a uma mesma OS/F. 

69 | 1 3 2

<!-- pagina 70 -->
_Figura 99 - Seleção de TRPs e itens na elaboração do TRD_ 

Assim como acontece no TRP, ao final de cada item é apresentada a barra de evolução dos TRDs, com opção de visualização do quadro resumo dos TRDs já elaborados relacionados àquele item. 

_Figura 100 - Quadro de acompanhamento de execução dos itens do contrato no TRD_ 

Continuando a elaboração do TRD, existe o campo para preenchimento de informações complementares. 

Caso o TRD tenha sido gerado em sistema externo, deve ser obrigatoriamente anexado o respectivo documento e preenchida a data de assinatura. 

Existe, ainda, a pergunta sobre a inclusão da autorização para emissão do instrumento de cobrança no TRD. Trata-se de uma inclusão opcional, onde o gestor do contrato já autoriza a emissão da nota fiscal ou instrumento equivalente no próprio TRD. Caso a opção “Sim” seja selecionada, ao final do documento que será gerado, haverá um parágrafo com a devida autorização. 

70 | 1 3 2

<!-- pagina 71 -->
M A N U A L T É 

C N I C O O P E R A C I O N A L – **C O N T R A T O S . G O V . B R I N O V A V E R S Ã O** 

_Figura 101 - Inclusão da Autorização para Emissão do Instrumento de Cobrança no Termo de Recebimento Definitivo_ 

_Figura 102 – Autorização para emissão de instrumento de cobrança incluído no TRD_ 

Por fim, ficam disponíveis as três opções: 

- Cancelar: cancela a inserção dos dados e volta para a página anterior sem salvar; 

- Salvar Rascunho: salva as informações inseridas, porém na situação Rascunho, ficando pendente de conclusão do TRD para que o fluxo de recebimento do objeto prossiga; e 

- Criar TRD: conclui-se a elaboração do Termo de Recebimento Definitivo, dando prosseguimento na etapa de assinatura do documento gerada no próprio sistema. 

- Informar TRD: Opção para TRPs informados no sistema Contratos.gov.br, ou seja, criados em sistema externo. Nesse botão não é solicitada a assinatura do documento. 

_Figura 103 - Botões de ação de um Termo de Recebimento Definitivo elaborado no sistema_ 

71 | 1 3 2

<!-- pagina 72 -->
_Figura 104 - Botões de ação de um Termo de Recebimento Definitivo informado no sistema (gerado em sistema externo)_ 

Ao clicar em “Criar TRD”, o usuário deverá selecionar os signatários que assinarão o documento. É importante ressaltar que é obrigatória a seleção do servidor cadastrado como “Gestor” ou seu substituto, podendo ser selecionados outros usuários para a assinatura facultativamente. Serão apresentados os usuários cadastrados como responsáveis pelo contrato pelo Setor Contratos no módulo Gestão Contratual na versão original do sistema Contratos.gov.br. 

_Figura 105 - Seleção dos Signatários para assinatura do Termo de Recebimento Definitivo_ 

## _<u>7.3.4.2. Assinar o Termo de Recebimento Definitivo</u>_ 

Após a seleção dos signatários para a assinatura do Termo de Recebimento Definitivo, a entrega aparecerá na listagem de entregas com a situação “Aguardando Assinatura” e, caso 

o usuário logado seja um dos marcados como signatário, ficará disponível o ícone , indicando a existência de um documento pendente de sua assinatura. 

_Figura 106 - Situação Aguardando Assinatura do Termo de Recebimento Definitivo_ 

Ao clicar no ícone , o usuário é levado para a tela de assinatura, onde é apresentado o arquivo PDF do Termo de Recebimento Definitivo. Dessa forma o usuário pode verificar o inteiro teor do documento com as opções: 

- “Voltar”: volta para a tela anterior sem executar qualquer ação, ou seja, o Termo de Recebimento Definitivo continua na situação “Aguardando Assinatura do TRD”; 

- “Ajustar”: volta a entrega para situação de elaboração do TRD, retirando a solicitação de assinatura, para que sejam realizadas as correções no teor do documento e, posteriormente, volte a ser colocado para assinatura; 

- “Assinar”: realizará a assinatura do documento, utilizando a ferramenta de assinatura eletrônica da plataforma Gov.br, diretamente dentro do sistema. 

72 | 1 3 2

<!-- pagina 73 -->
É C N I C O O P E R A C I O N A L – **C O N T R A T O S . G O V . B R I N O V A V E R S Ã O** 

M A N U A 

_Figura 107 - Assinar Termo de Recebimento Definitivo_ 

Após a assinatura, a situação do TRD ficará como “Concluído” ~~d~~ para os casos em que o Termo de Recebimento Definitivo foi elaborado sem a autorização para emissão do instrumento de cobrança. Caso o TRD tenha sido elaborado com a autorização para emissão do instrumento de cobrança, a situação da entrega ficará como “Aguard. Inst. Cobrança”. 

_Figura 108 - Situação após assinatura do Termo de Recebimento Definitivo_ 

73 | 1 3 2

<!-- pagina 74 -->
M A N U A L T É C N I C O O P E R A C I O N A L – **C O** 

**N T R A T O S . G O V . B R I N O V A V E R S Ã O** 

# 7.4. Visualizar Preposto do Contrato 

Ao visualizar a listagem dos Contratos, na coluna “Ações” o usuário poderá verificar os prepostos do fornecedor cadastrados naquele contrato através do ícone . 

_Figura 109 - Visualizar Preposto do Contrato_ 

Ao clicar sobre o ícone o sistema abrirá a página em que trás a relação de prepostos que já foram cadastrados naquele contrato, assim como a possibilidade de edição dos dados. 

_Figura 110 - Visualizar Preposto do Contrato_ 

É importante ressaltar que um preposto cadastrado não poderá ser excluído. Se houver a necessidade de alteração de um preposto do contrato, o usuário deve inativar o preposto que aparece na listagem através do botão “Editar” e em seguida adicionar um novo preposto no contrato. 

74 | 1 3 2

<!-- pagina 75 -->
## 7.4.1. Adicionar Preposto do Contrato 

Na tela em que é apresentada a relação de prepostos cadastrados naquele contrato existe o botão “Adicionar Preposto”. Através dele o usuário poderá informar os dados do preposto e ao salvar ele estará cadastrado passando a ter acesso as funcionalidades disponíveis para os prepostos de contrato pelo perfil fornecedor. 

_Figura 111 - Adicionar Preposto do Contrato_ 

8. Instrumento de cobrança 

O cadastro do Instrumento de cobrança (IC) ocorre por dois caminhos: 1) acessando a versão original do sistema (https://contratos.comprasnet.gov.br/) ou 2) pela nova versão do sistema (https://contratos.sistema.gov.br/). 

- 1) Versão original – acesse pelo **Gestão Contratual > Contratos ou Meus Contratos > Ações (mais) > Instrumentos de cobrança** 

- 2) Será direcionado para a tela de listagem dos ICs do contrato **> Clicar em Cadastrar instrumento de cobrança** 

_Figura 112 – Acesso pela versão original ao cadastro do instrumento de cobrança_ 

75 | 1 3 2

<!-- pagina 76 -->
_Figura 113 – Listagem inicial dos Instrumentos de cobrança do contrato_ 

- 3) Nova versão – acesse pelo **Fiscalização e Gestão de Contratos > Meus Contratos > Pesquise o contrato > Ações > Instrumento de cobrança > Clicar em Cadastrar instrumento de cobrança** (Figura 99). 

_Figura 114 – Tela listagem inicial contratos_ 

Após clicar em “Cadastrar instrumento de cobrança”, abrirá a tela de preenchimento do IC. Essa tela é composta por cinco abas. A primeira aba é “Dados do Instrumento de cobrança” 

**1. Aba** - Dados do Instrumento de Cobrança 

- **Dados do Contrato:** cabeçalho com as informações do contrato, pode ser ocultado os dados pela seta na lateral direita. 

- **Fornecedor Subcontratado** : caso o IC seja de um fornecedor subcontratado e que esteja indicado como subcontratado no contrato. 

- **Consulta SICAF:** consulta das certidões do fornecedor por integração automatizada com o SICAF. 

- **Unidade** : unidade na qual o contrato está cadastrado (pré-preenchido), podendo selecionar uma unidade descentralizada do contrato. 

- **Número do Processo Sei:** número do processo indicado no contrato (prépreenchido). 

- **Tipo Lista:** selecionar a que se refere o instrumento de cobrança (prestação de serviços, fornecimento de bens etc.). 

- **Tipo de Instrumento de Cobrança:** selecionar qual o tipo do IC (NFe, Nota fiscal, fatura, recibo etc.). 

- **Data de emissão:** informar a data de emissão do IC. 

- **Número:** informar o número do IC. 

- **Série:** informar o número da série, se houver. 

- **Chave NFe:** informar a chave em caso da seleção de NFe em tipo do IC, observando que a chave pode conter de 44 a 50 dígitos. 

76 | 1 3 2

<!-- pagina 77 -->
- **Arquivo de Instrumento de Cobrança:** inserir o documento de IC. 

**Dica:** Após seleção e preenchimento dos campos da aba, clique na seta na parte inferior da tela ou clique na próxima aba na parte superior. 

_Figura 115 – Aba - Dados do instrumento de cobrança_ 

**2. Aba** – Itens Instrumento de cobrança 

- **Dados do contrato:** a partir da segunda aba, os dados ficam ocultados, podendo ser expandidos clicando na seta. 

- **Glosa:** colocar o valor, se houver, podendo ser descontado do valor total ou não. Se descontar do valor total, marcar a opção “sim” após preenchimento. 

- **Juros/Multa:** colocar o valor, se houver. O valor informado aumenta o valor líquido do IC. 

- **Histórico do Contrato:** escolher o contrato ou seus termos, podendo escolher mais de um. 

- **Itens do histórico:** escolher um ou todos os itens do contrato ou termo selecionado 

- **Valor unitário e quantidade:** valores pré-prenchidos podendo ser editados. 

- **País de fabricação:** escolher o país de fabricação quando se tratar de fornecimento de bens. 

- **Atenção:** os valores de Glosa (marcando sim), Juros e Multa alteram o valor líquido que enviado para apropriação. Por ex.: Se o valor total dos itens faturados corresponde a R$ 100,00 e tem um valor a glosar de R$ 10,00, o valor líquido será de R$ 90,00. Esse valor será o valor do documento a apropriar no Gestão financeira. Caso não queira que esse valor diminuía o valor faturado, marcar a opção “não”. 

77 | 1 3 2

<!-- pagina 78 -->
_Figura 116 – Glosa em itens faturados_ 

**Outras funcionalidades** : além do preenchimento dos campos, a tela permite expandir a visualização ao clicar no ícone . Também é possível excluir um ou mais itens, ou ainda todos de uma vez, utilizando o ícone de lixeira; para exclusões em lote, o usuário pode selecionar todos os itens e desmarcar aqueles que não deseja excluir antes de confirmar a ação. Adicionalmente, há a funcionalidade de replicar itens, disponível por meio do 

ícone , que permite duplicar rapidamente as informações já inseridas. 

_Figura 117 – Aba – Itens Instrumento de cobrança_ 

**3. Aba** – Outras Informações 

- **Repactuação:** marcar sim ou não, meramente informativo. 

78 | 1 3 2

<!-- pagina 79 -->
- **Referência:** selecionar mês e ano de referência e o valor correspondente. Podendo adicionar vários meses. Observando que o Siafi aceita até 6 meses retroativo para lançamento de referência no centro de custos. 

- **Empenhos:** selecionar o empenho vinculado ao contrato. <u>O saldo é atualizado na seleção do empenho em tempo real com Siafi (conta Empenhos a liquidar).</u> Observando que o caso o Siafi esteja fora do horário de funcionamento, o valor apresentado será o valor da última atualização. 

- **Informações complementares:** preencher, se houver. 

- **Arquivo complementar:** inserir, se houver. 

_Figura 118 – Aba – Outras informações_ 

**4. Aba** – Tributações 

A aba “Tributações” não é de preenchimento obrigatório, para se tornar, é necessário alterar as configurações do órgão e escolher a opção “Aba Tributações” “Sim” (configuração realizada pelo administrador de órgão). <u>As informações dessa aba são meramente informativas.</u> 

- **Optante pelo simples:** marcar sim ou não. 

- **Adicionar Tributação:** se clicar no ícone, abre campos para preenchimento. 

- **Base cálculo INSS:** inserir o valor da base de cálculo. 

- **Optante CPRB:** escolher sim ou não. 

- **Alíquota INSS:** mostrada automaticamente a partir do sim ou não do campo anterior. 

79 | 1 3 2

<!-- pagina 80 -->
- **Valor INSS:** o valor é calculado – base x alíquota (não podendo ser editado). 

_Figura 119 – Aba – Tributações_ 

**5. Aba** – Liquidação da Despesa 

- **Data de recebimento:** informar a data de protocolo de recebimento do IC. 

- **Data de liquidação de despesa:** informar a data de ateste do documento. 

- **Data limite de pagamento:** a data é informada a partir da data de ateste com base na IN 77/2022. 

- **Atestado por:** pode ser inserido a informação de quem atestou desde que cadastrado como responsável por contrato. 

_Figura 120 – Aba – Liquidação da despesa_ 

**Atenção:** No caso de alteração da data limite de pagamento para uma data posterior, será necessário justificar. Escolher entre as opções de justificativa ou informar a justificativa no caso de selecionar a opção “Outra”. 

80 | 1 3 2

<!-- pagina 81 -->
_Figura 121 – Justificativa da alteração da data limite de pagamento_ 

Após o registro de todas as informações obrigatórias, realizar o cadastro do Instrumento de cobrança clicando em “Criar Instrumento de Cobrança”. 

**Atenção:** Ao anexar um documento durante o cadastro do Instrumento de Cobrança (IC), caso haja pendências de preenchimento nos campos obrigatórios, o arquivo anexado não será salvo. Nessas situações, será necessário realizar o anexo novamente após a regularização das pendências. Os arquivos anexados somente serão efetivamente salvos após a conclusão do cadastro do IC. Exemplo: Caso todos os campos tenham sido preenchidos, exceto o campo “País de fabricação”, o sistema apresentará mensagem de erro no momento do cadastro. Como consequência, o arquivo previamente anexado será excluído, sendo necessário anexálo novamente após o preenchimento do campo pendente. 

Os Instrumentos de Cobrança são apresentados em ordem cronológica após o cadastro. A listagem poderá ser alterada por meio da aplicação dos filtros predefinidos ou pela inclusão de novos filtros, disponíveis na opção de visibilidade de colunas. Adicionalmente, é possível realizar a exportação das informações exibidas. Ressalta-se que a exportação considera apenas os registros apresentados na tela. Para exportar a totalidade dos registros, o usuário deverá selecionar a opção **“Todos”** , localizada no canto inferior esquerdo da tela. 

81 | 1 3 2

<!-- pagina 82 -->
_Figura 122 – listagem dos instrumentos de cobrança após cadastro_ 

Pela listagem do ICs é possível visualizar o documento na coluna “Ações” clicando no ícone . Além da consulta às informações preenchidas, o usuário poderá acompanhar o histórico do documento, incluindo registros de criação e edições realizadas. Adicionalmente, é possível realizar a impressão dessa visualização, por meio do ícone de impressora localizado no canto superior direito da tela. 

8.1.1. Cadastro do Instrumento de cobrança pelo fornecedor 

Para os Instrumentos de Cobrança (IC) cadastrados pelo fornecedor, o órgão deverá realizar a análise do documento, podendo optar pelo preenchimento das informações pendentes ou pela recusa do IC. Ao complementar as informações faltantes, o documento será aceito, permitindo o prosseguimento do fluxo processual. Em caso de recusa, o IC será devolvido ao fornecedor, que poderá corrigir as informações para novo envio ou, alternativamente, cancelar o documento e cadastrar um novo Instrumento de Cobrança. 

O Instrumento de Cobrança (IC) cadastrado pelo fornecedor, após seu recebimento pelo órgão, permanecerá na situação **“Aguardando fiscal”** , sendo sinalizado por meio de alerta no ícone da carteira. O IC recusado será classificado na situação **“Recusado pelo fiscal”** , não sendo permitida sua edição, devendo-se aguardar a correção pelo fornecedor ou novo documento. Caso o fornecedor realize o cancelamento do documento, o IC passará a constar na situação **“Cancelado pelo fornecedor”** , sendo gerado um novo documento. 

_Figura 123 – Recebimento de IC cadastrado pelo fornecedor_ 

82 | 1 3 2

<!-- pagina 83 -->
_Figura 124 – Recusa do IC cadastrado pelo fornecedor_ 

9. Gestão de Atas 

Menu habilitado para o perfil Gestor de Atas, voltado para acesso às funcionalidades relacionadas à gestão de atas de registro de preços regidas pela Lei nº 14.133/2021 e derivadas. 

- 9.1. Listar Atas de Registro de Preços 

Acessando o menu Gestão de Atas > Ata de Registro de Preços, são exibidas as atas de registro de preços da unidade. 

83 | 1 3 2

<!-- pagina 84 -->
_Figura 125 - Lista de atas de registro de preços_ 

Ao clicar no ícone visualizar , são apresentadas as informações da ata. 

_Figura 126 – Detalhes da ata de registro de preços_ 

84 | 1 3 2

<!-- pagina 85 -->
## 9.2. Cadastro de Ata de Registro de Preços 

Para efetuar o cadastro de uma nova ata de registro de preços, acesse Gestão de Atas > Ata de Registro de Preços e clique em + Criar Ata, 

_Figura 127 – Criar ata de registro de preços_ 

## Preencha os campos apresentados, 

_Figura 128 - Criar ata de registro de preços_ 

- Número da ata*: Informe o número da ata, que deve conter cinco dígitos. Não são aceitos números já utilizados para registro de outra ata de registro de preços do mesmo ano. Informando menos que cinco dígitos, o sistema incluirá 0 à esquerda para completar os cinco dígitos necessários. O número da ata não pode ser composto apenas por zeros. 

- Ano da ata*: Informe o ano com quatro dígitos; 

Os campos marcados com * são de preenchimento obrigatório. 

85 | 1 3 2

<!-- pagina 86 -->
Preenchidos os dados, clique no ícone Validar : 

_Figura 129 - Criar ata de registro de preços_ 

Preencha os campos apresentados: 

- Objeto*: informe o objeto da ata de registro de preços; 

- Data de assinatura*: selecione a data no calendário exibido; 

- Data inicial de vigência*: selecione a data no calendário exibido. A data inicial de vigência deve ser uma data posterior à data de assinatura; 

- Data final de vigência*: selecione a data no calendário exibido; 

- Número do processo*: informe o número do processo relacionado à ata; 

- Autoridade signatária: busque os registros de usuários cadastrados como autoridade signatária da unidade para seleção; 

- Compra centralizada?: por padrão é marcada a opção “Não”. Se necessário, altere a resposta de acordo com a característica da compra; Observação: conforme art. 2º, item VII do decreto 11.462/2023, compra centralizada se refere à compra ou contratação de bens, serviços ou obras, em que o órgão ou a entidade gerenciadora conduz os procedimentos para registro de preços destinado à execução descentralizada, mediante prévia indicação da demanda pelos órgãos ou pelas entidades participantes. 

- Unidade gerenciadora: apresenta a unidade gerenciadora da ata, conforme _login_ do usuário, não permitindo alteração; 

- Unidade origem de compra*: apresenta a unidade conforme _login_ do usuário, permitindo alteração, necessária somente quando se tratar de compra subrogada. Será apresentada mensagem de alerta informando os dados utilizados para pesquisar a compra; 

- Número da compra/ ano*: informe o número e ano da compra no formato XXXXX/XXXX; 

- Modalidade da compra*: selecione na lista apresentada a modalidade da compra. 

86 | 1 3 2

<!-- pagina 87 -->
Os campos marcados com * são de preenchimento obrigatório. 

Preenchidos os dados, clique no ícone Buscar Compra para que sejam carregadas as informações sobre a compra. 

_Figura 130 - Criar ata de registro de preços - Buscar compra_ 

Aguarde enquanto os dados da compra são carregados sem fechar a página. Considerando que as compras possuem muitos fornecedores, unidades participantes e/ou itens, os itens são carregados e as quantidades por unidade são processadas enquanto se prossegue com a inclusão de informações na ata. 

Portanto, mesmo que a compra não tenha sido integralmente carregada ainda, é possível ir preenchendo algumas informações com os dados já buscados. Em se tratando de uma compra com muitos itens, participantes ou fornecedores, sugere-se aguardar o carregamento total da compra para evitar qualquer erro no cadastramento da ata, uma vez que a retificação não permite a inclusão de novos itens na mesma ata e não é permitida a repetição de número de uma ata. 

87 | 1 3 2

<!-- pagina 88 -->
_Figura 131 – Criar ata de registro de preços - Listar fornecedores da compra_ 

Acompanhe o processamento clicando no ícone do campo Quantidade registrada de cada item. A inclusão dos itens na ata pode continuar sem impedimentos. 

_Figura 132 - Detalhamento das unidades por item (durante o processamento das informações)_ 

Ao clicar no ícone do campo Quantidade registrada serão exibidas as informações das quantidades homologadas de cada UASG pertencente à ata ou das quantidades aceitas de adesão para o caso de unidades não participantes (caronas). 

Clique no ícone para exibir os itens do fornecedor: 

88 | 1 3 2

<!-- pagina 89 -->
_Figura 133 - Criar ata de registro de preços - Listar itens do fornecedor_ 

Na relação de itens, são apresentadas informações sobre número, tipo, código, descrição, classificação do fornecedor, quantidade registrada, valor unitário e valor total do item. 

Ao passar o mouse e/ou clicar no ícone , são exibidas informações como a descrição, a classificação dos fornecedores para o item, as unidades participantes e detalhes sobre o percentual de maior desconto (quando aplicável ao item). 

_Figura 134 - Detalhes da classificação dos fornecedores por item_ 

89 | 1 3 2

<!-- pagina 90 -->
_Figura 135 - Detalhamento das unidades por item (após o processamento das informações)_ 

Selecione os itens que farão parte da ata. Ao clicar em todos, é possível selecionar todos os itens da página atual. 

Podem ser incluídos quantos itens forem necessários, de diferentes fornecedores. Clique em Incluir item para que o item seja incluído na ata. 

_Figura 136 - Incluir item na criação da ata de registro de preços_ 

No campo Valor Total dos itens selecionados, será apresentado o valor total de todos os itens selecionados para compor a ata. 

90 | 1 3 2

<!-- pagina 91 -->
_Figura 137 - Campo valor total dos itens selecionados_ 

Finalizada a inclusão dos itens, inclua o arquivo da ata clicando em Selecione o arquivo, sendo possível o _upload_ do arquivo desejado. O envio é obrigatório para tornar a ata “Ativa”. Para ata “Em elaboração” (rascunho), o envio é facultativo. O arquivo incluído é salvo na listagem Arquivos da ata e enviado ao PNCP. 

_Figura 138 - Incluir arquivo da ata_ 

Finalizadas as inclusões, ao clicar em Criar ata. O cadastro da ata é realizado e o usuário é direcionado para a tela de listagem que apresenta a situação de cada ata. 

91 | 1 3 2

<!-- pagina 92 -->
_Figura 139 - Criar ata de registro de preços_ 

**Importante:** se o carregamento da compra estiver em andamento, a ata recebe o _status_ “Carregando compra” e é publicada automaticamente no Portal Nacional de Contratações Públicas (PNCP) após o término do processamento feito pelo sistema, quando passa a receber o _status_ “Ativa”. 

Caso ocorra algum erro no envio da publicação para o PNCP, a ata recebe o _status_ de “Erro publicar”. O sistema realizará o reenvio automático para publicação, portanto, nenhuma ação do usuário é necessária. Assim que regularizada a situação da ata, seu _status_ é alterado para “Ativa”. 

Ao clicar em “Salvar Rascunho”, ficará com a situação “Em elaboração”, permitindo sua edição 

(ação ”Editar“ ). É possível editar os campos Número da Ata, Ano da Ata, Objeto, Data de assinatura, Data inicial de vigência, Data final de vigência, Número do Processo, Autoridade signatária e Compra centralizada? 

No momento que o usuário estiver criando a ata é possível incluir ou excluir itens, desde que sejam pertencentes à mesma compra. 

É possível visualizar, incluir e excluir arquivos. É obrigatório e único o arquivo do tipo Ata de Registro de Preços e em caso de ter sido enviado um documento errado, deve ser incluído outro arquivo do mesmo tipo havendo a sua substituição no sistema e no PNCP. 

Uma ata com a situação de “Em elaboração” também pode ser excluída, ao se clicar em Excluir 

9.3. Arquivos de Ata de Registro de Preços 

92 | 1 3 2

<!-- pagina 93 -->
Para adicionar arquivos da Ata de Registro de Preços, acesse o menu Gestão de Atas > Ata de Registro de Preços, localize a ata, em ações selecione Lista de Arquivos. 

_Figura 140 - Acessar arquivos da ata de registro de preços_ 

A tela apresenta todos os arquivos já incluídos. 

Clique no ícone + Adicionar Arquivo. 

_Figura 141 - Lista de arquivos de ata de registro de preços / Adicionar arquivo_ 

São apresentadas as informações sobre a ata relacionada: número/ano da ata, número da compra/ano, modalidade da compra, data da assinatura, data inicial da vigência, data final da vigência, valor total. 

Preencha os campos apresentados: 

93 | 1 3 2

<!-- pagina 94 -->
_Figura 142 - Adicionar arquivo_ 

- Descrição*: informe o nome do arquivo; 

- Tipo*: selecione entre as opções apresentadas o tipo do arquivo – ata de registro de preços; termo aditivo; termo de apostilamento, termo de extinção, alteração ou outros; 

- Restrito: marque o campo caso o arquivo seja restrito, considerando conteúdo de informações sensíveis para a Lei Geral de Proteção de Dados Pessoais (LGPD). Se o campo for assinalado, o arquivo não será exibido no PNCP. O julgamento sobre se o arquivo deve ser restrito ou não cabe ao usuário. Um arquivo do tipo ata de registro de preços obrigatoriamente deve ser incluído, não podendo ser restrito; 

- Envio de arquivo da ata*: clique em Selecione o Arquivo e busque o arquivo a ser inserido. 

Os campos marcados com * são de preenchimento obrigatório. 

Preenchidos todos os campos, clique em Criar Arquivo. O arquivo inserido passa a ser apresentado na lista de arquivos com as ações: Alterar o Status do Arquivo para Público ou Alterar o status do Arquivo para privado; Baixar Arquivo e Excluir. Caso o arquivo seja marcado como público, ele será enviado para o PNCP, sendo enviado como ata, pois é o tipo de documento aceito pelo PNCP. Para mais esclarecimentos sobre os tipos de arquivos aceitos pelo PNCP, consultar o manual atualizado em <u>Manuais</u> - Portal Nacional de Contratações <u>Públicas - PNCP.</u> 

94 | 1 3 2

<!-- pagina 95 -->
M A N U A L T É C N I C 

O O P E R A C I O N A L – **C O N T R A T O S . G O V . B R I N O V A V E R S Ã O** 

_Figura 143 - Arquivo incluído_ 

**Importante:** Uma Ata de Registro de Preços obrigatoriamente terá um único arquivo do tipo “ata de registro de preços”. Assim, o arquivo do tipo Ata de Registro de Preços não pode ser excluído, sendo possível apenas sua substituição ao se adicionar um novo arquivo do mesmo tipo, sendo obrigatoriamente público. 

## 9.4. Envio de Ata de Registro de Preços para o PNCP 

O envio de uma ata de registro de preços é feito automaticamente para o Portal Nacional de Contratações Públicas (PNCP), após finalizado o carregamento da compra, desde que um arquivo do tipo Ata de Registro de Preços tenha sido inserido, bem como que a data de assinatura seja anterior à data de vigência início e esta seja igual ou anterior à data de vigência fim. 

Uma ata publicada no PNCP ficará com o _status_ “Ativa”. 

Caso ocorra algum erro no envio da publicação para o PNCP, a ata recebe o _status_ de “Erro publicar”. O sistema realizará o reenvio automático para publicação, portanto, nenhuma ação do usuário é necessária. Assim que regularizada a situação da ata, ela constará como “Ativa”. Caso o status de erro se mantenha por alguns dias sem correção automática, deve ser aberto chamado no portal de serviços para análise do erro. 

Ao clicar na ação PNCP, o usuário é direcionado para a publicação. 

95 | 1 3 2

<!-- pagina 96 -->
_Figura 144 - Consultar Ata de Registro de Preços no PNCP_ 

9.5. Retificação de Ata de Registro de Preços 

A retificação serve para correção de um dado inserido incorretamente e que está em dissonância com o documento externo que formalizou a ata de registro de preços. Para mudanças que não impliquem em erro de registro, deve ser utilizada a opção de alteração de ata. 

Para retificar informações inseridas em uma ata de registro de preços "Ativa”, acesse a lista de Atas de Registro de Preços disponível no menu Gestão de Atas > Ata de Registro de Preços. 

Localize a ata a ser retificada, clique na ação Retificar . Serão exibidas as informações da ata e a lista das retificações já realizadas caso existam. Clique em + Adicionar retificação. 

96 | 1 3 2

<!-- pagina 97 -->
_Figura 145- Adicionar retificação_ 

São exibidas as informações da ata. Não se deve preencher todos os campos novamente, mas tão somente aquele(s) que se deseja retificar. 

É possível retificar as informações dos campos Objeto, número e ano da ata, Data da assinatura, Vigência inicial, Vigência final, Compra centralizada? e Autoridade signatária. 

É obrigatório preencher o campo Justificativa/Motivo da retificação. 

Finalizada a inclusão das informações, clique em Retificar. 

_Figura 146 - Incluir retificação a ata_ 

97 | 1 3 2

<!-- pagina 98 -->
As informações retificadas são divulgadas automaticamente no PNCP. 

Obs: o número/ano da ata não poderá ser retificado para o mesmo número de uma ata já existente ou com o status cancelada. 

9.6. Alteração de Ata de Registro de Preços 

Enquanto a retificação serve para corrigir uma informação incorreta que diverge com o documento externo da ata de registro de preço, a alteração implica numa mudança no decorrer de sua vigência, não representando erro de registro. 

Para alterar uma ata de registro de preços com situação “Ativa”, acesse a lista de Atas de Registro de Preços disponível no menu Gestão de Atas > Ata de Registro de Preços. 

Localize a ata a ser alterada, clique na ação Alterar . Será exibida a listagem das alterações já realizadas, caso existam. Clique em + Adicionar alteração: 

_Figura 147 - Adicionar alteração de ata_ 

São apresentadas as informações da ata que será alterada e os campos para preenchimento: 

98 | 1 3 2

<!-- pagina 99 -->
_Figura 148- Adicionar alteração de ata_ 

Selecione o tipo de alteração: 

- Fornecedor: para alteração do fornecedor do item. Esse campo não poderá ser alterado se houver minuta, empenho, contrato, remanejamento ou solicitação de adesão para a ata selecionada; 

- Vigência: para alteração/prorrogação de vigência da ata; 

- Valor(es) registrado(s): Para alteração dos valores registrados; 

- Cancelamento de item(ns): Para cancelamento de item registrado; 

- Informativo: Para registro de alterações do tipo informativo. 

**Observação:** Mais de um tipo de alteração pode ser selecionado. 

A alteração de vigência só pode ser realizada uma vez por ata. 

As alterações de valor registrado e de cancelamento de item não podem ser realizadas para o mesmo item na mesma alteração. 

99 | 1 3 2

<!-- pagina 100 -->
Para **alteração do tipo Vigência para Órgãos Não-SISG** , preencha os campos apresentados: 

_Figura 149 - Alteração de ata do tipo Vigência para órgãos Não-SISG_ 

- Data de assinatura de alteração*: Informe uma data posterior à data de vigência inicial da ata e antes do período de vigência final da ata; 

- Anexo da alteração*: faça _upload_ do arquivo relacionado à alteração; 

- Descrição do anexo*: Informe o nome do arquivo inserido; 

- Data fim da vigência*: apresenta nova data fim da vigência. O sistema já apresenta a nova data fim da vigência contando um ano após a data de vigência final atual. Embora o sistema apresente o campo da nova “data fim da vigência” já preenchido, o usuário poderá alterá-lo, caso seja necessário. 

100 | 1 3 2

<!-- pagina 101 -->
- Quantitativo renovado na prorrogação da vigência? 

   - Caso a resposta seja “Sim”: o sistema disponibilizará o campo obrigatório “amparo legal da renovação de saldo” para que a unidade informe o normativo que embasa a renovação do saldo juntamente com a alteração (prorrogação) da vigência. 

   - Caso a resposta seja “Não”: apenas o prazo será estendido, restando como disponível o saldo não utilizado no primeiro período de vigência. 

Para **alteração do tipo Vigência para Órgãos SISG** , preencha os campos apresentados: 

_Figura 150 - Alteração de ata do tipo Vigência para órgãos Não-SISG_ 

- Data de assinatura de alteração*: Informe uma data posterior à data de vigência inicial da ata e antes do período de vigência final da ata; 

- Anexo da alteração*: faça _upload_ do arquivo relacionado à alteração; 

- Descrição do anexo*: Informe o nome do arquivo inserido; 

- Justificativa/motivo de alteração de vigência*: Informe a justificativa/motivo de alteração de vigência e se todas as exigências legais foram atendidas; 

- Data fim da vigência*: apresenta nova data fim da vigência. O sistema já apresenta a nova data fim da vigência contando um ano após a data de vigência final atual. Embora o sistema apresente o campo da nova “data fim da vigência” já preenchido, o usuário poderá alterá-lo, caso seja necessário. 

- Haverá renovação do quantitativo registrado para o segundo ano da ata?*: Com base no Parecer nº 75/2024/DECOR/CGU/AGU, é possível renovar o quantitativo da ata durante a prorrogação, desde que: (a) haja previsão no edital e no ETP, (b) o preço seja vantajoso, (c) o termo aditivo seja firmado dentro da vigência original. Fundamento: arts. 5º, 40, caput, e 84 da Lei nº 14.133/2021 e art. 22 do Decreto nº 11.462/2023. 

   - **Se o usuário marcar “Não”** : a vigência da ata será prorrogada por um novo período, porém, o quantitativo NÃO será renovado; 

101 | 1 3 2

<!-- pagina 102 -->
- **Se o usuário marcar “Sim”** : a vigência da ata será por um novo período e o quantitativo da ata também será renovado para o novo período e será apresentado um alerta para o usuário com a seguinte mensagem: 

- Se o usuário marcar “Sim” para a pergunta “Haverá renovação do quantitativo registrado para o segundo ano da ata?” também deverá assinalar se atendeu a cada uma das seguintes exigências constantes no Parecer nº 75/2024/DECOR/CGU/AGU: 

_Figura 151 – Perguntas para prorrogação de vigência com renovação de quantitativo da ata para órgãos SISG_ 

   - Foi comprovada a manutenção do preço vantajoso para a administração? 

   - Há previsão expressa da possibilidade de renovação dos quantitativos no ato convocatório (edital) e na ata de registro de preços? 

   - O tema da renovação dos quantitativos foi tratado expressamente na fase de planejamento da contratação? 

   - A prorrogação da ata será formalizada por termo aditivo dentro do prazo de sua vigência original? 

- O usuário também deverá fazer o _upload_ e anexar o arquivo contendo a justificativa da renovação de quantitativos. 

Clique em Criar Alteração. A alteração é registrada com sucesso e o usuário é direcionado para a lista de alterações. 

A alteração é registrada e publicada no PNCP. O arquivo inserido é salvo na lista Arquivos da ata. 

**Atenção** : A alteração do tipo “vigência” só pode ser realizada uma única vez. 

102 | 1 3 2

<!-- pagina 103 -->
## Para **alteração do tipo “Valor(es) registrado(s)** , preencha os campos apresentados: 

_Figura 152 - Alteração de ata do tipo Valor Registrado_ 

- Data de assinatura de alteração*: Informe uma data posterior à data de vigência inicial da ata; 

- Anexo da alteração*: faça _upload_ do arquivo relacionado à alteração; 

- Descrição do anexo*: informe o nome do arquivo inserido; 

- Novo desconto % OU Novo valor unitário: Caso o critério de julgamento da licitação tenha sido menor valor, apenas o campo “novo valor unitário” poderá ser alterado e caso o critério de julgamento da licitação tenha sido maior percentual de desconto, apenas o campo “novo desconto %” poderá ser alterado. 

Os itens que compõem a ata são exibidos para alteração de valor. No campo Novo Valor Unitário, informe o novo valor. 

O sistema exibe mensagem de alerta com as informações sobre minutas de empenho em andamento e emitidas e sobre contratos que possuem o item, para conhecimento do usuário. 

Clique em Criar Alteração. A alteração é registrada com sucesso e o usuário é direcionado para a lista de alterações. 

A alteração é registrada e publicada no PNCP. O arquivo inserido é salvo na lista Arquivos da ata. 

Para **alteração do tipo Cancelamento De Item(ns)** , preencha os campos apresentados: 

103 | 1 3 2

<!-- pagina 104 -->
_Figura 153 - Alteração de ata do tipo Cancelamento de item_ 

- Data de assinatura de alteração*: Informe uma data posterior à data de vigência inicial da ata; 

- Anexo da alteração*: faça _upload_ do arquivo relacionado à alteração; 

- Descrição do anexo*: informe o nome do arquivo inserido. 

Os itens que compõem a ata são exibidos para cancelamento. Marque o campo Cancelar item? para o item que deseja cancelar. 

O sistema exibe mensagem de alerta com as informações sobre minutas de empenho em andamento, emitidas e contratos que possuem o item, para conhecimento do usuário. 

Clique em Criar Alteração. A alteração é registrada com sucesso e o usuário é direcionado para a lista de alterações. 

A alteração é registrada e publicada no PNCP. O arquivo inserido é salvo na lista Arquivos da ata. 

Para **alteração do tipo Informativo** , preencha os campos apresentados: 

104 | 1 3 2

<!-- pagina 105 -->
_Figura 154 - Alteração de ata do tipo Informativo_ 

- Data de assinatura de alteração*: Informe uma data posterior à data de vigência inicial da ata; 

- Anexo da alteração*: faça _upload_ do arquivo relacionado à alteração; 

- Descrição do anexo*: Informe o nome do arquivo inserido; 

- Objeto da alteração*: informe o objeto da alteração. 

Clique em Criar Alteração. A alteração é registrada com sucesso e o usuário é direcionado para a lista de alterações. 

A alteração é registrada e publicada no PNCP. O arquivo inserido é salvo na lista Arquivos da ata. 

Os campos marcados com * são de preenchimento obrigatório. 

Para todas as opções de alteração é possível Salvar Rascunho, ficando a alteração em edição, para prosseguir com o preenchimento da solicitação posteriormente. 

105 | 1 3 2

<!-- pagina 106 -->
- 9.7. Remanejamento das quantidades registradas na ata de Registro de Preços 

   - 9.7.1. Solicitação de remanejamento 

Para solicitar remanejamento das quantidades registradas na ata de registro de preços, acesse o menu Gestão de Atas > + Solicitar remanejamento. 

Clique em +Adicionar solicitação de remanejamento. 

_Figura 155 – Adicionar solicitação de remanejamento_ 

Na aba Item(ns) para remanejamento, preencha o campo “unidade da compra” E **pelo menos um** dos seguintes campos para que o sistema realize a busca: 

- Número/ Ano da compra: busque pelo número da compra/ano. Somente serão apresentadas compras com atas vigentes; 

- Modalidade da compra: informe pelo menos os dois primeiros caracteres da modalidade, conforme o número da compra. Somente serão apresentadas as modalidades relacionadas ao número da compra informado; 

- Número da ata (Unidade gerenciadora): informe o número da ata da unidade gerenciadora. Realize a busca pelo número da ata/ano. Somente serão apresentadas atas vigentes; 

106 | 1 3 2

<!-- pagina 107 -->
_Figura 156 – Solicitação de remanejamento_ 

Após clicar no botão pesquisar , será exibida a relação de itens que possuem saldo para remanejamento da unidade gerenciadora e das participantes, conforme dados informados. Na relação de itens, serão exibidas as seguintes informações: 

- Número da ata; 

- Unidade de origem; 

- Tipo de unidade: gerenciadora ou participante; 

- Número do item; 

- Descrição do item; 

- Saldo para remanejamento. Deve ser observado pela unidade solicitante do remanejamento se está sendo respeitado o limite estabelecido no Decreto 11.462/2023 e Lei 14.133/2021. 

_Figura 157  – Item(ns) para remanejamento_ 

107 | 1 3 2

<!-- pagina 108 -->
Na **aba “Item(ns) para remanejamento”** o usuário deverá informar a quantidade solicitada para remanejamento no campo Quantidade Solicitada. 

Caso não queira prosseguir com a solicitação, o usuário clicará no botão Cancelar e poderá também Salvar Rascunho para prosseguir com o preenchimento da solicitação posteriormente. 

_Figura 158  – Solicitar remanejamento_ 

Para prosseguir no fluxo, o usuário poderá clicar no botão clicar diretamente na aba Dados e Arquivo(s). 

, localizado no rodapé, ou 

**Na aba Dados e Arquivo(s** ), o usuário responderá às seguintes perguntas, clicando em “Sim” ou “Não”: 

- Se “O remanejamento está sendo feito entre unidades de estado, Distrito Federal ou município distintos”: 

   - Caso a resposta seja “Sim”: o usuário informará se o fornecedor beneficiário da ata de registro de preços está de acordo com o fornecimento no novo ente federativo, para cumprimento do art. 30, §5º, do Decreto 11.462/2023. Neste caso, será obrigatório o envio de arquivo no campo Envio de Arquivo do Remanejamento da Ata XXXXX/AAAA. 

   - Caso a resposta seja “Não”: o usuário poderá prosseguir diretamente com a solicitação, podendo incluir, de forma opcional, o Envio de Arquivo do Remanejamento da Ata XXXXX/AAAA para _upload_ do arquivo que será anexado à solicitação. 

_Figura 159  – Dados e Arquivo(s) no Remanejamento_ 

Após finalizar essa etapa, o usuário deve clicar em Salvar Rascunho ou Solicitar remanejamento. 

108 | 1 3 2

<!-- pagina 109 -->
- Caso selecione Salvar Rascunho, será salva uma solicitação com o _status_ “em elaboração”, com o sequencial no formato NNNNN/AAAA- **R** , e o usuário ainda poderá visualizá-la ( ), editá-la ( ) ou excluí-la ( ). 

- Caso selecione Solicitar Remanejamento, será salva uma solicitação definitiva, com o sequencial no formato NNNNN/AAAA, que será encaminhada para análise da unidade gerenciadora e/ou participante e o usuário poderá visualizá-la ( ) ou cancelá-la ( ). 

   - 9.7.2. Consultar solicitação de remanejamento 

Para consultar as solicitações de remanejamento da ata, acesse Solicitar Remanejamento, disponível no menu Gestão de Atas > + Solicitar remanejamento. Logo aparecerá a lista das solicitações de remanejamento realizadas pela unidade com as seguintes informações: 

- Número da solicitação: se o usuário tiver salvado como rascunho o sequencial, será apresentada com o formato NNNNN/AAAA-R; 

- Número da ata; 

- Número da compra; 

- Modalidade da compra; 

- Situação, cujas opções poderão ser: “cancelada”, “em elaboração”, “aguardando aceitação da unidade participante”, “aguardando aceitação da unidade gerenciadora”, “aguardando aceitação” (quando for tanto da unidade gerenciadora quanto participante), “negado pela unidade participante”, “negado pela unidade gerenciadora”, “analisado pela unidade gerenciadora da ata”; 

- Criado em: data e horário em que a solicitação foi gerada; 

- Ações: 

- Caso a solicitação se apresente na situação “em elaboração”, as ações poderão ser: Editar ( ), Visualizar ( ) ou Excluir ( ). 

- Caso a solicitação apresente se na situação “cancelada”, o usuário somente poderá Visualizar ( ). 

- Para as demais situações, o usuário poderá selecionar Visualizar ( ) ou Cancelar ( ). 

109 | 1 3 2

<!-- pagina 110 -->
M A N U A L T É C N I C O O P E R A C I O N A L – **C O N T R A T O S . G O V . B R I N O V A V** 

**E R S Ã O** 

_Figura 160  – Lista de solicitação de remanejamento_ 

9.7.3. Analisar solicitação de remanejamento 

Para analisar as solicitações de remanejamento da ata, acesse Analisar Solicitação de Remanejamento, disponível no menu Gestão de Atas > Analisar solicitação de Remanejamento, e clique na aba correspondente (unidade participante ou unidade gerenciadora da ata), conforme seja a situação a ser analisada. 

_Figura 161  – Lista de análise de solicitação de remanejamento_ 

Será apresentada uma lista com a relação das solicitações a serem analisadas e contendo as seguintes informações: 

• Situação: 

- Caso a solicitação já tenha sido analisada, a situação será “analisado pela unidade participante” ou “analisado pela unidade gerenciadora da ata”, e, no campo ações, o usuário apenas poderá visualizá-la; 

- Caso ainda esteja “aguardando aceitação da unidade participante” ou “aguardando aceitação da unidade gerenciadora” ou “aguardando aceitação”, as ações poderão ser: visualizar ou editar a depender da unidade na qual o usuário estiver logado. 

110 | 1 3 2

<!-- pagina 111 -->
- Data do envio; 

- Nº da solicitação; 

- Nº da ata; 

- Nº da compra; 

- Modalidade; 

- Unidade destino; 

- Ações. 

Ao clicar em “Editar” ( ), a unidade poderá: 

- Aceitar a solicitação; 

- Negar a solicitação, inserindo obrigatoriamente uma justificativa; 

- Aceitar parcialmente a solicitação, inserindo obrigatoriamente uma justificativa. Na aceitação parcial, o usuário deverá informar a quantidade aceita parcialmente que deverá ser menor que a quantidade solicitada. 

A seguir poderá Salvar Rascunho ou Finalizar a Análise. 

_Figura 162  – Análise do remanejamento_ 

9.8. Relatório de execução de Ata 

O Relatório de Execução da Ata visa a atender o disposto no art. 82, §§1º e 2º da Lei 14.133/2021, a fim de informar as aquisições de item(ns) isolado(s) pertencente(s) a um grupo durante a vigência da ata e/ou justificar a não execução de todos os itens do grupo ao final da vigência da ata, sendo salvos os dados de cada usuário que registrou, editou e salvou a informação no sistema, responsabilizando-se este pela informação prestada. 

111 | 1 3 2

<!-- pagina 112 -->
Para gerar o relatório de execução de ata, acesse Gestão de Atas > Ata de registro de preços. 

_Figura 163 - Acesso ao Ata de registro de preços no Gestão de Atas_ 

A seguir será apresentada a lista das atas de registro de preços da unidade em que o usuário estiver logado e que figurem como gerenciadoras, participantes ou não participantes da compra (decorrentes de adesões). 

Em Ações, clicar no botão de Relatar Execução 

_Figura 164  – Relatar execução da ata em Ações_ 

Em Relatar Execução da Ata, serão apresentados todos os itens daquela ata, mesmo para os itens cuja quantidade não foi informada pela unidade, mas que pertença a um grupo. 

Para todos os itens, o usuário deverá informar a quantidade executada, sendo apresentada pelo sistema automaticamente a quantidade empenhada dentro do sistema Contratos.gov.br. Para os itens sem grupo, poderá ser informada uma justificativa caso não haja execução ao final da vigência da ata. Já para os itens que pertençam a um grupo, caso não haja execução de todos eles, a justificativa será obrigatória ao final da vigência da ata. 

112 | 1 3 2

<!-- pagina 113 -->
Para os itens que pertençam a um grupo, quando a unidade não solicitou adesão ou participou de todos os itens, a justificativa será obrigatória para o(s) item(ns) isolado(s) pertencente(s) a um grupo durante a vigência da ata. Se a unidade não possuir quantitativo de certos itens, eles aparecerão bloqueados para melhor visualização do grupo e identificação de que tipo de justificativa deverá ser dada. 

_Figura 165  – Item 00017 não pertencente a um grupo, mas está sem execução: campo justificativa opcional. Item 00018: campos bloqueados, pois a unidade não possui quantitativo nesse item, mas ele pertence à ata._ 

_Figura 166  – Item 00031 não pertence a um grupo: campo justificativa opcional, caso não haja quantidade executada/empenhada. Itens 00009, 00010 e 00011, pertencentes ao grupo 00001:_ 

_campo justificativa obrigatório, caso não haja quantidade executada/empenhada ao final da vigência da ata. Itens 00004 e 00007 pertencentes ao grupo 00002: campo justificativa obrigatório para o item 00004, pois se trata de adesão/participação isolada de item pertencente a grupo, sendo_ 

113 | 1 3 2

<!-- pagina 114 -->
_o item 00007 apresentado como bloqueado para melhor visualização do grupo, pois a unidade não possui saldo nesse item._ 

## 9.9. Adesão a Atas 

Acessando o menu Gestão de Atas > Solicitar adesão, são apresentadas as adesões da unidade e suas respectivas situações em esquema de cores: 

_Figura 167 - Lista de solicitações de adesão e suas situações_ 

Serão listadas as solicitações de adesão já realizadas pela unidade logada com as seguintes informações: 

- Situação: as situações da ata poderão ser: 

   - Cancelada: quando a unidade que solicitou adesão desiste do pedido; 

   - Negada: quando a unidade gerenciadora analisou, negando o pedido; 

   - Em elaboração: quando ainda está em rascunho, não tenho sido finalizada pela unidade solicitante; 

   - Aceita: quando a unidade gerenciadora analisou, aceitando o pedido; 

   - Enviada para aceitação: quando a unidade solicitante finalizou o pedido e enviou para análise pela gerenciadora. 

- Nº da solicitação; 

- Unidade Gerenciadora da ata; 

- Número da compra/ano; 

- Modalidade da compra; 

- Ações: as ações editar e excluir apenas aparecerão para as atas com a situação “em elaboração”. Para as atas que apresentem as demais situações, será apresentada apenas a ação visualizar. 

Para realizar a solicitação de adesão, é importante verificar se a configuração da unidade está correta e com todos os campos preenchidos, principalmente o campo “Esfera” que é validado 

114 | 1 3 2

<!-- pagina 115 -->
para verificação do atendimento ao art. 31, III, do Decreto 11.462/2023 e art. 86, §2º, III da Lei 14.13/2021 e suas alterações. 

Clique na ação Visualizar para verificar as informações de cada solicitação. 

9.9.1. Solicitar adesão à ata de registro de preços 

Para solicitar adesão a uma ata de registro de preços, acesse Gestão de Atas > Solicitar Adesão, clique em + Solicitar adesão: 

_Figura 168  – Lista de solicitações de adesão / Botão Solicitar adesão_ 

Na **aba Item(ns) para adesão** , preencha os campos que deseja utilizar para a busca. Pelo menos um dos seguintes campos deve ser informado para realizar a busca: 

_Figura 169  - Solicitar adesão_ 

115 | 1 3 2

<!-- pagina 116 -->
- Unidade gerenciadora: informe a unidade gerenciadora da ata que se pretende aderir; 

- Número da compra/ano: busque pelo número da compra/ano, sendo necessário informar a unidade gerenciadora. Somente serão apresentadas compras com atas vigentes; 

- Modalidade da compra: selecione conforme o número da compra, sendo necessário informar a unidade gerenciadora e o número da compra. Somente serão apresentadas as modalidades relacionadas ao número da compra informado; 

- Número da ata/ano: busque pelo número da ata/ano. Somente serão apresentadas atas vigentes; 

- Fornecedor: selecione o fornecedor; 

- Unidade solicitante: esse campo já vem preenchido e representa a unidade na qual o usuário está logado e está solicitando a adesão; 

- Itens da ata: indicar item específico da ata informada; 

- Mostrar atas registradas para enfrentamento dos impactos decorrentes do estado de calamidade pública?*: com as opções “Sim” ou “Não” para assinalar. Ao selecionar a opção “Sim”, serão exibidas apenas as atas registradas com amparo legal decorrentes dos normativos de calamidade pública, submetendo-se às exceções de limites de adesão neles previstos; 

- Aquisição emergencial de medicamentos e material de consumo médicohospitalar?*: com as opções “Sim” e “Não” para assinalar. Esse campo é visível quando a unidade gerenciadora da compra pertence ao Ministério da Saúde, possibilitando o atendimento de exceções previstas na legislação para a aquisição emergencial de medicamentos e material de consumo médico-hospitalar; 

- A adesão é destinada à execução descentralizada de programa ou projeto federal?*: com as opções “Sim” e “Não” para assinalar. Esse campo é visível quando a unidade solicitante é estadual, distrital ou municipal, possibilitando o atendimento de exceções previstas na legislação para execução descentralizada de programa ou projeto federal. 

- **Observação** : O botão Limpar apaga todas as informações registradas nos campos utilizados para a busca. 

Clique no ícone Buscar Itens para que sejam apresentados os itens de atas de registro de preços conforme os dados informados. Somente será(ão) exibido(s) item(ns) de ata(s) de registro de preços vigentes, com quantidade disponível para adesão e que permitem adesão para a unidade solicitante. Deve ser observado pela unidade solicitante da adesão se está sendo respeitado o limite estabelecido no Decreto 11.462/2023 e Lei 14.133/2021. 

**Observação** : Para solicitar a adesão a unidade solicitante não pode ser participante do item. 

Na aba **item(ns) para adesão** serão listados os itens da compra e/ou da ata selecionada e apresentadas as seguintes informações de cada item: 

- Unidade gerenciadora da ata; 

116 | 1 3 2

<!-- pagina 117 -->
- Número/ano da compra; 

- Modalidade; 

- Grupo; 

- Nº da ata; 

- Fornecedor (classificação); 

- Nº do item; 

- Descrição do item; 

- Tipo do item: material ou serviço; 

- Quantidade registrada; 

- Valor unitário. 

_Figura 170  - Solicitar adesão - Carregar itens_ 

Ao clicar no botão , o usuário poderá informar a quantidade que deseja solicitar do item marcado e serão apresentadas as seguintes informações adicionais: 

- Valor unitário do item; 

- Vigência da ata; 

- Quantidade disponível para adesão; 

- Quantidade solicitada; 

- Valor total para adesão. 

**Observação:** O campo Quantidade Disponível para Adesão apresenta o total disponível por item, que é a mesma, independentemente da classificação dos fornecedores do item, caso exista mais de um. Estes são apresentados em linhas separadas, uma para cada fornecedor do item. 

Na lista de itens, digite a quantidade desejada no campo Quantidade Solicitada, selecionando assim o item para compor a solicitação. 

**Importante:** O limite da quantidade solicitada por unidade é de 50% da quantidade registrada para o item, desde que não tenha sido atingida a quantidade total permitida para adesões. O sistema valida o limite estabelecido no Decreto 11.462/2023 e Lei 14.133/2021, mesmo que 

117 | 1 3 2

<!-- pagina 118 -->
outro tenha sido informado no Sistema do Compras, cabendo à unidade gerenciadora realizar o controle em caso de limites diferentes do estabelecido na legislação. 

Em algumas exceções previstas na legislação, é possível solicitar além da quantidade total para adesão, devendo ser respeitado o limite individual de 50% para CADA unidade em qualquer caso. 

Informe a quantidade desejada no campo Quantidade Solicitada, para habilitar a seleção do item. Selecione o(s) item(ns) que fará(ão) parte da solicitação de adesão. Podem ser incluídos quantos itens forem necessários, desde que sejam da mesma unidade gerenciadora e da mesma compra. 

O campo Valor Total para a Adesão apresenta o valor total por item. 

_Figura 171  - Solicitar adesão - Digitar quantidade solicitada e selecionar o item desejado_ 

Avance para a aba Justificativa e Anexos clicando no botão Anexos, preencha os campos indicados. 

. Na aba Justificativa e 

118 | 1 3 2

<!-- pagina 119 -->
_Figura 172  - Solicitar adesão - Inserir justificativa e anexos_ 

- Processo de adesão*: informe o número do processo relacionado à adesão; 

- Justificativa da vantagem da adesão*: informe a justificativa para a solicitação de adesão; 

- Anexo justificativa*: selecione e realize o _upload_ do arquivo correspondente ao campo anterior; 

- Foi realizada demonstração de que os valores registrados estão compatíveis com os valores praticados pelo mercado, nos termos da Lei 14.133/2021 (Art. 23 e art. 86, §2º, inc. III)?*: assinale “Sim” ou “Não”; 

- Anexo demonstração*: selecione e realize o _upload_ dos arquivos correspondentes ao campo anterior; 

- Houve prévia consulta e aceitação do fornecedor, nos termos da Lei 14.133/2021 (art. 86, §2º, inc. III)?*”: assinale “Sim” ou “Não”; 

- Anexo aceitação*: selecione e realize o _upload_ dos arquivos correspondentes ao campo anterior; 

- Justificativa de item isolado pertencente a um lote*: informe a justificativa de solicitação de item isolado pertencente a um lote. Esse campo é apresentado quando na seleção consta item que pertence a um lote/grupo da compra e não se está solicitando todos os itens do lote, situação que necessita da apresentação de justificativa. 

- Anexo justificativa item isolado: selecione e realize o _upload_ dos arquivos correspondentes ao campo anterior. 

Finalizada a inclusão das informações necessárias, ao clicar em Solicitar Adesão, a solicitação é registrada e o usuário é direcionado para a tela de listagem das solicitações. 

119 | 1 3 2

<!-- pagina 120 -->
_Figura 173  - Solicitar adesão - Enviar solicitação para análise_ 

Ao clicar em Salvar Rascunho, a solicitação fica na situação "Em elaboração”, podendo ser editada e/ou excluída posteriormente. 

A solicitação em situação “Finalizada” recebe um número no formato XXXXX/XXXX e é enviada para análise da unidade gerenciadora da ata, ficando então na situação "Enviada para aceitação". 

- 9.9.2. Analisar solicitação de adesão 

Acessando o menu Gestão de Atas > Analisar Solicitação de Adesão, são apresentadas as 

adesões recebidas para análise da unidade gerenciadora. Clique na ação Visualizar , 

para verificar as informações de cada solicitação, e na opção para fazer sua análise. 

_Figura 174  - Listar solicitações de adesão_ 

120 | 1 3 2

<!-- pagina 121 -->
_Figura 175  - Analisar solicitação de adesão_ 

São exibidas as informações incluídas pela unidade solicitante: 

- Unidade solicitante; 

- Número da solicitação; 

- Responsável pela solicitação: apresenta nome e e-mail do usuário que enviou a solicitação; 

- Justificativa da vantagem da adesão; 

- Anexo justificativa: clique para realizar o _download_ do documento inserido pelo solicitante; 

- Foi realizada demonstração de que os valores registrados estão compatíveis com os valores praticados pelo mercado, nos termos da Lei 14.133/2021 (Art. 23 e Art. 86, §2º, inc. III)? 

- Anexo Demonstração: clique para realizar o _download_ do documento inserido pelo solicitante; 

- Houve prévia consulta e aceitação do fornecedor, nos termos da Lei 14.133/2021 (Art. 86, §2º, inc. III)? 

- Anexo Aceitação: clique para realizar o _download_ do documento inserido pelo solicitante; 

- Justificativa de item isolado pertencente a um lote: é apresentado quando, na solicitação da adesão, consta item que pertence a um lote/grupo da compra e não se está solicitando todos os itens do lote; 

- Anexo justificativa item isolado: clique para realizar o _download_ do documento, caso tenha sido inserido pelo solicitante; 

- Aquisição emergencial de medicamentos e material de consumo médicohospitalar? : deve ser analisada pela gerenciadora a aplicabilidade da exceção prevista na legislação, caso tenha sido marcada como “sim” essa opção; 

121 | 1 3 2

<!-- pagina 122 -->
- A adesão é destinada à execução descentralizada de programa ou projeto federal?: deve ser analisada pela gerenciadora a aplicabilidade da exceção prevista na legislação, caso tenha sido marcada como “sim” essa opção; 

- Item(ns) analisado(s): no formato XX/XX - quantidade total de itens da solicitação/contabilização dos itens analisados. 

Na sequência são apresentadas as informações sobre o(s) item(ns) da solicitação. Cada item possui um _status_ em esquema de cores: 

- Preto: item não avaliado; 

- Verde: aceito; 

- Amarelo: aceito parcialmente; 

- Vermelho: negado. 

Ao passar o cursor do _mouse_ sobre o _status_ , é apresentada a informação relacionada. 

**Observação:** O campo Quantidade Disponível para Adesão apresenta o total disponível por item, que é a mesma, independentemente da classificação dos fornecedores do item, caso exista mais de um. 

Para analisar a solicitação, assinale uma das opções para cada item: 

- Aceitar: aceita integralmente a quantidade solicitada; 

- Negar: nega totalmente a quantidade solicitada; 

- Aceitar parcialmente: aceita quantidade menor que a solicitada, diferente de zero. 

Ao negar ou aceitar parcialmente, é necessário preencher o campo Justificativa/ Motivação. 

_Figura 176  - Analisar solicitação de adesão - Aceitar / Aceitar parcialmente / Negar adesão_ 

Ao clicar em Salvar Rascunho, as informações incluídas são salvas para conclusão posterior da análise. 

122 | 1 3 2

<!-- pagina 123 -->
Ao clicar em Finalizar Análise, a solicitação passa a constar na situação conforme resultado da análise e o usuário é direcionado para a tela que lista todas as solicitações, sendo disponibilizado para a unidade solicitante o resultado da análise. 

123 | 1 3 2

<!-- pagina 124 -->
## 10. Transparência 

10.1. Acesso ao módulo Transparência 

O menu Transparência não necessita de _login_ para acesso, será possível acessá-lo pelo botão Transparência da página de autenticação do sistema, pelo item Transparência no menu do sistema para usuários autenticados ou pelo endereço <u>https://contratos.sistema.gov.br/transparencia.</u> 

_Figura 1773  - Acesso ao Transparência - Tela de Login_ 

_Figura 178  - Acesso ao Transparência - Menu usuário autenticado_ 

124 | 1 3 2

<!-- pagina 125 -->
## 10.2. Transparência – Tela inicial Abaixo, imagem com detalhamento de todos os componentes da página inicial do sistema. 

_Figura 179  - Transparência - Tela Inicial_ 

10.3. Transparência – Consultar Atas 

Para consultar as atas de registro de preços, clique no ícone 

_Figura 180  – Consultar Ata de Registro de Preços_ 

125 | 1 3 2

<!-- pagina 126 -->
No campo Palavra-chave, informe o termo para busca: unidade gerenciadora, número da compra, número da ata ou órgão. 

No campo Status, escolha dentre as opções apresentadas: vigente, todos, não vigentes. 

Ao clicar em Busca Avançada, são apresentadas mais opções de busca. 

_Figura 181  – Busca avançada de atas de registro de Preços_ 

Preenchidas as informações, clique em Aplicar e em Pesquisar. Abaixo serão listados os resultados. 

_Figura 182  - Resultados pesquisa de atas de registro de preços_ 

126 | 1 3 2

<!-- pagina 127 -->
Ao clicar na seta indicada em cada resultado, é apresentado o detalhamento da ata de registro de preços selecionada. 

_Figura 183  - Detalhamento da ata de registro de preços_ 

Para cada item, é possível obter informações detalhadas, ao clicar em são apresentadas em abas. 

. As informações 

_Figura 184  - Detalhamento do item da ata de registro de preços_ 

127 | 1 3 2

<!-- pagina 128 -->
10.4. Transparência – Consultar Atas por item 

Para consultar itens de atas de registro de preços, clique no ícone 

_Figura 185  - Consultar atas de registro de preços por item_ 

No campo Palavra-chave, informe o termo para busca: unidade gerenciadora, número da compra, número da ata, código do item, descrição do item ou órgão. 

No campo Status, escolha dentre as opções apresentadas: vigente, todos, não vigentes. 

Ao clicar em Busca Avançada, são apresentadas mais opções de busca. 

_Figura 186  - Busca avançada de itens da ata de registro de preços_ 

Preenchidas as informações, clique em Aplicar e em Pesquisar. Abaixo serão listados os resultados. 

128 | 1 3 2

<!-- pagina 129 -->
_Figura 187  - Resultados da busca de itens da ata de registro de preços_ 

Para cada item, é possível obter informações detalhadas ao clicar em . 

10.5. Transparência – Atas de Registro de Preços 

Na tela inicial é possível filtrar as atas de registro de preços clicando no ícone . 

_Figura 188  - Filtrar atas de registro de preços_ 

Clicando no ícone, são apresentadas opções de filtro de resultados. 

129 | 1 3 2

<!-- pagina 130 -->
_Figura 189  - Filtrar atas de registro de preços_ 

Conforme o filtro, as informações são apresentadas a seguir – Valor Total Registrado; Lista De Atas De Registro De Preços; e, no gráfico, Atas de registro de preços por item (%). 

_Figura 190  - Informações apresentadas conforme filtro_ 

Na Lista de Atas de Registro de Preços, selecione a Ata de Registro de Preços sobre a qual deseja mais detalhamento para ser direcionado a ele. 

10.6. Transparência – Consultar Compras 

130 | 1 3 2

<!-- pagina 131 -->
Para consultar Compras, clique no ícone . 

Na parte superior da lista, é possível filtrar por unidade origem; unidade sub-rogada; tipo de compra (SISRP ou SISPP); modalidade e Lei, para facilitar a localização da compra desejada. 

_Figura 191 - Transparência - Consulta ao Saldo de Compras_ 

Ao clicar em ações Visualizar , o usuário obtém as informações sobre a compra: 

_Figura 192 - Visualizar compra_ 

131 | 1 3 2

<!-- pagina 132 -->
Ao clicar em ações Itens , o usuário tem acesso às informações sobre os itens que compõem a compra: 

_Figura 193 - Visualizar itens da compra_ 

Ao clicar na ação Visualizar de cada item, são apresentadas informações do item, abrangendo dados das unidades participantes, de fornecedores homologados e sobre a ata de registro de preços do item (se houver, somente as regidas pela Lei nº 14.133/2021). 

Ao clicar na ação Visualizar de cada fornecedor, são apresentadas informações referentes a contratos firmados, empenhos emitidos e suas alterações. 

132 | 1 3 2
