# KK2 Oraklet

## Krav

Python 3.14
uv installerat
Internet vid första körningen (för att ladda ner SmolLM2-135M modellen, ca 300 MB)
## Installation

Klona repot och installera beroenden:

```bash
git clone <repo-url>
cd kk2
uv sync
```

## Köra servern

```bash
uv run uvicorn app.main:app --reload
```

Servern startar på http://127.0.0.1:8000.

Första gången tar några minuter eftersom SmolLM2-modellen laddas ner.

## Använda API:et

Enklast är att öppna Swagger UI i webbläsaren:

http://127.0.0.1:8000/docs

Där kan du testa alla endpoints direkt.

### Endpoints

#### `GET /health`

Hälsokontroll. Svarar `{"status": "ok"}`.

#### `POST /data/upload`

Ladda upp en CSV-fil. Returnerar metadata (antal rader, kolumnnamn, datatyper).

#### `GET /data/stats`

Returnerar statistik (pandas `describe()`) för det uppladdade datasetet. Returnerar 404 om inget dataset laddats upp.

#### `POST /ai/ask`

Ställ en fråga om datasetet. AI:n bygger en prompt med datasetets statistik och svarar. Returnerar 404 om inget dataset laddats upp.

## Köra tester

```bash
uv run pytest app/tests/ -v
```

## Antaganden och begränsningar

Modellen är liten (135M parametrar), svaren är ofta felaktiga eller hallucinerade. Se `reflektion.md` för exempel.
Datasetet lagras i minnet och försvinner när servern startas om. Inget databas stöd.
Engelska prompterm, modellen presterar mycket dåligt på svenska.
Maxfilstorlek är 10 MB men kan justeras via `MAX_FILE_SIZE_MB` i `app/config.py`.
## Projektstruktur

```
app/
├── main.py              # FastAPI-app och endpoints
├── config.py            # Settings (läser .env)
├── schemas.py           # Pydantic-modeller för API:t
├── data.py              # Dataset-state (in-memory)
├── chain/
│   ├── runnable.py      # Basklasser: Runnable, RunnableLambda, RunnableSequence
│   ├── steps.py         # Kedjesteg: PromptBuilder, LLMRunner, ResponseParser
│   └── pipeline.py      # Den sammansatta kedjan (oraklet)
└── tests/
├── test_endpoints.py
└── test_chain.py
```