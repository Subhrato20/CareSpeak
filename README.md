## Voice Agent and Symptom Search Tools

A complete, working example of a Vapi voice agent plus companion HTTP tools for symptom understanding and Amazon product recommendations. It includes:

- my-vapi-agent: A Python client that starts a real-time Vapi voice call with your assistant, plus a minimal Flask tool server for symptom-based product search.
- my-vapi-tools: A standalone, production-ready tools suite with two options:
  - A simple symptom search tool.
  - An advanced multi-layer GPT pipeline that extracts symptoms from conversations, recommends medicines, searches Amazon via SearchAPI, and formats concise responses.

### Architecture at a glance

```mermaid
flowchart LR
    U["User (voice)"] -->|speech| Vapi["Vapi Agent"]
    Vapi -->|function call (webhook)| Tool["Tool Server (Flask)"]
    subgraph Tools
      Tool -->|simple| Simple["symptom_search_tool.py"]
      Tool -->|advanced| Pipeline["symptom_search_pipeline.py"]
    end
    Simple --> SearchAPI["SearchAPI (Amazon)"]
    Pipeline --> OpenAI["OpenAI (LLM)"]
    Pipeline --> SearchAPI
    Tool -->|JSON| Vapi
    Vapi -->|audio| U
```

### Repository structure

```
4x4/
├── my-vapi-agent/                 # Local voice caller + minimal tool server
│   ├── main.py                    # Starts a real-time voice call with Vapi
│   ├── symptom_search_server.py   # Simple Flask server + /webhook for Vapi tool
│   ├── symptom_search_tool.py     # Symptom→Amazon search (simple)
│   ├── requirements.txt           # SDK + Flask + requests
│   ├── README.md                  # Agent-specific setup
│   └── tests                      # test_vapi_client.py, test_symptom_search*.py
└── my-vapi-tools/                 # Standalone tools service (recommended)
    ├── symptom_search_tool.py     # Simple tool (optional LLM formatting)
    ├── symptom_search_pipeline.py # Multi-layer GPT pipeline tool
    ├── symptom_search_server.py   # Flask service exposing endpoints + webhook
    ├── vapi_tool_config.json      # Tool definition for Vapi
    ├── requirements.txt           # Flask, requests, OpenAI, etc.
    ├── render.yaml / Procfile     # Ready-to-deploy configs
    └── tests                      # test_server.py, test_endpoints.py, test_pipeline.py
```

### What you can build with this

- Start a real-time voice call with your Vapi assistant from Python.
- Let the assistant call an HTTP tool that:
  - Parses symptom descriptions.
  - Recommends OTC medicines.
  - Finds actual Amazon products (via SearchAPI) to mention by name/price.
  - Returns a concise, voice-friendly list back to the assistant.

Note: These tools provide general information and are not medical advice.

## Quick start

You can run either the simple tool or the advanced pipeline. The tools can be used independently of the caller.

### 1) Run the standalone tools service (recommended)

```bash
cd my-vapi-tools
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp env.example .env  # add your keys
python symptom_search_server.py  # runs on http://localhost:8080
```

Set these environment variables in `my-vapi-tools/.env`:

```
SEARCHAPI_API_KEY=your-searchapi-key
# Optional but recommended for the pipeline and LLM formatting
OPENAI_API_KEY=your-openai-key
```

Test locally:

```bash
curl http://localhost:8080/health
curl -X POST http://localhost:8080/process_conversation \
  -H "Content-Type: application/json" \
  -d '{"conversation":"I have a sore throat and cough","max_results":3}'
```

Integrate with Vapi:
1) Update `my-vapi-tools/vapi_tool_config.json` to point `url` to your `/webhook` endpoint.
2) Create the tool in the Vapi dashboard (or via API) and add it to your assistant.

### 2) Start a voice call from your machine (caller)

```bash
cd my-vapi-agent
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp env.example .env  # add your VAPI_PUBLIC_KEY and ASSISTANT_ID
python main.py  # microphone and speakers required
```

Set these environment variables in `my-vapi-agent/.env`:

```
VAPI_PUBLIC_KEY=your-vapi-public-key
ASSISTANT_ID=your-assistant-id
```

macOS only: if needed, install PortAudio for microphone access: `brew install portaudio`.

## How it works

- Simple tool (`symptom_search_tool.py`):
  - Receives `symptoms` (string), maps to a search query, calls SearchAPI (Amazon), filters results, and returns a concise product list. Optional OpenAI formatting produces short numbered output.

- Multi-layer pipeline (`symptom_search_pipeline.py`):
  - Layer 1: GPT extracts symptoms, severity, duration.
  - Layer 2: GPT recommends OTC medicines.
  - Layer 3: SearchAPI fetches matching Amazon products.
  - Layer 4: GPT formats a brief numbered list (name and price only).

Both are exposed via Flask servers with a Vapi-compatible `POST /webhook`.

## Key HTTP endpoints

- my-vapi-tools service (default port 8080):
  - `GET /health` – health check
  - `GET /` – service info and pipeline steps
  - `POST /process_conversation` – run the full pipeline
  - `POST /webhook` – Vapi tool function endpoint (`process_symptom_conversation`)

- my-vapi-agent minimal server (default port 5000):
  - `GET /health`
  - `POST /search_symptoms` – simple symptom→products
  - `POST /webhook` – Vapi tool function endpoint (`search_products_for_symptoms`)

## Environment variables

- Required for tools:
  - `SEARCHAPI_API_KEY` – SearchAPI key for Amazon search
  - `OPENAI_API_KEY` – Required for the pipeline; optional for LLM formatting in the simple tool

- Required for voice caller:
  - `VAPI_PUBLIC_KEY` – From Vapi dashboard
  - `ASSISTANT_ID` – Target assistant to call

## Deployment

The `my-vapi-tools` directory includes ready-to-use configs and guides:

- Render: `render.yaml`
- Railway/Heroku: `Procfile`
- Cloud Run: Dockerfile example in docs

See:
- `my-vapi-tools/DEPLOYMENT_GUIDE.md` for detailed steps
- `my-vapi-tools/POSTMAN_TESTING_GUIDE.md` for endpoint testing

## Testing

- my-vapi-tools:
  - `python test_endpoints.py` – smoke tests against a running local server
  - `python test_pipeline.py` – runs the multi-layer pipeline
  - `python test_server.py` – basic server checks

- my-vapi-agent:
  - `python test_vapi_client.py` – verifies Vapi SDK initialization
  - `python test_symptom_search.py` – tests the simple tool logic

Notes:
- Some tests require `SEARCHAPI_API_KEY` and/or `OPENAI_API_KEY`.
- Voice calling requires audio hardware and OS permissions.

## Troubleshooting

- Proxies issue: Both services defensively clear proxy-related env vars to avoid `proxies` keyword errors with HTTP clients/SDKs. See `my-vapi-agent/PROXIES_FIX_SUMMARY.md`.
- Missing keys: Ensure `.env` files exist in each directory with required variables.
- macOS audio: Install PortAudio and grant microphone permissions.
- No/low results: Try simpler symptoms; verify SearchAPI quota and connectivity.

## License

MIT – see `LICENSE`.

## Useful links

- Vapi dashboard: https://dashboard.vapi.ai
- Vapi docs: https://docs.vapi.ai
- SearchAPI: https://www.searchapi.io/
- OpenAI: https://platform.openai.com/docs
