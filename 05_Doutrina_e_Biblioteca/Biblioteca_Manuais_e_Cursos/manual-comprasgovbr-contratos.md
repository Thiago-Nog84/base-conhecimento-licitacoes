---
arquivo_original: "manual-comprasgovbr-contratos.pdf"
hash_pdf_md5: 8ca190f4b90abd3744a7fbb4cc708743
paginas: 183
metodo: "texto (pymupdf4llm) + OCR em 1 pagina(s)"
convertido_em: 2026-10-03T17:30:15
fonte: Base de Conhecimento CLC
---

<!-- pagina 1 (OCR) -->
© Contratos.gov.br

MANUAL
CONTRATOS.GOV.BR

VERSÃO 1.39.0 — ABRIL/2026

D
MINISTÉRIO DA |

GESTÃO E DA INOVAÇÃO : b

EM SERVIÇOS PÚBLICOS : :

DDDDDDDDDDDDDDDDDDDDDD

<!-- pagina 2 -->
M A N U A L  T É C N I C O  O P E R A C I O N A L  – **C O N T R A T O S . G O V . B R  I  V E R S Ã O  O R I G I N A L** 

# **Ministério da Gestão e da Inovação em Serviços Públicos - MGI** 

**Ministra:** Esther Dweck 

# **Secretaria de Gestão e Inovação - SEGES** 

**Secretário:** Roberto Pojo 

**Secretária Adjunta:** Regina Lemos de Andrade 

# **Departamento de Normas e Sistemas de Logística - DELOG** 

**Diretor:** Everton Batista dos Santos 

# **Coordenação-Geral dos Sistemas de Contratos e Patrimônio - CGCON** 

**Coordenadora Geral:** Anne Camila Knoll 

**Coordenador:** Edher Garrido Lombardi 

# **Equipe:** 

Alice Bressanelli Azevedo 

Brunno dos Passos Alves 

Cleiton Lucas Sampaio Pontes 

Fernanda Vieira Klein Teixeira 

Gildete Mamede Sales 

Kelson Soares Brito Lucas Borges Kappel Marcela Rocha Brum Patrícia Mattar Ricardo Arruda Sowek Rochanna Argenta Betto Barreto 

Sandra Regina Sousa Santos 

2 | 183

<!-- pagina 3 -->
# **Histórico de Versões** 

|**DATA**|**VERSÃO**|**DESCRIÇÃO**|
|---|---|---|
|28/04/2026|1.39.0|1. Evolução da funcionalidade Terceirizados para<br>inclusão de dependentes<br>2. Cadastro de um único para mais de um contrato<br>do tipo empenho do mesmo fornecedor|
|01/04/2026|1.38.0|3. Alteração do acesso para cadastro do<br>Instrumento de cobrança|
|27/03/2026|1.37.0|4. Cancelamento de Saldo de empenho inscrito em<br>Resto apagar|
|16/03/2026|1.36.0|1. Anexo do instrumento inicial<br>2. Inativação de responsáveis|
|29/01/2026|1.35.0|3. Inclusão da evolução no fluxo de detalhamento<br>do subelemento|
|07/01/2026|1.34.0|4. Inclusão da funcionalidade de exclusão de<br>contratos|
|19/12/2025|1.33.0|5. Inclusão da funcionalidade de Alterar DH<br>6. Inclusão da opção de não liquidar empenhos|
|05/11/2025|1.32.0|1. Criação automática deparâmetros do contrato.|
|13/10/2025|1.31.0|2. Configuração de assinatura de preposto na OSF<br>3. Criada aba 'Vigência' no termo de apostilamento<br>para registro de prorrogação automática (art.<br>111 e art. 115, §5º,da Lei 14.133/2021)|
|08/05/2025|1.30.0|1. Inclusão de campo para preenchimento de<br>postos previstos por CBO<br>2. Atualização das informações referentes aos<br>filtros da listagem de contratos e minutas de<br>empenhos.<br>3. Inclusão das funcionalidades Termo Aditivo,<br>Termo Extinção e Relatório final em contratos do<br>tipo empenho.<br>4. Atualização de informações referentes ao<br>cadastrado de instrumento de cobrança.|
|11/02/2025|1.29.0|1. Emissão de empenhos relacionados a plataforma<br>Contrata+Brasil.|
|03/01/2025|1.28.0|1. Inclusão das abas Dedução e Pré-doc na<br>Apropriação do Instrumento de Cobrança.<br>2. Inclusão Grupo Almoxarifado.|
|11/11/2024|1.27.0|1. Buscar Ordem Bancária<br>2. Obrigatoriedade de vinculação de minuta de<br>empenho e/ou empenho por unidade SISG para<br>contratos decorrentes de compra pública<br>3. Retirada  da  opção  de  grupo  de  usuário<br>“Execução folha” para usuários Administrador de<br>órgão e de unidade.|

3 | 183

<!-- pagina 4 -->
M A N U A L  T É C N I C O  O P E R A C I O N A L  – 

**C O N T R A T O S . G O V . B R  I  V E R S Ã O  O R I G I N A L** 

|09/09/2024|1.26.0|1. Inserção da opção salvar contrato do tipo<br>Rascunho em Adicionar Contratos.<br>2. Atualização das figuras com subelemento do<br>empenho no cadastro do instrumento de<br>cobrança.<br>3. Parâmetros do Contrato.<br>4. Código NCM/NBS.<br>5. Grupo de usuário: apoio administrativo.|
|---|---|---|
|18/06/2024|1.25.0|1. Inserção de observação referente a abertura de<br>campo para preenchimento de código de GRU<br>em Pagamento de Instrumento de Cobrança.<br>2. Atualização das figuras e revisão do Pagamento<br>de Instrumentos de Cobrança.|

4 | 183

<!-- pagina 5 -->
|||3. Inserção do campo Série no Instrumento de<br>cobrança do tipo Nota Fiscal<br>4. Transformação do “Termo de Encerramento” em<br>“Relatório Final”.|
|---|---|---|
|10/01/2024|1.24.0|1. Atualização de configurações de integração com<br>o SEI.<br>2. Termo de encerramento em Meus Contratos.<br>3. Atualização das figuras e revisão do Gestão<br>Contratual, Fiscalização e Tela Início.<br>4. Inserir busca de empenhos dos sistemas<br>financeiros externos.<br>5. Inserir informação de unidade na exportação dos<br>relatórios de fracionamento de despesa.<br>6. Atualização dos grupos de usuários (perfil<br>consulta).<br>7. Atualização de configuração do SEI por meio da<br>chave de acesso.|
|21/08/2023|1.23.0|1. Índices econômicos.<br>2. Possibilidade<br>dos<br>arquivos<br>advindos<br>do<br>SUPER/SEI a mais de um contrato.<br>3. Separação da tela de minutas de empenho para<br>o ano atual e anos anteriores.<br>4. Pagamento de instrumentos de cobrança|
|07/06/2023|1.22.0|1. Tela inicial e menu Meus Dados.|
|19/05/2023|1.21.0|1. Buscar itens da compra ao adicionar Contrato.<br>2. Consulta ao SICAF do Fornecedor.<br>3. Gerar PDF no Termo de Encerramento.|
|25/04/2023|1.20.0|1. Ações em Meus Contratos.<br>2. Criação de Contrato do Tipo Empenho.<br>3. Vinculação<br>automática<br>dos<br>empenhos<br>ao<br>Contrato.<br>4. Alteração da situação dos Instrumentos  de<br>Cobrança em lote.|
|05/04/2023|1.19.0|1. Permitir<br>designação<br>de<br>responsáveis<br>de<br>unidades descentralizadas.<br>2. Obrigatoriedade da informação do empenho<br>para unidades SISG ao adicionar Instrumento de<br>Cobrança.<br>3. Possibilidade de os responsáveis por contratos<br>vincularem empenhos em Meus contratos.<br>4. Módulo Transparência.<br>5. Alterar logo e nome do Sistema.<br>6. Incluir grupo de usuários Gestor de Atas.<br>7. Gerar PDF do empenho.<br>8. Definir/remover substitutivo de contrato.|

5 | 183

<!-- pagina 6 -->
|||9. Incluir país de fabricação de materiais no<br>Instrumento de Cobrança.<br>10. Menu Gestão de atas.|
|---|---|---|
|01/03/2023|1.18.0|1. Atualização da Consulta situação Fornecedor<br>SICAF, incluindo as certidões das receitas<br>estaduais/distrital e municipais.<br>2. Possibilidade de salvar Termo de Apostilamento<br>como Rascunho.|
|26/01/2023|1.17.6|1. Inclusão de orientações sobre a funcionalidade<br>de geração automática de cronograma<br>2. Inclusão de orientações sobre a funcionalidade<br>de Importação de autoridades signatárias<br>3. Atualização no cadastro de contrato (Data da<br>proposta)<br>4. Atualização no upload de arquivos do contrato<br>5. Atualizações no instrumento de cobrança<br>(cálculo da data limite) e nas informações<br>exibidas ao consultar|

6 | 183

<!-- pagina 7 -->
# Sumário 

|**1 – Apresentação ......................................................................................................................................... 8**|
|---|
|**2 - Grupos de Usuários ................................................................................................................................. 9**|
|**3 – Gestão Contratual ................................................................................................................................ 10**|
|3.1 – Contratos ........................................................................................................................................... 10|
|3.1.1 – Cadastro de Contratos..................................................................................................................... 11|
|3.1.2 – Cadastro de Contratos do tipo Empenho ........................................................................................ 23|
|3.1.3 – Ações em Contratos ........................................................................................................................ 26|
|3.2 – Fornecedores ..................................................................................................................................... 75|
|3.3 – Sub-rogações ...................................................................................................................................... 77|
|3.4 – Consultas ............................................................................................................................................ 78|
|3.5 – Relatórios ........................................................................................................................................... 87|
|3.6 – Índices econômicos ............................................................................................................................ 90|
|**4 – Fiscalização ........................................................................................................................................... 92**|
|4.1 – Meus contratos .................................................................................................................................. 92|
|4.2 – Arquivos ............................................................................................................................................. 93|
|4.3 – Conta-Depósito Vinculada .................................................................................................................. 94|
|4.4 – Empenhos ........................................................................................................................................ 102|
|4.5 – Cadastro de Instrumentos de Cobrança (Faturas) ............................................................................ 103|
|4.6 – Cadastro de Ocorrências .................................................................................................................. 103|
|4.7 – Cadastro de Terceirizados ................................................................................................................ 103|
|4.8 – Relatório Final .................................................................................................................................. 104|
|**5 – Gestão orçamentária .......................................................................................................................... 104**|
|5.1 – Minutas de Empenho ....................................................................................................................... 104|
|5.2 – Empenhos ........................................................................................................................................ 118|
|5.3 – Restos a Pagar .................................................................................................................................. 124|
|5.4 – Consulta ........................................................................................................................................... 124|
|**6 – Administração .................................................................................................................................... 127**|
|6.1 – Cadastro de usuários ........................................................................................................................ 127|
|6.2 – Alterar usuário ................................................................................................................................. 128|
|6.3 – Login de usuários ............................................................................................................................. 129|
|6.4 – Configuração de Unidade ................................................................................................................. 131|
|6.5 – Autoridade Signatária....................................................................................................................... 134|
|6.6 – Configuração de Órgão ..................................................................................................................... 138|
|**7 – Integração com Sistema Eletrônico de Informações (SEI) .................................................................... 141**|

7 | 183

<!-- pagina 8 -->
|7.1 – Preparar o ambiente do SEI .............................................................................................................. 141|
|---|
|1.1.1.<br>Cadastrar sistema.................................................................................................................. 141|
|1.1.2.<br>Cadastrar serviços do sistema ............................................................................................... 142|
|1.1.3.<br>Cadastrar operações do serviço ............................................................................................ 144|
|7.2 – Configurar a integração com SEI no.br Contratos.gov.br .................................................................. 147|
|7.2.1. Configurar órgão .............................................................................................................................. 147|
|7.2.2. Configurar unidade ........................................................................................................................... 149|
|**8 – Gestão de atas .................................................................................................................................... 152**|
|**9 – Transparência ..................................................................................................................................... 154**|
|9.1 – Contratos ......................................................................................................................................... 156|
|9.2 – Instrumentos de Cobrança ............................................................................................................... 159|
|9.3 - Terceirizados ..................................................................................................................................... 162|
|**10 – Gestão Financeira ............................................................................................................................. 165**|
|10.1 – Instrumentos de Cobrança ............................................................................................................. 165|
|10.2 – Apropriação de Instrumentos de Cobrança .................................................................................... 166|
|10.2.1 - Alterar DH .................................................................................................................................... 173|
|10.2.2 - Não liquidar itens de empenho .................................................................................................... 177|
|10.2.3 – Buscar Ordem Bancária ............................................................................................................... 179|
|**11 – Tela Início ......................................................................................................................................... 179**|
|11.1 – Apresentação ................................................................................................................................. 179|
|11.1 – Barra superior ................................................................................................................................ 180|
|11.1.1 – Abrir chamado ............................................................................................................................ 180|
|11.1.2 – Manual ........................................................................................................................................ 180|
|11.1.2 – Meus Dados ................................................................................................................................ 181|
|**12 – Disposições Finais ............................................................................................................................. 182**|

8 | 183

<!-- pagina 9 -->
# 1. Apresentação 

Com foco na busca pela eficiência da gestão e na melhoria do desempenho das instituições públicas, o Ministério da Gestão e da Inovação em Serviços Públicos (MGISP), em parceria com a AdvocaciaGeral da União, oferta o sistema Contratos.gov.br aos órgãos e entidades da administração pública direta, autárquica e fundacional, incluindo as empresas estatais. A ferramenta faz parte das medidas de eficiência organizacional para o aprimoramento da administração pública federal direta, autárquica e fundacional estabelecidas pelo Decreto nº 9.739, de 28 de março de 2019 (Art. 6º, IX). 

O Contratos.gov.br é uma ferramenta do governo federal que automatiza os processos de gestão contratual e conecta servidores públicos responsáveis pela execução e fiscalização de contratos, tornando informações disponíveis a qualquer momento e melhorando as condições de gestão e relacionamento com fornecedores. 

# **Quem pode utilizar:** 

- Órgãos e entidades da administração pública federal direta, autárquica e fundacional, bem como as empresas estatais; e 

- Demais órgãos e entidades de outros poderes ou das esferas estadual e municipal. 

# **Quanto custa:** 

- O sistema é ofertado gratuitamente aos órgãos e entidades integrantes do Sistema Integrado de Serviços Gerais (SISG), custeado pelo Ministério da Gestão e da Inovação em Serviços Públicos. 

# **Modelo de oferta do sistema:** 

- Disponibilizado de forma centralizada, evitando custos com hospedagem e manutenção de sistemas de Tecnologia da Informação e Comunicação (TIC). 

# **Vantagens da plataforma:** 

- Reduz os problemas relacionados às rotinas de trabalho; 

- Pleno controle das informações do que acontece no âmbito dos contratos de um órgão ou entidade; 

- Promove a eficiência na gestão contratual; 

- Proporciona informações para apoiar as decisões governamentais de alocação mais eficiente de recursos; 

- Infraestrutura centralizada, sem custos para órgãos e entidades do Poder Executivo federal; 

- Maior transparência das informações dos contratos celebrados por toda a administração pública, permitindo a padronização de rotinas e procedimentos. 

# **A ferramenta viabiliza:** 

- Controle de documentos diversos; 

- Controle sobre os prazos de vigência dos contratos; 

- Gestão sobre as informações financeiras do contrato; 

9 | 183

<!-- pagina 10 -->
- Visão global das penalidades aplicadas aos contratados; 

- Controle sobre o valor desembolsado em cada contrato e sobre todos os contratos do órgão ou entidade; 

- Gerenciamento dos diversos contratos sob a responsabilidade do gestor; 

- Facilidade e praticidade nas sub-rogações; 

- Padronização das ações de fiscalização por parte dos fiscais; 

- Controle dos atos administrativos praticados; 

- Controle sobre a fiscalização realizada; 

- Contato fácil com os fornecedores e solução rápida de impasses; 

- Controle sobre a realização de aditivos, apostilamentos, extinção e relatório final do contrato. 

# 2 - Grupos de Usuários 

|**TIPO**|**DESCRIÇÃO**|
|---|---|
|Administrador|Administrador master do sistema com todas as permissões.|
|Administrador<br>Órgão|Administrador do Órgão, com permissão de cadastrar usuários em todas as<br>Unidades Gestoras de seu Órgão. Acessa as funcionalidades do Administração<br>> Estrutura e > Usuário do seu órgão.|
|Administrador<br>Unidade|Administrador de unidade com permissão para cadastrar usuários da sua<br>unidade. Acessa as funcionalidades do Administração > Estrutura e > Usuário<br>da sua Unidade. Apenas Administrador ou Administrador do Órgão podem<br>cadastrar Administrador de Unidade.|
|Almoxarifado|Perfil com permissão para cadastrar Instrumento de Cobrança aos Contratos<br>do tipo Empenho e aos contratos de sua responsabilidade|
|Apoio<br>administrativo|Perfil de consultas a dados de Contratos, podendo inserir informações<br>referentes às funcionalidades de “Parâmetros” e “Responsáveis por<br>contrato”.|
|Consulta|Perfil de consultas a dados de Contratos, Fiscalização e Orçamento.|
|Execução<br>Financeira|Perfil com permissão de criar minutas de empenho, realizar apropriação de<br>instrumentos de cobrança, bem como criar contrato do tipo empenho. Acessa<br>as funcionalidades do Gestão Orçamentária e Gestão Financeira e no Gestão<br>Contratual para consulta ou criação de contrato do tipo empenho.|
|Gestor de Ata|Perfil de usuários que terão acesso ao ambiente da nova versão do<br>Contratos.gov.br, onde ocorre a gestão das atas de registro de preços. Acessa|

10 | 183

<!-- pagina 11 -->
||as funcionalidades no Contratos.gov.br – Nova Versão. Apenas Administrador<br>do Órgão ou Administrador Unidade podem cadastrar Gestor de Ata.|
|---|---|
|Preposto|Perfil com permissão para acompanhar seus contratos.|
|Responsável por<br>Contrato|Perfil de acompanhamento e manutenção dos contratos pelos quais é<br>responsável. Acessa as funcionalidades do Gestão Contratual > Meus<br>Contratos no Contratos.gov.br – Versão Original, bem como o módulo<br>Fiscalização e Gestão de Contratos do Contratos.gov.br – Nova Versão.|
|Setor Contratos|Perfil de Usuários que realizam a gestão do contrato, atuando na formalização<br>dos Contratos, Termos Aditivos, Termos de Apostilamento, entre outros.<br>Acessa as funcionalidades do Gestão Contratual.|

# 3 – Gestão Contratual 

Módulo habilitado para o perfil Setor Contratos, voltado aos usuários que realizam a gestão contratual. 

# 3.1 – Contratos 

Acessando o menu **Gestão Contratual > Contratos** , são exibidos todos os contratos registrados na unidade. Por padrão, só são exibidos contratos cujo status esteja ATIVO e pertencentes ao ANO atual. Para visualizar contratos INATIVOS basta clicar na coluna Ativo/ Inativo. Já para exibir os contratos com outras situações como ENCERRADO, EXTINTO, RASCUNHO, VIGENTE ou EXPIRADO utilize a coluna Situação e selecione as situações desejadas. 

Figura 1 – Contratos 

Por meio do “Adicionar Contratos” é possível incluir vários tipos de contratação (Contrato, Convênio, Empenho, entre outros). A tipo “Empenho” serve para aqueles decorrentes apenas de Nota de Empenho, tendo a opção de criação mais automatizada “Criar contrato do tipo Empenho”, explicada no item 3.1.2 deste Manual. 

11 | 183

<!-- pagina 12 -->
Além disso, existe a opção de criação do Contrato do tipo Rascunho, onde o usuário pode iniciar o registro do contrato, sem necessidade de informação da data de assinatura ou data de publicação. 

Em visibilidade da coluna, é possível acrescentar colunas na apresentação dos contratos com outras informações. No botão Pesquisar, busque por Número do instrumento, Fornecedor, Modalidade da Compra, Número Compra, Unidade Compra. 

Figura 2 – Visibilidade da coluna e botão de Pesquisar em Gestão Contratual 

3.1.1 – Cadastro de Contratos 

Para efetuar o cadastro de um novo contrato, clique em “Adicionar Contrato”. 

Figura 3 – Contratos 

Preencha os campos indicados na aba “Dados do contrato”: 

- “Fornecedor”: preencha com o fornecedor contratado; 

12 | 183

<!-- pagina 13 -->
- “Minutas de Empenho”: após preenchido o fornecedor, serão exibidas todas as minutas de empenho emitidas para aquele fornecedor na unidade. Após a seleção de uma das minutas, apenas as minutas da mesma compra serão exibidas. Caso tenha sido emitida minuta de empenho para a compra que originou o contrato que está sendo cadastrado, esta minuta poderá ser selecionada e várias informações como Unidade Compra, Modalidade, Amparo Legal, Número da Compra e Itens do contrato serão preenchidas automaticamente; 

- Fornecedor(es) subcontratado(s): possíveis fornecedores subcontratados no contrato. Se o fornecedor não for encontrado, poderá ser cadastrado; 

- “Data da Assinatura”: data de assinatura do contrato. Caso seja escolhida a opção Salvar Rascunho, este campo não é obrigatório; 

- “Data da Publicação no DOU”: caso preenchida com data posterior à data atual será criado extrato para publicação do contrato no Diário Oficial da União. Caso contrário, não será criada publicação. Para Contratos decorrentes da Lei 14.133/2021 e suas derivadas, onde não há obrigatoriedade de preenchimento desse campo, pode ser utilizado para registrar a data de divulgação do contrato no PNCP (Portal Nacional das Contratações Públicas), o que ocorre automaticamente no mesmo dia de registro do termo. Caso seja escolhida a opção Salvar Rascunho, este campo não é obrigatório; 

- “Autoridades Signatárias”: caso haja autoridades cadastradas na unidade, estas poderão ser selecionadas para signatárias do contrato (verificar o item 6.5 deste Manual). Apenas uma autoridade pode ser selecionada por contrato; 

- “Objeto”; 

- “Informações Complementares”; 

- “Modalidade Compra”; 

- “Amparo Legal”; 

- “Contrata +Brasil”: marcar sim ou não; 

- “Número Compra”; 

- “Unidade Compra”: preencha com a unidade que realizou a licitação (Unidade Gerenciadora da Compra) ou a compra direta; 

- “Unidade Beneficiária”: preencha se você estiver consumindo o saldo da compra de uma UASG polo ou subordinada à UASG do usuário. 

Os campos marcados com * são de preenchimento obrigatório. 

Os dados da compra informados por órgãos Sisg serão validados. Para os órgãos não-Sisg, serão validadas as compras realizadas com fulcro na Lei 14.133/2021. Se, para os casos, for identificado algum dado divergente da compra, não será permitida a conclusão do cadastro do contrato e isso impactará na emissão de minuta de empenho do tipo contrato (Compra não encontrada). 

**Obs.:** Órgão Sisg ao cadastrar um contrato ou editar um instrumento inicial, desde que selecionada no campo “Receita / Despesa” a opção de despesa e a modalidade seja diferente de “Não se aplica”, será necessário informar uma minuta de empenho no campo “Minutas de empenhos” na aba “Dados do contrato” ou adicionar um empenho na aba “Empenhos”. Caso contrário não será possível salvar o contrato e o sistema alertará com a seguinte mensagem _“O campo Minutas de_ 

13 | 183

<!-- pagina 14 -->
_Empenho ou Empenho é obrigatório quando o contrato é do tipo despesa e a modalidade decorrente de uma contratação.”_ 

Preenchidos os dados, clique em “Próxima Aba”. 

Figura 4 – Cadastro de Contrato – Dados do contrato 

Preencha os campos indicados na aba “Características do contrato”: 

- “Receita/Despesa”; 

- “Tipo”: selecione o tipo de instrumento que está sendo celebrado; 

- “Subtipo”; 

- “Categoria”: selecione a categoria do contrato; 

- “Dedicação Exclusiva de Mão de obra?”; 

   - “Aplicável o Decreto 11.430/2023 à contratação?”: esse campo só fica desbloqueado quando se tratar de contrato com dedicação exclusiva de mão de obra, tornando obrigatória a escolha de uma das opções. Para outras situações, o campo não fica disponível para preenchimento, haja vista que o Decreto 11.430/2023 não se aplica às demais opções. O Decreto é aplicável para contratação de serviços contínuos com regime de dedicação exclusiva de mão de obra, com quantitativos mínimos de vinte e vinco colaboradores, que tenha havido previsão em edital de licitação ou aviso de contratação 

14 | 183

<!-- pagina 15 -->
direta e o Estado possua acordo de cooperação técnica firmado com o Ministério de Gestão e Inovação em Serviços Públicos e o Ministério das Mulheres. Assim, que nem todos os Contratos do tipo Mão de obra com dedicação exclusiva estão sujeitos à aplicabilidade do Decreto, devendo ser observado se todos os requisitos anteriormente mencionados estão sendo atendidos; 

- “CBO”: Informe o Código Brasileiro de Ocupações (CBO) e a quantidade de postos. 

   - **Quando o Decreto nº 11.430/2023 for aplicável** : ao preencher o campo “Quantidade de postos previstos”, o campo “Quantidade de postos do Decreto nº 11.430/2023” será automaticamente calculado como 8% do valor inserido. Esse valor poderá ser editado manualmente. 

   - **Quando o Decreto nº 11.430/2023 não for aplicável** : o campo “Quantidade de postos do Decreto nº 11.430/2023” não será exibido. 

- “Subcategoria”: caso haja subcategorias cadastradas para o Órgão (verificar item 6.5 deste Manual), estas serão exibidas; 

- “Contrato”: informe um número de contrato que não esteja sendo utilizado. O número é composto por nove números, sendo os quatro últimos referentes ao ano do contrato que não pode ser futuro, nem cinquenta anos antes do ano vigente; 

- “Código Sistema Externo”: preencher com código do contrato sistema externo integrado 

- “Número Processo”; 

- “Unidade Gestora Origem do Contrato”: unidade que formalizou o contrato inicialmente. Esta opção vem bloqueada para edição para o primeiro registro do Contrato com a unidade do usuário que está cadastrando-o; 

- “Unidade Gestora Atual”: sendo o primeiro registro do contrato, deverá ser preenchida com a mesma unidade gestora origem do contrato. Após uma sub-rogação, esta unidade passa a ser para quem o contrato foi sub-rogado e é responsável por ele; 

- “Unidades Requisitantes”: unidades que são atendidas pelo contrato; 

- “Prorrogável”: indicar se o contrato é continuado (marcar a opção Sim) ou de escopo (marcar a opção Não); 

- “Prazo Indeterminado?”; 

- “Deseja gerar cronograma automático para o Contrato?”: Quando marcada a opção “Sim” será gerado o cronograma considerando as informações a serem preenchidas na aba “Vigência/Valores”. Quando marcada opção “Não”, será necessário incluir em Contratos > Mais (Engrenagem) > Cronograma > + Adicionar Cronograma Contrato, para que a informação do valor acumulado do contrato fique correta. 

- “Arquivo”: anexar o contrato assinado ou instrumento equivalente. Para contratos enviados ao PNCP, o anexo é obrigatório. O arquivo inserido nesta etapa será disponibilizado automaticamente no portal de Transparência, independentemente da legislação aplicável, e também será publicado no PNCP quando se tratar de contratos regidos pela Lei nº 14.133/2021. Caso o documento contenha dados pessoais que não possam ser divulgados publicamente, o órgão deverá realizar a devida anonimização dessas informações antes da publicação do arquivo. 

Os campos marcados com * são de preenchimento obrigatório. 

Preenchidos os dados, clique em “Próxima Aba”. 

15 | 183

<!-- pagina 16 -->
Figura 5 – Cadastro de Contrato – Características do contrato 

Na aba “Itens do contrato”, caso tenha sido vinculada Minuta de Empenho na aba Dados do Contrato, os itens já estarão cadastrados automaticamente. Lembrando que tais itens são os mesmos emitidos na Minuta de Empenho selecionada. O campo Tipo de Material virá selecionado como Consumo ou Permanente dependendo do subelemento da Minuta de empenho. Os campos em que será possível edição são: 

- “Quantidade”: quantidade contratada; 

- “Qtd. parcelas": campo criado para adequação do valor total do contrato em ajuste na importação das informações do sistema Compras para o sistema Contratos. Não confundir com o campo “Núm. Parcelas” previsto na próxima aba “Vigência/Valores”, onde deverá ser preenchida a quantidade de meses em que o contrato será pago. 

- “Data Início”: data de início do item no contrato. Deve ser igual ou posterior à data início da vigência do contrato; 

- “Ações”: permite excluir o item. 

Para os itens da compra que não foram emitidos empenho anterior – como um item que gere receita, por exemplo, e não exija prévio empenho, é possível buscá-lo por meio do “Buscar Itens da Compra”. 

Figura 6 – Aba “Itens do Contrato” com empenho vinculado 

Caso não tenha sido vinculada Minuta de Empenho, é possível “Inserir Item” ou “Buscar Itens da Compra”. 

16 | 183

<!-- pagina 17 -->
Figura 7 – Aba “Itens do Contrato” sem empenho vinculado 

Para a opção “Inserir Item”, preencha os campos indicados na aba “Itens do Contrato”: 

- “Tipo Item”: selecione o tipo do item Material ou Serviço; 

- “Tipo do Material”: opção bloqueada para itens de Serviço e obrigatória para itens de Material, devendo ser escolhida entre Consumo ou Permanente; 

- “Número Item Compra”: número do item informado na compra; 

- “Item”: CATMAT ou CATSER e descrição do item, podendo ser vista a descrição detalhada 

ao clicar sobre a seta “ ”, caso possua; 

- “Código NCM/NBS”: código NCM/NBS retornado da compra para o item. Caso não tenha sido informado ou a Compra não esteja retornando esse dado, o campo ficará sem informação; 

- “Quantidade”: quantidade contratada; 

- “Valor unitário”: valor unitário homologado do item; 

- “Qtd. parcelas”: esse campo será utilizado para multiplicar o valor informado na quantidade e no valor unitário para resultar no valor total a ser contratado; 

- “Valor total”: resultado da multiplicação dos campos “Quantidade”, “Valor unitário” e “Qtd. parcelas”; 

- “Data Início”: data de início do item no contrato. Deve ser igual ou posterior à data início da vigência do contrato. 

Após preenchidos todos os campos, clique em “Incluir”. Se houver mais itens a serem incluídos, repita o processo. 

17 | 183

<!-- pagina 18 -->
Figura 8 – Cadastro de Contrato – Itens do contrato 

Para a opção “Buscar Itens da Compra”, precisam estar preenchidos os dados “Fornecedor”, “Modalidade Compra”; “Amparo Legal”; “Número Compra” e “Unidade Compra” na aba “Dados do Contrato”. Serão listados todos os itens da compra para seleção, podendo ser escolhido todos ou algum específico. 

Figura 9 – Lista dos itens da compra buscada 

Após a seleção do(s) item (ns) que será(ão) objeto do contrato, clique em “Incluir”. 

Figura 10 – Inclusão dos itens da compra buscada 

Serão apresentados o(s) item(ns) selecionado(s). Preencha os campos indicados na aba “Itens do Contrato”: 

- “Tipo do Material”: opção bloqueada para itens de Serviço e obrigatória para itens de Material, devendo ser escolhida entre Consumo ou Permanente; 

- “Quantidade”: quantidade contratada; 

- “Data Início”: data de início do item no contrato. Deve ser igual ou posterior à data início da vigência do contrato. 

Figura 11 – Itens trazidos da compra para preenchimento 

18 | 183

<!-- pagina 19 -->
Preenchidos os dados, clique em “Próxima Aba”. 

Na aba “Empenhos” serão apresentados os empenhos que arcarão com as despesas daquele contrato. 

Caso tenha sido vinculada Minuta de Empenho na aba Dados do Contrato, os empenhos correspondentes já estarão cadastrados automaticamente, não permitindo exclusão, salvo se retirada a minuta de empenho. Para empenhos vinculados manualmente, terá a opção de excluir na coluna “Ações”, por meio do ícone . 

Figura 12 – Apresentação dos empenhos adicionados manualmente com opção de exclusão e vinculados 

automaticamente por meio da Minuta de empenho informada na aba “Dados do contrato” 

Para adicionar um empenho não decorrente de uma minuta de empenho emitida dentro do sistema Contratos.gov.br, seja para aqueles emitidos diretamente no Siafi ou no sistema financeiro externo de origem, para as unidades que possuam integração com o sistema Contratos.gov.br, preencha os campos indicados na aba “Empenhos”: 

- “Unidade Emitente do Empenho”: preencha a unidade emitente do empenho, ou seja, aquela em que o recurso orçamentário foi utilizado; 

- “Fornecedor”: preencha o fornecedor informado no empenho; 

- “Empenho”: informe o número do empenho no formato 202XNEXXXXXX e clique em “Adicionar” 

19 | 183

<!-- pagina 20 -->
Figura 13 – Aba Empenhos 

A(s) unidade(s) emitente(s) constante(s) nessa aba “Empenho” serão cadastradas automaticamente como unidade(s) descentralizada(s) desse contrato, caso seja(m) diferente(s) da unidade gestora do contrato, podendo ser consultada(s) em **Gestão contratual > Contratos > Ações > Unidades Descentralizadas** , bem como os empenhos informados serão associados ao contrato no **Gestão contratual > Contratos > Ações > Empenhos** automaticamente. 

Preenchidos os dados, clique em “Próxima Aba”. 

Preencha os campos indicados na aba “Vigência/Valores”: 

- “Data da proposta”: data-base da proposta na seleção do fornecedor que será utilizada para reajustamento do contrato; 

- “Data de início da vigência”: data de início da vigência do contrato. Deve ser igual ou posterior à data de assinatura do contrato; 

- “Data do término da vigência”: data de término da vigência do contrato; 

- “Valor Global”: valor global do contrato; 

- “Núm. Parcelas”: número de parcelas do contrato em que ocorrerá pagamento; 

- “Valor Parcela”: o valor da parcela é obtido através da divisão do valor global pelo número de parcelas. 

20 | 183

<!-- pagina 21 -->
Figura 14 – Cadastro de Contrato – Vigência/Valores 

Após preenchido todos os campos, clique em “Salvar e voltar”, se já deseja ativar o contrato. 

Caso seja um contrato em elaboração clique em “Salvar Rascunho”. Neste caso, ficará disponível a opção de edição na página inicial dos Contratos, basta clicar no ícone e realizar as edições necessárias. Ao salvar um contrato como rascunho, os campos da data de assinatura e data de publicação no DOU se tornam facultativos, tornando obrigatório seu preenchimento para ativá-lo, com exceção do campo data de publicação no DOU quando se tratar de contrato decorrente da Lei 14.133/2021 e derivadas, pois o campo permanece opcional. 

Um contrato salvo como rascunho não tem implicações externas, como publicações no Transparência, nem no PNCP, nem possui a maioria das funcionalidades no menu de ações que um contrato ativo possui, não sendo possível utilizar a mesma numeração de um contrato do mesmo tipo, mesmo que esteja como rascunho. 

Figura 15 – Contrato salvo como Rascunho 

21 | 183

<!-- pagina 22 -->
Para ativar um contrato, clicar no ícone  , sendo aberta uma caixa com os campos de data de assinatura, data de publicação no DOU e número do contrato para confirmação ou preenchimento das informações e após clicar em “Ativar”. 

Figura 16 – Ativar um contrato 

Se os dados estiverem corretos, tanto ao “Salvar e voltar” ou no “Ativar”, será exibida a tela de Publicações com a publicação do contrato cadastro, caso tenha sido inserida data posterior à atual no campo referente à publicação no DOU. 

Se houver algum erro, o sistema emitirá alerta acerca de quais campos deverão ser corrigidos. 

Na tela de “Publicações”, serão exibidas as relativas ao contrato, caso existentes. 

A formatação do texto da publicação NÃO deverá ser alterada! 

Caso algum dado esteja incorreto, altere os dados do contrato que a minuta da publicação será retificada. 

A “Data Publicação” será a data informada quando do cadastro do contrato. Se não for informada uma data futura, não será criada uma minuta de publicação. 

A “Situação Publicação” estará com status “A PUBLICAR”. 

A “Situação Imprensa” estará com status “PENDENTE”. 

A publicação não mais é enviada automaticamente, logo o usuário do grupo Setor Contratos precisa enviar manualmente, clicando no ícone . 

A “Situação Publicação” ficará com status “TRANSFERIDO PARA IMPRENSA” e a “Situação Imprensa” ficará com status “EM EDITORACAO”. 

Após a publicação, os status serão alterados para “PUBLICADO” e “PUBLICADA”, respectivamente. 

Figura 17 – Publicações 

22 | 183

<!-- pagina 23 -->
Se o contrato for originado a partir da Lei 14.133/2021, o ícone estará habilitado e, se clicado, levará para a página do contrato no Portal Nacional de Contratações Públicas (PNCP). 

Clicando no ícone (Mais), são exibidas várias ações possíveis de serem executadas no contrato: 

- “Arquivos”; 

- “Cronograma”; 

- “Despesas Acessórias”; 

- “Empenhos”; 

- “Histórico”; 

- “Garantias”; 

- “Itens”; 

- “Minutas de Documentos”; 

- “Padrões DH SIAFI”; 

- “Parâmetros”; 

- “PNCP Arquivos”; 

- “PNCP Link”; 

- “Prepostos”; 

- “Publicações DOU”; 

- “Responsáveis”; 

- “Status”; 

- “Unidades Descentralizadas”; 

- “Conta-Depósito Vinculada”; 

- “Instrumentos de Cobrança”; 

- “Local de execução”; 

- “Ocorrências”; 

- “Terceirizados” 

- “Instrumento Inicial”; 

- “Termo Aditivo”; 

- “Termo Apostilamento”; 

- “Termo Extinção”; 

- “Relatório Final”. 

Já para o contrato em “Rascunho”, as opções ao clicar no ícone (Mais) são: “Arquivos” e “Minutas de Documentos”. 

23 | 183

<!-- pagina 24 -->
Figura 18 – Ações – Mais opções (Contratos e Contratos Rascunho) 

3.1.2 – Cadastro de Contratos do tipo Empenho 

Os usuários com perfil Setor Contratos, Execução Financeira e Almoxarifado podem acessar essa funcionalidade. 

Para realizar o cadastro de contratos do tipo Empenho, serão necessários alguns requisitos: 

- Que a minuta de empenho seja do tipo Compra; 

- Que a minuta de empenho seja definida como substitutivo de contrato; 

- Que a minuta não tenha sido vinculada a outro contrato; 

- Que o empenho esteja assinado, e 

- Que tenha sido gerado o PDF do empenho (apenas para Lei 14.133/2021, para a s demais legislações não é necessária a impressão PDF, sendo opcional). 

Para definir um empenho como substitutivo de contrato, verificar o item 6.1, alínea “E” deste Manual. 

Após a assinatura do empenho, é necessário gerar o PDF do empenho para se certificar que ele está apto a se tornar um contrato. Para isso, ir em **Gestão orçamentária > Minuta empenho > Minutas 202X >** na minuta substitutiva de contrato clicar na engrenagem **“Mais” > PDF Empenho** . 

Realizadas as etapas acimas, ir em **Gestão Contratual > Contrato** e clique em “Criar Contrato do tipo Empenho” para efetuar o cadastro. 

Figura 19 – Criar Contrato do tipo Empenho 

Serão listados todos os empenhos que se encaixam nos requisitos mencionados acima e estejam aptos a se tornarem um contrato. É possível selecionar um ou mais empenhos para criação em lote desses contratos do tipo empenho. Após a seleção, clicar em “Criar Contrato(s) do tipo Empenho”. 

24 | 183

<!-- pagina 25 -->
Figura 20 – Seleção das minutas de empenho substitutivas de contrato 

Em seguida, será exibida a mensagem e criado o contrato automaticamente, cujo número será o mesmo da Nota de Empenho e puxando as informações contidas no empenho, com vigência inicial sendo a data de assinatura trazida pela data de emissão da minuta e a vigência final é o último dia do ano corrente. Caso o empenho seja inscrito em restos a pagar, deve ser editado o Instrumento Inicial para informar a nova data fim de vigência em **Gestão Contratual > Contratos > Mais > Instrumento Inicial > Editar** . 

Figura 21 - Contrato do tipo Empenho criado 

Ao ser criado, sendo um empenho decorrente de Compra da Lei 14.133, o contrato já é enviado automaticamente ao PNCP e o arquivo é anexado na **Gestão Contratual > Contratos > Mais > Arquivos** com a Nota de Empenho do SIAFI. 

25 | 183

<!-- pagina 26 -->
Figura 22 – Arquivos do Contrato do tipo Empenho no PNCP 

Figura 23 – Histórico do Contrato do tipo Empenho no PNCP 

Para contratos do tipo empenho não é possível incluir apostilamentos. 

Estão disponíveis algumas funcionalidades semelhantes aos outros tipos de contrato, que são explicadas nas alíneas a seguir: 

- “Arquivos”; 

- “Cronograma”; 

26 | 183

<!-- pagina 27 -->
- “Empenhos”; 

- “Histórico”; 

- “Itens”; 

- “Padrões DH SIAFI”; 

- “Parâmetros”; 

- “PNCP Link”; 

- “Prepostos”; 

- “Publicações”; 

- “Responsáveis”; 

- “Unidades Descentralizadas”; 

- “Instrumentos de Cobrança”; 

- “Local de Execução”; 

- “Ocorrências”; 

- “Instrumento Inicial”; 

- “Termo Aditivo; 

- “Termo Extinção”; 

- “Relatório Final”. 

Figura 24 – Submenu “Mais” em Ações do Contrato do tipo Empenho 

3.1.3 – Ações em Contratos 

A maioria das funcionalidades estão disponíveis apenas para usuário com perfil “Setor Contratos”. Algumas são apresentadas para outros perfis de usuário tão somente como consulta. Para os usuários responsáveis por contratos que desejem cadastrar alguma informação, o caminho deve ser 

27 | 183

<!-- pagina 28 -->
os **Gestão Contratual > Meus Contratos** , tratado no item 4.1 deste Manual. 

**A) ARQUIVOS** 

Para adicionar arquivos ao contrato pelo usuário do Setor Contratos, selecione o contrato desejado, clique no ícone “ ” e em “Arquivos”. 

Serão exibidos todos os arquivos já adicionados ao Contrato, inclusive os adicionados por Responsável por contrato (verificar o item 4.2 deste Manual), podendo alterar seu status, visualizálo e excluí-lo. 

Também será exibido o anexo do instrumento inicial. Para esse tipo de arquivo, não será possível alterar o status ou excluí-lo. Caso seja necessária a substituição, clique em “Editar”. 

Para Adicionar um novo arquivo clique em “Adicionar Arquivo do Contrato”. 

Figura 25 – Adicionar Arquivo do Contrato 

Figura 26 -Editar um arquivo 

Anexe o novo arquivo desejado e, em seguida, clique em “Salvar”. 

28 | 183

<!-- pagina 29 -->
Figura 27 – Substituir Anexo do Instrumento Inicial 

Preencha os campos indicados. Clique na aba “Envio local de anexo(s)” e depois em “Selecionar arquivo(s)”. Será aberta uma janela para que o arquivo em formato PDF seja selecionado. 

- “Tipo”: selecione o tipo de documento que está sendo inserido, cujas opções são: Contrato, Declaração Decreto 11.430/2023, Garantia, Nota de Empenho, Outras Publicações, Outros Arquivos, Planilha Custo, Publicações DOU, Relatório Final do Contrato, Termo Aditivo, Termo Apostilamento, Termo de Reconhecimento de Dívida, Termo de Referência e Termo Rescisão; 

- “Termo”: caso selecione Contrato, Termo Aditivo, Termo Apostilamento ou Termo Extinção, selecione a qual termo o arquivo se refere. Para outros documentos, aparecerá a opção “Não se aplica”. Se for escolhido algum desses tipos e não tiver registro do termo no sistema, aparecerá a opção “Não encontrado”, devendo ser feito o registro do termo anteriormente ao arquivo; 

- “Descrição”: descrição acerca do arquivo inserido; 

- “Nº processo Sapiens”: número do documento SEI do arquivo; 

- “Restrito?”: Marcar “Sim” se o arquivo tem informações sensíveis para a Lei Geral de Proteção de Dados Pessoais (LGPD). Se marcado como “Sim”, o arquivo não será exibido na seção de transparência do sistema. O julgamento sobre se o arquivo deve ser restrito ou não cabe ao gestor. Selecionada a opção “Não”, apenas usuários com login cadastrado naquela Unidade terá acesso ao documento. 

Para contratos da Lei 14.133/2021 e derivadas, os arquivos que sejam dos tipos Contrato, Termo de Extinção, Termo Aditivo, Termo de Apostilamento, Nota de Empenho e Relatório Final do Contrato e que estejam com a situação “Restrito: Não” são enviados ao PNCP. Para consultar os tipos de documentos aceitos para serem enviados ao PNCP, consulta o manual de integração atualizado, disponível em Manuais — Portal Nacional de Contratações Públicas - PNCP. Para os tipos Contrato, Aditivo, Apostilamento e Extinção é necessário que o respectivo termo tenha sido registrado no sistema e vinculado ao arquivo selecionado. Os outros tipos de arquivo, independentemente do 

29 | 183

<!-- pagina 30 -->
amparo legal da contratação, ao ser incluído como “Restrito: Não”, são enviados para o ambiente de transparência do sistema. 

Após preenchidos os campos, clique em “Salvar e voltar”. 

Os campos marcados com “*” são de preenchimento obrigatório. 

Figura 28 – Adicionar Arquivo do Contrato 

**B) VINCULAÇÃO DE ANEXO(S) DO SUPER (OU SEI)** 

Após a configuração do Super.gov.br ou do SEI do órgão ou da unidade, conforme procedimentos detalhados no item 7.2 deste manual, será possível utilizar a funcionalidade de vinculação de anexo(s) do Super (SEI), que vincula um link de documento do sistema de processo eletrônico do órgão diretamente ao contrato cadastrado no Contratos.gov.br. 

Através da aba “Vinculação de Documento(s) do Super (SEI)”, é possível consultar os documentos do processo eletrônico e associá-lo ao contrato no Contratos.gov.br. Porém, é preciso que tanto o processo, quanto o documento estejam com o nível de acesso definido como "Público". 

Caso não tenha sido feita a preparação do ambiente para esta integração (verificar item 7 deste Manual), aparecerá a mensagem de alerta: 

Figura 29 – Alerta de vinculação de documento do SUPER(SEI) sem a configuração de integração 

Após a configuração de integração feita, acesse o menu **Gestão Contratual > Contratos > Mais > Arquivos > Adicionar Arquivo do Contrato > aba Vinculação de Documento(s) do Super (SEI)** . 

30 | 183

<!-- pagina 31 -->
Figura 30 – Vinculação de anexo(s) do SUPER(SEI) 

O número do processo cadastrado no contrato é exibido por padrão, mas é possível selecionar outro(s) processo(s), caso esteja(m) relacionado(s)/anexado(s) no Super (ou SEI). Selecione o número de processo ao qual deseja consultar e clique em "Consultar anexos no SEI". 

Figura 31 – Selecionar processo 

Figura 32 – Consultar documentos no processo 

31 | 183

<!-- pagina 32 -->
Serão relacionados os documentos públicos do processo selecionado. O mesmo arquivo do processo pode ser vinculado a mais de um contrato. Apenas os documentos assinados serão passíveis de visualização e adicionar como arquivo. Utilize o campo “Pesquisar”, caso deseje localizar um documento específico 

- Clique no ícone , caso deseje visualizar o documento. 

Figura 33 – Pesquisa e visualização de documento 

- Selecione o(s) arquivos que deseja vincular ao contrato e clique em Selecionar Registros. 

Figura 34 – Selecionar registros 

- “Tipo”: selecione o tipo de documento que está sendo inserido, cujas opções são: Contrato, Declaração Decreto 11.430/2023, Garantia, Nota de Empenho, Outras Publicações, Outros Arquivos, Planilha Custo, Publicações DOU, Relatório Final do Contrato, Termo Aditivo, Termo Apostilamento, Termo de Reconhecimento de Dívida, Termo Referência e Termo Extinção; 

32 | 183

<!-- pagina 33 -->
- “Termo”: caso selecione Contrato, Termo Aditivo, Termo Apostilamento ou Termo Extinção, selecione a qual termo o arquivo se refere. Para outros documentos, aparecerá a opção “Não se aplica”. Se for escolhido algum desses tipos e não tiver registro do termo no sistema, aparecerá a opção “Não encontrado”, devendo ser feito o registro do termo anteriormente ao arquivo; 

- Preencha uma descrição para o arquivo, caso deseje. 

- Selecione se o arquivo será Público ou Restrito. Arquivos restritos não são disponibilizados no módulo Transparência do sistema ou enviados ao PNCP. 

- Após preenchidos os campos, clique em Salvar e voltar. 

Figura 35 – Preenchimento de campos em Arquivos 

- O arquivo será exibido na tela de visualização de arquivos do contrato. 

- Através da coluna "Origem" é possível verificar se o documento foi enviado a partir do dispositivo local ou se foi realizada vinculação pelo Super ou SEI. 

- A coluna Arquivos armazena a Descrição do documento. Observe que, no caso do Super (ou SEI), são exibidas tanto a descrição do documento constante no processo do SEI (incluindo seu número de referência dentro do processo), quanto a descrição informada pelo usuário no ato da vinculação. Caso queira visualizar os arquivos, basta clicar sobre o link. 

Figura 36 – Visualização do arquivo SEI/SUPER no sistema 

33 | 183

<!-- pagina 34 -->
- Para alterar o arquivo de Público para Restrito para que não seja exibido no módulo transparência ou no PNCP, clique no botão “ ” - “Alterar status do documento para restrito”. O ícone será alterado para “ ”- “Alterar status do documento para público”. 

Figura 37 – Alteração do status para público ou restrito 

- Para excluir um vínculo de arquivo, clique no ícone “ ” - Excluir. 

**C) CRONOGRAMA** 

Para visualizar o Cronograma do contrato, selecione o contrato desejado, clique no ícone e em “Cronograma”. 

Serão exibidas as parcelas do contrato geradas a partir do Contrato e seus Termos. 

O somatório das parcelas existentes no Cronograma do contrato reflete o Valor Acumulado do contrato. 

Caso deseje visualizar detalhes de uma parcela do cronograma, clique no ícone . 

Uma nova parcela do Cronograma poderá ser inserida clicando em “Adicionar Cronograma Contrato”. 

Figura 38 – Cronograma do Contrato 

Preencha os campos indicados: 

34 | 183

<!-- pagina 35 -->
- “Instrumento – Número (Histórico)”: selecione a qual termo contratual a parcela inserida se refere; 

- “Mês Referência”; 

- “Ano Referência”; 

- “Vencimento”; 

- “Soma ou Subtrai?”; 

- “Valor”: valor da parcela; 

- “Retroativo”. 

Após preenchidos todos os campos, clique em “Salvar e voltar”. 

Os campos marcados com * são de preenchimento obrigatório. 

Figura 39 – Cronograma do Contrato – Adicionar Parcela 

Para editar uma parcela do Cronograma, localize a parcela e clique no ícone . Altere os campos desejados e clique em “Salvar e voltar”. 

Figura 40 – Cronograma do Contrato – Editar Parcela 

Para excluir uma parcela do Cronograma, localize a parcela e clique no ícone . 

35 | 183

<!-- pagina 36 -->
Figura 41 – Cronograma do Contrato – Excluir Parcela 

# **D) DESPESAS ACESSÓRIAS** 

Para adicionar Despesas Acessórias ao contrato, selecione o contrato desejado, clique no ícone e em “Despesas Acessórias”. 

Despesas Acessórias são despesas decorrentes do contrato, mas que não compõe o valor contratual. Como exemplo, temos o IPTU. É uma despesa de obrigação do locatário, mas que seu valor não compõe o valor do contrato. 

Para incluir, clique em “Adicionar Despesa Acessória”. 

Figura 42 – Despesas Acessórias 

Preencha os campos indicados: 

- “Tipo Despesa”: pode ser dos tipos condomínio, garantia estendida, seguro, taxa ou tributo; 

- “Recorrência Despesa”: anual, mensal ou única; 

- “Descrição Complementar”; 

- “Vencimento”; 

- “Valor”. 

36 | 183

<!-- pagina 37 -->
Após preenchidos todos os campos, clique em “Salvar e voltar”. 

Os campos marcados com “*” são de preenchimento obrigatório. 

Figura 43 – Adicionar Despesa Acessória 

Para editar uma Despesa Acessória, localize a despesa e clique no ícone . 

Altere os campos desejados e clique em “Salvar e voltar”. 

Figura 44 – Editar Despesa Acessória 

Para excluir uma Despesa Acessória, localize a despesa e clique no ícone . 

Figura 45 – Excluir Despesa Acessória 

**E) EMPENHOS** 

Para adicionar Empenhos ao contrato, selecione o contrato desejado, clique no ícone e em “Empenhos”. 

37 | 183

<!-- pagina 38 -->
Serão exibidos os empenhos já adicionados ao contrato, sejam os vinculados automaticamente pelo sistema (ao inserir a minuta de empenho ao adicionar um novo Contrato ou ao emitir uma minuta de empenho do tipo Contrato) ou aquelas vinculadas individualmente, como explicado a seguir. 

Caso queira adicionar novo Empenho, clique em “Adicionar Empenho do Contrato”. 

Figura 46 – Empenhos Contrato 

Preencha os campos indicados: 

- “Unidade Emitente do Empenho”: é possível selecionar empenhos realizados por outra unidade, desde que ela esteja vinculada como unidade descentralizada do contrato (para adicionar uma unidade descentralizada ao contrato, seguir as orientações constante no item 3.1.3, alínea “L” deste Manual) ou unidade executora cadastrada nas configurações da unidade não-SISG. 

- “Favorecido”: fornecedor contratado; 

- “Empenho”: após selecionar a unidade emitente e o favorecido, é preciso digitar pelo menos 4 caracteres para que sejam exibidos todos os empenhos emitidos para o favorecido na unidade que ainda não tenham sido vinculados a outros contratos, sejam decorrentes de Minutas de Empenho realizadas no próprio sistema Contratos.gov.br, bem como de empenhos emitidos diretamente no SIAFI pelas unidades executoras ou sistemas financeiros externos. Caso o empenho não apareça na lista, é necessário digitar o número completo do empenho no campo, ex.: 2023NE000001, pois alguns não são listados automaticamente. 

Após preenchidos todos os campos, clique em “Salvar e voltar”. 

Os campos marcados com * são de preenchimento obrigatório. 

38 | 183

<!-- pagina 39 -->
Figura 47 – Adicionar Empenhos do Contrato 

Figura 48 – Escolher a Unidade do Empenho para contratos com Unidades Descentralizadas cadastradas 

Para editar um Empenho, localize o Empenho e clique no ícone . Altere os campos desejados e clique em “Salvar e voltar”. 

Figura 49 – Alterar Empenhos do Contrato 

Para excluir um Empenho, localize o Empenho e clique no ícone 

A exclusão do Empenho não implica na anulação do seu saldo, apenas seu registro no sistema para aquele contrato. 

A edição e exclusão de empenhos vinculados automaticamente ou que estejam vinculados a algum Instrumento de Cobrança não são permitidas. 

39 | 183

<!-- pagina 40 -->
Figura 50 – Excluir Empenhos do Contrato 

# **F) GARANTIAS** 

Para adicionar Garantias ao contrato, selecione o contrato desejado, clique no ícone e em “Garantias”. 

Serão exibidas as garantias já adicionadas ao contrato. 

Para adicionar uma nova garantia, clique em “Adicionar Garantia do Contrato”. 

Figura 51 – Adicionar Garantia do Contrato 

Preencha os campos indicados: 

- “Tipo”: selecione o tipo de garantia apresentada pela empresa (depósito caução, fiança bancária, seguro garantia ou título da dívida pública); 

- “Valor”: informe o valor da garantia; 

- “Vencimento”: data de vencimento da garantia. 

Após preenchidos todos os campos, clique em “Salvar e voltar”. 

Os campos marcados com “*” são de preenchimento obrigatório. 

Figura 52 – Adicionar Garantia do Contrato 

40 | 183

<!-- pagina 41 -->
Para editar uma Garantia, localize a Garantia e clique no ícone . 

Altere os campos desejados e clique em “Salvar e voltar”. 

Figura 53 – Editar Garantia do Contrato 

Para excluir uma Garantia, localize a Garantia e clique no ícone 

Figura 54 – Excluir Garantia do Contrato 

# **G) HISTÓRICO** 

Para consultar o Histórico do contrato, selecione o contrato desejado, clique no ícone e em “Histórico”. 

Serão exibidas informações básicas acerca do Contrato e todos os Termos já celebrados. 

Figura 55 – Histórico do Contrato 

41 | 183

<!-- pagina 42 -->
# **H) ITENS** 

Para consultar os Itens do contrato, selecione o contrato desejado, clique no ícone e em “Itens”. Serão exibidos todos os itens contratados. 

Figura 56 – Itens 

# **I) PARÂMETROS** 

Essa funcionalidade permite o acompanhamento dos prazos para recebimento provisório e definitivo das entregas feitas pelo fornecedor ou comunicadas pela fiscalização. Além disso, é por meio dela que se realiza a indicação quanto à obrigatoriedade ou não da Ordem de Serviço ou de Fornecimento (OS/F), para o contrato, bem como da assinatura do preposto. Para sua correta informação e registro no sistema, deve ser analisado o contrato, edital, aviso de contratação direta ou normativo que defina esses prazos e requisitos para a contratação. 

Figura 57 – Exemplo de como fica o acompanhamento das entregas do objeto quando está cadastrado o 

parâmetro do contrato e quando não está. 

42 | 183

<!-- pagina 43 -->
# **Criação automática de parâmetros do contrato** 

Quando o contrato não possuir parâmetros previamente cadastrados, estes serão **gerados automaticamente** quando o usuário **criar ou informar uma OS/F** . Nessa situação, o sistema atribuirá os seguintes valores padrão: 

**Obrigatório registro de OS/F:** Sim; **Assinatura do preposto obrigatória na OS/F:** Não; **Prazo para recebimento provisório:** 10 (dez) dias úteis; **Prazo para recebimento definitivo:** 10 (dez) dias úteis. 

Para adicionar Parâmetros ao Contrato, selecione o contrato desejado, clique no ícone e em “Parâmetros”. 

Serão exibidos todos os parâmetros já cadastrados. 

Para adicionar um novo Parâmetro, clique em “Adicionar Parâmetro Contrato”. 

Figura 58 – Parâmetros 

Preencha os campos indicados: 

- “Prazo para recebimento provisório”: escolher entre quantidade de dias úteis ou corridos; 

- “Prazo para recebimento definitivo”: escolher entre quantidade de dias úteis ou corridos; 

- “Prazo para pagamento”: escolher entre quantidade de dias úteis ou corridos; 

- “Data de pagamento recorrente”: preencher apenas no caso de ter um vencimento fixo para aquele contrato (ex.: energia elétrica); 

- “Obrigatório registro de OS/F”: informar se aquele contrato prevê que a execução se dê por meio de Ordem de Serviço/Fornecimento ou não. 

- “A assinatura do preposto é obrigatória na OS/F?”: permite indicar se a assinatura do preposto é requisito obrigatório para que a OS/F entre em execução. 

Após preenchidos todos os campos, clique em “Salvar e voltar”. 

Os campos marcados com “*” são de preenchimento obrigatório. 

43 | 183

<!-- pagina 44 -->
Figura 59 – Adicionar Parâmetros 

**J) PREPOSTOS** 

Para adicionar Prepostos do Contrato, selecione o contrato desejado, clique no ícone e em “Prepostos”. 

Serão exibidos todos os prepostos já cadastrados. 

Para adicionar um novo Preposto, clique em “Adicionar Preposto do Contrato”. 

Figura 60 – Prepostos 

Preencha os campos indicados na aba “Dados Preposto”: 

- “CPF” 

- “Nome Completo” 

- “E-mail” 

- “Telefone Fixo” 

- “Celular” 

Na aba “Outras informações”: 

- “Doc. Formalização” 

- “Inform. Complementar” 

- “Data Início” 

- “Data Fim” 

- “Situação”: ativo ou inativo 

44 | 183

<!-- pagina 45 -->
Após preenchidos todos os campos, clique em “Salvar e voltar”. 

Os campos marcados com * são de preenchimento obrigatório. 

Figura 61 – Adicionar Prepostos – aba Dados Preposto 

Figura 62 – Adicionar Prepostos – aba Outras Informações 

Para editar um Preposto, localize o Preposto e clique no ícone . Altere os campos desejados e clique em “Salvar e voltar”. 

Figura 63 – Editar Prepostos 

Para excluir um Preposto, localize o Preposto clique no ícone 

Caso o preposto tenha sido substituído, a recomendação é que seu cadastro seja editado para incluir a Data fim e colocado a Situação Inativo. 

45 | 183

<!-- pagina 46 -->
Figura 64 – Excluir Prepostos 

# **K) PUBLICAÇÕES DOU** 

Para visualizar as Publicações já realizadas do Contrato, selecione o contrato desejado, clique no ícone e em “Publicações”. 

Serão exibidas todas as publicações já realizadas. 

As publicações a serem realizadas pelo Contratos.gov.br são referentes a publicações de Contratos, Termos Aditivos, Termos de Apostilamento, Termos de Extinção, Relatório Final e suas retificações. 

Publicações de penalidades contratuais devem ser realizadas diretamente na Imprensa Nacional e não pelo Contratos.gov.br. 

Sugerimos que a adição de nova publicação deve ser realizada em último caso. Quando da inclusão de contratos e respectivos termos, já serão criadas suas publicações, desde que a data de publicação informada seja um dia útil posterior à data atual da inclusão. Para retificações de publicações, altere as informações do contrato ou termo que será criada uma publicação de retificação automaticamente. 

Para adicionar uma nova Publicação, clique em “Adicionar Publicação”. 

Figura 65 – Publicações 

Preencha os campos indicados: 

- “Data Publicação”: data da publicação devendo ser dia útil posterior a data atual; 

- “Instrumento”: selecione qual instrumento se refere a publicação; 

- “Texto DOU”: deverá ser preenchida com texto em formato padrão: 

##ATO EXTRATO DE (TIPO CONTRATO/TERMO) Nº (NÚMERO CONTRATO/TERMO) – UASG (NÚMERO DA UNIDADE) 

Nº Processo: (Número processo) 

<u>##TEX (Modalidade Compra) Nº (Número licitação). Contratante: (Nome da UASG).</u> 

46 | 183

<!-- pagina 47 -->
Contratado: (CNPJ do contratado). Objeto: (Objeto do contrato/termo). Fundamento Legal: (Fundamento Legal da Contratação). Vigência: (xx/xx/xxxx a xx/xx/xxxx). Valor Total: R$ (valor total contrato/termo). Data de Assinatura: (xx/xx/xxxx). 

##OFI (COMPRASNET 4.0 – xx/xx/xxxxx (Data assinatura do contrato/termo) 

- “CPF”: usuário deve ter habilitação na Imprensa Nacional para publicar na unidade; 

- “Status”: Deixe A PUBLICAR. 

Após preenchidos todos os campos, clique em “Salvar e voltar”. 

Os campos marcados com “*” são de preenchimento obrigatório. 

Datas retroativas ou atual não geram publicação na Imprensa Nacional. 

Figura 66 – Adicionar Publicações 

A “Situação Publicação” estará com status “A PUBLICAR”. 

A “Situação Imprensa” estará com status “PENDENTE”. 

A publicação não mais é enviada automaticamente, logo o usuário precisa enviar manualmente, 

clicando no ícone . 

A “Situação Publicação” ficará com status “TRANSFERIDO PARA IMPRENSA” e a “Situação Imprensa” ficará com status “EM EDITORACAO”. 

Após a publicação, os status serão alterados para “PUBLICADO” e “PUBLICADA”, respectivamente. 

É possível atualizar os status da publicação por meio do ícone . 

Para editar uma Publicação, localize a Publicação e clique no ícone . 

Apenas Publicações com status “A PUBLICAR” ou “ERRO” poderão ser editadas. 

Altere os campos desejados e clique em “Salvar e voltar”. 

47 | 183

<!-- pagina 48 -->
Figura 67 – Editar Publicações 

Para excluir uma Publicação, localize a Publicação e clique no ícone . Apenas Publicações com status “A PUBLICAR” ou “ERRO” poderão ser excluídas. 

Figura 68 – Excluir Publicações 

# **L) RESPONSÁVEIS** 

Para visualizar ou adicionar os Responsáveis no Contrato, selecione o contrato desejado, clique no ícone “ ” e em “Responsáveis”. 

Serão exibidos os Responsáveis já alocados no contrato. 

É possível adicionar qualquer usuário da unidade que se está logado, desde que este possua em seu cadastro o perfil Responsável por contrato. Para cadastrar um usuário de uma unidade descentralizada, é necessário que ela esteja adicionada como tal, bem como que o usuário tenha o perfil “Responsável por Contrato” atribuído em seu cadastro. É importante que todos que atuem na gestão e fiscalização contratual tenha esse perfil atribuído, podendo ser feito conforme a orientação dos itens 6.1. e 6.2 deste Manual. Para adicionar uma unidade descentralizada ao contrato, seguir as orientações constante no item 3.1, alínea “L” deste Manual. 

Para adicionar um novo responsável, clique em “Adicionar Responsável do Contrato”. 

48 | 183

<!-- pagina 49 -->
Figura 69 – Responsáveis do Contrato 

Preencha os campos indicados: 

- “Usuário”: selecione o usuário que será atribuído como responsável pelo contrato; 

- “Telefone Fixo” 

- “Telefone Celular” 

- “Função”: selecione a função do usuário no contrato; 

- “Instalação/Unidade” 

- “Portaria”: informe qual a portaria que atribuiu a fiscalização do contrato ao servidor; 

- “Data Início” 

- “Data Fim” 

- “Situação” 

Após preenchidos todos os campos, clique em “Salvar e voltar”. 

Os campos marcados com * são de preenchimento obrigatório. 

Figura 70 – Responsáveis do Contrato 

49 | 183

<!-- pagina 50 -->
Para editar um Responsável, clique no ícone . 

Altere os campos desejados e clique em “Salvar e voltar”. 

Figura 71 – Editar Responsável do Contrato 

Caso deseje substituir um usuário como Responsável, altere seu status para “INATIVO”, informando na Data fim o dia de sua atuação naquele contrato. 

# **M) UNIDADES DESCENTRALIZADAS** 

A descentralização do contrato permite que outras unidades que sejam atendidas por aquele contrato possam emitir empenhos para o contrato, permitindo que os pagamentos sejam realizados diretamente nessas unidades. Também é possível vincular responsáveis por contratos de outras unidades com a descentralização, desde que o usuário da unidade descentralizada possua em seu perfil a opção “Responsável por contratos”. Quando a unidade emite empenho para o contrato, o total empenhado é apresentado na tela. 

Para descentralizar um contrato para outras unidades, selecione o contrato desejado, clique no ícone e em “Unidades Descentralizadas”. 

Clique em “Adicionar Unidades”. 

Figura 72 – Unidades Descentralizadas 

Selecione a unidade para qual deseja descentralizar o contrato. 

Clique em “Salvar e Voltar”. 

50 | 183

<!-- pagina 51 -->
Figura 73 – Incluir Unidades Descentralizadas 

Para excluir uma Unidade Descentralizada, clique no ícone . 

Figura 74 – Excluir Unidades Descentralizadas 

**N) INSTRUMENTOS DE COBRANÇA (FATURAS)** 

Ao acessar o menu Gestão Contratual > Ações > Instrumento de Cobrança, o usuário é direcionado para a tela de cadastro do Instrumento de cobrança do contrato. Disponível também em: <u>https://contratos.sistema.gov.br/meus-contratos</u> (Nova versão). 

Para realizar o cadastro de um único Instrumento de Cobrança (IC) para mais de um contrato do tipo empenho de um mesmo fornecedor, siga os passos abaixo: 

1. Acesse o menu **Gestão Contratual > Contratos** ; 

2. Localize os contratos do tipo empenho do mesmo fornecedor; 

3. Selecione os contratos que deseja cadastrar o Instrumento de Cobrança; 

4. Clique no ícone **“Inserir Instrumento de Cobrança”** , localizado na parte superior da tela; 

5. O sistema irá direcionar automaticamente para a nova versão da tela de registro do Instrumento de Cobrança; 

6. Preencha os dados solicitados e conclua o cadastro. 

**Observação:** A funcionalidade está disponível apenas para contratos do tipo empenho pertencentes ao mesmo fornecedor. 

Figura 75 – Inserir Instrumento de cobrança para mais de um contrato do tipo empenho 

**O) OCORRÊNCIAS** 

Para visualizar as ocorrências cadastradas, selecione o contrato desejado, clique no ícone “ ” e em “Ocorrências”. Serão listadas todas as ocorrências já cadastradas, com possibilidade de detalhar as informações clicando no ícone . 

51 | 183

<!-- pagina 52 -->
Figura 76 – Ocorrências 

As ocorrências podem ser inseridas tanto por usuário Setor Contrato pelo caminho do Gestão Contratual > Contratos > Mais > Ocorrências, quanto pelo usuário vinculado como Responsável pelo Contrato (verificar alínea “K” deste item 3.1.3.) pelo caminho Gestão Contratual > Meus Contratos > Mais > Ocorrências. 

Para cadastrar uma Ocorrência, clique em “Ocorrências” e “Adicionar Ocorrência do Contrato”. 

Figura 77 – Ocorrências 

Preencha os Campos da Ocorrência: 

- “Situação”: qual situação da ocorrência; 

- “Ocorrência Concluída”: se a ocorrência que está sendo incluída ou está concluindo alguma outra ocorrência já cadastrada”; 

- “Nova Situação”: nova situação da ocorrência que está sendo atualizada; 

- “Data”: data da ocorrência; 

- “Ocorrência”: descrição de nova ocorrência ou da conclusão de ocorrência já cadastrada; 

- “Notifica Preposto”: se selecionado SIM, informar o e-mail do preposto e um e-mail será disparado com a descrição da ocorrência; 

- “E-mail preposto” 

- “Arquivos”: caso queira anexar arquivo à ocorrência. 

Após preenchidos todos os dados, clique em “Salvar e voltar”. 

Se todos os dados estiverem preenchidos corretamente, será retornado a tela anterior com a lista de todas as ocorrências cadastradas. 

52 | 183

<!-- pagina 53 -->
Figura 78– Adicionar ocorrência 

Não é permitida a edição de ocorrências já cadastradas. Para alterar a situação de uma ocorrência existente, o usuário deve registrar uma nova ocorrência, informando no campo “Ocorrência concluída” aquela que se deseja atualizar e, no campo “Nova Situação”, o status para o qual a ocorrência foi alterada. 

Ressalta-se que, ao incluir uma nova ocorrência com o objetivo de alterar a situação de outra já registrada, o sistema permite a seleção apenas de ocorrências que estejam com as situações “Atendida parcial” ou “Pendente”. 

Para excluir uma ocorrência, clicar no símbolo 

Figura 79 – Ocorrências do Contrato 

**P) TERCEIRIZADOS** 

Os terceirizados podem ser inseridos tanto por usuário Setor Contratos pelo caminho do **Gestão Contratual > Contratos > Mais > Terceirizados** , quanto pelo usuário vinculado como Responsável pelo Contrato (verificar alínea “K” deste item 3.1.3.) pelo caminho **Gestão Contratual > Meus Contratos > Mais > Terceirizados.** 

Para visualizar os terceirizados cadastrados, selecione o contrato desejado, clique no ícone e em “Terceirizados”. Serão listados todos os terceirizados já cadastrados, com possibilidade de detalhar as informações de cada funcionário clicando no ícone . 

53 | 183

<!-- pagina 54 -->
Figura 80 – Terceirizados 

Preencha os campos da aba “Dados Pessoais”: 

- “CPF” 

- “Telefone Fixo” 

- “Telefone Celular” 

- “Escolaridade” 

Os campos marcados com “*” são de preenchimento obrigatório. 

Após, clique em “Próxima aba”. 

Figura 81 – Cadastro de Terceirizados – Dados pessoais 

Preencha os campos da aba “Dados Funcionais”: 

- “CBO”: digite ou selecione na lista a classificação brasileira de ocupações; 

- “Descrição”: selecione na lista uma das descrições do CBO selecionado; 

- “Descrição Complementar”: detalhamento da função exercida pelo terceirizado; 

54 | 183

<!-- pagina 55 -->
- “Jornada Semanal”; 

- “Unidade da Prestação do Serviço”; 

- “Salário Mensal Bruto”; 

- “Custo Mensal do Terceirizado”: valor pago pelo posto de trabalho; 

- “Auxílio-Transporte” 

- “Auxílio-Alimentação” 

- “Data Início no Contrato”; 

- “Data Desligamento no Contrato” 

- “Situação” 

Figura 82 – Cadastro de Terceirizados – Dados Funcionais 

Após, clique em “Próxima aba”. 

Preencha os campos da aba “Dependentes”, quando houver. 

Clique em “Adicionar Dependente” e preencha os campos: 

- “CPF” 

- “Reembolso creche” 

- “Amparo Legal” 

- “Valor do benefício” 

55 | 183

<!-- pagina 56 -->
Figura 83 – Cadastro de Terceirizados – Dependentes 

Figura 84 – Cadastro de Terceirizados – Adicionar Dependentes 

Após preenchidas as informações, clique em “Incluir”. 

Para editar um dependente clique em . Para excluir, clique em 

Figura 85 – Cadastro de Terceirizados – Alterações no Dependente 

Após preenchidos todos os dados, clique em “Salvar e voltar”. 

~~Se todos os dados estiverem preenchidos corretamente, será retornado à tela anterior com a lista~~ 

56 | 183

<!-- pagina 57 -->
# de todos os terceirizados cadastrados. 

Os terceirizados poderão ser cadastrados em massa clicando em “Importar planilha preenchida”, desde que utilizada a planilha modelo disponível em “Baixar planilha modelo”: 

Figura 86 – Importação de Terceirizados 

Preencha todos os dados obrigatórios da Planilha Modelo de Terceirizados disponibilizada. 

Figura 87 – Planilha de Terceirizados 

Após preenchidos os dados dos terceirizados, salve a planilha e clique no botão “Importar planilha preenchida”. 

57 | 183

<!-- pagina 58 -->
Figura 88 – Importar planilha preenchida 

Clique em “Escolher arquivos”; 

Selecione a planilha e clique em “salvar” para realizar o cadastro dos terceirizados. 

Figura 89 – Selecionar Planilha de Terceirizados 

**Atenção:** O cadastro do terceirizado só será finalizado se todas as informações exigidas estiverem corretas. Apenas os cadastros validados vão aparecer na listagem. 

Para editar a informação de algum terceirizado ou para alterar sua situação para Inativo em caso de desligamento do funcionário, clique no ícone e para exclusão em caso de registro incorreto, clique no ícone . 

58 | 183

<!-- pagina 59 -->
Figura 90 – Ações em terceirizados do Contrato 

**Q) INSTRUMENTO INICIAL** 

Para editar os dados do contrato cadastrado, selecione o contrato desejado, clique no ícone e em “Instrumento Inicial”. 

Para editar o Instrumento Inicial, clique no ícone . 

Altere os dados desejados e clique em “Salvar e Voltar”. 

Figura 91 – Instrumento Inicial 

# **R) TERMO ADITIVO** 

Primeiro passo é realizar a pesquisa do contrato desejado. 

Na tabela de contratos serão apresentados os resultados da pesquisa. 

Figura 92 - Pesquisa de Contratos 

Para adicionar o Termo Aditivo ao cadastro do contrato, clique no ícone e em “Termo Aditivo”. 

59 | 183

<!-- pagina 60 -->
Figura 93 – Inclusão de Termo Aditivo 

Será apresentada a tela para realização do cadastro. Para adicionar um Termo Aditivo clique em “Adicionar Termo Aditivo”. 

Figura 94 - Inclusão de Termo Aditivo 

Preencha os campos dos dados solicitados e clique em Próxima Aba: Dados Gerais 

- “Qualificação”: serão exibidos tipos de qualificações do Termo Aditivo conforme seu objeto, podendo ser selecionado mais de um: 

   - a. ACRÉSCIMO/SUPRESSÃO: acréscimos ou supressões no contrato obedecidos os limites legais; 

   - b. VIGÊNCIA: prorrogação de contratos; 

   - c. FORNECEDOR: mudança de CNPJ ou alteração do prestador de serviços; 

   - d. REAJUSTE: reajuste dos valores contratados; 

   - e. INFORMATIVO: alteração de cláusula contratual. 

- “Deseja gerar cronograma automático para o Contrato?”: Quando marcada a opção “Sim” será gerado o cronograma considerando as informações a serem preenchidas na aba “Vigência/Valores”. Quando marcada opção “Não” será necessário incluir em Contratos > + (Engrenagem) > Cronograma > + Adicionar Cronograma Contrato, para que a informação valor acumulado do contrato fique correta. 

- “Número Termo Aditivo”: preencher no formato xxxxx/20xx. 

- “Objeto do TA”: inserir o objeto do Termo Aditivo. 

Os campos marcados com * são de preenchimento obrigatório. 

60 | 183

<!-- pagina 61 -->
<!-- Start of picture text -->
Figura 95 - Dados Gerais<br><!-- End of picture text -->

Figura 96 – Qualificação em Dados Gerais 

Preencha os campos dos dados solicitados e clique em Próxima Aba: Dados Aditivo 

- “Data Assinatura Aditivo”: data em que o TA foi assinado; 

- “Data Publicação Aditivo”: caso seja necessário publicação na Imprensa Nacional, deve ser inserida data posterior à data atual. Pode ser inserida a data de divulgação no PNCP, para contratos da Lei 14.133, o que ocorre no dia de registro do termo; 

- “Informações Complementares”: poderá ser preenchido caso haja alguma especificidade no documento. 

Caso tenha sido selecionada a qualificação “FORNECEDOR”, será permitido realizar a alteração do Fornecedor. Os campos marcados com * são de preenchimento obrigatório. 

Figura 97 - Dados Aditivo 

61 | 183

<!-- pagina 62 -->
A depender da qualificação escolhida, os campos serão habilitados. 

- “Quantidade”: “ACRÉSCIMO/SUPRESSÃO”; 

- “Valor unitário”: “REAJUSTE”; 

- “Qtde. parcelas”: “ACRÉSCIMO/SUPRESSÃO”. 

Figura 98 - Itens do contrato 

Os campos estarão disponíveis independente da qualificação escolhida. Contudo, apenas a qualificação VIGÊNCIA altera a Data Vig. Fim do contrato. 

- “Data Vig. Início”: data início estabelecida no TA, que deverá ser igual ou posterior à data de assinatura. Eventual efeito retroativo do reajuste deverá ser registrado na próxima aba “Retroativo”; 

- “Data Vig. Fim”: data vigência fim estabelecida no TA; 

- “Data Início Novo Valor” 

- “Número Parcelas”: número de parcelas estabelecidas na vigência informada. 

É importante ressaltar que a lógica estabelecida no termo original, seja ela qual for, não pode ser alterada no cadastrado das prorrogações. Ou seja, se for utilizado o critério de contrato data a data ou data a d-1 ou d+1, isso deve ser mantido nos aditivos. 

Os campos marcados com * são de preenchimento obrigatório. 

Figura 99 - Dados Vigência/Valores 

Os campos estarão disponíveis para edição apenas se a qualificação escolhida para o TA tenha sido “REAJUSTE”. 

- “Retroativo”: se houver retroativo a ser pago, selecionar a opção “SIM”; caso contrário, “NÃO”; 

62 | 183

<!-- pagina 63 -->
- “Mês Referência De”: mês inicial do retroativo; 

- “Ano Referência De”: ano inicial do retroativo; 

- “Mês Referência Até”: mês final do retroativo; 

- “Ano Referência Até”: ano final do retroativo; 

- “Vencimento Retroativo”: data de vencimento do valor retroativo a ser pago; 

- “Soma ou Subtrai”: informar se o valor retroativo será somado ou subtraído; 

- “Valor Retroativo”: valor total do retroativo para o período informado. 

Quando todos os campos estiverem preenchidos, clique em “Salvar e voltar”. 

Se todos os dados estiverem preenchidos corretamente, você será redirecionado para a tela de “Publicações”. 

Figura 100 – Dados Retroativo 

Após a inclusão do Termo Aditivo, é criada uma Publicação que será encaminhada automaticamente ao DOU no final do dia ou poderá ser enviada pelo usuário, caso tenha sido informada uma data futura útil no campo “Data Publicação”. 

Através da coluna “Ações”, o usuário poderá: 

- “Enviar Publicação” 

- “Atualizar Situação Imprensa” 

- “Visualizar” 

- “Editar” 

- “Deletar Publicação” 

ATENÇÃO: Publicações que estejam com a Situação Imprensa “PUBLICADA” não poderão ser deletadas e o padrão do texto do modelo não deve ser alterado, caso contrário o sistema da Imprensa Nacional não aceitará o extrato enviado. 

63 | 183

<!-- pagina 64 -->
Figura 101 – Publicações 

**S) TERMO DE APOSTILAMENTO** 

Pesquise pelo contrato desejado, clique no ícone e depois em “Termo de Apostilamento”. Clique em “Adicionar Termo de Apostilamento”. 

Figura 102 – Inclusão de Termo de Apostilamento 

Preencha os campos dos dados solicitados e clique em Próxima Aba: Dados Gerais 

- “Número Termo Apostilamento”: preencher no formato xxxxx/20xx; 

- “Data Assinatura Apostilamento”: data em que o termo de apostilamento foi assinado; 

- “Data da Publicação”: caso seja necessária publicação na Imprensa Nacional, deve ser inserida data posterior à data atual; 

- “Objeto do Apostilamento”: informar o objeto do Termo de Apostilamento; 

- “Unidade Gestora”: campo vem preenchido com a unidade gestora responsável pelo contrato. 

Os campos marcados com * são de preenchimento obrigatório. 

Figura 103 – Dados Gerais 

~~A aba~~ " ~~Vigência~~ " ~~deve ser preenchida exclusivamente nos casos de prorrogação automática~~ 

64 | 183

<!-- pagina 65 -->
previstos no art. 111 e no art. 115, § 5º, da Lei nº 14.133/2021. 

Preencha os campos dos dados solicitados e clique em Próxima Aba: Itens do Contrato 

- Os campos "Data Início de Vigência do Contrato" e "Data Fim de Vigência do Contrato" são exibidos bloqueados, trazendo as datas de vigência atuais do contrato; 

- “Data início de vigência do termo”: informe a nova data de início da prorrogação. Essa data não pode ser anterior à data de fim de vigência atual do contrato; 

- “Data fim de vigência do termo”: informe a nova data de término da prorrogação. Essa data deve ser posterior à data de fim de vigência atual do contrato. 

Figura 104 – Vigência 

Na próxima aba, preencha o novo Valor Unitário reajustado. 

Importante: Esta aba não estará disponível caso, na aba anterior "Vigência", tenha sido indicada a aplicação da prorrogação automática. Portanto, não é permitido registrar no mesmo termo de 

65 | 183

<!-- pagina 66 -->
apostilamento as qualificações de reajuste e prorrogação automática. Cada termo deve ser cadastrado com uma única finalidade. 

Figura 105 – Itens do Contrato 

Preencha os campos dos dados solicitados e clique em Próxima Aba: Valores 

Importante: Esta aba não estará disponível caso, na aba anterior "Vigência", tenha sido indicada a aplicação da prorrogação automática. Portanto, não é permitido registrar no mesmo termo de apostilamento as qualificações de reajuste e prorrogação automática. Cada termo deve ser cadastrado com uma única finalidade. 

- “Deseja gerar cronograma automático para o Contrato?”: Quando marcada a opção “Sim” será gerado o cronograma considerando as informações a serem preenchidas na aba “Valores”. Quando marcada opção “Não”, será necessário incluir em Contratos > + (Engrenagem) > Cronograma > + Adicionar Cronograma Contrato, para que a informação valor acumulado do contrato fique correta. 

- “Data Início Novo Valor”: início do novo valor reajustado; 

- “Data Fim Novo Valor”: fim do novo valor reajustado. 

ATENÇÃO: Caso o campo “Data Fim Novo Valor” não seja preenchido, o sistema considerará que o reajuste se aplicará até a vigência fim atual do contrato. 

Os campos marcados com * são de preenchimento obrigatório. 

66 | 183

<!-- pagina 67 -->
Figura 106 – Valores 

Preencha os campos com os dados solicitados: Retroativo 

Importante: Esta aba não estará disponível caso, na aba anterior "Vigência", tenha sido indicada a aplicação da prorrogação automática. Portanto, não é permitido registrar no mesmo termo de apostilamento as qualificações de reajuste e prorrogação automática. Cada termo deve ser cadastrado com uma única finalidade. 

- “Retroativo”: se houver retroativo a ser pago, selecionar a opção “SIM”; caso contrário, “NÃO”; 

- “Mês Referência De”: mês inicial do retroativo; 

- “Ano Referência De”: ano inicial do retroativo; 

- “Mês Referência Até”: mês final do retroativo; 

- “Ano Referência Até”: ano final do retroativo; 

- “Vencimento Retroativo”: data de vencimento do valor retroativo a ser pago; 

- “Soma ou Subtrai”: informar se o valor retroativo será somado ou subtraído; 

- “Valor Retroativo”: valor total do retroativo para o período informado. 

Quando todos os campos estiverem preenchidos, existe a possibilidade de Salvar Termo ou Salvar Rascunho. 

Se todos os dados estiverem preenchidos corretamente e seja clicado “Salvar Termo”, você será redirecionado para a tela de “Publicações”. 

Os campos marcados com “*” são de preenchimento obrigatório. 

67 | 183

<!-- pagina 68 -->
Figura 107 – Retroativo 

Após a inclusão do Termo de Apostilamento em “Salvar Termo”, caso a data de publicação seja posterior à data atual, é criada uma Publicação que será encaminhada automaticamente ao DOU no final do dia ou poderá ser enviada pelo usuário. 

Através da coluna “Ações”, o usuário poderá: 

- “Enviar Publicação” 

- “Atualizar Situação Imprensa” 

- “Visualizar” 

- “Editar” 

- “Deletar Publicação” 

**ATENÇÃO** : Publicações que estejam com a Situação Imprensa “PUBLICADA” não poderão ser deletadas. 

Figura 108 – Publicações 

Também é possível salvar um termo de apostilamento como rascunho do registro a ser feito ou finalizado posteriormente, não tendo impacto nas outras funcionalidades do sistema, nem 

68 | 183

<!-- pagina 69 -->
disponibilizado no ambiente de “Transparência”. Nessa situação, os campos “data de assinatura” e “data de publicação” não são obrigatórios. 

Para ativar um termo de apostilamento salvo como rascunho, pode-se editar o documento no ícone 

, ir até a última aba e clica em “Salvar Termo” ou por meio do ícone , onde será obrigatório o preenchimento das datas de assinatura e publicação. Sendo uma data de publicação posterior à data atual, será gerada uma publicação automaticamente. Uma vez salvo o apostilamento com a situação “ativo”, não será possível voltar como “rascunho”. 

Figura 109 – Ativar Termo de Apostilamento 

Figura 110 – Tela de confirmação ou preenchimento ao ativar termo de apostilamento 

**T) TERMO DE EXTINÇÃO** 

**IMPORTANTE:** Alteração de nomenclatura no sistema 

A partir de 11/09/2025, a nomenclatura “Termo de Rescisão” foi atualizada para “Termo de Extinção”. Essa alteração visa alinhar a terminologia do sistema às disposições da Lei nº 14.133/2021, considerando que a rescisão representa apenas uma das hipóteses de extinção contratual previstas na legislação. Importante destacar que não houve alterações de funcionalidade, limitando-se a uma atualização de nomenclatura. 

Pesquise pelo contrato desejado, clique no ícone e depois em “Termo de Extinção”. 

Clique em “Adicionar Termo de Extinção”. 

69 | 183

<!-- pagina 70 -->
Figura 111 – Adicionar Termo de Extinção 

Preencha as informações referentes ao Termo de Extinção: 

- “Observação”: objeto do Termo de Extinção; 

- “Número Processo”: número processo SEI ou sistema correspondente; 

- “Data Assinatura Extinção”: data em que a extinção foi assinada; 

- “Data Publicação”: caso deseje publicar na Imprensa Nacional, deve ser inserida data posterior à data atual e dia útil; 

- “Data Vig. Fim”: data fim de vigência do contrato com a extinção. 

Após todos os dados preenchidos, clique em “Salvar e voltar”. 

Se todos os dados estiverem preenchidos corretamente, você será redirecionado para a tela de “Publicações”. 

Os campos marcados com * são de preenchimento obrigatório. 

Figura 112 – Termo de Extinção 

# **U) RELATÓRIO FINAL** 

Para adicionar o Relatório Final em um contrato, esse precisa ter finalizada sua vigência ou ter Termo de Extinção registrado, bem como um Responsável do contrato vinculado (verificar o item 3.1.3 alínea “K” deste Manual). 

Pesquise pelo contrato desejado, clique no ícone e depois em “Relatório Final”. 

70 | 183

<!-- pagina 71 -->
# Clique em “Adicionar Relatório Final”. 

Figura 113 – Adicionar Relatório Final 

# Preencha as informações referentes ao Relatório Final: 

   1. Confirmar ou alterar o Número do Processo; 

   2. Preencher o campo “Data Encerramento do Contrato” com a data efetiva de seu encerramento. Após, informar a existência/inexistência de pendências administrativas e/ou financeiras respondendo as perguntas que seguem: 

      - 2.1. O objeto contratual foi entregue à Contratante em sua totalidade? 

      - 2.2. Foram cumpridas todas as obrigações financeiras junto à Contratada? 

         - 2.2.1. Caso seja marcada a opção “não” os campos “Saldo disponível ou bloqueado” e “Justificativa de não cumprimento das obrigações financeiras junto à Contratada” serão também de preenchimento obrigatório. 

      - 2.3. Valor total executado 

      - 2.4. Valor total pago 

      - 2.5. O saldo remanescente dos recursos depositados na Conta-Depósito Vinculada foi liberado para o Fornecedor até o encerramento do contrato? 

         - 2.5.1. Caso seja marcada a opção “não” os campos “Saldo bloqueado” e “Justificativa de bloqueio da Conta-Depósito Vinculada”” serão também de preenchimento obrigatório. 

      - 2.6. A garantia contratual foi integralmente devolvida para a Contratada? 

         - 2.6.1. Caso seja marcada a opção “não” os campos “Saldo bloqueado” e “Justificativa de bloqueio da garantia contratual” serão também de preenchimento obrigatório. 

      - 2.7. Marcar qual o grau de satisfação com o desempenho do contrato dentre as opções prédefinidas. 

      - 2.8. Responder se a necessidade formalizada no Planejamento da Contratação (DOD/DFD/ETP/TR/PB) foi plenamente atendida pelo contrato. 

   3. Preencher, caso sejam necessários, os campos: 

      - 3.1. “Consecução dos objetivos da contratação”: inserir evidências e observações sobre a consecução dos objetivos que tenham justificado a contratação, inclusos nos documentos de Planejamento da Contratação; 

      - 3.2. “Sugestões/Lições aprendidas”: inserir eventuais condutas a serem adotadas para o aprimoramento das atividades da Administração; 

      - 3.3. “Observação”: com alguma particularidade relacionada ao contrato que está sendo encerrado (não obrigatório); 

4. Signatário: serão relacionados os usuários cadastrados como responsáveis por contrato (ver item 3.1.3 alínea “K” deste Manual). 

Após todos os dados preenchidos, clique em “Salvar e voltar”. 

71 | 183

<!-- pagina 72 -->
**ATENÇÃO** : Após registrado o Relatório Final, não será mais possível criar minuta de empenho a partir daquele contrato, nem adicionar Instrumento de Cobrança. Ou seja, o Relatório Final é a ação final de um contrato. Então, certifique-se de que nenhuma ação será necessária antes de registrá-lo. 

O contrato não mais será exibido na lista de contratos ativos da unidade. 

Os campos marcados com * são de preenchimento obrigatório. 

Figura 114 – Relatório Final 

Acessando o menu **Gestão Contratual > Contratos** , são exibidos todos os contratos vigentes na unidade. A princípio, só são exibidos contratos cujo status esteja ATIVO. Para exibir contratos INATIVOS, RESCINDIDOS e ENCERRADOS, basta clicar na coluna Situação e selecionar as situações desejadas. 

72 | 183

<!-- pagina 73 -->
Figura 115 – Contratos 

Após salvar o Relatório Final, é possível realizar algumas ações, como: Gerar PDF, Visualizar, Editar e Excluir. 

Figura 116 – Ações do Relatório Final 

# **V) EXCLUSÃO DE CONTRATO** 

A funcionalidade de exclusão de contrato está disponível exclusivamente para o perfil “Setor Contratos”, Administrador. 

**IMPORTANTE!** A exclusão de um contrato é irreversível. Ao realizar a exclusão, a publicação do contrato será automaticamente removida do PNCP. No caso de contratos publicados no Diário Oficial da União (DOU), não haverá qualquer ação automática. Caberá ao usuário avaliar a necessidade de providenciar, junto à Imprensa Nacional, a publicação de uma matéria referente à exclusão do contrato. 

Pesquise pelo contrato desejado, clique no ícone e depois em “Excluir Contrato”. 

73 | 183

<!-- pagina 74 -->
Figura 117 – Funcionalidade de Excluir contrato 

Será habilitado um campo de justificativa. Preencha com as informações e clique em “ Salvar e Excluir”. Não havendo impedimentos, o contrato será excluído. 

Figura 118– Justificativa para exclusão de contrato 

A exclusão de contratos ativos não será permitida caso exista qualquer um dos seguintes registros vinculados ao contrato: 

- Entregas 

- Ordens de serviço ou de fornecimento 

- Declaração vinculada ao Decreto nº 11.430/2023 

- Antecipação de recebíveis do AntecipaGov ou domicílio bancário 

- Minuta do tipo “Contrato” 

- Instrumento de Cobrança 

- Apropriação de Instrumento de Cobrança 

- ~~Termo aditivo~~ 

74 | 183

<!-- pagina 75 -->
- Termo de apostilamento 

- 

- 

- Termo de extinção 

- Relatório final 

# 3.2 – Fornecedores 

Acessando o menu **Gestão Contratual > Fornecedores** , são exibidos todos os fornecedores cadastrados no Contratos.gov.br. 

Para pesquisar um fornecedor, clique no campo “Pesquisar” e informe os dados (CPF/CNPJ/UG/ID Genérico ou Nome/Razão Social). 

Caso o fornecedor não seja localizado, este pode ser incluído clicando em “Adicionar Fornecedor”, desde que o usuário possua o perfil Setor Contratos. 

Figura 119 – Adicionar Fornecedor 

Preencha os campos indicados: 

- “Tipo Fornecedor”: Pessoa Física, Pessoa Jurídica, UG Siafi (quando o fornecedor for um órgão da Administração) e ID Genérico (para empresas estrangeiras que não possuem CNPJ); 

- “CPF/CNPJ/UG/ID Genérico”; 

- “Nome”. 

Após todos os dados preenchidos, clique em “Salvar e voltar”. 

Os campos marcados com * são de preenchimento obrigatório. 

75 | 183

<!-- pagina 76 -->
Figura 120 – Salvar novo fornecedor 

É possível consultar a situação do SICAF do fornecedor por meio do ícone . Ao realizar a consulta, caso algum dado do fornecedor esteja incorreto, o sistema atualizará os dados do fornecedor automaticamente. 

Figura 121 – Fornecedores – Consulta ao SICAF 

# 3.3 – Sub-rogações 

Acessando o menu **Gestão Contratual > Sub-rogações** , são exibidas todas as sub-rogações de contratos realizadas pela unidade em seus contratos. 

Para sub-rogar um novo contrato, clique em “Adicionar Sub-rogação”. 

Após um contrato ser sub-rogado, este não estará mais visível na unidade. 

Figura 122 – Sub-rogações 

76 | 183

<!-- pagina 77 -->
Preencha os campos indicados: 

- “Número do Instrumento”: selecione o contrato que será sub-rogado; 

- “Unidade Destino”: informe para qual unidade o contrato está sendo sub-rogado; 

- “Data Termo”. 

Após todos os dados preenchidos, clique em “Salvar e voltar”. 

Os campos marcados com * são de preenchimento obrigatório. 

Figura 123 – Adicionar Sub-rogação 

# 3.4 – Consultas 

Acessando o menu **Gestão Contratual > Consultas** , será apresentado um menu com os tipos de consultas disponíveis: 

- “Arquivos” 

- “Cronogramas” 

- “Despesas Acessórias” 

- “Empenhos” 

- “Instrumentos de Cobrança” 

- “Garantias” 

- “Históricos” 

- “Itens” 

- “Ocorrências” 

- “Prepostos” 

- “Responsáveis” 

- “Terceirizados” 

77 | 183

<!-- pagina 78 -->
Figura 124 – Consultas 

# **A) ARQUIVOS** 

Para consultar um Arquivo, clique no menu **Gestão Contratual > Consultas > Arquivos** . 

Serão exibidos todos os arquivos cadastrados em todos os contratos. 

Os dados poderão ser exportados em “Excel”, “CSV” e “PDF” ou copiados, podendo ser incluídas outras informações por meio de “Visibilidade da coluna”, clicando sobre a(s) informação(ões) que deseja ser(em) exibida(s). 

Para aplicar os filtros existentes, clique em Núm. Contrato, Fornecedor e/ou Tipo e escolha a(s) opção(ões) que deseja ser(em) filtrada(s). 

Para pesquisar um Arquivo, clique no campo “Pesquisar” e informe os dados (Tipo de Arquivo, CPF/CNPJ/UG/ID Genérico, Nome/Razão Social, Objeto, Processo ou Número do instrumento). 

Figura 125 – Arquivos 

**B) CRONOGRAMA** 

Para consultar o Cronograma, clique no menu **Gestão Contratual > Consultas > Cronograma** . 

~~Serão exibidas todas as parcelas do cronograma de todos os contratos.~~ 

78 | 183

<!-- pagina 79 -->
Os dados poderão ser exportados em “Excel”, “CSV” e “PDF” ou copiados, podendo ser incluídas outras informações por meio de “Visibilidade da coluna”, clicando sobre a(s) informação(ões) que deseja ser(em) exibida(s). 

Para aplicar os filtros existentes, clique em Núm. Contrato, Fornecedor, Mês Ref., Ano Ref. e/ou Vencimento e escolha a(s) opção(ões) que deseja ser(em) filtrada(s). 

Para pesquisar um Cronograma, clique no campo “Pesquisar” e informe os dados (Número do Instrumento, CPF/CNPJ/UG/ID Genérico, Nome/Razão Social, Mês Referência ou Ano Referência). 

Figura 126 – Cronograma 

**C) DESPESAS ACESSÓRIAS** 

Para consultar as Despesas Acessórias, clique no menu **Gestão Contratual > Consultas > Despesas Acessórias** . 

Serão exibidas todas as despesas acessórias de todos os contratos. 

Os dados poderão ser exportados em “Excel”, “CSV” e “PDF” ou copiados, podendo ser incluídas outras informações por meio de “Visibilidade da coluna”, clicando sobre a(s) informação(ões) que deseja ser(em) exibida(s). 

Para aplicar os filtros existentes, clique em Núm. Contrato, Fornecedor, Tipo Despesa, Recorrência Despesa e/ou Vencimento e escolha a(s) opção(ões) que deseja ser(em) filtrada(s). 

Para pesquisar uma Despesa Acessória, clique no campo “Pesquisar” e informe os dados (Número do Instrumento, CPF/CNPJ/UG/ID Genérico ou Nome/Razão Social). 

79 | 183

<!-- pagina 80 -->
Figura 127 – Despesas Acessórias 

# **D) EMPENHOS** 

Para consultar os Empenhos, clique no menu **Gestão Contratual > Consultas > Empenhos** . 

Serão exibidos todos os empenhos emitidos na unidade. 

Os dados poderão ser exportados em “Excel”, “CSV” e “PDF” ou copiados, podendo ser incluídas outras informações por meio de “Visibilidade da coluna”, clicando sobre a(s) informação(ões) que deseja ser(em) exibida(s). 

Para aplicar os filtros existentes, clique em Núm. Contrato, Fornecedor, Fornecedor Empenho, Plano Interno e/ou Natureza Despesa e escolha a(s) opção(ões) que deseja ser(em) filtrada(s). 

Para pesquisar um Empenho, clique no campo “Pesquisar” e informe os dados (Número do Instrumento, CPF/CNPJ/UG/ID Genérico, Nome/Razão Social ou Número do Empenho). 

Figura 128 – Empenhos 

**E) INSTRUMENTOS DE COBRANÇA** 

80 | 183

<!-- pagina 81 -->
Para consultar os Instrumentos de Cobrança, clique no menu **Gestão Contratual > Consultas > Instrumentos de Cobrança.** 

Serão exibidos todas os instrumentos de cobrança cadastradas em todos os contratos da unidade. Os dados poderão ser exportados em “Excel”, “CSV” e “PDF” ou copiados, podendo ser incluídas outras informações por meio de “Visibilidade da coluna”, clicando sobre a(s) informação(ões) que deseja ser(em) exibida(s). 

Para aplicar os filtros existentes, clique em Número, Núm. Contrato, Fornecedor, Lei, Tipo Lista, Justificativa, Dt. Emissão, Dt. Ateste, Dt. Vencimento, Prazo Pagamento, Dt. Protocolo e/ou Situação e escolha a(s) opção(ões) que deseja ser(em) filtrada(s). 

Para pesquisar um Instrumento de Cobrança, clique no campo “Pesquisar” e informe os dados (Número do Instrumento, CPF/CNPJ/UG/ID Genérico, Nome/Razão Social ou Número do Instrumento de Cobrança). 

Figura 129 – Instrumentos de Cobrança 

**F) GARANTIAS** 

Para consultar as Garantias, clique no menu **Gestão Contratual > Consultas > Garantias** . 

Serão exibidas todas as garantias cadastradas em todos os contratos da unidade. 

Os dados poderão ser exportados em “Excel”, “CSV” e “PDF” ou copiados, podendo ser incluídas outras informações por meio de “Visibilidade da coluna”, clicando sobre a(s) informação(ões) que deseja ser(em) exibida(s). 

Para aplicar os filtros existentes, clique em Núm. Contrato, Fornecedor, Tipo Garantia e/ou Vencimento e escolha a(s) opção(ões) que deseja ser(em) filtrada(s). 

Para pesquisar uma Garantia, clique no campo “Pesquisar” e informe os dados (Número do Instrumento, CPF/CNPJ/UG/ID Genérico ou Nome/Razão Social). 

81 | 183

<!-- pagina 82 -->
Figura 130 – Garantias 

# **G) HISTÓRICOS** 

Para consultar o Histórico, clique no menu **Gestão Contratual > Consultas > Históricos** . 

Serão exibidos os históricos de todos os contratos da unidade. 

Os dados poderão ser exportados em “Excel”, “CSV” e “PDF” ou copiados, podendo ser incluídas outras informações por meio de “Visibilidade da coluna”, clicando sobre a(s) informação(ões) que deseja ser(em) exibida(s). 

Para aplicar os filtros existentes, clique em Núm. Contrato, Fornecedor, Receita/Despesa, Tipo, Observação, Número do instrumento Hist., Categoria, Fundamento Legal, Modalidade e/ou Valor Global Hist. e escolha a(s) opção(ões) que deseja ser(em) filtrada(s). 

Para pesquisar um Histórico, clique no campo “Pesquisar” e informe os dados (Número do Instrumento, CPF/CNPJ/UG/ID Genérico, Nome/Razão Social, Tipo ou Número do Instrumento Histórico). 

Figura 131 – Históricos 

**H) ITENS** 

82 | 183

<!-- pagina 83 -->
Para consultar os Itens, clique no menu **Gestão Contratual > Consultas > Itens** . 

Serão exibidos os itens de todos os contratos da unidade. 

Os dados poderão ser exportados em “Excel”, “CSV” e “PDF” ou copiados, podendo ser incluídas outras informações por meio de “Visibilidade da coluna”, clicando sobre a(s) informação(ões) que deseja ser(em) exibida(s). 

Para aplicar os filtros existentes, clique em Núm. Contrato, Fornecedor, Tipo Item e/ou Item Grupo e escolha a(s) opção(ões) que deseja ser(em) filtrada(s). 

Para pesquisar um Item, clique no campo “Pesquisar” e informe os dados (Número do Instrumento, CPF/CNPJ/UG/ID Genérico, Nome/Razão Social, Núm. Item Compra e Item). 

Figura 132 – Itens 

# **I) OCORRÊNCIAS** 

Para consultar as Ocorrências, clique no menu **Gestão Contratual > Consultas > Ocorrências** . 

Serão exibidas as ocorrências de todos os contratos da unidade. 

Os dados poderão ser exportados em “Excel”, “CSV” e “PDF” ou copiados, podendo ser incluídas outras informações por meio de “Visibilidade da coluna”, clicando sobre a(s) informação(ões) que deseja ser(em) exibida(s). 

Para aplicar os filtros existentes, clique em Núm. Ocorrência, Número do instrumento, Fornecedor, Usuário, Vig. Início, Vig. Fim e/ou Situação e escolha a(s) opção(ões) que deseja ser(em) filtrada(s). 

Para pesquisar uma Ocorrência, clique no campo “Pesquisar” e informe os dados (Número do Instrumento, CPF/CNPJ/UG/ID Genérico, Nome/Razão Social, Descrição, E-mail Preposto e Número Ocorrência). 

83 | 183

<!-- pagina 84 -->
Figura 133 – Ocorrências 

# **J) PREPOSTOS** 

Para consultar os Prepostos, clique no menu **Gestão Contratual > Consultas > Prepostos** . 

Serão exibidos os prepostos de todos os contratos da unidade. 

Os dados poderão ser exportados em “Excel”, “CSV” e “PDF” ou copiados, podendo ser incluídas outras informações por meio de “Visibilidade da coluna”, clicando sobre a(s) informação(ões) que deseja ser(em) exibida(s). 

Para aplicar os filtros existentes, clique em Núm. Contrato, Fornecedor, Preposto e/ou Data Início e escolha a(s) opção(ões) que deseja ser(em) filtrada(s). 

Para pesquisar um Preposto, clique no campo “Pesquisar” e informe os dados (Número do Instrumento, CPF/CNPJ/UG/ID Genérico, Nome/Razão Social ou Preposto). 

Figura 134 – Prepostos 

# **K) RESPONSÁVEIS** 

Para consultar os Responsáveis, clique no menu **Gestão Contratual > Consultas > Responsáveis** . 

84 | 183

<!-- pagina 85 -->
Serão exibidos os responsáveis de todos os contratos da unidade. 

Os dados poderão ser exportados em “Excel”, “CSV” e “PDF” ou copiados, podendo ser incluídas outras informações por meio de “Visibilidade da coluna”, clicando sobre a(s) informação(ões) que deseja ser(em) exibida(s). 

Para aplicar os filtros existentes, clique em Núm. Contrato, Fornecedor, Usuário, Função, Instalação/Unidade, Portaria, CPF do Responsável e/ou Nome do Responsável e escolha a(s) opção(ões) que deseja ser(em) filtrada(s). 

Para pesquisar um Responsável, clique no campo “Pesquisar” e informe os dados (Número do Instrumento, CPF/CNPJ/UG/ID Genérico, Nome/Razão Social, CPF ou Nome Responsável). 

Figura 135 – Responsáveis 

# **L) TERCEIRIZADOS** 

Para consultar os Terceirizados, clique no menu **Gestão Contratual > Consultas > Terceirizados** . Serão exibidos os terceirizados de todos os contratos da unidade. 

Os dados poderão ser exportados em “Excel”, “CSV” e “PDF” ou copiados, podendo ser incluídas outras informações por meio de “Visibilidade da coluna”, clicando sobre a(s) informação(ões) que deseja ser(em) exibida(s). 

Para aplicar os filtros existentes, clique em Núm. Contrato, Fornecedor, CPF, Nome, Descrição, Salário, Vale Alimentação, Auxílio Transporte e/ou Escolaridade e escolha a(s) opção(ões) que deseja ser(em) filtrada(s). 

Para pesquisar um Terceirizado, clique no campo “Pesquisar” e informe os dados (Número do Instrumento, CPF/CNPJ/UG/ID Genérico, Nome/Razão Social, CPF ou Nome Terceirizado ou Descrição). 

85 | 183

<!-- pagina 86 -->
Figura 136 – Terceirizados 

# 3.5 – Relatórios 

Acessando o menu **Gestão Contratual > Relatórios** , será apresentado um menu com os tipos de relatórios disponíveis: 

- “Contratos da UG” 

- “Contratos do Órgão” 

Figura 137 – Relatórios 

Para pesquisar o relatório de contratos daquela UG, clique no campo “Pesquisar” e informe os dados 

- Receita/Despesa 

- Tipo 

- Categoria 

- Subcategoria 

- Unid. Requisitantes 

- Número 

- <u>CNPJ/CPF/UG/Id Genérico</u> 

86 | 183

<!-- pagina 87 -->
- Nome 

- Processo 

- Objeto 

Figura 138 – Relatórios – Contratos da UG 

Na tabela de relatórios serão apresentados os resultados da pesquisa. 

Para detalhar o relatório do contrato, clique no ícone 

Figura 139 – Botão de Pesquisar no Relatório 

Será apresentada uma tela com os detalhes do resultado da pesquisa. 

Figura 140 – Detalhamento de Contrato no Relatório 

87 | 183

<!-- pagina 88 -->
Será apresentada uma tela com os detalhes do resultado da pesquisa. 

Figura 141 – Exportação de Relatório de Contratos da UG 

Para fazer uma exportação dos relatórios, clique no ícone e escolha o formato do arquivo desejado para a exportação. 

Os formatos de arquivo disponíveis para exportação são “xlsx”, “xls” e “csv”. 

Com a exportação, mais informações são disponibilizadas, como exibido a seguir. 

Figura 142 – Relatórios 

O Relatório de Contratos do Órgão segue a mesma lógica apresentada para o Relatório por Unidade, apresentando todos os contratos das Unidades ligadas aquele órgão, acrescentando na opção do botão Pesquisar a Unidade. 

Figura 143 – Relatório de Contratos do Órgão 

88 | 183

<!-- pagina 89 -->
# 3.6 – Índices econômicos 

A partir de junho/2023, o sistema passou a ofertar a possibilidade de consulta às séries e realizar cálculos dos índices econômicos: IGP-M (FGV), IPCA (IBGE), INCC (FGV), INPC (IBGE), IST (ANATEL) e ICTI (IPEA). 

Para consultar a série, clicar no menu **Gestão Contratual > Índices econômicos > Consulta Série** . Também pode ser pesquisado algum índice específico, digitando em “Pesquisar” no menu Gestão **Contratual > Índices econômicos >** a sigla desejada. 

Figura 144 – Consultar Série dos Índices Econômicos e Pesquisar 

Para realizar o cálculo de reajuste, clicar em **Gestão Contratual > Índices econômicos > Calculadora** . 

Figura 145 – Calculadora 

Inserir o período com a data início e a data fim, devendo clicar em “Enter” após digitar as datas ou selecionar diretamente no calendário abaixo. Quando o período é selecionado corretamente, as cores das datas selecionadas ficam destacadas, como mostra a figura abaixo: 

89 | 183

<!-- pagina 90 -->
Figura 146 – Selecionar Período de reajustamento 

Após, selecionar o índice desejado dentre as opções disponíveis: 

Figura 147 – Índices econômicos disponíveis 

Por fim, informar o valor a ser reajustado, clicando em “Calcular”: 

Figura 148 – Calcular o reajustamento do valor informado 

Caso não exista série para o período informado, o sistema retornará mensagem informando. Existindo a série, será retornado o valor reajustado, com a respectiva memória de cálculo: 

90 | 183

<!-- pagina 91 -->
Figura 149 – Resultado do cálculo realizado 

- 4 – Fiscalização 

As ferramentas disponíveis para a fiscalização contratual no Contratos.gov.br – Versão Original estão disponíveis através do submódulo Meus Contratos, dentro do Gestão Contratual. 

Um novo módulo relacionado à Fiscalização e Gestão Contratual está disponível na nova versão do sistema. O módulo está disponível para o perfil Responsável por Contrato, voltado aos usuários que realizam a fiscalização e o acompanhamento da execução contratual. 

- 4.1 – Meus contratos 

Para consultar seus contratos, clique no menu **Gestão Contratual > Meus Contratos** : 

Figura 150 – Meus Contratos 

Serão exibidos todos os contratos aos quais o usuário está atribuído, independentemente da UASG gerenciadora do contrato, inclusive sendo possível realizar as Ações em cada um deles. 

Em “Ações”, também é possível acessar a divulgação do contrato no Portal Nacional de Contratações 

Públicas (PNCP), para contratos decorrentes da Lei nº 14.133, de 2021, por meio do ícone . 

- Clicando no ícone , o usuário terá acesso às seguintes ações: 

91 | 183

<!-- pagina 92 -->
- “Arquivos” 

- “Conta-Depósito Vinculada” 

- “Empenhos” 

- “Instrumentos de Cobrança” 

- “Ocorrências” 

- “Terceirizados” 

- “Relatório Final” 

Figura 151 – Meus Contratos 

# 4.2 – Arquivos 

Para adicionar arquivos ao contrato, vá em **Gestão Contratual > Meus Contratos >** selecione o contrato desejado, clique no ícone e em “Arquivos”. 

Figura 152 – Arquivos em Meus Contratos 

Serão exibidos todos os arquivos já adicionados ao Contrato. Só é possível alterar o status e excluir os arquivos que foram adicionados pelo próprio usuário. Para os arquivos inseridos por outros 

92 | 183

<!-- pagina 93 -->
usuários, apenas aparecerá a opção de visualizar o arquivo e atualizar a situação do documento no SEI. Caso seja necessário excluir um arquivo de outro usuário, deverá ser solicitado ao usuário com perfil Setor Contratos, para que o faça no caminho **Gestão Contratual > Contratos > Mais > Arquivos** . 

Figura 153 – Ações em arquivos pelo Responsável por contrato 

Para adicionar, alterar restrição ou excluir um arquivo, local ou pelo SEI, consultar o item 3.1.3 alíneas “A” e “B” deste Manual. 

A diferença das regras contidas no menu de Contratos é que os responsáveis por contratos não poderão adicionar os tipos de documento Contrato, Termo Aditivo, Termo Apostilamento ou Termo Extinção ,os quais só poderão ser inseridos pelo usuário Setor Contratos. 

4.3 – Conta-Depósito Vinculada 

A Conta-Depósito Vinculada ― bloqueada para movimentação é um instrumento de gestão e gerenciamento de riscos para as contratações de serviços continuados com dedicação exclusiva de mão de obra pela Administração Pública Federal direta, autárquica e fundacional. O principal objetivo deste instituto reside na garantia de existência de saldo financeiro para fazer frente aos encargos trabalhistas devidos aos funcionários contratados pelas empresas terceirizadas para a prestação de serviços em órgãos e entidades. 

O quadro abaixo demonstra os percentuais obrigatórios para provisão mensal, totalizando as faixas percentuais dos valores para depósito vinculado, conforme item 14, do Anexo XII, da IN n° 05, de 2017: 

|**Reserva mensalpara opagamento de encargo**<br>**Percentual incidente sobre a remuneração**|**s trabalhis**|**tas**||
|---|---|---|---|
|**ITEM**|**Per**|**centual**|**(%)**|
|13º(décimo Terceiro)Salário||8,33%||
|Férias e 1/3(um terço)constitucional||12,10%||
|Multa sobre FGTS e aviso prévio indenizado e<br>sobre o avisoprévio trabalhado||4,00%||
|**Subtotal:**||**24,43%**||
|Incidência do Submódulo 2.2 sobre o<br>pagamento de férias, um terço constitucional<br>de férias e 13º (décimo terceiro) salário|7,39%|7,60%|7,82%|
|**TOTAL:**|**31,82%**|**32,03%**|**32,25%**|

93 | 183

<!-- pagina 94 -->
A Resolução 169 CNJ dispõe as formas de provisões a serem efetivados em conta-depósito vinculada para os órgãos do Poder Judiciário. 

**A) CADASTRO DA CONTA-DEPÓSITO VINCULADA** 

Para cadastrar a “Conta-Depósito Vinculada”, vá em **Gestão Contratual > Meus Contratos >** selecione o contrato desejado, clique no ícone , em “Conta Depósito-Vinculada” e “Adicionar Conta-Depósito Vinculada”. 

Figura 154 – Conta-Depósito Vinculada em Meus Contratos 

Figura 155 – Adicionar Conta-Depósito Vinculada 

A depender da Conta-Depósito Vinculada utilizada, os campos preenchidos no cadastro da conta são diferentes. 

Preencha os dados da “Conta-Depósito Vinculada” para IN 05/2017: 

- “Banco” 

- “Agência” 

- “Conta Corrente” 

- “Encargos SAT/GIIL-RAT (%)”: corresponde aos percentuais 1%, 2% ou 3% dependendo do grau de risco de acidente do trabalho, prevista no art. 22, inciso II, da Lei nº 8.212, de 1991. 

Após preenchidos todos os dados, clique em “Salvar e voltar”. 

**ATENÇÃO** : Cada contrato poderá ter apenas uma única Conta-Depósito Vinculada. 

94 | 183

<!-- pagina 95 -->
Figura 156 – Cadastro de Conta-Depósito Vinculada 

Preencha os dados da “Conta-Depósito Vinculada” para Resolução 169 CNJ: 

- “Banco” 

- “Agência” 

- “Conta Corrente” 

- “Percentual 13º salário” 

- “Percentual férias” 

- “Percentual abono de férias” 

- “Percentual multa sobre FGTS para as rescisões sem justa causa” 

- “Grupo A” 

Após preenchidos todos os dados, clique em “Salvar e voltar”. 

**ATENÇÃO:** Cada contrato poderá ter apenas uma única Conta-Depósito Vinculada. 

Figura 157 – Cadastro de Conta-Depósito Vinculada 

**B) DETALHAMENTO DA CONTA-DEPÓSITO VINCULADA** 

Figura 158 – Ações da Conta-Depósito Vinculada – pela IN 5/2017 

95 | 183

<!-- pagina 96 -->
Figura 159 – Ações da Conta-Depósito Vinculada – pela Resolução 169 CNJ 

Clicando no ícone 

   - , são exibidas ações relativas a “Conta-Depósito Vinculada”: 

- “Extrato de Lançamentos”: são exibidos todos os lançamentos detalhados por Empregado, Tipo de Movimentação, Mês, Ano, Verba (Encargo) e Valor; 

Figura 160 – Extrato de Lançamentos 

- “Movimentações”: são exibidas todas as movimentações já realizadas detalhadas com o Tipo de Movimentação, Mês, Ano e Total Movimentado; 

Figura 161 – Movimentações 

- “Nova Provisão”: realizar nova retenção para conta vinculada; 

- “Empregados/Liberação”: exibidos todos os terceirizados alocados no contrato com detalhe do Total provisionado e Saldo a ser liberado por terceirizado; 

Figura 162 – Empregados/Liberação 

- “Funções/Reajuste de remuneração”: exibidas todas as funções com respectivos salários do contrato. 

96 | 183

<!-- pagina 97 -->
Figura 163 – Funções/Reajuste de remuneração 

**C) NOVA PROVISÃO NA CONTA-DEPÓSITO VINCULADA** 

Acesse a Conta-Depósito Vinculada, clique no ícone e em “Nova Provisão”: 

Figura 164 – Conta-Depósito Vinculada 

Preencha os campos: 

- Mês Competência; 

- Ano Competência; 

- Empregados que ficarão de fora da provisão: será exibida uma lista com todos os terceirizados alocados no contrato. Caso haja um ou mais terceirizados que não serão provisionados naquele mês, basta selecioná-los na lista. 

Após preenchidos os dados, clique em “Salvar”. 

Será exibida a lista com todas as movimentações já realizadas. 

Figura 165 – Nova provisão 

Caso a haja algum erro na provisão realizada, esta poderá ser excluída clicando no ícone . 

97 | 183

<!-- pagina 98 -->
Figura 166 – Movimentações Conta-Depósito Vinculada 

Clicando no ícone e em “Lançamentos”, são exibidos todos os lançamentos da provisão realizada. 

Figura 167 – Lançamentos da Conta-Depósito Vinculada 

**D) LIBERAÇÃO NA CONTA-DEPÓSITO VINCULADA** 

Acesse a Conta-Depósito Vinculada, clique no ícone 

e em “Empregados/Liberação”: 

Figura 168 – Conta-Depósito Vinculada 

No menu de Movimentações, poderá ser efetuada uma liberação clicando em “Nova Liberação”. 

98 | 183

<!-- pagina 99 -->
Figura 169 – Movimentações Conta-Depósito Vinculada 

São listados todos os terceirizados alocados no contrato. 

Clique no ícone e em “Nova liberação para este empregado”: 

Figura 170 – Empregados/Liberação 

Preencha os campos relativos à Liberação: 

- Mês liberação; 

- Ano Liberação; 

- Situação da Liberação: 

   - a. Férias 

   - b. Décimo Terceiro 

   - c. Férias e Décimo Terceiro 

   - d. Rescisão 

   - e. Realocação 

Conforme a situação da Liberação informada, os campos serão ou não habilitados: 

- Valor para Férias: Férias/Férias e Décimo Terceiro/Rescisão 

- Valor para Décimo Terceiro: Décimo Terceiro/ Férias e Décimo Terceiro/Rescisão 

- Valor da multa caso a rescisão não seja por justa causa: Rescisão 

- Data da rescisão/realocação: Rescisão/Realocação 

Após o preenchimento dos campos, clique em “Salvar”. 

99 | 183

<!-- pagina 100 -->
Figura 171 – Nova Liberação 

**E) REAJUSTE DE REMUNERAÇÃO** 

Acesse a Conta-Depósito Vinculada, clique no ícone e em “Funções/Reajuste de remuneração”: 

Figura 172 – Conta-Depósito Vinculada 

Clique no ícone e em “Funções/Reajuste de remuneração”: 

Figura 173 - Funções/Reajuste de remuneração 

Preencha os dados para o Reajuste de Remuneração: 

- “Jornada semanal”: selecione a jornada de trabalho a ser reajustada; 

- “Descrição Complementar”: descrição detalhada conforme cadastrado nas informações do terceirizado; 

100 | 183

<!-- pagina 101 -->
- “Nova remuneração”: valor da nova remuneração; 

- “Mês Início”: mês início do novo salário; 

- “Ano Início”: ano início do novo salário; 

- “Mês Fim”: mês fim do novo salário; 

- “Ano Fim”: ano fim do novo salário. 

Após preenchidos todos os dados, clique em “Salvar”. 

Figura 174 – Reajuste de remuneração 

# 4.4 – Empenhos 

Os empenhos decorrentes das minutas de empenhos do tipo Contrato e os empenhos do tipo Compra vinculados ao Instrumento Inicial emitidos a partir de maio de 2023 estão sendo vinculados ao Contrato automaticamente. Os empenhos vinculados automaticamente não poderão ser excluídos, nem editados. Para os empenhos antigos e os demais casos, deve-se seguir os passos abaixo. 

Para cadastrar, consultar, editar ou excluir um empenho, vá em **Gestão Contratual > Meus Contratos >** selecione o contrato desejado, clique no ícone e em “Empenhos” e siga as instruções contidas no item 3.1.3 alínea “E” deste Manual. 

Figura 175 – Empenhos em Meus Contratos 

101 | 183

<!-- pagina 102 -->
- 4.5 – Cadastro de Instrumentos de Cobrança (Faturas) 

Para cadastrar, consultar, editar ou excluir um instrumento de cobrança, vá em **Gestão Contratual > Meus Contratos >** selecione o contrato desejado, clique no ícone e em “Instrumentos de Cobrança” e siga as instruções contidas no item 3.1.3 alínea “N” deste Manual. 

Figura 176 – Instrumentos de cobrança em Meus Contratos 

# 4.6 – Cadastro de Ocorrências 

Para cadastrar, consultar, editar ou excluir um instrumento de cobrança, vá em **Gestão Contratual > Meus Contratos >** selecione o contrato desejado, clique no ícone e em “Ocorrências” e siga as instruções contidas no item 3.1.3 alínea “O” deste Manual. 

Figura 177 – Ocorrências em Meus Contratos 

- 4.7 – Cadastro de Terceirizados 

Para cadastrar, consultar, editar ou excluir um Terceirizado, vá em **Gestão Contratual > Meus Contratos >** selecione o contrato desejado, clique no ícone e em “Terceirizados” e siga as instruções contidas no item 3.1.3 alínea “P” deste Manual. 

102 | 183

<!-- pagina 103 -->
Figura 178 – Terceirizados em Meus Contratos 

# 4.8 – Relatório Final 

Funcionalidade descrita no item 3.1.3 – Ações em Contratos, alínea “U” deste Manual. 

5 – Gestão orçamentária 

- 5.1 – Minutas de Empenho 

Funcionalidade habilitada para o perfil <u>Execução Financeira, permitindo a criação e alteração</u> (reforços e anulações e alteração de fonte) de minutas de empenho. 

São exibidos separadamente as minutas do ano corrente e as minutas dos anos anteriores (Restos a Pagar). 

Figura 179 – Minuta de empenho do ano corrente e dos anos anteriores 

Empenhos criados a partir do Compras.gov.br Contratos terão suas minutas listadas em “Minuta Empenho” permitindo alterações posteriores. 

Empenhos criados a partir do SIAFI estarão listados apenas em “Empenho”, devendo ser gerenciados pelo SIAFI. 

Para acessar a funcionalidade, acesse o menu **Gestão Orçamentária > Minuta Empenho** . 

Figura 180 – Gestão Orçamentária 

**A) CRIAR MINUTA DE EMPENHO** 

103 | 183

<!-- pagina 104 -->
**a. FLUXO 1 – Contrato/Compra** 

Caso deseje criar Minuta de Empenho, clique em 

Poderão ser criadas Minutas de Empenho a partir de um **Contrato** , uma **Compra,** de um **Suprimento de Fundos** ou do **Contrata+Brasil** 

Para minutas do tipo **Contrato** : 

- “Contrato”: pesquise o número do Contrato e selecione-o na lista de contratos. Para este tipo de minuta, o sistema validará os dados da Compra informados no Instrumento Inicial/Contrato. Caso algum dado esteja incorreto, o sistema emitirá uma mensagem de alerta “Compra não encontrada”. Assim, revise o cadastro do Instrumento Inicial/Contrato, corrigindo o dado errado, possibilitando, assim, a emissão da minuta de empenho do tipo Contrato. Para esse tipo emissão, o sistema passa a listar automaticamente os empenhos daquele contrato no menu **Gestão contratual > Contratos > Mais > Empenhos** e na aba “Empenho” do instrumento inicial. 

Clique em “Próxima Etapa” para prosseguir. 

Figura 181 – Criar Minuta de Empenho 

Para minutas do tipo “Compra”: 

- “Unidade Compra”: informe a UASG que realizou o processo de compra; 

- “Modalidade Licitação”: informe a modalidade de licitação da compra; 

- “Número/Ano”: informe o número e ano da compra. 

Clique em “Próxima Etapa” para prosseguir. 

Se os dados estejam preenchidos corretamente, você será encaminhado à etapa 2 do fluxo de empenho onde serão exibidos todos os fornecedores pertencentes aquela compra. 

Se os dados estiverem incorretos, será exibida mensagem de alerta. Revise os dados preenchidos. 

104 | 183

<!-- pagina 105 -->
Figura 182 – Criar Minuta de Empenho 

Para minutas do tipo “Suprimento”: 

- “Suprido”: pesquise pelo suprido através do nome ou CPF. 

Clique em “Próxima Etapa” para prosseguir. 

**ATENÇÃO:** O Suprido deverá estar cadastrado na base de dados de Fornecedores do Compras.gov.br Contratos. Verifique se o Suprido também está cadastrado no SIAFI. 

Figura 183 – Fluxo 1 – Contrato/Compra 

Para minutas do tipo “Contrata+Brasil”: 

- “Id contratação PNCP”: informe o número do id contratação PNCP . Clique em “Próxima Etapa” 

- para prosseguir 

105 | 183

<!-- pagina 106 -->
Se o campo estiver preenchido corretamente, você será encaminhado à etapa 2 do fluxo de empenho onde serão exibidos todos os fornecedores pertencentes aquela compra. Se o dado estiver incorreto, será exibida mensagem de alerta. 

Figura 184– Fluxo 1 – Minuta de empenho tipo “Contrata+Brasil” 

**b. FLUXO 2 – Fornecedor** 

São exibidos todos os Fornecedores com itens homologados disponíveis para empenhar. 

Selecione o fornecedor desejado clicando no ícone 

Figura 185 – Fluxo 2 – Fornecedor 

**Atenção:** Não será exibido fornecedor cujos itens estejam sem saldo ou com data de vigência expirada. 

106 | 183

<!-- pagina 107 -->
Figura 186 – Fluxo 2 – Fornecedor 

**c. FLUXO 3 – Itens** 

Exibidos todos os itens homologados que tenham saldo e estejam com vigência válida. 

Selecione o(s) item(s) que deseja empenhar. É possível escolher todos de uma só vez (quando não houver material e serviço no mesmo processo) clicando em “Ações”. 

**Atenção:** Não serão exibidos itens sem saldo ou com data de vigência encerrada. 

Figura 187 – Fluxo 3 – Itens 

**d. FLUXO 4 – Crédito Disponível** 

Exibidas todas as contas contábeis disponíveis para utilização na UG Emitente selecionada pelo usuário. Se usuário estiver habilitado em outras UASGs e desejar empenhar para alguma delas, basta alterar a UG emitente. Pode ser realizada pesquisa para localizar a conta contábil desejada seja pelo <u>PTRS, Fonte, ND, UGR ou Plano Interno.</u> 

Selecione a conta contábil desejada e clique em “Próxima Etapa”. 

107 | 183

<!-- pagina 108 -->
Figura 188 – Fluxo 4 – Crédito disponível 

**e. FLUXO 5 – Subelemento** 

São exibidos os itens selecionados para empenho. 

Deverá ser selecionado o Subelemento e a Quantidade ou Valor Total que se deseja empenhar. 

Os campos Quantidade e Valor Total estarão habilitados para preenchimento a depender do tipo da contratação realizada. 

Após preenchidos todos os dados, clique em “Próxima Etapa”. 

Figura 189 – Fluxo 5 – Subelemento 

Ao avançar, caso seja informado um valor que possa gerar o erro **(ER0462** ) “ _O valor da operação informado deve ser igual à multiplicação da quantidade pelo valor unitário_ ”, o sistema apresentará automaticamente sugestões de valores a menor e a maior em relação ao valor originalmente informado. Dessa forma, o empenho poderá ser emitido normalmente e, posteriormente, a diferença poderá ser ajustada por meio de anulação ou reforço irrisório. 

108 | 183

<!-- pagina 109 -->
Figura 190 – Fluxo 5 – Subelemento 

109 | 183

<!-- pagina 110 -->
**f. FLUXO 6 – Dados Empenho** 

Preencha os dados: 

- “Número Empenho”: quando a unidade realiza controle de numeração de empenho; 

- “ID CIPI”: para empenhos de obras e projetos de investimentos em infraestrutura; 

- “Data Emissão”: data de emissão do empenho; 

- “Tipo Empenho”: tipo de empenho Estimativo, Global ou Ordinário; 

- “Número Processo”: número processo SEI ou sistema correspondente; 

- “Amparo Legal”: selecione o amparo legal da minuta de empenho; 

- “Taxa de Câmbio”: no caso de empenho adquirido em moeda estrangeira; 

- “Local de Entrega”: local de entrega do produto ou prestação do serviço; 

- “Descrição/Observação”: descrição do objeto do empenho. 

Os campos marcados com * são de preenchimento obrigatório. 

Após preenchidos todos os dados, clique em “Próxima Etapa”. 

Figura 191 – Fluxo 6 – Dados Empenho 

- **g. FLUXO 7 – Passivo Anterior** 

Se a minuta de empenho for de Passivo Anterior, selecione “Passivo Anterior”, digite o número da Conta Contábil correspondente e clique em “Adicionar”. 

Clique em “Próxima Etapa”. 

110 | 183

<!-- pagina 111 -->
Figura 192 – Fluxo 7 – Passivo Anterior 

**h. FLUXO 8 – Finalizar** 

São exibidas as informações resumidas da minuta que está sendo gerada. 

Caso esteja tudo correto, clique em “Emitir Empenho SIAFI”. Se houver mais de um fornecedor para esta mesma compra, será habilitado a opção “Empenhar outro Fornecedor”. 

Figura 193 – Fluxo 8 – Finalizar 

**B) ALTERAR MINUTA DE EMPENHO** 

111 | 183

<!-- pagina 112 -->
# **a. FLUXO – Alteração de empenho do ano corrente** 

Primeiro passo é pesquisar e localizar a minuta de empenho em que se deseja efetuar reforço ou anulação. 

Localizada a minuta, clique no ícone e em “Alterar Empenho”. 

Figura 194 – Minutas de Empenho 

Se houver alguma alteração de reforço ou anulação já realizada na minuta será exibida na lista. Clique em “Adicionar Alteração do Empenho”. 

Figura 195 - Alteração Do Empenho 

Selecione o tipo de Operação desejada: 

- “Nenhuma” 

- “Reforço” 

- “Anulação” 

- “Anulação saldo irrisório” 

- “Reforço irrisório” 

**ATENÇÃO:** Não é possível avançar com uma alteração sem que pelo menos 1 item tenha um “Tipo de Operação” igual a **Reforço, Anulação, Anulação irrisória ou Reforço irrisório** . 

A opção de “Reforço” não está disponível para itens inativados, ou cujo valor tenha sido ajustado. Os campos Quantidade e Valor Total estarão habilitados para preenchimento a depender do tipo da contratação realizada. 

Clique em “Próxima Etapa”. 

112 | 183

<!-- pagina 113 -->
Figura 196 – Alteração Do Empenho 

Confira os dados da alteração e clique em “Emitir Empenho SIAFI”. 

Figura 197 – Alteração Do Empenho 

**b. FLUXO – Cancelamento de saldo de empenho inscrito em Resto a pagar** 

Primeiro, pesquise e localize a minuta de empenho que deseja cancelar, utilizando os filtros para facilitar a busca. 

(ações), escolhendo a opção “Alterar Empenho”. 

Em seguida, selecione a minuta e clique no ícone 

113 | 183

<!-- pagina 114 -->
Logo após em clique em “Adicionar Alteração do Empenho”, conforme ilustrado na figura 189 - alteração do Empenho. 

Figura 198– Alteração Do Empenho 

Selecione a operação “Cancelamento”, preencha o campo Quantidade ou Valor Total e, em seguida, clique em “Emitir empenho SIAFI” 

**C) ALTERAR A FONTE DA MINUTA DE EMPENHO** 

A alteração de fonte só é permitida para empenhos do tipo **Compra** . 

Acessar o menu **Gestão orçamentária > Minuta de empenho** . Pesquisar e localizar a minuta de empenho em que se deseja efetuar a alteração da fonte. 

114 | 183

<!-- pagina 115 -->
# Localizada a minuta, clique no ícone e em “Alterar Fonte”. 

Figura 199 – Minutas de Empenho 

Em seguida, será exibida a possibilidade de escolha de uma nova fonte orçamentária. Escolha a fonte para qual será feita a alteração do empenho e clique em “Próxima etapa”. 

Figura 200 – Escolha da nova fonte 

Na próxima etapa, “Subelemento”, definir, no campo **Qtd** , a quantidade que será anulada no empenho inicial e será alterada para a nova fonte. Quando existir mais de 1 item na lista, escolher quais terão uma quantidade anulada definindo o tipo de operação como “ANULAÇÃO”. 

**ATENÇÃO:** Não é possível avançar com uma alteração sem que pelo menos 1 item tenha um “Tipo de Operação” igual a **Anulação** . 

Clicar em “Próxima etapa”. 

115 | 183

<!-- pagina 116 -->
Figura 201 – Alteração da fonte 

Na última etapa, “Alteração do Empenho”, conferir os dados e clicar, ao final da página, em “Emitir Empenho SIAFI”. 

Como resultado, será emitida uma anulação para o empenho cuja fonte se desejava trocar e, automaticamente, será emitido um novo empenho, para a mesma compra e na mesma quantidade anulada no primeiro, mas com a nova fonte escolhida. A data de emissão do novo empenho será a mesma data do empenho que originou. 

No caso de empenhos originados de Atas de Registro de Preços, poderá ser alterada a fonte daqueles que tiverem sido emitidos durante a vigência da ata. 

**Importante:** Caso uma alteração de fonte não seja concluída, ficará, na lista de Minutas de Empenho, uma minuta pendente com situação “AGUARDANDO ANULAÇÃO”. 

# Figura 202– Empenho aguardando anulação 

Para excluí-la, é necessário entrar nas alterações do empenho que teria a fonte alterado clicando no ícone e em “Alterar Empenho”. Em seguida, excluir a minuta de empenho de alteração que está com situação “EM ANDAMENTO”. 

116 | 183

<!-- pagina 117 -->
Figura 203 – Empenho aguardando anulação 

Uma mensagem de alerta informando que a minuta de alteração de fonte será excluída aparecerá. Clicar em “Sim”. 

Figura 204 – Empenho aguardando anulação 

# **D) PDF EMPENHO** 

Para gerar o PDF do empenho emitido no SIAFI, acesse o menu **Gestão Orçamentária > Minuta Empenho > Mais > PDF Empenho** . Só é possível gerar o documento após as assinaturas do empenho no SIAFI. 

Figura 205– Gerar PDF do empenho 

117 | 183

<!-- pagina 118 -->
# **E) DEFINIR SUBSTITUTIVO DE CONTRATO** 

Para definir um empenho como substitutivo de contrato, acesse **Gestão Orçamentária > Minuta Empenho > Mais > Definir substitutivo de contrato** . 

Figura 206 – Definir substitutivo de contrato 

Também é possível definir uma minuta como substitutiva de contrato na etapa 6 ao adicionar uma minuta que seja do tipo Compra em: **Gestão Orçamentária > Minuta empenho > Adicionar Minuta de Empenho >** avançar até a etapa 6, conforme instruções do item 6.1 deste Manual. 

Figura 207 – Definir substitutivo de contrato – Etapa 6 

Só é possível definir um empenho como substitutivo de contrato quando este for do tipo **Compra** . Ou seja, a opção estará bloqueada para minutas do tipo Contrato e Suprimentos de Fundos. 

118 | 183

<!-- pagina 119 -->
Após a definição do empenho como substitutivo de contrato, é necessário criar um contrato do Tipo Empenho, conforme instrução do item 3.1.2 deste Manual. 

# **F) REMOVER SUBSTITUTIVO DE CONTRATO** 

Para remover um empenho como substitutivo de contrato, acesse **Gestão Orçamentária > Minuta Empenho > Mais > Remover substitutivo de contrato** . 

Essa opção só estará disponível caso ainda não tenha sido criado um contrato do tipo empenho, conforme explicado no item 3.1.2 deste Manual. 

Figura 208 – Remover substitutivo de contrato 

# 5.2 – Empenhos 

Para visualizar todos os empenhos emitidos para a unidade, acesse o menu **Gestão Orçamentária > Empenho** . Serão listados todos os empenhos emitidos para a unidade sejam eles emitidos pelo Compras.gov.br Contratos ou diretamente pelo SIAFI. 

119 | 183

<!-- pagina 120 -->
Figura 209 – Empenhos 

- **CADASTRO DE EMPENHO** 

Caso o empenho não esteja listado, este poderá ser adicionado clicando em “Adicionar Empenho”. Esta funcionalidade está disponível apenas para usuários do grupo Administrador. 

Figura 210 – Empenhos 

Preencha os campos indicados: 

- “Número Empenho” 

- “Credor/Fornecedor” 

- “Plano Interno (PI)” 

120 | 183

<!-- pagina 121 -->
- “Natureza Despesa (ND)” 

Após preenchidos todos os campos, clique em “Salvar e voltar”. 

Os campos marcados com * são de preenchimento obrigatório. 

Figura 211 – Empenhos 

- **PESQUISA DE EMPENHO** 

Para pesquisar um empenho, clique no campo “Pesquisar” e informe os dados (Número do Empenho, CPF/CNPJ/UG/ID GENÉRICO, NOME/RAZÃO SOCIAL ou Número/Ano da Compra). 

Os resultados da pesquisa serão apresentados na tabela de empenhos. 

Figura 212 – Pesquisa de Empenhos 

- **EDITAR CADASTRO DE EMPENHO** 

Para editar o cadastro de empenho, clique no ícone 

121 | 183

<!-- pagina 122 -->
Figura 213 – Editar Empenho 

Será apresentada a tela com os dados do empenho para edição. 

Após a edição, clique em “Salvar e voltar”. 

Figura 214 – Editar Empenho 

- **CADASTRO DE EMPENHO DETALHADO** 

Para cadastrar empenho detalhado, clique no ícone e “Empenho Detalhado”. 

122 | 183

<!-- pagina 123 -->
Figura 215 – Empenho Detalhado 

Será apresentada a tela para realização do cadastro. 

Para adicionar um empenho detalhado clique em “Adicionar Empenho Detalhado”. 

Figura 216 – Adicionar Empenho Detalhado 

Preencha os campos indicados. 

Clique em “Salvar e voltar”. 

Figura 217 – Adicionar Empenho Detalhado 

123 | 183

<!-- pagina 124 -->
- **EDITAR CADASTRO DE EMPENHO DETALHADO** 

Para editar o cadastro de empenho detalhado, clique no ícone 

Figura 218 – Editar Empenho Detalhado 

Será apresentada uma tela com os dados do contrato para edição. 

Após a edição, clique em “Salvar e voltar”. 

Figura 219 – Editar Empenho Detalhado 

- **DETALHAR CADASTRO DE EMPENHO DETALHADO** 

Para detalhar o cadastro de empenho detalhado, clique no ícone 

Figura 220 – Detalhar Cadastro de Empenho Detalhado 

Será apresentada uma tela com os detalhes do cadastro do Empenho Detalhado. 

124 | 183

<!-- pagina 125 -->
Figura 221 – Detalhar Cadastro de Empenho Detalhado 

- **EXCLUSÃO DO CADASTRO DE EMPENHO DETALHADO** 

Para excluir o cadastro de empenho detalhado, clique no ícone 

Figura 222 – Exclusão de Cadastro de Empenho Detalhado 

- 5.3 – Restos a Pagar 

Para visualizar todos os empenhos emitidos para a unidade inscritos em restos a pagar, acesse o menu **Gestão Orçamentária > Restos a Pagar** . Serão listados todos os empenhos emitidos para a unidade sejam eles emitidos pelo Compras.gov.br Contratos ou diretamente pelo SIAFI que estejam inscritos em restos a pagar. 

- 5.4 – Consulta 

É possível consultar os valores empenhados para cada tipo de Material, catalogado de acordo com o PDM (Padrão Descritivo de Materiais), bem como para cada Serviço, catalogado pelo Código de Serviço. Para acessar esta funcionalidade, vá em **Gestão Orçamentário > Consulta > Fracionamento de Despesa** , podendo ser escolhida a opção para Material ou Serviço. 

125 | 183

<!-- pagina 126 -->
Figura 223 – Consulta de Fracionamento de Despensa de Material ou Serviço 

Serão exibidos os itens que tiveram empenhos pela Unidade logada do usuário, podendo ser filtrado por ano de despesa. 

Figura 224 – Filtragem por Ano de emissão do empenho 

Também é possível utilizar o botão Pesquisar para buscar por Código PDM ou pela Descrição. 

Figura 225 – Pesquisa por Código PDM 

126 | 183

<!-- pagina 127 -->
Figura 226 – Pesquisa por Descrição 

No detalhamento do item, é possível verificar o quanto foi empenhado para aquele item, bem como todos os empenhos relacionados ao mesmo. 

Figura 227 – Detalhamento do fracionamento de despesa do item 

No filtro, pode selecionar o ano que deseja ser apresentado o relatório, podendo copiar as informações apresentadas em tela, bem como exportá-las em formatos de “Excel”, “CSV”, “PDF” ou imprimi-las, exceto o detalhamento que não é apresentado no relatório. 

127 | 183

<!-- pagina 128 -->
Figura 228 – Filtro e Exportação de dados no Fracionamento de despesa 

6 – Administração 

# 6.1 – Cadastro de usuários 

Para cadastrar um usuário na sua unidade, acesse o menu **Administração > Acesso > Usuários da minha unidade > Adicionar Usuário Unidade(s)** . 

Os grupos de usuário aparecerão a depender do cadastrador, por exemplo. 

Os campos indicados deverão ser preenchidos nas duas abas: 

- “CPF” 

- “Nome Completo” 

- “E-mail” 

- “UG/UASG Padrão”: preencher com a UASG padrão do usuário 

- “Demais UGs/UASGs”: preencher com as UASGs secundárias do usuário 

- “Grupos de Usuário”: selecionar o grupo de usuário a depender das atividades exercidas pelo usuário. 

Preenchidos todos os campos, clique em “Salvar e voltar”. 

O usuário será cadastrado e receberá senha provisória de acesso no e-mail indicado no cadastro. 

Os campos marcados com * são de preenchimento obrigatório. 

128 | 183

<!-- pagina 129 -->
Figura 229 – Cadastro de usuários 

- 6.2 – Editar dados do usuário 

Para editar dados de um usuário na sua unidade, acesse o menu **Administração> Acesso > Usuários** da minha unidade. 

Pesquise pelo usuário desejado seja pelo CPF, Nome ou E-mail e clique em e altere os dados desejados. 

Figura 230 – Editar dados do usuário 

Caso deseje inativar o usuário, altere sua “Situação” para Inativo e clique em “Salvar e voltar”. 

129 | 183

<!-- pagina 130 -->
Figura 231 – Inativar usuário 

6.3 – Login de usuários 

Desde 01º de novembro de 2024, o acesso ao sistema de contratos.gov.br no ambiente de produção é realizado exclusivamente por meio de login do Gov.br, com conta nível prata ou ouro, conforme alertado anteriormente em comunicado apresentado até essa data. 

Figura 232 – Comunicado novo login 

Ao acessar o sistema Contratos.gov.br, tanto na versão original, quanto na nova versão, será apresentada a nova tela de acesso com a opção de login pelo Gov.br e o acesso ao portal da transparência do sistema, bem como um ícone para acesso ao Portal de Serviços para abertura de chamados em caso de problema com o login. Haverá indicação na tela do ambiente em que o usuário está no canto inferior direito: produção ou treinamento, bem como a indicação de qual versão do sistema está sendo o login, logo abaixo do logo. 

130 | 183

<!-- pagina 131 -->
Figura 233 – Tela de login para acesso ao ambiente de produção na versão original do sistema 

Figura 234– Tela de login para acesso ao ambiente de produção na nova versão do sistema 

O ambiente de treinamento também passou por atualização, contudo o login permanece exclusivamente por meio de CPF e senha próprios do sistema nesse ambiente, servindo tanto para a versão original, quanto para nova versão. 

131 | 183

<!-- pagina 132 -->
Figura 235 – Tela de login para acesso ao ambiente de treinamento na versão original do sistema 

Figura 236 – Tela de login para acesso ao ambiente de treinamento na nova versão do sistema 

6.4 – Configuração de Unidade 

Para adicionar uma configuração em sua Unidade, acesse o menu **Administração > Estrutura > Unidade** , localize sua unidade e na coluna Ações selecione “Configuração” e “Adicionar Configuração da Unidade”. 

Poderá haver apenas uma configuração por Unidade. 

132 | 183

<!-- pagina 133 -->
Figura 237 – Configuração de Unidade 

Figura 238 – Configuração de Unidade 

Preencha os campos indicados na aba “Dados Gerais”: 

- “Padrão Formato Processo”: por padrão, todas as unidades estão pré-configuradas com o padrão SEI de numeração de processo. Caso sua unidade utilize outro padrão, basta alterar o campo para o padrão utilizado, lembrando de utilizar sempre a numeração “9” para os campos numéricos; 

- “Responsável Setor Contratos”: selecione dentre os usuários da unidade aquele que é responsável pelo Setor de Contratos. O usuário selecionado será aquele que receberá e-mails configurados pela Rotina Diária; 

- “Substituto Responsável Setor Contratos”; 

- “Ordenador de Despesa”; 

- “Substituto Ordenador Despesa”; 

- “Telefone 1”; 

- “Telefone 2”. 

Os campos marcados com “*” são de preenchimento obrigatório. 

133 | 183

<!-- pagina 134 -->
Figura 239 – Configuração de Unidade – Dados Gerais 

Preencha os campos indicados na aba “Rotina Diária”: 

- “Rotina Diária E-mails”: caso selecione SIM, serão enviados e-mails ao Responsável do Setor Contratos definido na etapa anterior com a relação de contratos da unidade próximos do vencimento conforme a Periodicidade definida; 

- “Periodicidade E-mails”: periodicidade de e-mails definida conforme o prazo encerramento de vigência dos contratos da unidade. Por padrão o sistema já preenche com 30;60;90;120;150;180. Isso quer dizer que quando for indicado contrato(s) com 180 dias para encerramento da vigência, estes serão indicados e informados via e-mail ao Responsável do Setor de Contratos e assim sucessivamente conforme datas definidas. A periodicidade pode ser alterada pela unidade bastando respeitar que o prazo informado deve ser em dias e a separação entre prazos se dá por “;”; 

- “Texto E-mail”: campo livre caso a unidade deseje inserir texto de informe referente a proximidade de encerramento de vigência dos contratos. 

Figura 240 – Configuração de Unidade – Rotina Diária 

134 | 183

<!-- pagina 135 -->
Preencha os campos indicados na aba “Extrato Mensal”: 

- “Extrato Mensal”: caso selecione SIM, será enviado um extrato à todos os Responsáveis de Contrato que estão atribuídos a contratos em sua unidade; 

- “Envia Extrato que dia do Mês”: dia do mês escolhido para envio do Extrato Mensal de contratos aos Responsáveis por Contrato; 

- “Texto E-mail”: campo livre caso a unidade deseje inserir texto de informe aos Responsáveis por Contrato. 

Após preenchidos todos os campos, clique em “Salvar e Voltar”. 

Figura 241 – Configuração de Unidade – Extrato Mensal 

Preencha os campos indicados na aba “Integração SEI”: 

- “URL API SEI”; 

- “Chave de acesso. 

Após preenchidos todos os campos, clique em “Salvar e Voltar”. 

6.5 – Autoridade Signatária 

Para cadastrar uma Autoridade Signatária em sua Unidade, acesse o menu **Administração > Estrutura > Unidade** , localize sua Unidade e na coluna Ações selecione “Autoridades Signatárias” e “Adicionar Autoridade Signatária”. 

135 | 183

<!-- pagina 136 -->
Figura 242 – Ações/Mais/Autoridades Signatárias 

Figura 243 – Adicionar Autoridade Signatária 

Preencha os campos indicados: 

   - “Nome da Autoridade Signatária” 

   - “Cargo da Autoridade Signatária” 

   - “Titular/Substituta” 

   - “Ativa/Inativa” 

- Preenchidos os campos, clique em “Salvar e voltar”. 

Figura 244 – Cadastro de Autoridade Signatária 

136 | 183

<!-- pagina 137 -->
Para editar o cadastro de uma Autoridade Signatária, clique no ícone . 

Figura 245 – Editar Cadastro de Autoridade Signatária 

Altere os campos desejados e clique em “Salvar e voltar”. 

Figura 246 – Editar Cadastro de Autoridade Signatária 

Para excluir o cadastro de uma Autoridade Signatária, clique no ícone 

A exclusão será realizada apenas para autoridades que foram preenchidas erroneamente e não tenham sido vinculadas a nenhum contrato. 

Para autoridades que já estejam vinculadas aos contratos da unidade, deve ser alterada apenas a situação da autoridade de “Ativo” para “Inativo”. 

Figura 247 – Excluir Cadastro de Autoridade Signatária 

137 | 183

<!-- pagina 138 -->
As Autoridades Signatárias podem ser cadastradas em massa. 

Para tanto, deve ser providenciado arquivo .TXT, contendo as informações: 

Nome da Autoridade Signatária | Cargo da Autoridade Signatária | Titular/Substituta | Ativa/Inativa 

Acessar o menu **Administração > Outros > Importações > Adicionar Importação** . 

Os campos indicados deverão ser preenchidos: 

- “Nome do Arquivo” 

- “Tipo”: selecionar “Autoridade Signatária” 

- “Unidade Gestora” 

- “Contrato” 

- “Grupo usuário” 

- “Delimitador”: informe “|” (barra reta) 

- “Arquivos” 

- “Situação” 

Clique em Escolher arquivos 

Selecione o arquivo .TXT e clique em Abrir; 

Preenchidos todos os campos, clique em “Salvar e voltar”. 

Os campos marcados com * são de preenchimento obrigatório. 

Figura 248 – Importar Autoridade Signatária 

138 | 183

<!-- pagina 139 -->
# 6.6 – Configuração de Órgão 

Para adicionar uma configuração em seu Órgão, acesse o menu **Administração > Estrutura > Órgão** , localize seu Órgão e na coluna Ações/Mais selecione “Configuração” e “Adicionar Configuração do Órgão”. 

Poderá haver apenas uma configuração por Órgão. 

Figura 249 – Configuração de Órgão 

Figura 250 – Adicionar Configuração de Órgão 

Preencha os campos indicados na aba “Básico”: 

139 | 183

<!-- pagina 140 -->
- “Padrão Formato Processo”: por padrão, todas as unidades estão pré-configuradas com o padrão SEI de numeração de processo. Caso seu Órgão utilize outro padrão, basta alterar o campo para o padrão utilizado, lembrando de utilizar sempre a numeração “9” para os campos numéricos. O padrão de processo configurado pelo Órgão será aplicado à todas as Unidades que estão vinculadas ao Órgão; 

- “Sistema Financeiro Externo”: deve ser preenchido com a sigla que representa o sistema financeiro que está integrado ao Contratos por meio do barramento Julius; 

- “Código do contrato no Sistema Externo obrigatório?”: indica se, no cadastro do Contrato, será obrigatório para o usuário informar um código que represente o mesmo contrato em outro sistema interno do órgão. 

- “Utiliza tributações?”: ao selecionar “Sim”, o preenchimento da aba tributações do instrumento de cobrança se tornará obrigatório para o órgão e todas as suas unidades vinculadas. 

Preenchido o formato do processo, clique em “Salvar e voltar”. 

Figura 251 – Configuração de Órgão - Básico 

**Obs.:** Os campos da aba “Migração” não deverão ser preenchidos. 

A aba “Integração Super (SEI)” é explicada detalhadamente no <mark>item 7</mark> deste Manual. 

Poderão ser cadastradas Subcategorias as Categorias de Contrato. 

Clique em “Subcategorias” e em “Adicionar Subcategoria do Órgão”. 

140 | 183

<!-- pagina 141 -->
Figura 252 – Configuração de Órgão – Subcategorias 

Figura 253 – Adicionar subcategoria do Órgão 

Preencha os campos indicados: 

- “Categoria”: selecione a categoria que você deseja subcategorizar; 

- “Subcategoria”: descreva qual subcategoria será criada; 

- “Situação”. 

As subcategorias criadas estarão disponíveis para todas as Unidades vinculadas ao Órgão. 

Os campos marcados com * são de preenchimento obrigatório. 

141 | 183

<!-- pagina 142 -->
Figura 254 – Configuração de Órgão - Subcategorias 

- 7 – Integração com Sistema Eletrônico de Informações (SEI) 

O SEI é uma ferramenta de gestão de documentos e processos eletrônicos utilizada atualmente em diversos órgãos públicos. 

Em parceria com o Instituto Nacional de Seguro Social, foi desenvolvida a integração entre os Sistemas Contratos.gov.br e o Sistema Eletrônico de Informações (SEI) em sua versão 3.1.7, compatível até a versão 4.1.0, visando a implementação de consulta do processo vinculado ao contrato diretamente no SEI do Órgão que dispuser, possibilitando a vinculação de documentos no Contratos, evitando redundância no armazenamento e o encaminhamento de minutas de artefatos de contrato para o processo eletrônico de referência. 

Para a utilização dessa funcionalidade, é necessário preparar previamente o ambiente do SEI, conforme orientações a seguir. 

- 7.1 – Preparar o ambiente do SEI 

O Administrador do SEI do órgão ou unidade deve incluir o sistema Contratos.gov.br e cadastrar os serviços que serão consumidos. 

- 1.1.1. <mark>Cadastrar sistema</mark> 

- Acesse o menu Administração > Sistemas > Novo no SEI. 

142 | 183

<!-- pagina 143 -->
Figura 255 – Menu de Sistemas do SEI 

- Selecione o órgão para o qual será configurada a integração. Se o SEI atender diversos órgãos, será necessário repetir a operação para cada instância. 

- Preencha o campo Sigla com Comprasgovbr. 

- Preencha o campo Nome com Compras.gov.br. 

- Clique em Salvar. 

Figura 256 – Cadastramento de novo sistema no SEI 

- 1.1.2. Cadastrar serviços do sistema 

- Uma vez cadastrado o Sistema, será necessário cadastrar os serviços. Acesse o menu Administração > Sistema > Listar. 

143 | 183

<!-- pagina 144 -->
Figura 257 – Submenu da listagem dos Sistemas do SEI 

- Na listagem exibida, clicar no botão Serviços (engrenagem) do sistema recém incluído. 

Figura 258 – Passo a passo para cadastrar novo serviço 

- Clique em Novo. 

Figura 259 – Passo a passo para cadastrar novo serviço 

- Na tela de cadastramento do serviço, utiliza os parâmetros: 

   - Identificação: ComprasgovbrServices 

144 | 183

<!-- pagina 145 -->
`o` Descrição: Compras.gov.br Services 

- Selecione a opção Gerar links de acesso externo. 

- Selecione a opção Chave de Acesso. 

Figura 260 - Passo a passo para cadastrar novo serviço 

- Copiar a Chave de Acesso: 

Figura 261 – Símbolo para copiar a Chave de Acesso 

- Clique em Salvar. 

Atenção ao cadastramento correto dos parâmetros, pois não será possível consumir o serviço, caso haja divergência! 

1.1.3. Cadastrar operações do serviço 

145 | 183

<!-- pagina 146 -->
- Uma vez cadastrado o Serviço, será necessário cadastrar as operações relacionadas a ele. Acesse o menu Administração > Sistema > Listar. 

- Na listagem exibida, clicar no botão Serviços (ícone engrenagem) do sistema Compras.gov.br. 

Figura 262 - Passo a passo para cadastrar operações do serviço 

- Na listagem exibida, clicar no botão Operações (ícone lista) do serviço ComprasgovbrServices. 

Figura 263 - Passo a passo para cadastrar operações do serviço 

- Na tela Operações, clique em Novo. 

146 | 183

<!-- pagina 147 -->
Figura 264 - Passo a passo para cadastrar operações do serviço 

- Na tela de cadastramento do Novo Serviço, utilize os seguintes parâmetros: 

   - Tipo da Operação: Adicionar Arquivo 

   - Unidade: Todas 

   - Tipo do Processo: Todos 

   - Tipo do Documento: Todos 

- Clique em Salvar. 

Figura 265 - Passo a passo para cadastrar operações do serviço 

   - Repita o procedimento clicando em “Novo” para cadastrar as demais operações listadas: 

- 1.1. Consultar Documento 

- 1.2. Consultar Processo 

- 1.3. Incluir Documento 

- 1.4. Listar Andamentos 

- 1.5. Listar Estados 

147 | 183

<!-- pagina 148 -->
- 7.2 – Configurar a integração com SEI no.br Contratos.gov.br 

   - 7.2.1. Configurar órgão 

   - Para habilitar a integração com o SEI para todas as unidades do órgão, como administrador do órgão no Contratos.gov.br, acesse o menu **Administração > Estrutura > Órgão** . 

Figura 266 – Configuração do Órgão 

- Clique sobre o ícone mais e selecione a opção Configuração. 

Figura 267 – Configuração do Órgão 

- Caso não tenha configuração cadastrada, clique no botão Adicionar Configuração do Órgão. 

- Se já houver configuração cadastrada, clique no ícone Editar. 

148 | 183

<!-- pagina 149 -->
Figura 268 – Configuração do Órgão 

- Selecione a aba Integração SEI. 

- Preencha o campo URL API SEI com o endereço do Webservice SEI (https://{url_sei}/sei/controlador_ws.php?servico=sei) e a Chave de Acesso do SEI do seu órgão. 

Figura 269 – Configuração do Órgão 

- Clique em “Testar conexão” para verificar se o WebService está devidamente configurado. 

Figura 270 – Configuração do Órgão 

149 | 183

<!-- pagina 150 -->
- Caso a mensagem seja de sucesso, clique em “Salvar e voltar”. Caso contrário, verifique se a URL está correta ou entre em contato com o Administrador SEI do seu órgão e solicite que revise as configurações, conforme Seção 1.1.1 deste manual. 

- Caso o erro na conexão persista mesmo com configurações corretas tanto no Contratos quanto SEI, entre em contato com a TI do seu órgão para verificar se é necessária a liberação dos IPs a seguir na rede de dados do órgão: 

Figura 271 – Configuração do Órgão 

- Após clicar em “Salvar e voltar” será exibida uma mensagem de sucesso e o endereço do webservice estará salvo para que a integração seja utilizada por todas as unidades do órgão. 

Figura 272 – Configuração do Órgão 

- Caso alguma unidade tenha a integração com o SEI configurada para unidade, o sistema realizará a comunicação com o webservice configurado para a unidade, não o webservice configurado para o órgão. 

7.2.2. Configurar unidade 

- Para habilitar a integração com o SEI para uma unidade, como administrador de unidade no Contratos.gov.br, acesse o menu **Administração > Estrutura > Unidade** . 

150 | 183

<!-- pagina 151 -->
Figura 273 – Configuração da Unidade 

- Clique sobre o ícone mais e selecione a opção Configuração. 

Figura 274 – Configuração da Unidade 

- Caso não tenha configuração cadastrada, clique no botão Adicionar Configuração. 

- Se já houver configuração cadastrada, clique no ícone Editar. 

Figura 275 – Configuração da Unidade 

- Selecione a aba Integração SEI. 

- Preencha o campo URL API SEI com o endereço do Webservice SEI (https://{url_sei}/sei/controlador_ws.php?servico=sei) e a Chave de Acesso SEI da sua unidade. 

151 | 183

<!-- pagina 152 -->
Figura 276 – Configuração da Unidade 

- Clique em “Testar conexão” para verificar se o WebService está devidamente configurado. 

Figura 277 – Configuração da Unidade 

- Caso a mensagem seja de sucesso, clique em “Salvar e voltar”. Caso contrário, verifique se a URL está correta ou entre em contato com o Administrador SEI ~~d~~ a sua unidade e solicite que revise as configurações, conforme Seção 1 deste manual. 

- Caso o erro na conexão persista mesmo com configurações corretas tanto no Contratos quanto no SEI, entre em contato com a TI da sua unidade para verificar se é necessária a liberação dos IPs a seguir na rede de dados da unidade. 

152 | 183

<!-- pagina 153 -->
Figura 278 – Configuração da Unidade 

- Após clicar em “Salvar e voltar” será exibida uma mensagem de sucesso e o endereço do webservice estará salvo para que a integração seja utilizada pela unidade. 

Figura 279 – Configuração da Unidade 

- 8 – Gestão de atas 

Por meio do menu Gestão de Atas é possível acessar o novo Sistema do Contratos.gov.br, onde serão realizadas as novas funcionalidades do sistema e migradas paulatinamente as funções existentes na primeira versão. Atualmente, o sistema disponibiliza a gestão de atas de registro de preços, com amparo legal na Lei nº 14.133/2021, conectando as unidades, divulgando e agregando transparência às atas de registro de preços e ações relacionadas, aprimorando as condições gerenciais envolvidas. 

153 | 183

<!-- pagina 154 -->
Figura 280 – Acesso ao menu Gestão de atas 

Ao clicar sobre o menu Gestão de atas, o usuário será redirecionado à nova versão do Sistema: 

Figura 281 – Tela inicial do novo Sistema Contratos.gov.br 

Um manual específico sobre o novo Sistema Contratos.gov.br está disponível em Menu > Manual: 

154 | 183

<!-- pagina 155 -->
Figura 282 – Acesso ao Manual do Gestão de atas 

- 9 – Transparência 

<!-- Start of picture text -->
O acesso ao Transparência é possível tanto ao usuário com login e senha, por meio do menu ou no<br>botão  :<br><!-- End of picture text -->

<!-- Start of picture text -->
Figura 283 – Acesso ao Transparência por meio de login<br><!-- End of picture text -->

Para acessar o Transparência sem login, clicar no campo indicado abaixo: 

155 | 183

<!-- pagina 156 -->
Figura 284 – Acesso à página da transparência sem login 

Na tela inicial, são apresentados os filtros por “Órgão”, “Unidade Gestora”, “Fornecedor” e “Contrato”, podendo ser escolhido um ou mais. 

Logo abaixo, temos os quantitativos dos contratos de acordo com o status ativo (cor verde) e prazos de vigência decrescente, onde é possível clicar sobre cada tipo para visualizar os contratos em cada status. Ao lado, possui um gráfico que aponta o valor total contratado de acordo com a categoria cadastrada, podendo marcar ou desmarcar qual categoria deseja visualizar. Ao lado direito, temos gráfico com o quantitativo de contratos listados por ano. Por fim, é apresentado o cronograma estimado mensal por ano de contratação. 

156 | 183

<!-- pagina 157 -->
Figura 285 – Tela inicial do Transparência 

No menu Consulta do lado esquerdo, são encontrados os submenus: **Contratos** , **Instrumentos de Cobrança** e **Terceirizados** . 

# 9.1 – Contratos 

Funcionalidade que permite consultar todos os terceirizados contratos cadastrados no sistema. 

Para acessar a funcionalidade, acesse o menu **Consulta > Contratos** . 

157 | 183

<!-- pagina 158 -->
Figura 286 – Consulta Contratos 

É possível aplicar os seguintes filtros para restringir as informações apresentadas por: “Órgão”, “Unidade Gestora”, “Fornecedor”, “Número Contrato”, “Receita/Despesa”, “Tipo”, “Categorias”, “Vigência Início”, “Vigência Fim”, “Valor Global” e “Valor Parcela”. 

Figura 287 – Filtros em Consulta Contratos 

É possível alterar a visibilidade das colunas, para incluir ou excluir as seguintes informações disponibilizadas: “Órgão”, “Unidade Gestora”, “Unidade Gestora Origem do Contrato”, “Receita/Despesa”, “Número Contrato”, “Unidade Realizadora da Compra”, “Número da Compra”, “Modalidade da Compra”, “Amparo Legal”, “Unidades Requisitantes”, “Tipo”, “Categoria”, 

158 | 183

<!-- pagina 159 -->
“Subcategoria”, “Fornecedor”, “Processo”, “Objeto”, “Informações Complementares”, “Vig. Início”, “Vig. Fim”, “Valor Global”, “Núm. Parcelas”, “Valor Parcela”, “Valor Acumulado”, “Total Despesas Acessórias”, “Instrumentos de Cobrança”, “Terceirizados” e “Arquivos”. 

Figura 288 – Visibilidade da coluna em Consulta Contratos 

Pode-se copiar as informações apresentadas em tela, bem como exportá-las em formatos de “Excel”, “CSV”, “PDF” ou imprimi-las. 

Figura 289 – Funcionalidades em Consulta Terceirizados 

Em Ações, no botão é possível visualizar as informações detalhadas por contrato. Nela, além das informações contidas das colunas da tela anterior, encontram-se o “Histórico”, “Despesas acessórias”, “Empenhos”, “Faturas”, “Garantias”, “Itens”, “Prepostos” e “Responsáveis”. No detalhamento, também são fornecidos os links diretos para as consultas dos Instrumentos de Cobrança e dos Terceirizados daquele contrato, bem como o download dos arquivos inseridos com o status público. 

159 | 183

<!-- pagina 160 -->
Figura 290 – Detalhamento do contrato 

9.2 – Instrumentos de Cobrança 

Funcionalidade que permite consultar todos os instrumentos de cobrança cadastrados no sistema. 

160 | 183

<!-- pagina 161 -->
Para acessar a funcionalidade, acesse o menu “Consulta” -> “Instrumentos de Cobrança”. 

Figura 291 – Consulta Instrumentos de Cobrança 

É possível aplicar os seguintes filtros para restringir as informações apresentadas por: “Órgão”, “Unidade Gestora”, “Fornecedor”, “Tipo Lista”, “Justificativa”, “Situação”, “Lei” e “Número Contrato”. 

Figura 292– Filtros em Consulta Contratos 

161 | 183

<!-- pagina 162 -->
É possível alterar a visibilidade das colunas, para incluir ou excluir as seguintes informações disponibilizadas: “Órgão”, “Unidade Gestora”, “Fornecedor”, “Número Contrato”, “Lei”, “Tipo Lista”, “Justificativa”, “Número”, “Dt. Emissão”, “Dt. Ateste”, “Dt. Vencimento”, “Prazo Pagamento”, “Valor”, “Juros”, “Multa”, “Glosa”, “Valor Líquido a pagar”, “Processo”, “Dt. Protocolo”, “Informações complementares”, “Repactuação”, “Mês referência”, “Ano referência” e “Situação”. 

Figura 293 – Visibilidade da coluna em Consulta Contratos 

Pode-se copiar as informações apresentadas em tela, bem como exportá-las em formatos de “Excel”, “CSV”, “PDF” ou imprimi-las. 

Figura 294 – Funcionalidades em Consulta Instrumentos de Cobrança 

162 | 183

<!-- pagina 163 -->
Em Ações, no botão é possível visualizar as informações detalhadas por instrumento de cobrança. Nela, além das informações contidas das colunas da tela anterior, encontram-se dados sobre “Histórico do contrato”, “Tipo de instrumento de cobrança”, “Arquivo”, “Valor faturado” e “Ações”. 

Figura 295 – Detalhamento do instrumento de cobrança 

# 9.3 - Terceirizados 

Funcionalidade que permite consultar todos os terceirizados contratados com mão de obra exclusiva e cadastrados no sistema. 

Para acessar a funcionalidade, acesse o menu “Consulta” -> “Terceirizados”. 

Figura 296 – Consulta Terceirizados 

163 | 183

<!-- pagina 164 -->
É possível aplicar os seguintes filtros para restringir as informações apresentadas por: “Órgão”, “Unidade Gestora”, “Fornecedor”, “Situação”, “Número Contrato”. 

Figura 297 – Filtros Consulta Terceirizados 

É possível alterar a visibilidade das colunas, para incluir ou excluir as seguintes informações disponibilizadas: “Órgão”, “Unidade Gestora”, “Fornecedor”, “Número Contrato”, “CPF”, “Descrição”, “Descrição Complementar”, “Jornada semanal”, “Unidade”, “Salário”, “Custo”, “Auxílio Transporte”, “Vale alimentação”, “Escolaridade”, “Data Início”, “Data Fim” e “Situação”. 

Figura 298 – Visibilidade da coluna em Consulta Terceirizados 

Pode-se copiar as informações apresentadas em tela, bem como exportá-las em formatos de “Excel”, “CSV”, “PDF” ou imprimi-las. 

164 | 183

<!-- pagina 165 -->
Figura 299 – Funcionalidades em Consulta Terceirizados 

Em Ações, no botão é possível visualizar as informações detalhadas por terceirizado. Nela, além das informações contidas das colunas da tela anterior, encontram-se dado sobre a realocação ou não do funcionário. 

Figura 300 – Detalhamento do terceirizado 

165 | 183

<!-- pagina 166 -->
10 – Gestão Financeira 

Atenção: a partir do dia 2 de abril de 2026, o cadastro dos instrumentos de cobrança passou a ser realizado na nova versão do sistema, disponível em https://contratos.sistema.gov.br/. 

Para mais informações, acesse o _Manual Técnico Operacional do Sistema Contratos.gov.br – Gestão de Atas de Registro de Preços e Fiscalização e Gestão de Contratos – Perfil Governo_ , disponível em <u>https://www.gov.br/compras/pt-br/acesso-ainformacao/manuais/manuais#CONTRATOS.</u> 

Além disso, a partir da mesma data, os instrumentos de cobrança também poderão ser cadastrados pelo fornecedor. Nesse caso, as orientações estão disponíveis no _Manual Técnico Operacional do Sistema Contratos.gov.br – Perfil Fornecedor_ . 

10.1 – Instrumentos de Cobrança 

Por meio dessa funcionalidade, é possível alterar o status da situação financeira dos instrumentos de cobrança, tanto de forma individual quanto em lote. 

Para acessar o módulo, o usuário deve possuir o perfil <u>Execução Financeira</u> em seu cadastro (conforme itens 2, 6.1 e 6.2 deste Manual). 

Para realizar a alteração da situação dos instrumentos de cobrança, acesse: Gestão Financeira > Instrumentos de Cobrança. 

Figura 301 – Instrumentos de Cobrança no menu Gestão Financeira 

A barra superior disponibiliza filtros de pesquisa que facilitam a localização do instrumento de cobrança. No campo "Pesquisar", é possível buscar o instrumento de cobrança pelo seu número ou pelo número do contrato. 

Figura 302 – Barra de filtros para exibição dos instrumentos de cobrança 

Para realizar a alteração **em lote** , selecione os instrumentos de cobrança desejados e clique no ícone “Alterar situação”, localizado na parte superior da tela. Em seguida, escolha a nova situação e <u>informe a justificativa.</u> 

166 | 183

<!-- pagina 167 -->
Figura 303 – Seleção dos instrumentos de cobrança para alteração de situação em lote 

Para alteração da situação de forma **individual** , selecione ou pesquise o instrumento de cobrança que deseja alterar a situação e, em seguida, clique no ícone “Editar” na coluna “Ações” e preencha as informações necessárias para realizar a alteração. 

Figura 304 – Pesquisa do Instrumento de cobrança para alteração individual da situação 

Figura 305 – Alteração da situação do instrumento de cobrança de forma individual 

Instrumento de cobrança na **situação Siafi Apropriado** só altera para situações: Pago, Pago Parcial, Pronto Pagamento e Siafi Cancelado. 

167 | 183

<!-- pagina 168 -->
10.2 – Apropriação de Instrumentos de Cobrança 

Acessar **Gestão Financeira > Apropriação > Instrumentos de Cobrança** , serão listados todos os instrumentos cobranças cadastrados na situação **Pendente** e com **data de emissão do ano corrente** . Se clicar em “Remover filtros” é feita a exclusão dos filtros preexistentes, aparecendo as demais situações dos Instrumentos de Cobrança. 

Para facilitar a seleção do documento, utilize os filtros de seleção na barra superior ou o campo pesquisar. 

Figura 306 – Listagem inicial dos instrumentos de cobrança disponíveis para apropriação 

É possível editar o Instrumento de Cobrança para realizar correções de informações divergentes no Instrumento de Cobrança. Para tanto, basta clicar no ícone e realizar as edições. 

A apropriação pode ser realizada de forma **individual** ou **em lote** . 

Para realizar **em lote** , selecione os instrumentos de cobrança que sejam do mesmo contrato ou do mesmo fornecedor quando for contrato do tipo empenho e, em seguida, clique no ícone “Apropriar Faturas”. 

Figura 307 - Seleção de vários instrumentos para apropriação em lote 

Para realizar de forma individual, clique no ícone “Apropriação de Fatura” da coluna “Ações” 

168 | 183

<!-- pagina 169 -->
Figura 308 - Iniciar apropriação individual 

Após a seleção dos ICs que serão apropriados, irá aparecer uma caixa de diálogo para escolha de como deseja realizar a apropriação. Podendo realizar uma **Nova apropriação** ou **Copiar de** uma apropriação anterior que copia alguns dados, como: situação de PCO e as contas contábeis; situação de Dedução e dados de centro de custo. 

Ao utilizar a opção de **Copiar de** os dados referente a datas (vencimento e pagamento) e percentual de recolhimento da lista de recolhedores da aba Dedução não são copiadas da anterior, sendo necessário o preenchimento desses dados ou a exclusão da aba. 

Figura 309 - Caixa de diálogo para seleção de como deseja apropriar 

Para essa demonstração iremos utilizar a opção **Nova Apropriação** . 

Após selecionar a opção desejada (Nova apropriação ou Copiar de) será direcionado para a tela “Apropriação de instrumento de cobrança – Formulário de alteração de instrumento de cobrança”. 

Nessa tela é necessário selecionar o “tipo de DH padrão”, dentre as opções disponíveis. Qualquer outro tipo de DH a ser apropriado de empenhos emitidos pelo sistema Contratos que não consta na listagem, deverá ser solicitado via abertura de chamado. 

Nessa demonstração utilizaremos a opção “NP – Nota de Pagamento”. 

Após selecionar o “Tipo DH Padrão” não é possível alterar. Em caso de erro, excluir a apropriação e iniciá-la selecionando o novamente o “Tipo DH Padrão” correto. 

169 | 183

<!-- pagina 170 -->
<!-- Start of picture text -->
Figura 310 - Aba Dados Básicos<br><!-- End of picture text -->

Na aba “Dados Básicos”, as informações estão preenchidas de forma automática a partir das informações do Instrumento de Cobrança e do Instrumento Contratual. Caso o usuário deseje, pode alterar, selecionar ou incluir as informações nos campos relacionados a seguir: 

- _UG Emitente_ 

- _Código da UG pagadora_ 

- _Data de Emissão Contábil_ 

- _Data de Vencimento_<sup>_1_</sup> _0F_ 

- _Taxa de Câmbio_ 

- _Processo_ 

- _Ateste_ 

- _Observações_ 

- _Informações Adicionais_ 

Na seleção de “Código da UG pagadora” irão aparecer, além da UG padrão do (a) usuário (a), as demais UGs cadastradas para o (a) usuário (a). No entanto, só será possível realizar a apropriação para a UG emitente da minuta, isto é, a UG que tem o crédito disponível para realizar o pagamento. 

O campo observação traz um texto de preenchimento automático pelo sistema, podendo ser alterado, pois se trata de um campo editável. 

Após preencher e verificar se todos os campos estão com as informações corretas, clique em “Confirmar Dados Básicos”. 

> 1 O campo “Data de Vencimento” obedece às regras da ordem cronológica de pagamento, conforme disponível na Instrução Normativa 77 de 2022 da SEGES, qualquer alteração é de total responsabilidade do (a) usuário (a). 

170 | 183

<!-- pagina 171 -->
Figura 311 - Aba Principal com Orçamento 

Na aba “Principal com Orçamento” é necessário preencher os seguintes campos listado abaixo: 

- _Situação_ : escolher a situação de PCO. 

- _Deseja Repetir os Dados das Contas_ : caso tenha mais de um empenho e usuário (a) queira replicar as informações das contas contábeis para as demais caixas. Se marcar “Sim” será necessário apenas informar as contas no primeiro empenho, para os demais serão copiadas as informações. Em caso de alteração, a informação não é replicada para as demais, sendo necessário alterar manualmente. 

- _Tem Contrato?_ Sim ou Não 

- _Despesa Antecipada?_ Sim ou Não 

- _Conta de Contrato_ : caso tenha informado "Sim”, é necessário preencher o número da conta contrato. 

- _Código GRU_ : preencher quando o credor da apropriação for do tipo UG Siafi (Ex. Empresa Brasileira de Comunicação). Para demais credores, embora o campo também esteja disponível, não é necessário realizar o preenchimento, deixar em branco. 

- _Favorecido do Contrato_ : preenchido automaticamente pela mesma informação da aba “Dados básicos”, sendo campo editável. 

- _Empenho_ : os dados do empenho, como número e valor são preenchidos automaticamente pelas informações cadastradas no instrumento de cobrança. 

É possível realizar alterações acrescentado um outro número de Empenho e valor, desde que o Empenho a ser informado seja da mesma UG emitente que vinculou o Instrumento de Cobrança e o seu valor não ultrapasse o valor do “Documento de origem” que consta na “Aba de dados básicos” da apropriação. Em caso de alteração, clicar em antes de preencher os dados das contas contábeis. 

171 | 183

<!-- pagina 172 -->
Para incluir um novo número de Empenho, clicar no ícone , para duplicar clique no ícone e para excluir no ícone   . 

Em seguida as informações dos empenhos, conforme a “Situação” escolhida, será disponibilizado campos para preenchimento que complementarão a especificação orçamentária da despesa que está sendo cadastrada. O número e tipos de dados a serem preenchidos variam conforme a Situação contábil e conforme tipo de Credor. **Ex.** DSP001 - AQUISICAO DE SERVICOS - PESSOAS JURIDICAS, tem que preencher a conta contábil de Variação Patrimonial Diminutiva (VPD) e a conta contábil de Passivo (Contas a pagar). 

**Obs.:** É possível inserir uma nova aba para incluir uma Situação diferente, clicando no ícone ao lado da Situação já informada ou, excluir uma das Situações, clicando no ícone 

Após preencher e verificar se todos os campos estão com as informações corretas, clique em “Confirmar Dados Principal com Orçamento “. 

Caso não esteja disponível uma situação de PCO no sistema, solicitar via abertura chamado. 

Figura 312 - Aba Dedução 

Para abrir uma situação na aba Dedução, clicar em , caso deseja excluir qualquer situação aberta, clicar em e selecionar a situação desejada. Ao abrir uma situação de Dedução é necessário preencher os seguintes campos: 

- _Situação_ : a partir da situação escolhida, abre novos campos a serem preenchidos, por ex. “Código de recolhimento”. 

172 | 183

<!-- pagina 173 -->
- _UG Pagadora_ : vem preenchido pelos dados da aba dados básicos 

- _Data de Vencimento_ e _Data de Pagamento_ 

- _Possui Acréscimo:_ ao selecionar “Sim” será necessário preencher outros campos que serão abertos. 

- _Lista de recolhedores_ : (clicar no + para abrir) a informação do recolhedor vem preenchida da aba dados básicos, sendo um campo editável para alteração. Ao indicar o % a ser recolhido o valor da receita é preenchido automaticamente, preenchendo também o valor do item. O campo “Valor item” é editável, caso seja necessário alterar o valor. 

- _Relacionamentos_ : caso seja apenas um empenho informado na aba PCO, essa informação será preenchida automaticamente, caso não, deverá ser selecionado o empenho que deseja relacionar. 

- _Pré-doc_ : os dados a serem preenchidos no pré-doc variam de acordo com a situação escolhida. Esses dados podem ou não serem preenchidos. No entanto, uma vez aberta a aba para preenchimento, será obrigatório informar seus dados, caso contrário, exclua antes de salvar a aba. 

Após preencher e verificar se todos os campos estão com as informações corretas, clicar em “Confirmar Dados da Dedução”. 

Caso não esteja disponível uma situação de Dedução no sistema, solicitar via abertura chamado. 

Figura 313 - Aba de Dados de Pagamento 

Na aba Dados do pagamento a linha “Grupo Principal” as informações já estão preenchidas de forma automática. 

Na linha “Lista de Favorecidos” consta as seguintes informações: 

- _Favorecido_ : CNPJ da empresa contratada, podendo ser alterado 

- _Valor_ : o valor apresentado é a subtração entre a aba PCO e aba Dedução, resultando no valor a ser pago. 

- _Pré-doc_ : dados do domicílio bancário da empresa contratada. Clicar em “Pré-doc” e inserir as informações a partir da escolha do “Tipo de OB”. As informações dos dados bancários ficaram salvas a partir da segunda apropriação para o contrato ou para o fornecedor quando for contrato do tipo empenho. 

- _Enviar dados de pagamento?_ Sim ou Não. Ao selecionar a opção “Não”, os dados de pagamento não serão enviados ao Siafi, podendo ser preenchidos diretamente no Siafi ou 

173 | 183

<!-- pagina 174 -->
por meio da funcionalidade Alterar DH (item 10.2.1). Ao escolher “Sim” os dados são enviados normalmente para Siafi. 

Quando o instrumento de cobrança for proveniente de um contrato que tenha operação de crédito do Antecipagov as informações de domicílio bancário estarão preenchidas sem possibilidade de alteração (Instrução Normativa nº 82/2025). Orienta-se não fazer a alteração dos dados no Siafi. 

**Obs.** As abas Dedução e Pré-doc, **não são de preenchimento obrigatório no Contratos** , podendo ser preenchidas no Siafi através da alteração do documento hábil. Bem como qualquer outra aba não constante na apropriação do Contratos, continuarão sendo preenchidas no Siafi por meio da alteração do documento hábil. 

Figura 314 - Aba Centro Custo 

Na aba Centro de Custo deverão ser preenchidos os campos informados a seguir: 

- _Centro de Custo_ : Centro de custo que será associado aos itens do Documento Hábil. 

- _Mês_ : Corresponde ao mês a que o Centro de Custo se refere (Data do fato gerador). 

- _Ano_ : Corresponde ao ano a que o Centro de Custo se refere. 

- _SIORG_ : Corresponde ao código SIORG a que o Centro de Custo se refere. 

- _UG Beneficiada_ : Código da UG beneficiada pelo Custo 

Os campos acima são preenchidos apenas para as Situações Siafi que tenham alocação de custos, para demais Situações não irá aparecer a caixa de centro de custo para preenchimento. 

Após preencher as informações, clicar em “Confirmar Centro de Custo” e depois clicar em “Apropriar Siafi”. 

Após envio dos dados para Siafi, o documento pode ser gerado ficando na situação “Siafi Apropriado” ou pode conter algum erro. Sendo necessário realizar os ajustes para envio novamente. Ainda, em caso de alguma instabilidade o documento pode ficar na situação “Aguardando Siafi”, sendo necessário após um curto prazo de tempo clicar no ícone “Atualizar”. 

# 10.2.1 - Alterar DH 

Após a apropriação de um instrumento de cobrança é possível realizar a alteração do DH com a inclusão de novos itens. 

A inclusão de novos itens é permitida para **DH** na situação **Siafi Apropriado** nas abas: 

174 | 183

<!-- pagina 175 -->
- **Principal com Orçamento (PCO)** 

- **Dedução** 

- **Dados de Pagamento** 

- **Centro de Custo –** quando houver a inclusão de um novo item na aba PCO em uma situação afeta custo “sim” e/ou quando houver novo item na aba Dedução com acréscimos (juros, multa, encargos ou outros). 

Para tanto, basta acessar o documento já apropriado. Para encontrar o documento que deseja incluir novos itens, basta colocar o número do instrumento de cobrança ou contrato no campo pesquisar, selecionar nos filtros a situação “Siafi Apropriado” ou “Remover os filtros”. Em seguida clique no ícone “Apropriações” da coluna “Ações” para entrar no documento apropriado. 

Figura 315 – Listagem inicial dos instrumentos de cobrança/apropriações 

Na tela “Pagamento de Instrumento de Cobrança”, clicar no ícone “Alterar DH” disponível na coluna “Ações”, e na tela seguinte (Alteração de DH) clicar no ícone “Adicionar Alteração de DH” incluir novos itens no documento já apropriado. 

Figura 316 – Tela de Alteração de DH 

Na aba PCO é possível incluir um novo item de empenho em uma situação já apropriada ou uma nova situação de PCO. No exemplo abaixo vamos demonstrar com a inclusão de uma nova situação de PCO. 

1. Clique no “+” para inserir uma nova situação na aba PCO. 

2. Em seguida escolha a situação que deseja incluir e preencha os campos. 

175 | 183

<!-- pagina 176 -->
3. Clique no “+” para inserir os dados do empenho: número do empenho e valor a ser apropriado. Clicar em salvar, logo abaixo do valor. 

4. Confirmar dados PCO. 

Figura 317 – Inclusão de situação de PCO 

Se a inclusão da nova situação de PCO for “afeta custo sim” deverá preencher a aba “Centro de custo”. 

Se  não  houver  mais  nenhuma  inclusão,  clicar  em  “Alterar  DH  no  Siafi”  e  informar  o motivo/observação da alteração, em seguida confirmar. 

Figura 318 – Finalização da Alteração de DH 

1. Para inserir uma nova situação de PCO, clicar no ícone “+” ao lado da situação já incluída e selecionar a situação e realizar os preenchimentos dos campos e salvar. 

Na aba Dedução é possível incluir uma nova situação, observando as seguintes condições: 

- Inserir na alteração de DH apenas uma situação de Dedução - necessário não ter enviado na apropriação anterior os dados de pagamento. 

176 | 183

<!-- pagina 177 -->
- Inserir na alteração de DH uma situação de Dedução juntamente com um novo item na aba PCO – o valor da dedução deverá ser igual ou menos do que o valor inserido na aba PCO. 

No exemplo a seguir, foi inserido uma nova situação na aba PCO no valor de R$ 3,00 e uma nova situação de dedução no valor de R$ 1,00. Na aba “Dados de Pagamento” o valor a ser enviado será de R$ 2,00. 

1. Clique no “+” para inserir uma nova situação de Dedução. 

2. Preencha todos os campos correspondentes. 

3. O preenchimento do pré-doc é facultativo, para o exemplo não foi preenchido. 

4. Confirmar Dados Dedução 

Figura 319 – Inclusão de situação de Dedução 

O valor a ser enviado em “Dados de Pagamento” é a subtração entre o valor inserido na aba “PCO” e “Dedução”, podendo ser igual a zero. 

Na função de “Alterar DH” é possível não enviar os dados de pagamento, selecionando a opção “não” e confirmar a aba antes de enviar. 

Figura 320 – Envio de Dados de pagamento 

# **Outras situações possíveis de alteração de DH:** 

177 | 183

<!-- pagina 178 -->
- **Apropriação do instrumento de cobrança enviada ao Siafi apenas com aba PCO preenchida sem dados de pagamento:** permite a inclusão de uma situação de Dedução sem envio dos dados de pagamento na alteração. 

- **Apropriação do instrumento de cobrança enviada ao Siafi com aba PCO e dedução preenchidas sem dados de pagamento:** permite o envio dos dados de pagamento na alteração. 

- **Apropriação do instrumento de cobrança enviada ao Siafi apenas com aba PCO preenchida sem dados de pagamento:** permite o envio dos dados de pagamento na alteração. 

- **Apropriação do instrumento de cobrança enviada ao Siafi apenas com aba PCO preenchida sem dados de pagamento:** permite a inclusão de uma situação de Dedução e o envio dos dados de pagamento na alteração. 

## **ATENÇÃO:** 

- O cancelamento do DH no Contratos, cancela o DH e suas alterações. Não é possível cancelamento de partes do DH, apenas no Siafi. 

- Não é possível incluir novo item de Dedução sem inclusão de item na aba PCO quando a apropriação anterior foi enviada com Dados de Pagamento. 

- Não é possível incluir itens de acréscimos em uma situação de Dedução já apropriada. Apenas na inclusão de uma nova situação. 

- Não é possível marcar “não” na aba de dados de pagamento quando a apropriação for de um instrumento de cobrança proveniente de um contrato com operação de crédito de Antecipagov. 

# 10.2.2 – Não liquidar itens de empenhos 

Ao incluir uma nova apropriação, é possível **não liquidar os itens de empenho** da aba Principal com Orçamento. Para tanto, basta selecionar a opção “Não” na aba PCO, após a escolha da situação. Se for uma situação que afeta custo (DSP001, por ex.) deverá preencher o centro de custo antes de concluir a apropriação, se for uma situação que não afeta custo (DSP101, por ex.) seguir para o envio dos dados após preenchimento dos dados da aba PCO. 

Após preenchimento dos dados e confirmação da aba PCO e preenchimento da aba Centro de Custo (se houver), clicar em "Apropriar Siafi”. 

178 | 183

<!-- pagina 179 -->
Figura 321 – Não liquidar itens de empenho na aba PCO 

Após o envio da apropriação para Siafi sem liquidação dos empenhos, é possível realizar a liquidação pela função de alterar DH. Para tanto, selecione o instrumento de cobrança que deseja liquidar os itens de empenho e clique no ícone “Alterar DH”. Ao entrar no documento apropriado, clicar em “Liquidar Empenhos no Siafi” e verificar a data de Ateste, podendo alterar, se for o caso, e confirmar. 

Figura 322 – Liquidação dos itens de empenho 

Após a liquidação dos itens de empenho na aba PCO, o documento fica disponível para inclusão de novos itens de PCO ou dedução, ou apenas para envio dos dados de pagamento. Caso não tenha alteração a se fazer além da liquidação dos empenhos, clicar em “Alterar DH” preencher os dados de motivação/observação e enviar para Siafi. 

179 | 183

<!-- pagina 180 -->
Quando iniciar uma apropriação pelo **Copiar De** e for marcar “Não” em Liquidado na aba PCO, observar se há itens na aba Dedução abertos. Caso tenha, realizar a exclusão do item antes de enviar para Siafi, caso contrário, o documento ficará na situação “Aguardando Siafi”. 

# 10.2.3 – Buscar Ordem Bancária 

Caso a Apropriação esteja realizada no Siafi (Paga), é possível buscar os dados da Ordem Bancária da Apropriação: Conta Bancária, Nº da Agência, Nº Banco, Nº Documento OB, Nº Cancelamento OB, Data de Emissão, Valor e Observação. Para tanto, selecione em Gestão Financeira > Apropriação > Instrumento de Cobrança, as Apropriações com a situação “Siafi Apropriado”, em Ações clique no ícone “ ” – “Apropriação em Andamento” e depois no ícone “ ” – “Busca Ordem Bancária”. 

Figura 323 – Buscar Ordem Bancária 

11 – Tela Início 

# 11.1 – Apresentação 

Na tela inicial, temos acesso às informações dos quantitativos de Novos contratos, Contratos vigentes, Contratos vencidos e Mensagens pendentes dos últimos cinco dias. 

Logo abaixo, temos o feed de notícias com as informações recentes relacionadas aos sistemas estruturantes ou aos Contratos. Ao lado, fica o gráfico com as informações dos contratos por categoria da Unidade logada do usuário. Por fim, o calendário com as informações de vigência dos contratos. 

180 | 183

<!-- pagina 181 -->
Figura 324 – Tela de início 

11.1 – Barra superior 

11.1.1 – Abrir chamado 

Caso o usuário enfrente alguma dificuldade não sanável no Manual ou o sistema apresente algum comportamento fora do comum, deve-se abrir chamado para equipe especializada, que auxiliará na resolução do problema apresentado. Ao clicar em “Abrir chamado”, o usuário será redirecionado ao Portal de Serviços. 

Figura 325 – Informar erro – Acesso ao Portal de Serviços 

# 11.1.2 – Manual 

Ao clicar em Manual, o usuário será encaminhado à página com a versão atualizada do Manual “www.gov.br/compras/pt-br/acesso-a-informacao/manuais/comprasgovbr-contratos/manual- <u>comprasgovbr-contratos.pdf”.</u> 

No “Histórico de versões” se tem as informações das informações alteradas ou incluídas em cada versão do Manual. 

181 | 183

<!-- pagina 182 -->
Figura 326 - Manual 

# 11.1.2 – Meus Dados 

No canto superior direito, fica a funcionalidade dos “Meus Dados”: 

Figura 327 – Meus Dados 

Nela é possível atualizar os dados da conta ou alterar a senha do usuário. Ao clicar em “Atualizar minha conta”, são apresentados os dados: 

- CPF: campo bloqueado e com o CPF do usuário; 

- Nome: passível de edição e atualização pelo usuário, sendo apresentado o nome completo 

- cadastrado inicialmente; 

182 | 183

<!-- pagina 183 -->
- E-mail: passível de edição e atualização pelo usuário, sendo apresentado o nome completo cadastrado inicialmente; 

- UG Primária: campo bloqueado com a unidade principal cadastrada inicialmente; 

- Senha SIAFI: campo está prestes a ser omitido, pois o sistema já faz a integração com o SIAFI a 

- partir do CPF do usuário, sem precisar informar a senha do SIAFI neste menu. 

Ao atualizar as informações, basta clicar em “Salvar”. 

Figura 328 – Atualizar minha conta em Meus Dados 

Para alteração de senha, clicar em “Mudar senha”, onde deverá ser informada a senha antiga, a nova senha e confirmada a nova senha, clicando em “Mudar senha” para salvar. 

Figura 329 – Mudar senha em Meus Dados 

Para incluir uma foto no perfil do usuário, é preciso que o usuário faça um registro na página <u>http://pt.gravatar.com/ com o mesmo e-mail informado no cadastro do Sistema e inclua sua foto.</u> Automaticamente, o sistema Contratos irá atualizar a foto do usuário no dia seguinte a essa inclusão. 

12 – Disposições Finais 

Este manual trouxe o passo a passo das operações realizadas no sistema Contratos.gov.br. 

Aguardem que virão novas funcionalidades em breve! 

Em caso de dúvidas, entre em contato com a Central de Atendimento por meio do telefone 0800979-9001 ou do endereço eletrônico https://www.gov.br/gestao/ptbr/assuntos/gestaoeinovacao/central-de-atendimento. O suporte é realizado de segunda à sextafeira, das 07:00 às 20:00 horas. 

183 | 183
