# Sistema de Gestão de Licitações — MPPI
## Roadmap Técnico · Django / Python
**Órgão:** Ministério Público do Estado do Piauí — CLC / Assessoria de Compras  
**Escopo:** Ciclo interno (PCA → Planejamento → Cotação → SRP → Contratos) — fase externa reservada para fase futura  
**Versão:** 3.0 — Consolidado em junho/2026  
**Alterações v3.0:** Reflete o estado real do código em 25/06/2026. Incorpora: refatoração do `ItemPCA` (tipo_demanda × modalidade × unidade_orcamentaria × suspensão parcial); modelo `VinculoPCAItemARP` para multiexercício e lotes; integração dupla com a API Compras.gov.br (dadosabertos + Comprasnet Contratos); management commands de importação de ARPs, contratos e empenhos; saldo denormalizado no `ItemARP`; `ContratoComprasnet`, `EmpenhoComprasnet`, `ContratoARP`, `ItemContratoARP`; 14 unidades requisitantes (CONINT adicionado); UASG MPPI = 926092 / CNPJ MPPI = 05805924000189.

---

## 0. Posicionamento de mercado e decisões estratégicas de escopo

### 0.1 Panorama competitivo

Análise realizada em junho/2026 das principais ferramentas do mercado brasileiro:

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
| Fase externa (pregão/disputa) requer homologação SEGES/MGI | **Fase externa FORA DO ESCOPO** — reservada para fase futura após consulta ao CNMP |
| Nenhuma startup integra ao SEI | Integração SEI/MPPI planejada para Estágio 2 como diferencial exclusivo |
| 86,4% dos registros do PNCP com inconsistências (Acórdão TCU 2916/2025) | Validação CATMAT/CATSER obrigatória antes de qualquer publicação no PNCP |
| Pesquisa de preços sem "cesta de preços" multifonte | Implementar conforme Acórdão TCU 1712/2025 |

### 0.3 Decisão formal: fase externa fora do escopo

A fase externa (pregão eletrônico, sala de disputa em tempo real) é um produto por si só:

- **Regulatório:** exige homologação SEGES/MGI e validação do CNMP
- **Técnico:** sala de disputa exige WebSocket em tempo real (Django Channels + Redis), disponibilidade 99,9%+ durante janelas de pregão
- **Escopo:** o valor do sistema está no ciclo interno

**Implementação:** criar placeholder `apps/licitacao/fase_externa/README.md`. Nunca criar endpoints, views ou models relacionados a lances, disputa ou pregão eletrônico sem decisão explícita.

### 0.4 Regras transversais para o Claude Code

As regras abaixo aplicam-se a todas as implementações, em todos os estágios:

1. **`numero_sei` obrigatório em todo model principal** — é o identificador de rastreabilidade no SEI/MPPI
2. **Fundamento legal nos docstrings** — citar o normativo exato (ex: `"Ato PGJ 1381/2024, art. 7º, §1º"`)
3. **Fase externa = fora do escopo** — nunca criar endpoints, views ou models de sala de disputa, lances ou pregão eletrônico
4. **SRP é o diferencial central** — implementar com máxima fidelidade; validações de saldo e carona são críticas e não podem ser simplificadas
5. **PNCP é condição de eficácia** — contratos sem publicação no PNCP são ineficazes (art. 174 NLLC); nunca silenciar erro de publicação
6. **Limites de dispensa em settings** — nunca hardcodar `R$ 50.000` / `R$ 100.000`; sempre referenciar `settings.LIMITE_DISPENSA_*`
7. **IA sempre com disclaimer de revisão** — todo documento gerado por IA deve conter aviso de revisão obrigatória antes de autuação no SEI/MPPI
8. **UASG MPPI = 926092 / CNPJ MPPI = 05805924000189** — usar estas constantes em qualquer integração com APIs externas; não hardcodar em outros lugares
9. **Saldo de ARP é denormalizado** — `ItemARP.quantidade_contratada` e `quantidade_cedida_carona` são atualizados via `save()` e não devem ser recalculados a partir de relacionamentos (performance)
10. **`VinculoPCAItemARP` é a ponte PCA ↔ ARP** — nunca criar FK direto de `ItemPCA` para `ItemARP`; o vínculo é N:M com quantidade comprometida e validação de vigência

---

## 1. Contexto institucional e framework normativo

### 1.1 Posição institucional

O MPPI é órgão do Ministério Público estadual com autonomia funcional e administrativa (art. 127 CF/88 e Lei Orgânica do MPPI). Não integra o Poder Executivo estadual:

- O Decreto Estadual 21.872/2023 aplica-se **subsidiariamente** (Ato PGJ 1382/2024, art. 1º, §1º)
- Os regulamentos da **União** aplicam-se **primariamente**, por opção expressa (Ato PGJ 1382/2024, art. 1º caput e §2º + Ato PGJ 1413/2024)
- As **Resoluções do CNMP** têm força normativa obrigatória
- A **PGE-PI** não assessora o MPPI juridicamente — essa função é da **APPL** (Ato PGJ 1414/2024, art. 14)

### 1.2 Framework normativo hierarquizado

| Nível | Normativo | Aplicação no MPPI |
|---|---|---|
| 1 — Constitucional | CF/88, arts. 127–130 | Base da autonomia do MP |
| 2 — Lei federal | Lei 14.133/2021 (NLLC) | Eixo central — aplicação integral |
| 3 — CNMP | Res. CNMP 283/2024 (TIC) | Obrigatória para contratações de TI |
| 4 — Federal (INs) | IN SEGES 65/2021 (preços), IN 58/2022 (ETP), IN 81/2022 (TR), IN 67/2021 (dispensa eletrônica) | Aplicadas por opção expressa (Ato PGJ 1382/2024) |
| 5 — AGU (modelos) | Minutas padronizadas AGU | Adotados pelo MPPI (Ato PGJ 1413/2024, §2º) |
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
    └── Assessoria de Compras (chefiada por [nome do usuário] — Assessor de Compras / Agente de Contratação)
        ├── Consolidação do PCA
        ├── Fase preparatória (validação de DFD, ETP, TR, Mapa de Risco, Pesquisa de Preços)
        ├── Condução e julgamento dos procedimentos licitatórios
        └── Governança, gestão de equipe e tecnologia
```

**Unidades requisitantes do MPPI — 14 unidades** (Ato PGJ 1381/2024, art. 7º, §1º + CONINT incluído):
CPPT, CTI, CAA, CRH, GSI, CEAF, CI, CLC, CCF, APG, CONINT, GAECO, FPROCON, CCS

> **Nota v3.0:** O roadmap v2.0 listava 13 unidades. A unidade CONINT (Controle Interno) foi adicionada ao código (migration 0001). A descrição correta da CPPT é "Coordenadoria de Perícias e Pareceres Técnicos" (e não "Patrimônio e Prestação de Contas" como estava no rascunho anterior).

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

### 1.5 Unidades orçamentárias do MPPI

O sistema distingue **unidade requisitante** (setor que demanda) de **unidade orçamentária** (fonte de recursos):

| Código | Nome | Uso |
|---|---|---|
| `pgj` | PGJ — Procuradoria-Geral de Justiça | Dotação geral do MPPI |
| `fmmp` | FMMP — Fundo de Modernização do Ministério Público | Contrações de modernização/TI |
| `fepdc` | FEPDC — Fundo Estadual de Proteção e Defesa do Consumidor | Contrações vinculadas ao PROCON/FPROCON |

### 1.6 Particularidades do SRP para o MPPI

O Decreto Estadual **21.938/2023** regulamenta o SRP no âmbito do Piauí. Aplica-se subsidiariamente. Pontos de atenção:

- O MJR 86/2025 (Adesão a ARP) é a orientação interna do MPPI para caronas — orienta as validações do sistema
- O MJR 95/2025 (Prorrogação de ARP) orienta os critérios de prorrogação
- Limite de carona: **50% do quantitativo por item por órgão aderente** (Decreto 11.462/2023, art. 9º) — violação gera nulidade contratual e exposição ao TCU (Acórdão TCU 1507/2024)

**O módulo SRP é o maior diferencial competitivo.** As quatro dimensões integradas:

| Dimensão | Descrição | Lacuna no mercado |
|---|---|---|
| **ARPs originadas** | Atas geradas pelo MPPI como órgão gerenciador — itens, saldos, vigências | Ausente em todas as startups |
| **Contratações decorrentes** | Pedidos de fornecimento emitidos com base em ARP própria — débito automático de saldo | Ausente em todas as startups |
| **Caronas cedidas** | Órgãos externos que aderiram às ARPs do MPPI — controle do limite de 50%/item | Ausente em todas as startups |
| **Caronas recebidas** | ARPs de outros órgãos às quais o MPPI aderiu — saldo autorizado vs. utilizado | Ausente em todas as startups |

---

## 2. Estado atual do código (junho/2026)

### 2.1 Estrutura de apps — implementado

```
pca-multiexercicio-backend/
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── core/          ✅ Implementado — Orgao, UnidadeRequisitante, Perfil
│   ├── pca/           ✅ Implementado — PlanoContratacaoAnual, DFD, ItemPCA
│   ├── srp/           ✅ Implementado — ARP completa com 4 dimensões + APIs externas
│   ├── planejamento/  🔲 Pendente — ETP, MatrizRisco, TermoReferencia
│   ├── cotacao/       🔲 Pendente — PesquisaPrecos, FontePreco, ItemCotacao
│   ├── licitacao/     🔲 Pendente — ProcessoLicitatorio (stub criado)
│   ├── contratos/     🔲 Pendente — Contrato, Aditivo, Apostilamento, OrdemFornecimento
│   ├── juridico/      🔲 Pendente — ControleJuridico, ManifestacaoAPPL, MJR
│   ├── pncp/          🔲 Pendente — Client PNCP, serializers, publicação
│   └── notificacoes/  🔲 Pendente — Celery tasks de alertas
├── manage.py
└── requirements.txt
```

### 2.2 App `core` — ✅ Implementado

Models: `Orgao`, `UnidadeRequisitante` (14 unidades), `Perfil` (16 perfis de acesso).

**Diferenças em relação ao roadmap v2.0:**
- CONINT (Controle Interno) adicionado como 14ª unidade requisitante
- CPPT = "Coordenadoria de Perícias e Pareceres Técnicos"

### 2.3 App `pca` — ✅ Implementado (com extensões)

Models: `PlanoContratacaoAnual`, `DocumentoFormalizacaoDemanda`, `ItemPCA`.

**Extensões implementadas além do roadmap v2.0:**

#### `ItemPCA` — refatoração (migration 0003)

A migration 0003 (`refactor_itempca_tipo_modalidade`) separou o campo monolítico `tipo_contratacao` em dois campos ortogonais e adicionou novos campos:

```python
# NATUREZA DA DEMANDA (o quê)
tipo_demanda = [
    ("nova",           "Nova Contratação"),
    ("renovacao",      "Renovação de Contrato"),
    ("aditivo",        "Termo Aditivo"),
    ("apostilamento",  "Apostilamento"),
    ("repactuacao",    "Repactuação"),
    ("indeterminado",  "Indeterminado"),
]

# INSTRUMENTO LEGAL (como será feita)
modalidade = [
    ("pregao_eletronico",  "Pregão Eletrônico"),
    ("concorrencia",       "Concorrência"),
    ("concurso",           "Concurso"),
    ("dispensa",           "Contratação Direta — Dispensa (art. 75 NLLC)"),
    ("inexigibilidade",    "Contratação Direta — Inexigibilidade (art. 74 NLLC)"),
    ("arp_propria",        "ARP Própria (MPPI como gerenciador)"),
    ("arp_carona",         "ARP Carona (adesão a ARP de outro órgão)"),
]

# NORMATIVO REGENTE
normativo = [("14133_2021", "Lei 14.133/2021"), ("8666_1993", "Lei 8.666/1993 (transitório)")]

# FONTE ORÇAMENTÁRIA
unidade_orcamentaria = [
    ("pgj",   "PGJ — Procuradoria-Geral de Justiça"),
    ("fmmp",  "FMMP — Fundo de Modernização do Ministério Público"),
    ("fepdc", "FEPDC — Fundo Estadual de Proteção e Defesa do Consumidor"),
]

# RASTREABILIDADE E GESTÃO
codigo_pca          → auto-gerado no formato PCA-XXXX-AAAA (único, usado como referência externa)
valor_empenhado     → valor efetivamente empenhado (atualizado conforme execução orçamentária)
status              → ["nao_iniciado", "iniciado", "em_diligencia", "em_andamento", "concluido", "suspenso"]

# SUSPENSÃO PARCIAL
item_pai            → FK para si mesmo; preenchido apenas em suspensões parciais
                      O item pai continua ativo; o item filho registra os quantitativos paralisados
```

#### `DocumentoFormalizacaoDemanda`
- Status `suspensa` adicionado ao workflow

### 2.4 App `srp` — ✅ Implementado (escopo expandido)

#### Identificadores do MPPI nas APIs externas
```
UASG MPPI   = 926092
CNPJ MPPI   = 05805924000189
```

#### `AtaRegistroPrecos` — extensões

```python
# Campo renomeado: numero_ata → numero_arp (mais preciso)
numero_arp = CharField(max_length=30, help_text="Número sequencial (ex: 001/2027)")

# Integração API Compras.gov.br (dadosabertos.compras.gov.br)
codigo_uasg_gerenciadora = CharField(...)      # "926092" para o MPPI
numero_controle_pncp_ata = CharField(...)      # Retornado pela API Compras.gov.br
id_compra_compras_gov    = CharField(...)      # Campo idCompra da API
importada_da_api         = BooleanField(...)   # True se importada automaticamente
link_ata_pncp            = URLField(...)       # URL PNCP para consulta de contratos

# Prorrogação (Termo Aditivo — art. 84 Lei 14.133/2021)
data_fim_vigencia_original  = DateField(...)   # Data original antes da prorrogação
quantitativos_renovados     = BooleanField()   # Se quantitativos foram renovados
data_prorrogacao            = DateField(...)   # Data da publicação da prorrogação no PNCP

# modalidade_origem: pregao_eletronico | concorrencia | dispensa_srp
```

#### `ItemARP` — extensões

```python
# Agrupamento em lotes
numero_lote = CharField(blank=True)            # "Lote 1", "Lote 2" etc.

# Referência de custo (obras e serviços)
banco_referencia         = CharField(choices=["catmat","catser","sinapi","orse","outro"])
codigo_referencia_banco  = CharField(blank=True) # Ex: "91871" (SINAPI), "9718" (ORSE)

# Integração API Compras.gov.br
codigo_item_compras_gov = IntegerField(null=True)   # codigoItem (código PDM/CATMAT numérico)
maximo_adesao_api       = DecimalField(null=True)   # maximoAdesao da API; 0 = carona bloqueada
importado_da_api        = BooleanField(default=False)

# Saldo denormalizado (atualizado via save() — não recalcular por relacionamentos)
quantidade_contratada       = DecimalField(default=0)  # Debitado por ContratacaoDecorrente
quantidade_cedida_carona    = DecimalField(default=0)  # Debitado por AdesaoARP autorizada

# Properties de saldo
quantidade_disponivel         → registrada − contratada − cedida_carona
quantidade_comprometida_pca   → soma dos VinculoPCAItemARP (demanda certa do PCA)
quantidade_disponivel_eventual → registrada − comprometida_pca − contratada − cedida_carona
limite_carona_por_aderente    → 50% da quantidade_registrada (Dec. 11.462/2023, art. 9º)
```

#### `VinculoPCAItemARP` — modelo novo (não existia no roadmap v2.0)

Este modelo é a ponte N:M entre `ItemPCA` e `ItemARP`. Resolve os cenários de multiexercício e lotes:

```python
class VinculoPCAItemARP(models.Model):
    """
    Vínculo entre uma demanda aprovada no PCA e um item da ARP.
    Representa a quantidade "comprometida" pela demanda do PCA.

    Distinção fundamental:
      - quantidade_comprometida_pca → dotação comprometida (aquisição certa)
      - quantidade_disponivel_eventual → saldo não comprometido (eventual)

    Cenários cobertos:
      1. Multiexercício: ItemPCA de 2027 vinculado a ARP originada em 2026
      2. Lotes: múltiplos ItemPCAs (detergente, sabão, saco de lixo)
         vinculados ao mesmo ItemARP quando agrupados em lote

    Validações em clean():
      1. ARP deve estar vigente (status='vigente' e dentro do prazo)
      2. Soma dos comprometimentos não pode exceder quantidade_registrada
    """
    item_pca              = FK → pca.ItemPCA (limit_choices_to is_srp=True)
    item_arp              = FK → srp.ItemARP
    quantidade_comprometida = DecimalField
    observacoes           = TextField(blank=True)
    criado_por            = FK → AUTH_USER_MODEL
    criado_em             = DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("item_pca", "item_arp")
```

#### `ContratacaoDecorrente` — simplificado

- Agora é por item (um registro por item contratado), não por pedido com múltiplos itens
- `save()` debita automaticamente `item_arp.quantidade_contratada`

#### `AdesaoARP` — por item + validação dupla

```python
def clean(self):
    # Regra 1 — Limite de 50% por item por aderente (Dec. 11.462/2023, art. 9º)
    # Regra 2 — Se maximo_adesao_api == 0 (bloqueada no Compras.gov),
    #            exige numero_sei_autorizacao (MPPI pode liberar via SEI mesmo
    #            quando o sistema central indica bloqueio por questão cadastral)
```

#### Modelos de integração externa (novos)

```python
ContratoComprasnet   # Contratos importados via contratos.comprasnet.gov.br/api/contrato/ug/{uasg}
EmpenhoComprasnet    # Empenhos importados via v1 autenticada (pdm/{pdm}/ug/{uasg}/ano/{ano})
ContratoARP          # Contratos importados via dadosabertos (/modulo-contrato/) ou PNCP
ItemContratoARP      # Itens dos ContratoARP — rastreia consumo por item da ARP
ARPExterna           # Carona recebida — ARP de outro órgão à qual o MPPI aderiu
```

**`ContratoARP.is_carona`:** `True` quando o `uasg_contratante` difere do gerenciador da ARP — distingue contratações próprias do MPPI de caronas cedidas firmadas diretamente entre o órgão aderente e o fornecedor.

### 2.5 Management commands — ✅ Implementados

```
apps/srp/management/commands/
├── importar_arp_compras_gov.py   — Importa ARPs via dadosabertos.compras.gov.br/modulo-arp/
│                                   Endpoint 1: consultarARP (cabeçalhos)
│                                   Endpoint 2: consultarARPItem (itens — filtro local por numeroAtaRegistroPreco)
│                                   Flags: --uasg, --ano-inicio, --atualizar, --dry-run, --listar
│
├── importar_arp_pncp.py          — Fallback: importa ARPs não disponíveis no dadosabertos
│                                   via PNCP REST API (/v1/orgaos/{cnpj}/compras/{ano}/{seq}/atas)
│                                   Resolve itens e fornecedor via /itens e /itens/{n}/resultados
│                                   Flags: --cnpj, --ano-compra, --seq-compra, --numero-controle, --dry-run
│
├── importar_contratos_arp.py     — Importa ContratoARP + ItemContratoARP
│                                   Fonte auto: dadosabertos primeiro, PNCP como fallback
│                                   Vínculo com AtaRegistroPrecos via link_ata_pncp (regex)
│                                   Distingue is_carona pelo uasg_contratante
│                                   Flags: --uasg, --ano-inicio, --atualizar, --dry-run, --debug, --fonte
│
├── sincronizar_contratos_comprasnet.py — Fase 1: ContratoComprasnet (sem auth)
│                                         Fase 2: EmpenhoComprasnet por PDM/CATSER (JWT auth)
│                                         Atualiza ItemARP.quantidade_contratada via empenhos
│                                         Flags: --uasg, --com-empenhos, --incluir-inativos, --ano, --dry-run
│
└── sincronizar_saldo_arp.py      — Recalcula saldos denormalizados dos ItemARPs
```

### 2.6 Serviço `ComprasnetContratosClient` — ✅ Implementado

```
apps/srp/services/comprasnet_contratos.py
```

Endpoints cobertos:

| Endpoint | Auth | Uso |
|---|---|---|
| `GET /api/contrato/ug/{uasg}` | Nenhuma | Contratos ativos da UG |
| `GET /api/contrato/inativo/ug/{uasg}` | Nenhuma | Contratos inativos |
| `GET /api/contrato/{id}/itens` | Nenhuma | Itens do contrato |
| `GET /api/contrato/{id}/empenhos` | Nenhuma | Empenhos do contrato |
| `POST /api/v1/auth/login` | — | Obtém token JWT (CPF + senha SISG) |
| `GET /api/v1/empenho/pdm/{pdm}/ug/{uasg}/ano/{ano}` | JWT | Empenhos por PDM/CATMAT |
| `GET /api/v1/empenho/codigoservico/{cod}/ug/{uasg}/ano/{ano}` | JWT | Empenhos por CATSER |
| `GET /api/v1/empenho/ano/{ano}/ug/{uasg}` | JWT | Todos os empenhos da UG no ano |

**Credenciais:** `COMPRASNET_CONTRATOS_CPF` e `COMPRASNET_CONTRATOS_SENHA` (formato com pontos e traço). Token armazenado em memória; reautentica automaticamente em caso de 401.

---

## 3. Estágio 1 — Fundação (0–12 meses)

### 3.1 Apps pendentes de implementação

#### App `planejamento` — ETP, MatrizRisco, TermoReferencia

```python
# apps/planejamento/models.py
# Base legal: art. 18 NLLC + IN SEGES 58/2022 (ETP) + IN SEGES 81/2022 (TR)
# Para TI: Res. CNMP 283/2024 (arts. 10–20, 45)
# Modelos AGU adotados pelo Ato PGJ 1413/2024

class ETP(models.Model):
    """
    Estudo Técnico Preliminar — art. 18 NLLC + IN SEGES 58/2022.
    Para TI: TCO obrigatório (Res. CNMP 283/2024, art. 10).
    Dispensado nas hipóteses do Decreto 21.872/2023, art. 27.
    """
    item_pca        = OneToOneField('pca.ItemPCA', related_name='etp', null=True)
    numero_sei      = CharField(max_length=30, blank=True)
    numero_etp      = CharField(max_length=30)
    is_ti           = BooleanField(default=False)
    # 11 campos obrigatórios da IN SEGES 58/2022
    necessidade_contratacao, requisitos_contratacao, levantamento_mercado,
    descricao_solucao, estimativa_quantidade, estimativa_custo,
    justificativa_parcelamento, contratacoes_correlatas, alinhamento_pca,
    resultados_pretendidos, providencias_previas, impactos_ambientais
    # TI adicional (Res. CNMP 283/2024, art. 10)
    tco_total                = DecimalField(null=True)
    solucao_em_outros_orgaos = TextField(blank=True)
    software_livre_avaliado  = BooleanField(default=False)
    # IA e revisão
    gerado_por_ia, ia_modelo_utilizado, ia_revisado_por
    # Dispensa
    etp_dispensado           = BooleanField(default=False)
    fundamento_dispensa_etp  = CharField(max_length=200, blank=True)
    status                   = ['rascunho', 'em_revisao', 'aprovado']

class EquipePlanejamentoTI(models.Model):
    """Res. CNMP 283/2024, art. 9º — tripartite: Requisitante + Técnico + Administrativo."""
    etp, integrante_requisitante, integrante_tecnico, integrante_administrativo, lider, ato_designacao_sei

class MatrizRisco(models.Model):
    """
    Decreto 21.872/2023, arts. 29–34 + art. 8º, IV, Ato PGJ 1381/2024.
    Para TI: 3 fases — planejamento, seleção, gestão (Res. CNMP 283/2024, art. 45).
    Metodologia 5×5 (probabilidade × impacto).
    """
    etp, fase_atual  # planejamento | selecao | gestao

class RiscoItem(models.Model):
    """probabilidade (1–5) × impacto (1–5) → nivel_risco calculado automaticamente."""
    matriz, descricao_risco, causa, consequencia, probabilidade, impacto,
    nivel_risco (editable=False), responsavel, acao_preventiva, acao_contingencia
    # nivel_risco = probabilidade * impacto (calculado em save())

class TermoReferencia(models.Model):
    """
    Art. 6º, XXIII, NLLC + IN SEGES 81/2022 + Modelo AGU (Ato PGJ 1413/2024).
    Para TI: vedações do art. 19 Res. CNMP 283/2024.
    Serviços contínuos: prazo mín. 24 meses / máx. 120 meses (Ato PGJ 1415/2024).
    """
    etp, objeto, fundamentacao_legal, descricao_solucao, requisitos_habilitacao,
    criterio_julgamento, prazo_execucao, local_execucao,
    obrigacoes_contratante, obrigacoes_contratado, criterios_medicao,
    is_servico_continuo, prazo_inicial_meses, prazo_maximo_meses,
    is_srp, justificativa_srp,
    modalidade_remuneracao_ti, vedacoes_ti_observadas,
    gerado_por_ia, modelo_agu_base, status, numero_sei
```

#### App `cotacao` — Pesquisa de Preços

```python
# apps/cotacao/models.py
# Base legal: IN SEGES 65/2021 + Dec. 21.872/2023, arts. 43–51
# Acórdão TCU 1712/2025: "cesta de preços" multifonte com saneamento estatístico
# Para TI: Res. CNMP 283/2024, art. 28 (estimativa) + art. 10 (TCO)

class PesquisaPrecos(models.Model):
    """Vinculada ao ETP. Fontes obrigatórias da IN SEGES 65/2021, art. 5º."""
    etp, numero_sei, responsavel, metodologia, normativo_base, status

class FontePreco(models.Model):
    """
    Fontes: pncp | painel_precos | bec_pi | sinapi | contrato_similar
            nfe | fornecedor (mín. 3) | midia_especializada | outro
    """
    pesquisa, tipo, identificador, data_referencia, descricao

class ItemCotacao(models.Model):
    """
    "Cesta de preços" conforme Acórdão TCU 1712/2025.
    Saneamento estatístico: média, mediana, média saneada, preço de referência.
    """
    pesquisa, descricao, codigo_catmat_catser, unidade_medida, quantidade,
    precos_coletados (JSONField),
    preco_medio, preco_mediana, preco_medio_saneado, preco_referencia,
    valor_total_estimado, justificativa_preco,
    tco_detalhamento (JSONField, para TI)
```

#### App `contratos` — Gestão da Contratação

```python
# apps/contratos/models.py
# Ato PGJ 1415/2024: serviços contínuos — prazo mín. 24 meses, máx. 120 meses
# Res. CNMP 283/2024, art. 36: equipe de gestão TI (quadripartite)
# art. 174 NLLC: publicação no PNCP como condição de eficácia

class Contrato(models.Model):
    orgao, processo_licitatorio, numero_contrato, ano, numero_sei, objeto,
    contratado_cnpj, contratado_razao, valor_inicial, valor_atual,
    data_assinatura, data_inicio_vigencia, data_fim_vigencia,
    is_servico_continuo, prazo_maximo_meses (máx. 120),
    gestor, fiscal_adm, fiscal_tecnico, fiscal_requisitante_ti (TI),
    is_contrato_ti, pncp_id, publicado_pncp,
    # Properties: saldo_contratual, dias_para_vencimento, exige_alerta_renovacao
    # TI: alerta com 120 dias (Res. CNMP 283/2024, art. 39); outros: 90 dias

class Aditivo(models.Model):
    """clean(): valida prazo máximo para serviços contínuos (Ato PGJ 1415/2024)."""
    contrato, numero, tipo, data_assinatura, novo_valor, nova_data_fim,
    fundamento_legal, justificativa, numero_sei, pncp_id, publicado_pncp

class Apostilamento(models.Model):
    contrato, numero, data, descricao, numero_sei, novo_indice_reajuste

class OrdemFornecimento(models.Model):
    """Res. CNMP 283/2024, art. 38: OS/OFB para contratos de TI."""
    contrato, numero, data_emissao, data_entrega_prevista, data_atendimento,
    descricao, valor_total, status,
    volume_servico, cronograma_execucao, responsavel_tecnico  # TI
```

#### App `juridico` — Controle jurídico e MJRs

```python
# apps/juridico/models.py
# Limites: settings.LIMITE_DISPENSA_BENS_SERVICOS e settings.LIMITE_DISPENSA_OBRAS
# (Decreto Federal 12.807/2025 — nunca hardcodar)

class ControleJuridico(models.Model):
    """
    Controla se a contratação exige ou não manifestação da APPL.
    Lógica: Ato PGJ 1383/2024, art. 1º.
    verificar_dispensa(valor, tipo, usa_modelo_padrao) → {'dispensado': bool, ...}
    """
    etp, valor_estimado, tipo_contratacao, situacao, fundamento_dispensa,
    numero_parecer_appl, data_manifestacao, parecer_appl, numero_sei_parecer

class ManifestacaoJuridicoReferencial(models.Model):
    """
    MJRs vigentes:
      MJR 56/2025  — Substituição de Marca
      MJR 66/2025  — Pagamento por Indenização
      MJR 86/2025  — Adesão a ARP (Carona) — orienta clean() de AdesaoARP
      MJR 92/2024  — Dispensa Art. 75 I e II
      MJR 95/2025  — Prorrogação de ARP — orienta campo fundamento_prorrogacao
    """
    numero, tema, titulo, ementa, conclusao, fundamentos_legais, numero_sei,
    data_publicacao, vigente
```

#### App `pncp` — Integração com o PNCP

```python
# apps/pncp/client.py
# art. 174 NLLC: condição de eficácia dos contratos
# MPPI usa API REST pública do PNCP com certificado ICP-Brasil (não é SISG)
# CNPJ MPPI = 05805924000189

class PNCPClient:
    """Autenticação via certificado digital ICP-Brasil (settings.PNCP_CERT_PATH + KEY_PATH)."""
    def publicar_pca(cnpj_orgao, payload) → dict
    def publicar_ata(cnpj_orgao, payload) → dict
    def publicar_contrato(cnpj_orgao, payload) → dict
    def publicar_aditivo(cnpj_orgao, compra_seq, contrato_seq, payload) → dict
    def consultar_precos_pncp(codigo_item, uf='PI') → list   # Pesquisa de preços
```

**Serializers necessários:** `PCASerializer`, `ARPSerializer`, `ContratoSerializer`, `AditivoSerializer` — mapear campos locais para o schema do PNCP; validar CATMAT/CATSER antes de enviar.

#### App `notificacoes` — Alertas automáticos (Celery Beat)

```python
# apps/notificacoes/tasks.py

@shared_task verificar_vigencias_contratos()
    # TI: alertas em 120, 90, 60, 30 dias (Res. CNMP 283/2024, art. 39)
    # Outros: 90, 60, 30, 15 dias

@shared_task verificar_vigencias_arps()
    # Vencimento: 90, 60, 30, 15 dias
    # Saldo crítico: < 25% e < 10% do quantitativo

@shared_task verificar_prazos_pca()
    # Alertas do calendário PCA (Ato PGJ 1381/2024):
    # prazo_coleta_fim: 30, 15, 10, 5 dias
    # prazo_consolidacao_fim: idem
    # prazo_aprovacao_fim: idem

# schedule (config/celery_beat_schedule.py):
# verificar-vigencias-contratos → crontab(hour=6, minute=0)
# verificar-vigencias-arps      → crontab(hour=6, minute=15)
# verificar-prazos-pca          → crontab(hour=6, minute=30)
```

### 3.2 API REST (DRF) — pendente

Endpoints a implementar para o módulo SRP (já tem models e services):

```
GET  /api/v1/srp/arps/                        → lista ARPs do órgão
GET  /api/v1/srp/arps/{id}/                   → detalhe + saldo por item
GET  /api/v1/srp/arps/{id}/itens/             → itens com saldo disponível/eventual
POST /api/v1/srp/arps/{id}/contratacoes/      → emite pedido de fornecimento
POST /api/v1/srp/arps/{id}/adesoes/           → registra carona cedida
GET  /api/v1/srp/vinculos-pca/                → vínculos PCA × ARP
POST /api/v1/srp/vinculos-pca/                → cria vínculo (valida vigência + qtd)
GET  /api/v1/srp/arps-externas/               → caronas recebidas
GET  /api/v1/pca/                             → PCAs do órgão
GET  /api/v1/pca/{id}/itens/                  → itens com status e código PCA
```

### 3.3 Configurações Django

```python
# config/settings.py (adicionar/verificar)

# APIs externas
PNCP_CERT_PATH                  = env('PNCP_CERT_PATH')
PNCP_KEY_PATH                   = env('PNCP_KEY_PATH')
PNCP_CNPJ_MPPI                  = '05805924000189'
COMPRASNET_UASG_MPPI            = '926092'
COMPRASNET_CONTRATOS_CPF        = env('COMPRASNET_CONTRATOS_CPF', default='')
COMPRASNET_CONTRATOS_SENHA      = env('COMPRASNET_CONTRATOS_SENHA', default='')

# Limites de dispensa — Decreto Federal 12.807/2025
LIMITE_DISPENSA_BENS_SERVICOS   = 50_000     # art. 75, I NLLC
LIMITE_DISPENSA_OBRAS           = 100_000    # art. 75, II NLLC

# SEI/MPPI (Estágio 2)
SEI_MPPI_API_URL                = env('SEI_MPPI_API_URL', default='')
SEI_MPPI_API_TOKEN              = env('SEI_MPPI_API_TOKEN', default='')
SEI_MPPI_UNIDADE_CLC            = env('SEI_MPPI_UNIDADE_CLC', default='')

# Anthropic (IA — Estágio 2)
ANTHROPIC_API_KEY               = env('ANTHROPIC_API_KEY', default='')

# Celery (ainda não configurado)
CELERY_BROKER_URL               = env('CELERY_BROKER_URL', default='redis://redis:6379/0')
CELERY_RESULT_BACKEND           = 'django-db'
```

---

## 4. Estágio 2 — Diferenciação (12–24 meses)

### 4.1 IA generativa com base legal do MPPI

```python
# apps/planejamento/ia_service.py
# Modelo: claude-sonnet-4-6

SYSTEM_PROMPT_MPPI  → framework normativo hierarquizado (7 níveis) + estrutura MPPI

# Funções a implementar:
gerar_etp_mppi(item_pca_dados, unidade, is_ti)
    # IN SEGES 58/2022 + se TI: Res. CNMP 283/2024 (TCO, riscos 3 fases, software livre)

gerar_tr_mppi(etp_dados, unidade, is_ti, is_srp, is_servico_continuo)
    # IN SEGES 81/2022 + Modelo AGU (Ato PGJ 1413/2024)
    # is_servico_continuo → cláusula de 24–120 meses (Ato PGJ 1415/2024)
    # is_srp → cláusulas de registro de preços
    # is_ti → vedações art. 19 Res. CNMP 283/2024

gerar_mapa_risco(etp_dados, unidade, is_ti)
    # 5×5 (Dec. 21.872/2023, arts. 29–34)
    # is_ti → 3 fases (Res. CNMP 283/2024, art. 45)

analisar_conformidade_dfd(dfd_texto, unidade)
    # Retorna JSON: {conformidades, achados, parecer_sintetico, apto_para_etp}
    # achados: classificacao (critico|atencao|conforme), campo, fundamento, recomendacao

redigir_oficio_saneamento(achados, numero_processo, unidade)
    # Minuta de ofício de saneamento no padrão da Assessoria de Compras

analisar_conformidade_arp(arp_dados)
    # MJR 86/2025: vigência, PNCP, limite 50%, vantajosidade, objeto
    # Retorna JSON: {conformidades, achados, parecer_sintetico, apta_para_adesao}
```

**Regra:** todo documento gerado por IA deve conter ao final o aviso:
> *"Este documento foi elaborado com auxílio de IA e deve ser revisado e validado pelos servidores responsáveis antes de autuação no SEI/MPPI."*

### 4.2 Analytics de SRP — `apps/srp/analytics.py`

```python
def get_analytics_srp(orgao_id, ano=None) → dict:
    # ARPs subutilizadas: < 20% consumido com vigência > 60 dias
    # ARPs em risco de esgotamento: > 90% consumido
    # Top 10 fornecedores por volume de caronas cedidas
    # Top 10 órgãos aderentes
    # Candidatas a prorrogação: vencendo em 30 dias com saldo > 30% (MJR 95/2025)
```

### 4.3 Integração SEI/MPPI

```python
# apps/sei/client.py
class SEIMPPIClient:
    criar_processo_licitacao(tipo, objeto, unidade_id, interessado) → dict
    incluir_documento(numero_processo, tipo_documento, descricao, conteudo_base64) → dict
    tramitar_para_clc(numero_processo, observacao) → dict
    consultar_processo(numero_processo) → dict

# apps/sei/signals.py
@receiver(post_save, DFD)          → dfd_enviado_tramitar_sei (status='enviado')
@receiver(post_save, ETP)          → etp_aprovado_incluir_sei (status='aprovado')
@receiver(post_save, ARP, created) → arp_criada_abrir_processo_sei
```

### 4.4 Dashboard de governança

```python
def get_dashboard_mppi(orgao_id) → dict:
    # pca: status, total_itens, itens_srp
    # srp: 4 dimensões completas + alertas de vencimento (30/60/90 dias)
    # contratos: vigentes, vencendo_30d, vencendo_120d_ti
    # juridico: aguardando_appl, dispensados
    # qualidade_dados: itens_sem_catmat_catser, arps_nao_publicadas_pncp,
    #                  contratos_nao_publicados_pncp (resposta ao Acórdão TCU 2916/2025)
```

---

## 5. Estágio 3 — Plataforma (24+ meses)

```
# 5.1 Fase externa — FORA DO ESCOPO ATUAL
# DECISÃO FORMAL: fase externa excluída após análise de mercado (jun/2026).
# Placeholder: apps/licitacao/fase_externa/README.md
# Pré-requisitos:
#   - Consolidar Estágios 1 e 2
#   - Consultar CNMP sobre plataforma eletrônica própria para MPs estaduais
#   - Avaliar BLL / BNC / Licitar Digital vs. solução própria
#   - Homologação SEGES/MGI
#   - Django Channels + Redis para sala de disputa em tempo real
#   - SLA 99,9%+ durante janelas de pregão
# NUNCA criar endpoints, views ou models de lances/disputa sem decisão explícita.

# 5.2 Multi-órgão / Fundo
# FPROCON pode ter processos licitatórios próprios (já preparado no core.Orgao).
# Implementar OrgaoMiddleware: injeta request.orgao_ativo via JWT claim.

# 5.3 Analytics avançado de PCA
# - Planejado vs. executado (% de efetivação por unidade e por modalidade)
# - Tempo médio do ciclo (DFD → ETP → TR → contrato) por modalidade
# - Aderência ao calendário (Ato PGJ 1381/2024, art. 18)
# - Relatórios bimestrais automatizados de risco (jul/set/nov — art. 17)

# 5.4 Qualidade de dados PNCP (apps/pncp/qualidade.py)
# Resposta ao Acórdão TCU 2916/2025 (86,4% de registros inconsistentes):
#   - validar_catmat_catser(codigo): consulta base antes de publicar
#   - relatorio_inconsistencias_pncp(orgao_id): lista tudo fora do padrão
#   - Signal pre_save em ItemCotacao e ItemPCA: bloqueia publicação sem código válido
#   - Endpoint GET /api/v1/qualidade/pncp/
```

---

## 6. Checklist de entrega

### Estágio 1

#### Apps e models
- [x] App `core` criado: `Orgao`, `UnidadeRequisitante` (14 unidades), `Perfil`
- [x] App `pca` criado: `PlanoContratacaoAnual`, `DFD`, `ItemPCA` com refatoração tipo_demanda × modalidade
- [x] App `srp` criado: 4 dimensões completas + modelos de integração externa
- [ ] App `planejamento` criado: `ETP`, `EquipePlanejamentoTI`, `MatrizRisco`, `RiscoItem`, `TermoReferencia`
- [ ] App `cotacao` criado: `PesquisaPrecos`, `FontePreco`, `ItemCotacao`
- [ ] App `contratos` criado: `Contrato`, `Aditivo`, `Apostilamento`, `OrdemFornecimento`
- [ ] App `juridico` criado: `ControleJuridico`, `ManifestacaoJuridicoReferencial`
- [ ] App `pncp` criado: `PNCPClient`, serializers de publicação, Celery tasks
- [ ] App `notificacoes` criado: tasks Celery de alertas de vigência e prazos PCA
- [ ] Placeholder `apps/licitacao/fase_externa/README.md` com decisão formal de escopo

#### Fixtures
- [ ] `unidades_mppi.json` com as 14 unidades requisitantes
- [ ] `mjrs_mppi.json` com os 5 MJRs (56/2025, 66/2025, 86/2025, 92/2024, 95/2025)

#### Validações críticas
- [x] `ItemAdesaoARP.clean()` — limite 50%/item/aderente (MJR 86/2025 + Dec. 11.462/2023, art. 9º)
- [x] `AdesaoARP.clean()` — validação de maximo_adesao_api == 0 exige numero_sei
- [x] `VinculoPCAItemARP.clean()` — ARP vigente + não exceder quantidade_registrada
- [x] `ContratacaoDecorrente.save()` — debita `quantidade_contratada` automaticamente
- [x] `AdesaoARP.save()` — debita `quantidade_cedida_carona` automaticamente
- [ ] `Aditivo.clean()` — prazo máximo 120 meses para serviços contínuos (Ato PGJ 1415/2024)
- [ ] `ControleJuridico.verificar_dispensa()` — lógica do Ato PGJ 1383/2024
- [ ] `RiscoItem.save()` — `nivel_risco = probabilidade × impacto`
- [ ] Validação CATMAT/CATSER (signal `pre_save`) antes de publicação no PNCP
- [ ] `Contrato.exige_alerta_renovacao` — 120 dias para TI, 90 dias para demais

#### Integrações
- [x] `importar_arp_compras_gov` — importação ARPs via dadosabertos.compras.gov.br
- [x] `importar_arp_pncp` — fallback importação via PNCP REST API
- [x] `importar_contratos_arp` — importação contratos (dadosabertos + PNCP)
- [x] `sincronizar_contratos_comprasnet` — contratos + empenhos Comprasnet
- [x] `ComprasnetContratosClient` — cliente HTTP com auth JWT e retry automático
- [ ] `PNCPClient` — publicação de PCA, ARP, contrato, aditivo (autenticação ICP-Brasil)
- [ ] Serializers PNCP: `PCASerializer`, `ARPSerializer`, `ContratoSerializer`, `AditivoSerializer`

#### API REST (DRF)
- [ ] Endpoints SRP: arps, itens, contratacoes, adesoes, vinculos-pca, arps-externas
- [ ] Endpoints PCA: pcas, itens, dfds
- [ ] Endpoints planejamento: etps, matrizes-risco, termos-referencia
- [ ] Autenticação JWT em todos os endpoints
- [ ] Admin Django configurado para todos os models

#### Testes unitários
- [x] *(modelo de saldo denormalizado implementado — testes pendentes)*
- [ ] `test_saldo_item_arp` — `ContratacaoDecorrente.save()` debita `quantidade_contratada`
- [ ] `test_limite_carona_50pct` — `AdesaoARP.clean()` rejeita > 50% por aderente
- [ ] `test_carona_bloqueada_sem_sei` — `AdesaoARP.clean()` exige SEI quando maximo_adesao_api == 0
- [ ] `test_vinculo_pca_arp_excede_qtd` — `VinculoPCAItemARP.clean()` rejeita excesso
- [ ] `test_vinculo_arp_vencida` — `VinculoPCAItemARP.clean()` rejeita ARP encerrada
- [ ] `test_prazo_servico_continuo` — `Aditivo.clean()` rejeita > 120 meses
- [ ] `test_dispensa_appl_valor` — `verificar_dispensa()` abaixo e acima do limite
- [ ] `test_dispensa_appl_modelo` — sem modelo padronizado não dispensa APPL
- [ ] `test_nivel_risco_calculado` — `RiscoItem.save()` calcula `probabilidade × impacto`
- [ ] `test_calendario_pca` — `gerar_calendario(ano)` retorna datas corretas

### Estágio 2
- [ ] `apps/planejamento/ia_service.py` com `SYSTEM_PROMPT_MPPI` (7 níveis normativos)
- [ ] Funções IA: `gerar_etp_mppi`, `gerar_tr_mppi`, `gerar_mapa_risco`, `analisar_conformidade_dfd`, `redigir_oficio_saneamento`, `analisar_conformidade_arp`
- [ ] `SEIMPPIClient` com 4 métodos + signals de automação SEI
- [ ] `get_analytics_srp()` completo
- [ ] Dashboard consolidado: `GET /api/v1/dashboard/`
- [ ] `GET /api/v1/srp/analytics/`
- [ ] Celery Beat configurado (docker-compose com Redis)

### Estágio 3
- [ ] Análise de viabilidade da fase externa: CNMP + SEGES/MGI
- [ ] `OrgaoMiddleware` para multi-tenancy por fundo
- [ ] Analytics de eficiência do PCA
- [ ] Relatórios bimestrais de risco PCA automatizados
- [ ] `apps/pncp/qualidade.py`: validações CATMAT/CATSER e relatório de inconsistências

---

## 7. Próximos passos imediatos (ordem sugerida)

1. **Testes unitários do SRP** — prioridade máxima antes de avançar; os models já estão prontos e as regras de negócio críticas precisam de cobertura antes de qualquer deploy.

2. **App `planejamento`** — criar models ETP, MatrizRisco, TermoReferencia; vincular ao `ItemPCA` já existente.

3. **App `juridico`** — `ControleJuridico.verificar_dispensa()` e fixtures dos MJRs; bloqueia PCA sem este controle.

4. **App `contratos`** — models locais (não confundir com `ContratoComprasnet` que é importado via API); adicionar `Aditivo.clean()` com validação de prazo.

5. **App `pncp`** — `PNCPClient` + serializers + Celery task de publicação; é condição de eficácia dos contratos (art. 174 NLLC).

6. **App `notificacoes`** — Celery Beat para alertas de vigência e prazos do PCA; depende da configuração do Redis/Celery.

7. **API REST (DRF)** — endpoints do SRP primeiro (já tem models e services maduros), depois PCA, depois planejamento.

8. **App `cotacao`** — pesquisa de preços conforme Acórdão TCU 1712/2025; bloqueante para os apps de planejamento.

9. **Admin Django** — configurar `list_display`, `list_filter`, `search_fields` e `inlines` para todos os models do SRP e PCA.

10. **Estágio 2** — IA generativa e integração SEI após estabilização do ciclo interno completo.
