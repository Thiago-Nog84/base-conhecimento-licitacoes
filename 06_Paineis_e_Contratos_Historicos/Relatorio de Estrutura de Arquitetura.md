---
arquivo_original: "Relatorio de Estrutura de Arquitetura.pdf"
hash_pdf_md5: 3543cd16ca2af5ab9ca4ba4f6953cf57
paginas: 8
metodo: "texto (pymupdf4llm)"
convertido_em: 2026-10-03T15:29:06
fonte: Base de Conhecimento CLC
---

<!-- pagina 1 -->
# PCA-MPPI — Detalhamento Técnico do Sistema e Estrutura de Arquitetura 

# ## 1. Finalidade do Documento 

Este documento tem por finalidade apresentar, de forma extensa, técnica e institucionalmente orientada, a estrutura completa do sistema **PCA-MPPI**, incluindo sua organização arquitetural, o conjunto de tecnologias empregadas, os recursos de integração entre front-end e back-end, os principais subsistemas funcionais, os mecanismos de segurança e os pontos relevantes para evolução, manutenção e eventual transferência de responsabilidade técnica. 

O objetivo deste texto é servir como referência para engenheiros de software, arquitetos, analistas e demais profissionais de tecnologia que venham a atuar na manutenção, ampliação, refatoração ou suporte do sistema. Ao invés de funcionar apenas como um manual de operação, este documento busca explicar **como o sistema é estruturado internamente**, quais são suas premissas de desenho e de que forma os módulos dialogam entre si para compor a solução final. 

# ## 2. Visão Geral da Solução 

O **PCA-MPPI** é uma plataforma web institucional desenvolvida para apoiar o Ministério Público do Estado do Piauí no gerenciamento do Plano Anual de Contratações. A aplicação foi concebida para centralizar a entrada, a consolidação, a priorização, o monitoramento e a análise das demandas de contratação, substituindo processos dispersos, planilhas isoladas e controles manuais fragmentados por um ambiente único, rastreável e progressivamente automatizado. 

Do ponto de vista funcional, o sistema opera como um núcleo de governança de contratações. Ele reúne em uma mesma base as informações de planejamento, execução, suspensão, reativação, conformidade, orçamento, relatórios e prazos, permitindo que diferentes perfis institucionais acessem e tratem os dados de acordo com sua competência. Essa característica é particularmente importante porque o PCA não é apenas uma lista de demandas: ele é um instrumento de coordenação administrativa, planejamento orçamentário e acompanhamento da maturidade de contratação ao longo do exercício. 

A solução também incorpora um conceito de **evolução por exercício**, permitindo que o sistema seja utilizado como ambiente de execução para um ano corrente e, simultaneamente, como ambiente de planejamento para exercícios futuros. Isso exige uma arquitetura que suporte segregação lógica por ano, persistência histórica, múltiplos estados das demandas e distinção entre o que pertence ao fluxo operacional ativo e o que deve permanecer apenas para histórico ou análise gerencial. 

# ## 3. Modelo Arquitetural Geral 

A arquitetura do PCA-MPPI pode ser compreendida como uma combinação de três eixos centrais: 

# 1. **Interface cliente em SPA** 

A camada de apresentação é implementada como uma Single Page Application, isto é, uma aplicação em que as navegações entre páginas ocorrem predominantemente no cliente, sem recarregamentos completos de navegador. Esse desenho oferece melhor experiência ao usuário, maior fluidez entre módulos e menor custo de interação em telas complexas.

<!-- pagina 2 -->
# 2. **Backend as a Service com Supabase** 

O sistema utiliza Supabase como plataforma de autenticação, persistência, regras de acesso e execução de rotinas de banco. Nesse modelo, o front-end consome o banco diretamente por meio do cliente Supabase, o que reduz a necessidade de uma camada intermediária tradicional para muitas operações de leitura e gravação. 

# 3. **Gestão assíncrona de dados via React Query** 

As consultas, mutações, caches e revalidações de dados são gerenciadas por TanStack Query. Isso permite que a aplicação seja altamente reativa, reduzindo dependências de estado global e favorecendo a consistência da interface após operações de inclusão, edição, suspensão, reativação ou exclusão. 

Essa combinação estabelece um sistema modular, de rápida resposta ao usuário, com boa separação entre UI, sincronização de estado e persistência. Em termos práticos, trata-se de uma arquitetura adequada para sistemas administrativos de médio porte, com forte intensidade de consulta, atualização em tempo real percebida pelo usuário e necessidade de rastreabilidade. 

## 4. Camadas do Sistema 

Embora a implementação não esteja rigidamente expressa como um monólito em camadas clássico, é possível reconhecer a presença de estratos funcionais claramente delimitados. 

### 4.1. Camada de Apresentação 

É a camada visível ao usuário. Responsável por: 

- renderização das páginas; 

- exibição de tabelas, cards, gráficos, modais e formulários; 

- navegação por rotas; 

- interação com filtros, botões e ações de linha; 

- controle visual do estado das telas. 

Essa camada é desenvolvida em React, com forte apoio de componentes reutilizáveis, Tailwind CSS e bibliotecas de UI acessível. 

### 4.2. Camada de Estado e Orquestração 

É a camada responsável por administrar o estado local e o comportamento assíncrono da aplicação. Ela inclui: 

- estados temporários de UI; 

- abertura e fechamento de modais; 

- controle de abas; 

- critérios de filtragem; 

- cache e invalidação de consultas remotas; 

- sincronização pós-mutation. 

O sistema privilegia o uso de React Query para dados remotos e `useState` para estados localizados de interface, evitando excesso de complexidade em gerenciamento global. 

### 4.3. Camada de Domínio

<!-- pagina 3 -->
É o conjunto de regras de negócio que traduzem o funcionamento institucional do PCA. Essa camada, ainda que distribuída entre hooks, funções utilitárias, páginas e scripts SQL, contém a lógica referente a: 

- demandas ativas; 

- sobrestamento e suspensão; 

- reativação e fusão reversa; 

- orçamento; 

- cálculo de valores estimados e executados; 

- status das demandas; 

- regras de conformidade; 

- priorização e prazos. 

### 4.4. Camada de Persistência 

É composta pelo Supabase/PostgreSQL e por suas estruturas associadas: - tabelas principais do sistema; 

- índices; 

- funções e procedures; 

- triggers; 

- políticas de RLS; 

- migrações SQL; 

- relacionamentos entre entidades. 

Essa camada é a base de verdade dos dados e é onde estão centralizadas as garantias de integridade. 

## 5. Stack Tecnológica 

# ### 5.1. Front-end 

O front-end foi desenhado com uma stack moderna e robusta: 

- **React 18**: composição declarativa da interface. 

- **TypeScript**: segurança de tipos e previsibilidade do código. 

- **Vite**: build rápido e experiência de desenvolvimento eficiente. 

- **Tailwind CSS**: estilização utilitária e consistência visual. 

- **shadcn/ui**: base de componentes reusáveis e acessíveis. 

- **Radix UI**: primitivas acessíveis para menus, dialogs, selects e tabs. 

- **React Router**: navegação client-side. 

- **React Hook Form**: administração de formulários. 

- **Zod**: validação de campos e schemas. 

- **Lucide React**: iconografia consistente. 

- **Framer Motion**: microanimações e refinamento da experiência. 

# ### 5.2. Estado e dados 

- **TanStack Query (React Query v5)**: consultas, cache, revalidação e mutações. 

# ### 5.3. Back-end 

- **Supabase**: autenticação, banco, segurança e acesso aos dados. - **PostgreSQL**: persistência relacional e execução de lógica SQL. - **RLS**: controle refinado de acesso no banco. 

### 5.4. Exportação e documentos

<!-- pagina 4 -->
- **jsPDF** e **jsPDF-AutoTable**: produção de documentos exportáveis diretamente no navegador. 

## 6. Organização de Diretórios e Convenções de Código 

A arquitetura de pastas foi desenhada para facilitar escalabilidade e localização funcional. 

```text src/ ├── components/    # Componentes reutilizáveis e blocos genéricos de interface ├── hooks/         # Hooks customizados e lógica isolada ├── integrations/  # Integrações com APIs e Supabase ├── lib/           # Funções auxiliares e utilidades centrais ├── modules/       # Agrupamento por domínio de negócio ├── pages/         # Páginas e rotas principais ├── utils/         # Funções puras e ferramentas auxiliares ├── App.tsx        # Estrutura principal de rotas e providers └── main.tsx       # Inicialização da aplicação React ``` 

### 6.1. Função esperada de cada diretório - `components/`: fragmentos de UI que se repetem entre telas. - `hooks/`: lógica compartilhada de acesso a dados ou comportamento. - `integrations/`: conexão com serviços externos. - `lib/`: funções base de apoio ao aplicativo. - `modules/`: delimitação por áreas de negócio. - `pages/`: telas correspondentes às rotas. - `utils/`: funções sem estado, puras, focadas em formatação e transformação. 

## 7. Fluxo de Dados e Sincronização 

O sistema foi desenhado para operar com **fonte de verdade remota**, reduzindo duplicações de estado e inconsistências. 

### 7.1. Fluxo padrão de leitura 

1. A página monta. 

2. Um hook ou função de acesso consulta o Supabase. 

3. `useQuery` administra a requisição, cache e revalidação. 

4. Os dados são renderizados em tabelas, cards, gráficos ou formulários. 

### 7.2. Fluxo padrão de escrita 

1. O usuário executa uma ação: salvar, editar, suspender, reativar. 

2. `useMutation` dispara a operação. 

3. O Supabase executa a persistência e validação. 

4. A aplicação invalida queries afetadas. 

5. A interface reflete automaticamente o novo estado. 

### 7.3. Estado de interface

<!-- pagina 5 -->
Estados locais, como modais, filtros, seleção de linha e abas, devem permanecer confinados ao componente ou página responsável. Isso evita poluição do estado e torna a manutenção mais previsível. 

# ## 8. Segurança, Autenticação e Autorização 

# ### 8.1. Autenticação 

A autenticação é feita com o ecossistema do Supabase, que administra login, sessão e persistência do usuário autenticado. 

### 8.2. Controle por perfil 

A aplicação opera com perfis de acesso diferenciados. Isso significa que: 

- nem todas as páginas são visíveis para todos; 

- nem todas as ações aparecem para todos; 

- a UI acompanha o perfil do usuário autenticado. 

# ### 8.3. RLS 

A camada de RLS no PostgreSQL impede acesso indevido aos dados, mesmo que o front-end seja manipulado. Esse ponto é crucial, pois a interface nunca deve ser tratada como mecanismo único de proteção. 

### 8.4. Auditoria 

Sempre que possível, as operações de inclusão, edição, suspensão, reativação ou exclusão devem manter rastreabilidade de: 

- usuário responsável; 

- data e hora; 

- valores anteriores e novos; 

- motivo ou contexto da alteração. 

# ## 9. Módulos Funcionais e Subdomínios 

# ### 9.1. Visão Geral 

Painel executivo com métricas consolidadas do exercício. Reúne indicadores de planejamento, execução e status geral. 

# ### 9.2. Demandas Ativas 

Ambiente de execução principal das contratações em andamento. Suporta filtros, edição, ações em massa e histórico. 

# ### 9.3. Demandas Suspensas 

Área dedicada às demandas afastadas do fluxo principal, incluindo suspensão total e parcial, com mecanismos de reativação. 

# ### 9.4. Nova Contratação 

Tela formal de cadastro de novas demandas. Contém validações, campos obrigatórios e cálculo de atributos derivados. 

### 9.5. Setores Demandantes

<!-- pagina 6 -->
Painel de leitura consolidada por setor, voltado à análise gerencial e à visão orçamentária. 

### 9.6. Controle de Prazos 

Componente temporal do sistema, responsável por monitorar datas previstas, vencimentos e atrasos. 

### 9.7. Riscos e Pendências 

Reúne demandas que requerem intervenção, estejam atrasadas ou prestes a ultrapassar o prazo esperado. 

### 9.8. Prioridades 

Permite leitura estratégica da fila de contratações por relevância institucional. 

### 9.9. Conformidade 

Submódulo de verificação de completude documental e aderência processual. 

### 9.10. Licitações SRP 

Gerencia os casos que seguem o Sistema de Registro de Preços, com lógica e campos específicos. 

### 9.11. Resultados Alcançados 

Apresenta as contratações efetivamente concluídas e consolidadas no exercício. 

### 9.12. Relatórios 

Catálogo central de relatórios para apoio à gestão, auditoria, estratégia e prestação de informações. 

### 9.13. Orçamento 

Concentra a visão de saldo, limite, execução e distribuição por unidade orçamentária. 

### 9.14. Gerenciamento de Usuários 

Permite administrar credenciais, perfis e permissões. 

### 9.15. Notificações 

Canal institucional para avisos e comunicação interna. 

### 9.16. Minha Conta 

Área pessoal de atualização dos dados do usuário logado. 

### 9.17. Tutorial e FAQ 

Documentação operacional integrada ao sistema. 

## 10. Relatórios, Exportação e Documentos Estratégicos 

O subsistema de relatórios é um dos componentes mais relevantes da aplicação, pois traduz os dados transacionais em documentos de leitura executiva. 

# ### 10.1. Tipos de relatórios 

- documento formal do PCA; 

- relatório gerencial completo; 

- relatório de auditoria e conformidade; 

- relatório de riscos e prazos críticos; 

- relatório de demandas suspensas;

<!-- pagina 7 -->
- extrato consolidado de orçamento; - relatório de número de contratos; 

- outros relatórios estratégicos e analíticos. 

### 10.2. Exportação A plataforma gera arquivos em PDF e CSV, permitindo: - análise externa; - compartilhamento institucional; - leitura executiva; - apoio a controles internos; - eventual auditoria ou prestação de contas. 

## 11. Implantação e Ambiente de Execução 

- A implantação segue o padrão de aplicações web modernas: - front-end hospedado em ambiente web; - integração com Supabase; - execução no navegador; 

- persistência centralizada; 

- ambiente local de desenvolvimento baseado em Vite. 

### 11.1. Ambiente local Para subir o projeto: 

- instalar dependências; 

- configurar `.env`; 

- apontar para o projeto Supabase correto; 

- executar o servidor de desenvolvimento. 

### 11.2. Banco e migrações 

Qualquer alteração de estrutura deve ser acompanhada por migração SQL, especialmente quando envolve: 

- novas colunas; - mudanças em RLS; - criação de funções; - triggers; 

- views; 

- tabelas de apoio. 

## 12. Desempenho, Escalabilidade e Extensibilidade 

### 12.1. Desempenho 

O uso de React Query, componentes reutilizáveis e consultas focadas minimiza reprocessamentos desnecessários e melhora a experiência do usuário. 

### 12.2. Escalabilidade 

A estrutura por módulos e por domínio facilita a ampliação do sistema sem reescrita global. 

### 12.3. Extensibilidade

<!-- pagina 8 -->
A adoção de componentes reutilizáveis, hooks e separação por páginas torna o sistema mais apto a receber novos fluxos, relatórios e exercícios anuais. 

## 13. Pontos de Atenção para Evolução 

Ao assumir o código, o engenheiro deve priorizar a leitura dos seguintes aspectos: 

- rotas existentes; 

- estrutura de tabelas no Supabase; 

- políticas de RLS; 

- mecanismos de suspensão e reativação; 

- consultas agregadas dos dashboards; 

- geração de relatórios; 

- validações de formulários; 

- regras específicas de cada exercício. 

A compreensão correta desses pontos evita regressões e mantém a coerência funcional do sistema. 

## 14. Conclusão 

O PCA-MPPI deve ser compreendido como uma solução institucional de governança, planejamento e acompanhamento de contratações, construída sobre uma arquitetura moderna, modular e fortemente dependente de segurança no banco de dados. Seu funcionamento combina SPA, BaaS, tipagem forte, validação declarativa, sincronização assíncrona de estado e documentação operacional integrada. 

Do ponto de vista técnico, a solução oferece uma base sólida para evolução contínua. Contudo, por se tratar de um sistema com regras institucionais específicas, qualquer manutenção deve ser conduzida com atenção aos fluxos de negócio, à integridade dos dados e ao impacto das mudanças sobre relatórios, dashboards, permissões e exercício corrente.
