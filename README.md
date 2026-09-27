# Placecheck — Agregador de Imóveis

MVP de um buscador e agregador de anúncios imobiliários. O projeto segue o plano em [`DEVELOPMENT_PLAN.md`](DEVELOPMENT_PLAN.md) e começa como um monólito Django modular.

## Desenvolvimento local

1. Copie `.env.example` para `.env`.
2. Suba o ambiente:

   ```bash
   docker compose up --build
   ```

3. Acesse:
   - API: http://localhost:8000/health/
   - Frontend: http://localhost:5173

O backend executa as migrations automaticamente ao iniciar. Para executar os testes sem Docker, instale as dependências de `backend/requirements.txt` em um ambiente Python 3.12.

Possíveis sources:
- Ideal Imóveis
- Quarto Andar


## Estado atual

Sprint 2 (Provider framework) concluída. O contrato de providers, normalização, `ManualProvider` e pipeline de persistência estão disponíveis. Celery, agendamento, retries e fontes externas serão implementados nas próximas sprints.
