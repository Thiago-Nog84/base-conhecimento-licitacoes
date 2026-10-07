---
arquivo_original: "Guia Onboarding.pdf"
hash_pdf_md5: 1c8c680d3a5057327db76e6c1d5c6503
paginas: 8
metodo: "texto (pymupdf4llm)"
convertido_em: 2026-10-03T15:07:51
fonte: Base de Conhecimento CLC
---

<!-- pagina 1 -->
# PCA-MPPI — Relatório Técnico e Guia Institucional de Onboarding 

# ## 1. Apresentação Geral 

O presente documento tem por finalidade oferecer uma visão técnica abrangente, detalhada e institucionalmente orientada sobre a solução **PCA-MPPI**, sistema desenvolvido para apoio ao Ministério Público do Estado do Piauí no planejamento, controle, acompanhamento e gestão do Plano Anual de Contratações. O objetivo deste material é servir como referência inicial para qualquer engenheiro de software, desenvolvedor, analista de sistemas ou colaborador técnico que venha a assumir a manutenção, a evolução ou a integração da aplicação em qualquer etapa de seu ciclo de vida. 

A solução foi concebida para substituir controles fragmentados, planilhas descentralizadas e fluxos manuais por uma plataforma web centralizada, auditável e aderente às necessidades institucionais do órgão. Seu desenho contempla tanto a dimensão operacional, voltada ao registro e tramitação de demandas, quanto a dimensão gerencial e estratégica, orientada ao monitoramento de indicadores, controle orçamentário, relatórios, conformidade e rastreabilidade das ações executadas ao longo do exercício. 

Trata-se, portanto, de uma aplicação com natureza híbrida: ao mesmo tempo em que funciona como sistema transacional de registro e acompanhamento de demandas, também opera como instrumento de apoio à governança institucional, à tomada de decisão e à consolidação do planejamento anual das contratações. 

## 2. Contexto Funcional do Sistema 

O PCA-MPPI foi desenvolvido para suportar o ciclo institucional do Plano Anual de Contratações em uma estrutura única, organizada por exercício. Em termos práticos, isso significa que o sistema é capaz de administrar simultaneamente diferentes anos-base, como PCA 2026, PCA 2027 e exercícios futuros, mantendo segregação lógica entre os conjuntos de dados e respeitando a fase em que cada exercício se encontra. 

No plano funcional, a aplicação contempla: 

- cadastro de demandas de contratação; 

- acompanhamento do fluxo de execução; 

- separação entre demandas ativas, suspensas e sobrestadas; 

- análise de prazos e riscos; 

- visualização de indicadores consolidados; 

- extração de relatórios para uso gerencial, estratégico e de auditoria; 

- manutenção de trilhas históricas de alteração; 

- governança de acesso por perfis e permissões. 

Esse arranjo foi desenhado para lidar com o fato de que o Plano Anual de Contratações não é um objeto estático, mas um instrumento vivo, revisável e sujeito a ajustes decorrentes de novas necessidades institucionais, mudanças orçamentárias, suspensão de demandas, replanejamento, adequações de prioridade e transformações no cronograma de execução. 

## 3. Arquitetura de Solução

<!-- pagina 2 -->
A arquitetura adotada pelo PCA-MPPI segue o modelo de **Single Page Application (SPA)**, com front-end desacoplado de um backend como serviço (BaaS), utilizando o Supabase como base central de autenticação, persistência e segurança. Tal desenho favorece simplicidade operacional, rapidez no desenvolvimento, manutenção modular e possibilidade de evolução sem acoplamento excessivo entre interface e camada de dados. 

Do ponto de vista arquitetural, a solução pode ser compreendida em três grandes blocos: 

### 3.1. Camada de Apresentação 

Responsável por toda a experiência visual e interativa do usuário. É implementada em React, com roteamento no lado do cliente e forte uso de componentes reutilizáveis para padronização da interface. 

### 3.2. Camada de Estado e Sincronização 

Responsável pela gestão de dados remotos e sincronização de estados assíncronos, com uso predominante de TanStack Query (React Query), o que reduz a necessidade de estados globais complexos e melhora a previsibilidade das atualizações de tela. 

### 3.3. Camada de Dados e Segurança 

Baseada em Supabase, com PostgreSQL, autenticação nativa, políticas de Row Level Security (RLS) e operações diretas sobre o banco por meio do cliente Supabase. Essa camada concentra as regras de persistência, autorização, integridade e, quando aplicável, rotinas transacionais por meio de SQL, funções e migrações. 

## 4. Stack Tecnológica 

A solução foi construída sobre um conjunto tecnológico moderno e amplamente adotado em aplicações web corporativas. A seguir, são descritos os principais componentes da stack e seu papel específico no projeto. 

### 4.1. Front-end 

- **React 18**: biblioteca principal da interface, utilizada para construção de componentes funcionais, composição declarativa da UI e gerenciamento do ciclo visual da aplicação. - **TypeScript 5.8**: linguagem utilizada em toda a base de código para conferir tipagem estática, previsibilidade, segurança semântica e melhor suporte em tempo de desenvolvimento. - **Vite**: ferramenta de build e servidor de desenvolvimento, adotada por sua velocidade, simplicidade de configuração e excelente experiência em hot reload. 

- **Tailwind CSS**: framework utilitário empregado para estilização e composição visual, reduzindo a necessidade de folhas de estilo extensas e favorecendo consistência visual. - **shadcn/ui**: conjunto de componentes base reutilizáveis e acessíveis, cuja filosofia de uso se ajusta ao projeto por permitir customização sem impor uma camada pesada de abstração. - **Radix UI**: primitives acessíveis que sustentam componentes mais complexos, como dialogs, menus, selects e tabs. 

- **React Router**: biblioteca responsável pelo roteamento e navegação entre páginas da SPA. - **React Hook Form**: gerenciamento de formulários com melhor desempenho e menos rerenderizações. 

- **Zod**: validação declarativa de schemas, empregada para garantir consistência nos dados de entrada. 

- **Lucide React**: biblioteca de ícones, usada em ações, menus, botões e indicações visuais.

<!-- pagina 3 -->
- **Framer Motion**: aplicada em microinterações e animações que reforçam a fluidez visual da aplicação. 

### 4.2. Estado e Data Fetching 

- **TanStack Query (React Query v5)**: pilar do modelo de sincronização de dados assíncronos. É responsável por consulta, cache, invalidação, revalidação e mutações de dados de forma eficiente. 

### 4.3. Back-end e Banco de Dados 

- **Supabase**: plataforma BaaS utilizada para autenticação, persistência de dados, políticas de segurança e integração com o front-end. 

- **PostgreSQL**: banco relacional subjacente, utilizado para armazenar as entidades do domínio do PCA. 

- **Row Level Security (RLS)**: mecanismo nativo do PostgreSQL empregado para restringir o acesso aos registros de acordo com o perfil do usuário e com as regras institucionais definidas. 

### 4.4. Geração de Relatórios 

- **jsPDF** e **jsPDF-AutoTable**: bibliotecas utilizadas na geração de relatórios em PDF diretamente no cliente, especialmente para listagens tabulares e documentos de apoio institucional. 

## 5. Estrutura de Diretórios e Organização Interna 

A estrutura do projeto foi desenhada para favorecer modularidade, legibilidade e separação de responsabilidades. A organização principal está concentrada dentro de `src/`, com divisão por natureza funcional. 

```text 

src/ 

├── components/    # Componentes reutilizáveis e blocos de interface compartilhados ├── hooks/         # Hooks customizados com lógica isolada de consulta, mutação ou transformação de dados ├── integrations/  # Integrações com serviços externos, especialmente o cliente Supabase ├── lib/           # Funções utilitárias centrais, helpers e configurações de suporte ├── modules/       # Agrupamento por domínio de negócio, útil para escalabilidade e separação conceitual 

├── pages/         # Páginas/rotas da aplicação, cada uma representando uma tela funcional ├── utils/         # Funções auxiliares puras, como formatação e geração de documentos ├── App.tsx        # Componente raiz responsável pelas rotas principais 

└── main.tsx       # Entrada principal da aplicação React e configuração dos providers globais 

### 5.1. Diretriz de uso das pastas 

- **components/** deve concentrar elementos visuais reaproveitáveis e independentes de página. 

- **hooks/** deve reunir consultas encapsuladas e lógicas de atualização que se repetem. - **integrations/** deve ser o local preferencial para conexão com Supabase e demais integrações externas. 

- **modules/** deve ser utilizado quando houver necessidade de separar domínios complexos por responsabilidade. 

- **pages/** deve conter as telas que correspondem às rotas principais do sistema. 

- **utils/** deve guardar funções puras e utilidades sem dependência de estado visual.

<!-- pagina 4 -->
# ## 6. Fluxo de Dados e Gerenciamento de Estado 

O PCA-MPPI adota uma estratégia de estado que privilegia a simplicidade operacional e a previsibilidade. Ao invés de manter grandes volumes de dados em contextos globais ou arquiteturas excessivamente centralizadas, o sistema emprega majoritariamente **React Query** para tratar o acesso a dados remotos. 

# ### 6.1. Padrão de uso 

O fluxo típico de dados segue a seguinte sequência: 

1. uma função assíncrona consulta ou persiste informações por meio do Supabase Client; 

2. os dados são consumidos por `useQuery` ou `useMutation`; 

3. ao concluir uma mutação com sucesso, as queries relacionadas são invalidadas; 

4. a interface é revalidada de forma automática, sem necessidade de recarregamento manual da página. 

# ### 6.2. Estado local 

`useState` é reservado para estados de interface e comportamento localizado, como: 

- modais abertos ou fechados; 

- filtros temporários; 

- abas ativas; 

- seleção de linhas; 

- estados transitórios de carregamento visual. 

# ### 6.3. Regra de desenvolvimento 

O repositório adota a premissa de que os dados remotos devem ser tratados como fonte de verdade no servidor, enquanto a interface opera como consumidora e orquestradora de interações. Isso reduz inconsistências e facilita a manutenção em médio prazo. 

# ## 7. Autenticação, Segurança e Autorização 

A aplicação manipula informações institucionais sensíveis, o que exige cuidado com autenticação, autorização e segregação de acesso. 

# ### 7.1. Autenticação 

A autenticação é gerida pelo Supabase, com sessão controlada pelo SDK da plataforma. 

# ### 7.2. Autorização 

O sistema adota controle por perfis de acesso, com diferentes níveis de permissão conforme o papel institucional do usuário. A interface reflete essas permissões e oculta ações incompatíveis com o perfil logado, embora a verdadeira barreira de segurança esteja na camada de banco de dados. 

# ### 7.3. RLS 

As políticas de Row Level Security são parte central da segurança. Elas garantem que: 

- o usuário visualize apenas os registros permitidos; 

- operações de inclusão, edição e exclusão respeitem o perfil; 

- regras de acesso sejam aplicadas no próprio banco, e não apenas no front-end. 

### 7.4. Princípio de segurança adotado

<!-- pagina 5 -->
A interface nunca deve ser tratada como único mecanismo de proteção. O front-end apenas melhora a experiência e reduz erros operacionais; a segurança efetiva deve ser assegurada por políticas de banco e por validações consistentes em toda a cadeia de persistência. 

# ## 8. Módulos Funcionais Principais 

O sistema está organizado em módulos que representam as áreas centrais da operação institucional. 

# ### 8.1. Visão Geral 

Página inicial analítica com indicadores e gráficos consolidados do exercício. É a principal porta de entrada do usuário para visão executiva do sistema. 

# ### 8.2. Demandas Ativas 

Módulo de acompanhamento da carteira executável de demandas. Permite consulta, edição, histórico, filtros e ações operacionais. 

# ### 8.3. Demandas Suspensas 

Módulo destinado às demandas que foram retiradas temporária ou parcialmente do fluxo principal, com possibilidade de reativação, fusão reversa e rastreio histórico. 

# ### 8.4. Nova Contratação 

Formulário formal para cadastramento de novas demandas no PCA, com validações de negócio, atribuição de setor, tipo de contratação, valores e justificativas. 

# ### 8.5. Setores Demandantes 

Módulo gerencial que consolida a distribuição das demandas por setor requisitante, permitindo leitura estratégica da demanda institucional. 

# ### 8.6. Controle de Prazos 

Painel de monitoramento temporal que acompanha a evolução das demandas e alerta sobre vencimentos, atrasos e riscos operacionais. 

# ### 8.7. Riscos e Pendências 

Área voltada à identificação de gargalos, riscos de descumprimento e demandas que precisam de atenção imediata. 

# ### 8.8. Prioridades de Contratação 

Tela que organiza as demandas por prioridade, favorecendo decisões de gestão e rebalanceamento da fila de execução. 

# ### 8.9. Conformidade 

Módulo de verificação documental e regulatória, com foco em assegurar a consistência dos processos e o cumprimento das exigências legais. 

# ### 8.10. Licitações SRP 

Subsistema específico para demandas vinculadas ao Sistema de Registro de Preços, com lógica própria de acompanhamento. 

### 8.11. Resultados Alcançados

<!-- pagina 6 -->
Painéis voltados à leitura dos resultados efetivamente executados, com foco na conclusão das contratações. 

# ### 8.12. Relatórios 

Catálogo de documentos gerenciais, estratégicos e operacionais, com exportações e visualizações específicas para diferentes finalidades institucionais. 

# ### 8.13. Orçamento 

Módulo de apoio à gestão de limites, saldos e visão financeira por unidade ou setor. 

# ### 8.14. Gerenciamento de Usuários 

Área administrativa para controle de perfis, contas, acessos e manutenção cadastral. 

# ### 8.15. Notificações 

Canal interno de avisos e comunicados institucionais. 

# ### 8.16. Minha Conta 

Página voltada à atualização de dados pessoais do usuário autenticado. 

# ### 8.17. Tutorial e FAQ 

Documentação operacional embutida no sistema para orientação dos usuários e suporte ao uso cotidiano. 

## 9. Padrões de Desenvolvimento e Boas Práticas 

A continuidade do projeto deve observar uma série de diretrizes que garantem consistência, previsibilidade e menor risco de regressão. 

# ### 9.1. Tipagem 

- Evitar o uso de `any`. 

- Preferir interfaces explícitas e tipos bem definidos. 

- Quando possível, reutilizar tipagens derivadas do banco. 

# ### 9.2. Formulários 

- Empregar `React Hook Form` em conjunto com `Zod`. 

- Validar entradas tanto no front-end quanto, quando necessário, na camada de persistência. 

# ### 9.3. Estilização 

- Utilizar Tailwind CSS como padrão dominante. 

- Empregar `cn()` para composição segura de classes. 

# ### 9.4. Componentização 

- Reutilizar componentes sempre que uma estrutura visual ou funcional for repetida. 

- Extrair lógica repetida para hooks, utilitários ou módulos dedicados. 

# ### 9.5. Banco de dados 

- Qualquer ajuste estrutural no banco deve ser acompanhado de migração. 

- Mudanças em tabelas, funções ou políticas RLS precisam ser avaliadas quanto ao impacto sistêmico.

<!-- pagina 7 -->
### 9.6. Consultas e desempenho - Evitar consultas desnecessariamente amplas. 

- Indexar colunas relevantes para filtros, relações e políticas de segurança. 

- Revalidar o comportamento das páginas após mutações para impedir inconsistências na interface. 

## 10. Configuração do Ambiente Local ### 10.1. Requisitos mínimos - Node.js 18 ou superior. - NPM ou Yarn. 

- Instância Supabase acessível para desenvolvimento/homologação. ### 10.2. Instalação ```bash git clone https://github.com/mppi/pca-mppi.git cd pca-mppi npm install ``` 

### 10.3. Variáveis de ambiente Crie um arquivo `.env` na raiz do projeto com as credenciais do Supabase: ```env VITE_SUPABASE_URL=SuaURL VITE_SUPABASE_ANON_KEY=SuaChaveAnonima ``` ### 10.4. Execução ```bash npm run dev ``` A aplicação normalmente ficará disponível em: ```bash http://localhost:8080 ``` 

## 11. Diretrizes para Evolução e Manutenção 

Antes de implementar novas funcionalidades ou alterar fluxos existentes, recomenda-se que o engenheiro responsável: 

- verifique o estado atual das rotas e páginas afetadas; 

- examine o esquema do banco e as migrações existentes; 

- confirme o impacto sobre RLS, relatórios e dashboards; 

- valide os efeitos da mudança nos diferentes perfis de acesso; 

- teste em ambiente de desenvolvimento ou homologação antes de promover qualquer alteração para produção.

<!-- pagina 8 -->
A regra prática é tratar o PCA-MPPI não apenas como uma aplicação front-end, mas como um ecossistema institucional que envolve dados, segurança, governança e aderência funcional ao planejamento anual de contratações do órgão. 

## 12. Observações Finais 

Este sistema encontra-se em evolução contínua e possui regras de negócio próprias, fortemente vinculadas ao contexto institucional do MPPI. Por essa razão, qualquer nova implementação deve ser tratada com cautela, observando o encadeamento entre interface, dados, relatórios, permissões e regras de negócio. 

Em síntese, o PCA-MPPI deve ser mantido como uma plataforma de alta confiabilidade, com foco na integridade dos dados, estabilidade da experiência do usuário e aderência permanente aos objetivos estratégicos da instituição.
