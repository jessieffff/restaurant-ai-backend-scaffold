# Restaurant AI Backend Scaffold

Start the Restaurant AI Agent Backend project with a working FastAPI service,
automated quality checks, local data-service definitions, GitHub workflow
templates, and an engineering documentation structure.

## Create your private implementation repository

Use this repository as a **GitHub template**, not a normal fork. A repository
created from the public template can be private, while a normal fork of a
public repository remains public.

### GitHub website

1. Select **Use this template**.
2. Select **Create a new repository**.
3. Choose your account and a project name.
4. Set visibility to **Private**.
5. Create the repository, then clone it locally.

### GitHub CLI

```bash
gh repo create YOUR_REPOSITORY_NAME \
  --private \
  --template jessieffff/restaurant-ai-backend-scaffold \
  --clone
```

## Quick start

Requirements:

- Python 3.11, 3.12, or 3.13
- Git
- Docker with Docker Compose
- GNU Make

GitHub CLI authentication is required by Session 3 for the merge guard. Ollama
is required by Session 6 for local model work. `make doctor` reports both as
later requirements without blocking the initial setup.

Prepare the local environment:

```bash
make bootstrap
make doctor
make check
```

In the generated GitHub repository, open **Actions → quality → Run workflow**
and confirm the first quality run passes.

Start only the API during early development:

```bash
make run
```

Open:

- API documentation: <http://127.0.0.1:8000/docs>
- Liveness: <http://127.0.0.1:8000/health/live>
- Readiness: <http://127.0.0.1:8000/health/ready>

Start the local service stack:

```bash
make up
make logs
```

Local services:

| Service | Address |
|---|---|
| API | <http://127.0.0.1:8000> |
| PostgreSQL with pgvector | `127.0.0.1:5432` |
| Valkey | `127.0.0.1:6379` |
| RabbitMQ AMQP | `127.0.0.1:5672` |
| RabbitMQ management | <http://127.0.0.1:15672> |

The credentials in `.env.example` are local-development placeholders only.
Do not reuse them outside the local environment.

## What is included

- FastAPI application factory
- Liveness and application-level readiness endpoints
- Pydantic settings loaded from environment variables
- Unit tests
- Ruff linting and formatting
- Strict mypy configuration
- GitHub Actions quality workflow
- Dockerfile
- Docker Compose services for PostgreSQL/pgvector, Valkey, and RabbitMQ
- Zero-cost pull-request merge guard for GitHub Free private repositories
- Issue and pull-request templates
- ADR, evidence, runbook, incident, and engineering-documentation templates
- Local bootstrap and environment doctor scripts

## Why this foundation is included

| Foundation | Purpose |
|---|---|
| Runnable FastAPI service | Verifies the Python environment and provides the first executable vertical slice |
| Quality checks and CI | Establishes one repeatable lint, type, test, and evidence workflow |
| Local data services | Provides the PostgreSQL, vector, cache, and messaging systems used across later sessions |
| GitHub templates and merge guard | Standardizes task delivery and provides a zero-cost controlled merge path |
| Engineering documentation | Preserves decisions, contracts, operations knowledge, measurements, and evidence as the system grows |

## What you build during the course

- Versioned customer, staff, and agent APIs
- PostgreSQL schema, migrations, constraints, indexes, and transactions
- Dependency-aware readiness for PostgreSQL, Valkey, and RabbitMQ
- Reservation and ordering domains
- Idempotency and concurrency controls
- Valkey caching and rate limiting
- LangGraph workflows, model gateway, typed tools, and confirmation safety
- RAG ingestion, retrieval, citations, isolation, and evaluation
- RabbitMQ topology, outbox relay, workers, retries, and dead letters
- Authentication, authorization, audit, and PII controls
- Logs, metrics, traces, SLOs, alerts, runbooks, and incident evidence
- Load testing and performance optimization
- Kubernetes deployment, smoke tests, and rollback

## Project layout

```text
.
├── .github/                 GitHub workflow and collaboration templates
├── docs/                    Architecture, contracts, evidence, and operations
├── scripts/                 Bootstrap and environment checks
├── src/restaurant_agent/
│   ├── agent/               LangGraph workflow added during the course
│   ├── api/                 FastAPI routes
│   ├── core/                Configuration and cross-cutting application setup
│   ├── domain/              Reservation, ordering, and restaurant rules
│   ├── platform/            Database, cache, broker, model, and telemetry adapters
│   ├── rag/                 Ingestion, retrieval, citations, and evaluation
│   └── worker/              Relay and asynchronous workers
└── tests/                   Automated tests
```

## First project task

After setup:

1. Run `make check`.
2. Open the generated API documentation.
3. Read `CONTRIBUTING.md`.
4. Create the first Task Issue.
5. Create a short-lived branch from `main`.
6. Make one bounded change and open a pull request.
7. Preserve the CI link in `docs/evidence/ledger.md`.

## Pull-request merge guard

Before Session 3, install and authenticate GitHub CLI:

```bash
gh auth login
```

Verify and squash-merge a pull request only after its CI checks pass:

```bash
make merge PR=123 DRY_RUN=1
make merge PR=123
```

The guard requires an open, current, mergeable pull request targeting `main`,
verifies every reported check is passing, locks the merge to the verified head
commit, squash-merges, and deletes the source branch.

## Safety

- Use synthetic data only.
- Never commit `.env`, credentials, access tokens, private keys, or real PII.
- Keep deterministic tests independent from hosted model availability.
- Keep every required workflow on a zero-payment path.

## License

MIT. See [LICENSE](LICENSE).
