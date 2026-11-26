# osu! RAG

A Retrieval-Augmented Generation (RAG) application for answering questions about **osu!** using information from the [osu! wiki](https://osu.ppy.sh/wiki/en/Main_page).

The project combines **Qwen3.5-2B** for answer generation and **BGE-small-en-v1.5** for semantic embeddings, with PostgreSQL and pgvector for vector storage and similarity search.

## Motivation

While exploring backend engineering job opportunities, I noticed that RAG and LLM-related experience appeared frequently in job requirements.

I decided to build this project to get hands-on experience with Retrieval-Augmented Generation, explore how LLMs and embedding models work together, and experiment with integrating AI capabilities into a backend application.

Note: You won't find here best programming practices while this project is RAG specific

## Tech Stack

| Component | Technology |
|---|---|
| Backend | Python, FastAPI |
| LLM | [Qwen3.5-2B](https://huggingface.co/Qwen/Qwen3.5-2B) |
| Embedding model | [BGE-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5) |
| Database | PostgreSQL |
| Vector search | pgvector |
| Database migrations | Alembic |
| Dependency management | uv |
| Infrastructure | Docker Compose |
| Testing | pytest |

## How It Works

The application follows a typical RAG pipeline:

1. **Data ingestion** — osu! wiki content is processed and stored in PostgreSQL.
2. **Embedding generation** — BGE converts textual content into vector embeddings.
3. **Retrieval** — a user's question is converted into an embedding and used to find semantically relevant documents through pgvector.
4. **Context construction** — retrieved documents are assembled into a context for the LLM.
5. **Answer generation** — Qwen3.5-2B generates an answer based on the retrieved context.

## Project Structure

The repository is organized into two main parts: the backend application and the wiki ingestion utility.

```text
.
├── alembic/                 # Database migrations
├── app/
│   ├── configs/             # Application configuration
│   ├── core/                # Database and shared infrastructure
│   ├── dtos/                # Data transfer objects
│   ├── exception_handlers/  # Exception handling
│   ├── models/               # Database models
│   ├── repositories/        # Database access layer
│   ├── routers/             # API endpoints
│   ├── services/            # Business logic and RAG services
│   └── main.py              # Application entry point
├── faqer/                   # osu! wiki ingestion utility
├── models/                  # Locally downloaded ML models
├── tests/
│   └── integration/         # Integration tests
├── docker-compose.yml
├── alembic.ini
├── pyproject.toml
├── uv.lock
└── README.md
```

## Getting Started

### Prerequisites

Make sure you have the following installed:

- [Docker](https://www.docker.com/)
- [uv](https://docs.astral.sh/uv/)

### 1. Start PostgreSQL

From the project root, start the database:

```bash
docker compose up -d
```

Connect to the PostgreSQL container:

```bash
docker compose exec pg psql -U postgres
```

Create a database and enable the pgvector extension:

```sql
CREATE DATABASE osu;
\c osu
CREATE EXTENSION IF NOT EXISTS vector;
```

### 2. Download the models

Download the following models from Hugging Face:

- [Qwen3.5-2B](https://huggingface.co/Qwen/Qwen3.5-2B)
- [BGE-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5)

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
MODELS_EMBEDDING_MODEL=/path/to/bge_model
MODELS_LLM_MODEL=/path/to/qwen_model

DATABASE_URL="postgresql+psycopg://postgres:1234@localhost:5432/osu"
```

### 4. Install dependencies and run migrations

Install the project dependencies:

```bash
uv sync
```

Apply database migrations:

```bash
uv run alembic upgrade head
```

### 5. Ingest osu! wiki data

Download the [osu! wiki repository](https://github.com/ppy/osu-wiki) and run the ingestion utility:

```bash
uv run -m faqer.main /path/to/osu-wiki
```

This processes the wiki content and populates the database with records used by the RAG pipeline.

## Running Tests

Run integration tests with:

```bash
uv run pytest -m integration
```
