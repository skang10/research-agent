```
uvx pre-commit install
uvx pre-commit autoupdate
uvx pre-commit run --all-files
```

```
uv run uvicorn app.main:app --reload
```
```
curl http://127.0.0.1:8787/
curl http://127.0.0.1:8787/docs
```
```
curl -i -X POST   http://127.0.0.1:8787/api/sources   -F "files=@tests/fixtures/test_source.pdf"

curl -X POST   http://127.0.0.1:8787/api/sources   -F "files=@tests/fixtures/test_source.txt"
curl -N -X POST   http://127.0.0.1:8787/api/research   -H "Content-Type: application/json"   -d '{"request":"Who is the attendee of the meeting?"}'
curl -N -X POST   http://127.0.0.1:8787/api/research   -H "Content-Type: application/json"   -d '{"request":"What are the latest major OpenAI announcements? Search the web."}'
```
```
uv run pytest -s -v -m integration
```


```
backend/
│
├── pyproject.toml
├── uv.lock
├── .env.example
├── .gitignore
├── README.md
├── Dockerfile
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── sources.py
│   │   └── research.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py
│   │
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── client.py
│   │   └── fake.py
│   │
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── research_agent.py
│   │   ├── context.py
│   │   ├── state.py
│   │   └── prompts.py
│   │
│   ├── retrieval/
│   │   ├── __init__.py
│   │   ├── parsing.py
│   │   ├── chunking.py
│   │   ├── embeddings.py
│   │   ├── retriever.py
│   │   └── ingest.py
│   │
│   ├── storage/
│   │   ├── __init__.py
│   │   └── vector_store.py
│   │
│   └── tools/
│       ├── __init__.py
│       ├── base.py
│       ├── local_search.py
│       ├── web_search.py
│       └── web_fetch.py
│
├── tests/
│   ├── test_sources.py
│   ├── test_research.py
│   ├── test_retrieval.py
│   └── test_agent.py
│
└── uploads/
```

```
                    Frontend
                       │
                 API layer
              ╱              ╲
       /sources              /research
          │                     │
        ingest                 Agent
          │                ╱     │     ╲
        parse           Context  LLM   Tools
          │                            ╱   ╲
        chunk                    Local    Web
          │                        │
       embedding              Retriever
          │                        │
          └──────→ Vector Store ←─┘
```
