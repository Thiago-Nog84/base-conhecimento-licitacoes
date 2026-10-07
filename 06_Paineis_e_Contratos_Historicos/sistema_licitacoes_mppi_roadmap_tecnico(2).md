# Sistema de Gestão de Licitações — MPPI
## Roadmap Técnico · Django / Python
**Órgão:** Ministério Público do Estado do Piauí — CLC / Assessoria de Compras  
**Escopo:** Ciclo interno (PCA → Planejamento → Cotação → SRP → Contratos) — fase externa reservada para fase futura  
**Versão:** 2.0 — Consolidado em junho/2026  
**Alterações v2.0:** Incorporação da análise comparativa de mercado (StartGov, GDL, licito.guru, Compras.gov.br, Betha, IPM, BLL, BNC, Banco de Preços, Fonte de Preços); decisão formal de exclusão da fase externa do escopo; SRP elevado a diferencial central; dashboard SRP com 4 dimensões; analytics de SRP; qualidade de dados PNCP; signals SEI; função IA para conformidade de ARP; regras transversais para o Claude Code; testes unitários expandidos; checklist atualizado.

---

## 0. Posicionamento de mercado e decisões estratégicas de escopo

### 0.1 Panorama competitivo

Análise realizada em junho/2026 das principais ferramentas do mercado brasileiro de gestão de licitações para órgãos públicos:

| Categoria | Ferramentas | Característica |
|---|---|---|
| Sistemas oficiais | Compras.gov.br / PGC / ETP Digital / Contratos.gov.br / PNCP | Gratuitos, abrangentes, usabilidade datada, qualidade de dados criticada pelo TCU |
| ERPs públicos | Betha, IPM Atende.Net | Cobertura transacional ampla, pouca IA generativa |
| Startups de IA | StartGov, GDL/Exponencial CTI, licito.guru | IA em documentos da fase interna, escopo estreito |
| Plataformas de pregão | BLL, BNC, Portal de Compras Públicas, Licitar Digital | Fase externa e pesquisa de preços |
| Bancos de preços | Banco de Preços (Negócios Públicos), Fonte de Preços | Pesquisa multifonte, saneamento estatístico |

### 0.2 Lacunas identificadas e impacto no projeto

| Lacuna de mercado identificada | Decisão para este projeto |
|---|---|
| **Nenhuma startup cobre o ciclo SRP completo** (ARPs originadas + contratações decorrentes + caronas cedidas + caronas recebidas) | **SRP é o maior diferencial competitivo — prioridade máxima no Estágio 1** |
| Fase externa (pregão/disputa) requer homologação SEGES/MGI e infraestrutura WebSocket própria | **Fase externa FORA DO ESCOPO** — reservada para fase futura após consulta ao CNMP |
| Nenhuma startup integra ao SEI (expediente padrão de órgãos federais e MPs estaduais) | Integração SEI/MPPI planejada para Estágio 2 como diferencial exclusivo |
| 86,4% dos registros do PNCP com inconsistências (Acórdão TCU 2916/2025) | Validação CATMAT/CATSER obrigatória antes de qualquer publicação no PNCP |
| Pesquisa de preços sem "cesta de preços" multifonte adequada | Implementar conforme Acórdão TCU 1712/2025 — múltiplas fontes com saneamento estatístico |
| StartGov substitui o SEI por módulo próprio; GDL e licito.guru não têm expediente | Sistema MPPI integra ao SEI nativo — não substitui o expediente institucional |

### 0.3 Decisão formal: fase externa fora do escopo

A fase externa (pregão eletrônico, sala de disputa em tempo real, habilitação eletrônica) é um produto por si só, com requisitos regulatórios, técnicos e de disponibilidade incompatíveis com o ciclo interno:

- **Regulatório:** exige homologação SEGES/MGI e, para MPs, validação do CNMP sobre uso de plataforma eletrônica própria vs. adesão a plataforma já homologada (BLL, BNC, Licitar Digital)
- **Técnico:** sala de disputa exige WebSocket em tempo real (Django Channels + Redis), disponibilidade 99,9%+ durante janelas de pregão e infraestrutura de alta disponibilidade
- **Escopo:** o valor do sistema está no ciclo interno — planning, cotação, SRP e contratos — que nenhuma solução cobre adequadamente para órgãos estaduais do MP

**Implementação:** criar placeholder `apps/licitacao/fase_externa/README.md` documentando essa decisão e os pré-requisitos para futura implementação. Nunca criar endpoints, views ou models relacionados a lances, disputa ou pregão eletrônico sem decisão explícita.

### 0.4 Regras transversais para o Claude Code

As regras abaixo aplicam-se a todas as implementações deste projeto, em todos os estágios:

1. **`numero_sei` obrigatório em todo model principal** — é o identificador de rastreabilidade no SEI/MPPI
2. **Fundamento legal nos docstrings** — citar o normativo exato (ex: `"Ato PGJ 1381/2024, art. 7º, §1º"`)
3. **Fase externa = fora do escopo** — nunca criar endpoints, views ou models relacionados a sala de disputa, lances ou pregão eletrônico
4. **SRP é o diferencial central** — implementar com máxima fidelidade; validações de saldo e carona são críticas e não podem ser simplificadas
5. **PNCP é condição de eficácia** — contratos sem publicação no PNCP são ineficazes (art. 174 NLLC); nunca silenciar erro de publicação
6. **Limites de dispensa em settings** — nunca hardcodar `R$ 50.000` / `R$ 100.000` no código; sempre referenciar `settings.LIMITE_DISPENSA_*` para facilitar atualização por decreto
7. **IA sempre com disclaimer de revisão** — todo documento gerado por IA deve conter aviso de revisão obrigatória antes de autuação no SEI/MPPI



### 1.1 Posição institucional
O MPPI é órgão do Ministério Público estadual com autonomia funcional e administrativa (art. 127 CF/88 e Lei Orgânica do MPPI). Não integra o Poder Executivo estadual, razão pela qual:
- O Decreto Estadual 21.872/2023 aplica-se **subsidiariamente** (Ato PGJ 1382/2024, art. 1º, §1º)
- Os regulamentos da **União** (INs SEGES, modelos AGU) aplicam-se **primariamente**, por opção expressa do MPPI (Ato PGJ 1382/2024, art. 1º caput e §2º acrescentado pelo Ato PGJ 1413/2024)
- As **Resoluções do CNMP** têm força normativa obrigatória para todos os MPs estaduais
- A **PGE-PI** não é o órgão de assessoramento jurídico do MPPI — essa função é exercida pela **APPL** (Assessoria para Pareceres em Processos Licitatórios), conforme Ato PGJ 1414/2024, art. 14

### 1.2 Framework normativo hierarquizado

| Nível | Normativo | Aplicação no MPPI |
|---|---|---|
| 1 — Constitucional | CF/88, arts. 127–130 | Base da autonomia do MP |
| 2 — Lei federal | Lei 14.133/2021 (NLLC) | Eixo central — aplicação integral |
| 3 — CNMP | Res. CNMP 283/2024 (TIC) | Obrigatória para contratações de TI |
| 4 — Federal (INs) | IN SEGES 65/2021 (preços), IN 58/2022 (ETP), IN 81/2022 (TR), IN 67/2021 (dispensa eletrônica) | Aplicadas por opção expressa (Ato PGJ 1382/2024) |
| 5 — AGU (modelos) | Minutas padronizadas AGU (bens, serviços, TIC, contratação direta) | Adotados pelo MPPI (Ato PGJ 1413/2024, §2º) |
| 6 — Estadual (subsidiário) | Decreto 21.872/2023, Decreto 21.938/2023 (SRP-PI) | Subsidiário, no que for cabível |
| 7 — Interno MPPI | Ato PGJ 1381/2024 (PCA), 1382/2024+1413/2024 (impl. 14133), 1383/2024 (dispensa parecer), 1414/2024+1448/2024 (agente contratação), 1415/2024 (serviços contínuos) | Vinculante — prioridade sobre os demais |

### 1.3 Estrutura organizacional relevante

```
PGJ (Procurador-Geral de Justiça)
│
├── APPL — Assessoria para Pareceres em Processos Licitatórios
│   └── Controle prévio de legalidade de editais, minutas, termos aditivos
│
├── APG — Assessoria de Planejamento e Gestão
│   └── Co-responsável pela consolidação e monitoramento do PCA (Ato 1381/2024, art. 5º)
│
└── CLC — Coordenadoria de Licitações e Contratos
    │
    └── Assessoria de Compras (chefiada por [nome do usuário] — Assessor de Compras / Agente de Contratação)
        ├── Consolidação do PCA
        ├── Fase preparatória (validação de DFD, ETP, TR, Mapa de Risco, Pesquisa de Preços)
        ├── Condução e julgamento dos procedimentos licitatórios
        └── Governança, gestão de equipe e tecnologia
```

**Unidades requisitantes do MPPI** (Ato PGJ 1381/2024, art. 7º, §1º):
CPPT, CTI, CAA, CRH, GSI, CEAF, CI, CLC, CCF, APG, GAECO, FPROCON, CCS

### 1.4 Fluxo de aprovação do PCA (Ato PGJ 1381/2024)

```
10–30 jul    → Unidades requisitantes inserem demandas (DFD incluído)
1–20 ago     → CLC + APG analisam e consolidam
até 30 ago   → PGJ aprova
até 30 ago   → Publicação no PNCP e Portal de Transparência (art. 11º, §4º)
1–30 out     → 1ª revisão (adequação à proposta orçamentária)
até 30d úteis após LOA → 2ª revisão (adequação à LOA aprovada)
jul/set/nov  → Relatórios bimestrais de riscos de não efetivação (art. 17º)
```

### 1.5 Dispensa de análise jurídica (Ato PGJ 1383/2024)
Não é obrigatória manifestação da APPL nas contratações diretas de pequeno valor (art. 75, I, II e §3º e art. 74 até os limites do art. 75, I e II da Lei 14.133/2021), **salvo**:
- Celebração de contrato não baseado em modelo padronizado do MPPI
- Dúvida do administrador sobre a legalidade

### 1.6 Particularidades do SRP para o MPPI
O Decreto Estadual **21.938/2023** regulamenta o SRP no âmbito do Piauí. Aplica-se subsidiariamente ao MPPI. Pontos de atenção em relação ao Decreto Federal 11.462/2023:
- Verificar limites de carona e procedimentos de autorização específicos do Decreto 21.938/2023
- O MJR 86/2025 (Manifestação Jurídico Referencial sobre Adesão a ARP) é a orientação interna do MPPI para caronas — deve orientar as validações do sistema
- O MJR 95/2025 (Prorrogação de ARP) orienta os critérios de prorrogação

**O módulo SRP é o maior diferencial competitivo deste sistema.** Análise de mercado (junho/2026) confirmou que nenhuma startup (StartGov, GDL/Exponencial CTI, licito.guru) implementa o ciclo completo. O Compras.gov.br e os ERPs (Betha, IPM) cobrem parcialmente. As quatro dimensões que o sistema deve cobrir de forma integrada:

| Dimensão | Descrição | Lacuna no mercado |
|---|---|---|
| **ARPs originadas** | Atas geradas pelo MPPI como órgão gerenciador — itens, saldos, vigências | Ausente em todas as startups |
| **Contratações decorrentes** | Pedidos de fornecimento emitidos com base em ARP própria — débito automático de saldo | Ausente em todas as startups |
| **Caronas cedidas** | Órgãos externos que aderiram às ARPs do MPPI — controle do limite de 50%/item (Dec. 11.462/2023, art. 29 / MJR 86/2025) | Ausente em todas as startups |
| **Caronas recebidas** | ARPs de outros órgãos às quais o MPPI aderiu — saldo autorizado vs. utilizado | Ausente em todas as startups |



### 1.7 Contratações de TI — Res. CNMP 283/2024
Para todas as contratações de soluções de TIC no MPPI, a Resolução CNMP 283/2024 é obrigatória e estabelece:
- **Equipe de Planejamento** tripartite: Integrante Requisitante + Técnico + Administrativo
- **ETP com TCO** (Total Cost of Ownership) obrigatório
- **Equipe de Gestão e Fiscalização** quadripartite: fiscal requisitante + técnico + administrativo + gestor
- Modalidade de remuneração: pontos de função, sprint, alocação com resultados etc.
- **MOTec** (Manual de Orientações Técnicas) como instrumento obrigatório
- Vedações específicas (art. 19º): indicar pessoas, exigir credenciamento de fabricante para habilitação etc.

### 1.8 Dispensa de parecer jurídico — impacto no sistema
O sistema deve controlar automaticamente se uma contratação direta exige ou não manifestação da APPL com base nos limites do Ato PGJ 1383/2024 e nos valores vigentes (atualizados pelos Decretos Federais 12.343/2024 e 12.807/2025).

---

## 2. Estágio 1 — Fundação (0–12 meses)

### Objetivo
Entregar o núcleo transacional aderente ao framework normativo do MPPI: do PCA à execução contratual, com SRP completo, respeitando os fluxos internos de aprovação e os normativos identificados.

---

### 2.1 Estrutura Django — Apps e responsabilidades

```
mppi_licitacoes/
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── core/              # Orgao, UnidadeRequisitante, Perfil, Usuario
│   ├── pca/               # PlanoContratacaoAnual, ItemPCA, DFD
│   ├── planejamento/      # ETP, MatrizRisco, TermoReferencia, EquipePlanejamento (TI)
│   ├── cotacao/           # PesquisaPrecos, FontePreco, ItemCotacao
│   ├── licitacao/         # ProcessoLicitatorio, metadados de edital
│   ├── srp/               # AtaRegistroPrecos, ContratacaoDecorrente, Adesao, ARPExterna
│   ├── contratos/         # Contrato, Aditivo, Apostilamento, OrdemFornecimento
│   ├── juridico/          # ControleJuridico, ManifestacaoAPPL, MJR
│   ├── pncp/              # Client API PNCP, serializers, Celery tasks
│   └── notificacoes/      # Alertas de vigência, saldo, prazos do PCA
├── manage.py
└── requirements.txt
```

---

### 2.2 App `core` — Entidades base do MPPI

```python
# apps/core/models.py

class Orgao(models.Model):
    """
    Representa o MPPI e seus fundos (FPROCON, etc.).
    O MPPI é órgão do MP estadual — não integra o Executivo.
    """
    nome            = models.CharField(max_length=255,
                        default='Ministério Público do Estado do Piauí')
    sigla           = models.CharField(max_length=20, default='MPPI')
    cnpj            = models.CharField(max_length=18, unique=True)
    # MPPI não possui UASG — usa código próprio no PNCP
    pncp_codigo_orgao = models.CharField(max_length=50, blank=True)
    uf              = models.CharField(max_length=2, default='PI')
    esfera          = models.CharField(max_length=20, default='estadual_mp')
    ativo           = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Órgão'


class UnidadeRequisitante(models.Model):
    """
    Unidades requisitantes do MPPI conforme Ato PGJ 1381/2024, art. 7º, §1º.
    CPPT, CTI, CAA, CRH, GSI, CEAF, CI, CLC, CCF, APG, GAECO, FPROCON, CCS.
    """
    UNIDADES_FIXAS = [
        ('CPPT',    'CPPT — Coordenadoria de Patrimônio e Prestação de Contas'),
        ('CTI',     'CTI — Coordenadoria de Tecnologia da Informação'),
        ('CAA',     'CAA — Coordenadoria de Apoio Administrativo'),
        ('CRH',     'CRH — Coordenadoria de Recursos Humanos'),
        ('GSI',     'GSI — Gerência de Segurança Institucional'),
        ('CEAF',    'CEAF — Centro de Estudos e Aperfeiçoamento Funcional'),
        ('CI',      'CI — Coordenadoria de Infraestrutura'),
        ('CLC',     'CLC — Coordenadoria de Licitações e Contratos'),
        ('CCF',     'CCF — Coordenadoria de Contabilidade e Finanças'),
        ('APG',     'APG — Assessoria de Planejamento e Gestão'),
        ('GAECO',   'GAECO — Grupo de Atuação Especial Contra o Crime Organizado'),
        ('FPROCON', 'FPROCON — Fundo de Proteção ao Consumidor'),
        ('CCS',     'CCS — Coordenadoria de Comunicação Social'),
    ]
    orgao           = models.ForeignKey(Orgao, on_delete=models.CASCADE, related_name='unidades')
    sigla           = models.CharField(max_length=20, choices=UNIDADES_FIXAS)
    nome            = models.CharField(max_length=255)
    responsavel     = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                        on_delete=models.SET_NULL, related_name='unidades_responsavel')
    ativo           = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Unidade Requisitante'


class Perfil(models.Model):
    """
    Perfis de acesso conforme os normativos do MPPI.
    Ato PGJ 1414/2024: agente, equipe apoio, comissão.
    Ato PGJ 1381/2024: requisitante, área técnica, setor licitações, autoridade.
    Res. CNMP 283/2024: equipe de planejamento TI, equipe de gestão TI.
    """
    PERFIS = [
        # Fase interna — planejamento
        ('requisitante',        'Requisitante (art. 7º Ato PGJ 1381/2024)'),
        ('area_tecnica',        'Área Técnica'),
        ('apg',                 'APG — Assessoria de Planejamento e Gestão'),
        # CLC / Assessoria de Compras
        ('assessor_compras',    'Assessor de Compras / Agente de Contratação'),
        ('equipe_apoio',        'Equipe de Apoio (Ato PGJ 1414/2024)'),
        ('comissao',            'Membro de Comissão de Contratação'),
        # Jurídico
        ('appl',                'APPL — Assessoria para Pareceres em Processos Licitatórios'),
        # Gestão de contratos
        ('gestor_contrato',     'Gestor de Contrato'),
        ('fiscal_adm',          'Fiscal Administrativo'),
        ('fiscal_tecnico',      'Fiscal Técnico'),
        ('fiscal_requisitante', 'Fiscal Requisitante (TI — Res. CNMP 283/2024)'),
        # TI
        ('int_requisitante_ti', 'Integrante Requisitante TI (Res. CNMP 283/2024)'),
        ('int_tecnico_ti',      'Integrante Técnico TI (Res. CNMP 283/2024)'),
        ('int_administrativo_ti','Integrante Administrativo TI (Res. CNMP 283/2024)'),
        # Autoridade
        ('autoridade',          'Autoridade Competente (PGJ ou delegado)'),
        ('auditor',             'Auditor Interno'),
    ]
    usuario         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    orgao           = models.ForeignKey(Orgao, on_delete=models.CASCADE)
    perfil          = models.CharField(max_length=30, choices=PERFIS)
    unidade         = models.ForeignKey(UnidadeRequisitante, null=True, blank=True,
                        on_delete=models.SET_NULL)
    ativo           = models.BooleanField(default=True)

    class Meta:
        unique_together = ('usuario', 'orgao', 'perfil')
        verbose_name = 'Perfil de Acesso'
```

---

### 2.3 App `pca` — Plano de Contratações Anual

```python
# apps/pca/models.py
# Base legal: Ato PGJ 1381/2024 + art. 12, VII, NLLC + art. 8º Decreto 21.872/2023

class PlanoContratacaoAnual(models.Model):
    """
    PCA do MPPI para um exercício fiscal.
    Fluxo de status baseado no Ato PGJ 1381/2024, arts. 10–12.
    """
    STATUS = [
        ('coleta',          'Coleta de demandas (10–30 jul)'),
        ('consolidacao',    'Consolidação CLC + APG (1–20 ago)'),
        ('aprovacao',       'Aguardando aprovação PGJ'),
        ('aprovado',        'Aprovado pelo PGJ'),
        ('publicado_pncp',  'Publicado no PNCP'),
        ('revisao_out',     'Em revisão (1–30 out)'),
        ('revisao_loa',     'Em revisão pós-LOA'),
    ]
    orgao               = models.ForeignKey('core.Orgao', on_delete=models.CASCADE)
    exercicio           = models.PositiveIntegerField()
    status              = models.CharField(max_length=20, choices=STATUS, default='coleta')
    # Datas do calendário (Ato PGJ 1381/2024)
    prazo_coleta_inicio = models.DateField(null=True, blank=True)   # 10 jul
    prazo_coleta_fim    = models.DateField(null=True, blank=True)   # 30 jul
    prazo_consolidacao_fim = models.DateField(null=True, blank=True) # 20 ago
    prazo_aprovacao_fim = models.DateField(null=True, blank=True)   # 30 ago
    data_aprovacao_pgj  = models.DateField(null=True, blank=True)
    data_publicacao_pncp = models.DateTimeField(null=True, blank=True)
    pncp_sequencial     = models.CharField(max_length=100, blank=True)
    # Aprovação
    aprovado_por        = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                            on_delete=models.SET_NULL, related_name='pcas_aprovados')
    observacoes_pgj     = models.TextField(blank=True)
    criado_em           = models.DateTimeField(auto_now_add=True)
    atualizado_em       = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('orgao', 'exercicio')
        verbose_name = 'Plano de Contratação Anual'
        ordering = ['-exercicio']


class DocumentoFormalizacaoDemanda(models.Model):
    """
    DFD — Documento de Formalização de Demanda.
    Fundamenta a inclusão do item no PCA (Ato PGJ 1381/2024, art. 8º, I).
    Elaborado pela unidade requisitante; instrução no SEI.
    """
    STATUS = [
        ('rascunho', 'Rascunho'),
        ('enviado',  'Enviado ao setor de licitações'),
        ('aprovado', 'Aprovado'),
        ('devolvido','Devolvido para adequação'),
    ]
    pca                 = models.ForeignKey(PlanoContratacaoAnual, on_delete=models.CASCADE,
                            related_name='dfds')
    unidade             = models.ForeignKey('core.UnidadeRequisitante', on_delete=models.CASCADE)
    numero_sei          = models.CharField(max_length=30, blank=True,
                            help_text='Número do processo SEI/MPPI onde está autuado o DFD')
    numero_dfd          = models.CharField(max_length=30, blank=True)
    descricao_objeto    = models.TextField()
    justificativa       = models.TextField(
                            help_text='Motivação da necessidade; base: art. 6º Ato PGJ 1381/2024')
    prazo_necessidade   = models.DateField()
    grau_prioridade     = models.CharField(max_length=10,
                            choices=[('baixo','Baixo'),('medio','Médio'),('alto','Alto')])
    status              = models.CharField(max_length=15, choices=STATUS, default='rascunho')
    requisitante        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                            null=True, related_name='dfds_requisitados')
    criado_em           = models.DateTimeField(auto_now_add=True)


class ItemPCA(models.Model):
    """
    Item individual do PCA (Ato PGJ 1381/2024, art. 7º).
    Inclui todos os campos obrigatórios listados nos incisos I–XIII do art. 7º.
    """
    CATEGORIAS = [
        ('material',    'Material (CATMAT)'),
        ('servico',     'Serviço (CATSER)'),
        ('obras',       'Obras e Serviços de Engenharia'),
        ('solucao_ti',  'Solução de TIC (Res. CNMP 283/2024)'),
        ('publicidade', 'Publicidade (Dec. 21.813/2023)'),
    ]
    TIPO_CONTRATACAO = [
        ('licitacao',           'Licitação'),
        ('dispensa',            'Contratação Direta — Dispensa'),
        ('inexigibilidade',     'Contratação Direta — Inexigibilidade'),
        ('adesao_arp',          'Adesão a ARP (Carona)'),
        ('renovacao_contrato',  'Renovação de Contrato'),
        ('renovacao_arp',       'Prorrogação de ARP'),
    ]
    dfd                 = models.ForeignKey(DocumentoFormalizacaoDemanda, on_delete=models.CASCADE,
                            related_name='itens')
    numero_item         = models.PositiveIntegerField(help_text='Inciso I — art. 7º Ato 1381/2024')
    # Inciso I: tipo e código do item
    categoria           = models.CharField(max_length=20, choices=CATEGORIAS)
    codigo_catmat_catser = models.CharField(max_length=20, blank=True,
                            help_text='§1º (segundo) art. 7º — nível de classe mínimo')
    # Inciso II: unidade de fornecimento
    unidade_fornecimento = models.CharField(max_length=30)
    # Inciso III: quantidade
    quantidade_estimada = models.DecimalField(max_digits=14, decimal_places=4)
    # Inciso IV: descrição sucinta
    descricao           = models.TextField()
    # Inciso V: justificativa (herdada do DFD)
    # Inciso VI: tipo de contratação
    tipo_contratacao    = models.CharField(max_length=25, choices=TIPO_CONTRATACAO)
    # Inciso VII: estimativa preliminar de valor
    valor_unitario_estimado  = models.DecimalField(max_digits=14, decimal_places=2)
    valor_total_estimado     = models.DecimalField(max_digits=16, decimal_places=2)
    # Inciso VIII: grau de prioridade (herdado do DFD)
    # Inciso IX: data de vencimento do contrato anterior
    data_vencimento_contrato_anterior = models.DateField(null=True, blank=True)
    # Inciso X: data pretendida para conclusão
    data_pretendida_conclusao = models.DateField(null=True, blank=True)
    # Inciso XI: vinculação/dependência
    item_dependente     = models.ForeignKey('self', null=True, blank=True,
                            on_delete=models.SET_NULL, related_name='dependentes')
    # Inciso XII: área requisitante e responsável (no DFD)
    # Inciso XIII: outras informações
    observacoes         = models.TextField(blank=True)
    # SRP
    is_srp              = models.BooleanField(default=False,
                            help_text='Será contratado via SRP (art. 82 NLLC)')
    justificativa_srp   = models.TextField(blank=True)
    # Rastreabilidade
    etp                 = models.ForeignKey('planejamento.ETP', null=True, blank=True,
                            on_delete=models.SET_NULL, related_name='itens_pca')

    class Meta:
        verbose_name = 'Item do PCA'
        ordering = ['numero_item']
```

---

### 2.4 App `planejamento` — Fase interna (arts. 17–76 Dec. 21.872/2023 + Ato PGJ 1381/2024)

```python
# apps/planejamento/models.py

class ETP(models.Model):
    """
    Estudo Técnico Preliminar — art. 18 NLLC + IN SEGES 58/2022.
    Aplicada ao MPPI por opção do Ato PGJ 1382/2024.
    Para TI: conteúdo ampliado pela Res. CNMP 283/2024 (arts. 10–16), incluindo TCO.
    Dispensado nas hipóteses do Decreto 21.872/2023, art. 27.
    """
    STATUS = [
        ('rascunho',    'Rascunho'),
        ('em_revisao',  'Em revisão'),
        ('aprovado',    'Aprovado'),
    ]
    item_pca        = models.OneToOneField('pca.ItemPCA', on_delete=models.CASCADE,
                        related_name='etp', null=True, blank=True)
    numero_sei      = models.CharField(max_length=30, blank=True,
                        help_text='Número do processo SEI/MPPI')
    numero_etp      = models.CharField(max_length=30)
    is_ti           = models.BooleanField(default=False,
                        help_text='Contratação de TIC — aplica Res. CNMP 283/2024')
    # Campos padrão IN SEGES 58/2022
    necessidade_contratacao     = models.TextField()
    requisitos_contratacao      = models.TextField()
    levantamento_mercado        = models.TextField()
    descricao_solucao           = models.TextField()
    estimativa_quantidade       = models.TextField()
    estimativa_custo            = models.DecimalField(max_digits=16, decimal_places=2, null=True)
    justificativa_parcelamento  = models.TextField()
    contratacoes_correlatas     = models.TextField(blank=True)
    alinhamento_pca             = models.TextField(
                                    help_text='Vinculação com o PCA vigente')
    resultados_pretendidos      = models.TextField()
    providencias_previas        = models.TextField(blank=True)
    impactos_ambientais         = models.TextField(
                                    help_text='Art. 11, I, NLLC — sustentabilidade')
    declaracao_viabilidade      = models.BooleanField(default=False)
    # Campos adicionais para TI (Res. CNMP 283/2024, art. 10)
    tco_total                   = models.DecimalField(max_digits=16, decimal_places=2,
                                    null=True, blank=True,
                                    help_text='TCO — Total Cost of Ownership (art. 10, Res. CNMP 283/2024)')
    solucao_em_outros_orgaos    = models.TextField(blank=True,
                                    help_text='Res. CNMP 283/2024, art. 10 — levantamento de mercado TI')
    software_livre_avaliado     = models.BooleanField(default=False)
    # IA e revisão
    gerado_por_ia               = models.BooleanField(default=False)
    ia_modelo_utilizado         = models.CharField(max_length=50, blank=True)
    ia_revisado_por             = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
                                    blank=True, on_delete=models.SET_NULL,
                                    related_name='etps_revisados')
    status                      = models.CharField(max_length=15, choices=STATUS, default='rascunho')
    # Dispensa de ETP (Decreto 21.872/2023, art. 27)
    etp_dispensado              = models.BooleanField(default=False)
    fundamento_dispensa_etp     = models.CharField(max_length=200, blank=True,
                                    help_text='Ex: art. 75, I, Lei 14.133/2021 — abaixo do limite')
    atualizado_em               = models.DateTimeField(auto_now=True)


class EquipePlanejamentoTI(models.Model):
    """
    Equipe de Planejamento para contratações de TIC.
    Res. CNMP 283/2024, art. 9º — tripartite: Requisitante + Técnico + Administrativo.
    """
    etp                 = models.OneToOneField(ETP, on_delete=models.CASCADE,
                            related_name='equipe_planejamento_ti')
    integrante_requisitante  = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.SET_NULL, null=True,
                                related_name='ep_requisitante')
    integrante_tecnico       = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.SET_NULL, null=True,
                                related_name='ep_tecnico')
    integrante_administrativo = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.SET_NULL, null=True,
                                related_name='ep_administrativo')
    lider                   = models.CharField(max_length=20,
                                choices=[('requisitante','Requisitante'),
                                         ('tecnico','Técnico'),
                                         ('administrativo','Administrativo')],
                                default='requisitante',
                                help_text='Preferencialmente o Requisitante — art. 9º Res. CNMP 283/2024')
    ato_designacao_sei      = models.CharField(max_length=30, blank=True)


class MatrizRisco(models.Model):
    """
    Mapa e Matriz de Riscos.
    Decreto 21.872/2023, arts. 29–34; art. 8º, IV, Ato PGJ 1381/2024.
    Matriz obrigatória para contratos acima de 2% do limite do art. 6º, XXII, NLLC.
    Metodologia 5×5 (probabilidade × impacto).
    Para TI: Res. CNMP 283/2024, art. 45.
    """
    etp                 = models.OneToOneField(ETP, on_delete=models.CASCADE,
                            related_name='matriz_risco')
    # Res. CNMP 283/2024, art. 45: mapa deve cobrir todas as três fases
    fase_atual          = models.CharField(max_length=20,
                            choices=[('planejamento','Planejamento'),
                                     ('selecao','Seleção'),
                                     ('gestao','Gestão')],
                            default='planejamento')

class RiscoItem(models.Model):
    PROBABILIDADE   = [(1,'Muito baixa'),(2,'Baixa'),(3,'Média'),(4,'Alta'),(5,'Muito alta')]
    IMPACTO         = [(1,'Muito baixo'),(2,'Baixo'),(3,'Médio'),(4,'Alto'),(5,'Muito alto')]
    RESPONSAVEL     = [('adm','Administração'),('contratado','Contratado'),
                       ('compartilhado','Compartilhado')]
    matriz          = models.ForeignKey(MatrizRisco, on_delete=models.CASCADE, related_name='itens')
    descricao_risco = models.TextField()
    causa           = models.TextField()
    consequencia    = models.TextField()
    probabilidade   = models.PositiveSmallIntegerField(choices=PROBABILIDADE)
    impacto         = models.PositiveSmallIntegerField(choices=IMPACTO)
    nivel_risco     = models.PositiveSmallIntegerField(editable=False)
    responsavel     = models.CharField(max_length=20, choices=RESPONSAVEL)
    acao_preventiva = models.TextField()
    acao_contingencia = models.TextField()

    def save(self, *args, **kwargs):
        self.nivel_risco = self.probabilidade * self.impacto
        super().save(*args, **kwargs)


class TermoReferencia(models.Model):
    """
    Termo de Referência.
    Art. 8º, III, Ato PGJ 1381/2024 + art. 6º, XXIII, NLLC + IN SEGES 81/2022.
    Aplicada ao MPPI por opção do Ato PGJ 1382/2024.
    Para TI: conteúdo ampliado pela Res. CNMP 283/2024 (arts. 17–20).
    Modelo base: AGU (adotado pelo Ato PGJ 1413/2024, §2º).
    Vedações TI: art. 19 Res. CNMP 283/2024 registradas no campo 'vedacoes_ti'.
    """
    STATUS = [
        ('rascunho',    'Rascunho'),
        ('em_revisao',  'Em revisão'),
        ('appl',        'Aguardando análise APPL'),
        ('aprovado',    'Aprovado'),
        ('publicado',   'Publicado'),
    ]
    etp             = models.OneToOneField(ETP, on_delete=models.CASCADE,
                        related_name='termo_referencia')
    numero_sei      = models.CharField(max_length=30, blank=True)
    objeto          = models.TextField()
    fundamentacao_legal = models.TextField(
                        help_text='Inclui referência ao ETP e normativos aplicáveis ao MPPI')
    descricao_solucao = models.TextField()
    requisitos_habilitacao = models.TextField()
    criterio_julgamento = models.CharField(max_length=30,
                            choices=[('menor_preco','Menor Preço'),
                                     ('maior_desconto','Maior Desconto'),
                                     ('melhor_tecnica','Melhor Técnica e Preço'),
                                     ('maior_retorno','Maior Retorno Econômico')])
    prazo_execucao  = models.PositiveIntegerField(help_text='Em dias')
    local_execucao  = models.TextField()
    obrigacoes_contratante  = models.TextField()
    obrigacoes_contratado   = models.TextField()
    criterios_medicao       = models.TextField()
    # Serviços contínuos — Ato PGJ 1415/2024
    is_servico_continuo     = models.BooleanField(default=False)
    prazo_inicial_meses     = models.PositiveSmallIntegerField(null=True, blank=True,
                                help_text='Mín. 24 meses para serviços contínuos — art. 5º Ato 1415/2024')
    prazo_maximo_meses      = models.PositiveSmallIntegerField(null=True, blank=True,
                                help_text='Máx. 120 meses (prazo decenal)')
    # SRP
    is_srp                  = models.BooleanField(default=False)
    justificativa_srp       = models.TextField(blank=True)
    # TI — Res. CNMP 283/2024
    modalidade_remuneracao_ti = models.CharField(max_length=30, blank=True,
                                choices=[
                                    ('pontos_funcao',   'Pontos de função + horas'),
                                    ('sprint',          'Valor fixo por sprint'),
                                    ('alocacao',        'Alocação vinculada a resultados'),
                                    ('fixo_mensal',     'Valor fixo mensal por sistema'),
                                    ('fixo_alocacao',   'Fixo por alocação com resultados'),
                                ])
    vedacoes_ti_observadas  = models.BooleanField(default=False,
                                help_text='Confirmação de que as vedações do art. 19 Res. CNMP 283/2024 foram observadas')
    # IA e modelo
    gerado_por_ia           = models.BooleanField(default=False)
    modelo_agu_base         = models.CharField(max_length=100, blank=True,
                                help_text='Modelo AGU utilizado como base (Ato PGJ 1413/2024)')
    status                  = models.CharField(max_length=15, choices=STATUS, default='rascunho')
    atualizado_em           = models.DateTimeField(auto_now=True)
```

---

### 2.5 App `cotacao` — Pesquisa de Preços

```python
# apps/cotacao/models.py
# Base legal: IN SEGES 65/2021 (opção do Ato PGJ 1382/2024)
# Dec. 21.872/2023, arts. 43–51 (subsidiário) | Acórdão TCU 1712/2025
# CGE-PI IN 01/2021 — pesquisa de preços (subsidiária)
# Para TI: Res. CNMP 283/2024, art. 10 (TCO) + art. 28 (estimativa de valor)

class PesquisaPrecos(models.Model):
    STATUS = [
        ('em_andamento', 'Em andamento'),
        ('concluida',    'Concluída'),
        ('aprovada',     'Aprovada'),
    ]
    etp             = models.OneToOneField('planejamento.ETP', on_delete=models.CASCADE,
                        related_name='pesquisa_precos')
    numero_sei      = models.CharField(max_length=30, blank=True)
    responsavel     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                        null=True, related_name='pesquisas_responsavel')
    # Metodologia declarada (IN 65/2021, art. 5º)
    metodologia     = models.TextField(
                        help_text='Justificativa da metodologia — IN SEGES 65/2021, art. 5º')
    # Opção expressa pelo normativo utilizado (Ato PGJ 1382/2024)
    normativo_base  = models.CharField(max_length=50, default='IN SEGES 65/2021')
    status          = models.CharField(max_length=15, choices=STATUS, default='em_andamento')
    criado_em       = models.DateTimeField(auto_now_add=True)
    concluida_em    = models.DateTimeField(null=True, blank=True)


class FontePreco(models.Model):
    """
    Fonte consultada.
    Fontes prioritárias (IN SEGES 65/2021 + Dec. 21.872/2023, art. 43):
    I — sistemas oficiais (PNCP, Painel de Preços, BEC-PI)
    II — contratos similares até 1 ano
    III — mídia especializada / tabelas aprovadas
    IV — notas fiscais eletrônicas
    V — pesquisa direta ≥3 fornecedores (com justificativa)
    Para obras: SINAPI, tabelas do SEINFRA-PI.
    """
    TIPOS = [
        ('pncp',            'PNCP — Portal Nacional de Contratações Públicas'),
        ('painel_precos',   'Painel de Preços Gov.br'),
        ('bec_pi',          'BEC-PI — Bolsa Eletrônica de Compras do Piauí'),
        ('sinapi',          'SINAPI'),
        ('contrato_similar','Contrato similar (até 1 ano)'),
        ('nfe',             'Nota Fiscal Eletrônica'),
        ('fornecedor',      'Cotação direta de fornecedor (mín. 3)'),
        ('midia_especializada', 'Mídia especializada / tabela aprovada'),
        ('outro',           'Outro'),
    ]
    pesquisa        = models.ForeignKey(PesquisaPrecos, on_delete=models.CASCADE,
                        related_name='fontes')
    tipo            = models.CharField(max_length=25, choices=TIPOS)
    identificador   = models.CharField(max_length=300,
                        help_text='Número do contrato, URL, cotação, NF-e etc.')
    data_referencia = models.DateField()
    descricao       = models.TextField(blank=True)


class ItemCotacao(models.Model):
    """
    Item cotado com resultado do saneamento estatístico.
    Acórdão TCU 1712/2025: "cesta de preços" com múltiplas fontes.
    """
    pesquisa            = models.ForeignKey(PesquisaPrecos, on_delete=models.CASCADE,
                            related_name='itens')
    descricao           = models.TextField()
    codigo_catmat_catser = models.CharField(max_length=20, blank=True)
    unidade_medida      = models.CharField(max_length=30)
    quantidade          = models.DecimalField(max_digits=14, decimal_places=4)
    precos_coletados    = models.JSONField(default=list,
                            help_text='[{"fonte_id": 1, "preco_unitario": 10.50, '
                                      '"excluido": false, "motivo_exclusao": ""}]')
    # Resultado estatístico
    preco_medio             = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    preco_mediana           = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    preco_medio_saneado     = models.DecimalField(max_digits=14, decimal_places=2, null=True,
                                help_text='Média após remoção de outliers — metodologia TCU')
    preco_referencia        = models.DecimalField(max_digits=14, decimal_places=2, null=True,
                                help_text='Preço adotado como referência para a licitação')
    valor_total_estimado    = models.DecimalField(max_digits=16, decimal_places=2, null=True)
    justificativa_preco     = models.TextField(blank=True)
    # TCO para TI (Res. CNMP 283/2024, art. 10)
    tco_detalhamento        = models.JSONField(null=True, blank=True,
                                help_text='Componentes do TCO para contratações de TIC')
```

---

### 2.6 App `juridico` — Controle jurídico e MJRs

```python
# apps/juridico/models.py
# APPL — Assessoria para Pareceres em Processos Licitatórios (Ato PGJ 1414/2024, art. 14)
# Ato PGJ 1383/2024: dispensa de manifestação jurídica para pequeno valor

from decimal import Decimal

# Limites atualizados pelo Decreto Federal 12.807/2025
LIMITE_DISPENSA_I   = Decimal('50000.00')   # bens e serviços — art. 75, I
LIMITE_DISPENSA_II  = Decimal('100000.00')  # obras e serviços de engenharia — art. 75, II
# Atualizar conforme novos decretos


class ControleJuridico(models.Model):
    """
    Registra se um processo exige ou não manifestação da APPL
    com base no Ato PGJ 1383/2024 e nos limites vigentes.
    """
    SITUACAO = [
        ('dispensado',          'Dispensado — Ato PGJ 1383/2024'),
        ('obrigatorio',         'Obrigatório — exige manifestação APPL'),
        ('pendente',            'Pendente de análise'),
        ('manifestacao_emitida','Manifestação emitida pela APPL'),
        ('aprovado',            'Aprovado pela APPL'),
        ('reprovado',           'Reprovado pela APPL'),
    ]
    # Pode ser vinculado a ETP ou diretamente ao processo
    etp             = models.OneToOneField('planejamento.ETP', on_delete=models.CASCADE,
                        related_name='controle_juridico', null=True, blank=True)
    valor_estimado  = models.DecimalField(max_digits=16, decimal_places=2)
    tipo_contratacao = models.CharField(max_length=30)
    situacao        = models.CharField(max_length=25, choices=SITUACAO)
    fundamento_dispensa = models.TextField(blank=True,
                            help_text='Ex: art. 75, I — R$ X < R$ 50.000 — Ato PGJ 1383/2024')
    # Se obrigatório
    numero_parecer_appl = models.CharField(max_length=30, blank=True)
    data_manifestacao   = models.DateField(null=True, blank=True)
    parecer_appl        = models.TextField(blank=True)
    numero_sei_parecer  = models.CharField(max_length=30, blank=True)
    criado_em           = models.DateTimeField(auto_now_add=True)

    @classmethod
    def verificar_dispensa(cls, valor: Decimal, tipo: str, usa_modelo_padrao: bool) -> dict:
        """
        Verifica se a contratação dispensa manifestação da APPL.
        Lógica: Ato PGJ 1383/2024, art. 1º.
        """
        if not usa_modelo_padrao:
            return {'dispensado': False,
                    'motivo': 'Contrato não baseado em modelo padronizado do MPPI'}
        limite = LIMITE_DISPENSA_II if tipo == 'obras' else LIMITE_DISPENSA_I
        if valor <= limite:
            return {
                'dispensado': True,
                'fundamento': f'Ato PGJ 1383/2024, art. 1º — valor (R$ {valor}) '
                              f'abaixo do limite (R$ {limite})'
            }
        return {'dispensado': False,
                'motivo': f'Valor (R$ {valor}) supera o limite de dispensa (R$ {limite})'}


class ManifestacaoJuridicoReferencial(models.Model):
    """
    MJR — Manifestação Jurídico Referencial do MPPI.
    Orientações consolidadas da APPL para situações recorrentes.
    Referência: MJR 56/2025, 66/2025, 86/2025, 92/2024, 95/2025.
    """
    TEMAS = [
        ('substituicao_marca',  'MJR 56/2025 — Substituição de Marca'),
        ('pagamento_indenizacao','MJR 66/2025 — Pagamento por Indenização'),
        ('adesao_arp',          'MJR 86/2025 — Adesão a ARP (Carona)'),
        ('dispensa_75_i_ii',    'MJR 92/2024 — Dispensa Art. 75 I e II'),
        ('prorrogacao_arp',     'MJR 95/2025 — Prorrogação de ARP'),
    ]
    numero          = models.CharField(max_length=20, unique=True)
    tema            = models.CharField(max_length=30, choices=TEMAS)
    titulo          = models.CharField(max_length=255)
    ementa          = models.TextField()
    conclusao       = models.TextField()
    fundamentos_legais = models.TextField()
    numero_sei      = models.CharField(max_length=30, blank=True)
    data_publicacao = models.DateField()
    vigente         = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Manifestação Jurídico Referencial (MJR)'
        ordering = ['-data_publicacao']
```

---

### 2.7 App `srp` — Sistema de Registro de Preços ⭐ DIFERENCIAL CENTRAL

> **Nota para o Claude Code:** Esta é a app de maior valor competitivo do sistema. Nenhuma startup do mercado (StartGov, GDL, licito.guru) implementa o ciclo completo de SRP. O Compras.gov.br cobre parcialmente; Betha e IPM têm cobertura parcial. Implementar com máxima fidelidade ao Decreto Federal 11.462/2023, ao Decreto Estadual 21.938/2023 (subsidiário) e ao MJR 86/2025 do MPPI. As validações de saldo e limite de carona são críticas — não simplificar.

```python
# apps/srp/models.py
# Base legal: arts. 82–86 NLLC
# Decreto Federal 11.462/2023 (aplicado por opção — Ato PGJ 1382/2024)
# Decreto Estadual 21.938/2023 (subsidiário)
# MJR 86/2025 — orientação interna do MPPI para caronas
# MJR 95/2025 — orientação interna do MPPI para prorrogação de ARP
# POP Contratação Direta — Adesão ARP (procedimento operacional padrão do MPPI)

from decimal import Decimal

class AtaRegistroPrecos(models.Model):
    STATUS = [
        ('vigente',   'Vigente'),
        ('suspensa',  'Suspensa'),
        ('cancelada', 'Cancelada'),
        ('encerrada', 'Encerrada'),
    ]
    orgao_gerenciador   = models.ForeignKey('core.Orgao', on_delete=models.CASCADE,
                            related_name='arps_gerenciadas')
    processo_licitatorio = models.ForeignKey('licitacao.ProcessoLicitatorio', null=True,
                            blank=True, on_delete=models.SET_NULL, related_name='arps')
    numero_ata          = models.CharField(max_length=30)
    ano                 = models.PositiveSmallIntegerField()
    objeto              = models.TextField()
    fornecedor_cnpj     = models.CharField(max_length=18)
    fornecedor_razao    = models.CharField(max_length=255)
    data_assinatura     = models.DateField()
    data_vigencia_inicio = models.DateField()
    data_vigencia_fim   = models.DateField()
    # Prorrogação — MJR 95/2025 define os critérios internos do MPPI
    prorrogada          = models.BooleanField(default=False)
    data_prorrogacao    = models.DateField(null=True, blank=True)
    fundamento_prorrogacao = models.TextField(blank=True,
                                help_text='Critérios do MJR 95/2025 e art. 12 Dec. 11.462/2023')
    numero_sei          = models.CharField(max_length=30, blank=True)
    status              = models.CharField(max_length=15, choices=STATUS, default='vigente')
    pncp_id             = models.CharField(max_length=100, blank=True)
    publicada_pncp      = models.BooleanField(default=False)
    data_publicacao_pncp = models.DateTimeField(null=True, blank=True)
    criado_em           = models.DateTimeField(auto_now_add=True)
    atualizado_em       = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('orgao_gerenciador', 'numero_ata', 'ano')
        verbose_name = 'Ata de Registro de Preços'

    @property
    def dias_para_vencimento(self):
        from django.utils import timezone
        return (self.data_vigencia_fim - timezone.now().date()).days

    @property
    def valor_total_registrado(self):
        from django.db.models import Sum, F
        return self.itens.aggregate(
            total=Sum(F('preco_unitario') * F('quantidade_registrada'))
        )['total'] or Decimal('0')

    @property
    def saldo_disponivel(self):
        consumido = self.contratacoes_decorrentes.filter(
            status__in=['ativa', 'encerrada']
        ).aggregate(total=models.Sum('valor_total'))['total'] or Decimal('0')
        return self.valor_total_registrado - consumido


class ItemARP(models.Model):
    ata                     = models.ForeignKey(AtaRegistroPrecos, on_delete=models.CASCADE,
                                related_name='itens')
    numero_item             = models.PositiveIntegerField()
    codigo_catmat_catser    = models.CharField(max_length=20, blank=True)
    descricao               = models.TextField()
    unidade_medida          = models.CharField(max_length=30)
    quantidade_registrada   = models.DecimalField(max_digits=14, decimal_places=4)
    preco_unitario          = models.DecimalField(max_digits=14, decimal_places=2)

    @property
    def quantidade_consumida(self):
        from django.db.models import Sum
        return ItemContratacaoDecorrente.objects.filter(
            item_arp=self,
            contratacao__status__in=['ativa', 'encerrada']
        ).aggregate(total=Sum('quantidade'))['total'] or Decimal('0')

    @property
    def saldo_quantidade(self):
        return self.quantidade_registrada - self.quantidade_consumida

    @property
    def percentual_consumido(self):
        if self.quantidade_registrada == 0:
            return 0
        return float(self.quantidade_consumida / self.quantidade_registrada * 100)


class ContratacaoDecorrente(models.Model):
    """Pedido de fornecimento emitido com base em ARP do MPPI."""
    STATUS = [('ativa','Ativa'),('encerrada','Encerrada'),('cancelada','Cancelada')]
    ata                     = models.ForeignKey(AtaRegistroPrecos, on_delete=models.CASCADE,
                                related_name='contratacoes_decorrentes')
    unidade_requisitante    = models.ForeignKey('core.UnidadeRequisitante',
                                on_delete=models.CASCADE)
    numero_pedido           = models.CharField(max_length=30)
    numero_sei              = models.CharField(max_length=30, blank=True)
    data_emissao            = models.DateField()
    data_entrega_prevista   = models.DateField(null=True, blank=True)
    valor_total             = models.DecimalField(max_digits=16, decimal_places=2)
    status                  = models.CharField(max_length=15, choices=STATUS, default='ativa')
    observacoes             = models.TextField(blank=True)
    contrato                = models.ForeignKey('contratos.Contrato', null=True, blank=True,
                                on_delete=models.SET_NULL, related_name='contratacoes_srp')

class ItemContratacaoDecorrente(models.Model):
    contratacao     = models.ForeignKey(ContratacaoDecorrente, on_delete=models.CASCADE,
                        related_name='itens')
    item_arp        = models.ForeignKey(ItemARP, on_delete=models.CASCADE,
                        related_name='contratacoes')
    quantidade      = models.DecimalField(max_digits=14, decimal_places=4)
    preco_unitario  = models.DecimalField(max_digits=14, decimal_places=2)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.quantidade > self.item_arp.saldo_quantidade:
            raise ValidationError(
                f'Quantidade ({self.quantidade}) supera o saldo disponível na ARP '
                f'({self.item_arp.saldo_quantidade} {self.item_arp.unidade_medida}).'
            )


class AdesaoARP(models.Model):
    """
    Carona — adesão de órgão não participante à ARP do MPPI.
    Critérios internos: MJR 86/2025 + POP Adesão ARP do MPPI.
    Decreto Federal 11.462/2023, arts. 28–32 (aplicado por opção).
    Decreto Estadual 21.938/2023 (subsidiário).
    Limite: 50% do quantitativo de cada item por órgão aderente.
    """
    STATUS = [
        ('solicitada',  'Solicitada'),
        ('autorizada',  'Autorizada pelo MPPI'),
        ('recusada',    'Recusada'),
        ('cancelada',   'Cancelada'),
    ]
    ata                     = models.ForeignKey(AtaRegistroPrecos, on_delete=models.CASCADE,
                                related_name='adesoes')
    orgao_aderente_nome     = models.CharField(max_length=255)
    orgao_aderente_cnpj     = models.CharField(max_length=18)
    orgao_aderente_esfera   = models.CharField(max_length=30)
    numero_sei_adesao       = models.CharField(max_length=30, blank=True,
                                help_text='Processo SEI/MPPI da solicitação de carona')
    data_solicitacao        = models.DateField()
    data_autorizacao        = models.DateField(null=True, blank=True)
    # Exigida pelo MJR 86/2025 e art. 28, §1º, Dec. 11.462/2023
    justificativa_vantajosidade = models.TextField(
                                help_text='Obrigatória — MJR 86/2025 e art. 28 §1º Dec. 11.462/2023')
    mjr_86_observado        = models.BooleanField(default=False,
                                help_text='Confirmação de observância do MJR 86/2025')
    status                  = models.CharField(max_length=15, choices=STATUS, default='solicitada')
    publicada_pncp          = models.BooleanField(default=False)

class ItemAdesaoARP(models.Model):
    adesao                  = models.ForeignKey(AdesaoARP, on_delete=models.CASCADE,
                                related_name='itens')
    item_arp                = models.ForeignKey(ItemARP, on_delete=models.CASCADE,
                                related_name='adesoes')
    quantidade_solicitada   = models.DecimalField(max_digits=14, decimal_places=4)
    quantidade_autorizada   = models.DecimalField(max_digits=14, decimal_places=4,
                                null=True, blank=True)

    @property
    def limite_legal(self):
        """50% do quantitativo registrado — Dec. 11.462/2023, art. 29 / MJR 86/2025."""
        return self.item_arp.quantidade_registrada * Decimal('0.5')

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.quantidade_solicitada > self.limite_legal:
            raise ValidationError(
                f'Quantidade ({self.quantidade_solicitada}) supera o limite legal de 50% '
                f'({self.limite_legal} {self.item_arp.unidade_medida}) — '
                f'Dec. 11.462/2023, art. 29 / MJR 86/2025.'
            )


class ARPExterna(models.Model):
    """
    Carona recebida — ARP de outro órgão à qual o MPPI aderiu.
    Procedimento: POP Adesão ARP do MPPI.
    """
    orgao_gerenciador_nome  = models.CharField(max_length=255)
    orgao_gerenciador_cnpj  = models.CharField(max_length=18)
    numero_ata_externa      = models.CharField(max_length=30)
    ano_ata_externa         = models.PositiveSmallIntegerField()
    objeto                  = models.TextField()
    fornecedor_cnpj         = models.CharField(max_length=18)
    fornecedor_razao        = models.CharField(max_length=255)
    numero_sei_adesao_mppi  = models.CharField(max_length=30, blank=True,
                                help_text='Processo SEI/MPPI da adesão')
    data_adesao             = models.DateField()
    data_vigencia_fim       = models.DateField()
    quantidade_autorizada   = models.DecimalField(max_digits=14, decimal_places=4)
    valor_autorizado        = models.DecimalField(max_digits=16, decimal_places=2)
    quantidade_utilizada    = models.DecimalField(max_digits=14, decimal_places=4, default=0)
    valor_utilizado         = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    pncp_ata_externa_id     = models.CharField(max_length=100, blank=True)
    observacoes             = models.TextField(blank=True)

    @property
    def saldo_quantidade(self):
        return self.quantidade_autorizada - self.quantidade_utilizada

    @property
    def saldo_valor(self):
        return self.valor_autorizado - self.valor_utilizado

    class Meta:
        verbose_name = 'ARP Externa (Carona Recebida)'
```

---

### 2.8 App `contratos` — Gestão da Contratação

```python
# apps/contratos/models.py
# Ato PGJ 1415/2024: serviços contínuos — prazo mín. 24 meses, máx. 120 meses
# Ato PGJ 0462/2013: fiscalização de contratos (mantido até revogação expressa)
# Equipe de gestão TI (quadripartite) — Res. CNMP 283/2024, art. 36

class Contrato(models.Model):
    STATUS = [
        ('vigente',    'Vigente'),
        ('suspenso',   'Suspenso'),
        ('rescindido', 'Rescindido'),
        ('encerrado',  'Encerrado'),
    ]
    orgao                   = models.ForeignKey('core.Orgao', on_delete=models.CASCADE)
    processo_licitatorio    = models.ForeignKey('licitacao.ProcessoLicitatorio', null=True,
                                blank=True, on_delete=models.SET_NULL)
    numero_contrato         = models.CharField(max_length=30)
    ano                     = models.PositiveSmallIntegerField()
    numero_sei              = models.CharField(max_length=30, blank=True,
                                help_text='Número do processo SEI/MPPI do contrato')
    objeto                  = models.TextField()
    contratado_cnpj         = models.CharField(max_length=18)
    contratado_razao        = models.CharField(max_length=255)
    valor_inicial           = models.DecimalField(max_digits=16, decimal_places=2)
    valor_atual             = models.DecimalField(max_digits=16, decimal_places=2)
    data_assinatura         = models.DateField()
    data_inicio_vigencia    = models.DateField()
    data_fim_vigencia       = models.DateField()
    # Serviços contínuos — Ato PGJ 1415/2024
    is_servico_continuo     = models.BooleanField(default=False)
    prazo_maximo_meses      = models.PositiveSmallIntegerField(null=True, blank=True,
                                help_text='Máx. 120 meses — art. 5º Ato PGJ 1415/2024')
    status                  = models.CharField(max_length=15, choices=STATUS, default='vigente')
    # Gestão — Ato PGJ 1414/2024 + Ato PGJ 0462/2013
    gestor                  = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.SET_NULL, null=True,
                                related_name='contratos_geridos')
    fiscal_adm              = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.SET_NULL, null=True,
                                related_name='contratos_fiscal_adm')
    fiscal_tecnico          = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.SET_NULL, null=True,
                                related_name='contratos_fiscal_tecnico')
    # TI — Res. CNMP 283/2024, art. 36 (quadripartite)
    fiscal_requisitante_ti  = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='contratos_fiscal_req_ti')
    is_contrato_ti          = models.BooleanField(default=False)
    # PNCP
    pncp_id                 = models.CharField(max_length=100, blank=True)
    publicado_pncp          = models.BooleanField(default=False)
    criado_em               = models.DateTimeField(auto_now_add=True)
    atualizado_em           = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('orgao', 'numero_contrato', 'ano')

    @property
    def saldo_contratual(self):
        empenhado = self.ordens_fornecimento.filter(
            status__in=['emitida', 'atendida']
        ).aggregate(total=models.Sum('valor_total'))['total'] or Decimal('0')
        return self.valor_atual - empenhado

    @property
    def dias_para_vencimento(self):
        from django.utils import timezone
        return (self.data_fim_vigencia - timezone.now().date()).days

    @property
    def exige_alerta_renovacao(self):
        """
        Res. CNMP 283/2024, art. 39: verificação com mínimo 120 dias de antecedência
        para prorrogação/renovação de contratos de TI.
        """
        if self.is_contrato_ti:
            return self.dias_para_vencimento <= 120
        return self.dias_para_vencimento <= 90


class Aditivo(models.Model):
    TIPO = [
        ('prazo',       'Prorrogação de prazo'),
        ('valor',       'Acréscimo de valor'),
        ('prazo_valor', 'Prazo e valor'),
        ('supressao',   'Supressão'),
        ('objeto',      'Alteração de objeto'),
    ]
    contrato            = models.ForeignKey(Contrato, on_delete=models.CASCADE,
                            related_name='aditivos')
    numero              = models.PositiveSmallIntegerField()
    tipo                = models.CharField(max_length=20, choices=TIPO)
    data_assinatura     = models.DateField()
    novo_valor          = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True)
    nova_data_fim       = models.DateField(null=True, blank=True)
    fundamento_legal    = models.CharField(max_length=100)
    justificativa       = models.TextField()
    numero_sei          = models.CharField(max_length=30, blank=True)
    pncp_id             = models.CharField(max_length=100, blank=True)
    publicado_pncp      = models.BooleanField(default=False)

    def clean(self):
        """Valida prazo máximo para serviços contínuos (Ato PGJ 1415/2024)."""
        from django.core.exceptions import ValidationError
        if self.nova_data_fim and self.contrato.is_servico_continuo:
            from dateutil.relativedelta import relativedelta
            meses = (self.nova_data_fim.year - self.contrato.data_inicio_vigencia.year) * 12 + \
                    (self.nova_data_fim.month - self.contrato.data_inicio_vigencia.month)
            prazo_max = self.contrato.prazo_maximo_meses or 120
            if meses > prazo_max:
                raise ValidationError(
                    f'Prazo total ({meses} meses) supera o máximo de {prazo_max} meses '
                    f'para serviços contínuos — art. 5º Ato PGJ 1415/2024.'
                )


class Apostilamento(models.Model):
    contrato            = models.ForeignKey(Contrato, on_delete=models.CASCADE,
                            related_name='apostilamentos')
    numero              = models.PositiveSmallIntegerField()
    data                = models.DateField()
    descricao           = models.TextField()
    numero_sei          = models.CharField(max_length=30, blank=True)
    novo_indice_reajuste = models.CharField(max_length=50, blank=True)


class OrdemFornecimento(models.Model):
    """
    Ordem de Fornecimento / Ordem de Serviço (OS/OFB).
    Res. CNMP 283/2024, art. 38: OS/OFB para contratos de TI com campos obrigatórios.
    """
    STATUS = [('emitida','Emitida'),('atendida','Atendida'),('cancelada','Cancelada')]
    contrato            = models.ForeignKey(Contrato, on_delete=models.CASCADE,
                            related_name='ordens_fornecimento')
    numero              = models.CharField(max_length=30)
    data_emissao        = models.DateField()
    data_entrega_prevista = models.DateField()
    data_atendimento    = models.DateField(null=True, blank=True)
    descricao           = models.TextField()
    valor_total         = models.DecimalField(max_digits=16, decimal_places=2)
    status              = models.CharField(max_length=15, choices=STATUS, default='emitida')
    # Para OS de TI (Res. CNMP 283/2024, art. 38)
    volume_servico      = models.TextField(blank=True,
                            help_text='Pontos de função, sprints, horas etc.')
    cronograma_execucao = models.TextField(blank=True)
    responsavel_tecnico = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                            on_delete=models.SET_NULL, related_name='oss_responsavel')
```

---

### 2.9 App `pncp` — Integração com o PNCP

```python
# apps/pncp/client.py
# Publicação obrigatória: art. 174 NLLC — condição de eficácia dos contratos
# MPPI não é SISG — utiliza API REST pública do PNCP com credencial própria

import requests
from django.conf import settings

PNCP_BASE_URL = 'https://pncp.gov.br/api/pncp/v1'

class PNCPClient:
    def __init__(self):
        self.session = requests.Session()
        # MPPI autentica com certificado digital ICP-Brasil
        self.session.cert = (settings.PNCP_CERT_PATH, settings.PNCP_KEY_PATH)
        self.session.headers.update({'Content-Type': 'application/json'})

    def publicar_pca(self, cnpj_orgao: str, payload: dict) -> dict:
        resp = self.session.post(f'{PNCP_BASE_URL}/orgaos/{cnpj_orgao}/compras', json=payload)
        resp.raise_for_status()
        return resp.json()

    def publicar_ata(self, cnpj_orgao: str, payload: dict) -> dict:
        resp = self.session.post(f'{PNCP_BASE_URL}/orgaos/{cnpj_orgao}/atas', json=payload)
        resp.raise_for_status()
        return resp.json()

    def publicar_contrato(self, cnpj_orgao: str, payload: dict) -> dict:
        resp = self.session.post(f'{PNCP_BASE_URL}/orgaos/{cnpj_orgao}/contratos', json=payload)
        resp.raise_for_status()
        return resp.json()

    def consultar_precos_pncp(self, codigo_item: str, uf: str = 'PI') -> list:
        """Busca preços praticados no PNCP para pesquisa de preços."""
        params = {'codigoItem': codigo_item, 'uf': uf}
        resp = self.session.get(f'{PNCP_BASE_URL}/contratacoes', params=params)
        resp.raise_for_status()
        return resp.json().get('data', [])
```

---

### 2.10 App `notificacoes` — Alertas automáticos

```python
# apps/notificacoes/tasks.py  (Celery Beat)

from celery import shared_task
from django.utils import timezone

LIMIARES_DIAS_CONTRATO   = [90, 60, 30, 15]
LIMIARES_DIAS_CONTRATO_TI = [120, 90, 60, 30]  # Res. CNMP 283/2024, art. 39
LIMIARES_DIAS_ARP        = [90, 60, 30, 15]
LIMIARES_SALDO_ARP_PCT   = [25, 10]
# Prazos PCA (Ato PGJ 1381/2024)
ALERTAS_PCA = [
    ('prazo_coleta',        30, 'Prazo de coleta de demandas do PCA se encerra em {} dias (10–30 jul)'),
    ('prazo_consolidacao',  15, 'Prazo de consolidação do PCA se encerra em {} dias (1–20 ago)'),
    ('prazo_aprovacao',     10, 'Prazo de aprovação do PCA pelo PGJ se encerra em {} dias (até 30 ago)'),
]

@shared_task
def verificar_vigencias_contratos():
    from apps.contratos.models import Contrato
    hoje = timezone.now().date()
    for contrato in Contrato.objects.filter(status='vigente'):
        limiares = LIMIARES_DIAS_CONTRATO_TI if contrato.is_contrato_ti else LIMIARES_DIAS_CONTRATO
        for limiar in limiares:
            data_alvo = hoje + timezone.timedelta(days=limiar)
            if contrato.data_fim_vigencia == data_alvo:
                _criar_alerta(
                    tipo='contrato_vencimento',
                    objeto_id=contrato.id,
                    objeto_tipo='Contrato',
                    mensagem=f'Contrato {contrato.numero_contrato}/{contrato.ano} '
                             f'({contrato.contratado_razao}) vence em {limiar} dias.',
                    destinatarios=[contrato.gestor, contrato.fiscal_adm]
                )

@shared_task
def verificar_vigencias_arps():
    from apps.srp.models import AtaRegistroPrecos, ItemARP
    hoje = timezone.now().date()
    for arp in AtaRegistroPrecos.objects.filter(status='vigente'):
        for limiar in LIMIARES_DIAS_ARP:
            if arp.data_vigencia_fim == hoje + timezone.timedelta(days=limiar):
                _criar_alerta(
                    tipo='arp_vencimento',
                    objeto_id=arp.id,
                    objeto_tipo='ARP',
                    mensagem=f'ARP {arp.numero_ata}/{arp.ano} vence em {limiar} dias. '
                             f'Saldo disponível: R$ {arp.saldo_disponivel:,.2f}. '
                             f'Verificar MJR 95/2025 para prorrogação.',
                    destinatarios=[]
                )
    for item in ItemARP.objects.filter(ata__status='vigente'):
        pct = 100 - item.percentual_consumido
        for limiar in LIMIARES_SALDO_ARP_PCT:
            if pct <= limiar:
                _criar_alerta(
                    tipo='arp_saldo_critico',
                    objeto_id=item.id,
                    objeto_tipo='ItemARP',
                    mensagem=f'Item "{item.descricao[:80]}" da ARP {item.ata.numero_ata} '
                             f'com apenas {pct:.1f}% de saldo restante.',
                    destinatarios=[]
                )
                break

@shared_task
def verificar_prazos_pca():
    """Alertas sobre os prazos do calendário PCA (Ato PGJ 1381/2024)."""
    from apps.pca.models import PlanoContratacaoAnual
    hoje = timezone.now().date()
    for pca in PlanoContratacaoAnual.objects.exclude(status__in=['publicado_pncp']):
        prazos = {
            'prazo_coleta':       pca.prazo_coleta_fim,
            'prazo_consolidacao': pca.prazo_consolidacao_fim,
            'prazo_aprovacao':    pca.prazo_aprovacao_fim,
        }
        for chave, prazo in prazos.items():
            if prazo:
                dias_restantes = (prazo - hoje).days
                if dias_restantes in [30, 15, 10, 5]:
                    _criar_alerta(
                        tipo=f'pca_{chave}',
                        objeto_id=pca.id,
                        objeto_tipo='PCA',
                        mensagem=f'PCA {pca.exercicio}: {chave.replace("_"," ")} '
                                 f'em {dias_restantes} dias ({prazo}).',
                        destinatarios=[]
                    )

def _criar_alerta(tipo, objeto_id, objeto_tipo, mensagem, destinatarios):
    # Implementar: Notificacao model + e-mail + integração SEI (Fase 2)
    import logging
    logging.getLogger('notificacoes').info(f'[{tipo}] {objeto_tipo} #{objeto_id}: {mensagem}')
```

---

## 3. Estágio 2 — Diferenciação (12–24 meses)

### 3.1 IA generativa com base legal do MPPI

```python
# apps/planejamento/ia_service.py

import anthropic

client = anthropic.Anthropic()

SYSTEM_PROMPT_MPPI = """
Você é um especialista em contratações públicas do Ministério Público do Estado do Piauí (MPPI),
com profundo conhecimento de:

FRAMEWORK NORMATIVO DO MPPI (em ordem de prioridade):
1. Lei 14.133/2021 (NLLC) — eixo central
2. Resolução CNMP 283/2024 — contratações de TIC no MP
3. IN SEGES 65/2021 (pesquisa de preços), IN 58/2022 (ETP), IN 81/2022 (TR) — adotadas pelo Ato PGJ 1382/2024
4. Modelos AGU — adotados pelo Ato PGJ 1413/2024
5. Decreto Estadual 21.872/2023 e 21.938/2023 — subsidiários
6. Ato PGJ 1381/2024 — PCA do MPPI
7. Ato PGJ 1382/2024 + 1413/2024 — implementação da NLLC no MPPI
8. Ato PGJ 1383/2024 — dispensa de parecer jurídico
9. Ato PGJ 1414/2024 + 1448/2024 — agente de contratação
10. Ato PGJ 1415/2024 — serviços contínuos (prazo mín. 24 meses, máx. 120 meses)
11. MJRs MPPI: 56/2025 (marca), 66/2025 (indenização), 86/2025 (carona ARP), 92/2024 (dispensa), 95/2025 (prorrogação ARP)
12. Jurisprudência TCU, TCE-PI e acórdãos relevantes

ESTRUTURA ORGANIZACIONAL:
- CLC / Assessoria de Compras: fase preparatória, licitações e contratos
- APPL: assessoramento jurídico e controle prévio de legalidade
- APG: co-responsável pelo PCA
- Instrução dos processos ocorre no SEI/MPPI

Redija documentos em linguagem jurídico-administrativa compatível com os padrões do MPPI,
citando sempre o normativo interno aplicável além do federal/estadual.
"""

def gerar_etp_mppi(item_pca_dados: dict, unidade: str, is_ti: bool = False) -> str:
    """Gera rascunho de ETP conforme IN SEGES 58/2022 e, se TI, Res. CNMP 283/2024."""
    normativo_adicional = (
        'Para esta contratação de TIC, aplica-se obrigatoriamente a Resolução CNMP 283/2024, '
        'incluindo TCO (Total Cost of Ownership), avaliação de software livre, e os critérios '
        'do art. 10 da Resolução. Inclua seção específica de Gerenciamento de Riscos conforme '
        'art. 45 da Res. CNMP 283/2024.'
    ) if is_ti else ''

    prompt = f"""
Com base nas informações abaixo, elabore um Estudo Técnico Preliminar (ETP) completo para
instrução no SEI/MPPI, conforme a IN SEGES 58/2022 (adotada pelo Ato PGJ 1382/2024),
o art. 18 da Lei 14.133/2021 e o art. 8º, II, do Ato PGJ 1381/2024.
{normativo_adicional}

UNIDADE REQUISITANTE: {unidade}
OBJETO: {item_pca_dados['descricao_objeto']}
JUSTIFICATIVA: {item_pca_dados['justificativa']}
VALOR ESTIMADO: R$ {item_pca_dados.get('valor_estimado', 'a apurar')}
CATEGORIA: {item_pca_dados['categoria']}
É SRP: {'Sim' if item_pca_dados.get('is_srp') else 'Não'}

Estruture com todas as seções da IN SEGES 58/2022, referenciando os normativos do MPPI.
Inclua ao final: "Este ETP foi elaborado com auxílio de IA e deve ser revisado e validado
pelos servidores responsáveis antes de autuação no SEI/MPPI."
"""
    msg = client.messages.create(
        model='claude-sonnet-4-6',
        max_tokens=4096,
        system=SYSTEM_PROMPT_MPPI,
        messages=[{'role': 'user', 'content': prompt}]
    )
    return msg.content[0].text


def analisar_conformidade_dfd(dfd_texto: str, unidade: str) -> dict:
    """
    Analisa DFD quanto à conformidade com o Ato PGJ 1381/2024 e a NLLC.
    Replica a lógica de análise da Assessoria de Compras do MPPI.
    """
    prompt = f"""
Analise o DFD abaixo quanto à conformidade com:
- Ato PGJ 1381/2024, arts. 7º e 8º (campos obrigatórios do DFD)
- Lei 14.133/2021, art. 12, VII
- Boas práticas de instrução processual do MPPI

Retorne JSON com:
{{
  "conformidades": ["..."],
  "achados": [
    {{
      "classificacao": "critico|atencao|conforme",
      "campo": "...",
      "descricao": "...",
      "fundamento": "Ato PGJ 1381/2024, art. X / Lei 14.133/2021, art. Y",
      "recomendacao": "..."
    }}
  ],
  "parecer_sintetico": "...",
  "apto_para_etp": true/false
}}

DFD DA UNIDADE {unidade}:
{dfd_texto[:4000]}
"""
    msg = client.messages.create(
        model='claude-sonnet-4-6',
        max_tokens=2048,
        system=SYSTEM_PROMPT_MPPI,
        messages=[{'role': 'user', 'content': prompt}]
    )
    import json
    return json.loads(msg.content[0].text)


def redigir_oficio_saneamento(achados: list, numero_processo: str, unidade: str) -> str:
    """
    Gera minutas de ofício de saneamento com base nos achados da análise.
    Padrão de comunicação da Assessoria de Compras do MPPI.
    """
    prompt = f"""
Com base nos achados abaixo, redija uma minuta de Ofício de Saneamento para a unidade
{unidade}, no padrão de comunicação da CLC/Assessoria de Compras do MPPI.

Processo SEI/MPPI: {numero_processo}

ACHADOS:
{json.dumps(achados, ensure_ascii=False, indent=2)}

O ofício deve:
1. Identificar o processo e o objeto
2. Listar os pontos de saneamento de forma numerada e objetiva
3. Citar o fundamento legal de cada ponto
4. Fixar prazo para resposta (sugerir 5 dias úteis para críticos, 10 para atenção)
5. Usar linguagem jurídico-administrativa compatível com o MPPI
"""
    msg = client.messages.create(
        model='claude-sonnet-4-6',
        max_tokens=2048,
        system=SYSTEM_PROMPT_MPPI,
        messages=[{'role': 'user', 'content': prompt}]
    )
    return msg.content[0].text


def gerar_tr_mppi(etp_dados: dict, unidade: str,
                   is_ti: bool = False,
                   is_srp: bool = False,
                   is_servico_continuo: bool = False) -> str:
    """
    Gera Termo de Referência conforme IN SEGES 81/2022 + modelo AGU (Ato PGJ 1413/2024).
    Se is_servico_continuo=True: inclui cláusula de prazo mín. 24 meses / máx. 120 meses (Ato PGJ 1415/2024).
    Se is_srp=True: inclui cláusulas específicas de Registro de Preços.
    Se is_ti=True: aplica vedações do art. 19 Res. CNMP 283/2024.
    """
    clausulas_especificas = []
    if is_servico_continuo:
        clausulas_especificas.append(
            'Incluir cláusula de prazo contratual: mínimo 24 meses, máximo 120 meses '
            '(art. 5º Ato PGJ 1415/2024). Justificar o prazo inicial proposto.'
        )
    if is_srp:
        clausulas_especificas.append(
            'Incluir cláusulas específicas de Registro de Preços: '
            'vigência da ARP (máx. 12 meses), condições de revisão de preços, '
            'hipóteses de cancelamento do registro (arts. 82–86 NLLC + Decreto 11.462/2023).'
        )
    if is_ti:
        clausulas_especificas.append(
            'Observar vedações do art. 19 Res. CNMP 283/2024. '
            'Incluir modalidade de remuneração (pontos de função, sprint, alocação com resultados). '
            'Prever obrigações de entrega de artefatos e critérios de aceite.'
        )

    prompt = f"""
Elabore um Termo de Referência completo para instrução no SEI/MPPI, conforme:
- IN SEGES 81/2022 (adotada pelo Ato PGJ 1382/2024)
- Modelo AGU (adotado pelo Ato PGJ 1413/2024, §2º)
- Art. 6º, XXIII, Lei 14.133/2021

UNIDADE REQUISITANTE: {unidade}
DADOS DO ETP: {json.dumps(etp_dados, ensure_ascii=False)[:3000]}

CLÁUSULAS ESPECIAIS:
{chr(10).join(f'- {c}' for c in clausulas_especificas) if clausulas_especificas else '- Nenhuma'}

Inclua ao final: "Este TR foi elaborado com auxílio de IA e deve ser revisado e validado
pelos servidores responsáveis antes de autuação no SEI/MPPI."
"""
    msg = client.messages.create(
        model='claude-sonnet-4-6',
        max_tokens=4096,
        system=SYSTEM_PROMPT_MPPI,
        messages=[{'role': 'user', 'content': prompt}]
    )
    return msg.content[0].text


def gerar_mapa_risco(etp_dados: dict, unidade: str, is_ti: bool = False) -> str:
    """
    Gera Mapa de Riscos metodologia 5×5 (TCU).
    Se is_ti=True: cobre as 3 fases (planejamento, seleção, gestão) — Res. CNMP 283/2024, art. 45.
    Base legal: Decreto 21.872/2023, arts. 29–34 + art. 8º, IV, Ato PGJ 1381/2024.
    """
    escopo_fases = (
        'Cobrir as TRÊS fases: planejamento, seleção do fornecedor e gestão contratual '
        '(Res. CNMP 283/2024, art. 45).'
    ) if is_ti else 'Cobrir a fase de planejamento e contratação.'

    prompt = f"""
Elabore um Mapa de Riscos (metodologia 5×5) conforme Decreto 21.872/2023, arts. 29–34
e art. 8º, IV, Ato PGJ 1381/2024. {escopo_fases}

Para cada risco: descrição, causa, consequência, probabilidade (1–5), impacto (1–5),
nível (prob × impacto), responsável (Administração/Contratado/Compartilhado),
ação preventiva e ação de contingência.

UNIDADE: {unidade}
OBJETO: {etp_dados.get('descricao_objeto', 'não informado')}
CATEGORIA: {etp_dados.get('categoria', 'não informada')}

Inclua ao final: "Este Mapa de Riscos foi elaborado com auxílio de IA e deve ser revisado
pelos servidores responsáveis antes de autuação no SEI/MPPI."
"""
    msg = client.messages.create(
        model='claude-sonnet-4-6',
        max_tokens=3000,
        system=SYSTEM_PROMPT_MPPI,
        messages=[{'role': 'user', 'content': prompt}]
    )
    return msg.content[0].text


def analisar_conformidade_arp(arp_dados: dict) -> dict:
    """
    Analisa ARP para adesão (carona) conforme MJR 86/2025 do MPPI.
    Verifica: vantajosidade, limite de quantitativos (50%/item), vigência, publicação PNCP.
    Retorna JSON no mesmo formato de analisar_conformidade_dfd.
    """
    prompt = f"""
Analise a Ata de Registro de Preços abaixo quanto à viabilidade de adesão (carona) pelo MPPI:
- MJR 86/2025 (orientação interna MPPI para caronas)
- Decreto Federal 11.462/2023, arts. 28–32
- Decreto Estadual 21.938/2023 (subsidiário)
- Lei 14.133/2021, arts. 82–86

Verificar: (1) vigência suficiente, (2) publicação no PNCP, (3) limite de 50% do
quantitativo/item (art. 29 Dec. 11.462/2023), (4) justificativa de vantajosidade
(MJR 86/2025 + art. 28 §1º Dec. 11.462/2023), (5) compatibilidade do objeto.

Retorne JSON:
{{
  "conformidades": ["..."],
  "achados": [
    {{
      "classificacao": "critico|atencao|conforme",
      "campo": "...",
      "descricao": "...",
      "fundamento": "MJR 86/2025 / Decreto 11.462/2023, art. X",
      "recomendacao": "..."
    }}
  ],
  "parecer_sintetico": "...",
  "apta_para_adesao": true
}}

DADOS DA ARP:
{json.dumps(arp_dados, ensure_ascii=False)[:3000]}
"""
    msg = client.messages.create(
        model='claude-sonnet-4-6',
        max_tokens=2048,
        system=SYSTEM_PROMPT_MPPI,
        messages=[{'role': 'user', 'content': prompt}]
    )
    import json as _json
    return _json.loads(msg.content[0].text)
```

### 3.1.1 Analytics de SRP — `apps/srp/analytics.py`

```python
# apps/srp/analytics.py
# Analytics de SRP — diferencial exclusivo; nenhuma startup do mercado oferece isso

from django.utils import timezone
from django.db.models import Sum, F, Count, Avg
from decimal import Decimal

def get_analytics_srp(orgao_id: int, ano: int = None) -> dict:
    """
    Analytics de SRP para governança e tomada de decisão.
    Identifica oportunidades de uso e riscos de esgotamento/vencimento.
    """
    from apps.srp.models import AtaRegistroPrecos, ItemARP, AdesaoARP, ARPExterna

    hoje = timezone.now().date()
    qs = AtaRegistroPrecos.objects.filter(orgao_gerenciador_id=orgao_id)
    if ano:
        qs = qs.filter(ano=ano)
    vigentes = qs.filter(status='vigente')

    # ARPs subutilizadas: itens com < 20% consumido e vigência > 60 dias
    itens_subutilizados = [
        item for arp in vigentes
        for item in arp.itens.all()
        if item.percentual_consumido < 20
        and (arp.data_vigencia_fim - hoje).days > 60
    ]

    # ARPs em risco de esgotamento: itens com saldo < 10%
    itens_criticos = [
        item for arp in vigentes
        for item in arp.itens.all()
        if item.percentual_consumido > 90
    ]

    # Top 10 fornecedores por volume de caronas cedidas
    top_fornecedores_caronas = (
        AdesaoARP.objects
        .filter(ata__orgao_gerenciador_id=orgao_id, status='autorizada')
        .values(fornecedor=F('ata__fornecedor_razao'))
        .annotate(total_adesoes=Count('id'))
        .order_by('-total_adesoes')[:10]
    )

    # Top 10 órgãos aderentes
    top_orgaos_aderentes = (
        AdesaoARP.objects
        .filter(ata__orgao_gerenciador_id=orgao_id, status='autorizada')
        .values('orgao_aderente_nome', 'orgao_aderente_cnpj')
        .annotate(total_adesoes=Count('id'))
        .order_by('-total_adesoes')[:10]
    )

    # ARPs que vencem em 30 dias com saldo > 30% — candidatas a prorrogação (MJR 95/2025)
    candidatas_prorrogacao = [
        arp for arp in vigentes
        if 0 < (arp.data_vigencia_fim - hoje).days <= 30
        and arp.valor_total_registrado > 0
        and float(arp.saldo_disponivel / arp.valor_total_registrado) > 0.30
    ]

    return {
        'arps_subutilizadas': len(itens_subutilizados),
        'itens_subutilizados': [
            {
                'arp': item.ata.numero_ata,
                'item': item.descricao[:80],
                'percentual_consumido': round(item.percentual_consumido, 1),
                'dias_vigencia_restantes': (item.ata.data_vigencia_fim - hoje).days,
            }
            for item in itens_subutilizados[:20]
        ],
        'itens_criticos_esgotamento': len(itens_criticos),
        'top_fornecedores_caronas': list(top_fornecedores_caronas),
        'top_orgaos_aderentes': list(top_orgaos_aderentes),
        'candidatas_prorrogacao': [
            {
                'arp': arp.numero_ata,
                'objeto': arp.objeto[:80],
                'vencimento': str(arp.data_vigencia_fim),
                'saldo_pct': round(
                    float(arp.saldo_disponivel / arp.valor_total_registrado * 100), 1
                ),
                'fundamento_prorrogacao': 'MJR 95/2025 + art. 12 Decreto 11.462/2023',
            }
            for arp in candidatas_prorrogacao
        ],
    }
```

### 3.2 Integração SEI/MPPI

```python
# apps/sei/client.py
# SEI/MPPI — Sistema Eletrônico de Informações (padrão PEN/TRF4)
# Permite criar processos, incluir documentos e tramitar internamente

import requests
from django.conf import settings

class SEIMPPIClient:
    """
    Integração com o SEI/MPPI via API REST.
    Todos os processos licitatórios do MPPI são autuados no SEI.
    Números de processo SEI são referenciados em todos os models.
    """
    def __init__(self):
        self.base_url = settings.SEI_MPPI_API_URL
        self.token    = settings.SEI_MPPI_API_TOKEN
        self.session  = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
        })

    def criar_processo_licitacao(self, tipo: str, objeto: str,
                                  unidade_id: str, interessado: str) -> dict:
        """
        Abre processo no SEI/MPPI para instrução do procedimento licitatório.
        Tipos de processo configurados no SEI do MPPI.
        """
        payload = {
            'IdTipoProcesso': tipo,
            'Especificacao': objeto[:50],
            'Assuntos': [{'CodigoEstruturado': '06.05.01'}],  # Licitações
            'Interessados': [{'Nome': interessado}],
            'UnidadeGerador': unidade_id,
            'NivelAcesso': 0,
        }
        resp = self.session.post(f'{self.base_url}/processos', json=payload)
        resp.raise_for_status()
        return resp.json()

    def incluir_documento(self, numero_processo: str, tipo_documento: str,
                           descricao: str, conteudo_base64: str,
                           nivel_acesso: int = 0) -> dict:
        payload = {
            'NumeroProcedimento': numero_processo,
            'IdSerie': tipo_documento,
            'Descricao': descricao,
            'Conteudo': conteudo_base64,
            'NivelAcesso': nivel_acesso,
        }
        resp = self.session.post(f'{self.base_url}/documentos', json=payload)
        resp.raise_for_status()
        return resp.json()

    def tramitar_para_clc(self, numero_processo: str, observacao: str = '') -> dict:
        """Tramita processo para a CLC/Assessoria de Compras."""
        payload = {
            'NumeroProcedimento': numero_processo,
            'UnidadesDestino': [{'IdUnidade': settings.SEI_MPPI_UNIDADE_CLC}],
            'SinManterAberto': False,
            'Observacao': observacao,
        }
        resp = self.session.post(f'{self.base_url}/processos/tramitar', json=payload)
        resp.raise_for_status()
        return resp.json()

    def consultar_processo(self, numero_processo: str) -> dict:
        """Retorna metadados do processo SEI/MPPI."""
        resp = self.session.get(f'{self.base_url}/processos/{numero_processo}')
        resp.raise_for_status()
        return resp.json()
```

### 3.2.1 Signals de automação SEI — `apps/sei/signals.py`

```python
# apps/sei/signals.py
# Automação: aciona o SEI/MPPI em eventos-chave do ciclo de contratações

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender='pca.DocumentoFormalizacaoDemanda')
def dfd_enviado_tramitar_sei(sender, instance, **kwargs):
    """
    Quando DFD muda para status 'enviado', tramita automaticamente para CLC no SEI.
    Reduz intervenção manual e garante rastreabilidade.
    """
    if instance.status == 'enviado' and instance.numero_sei:
        from apps.sei.client import SEIMPPIClient
        client = SEIMPPIClient()
        client.tramitar_para_clc(
            instance.numero_sei,
            observacao=f'DFD {instance.numero_dfd} — {instance.descricao_objeto[:100]}'
        )

@receiver(post_save, sender='planejamento.ETP')
def etp_aprovado_incluir_sei(sender, instance, **kwargs):
    """
    Quando ETP é aprovado, inclui documento no processo SEI correspondente.
    """
    if instance.status == 'aprovado' and instance.numero_sei:
        from apps.sei.client import SEIMPPIClient
        import base64
        # Gerar PDF do ETP e incluir no SEI
        # (implementação do gerador de PDF na Fase 2)
        pass

@receiver(post_save, sender='srp.AtaRegistroPrecos')
def arp_criada_abrir_processo_sei(sender, instance, created, **kwargs):
    """
    Se ARP criada sem numero_sei, abre processo automaticamente no SEI/MPPI.
    """
    if created and not instance.numero_sei:
        from apps.sei.client import SEIMPPIClient
        client = SEIMPPIClient()
        resultado = client.criar_processo_licitacao(
            tipo='ARP',
            objeto=instance.objeto[:50],
            unidade_id=settings.SEI_MPPI_UNIDADE_CLC,
            interessado=instance.fornecedor_razao,
        )
        instance.__class__.objects.filter(pk=instance.pk).update(
            numero_sei=resultado.get('NumeroProcedimento', '')
        )
```

### 3.3 Dashboard de governança do MPPI

```python
# apps/core/views/dashboard.py

def get_dashboard_mppi(orgao_id: int) -> dict:
    """
    Dashboard consolidado: PCA × Contratos × SRP × Alertas.
    Indicadores relevantes para a CLC/Assessoria de Compras do MPPI.
    """
    from django.utils import timezone
    from apps.pca.models import PlanoContratacaoAnual, ItemPCA
    from apps.srp.models import AtaRegistroPrecos, AdesaoARP, ARPExterna
    from apps.contratos.models import Contrato
    from apps.juridico.models import ControleJuridico

    hoje  = timezone.now().date()
    ano   = hoje.year

    pca_corrente = PlanoContratacaoAnual.objects.filter(
        orgao_id=orgao_id, exercicio=ano
    ).first()

    arps_vigentes = AtaRegistroPrecos.objects.filter(
        orgao_gerenciador_id=orgao_id, status='vigente'
    )

    return {
        'pca': {
            'exercicio':         ano,
            'status':            pca_corrente.status if pca_corrente else 'não iniciado',
            'total_itens':       pca_corrente.dfds.first().itens.count() if pca_corrente else 0,
            'itens_srp':         ItemPCA.objects.filter(
                                    dfd__pca__orgao_id=orgao_id,
                                    dfd__pca__exercicio=ano,
                                    is_srp=True
                                 ).count(),
        },
        'srp': {
            'arps_vigentes':     arps_vigentes.count(),
            'arps_vencendo_30d': arps_vigentes.filter(
                                    data_vigencia_fim__lte=hoje + timezone.timedelta(days=30)
                                 ).count(),
            'arps_vencendo_60d': arps_vigentes.filter(
                                    data_vigencia_fim__lte=hoje + timezone.timedelta(days=60)
                                 ).count(),
            'arps_vencendo_90d': arps_vigentes.filter(
                                    data_vigencia_fim__lte=hoje + timezone.timedelta(days=90)
                                 ).count(),
            'valor_registrado':  sum(a.valor_total_registrado for a in arps_vigentes),
            'saldo_disponivel':  sum(a.saldo_disponivel for a in arps_vigentes),
            # Dimensão 2 — Contratações decorrentes
            'contratacoes_decorrentes_ativas': ContratacaoDecorrente.objects.filter(
                                    ata__orgao_gerenciador_id=orgao_id,
                                    status='ativa'
                                 ).count(),
            'valor_contratacoes_decorrentes': ContratacaoDecorrente.objects.filter(
                                    ata__orgao_gerenciador_id=orgao_id,
                                    status__in=['ativa', 'encerrada']
                                 ).aggregate(total=models.Sum('valor_total'))['total'] or Decimal('0'),
            # Dimensão 3 — Caronas cedidas
            'caronas_cedidas':   AdesaoARP.objects.filter(
                                    ata__orgao_gerenciador_id=orgao_id,
                                    status='autorizada'
                                 ).count(),
            'orgaos_aderentes_distintos': AdesaoARP.objects.filter(
                                    ata__orgao_gerenciador_id=orgao_id,
                                    status='autorizada'
                                 ).values('orgao_aderente_cnpj').distinct().count(),
            # Dimensão 4 — Caronas recebidas
            'caronas_recebidas': ARPExterna.objects.filter(
                                    data_vigencia_fim__gte=hoje
                                 ).count(),
            'valor_utilizado_caronas_recebidas': ARPExterna.objects.aggregate(
                                    total=models.Sum('valor_utilizado')
                                 )['total'] or Decimal('0'),
        },
        'contratos': {
            'vigentes':          Contrato.objects.filter(
                                    orgao_id=orgao_id, status='vigente'
                                 ).count(),
            'vencendo_30d':      Contrato.objects.filter(
                                    orgao_id=orgao_id, status='vigente',
                                    data_fim_vigencia__lte=hoje + timezone.timedelta(days=30)
                                 ).count(),
            'vencendo_120d_ti':  Contrato.objects.filter(
                                    orgao_id=orgao_id, status='vigente',
                                    is_contrato_ti=True,
                                    data_fim_vigencia__lte=hoje + timezone.timedelta(days=120)
                                 ).count(),
        },
        'juridico': {
            'aguardando_appl':   ControleJuridico.objects.filter(
                                    situacao='obrigatorio'
                                 ).count(),
            'dispensados':       ControleJuridico.objects.filter(
                                    situacao='dispensado'
                                 ).count(),
        },
        # Qualidade de dados — resposta ao Acórdão TCU 2916/2025
        'qualidade_dados': {
            'itens_sem_catmat_catser': ItemPCA.objects.filter(
                                    dfd__pca__orgao_id=orgao_id,
                                    dfd__pca__exercicio=ano,
                                    codigo_catmat_catser=''
                                 ).count(),
            'arps_nao_publicadas_pncp': AtaRegistroPrecos.objects.filter(
                                    orgao_gerenciador_id=orgao_id,
                                    status='vigente',
                                    publicada_pncp=False
                                 ).count(),
            'contratos_nao_publicados_pncp': Contrato.objects.filter(
                                    orgao_id=orgao_id,
                                    status='vigente',
                                    publicado_pncp=False
                                 ).count(),
        },
    }
```

---

## 4. Estágio 3 — Plataforma (24+ meses)

```
# Itens reservados para fase futura:

# 4.1 Fase externa — FORA DO ESCOPO ATUAL
# ─────────────────────────────────────────────────────────────
# DECISÃO: fase externa excluída formalmente do escopo após análise de mercado (jun/2026).
# Requer homologação específica para o MP (não é SISG/federal).
# Criar placeholder: apps/licitacao/fase_externa/README.md
#
# Pré-requisitos antes de iniciar:
#   - Consolidar ciclo interno completo (Estágios 1 e 2)
#   - Consultar CNMP sobre requisitos para plataforma eletrônica do MP
#   - Decisão: desenvolver próprio vs. integrar BLL / BNC / Licitar Digital
#   - Homologação SEGES/MGI
#   - Infraestrutura WebSocket (Django Channels + Redis) para sala de disputa em tempo real
#   - SLA de disponibilidade 99,9%+ durante janelas de pregão
#
# NUNCA criar endpoints, views ou models de lances/disputa sem decisão explícita.

# 4.2 Multi-órgão / Fundo
# ─────────────────────────────────────────────────────────────
# O MPPI possui fundos (FPROCON) que podem ter processos licitatórios próprios.
# Middleware de multi-tenancy por fundo/órgão (já preparado no core.Orgao).
# Implementar OrgaoMiddleware: injeta request.orgao_ativo via JWT claim.
# Todos os ViewSets devem filtrar por orgao=request.orgao_ativo.

# 4.3 Analytics avançado de PCA
# ─────────────────────────────────────────────────────────────
# - Painel de eficiência: itens planejados vs. executados (% de efetivação)
# - Tempo médio do ciclo por modalidade (DFD → ETP → TR → contrato)
# - Aderência ao calendário de licitações (Ato PGJ 1381/2024, art. 18)
# - Relatórios bimestrais automatizados de risco de não efetivação (jul/set/nov — art. 17)
# - Itens sem ETP iniciado com alerta de atraso

# 4.4 Qualidade de dados PNCP — apps/pncp/qualidade.py
# ─────────────────────────────────────────────────────────────
# Resposta ao Acórdão TCU 2916/2025: 86,4% de registros inconsistentes.
# Implementar:
#   - validar_catmat_catser(codigo): consulta base CATMAT/CATSER antes de publicar
#   - relatorio_inconsistencias_pncp(orgao_id): lista tudo fora do padrão
#   - Signal pre_save em ItemCotacao e ItemPCA: bloqueia publicação sem código válido
#   - Endpoint GET /api/v1/qualidade/pncp/ com relatório de inconsistências
```

---

## 5. Configurações Django para o MPPI

```python
# config/settings/base.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party
    'rest_framework',
    'rest_framework_simplejwt',
    'django_celery_beat',
    'django_celery_results',
    'corsheaders',
    'auditlog',
    # Apps MPPI
    'apps.core',
    'apps.pca',
    'apps.planejamento',
    'apps.cotacao',
    'apps.licitacao',
    'apps.srp',
    'apps.contratos',
    'apps.juridico',
    'apps.pncp',
    'apps.notificacoes',
    # Fase 2
    # 'apps.sei',
    # 'apps.ia',
]

# PNCP — MPPI usa certificado ICP-Brasil (não é SISG)
PNCP_CERT_PATH      = env('PNCP_CERT_PATH')
PNCP_KEY_PATH       = env('PNCP_KEY_PATH')
PNCP_CNPJ_MPPI      = env('PNCP_CNPJ_MPPI')

# SEI/MPPI (Fase 2)
SEI_MPPI_API_URL    = env('SEI_MPPI_API_URL', default='')
SEI_MPPI_API_TOKEN  = env('SEI_MPPI_API_TOKEN', default='')
SEI_MPPI_UNIDADE_CLC = env('SEI_MPPI_UNIDADE_CLC', default='')

# Anthropic (IA — Fase 2)
ANTHROPIC_API_KEY   = env('ANTHROPIC_API_KEY', default='')

# Limites de dispensa — atualizar conforme novos decretos
# Decreto Federal 12.807/2025
LIMITE_DISPENSA_BENS_SERVICOS = 50_000
LIMITE_DISPENSA_OBRAS         = 100_000

# Celery
CELERY_BROKER_URL      = env('CELERY_BROKER_URL', default='redis://redis:6379/0')
CELERY_RESULT_BACKEND  = 'django-db'
CELERY_BEAT_SCHEDULER  = 'django_celery_beat.schedulers:DatabaseScheduler'
```

```python
# config/celery_beat_schedule.py

from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'verificar-vigencias-contratos': {
        'task': 'apps.notificacoes.tasks.verificar_vigencias_contratos',
        'schedule': crontab(hour=6, minute=0),
    },
    'verificar-vigencias-arps': {
        'task': 'apps.notificacoes.tasks.verificar_vigencias_arps',
        'schedule': crontab(hour=6, minute=15),
    },
    'verificar-prazos-pca': {
        'task': 'apps.notificacoes.tasks.verificar_prazos_pca',
        'schedule': crontab(hour=6, minute=30),
    },
}
```

---

## 6. Checklist de entrega por estágio

### Estágio 1
- [ ] Apps `core`, `pca`, `planejamento`, `cotacao`, `licitacao`, `srp`, `contratos`, `juridico`, `pncp`, `notificacoes` criados com migrations
- [ ] Fixture `unidades_mppi.json` com as 13 unidades requisitantes (Ato PGJ 1381/2024, art. 7º, §1º)
- [ ] Fixture `mjrs_mppi.json` com os 5 MJRs (56/2025, 66/2025, 86/2025, 92/2024, 95/2025)
- [ ] Placeholder `apps/licitacao/fase_externa/README.md` criado com decisão formal de escopo
- [ ] Calendário PCA gerado automaticamente via `PlanoContratacaoAnual.gerar_calendario(exercicio)`
- [ ] Lógica de dispensa de parecer APPL em `ControleJuridico.verificar_dispensa()` (Ato PGJ 1383/2024)
- [ ] Validação de limite de carona 50%/item em `ItemAdesaoARP.clean()` (MJR 86/2025 + Dec. 11.462/2023, art. 29)
- [ ] Validação de prazo máximo 120 meses em `Aditivo.clean()` (Ato PGJ 1415/2024)
- [ ] Alerta de renovação com 120 dias para contratos de TI (Res. CNMP 283/2024, art. 39)
- [ ] `EquipePlanejamentoTI` (tripartite — Res. CNMP 283/2024, art. 9º)
- [ ] `EquipeGestaoFiscalizacaoTI` (quadripartite — Res. CNMP 283/2024, art. 36)
- [ ] Dashboard SRP com 4 dimensões: ARPs originadas, contratações decorrentes, caronas cedidas (com count de órgãos distintos), caronas recebidas
- [ ] `numero_sei` presente em todos os models principais
- [ ] Integração PNCP: publicação de PCA, ARP, contrato e aditivo via Celery task
- [ ] Serializers PNCP: `PCASerializer`, `ARPSerializer`, `ContratoSerializer`, `AditivoSerializer`
- [ ] Validação CATMAT/CATSER (signal `pre_save`) antes de publicação no PNCP
- [ ] Limites de dispensa referenciados via `settings.LIMITE_DISPENSA_*` (nunca hardcoded)
- [ ] Admin Django configurado para todos os models
- [ ] API REST (DRF) com endpoints para cada módulo + autenticação JWT
- [ ] Testes unitários:
  - [ ] `test_saldo_arp` — `AtaRegistroPrecos.saldo_disponivel` decresce após `ContratacaoDecorrente`
  - [ ] `test_limite_carona_50pct` — `ItemAdesaoARP.clean()` rejeita > 50%
  - [ ] `test_prazo_servico_continuo` — `Aditivo.clean()` rejeita > 120 meses
  - [ ] `test_dispensa_appl_valor` — `verificar_dispensa()` abaixo e acima do limite
  - [ ] `test_dispensa_appl_modelo` — sem modelo padronizado não dispensa APPL
  - [ ] `test_nivel_risco_calculado` — `RiscoItem.save()` calcula `probabilidade × impacto`
  - [ ] `test_saldo_item_arp` — `ItemContratacaoDecorrente.clean()` bloqueia > saldo
  - [ ] `test_calendario_pca` — `gerar_calendario(ano)` retorna datas corretas

### Estágio 2
- [ ] `apps/ia/prompts.py` com `SYSTEM_PROMPT_MPPI` carregando framework normativo completo (7 níveis)
- [ ] Funções IA: `gerar_etp_mppi`, `gerar_tr_mppi`, `gerar_mapa_risco`, `analisar_conformidade_dfd`, `redigir_oficio_saneamento`, `analisar_conformidade_arp`
- [ ] ETP de TIC com TCO, seção de riscos das 3 fases e avaliação de software livre (Res. CNMP 283/2024)
- [ ] TR com suporte a `is_servico_continuo`, `is_srp` e `is_ti`
- [ ] `SEIMPPIClient` com: `criar_processo_licitacao`, `incluir_documento`, `tramitar_para_clc`, `consultar_processo`
- [ ] Signals SEI: DFD→tramitar CLC, ETP aprovado→incluir documento, ARP criada→abrir processo
- [ ] Analytics de SRP: `get_analytics_srp()` com subutilizados, críticos, top fornecedores/órgãos, candidatas a prorrogação
- [ ] Dashboard consolidado MPPI: PCA + SRP (4 dimensões) + contratos + jurídico + qualidade de dados
- [ ] Endpoint `GET /api/v1/dashboard/` com JWT
- [ ] Endpoint `GET /api/v1/srp/analytics/`
- [ ] Alertas de prazo PCA integrados ao Celery Beat

### Estágio 3
- [ ] Análise de viabilidade da fase externa: consultar CNMP + SEGES/MGI; avaliar BLL/BNC/Licitar Digital vs. solução própria
- [ ] `OrgaoMiddleware` para multi-tenancy por fundo (FPROCON)
- [ ] Analytics de eficiência do PCA: planejado vs. executado, tempo de ciclo, aderência ao calendário
- [ ] Relatórios bimestrais de risco PCA automatizados (jul/set/nov — art. 17 Ato PGJ 1381/2024)
- [ ] `apps/pncp/qualidade.py`: `validar_catmat_catser`, `relatorio_inconsistencias_pncp`, endpoint de qualidade
- [ ] Endpoint `GET /api/v1/pca/analytics/`
- [ ] Endpoint `GET /api/v1/qualidade/pncp/`
