# Prompt para iniciar a sessão local

Estamos iniciando o desenvolvimento de um MVP chamado **Agregador de Imóveis**.

Leia integralmente o arquivo `DEVELOPMENT_PLAN.md` antes de alterar qualquer arquivo.

## Objetivo

Construir um buscador que agregue anúncios imobiliários de fontes autorizadas ou permitidas, normalize os dados, identifique anúncios duplicados que representam o mesmo imóvel, mantenha histórico de preços e redirecione o usuário para a oferta original.

## Stack

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

## Diretrizes

- não criar microserviços;
- usar monólito Django modular;
- providers devem permanecer desacoplados do domínio;
- crawler/provider nunca salva diretamente em `Listing`;
- usar pipeline `RawListing -> Normalizer -> Listing`;
- priorizar código simples e explícito;
- não implementar funcionalidades fora do MVP;
- criar testes para regras importantes;
- não implementar scraping de fontes sem autorização/permissão;
- não adicionar dependências sem necessidade;
- migrations devem ser pequenas e revisáveis.

## Tarefa inicial

Comece pela **Sprint 0 — Bootstrap** descrita em `DEVELOPMENT_PLAN.md`.

Antes de implementar:

1. inspecione o repositório;
2. rode `git status`;
3. identifique o que já existe;
4. apresente um plano curto;
5. então implemente a Sprint 0.

Ao finalizar:

- execute os testes disponíveis;
- valide `docker compose up`;
- informe o que foi criado;
- informe pendências reais, se existirem;
- não avance para a Sprint 1 sem concluir os critérios de aceite da Sprint 0.
