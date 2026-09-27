# MVP — Agregador de Imóveis

## 1. Objetivo do projeto

Construir um buscador/agregador de imóveis que:

1. colete anúncios de fontes autorizadas ou permitidas;
2. normalize os dados coletados;
3. identifique anúncios que provavelmente representam o mesmo imóvel;
4. permita busca e filtros;
5. compare ofertas do mesmo imóvel;
6. mantenha histórico de preço;
7. redirecione o usuário para o anúncio original;
8. registre cliques/redirecionamentos para futura análise e monetização.

O produto NÃO deve substituir os portais de origem.

A conversão, contato com anunciante e fechamento devem acontecer no site original.

---

# 2. Princípios do MVP

Prioridades:

- simplicidade;
- arquitetura extensível;
- baixo custo inicial;
- monólito modular;
- providers desacoplados;
- ingestão assíncrona;
- deduplicação inicialmente baseada em regras;
- nenhuma dependência obrigatória de IA;
- nenhuma dependência obrigatória de scraping de portais que o proíbam.

O MVP deve funcionar inicialmente com 1 ou 2 fontes.

---

# 3. Stack inicial

## Backend

- Python 3.12
- Django
- Django REST Framework

## Banco

- PostgreSQL

## Processamento assíncrono

- Celery
- Redis

## Frontend

- React
- TypeScript
- Vite

## Infra local

- Docker
- Docker Compose

## Testes

- pytest
- pytest-django

---

# 4. Arquitetura

```text
                     FONTES

             API / XML / Crawler

                     ↓

                Providers

                     ↓

                  Celery

                     ↓

                Normalizer

                     ↓

                 Listing

                     ↓

               Deduplicator

                     ↓

                 Property

                     ↓

                PostgreSQL

                     ↓

              Django REST API

                 ↙       ↘

              React     Redirect
                           ↓
                     Site original
```

O projeto deve começar como um monólito Django modular.

Não criar microserviços no MVP.

---

# 5. Organização sugerida do backend

```text
backend/
├── config/
│   ├── settings/
│   ├── urls.py
│   ├── celery.py
│   └── wsgi.py
│
├── apps/
│   ├── properties/
│   │   ├── models.py
│   │   ├── services/
│   │   ├── selectors/
│   │   ├── serializers.py
│   │   ├── filters.py
│   │   ├── views.py
│   │   └── tests/
│   │
│   ├── listings/
│   │   ├── models.py
│   │   ├── services/
│   │   ├── serializers.py
│   │   └── tests/
│   │
│   ├── sources/
│   │   ├── models.py
│   │   ├── providers/
│   │   ├── crawlers/
│   │   ├── normalizers/
│   │   └── tests/
│   │
│   ├── ingestion/
│   │   ├── tasks.py
│   │   ├── services/
│   │   └── tests/
│   │
│   ├── deduplication/
│   │   ├── services/
│   │   └── tests/
│   │
│   └── analytics/
│       ├── models.py
│       ├── services/
│       └── tests/
│
├── manage.py
├── pyproject.toml
└── Dockerfile
```

---

# 6. Entidades principais

## Source

Representa uma fonte de anúncios.

Campos sugeridos:

```text
id
name
slug

provider_type
base_url

is_active

can_store_images
can_store_description

created_at
updated_at
```

Valores possíveis de `provider_type`:

```text
api
xml
crawler
manual
```

---

## Property

Representa o imóvel físico/conceitual.

```text
id

property_type

city
state
neighborhood

latitude
longitude

area

bedrooms
bathrooms
suites
parking_spaces

created_at
updated_at
```

O Property não representa um anúncio.

Ele representa a entidade que pode possuir vários anúncios.

---

## Listing

Representa um anúncio encontrado em uma fonte.

```text
id

property_id
source_id

external_id

title
description

transaction_type
property_type

price
condominium_fee
iptu

area

bedrooms
bathrooms
suites
parking_spaces

city
state
neighborhood

latitude
longitude

url

published_at

first_seen_at
last_seen_at

is_active

created_at
updated_at
```

Constraint recomendada:

```text
(source_id, external_id) UNIQUE
```

---

## ListingPriceHistory

```text
id
listing_id
price
captured_at
```

Sempre que o preço mudar, inserir um novo registro.

---

## RedirectEvent

Registra saída para o site original.

```text
id
listing_id
property_id

session_id

created_at

referer
user_agent
```

Evitar armazenar dado pessoal desnecessário.

---

# 7. Contrato de Provider

Todas as fontes devem implementar um contrato comum.

Exemplo:

```python
from abc import ABC, abstractmethod

class ListingProvider(ABC):

    @abstractmethod
    def discover(self):
        raise NotImplementedError

    @abstractmethod
    def fetch(self, reference):
        raise NotImplementedError

    @abstractmethod
    def parse(self, payload):
        raise NotImplementedError
```

Implementações possíveis:

```text
ApiProvider
XmlFeedProvider
CrawlerProvider
ManualProvider
```

Providers concretos devem ficar separados da lógica de negócio.

Exemplo:

```text
sources/providers/imobiliaria_x.py
sources/providers/imobiliaria_y.py
```

---

# 8. Objetos intermediários

Crawler/provider não deve gravar diretamente em `Listing`.

Criar objeto intermediário.

Exemplo:

```python
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class RawListing:
    source_external_id: str

    title: str | None
    description: str | None

    transaction_type: str | None
    property_type: str | None

    price: Decimal | None
    condominium_fee: Decimal | None
    iptu: Decimal | None

    area: float | None

    bedrooms: int | None
    bathrooms: int | None
    suites: int | None
    parking_spaces: int | None

    city: str | None
    state: str | None
    neighborhood: str | None

    latitude: float | None
    longitude: float | None

    url: str
```

Pipeline:

```text
Provider
   ↓
RawListing
   ↓
Normalizer
   ↓
NormalizedListing
   ↓
Upsert Listing
```

---

# 9. Normalização

Criar uma camada independente responsável por converter diferenças entre fontes.

Exemplos:

```text
"3 dormitórios"
"3 dorms"
"3 quartos"
```

deve resultar em:

```text
bedrooms = 3
```

Preço:

```text
R$ 650.000
R$650.000,00
650000
```

deve resultar em:

```text
Decimal("650000.00")
```

Normalizar inicialmente:

- preço;
- condomínio;
- IPTU;
- área;
- quartos;
- banheiros;
- suítes;
- vagas;
- cidade;
- estado;
- bairro;
- tipo do imóvel;
- tipo da negociação.

---

# 10. Pipeline de ingestão

Fluxo inicial:

```text
Celery Beat
    ↓
sync_source(source_id)
    ↓
provider.discover()
    ↓
enqueue referências
    ↓
fetch_listing(reference)
    ↓
provider.fetch()
    ↓
provider.parse()
    ↓
normalize()
    ↓
upsert_listing()
    ↓
price_history()
    ↓
deduplicate()
```

Separar tarefas pesadas.

Sugestão inicial:

```text
sync_source
fetch_listing
process_listing
deduplicate_listing
```

---

# 11. Políticas para crawler

O crawler deve ser usado somente em fontes onde seu uso seja autorizado ou permitido.

Regras:

- respeitar Termos de Uso;
- verificar robots.txt;
- utilizar identificação clara quando aplicável;
- usar rate limit;
- utilizar cache;
- evitar requisições desnecessárias;
- não contornar CAPTCHA;
- não contornar login;
- não contornar bloqueios;
- não rotacionar IP para escapar de proteção;
- não acessar endpoints privados;
- não coletar telefone/e-mail sem necessidade e base adequada;
- armazenar a URL original;
- permitir remoção de uma fonte;
- refletir exclusões/inativação do anúncio.

---

# 12. Deduplicação V1

Não utilizar machine learning inicialmente.

Criar score baseado em regras.

Exemplo:

```text
mesma cidade                +10
mesmo bairro                +20
área dentro de ±5%          +20
quartos iguais              +15
banheiros iguais            +5
vagas iguais                +10
preço dentro de ±10%        +5
coordenadas próximas        +15
```

Score sugerido:

```text
>= 80 -> provável duplicidade
60-79 -> revisar/considerar
< 60 -> imóveis diferentes
```

A pontuação deverá ser configurável.

---

# 13. Estratégia para criação de Property

Ao processar um novo Listing:

```text
novo listing
     ↓
buscar Properties candidatos
     ↓
calcular similarity score
     ↓
score suficiente?
   ↙       ↘
 SIM       NÃO
 ↓          ↓
associar   criar Property
```

Não comparar contra todos os imóveis.

Primeiro reduzir candidatos por:

```text
cidade
bairro
property_type
faixa de área
quartos
```

---

# 14. Evolução futura da deduplicação

Não implementar no MVP, mas deixar a arquitetura preparada para:

- embeddings de texto;
- similaridade de descrição;
- perceptual hash de imagens;
- geolocalização;
- machine learning;
- score baseado em histórico.

---

# 15. Histórico de preço

Ao atualizar um Listing:

```python
if listing.price != new_price:
    ListingPriceHistory.objects.create(
        listing=listing,
        price=new_price,
    )
```

Informações derivadas:

```text
preço atual
preço anterior
menor preço registrado
maior preço registrado
queda percentual
dias desde primeira captura
```

---

# 16. API do MVP

## Listar imóveis

```http
GET /api/properties/
```

Filtros:

```text
city
state
neighborhood

transaction_type
property_type

min_price
max_price

min_area
max_area

bedrooms
bathrooms
parking_spaces

ordering
page
```

---

## Detalhes do imóvel

```http
GET /api/properties/{id}/
```

Resposta deverá incluir:

```text
dados do Property
menor preço
quantidade de ofertas
lista de Listings
histórico resumido
```

---

## Redirecionar para oferta

```http
GET /out/{listing_id}/
```

Fluxo:

```text
registrar RedirectEvent
        ↓
HTTP 302
        ↓
listing.url
```

---

# 17. Ordenação

Implementar no MVP:

```text
menor preço
maior preço
menor preço/m²
maior área
mais recente
maior queda de preço
```

---

# 18. Frontend

## Página inicial

Campos:

```text
Comprar / Alugar

Cidade

Preço máximo

Quartos

[ Buscar ]
```

---

## Resultados

Card:

```text
Apartamento

Buritis — Belo Horizonte

90 m²
3 quartos
2 vagas

A partir de
R$ 599.000

3 ofertas

[ Ver ofertas ]
```

---

## Detalhes

Exemplo:

```text
Apartamento — Buritis

90 m²
3 quartos
2 vagas

Menor preço
R$ 599.000

Preço caiu R$ 21.000
desde a primeira captura


OFERTAS

Fonte A
R$ 599.000
[ Ver anúncio ]

Fonte B
R$ 615.000
[ Ver anúncio ]

Fonte C
R$ 620.000
[ Ver anúncio ]
```

---

# 19. Métricas mínimas

Registrar:

```text
quantidade de fontes
listings ativos
properties ativos
duplicidades identificadas
históricos de preço
pesquisas
visualizações de Property
redirects
CTR por fonte
```

---

# 20. Fora do MVP

Não implementar inicialmente:

- aplicativo mobile;
- financiamento;
- chat;
- CRM;
- login social;
- cadastro de corretores;
- favoritos sincronizados;
- notificações push;
- mapa avançado;
- busca por IA;
- ML para deduplicação;
- recomendação personalizada;
- avaliação automática de imóvel.

---

# 21. Roadmap

## Sprint 0 — Bootstrap

Objetivo:

subir ambiente local.

Entregas:

- repositório;
- `.gitignore`;
- `.env.example`;
- Docker Compose;
- PostgreSQL;
- Redis;
- Django;
- Celery;
- health check;
- frontend React.

Critério de aceite:

```text
docker compose up
```

deve subir:

```text
backend
postgres
redis
celery
frontend
```

---

# 22. Sprint 1 — Domínio

Implementar:

```text
Source
Property
Listing
ListingPriceHistory
RedirectEvent
```

Também:

- migrations;
- admin;
- factories;
- testes dos modelos;
- constraints.

Critério de aceite:

ser possível cadastrar manualmente uma fonte e anúncios.

---

# 23. Sprint 2 — Provider framework

Criar:

```text
ListingProvider
CrawlerProvider
ApiProvider
XmlFeedProvider
```

Implementar:

```text
RawListing
Normalizer
NormalizedListing
```

Criar uma fonte inicial.

Critério de aceite:

executar provider e persistir Listings normalizados.

---

# 24. Sprint 3 — Celery e ingestão

Criar tasks:

```text
sync_source
fetch_listing
process_listing
```

Criar agendamento com Celery Beat.

Implementar:

- retry;
- timeout;
- logs;
- controle de erros;
- rate limit por fonte.

Critério de aceite:

um source ativo ser sincronizado automaticamente.

---

# 25. Sprint 4 — Histórico

Implementar:

- atualização idempotente;
- detecção de mudança de preço;
- ListingPriceHistory;
- atualização de `last_seen_at`;
- desativação de listings não encontrados.

Critério de aceite:

alterar o preço na fonte deve criar histórico.

---

# 26. Sprint 5 — Deduplicação

Implementar:

```text
candidate selector
similarity calculator
threshold
property matcher
```

Critério de aceite:

dois anúncios equivalentes em fontes diferentes devem ser associados ao mesmo Property.

---

# 27. Sprint 6 — REST API

Implementar:

```text
GET /api/properties/
GET /api/properties/{id}/
GET /out/{listing_id}/
```

Adicionar:

- filtros;
- paginação;
- ordenação;
- documentação OpenAPI.

Critério de aceite:

ser possível fazer uma busca completa pelo backend.

---

# 28. Sprint 7 — Frontend

Criar:

```text
Home
SearchResults
PropertyDetails
```

Critério de aceite:

usuário consegue:

```text
buscar
↓
visualizar resultados
↓
abrir imóvel
↓
comparar ofertas
↓
clicar no anúncio original
```

---

# 29. Sprint 8 — Métricas básicas

Adicionar:

- visualização de imóvel;
- redirect;
- CTR por fonte;
- quantidade de listings;
- quantidade de properties;
- percentual de duplicidade.

Não criar dashboard complexo inicialmente.

---

# 30. Definição de MVP concluído

O MVP está concluído quando o fluxo abaixo funcionar:

```text
Usuário pesquisa:

Apartamento
Belo Horizonte
3 quartos
até R$ 700 mil

              ↓

Sistema retorna:

87 imóveis únicos
115 anúncios

              ↓

Apartamento X

Fonte A     R$ 599.000
Fonte B     R$ 615.000
Fonte C     R$ 620.000

Preço caiu R$ 21 mil

              ↓

[ Ver melhor oferta ]

              ↓

redirect para a fonte original
```

---

# 31. Primeiro objetivo local

Não começar pelo crawler.

Começar pela fundação.

Primeira sessão de desenvolvimento:

## Passo 1

Criar:

```text
backend/
frontend/
docker-compose.yml
.env.example
README.md
```

## Passo 2

Subir:

```text
PostgreSQL
Redis
Django
Celery
React
```

## Passo 3

Criar apps Django:

```bash
python manage.py startapp properties
python manage.py startapp listings
python manage.py startapp sources
python manage.py startapp ingestion
python manage.py startapp deduplication
python manage.py startapp analytics
```

Preferencialmente mover para `apps/`.

## Passo 4

Implementar:

```text
Source
Property
Listing
```

antes dos demais modelos.

## Passo 5

Criar factories e testes.

## Passo 6

Cadastrar manualmente dados fictícios.

Exemplo:

```text
Property

Apartamento
Buritis
90 m²
3 quartos
2 vagas
```

Listings:

```text
Fonte A
R$ 599.000

Fonte B
R$ 615.000
```

## Passo 7

Somente depois começar o framework de providers.

---

# 32. Instrução recomendada para iniciar sessão com agente de código

Pode-se iniciar uma sessão local usando este prompt:

```text
Estamos iniciando o desenvolvimento de um MVP chamado Agregador de Imóveis.

Leia integralmente o arquivo DEVELOPMENT_PLAN.md antes de alterar qualquer arquivo.

O objetivo do produto é agregar anúncios imobiliários de fontes autorizadas ou permitidas, normalizar os dados, identificar anúncios duplicados que representam o mesmo imóvel, manter histórico de preços e redirecionar o usuário para a oferta original.

Stack:

- Python 3.12
- Django
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- React
- TypeScript
- Vite
- Docker Compose
- pytest

Diretrizes:

- não criar microserviços;
- usar monólito Django modular;
- manter providers desacoplados do domínio;
- crawler/provider nunca deve salvar diretamente no modelo Listing;
- usar RawListing -> Normalizer -> Listing;
- priorizar código simples;
- não implementar funcionalidades fora do MVP;
- criar testes para regras de domínio importantes;
- não implementar scraping de sites sem autorização/permissão.

Comece pela Sprint 0 descrita em DEVELOPMENT_PLAN.md.

Antes de implementar, inspecione o estado atual do repositório e apresente um plano curto das alterações.

Depois execute a implementação da Sprint 0.
```

---

# 33. Regras para o agente de desenvolvimento

Sempre que continuar uma nova sessão:

```text
1. Ler DEVELOPMENT_PLAN.md.
2. Verificar git status.
3. Verificar estrutura atual.
4. Identificar sprint atual.
5. Não avançar para próxima sprint sem completar critérios de aceite.
6. Criar testes junto com regras de domínio.
7. Manter migrations pequenas.
8. Não adicionar dependências desnecessárias.
9. Não alterar arquitetura sem justificar.
10. Atualizar README quando necessário.
```

---

# 34. Primeira milestone

Nome sugerido:

```text
M1 — Searchable Inventory
```

Inclui:

```text
Source
Property
Listing
provider framework
1 fonte
normalização
ingestão
API de busca
frontend básico
redirect
```

Ainda sem deduplicação sofisticada.

---

# 35. Segunda milestone

```text
M2 — Property Intelligence
```

Inclui:

```text
deduplicação
histórico de preço
preço por m²
queda de preço
múltiplas ofertas
analytics
```

---

# 36. Ideias futuras

Após validar o MVP:

```text
alertas de novos imóveis
alertas de queda de preço
favoritos
busca semântica
mapa
comparação de bairros
score de oportunidade
preço/m² regional
histórico de disponibilidade
parcerias com imobiliárias
feeds próprios
API pública
```

---

# 37. Regra central do produto

O ativo principal não deve ser o crawler.

O ativo principal deve ser:

```text
dados normalizados
+
deduplicação
+
histórico
+
comparação
+
busca
```

Isso permite substituir qualquer fonte de coleta no futuro sem reconstruir o produto.
