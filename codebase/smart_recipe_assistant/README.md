# Smart Recipe Assistant

![Smart Recipe Assistant Demo](agent_demo.gif)

## Overview

**Smart Recipe Assistant** is an AI-powered culinary companion built with Google's Agent Development Kit (ADK) and Google Cloud services. It helps users search and save recipes, scale ingredient proportions and unit measurements, generate dish preview images and short cooking videos, store dietary restrictions and allergies across sessions, locate nearby grocery stores, and render interactive UI cards.

---

## Architecture & Integrated Google Cloud Services

The agent's capabilities are driven by the code in `app/` and configured in `agents-cli-manifest.yaml`:

### 🧠 Google Cloud Services
- **Vertex AI Memory Bank Service**: Cross-session memory persistence (`VertexAiMemoryBankService`) to remember user dietary restrictions, food allergies (e.g. peanuts, dairy, gluten), and culinary preferences across chat conversations.
- **Google Cloud Firestore**: Recipe catalog persistence and querying using the `recipes` collection.
- **Google Cloud Storage**: Public bucket hosting (`smart-recipe-assistant-assets-qwiklabs-01`) for generated dish preview images and cooking videos.
- **Vertex AI Imagen (`imagen-3.0-generate-002`)**: Generates realistic dish preview images and returns public Cloud Storage HTTPS URLs.
- **Vertex AI Gemini Omni (`gemini-omni-flash-preview`)**: Generates short cooking preview videos in the `global` location.
- **Vertex AI Agent Engine / Agent Runtime**: Manages agent execution and provides a secure Python code execution sandbox (`AgentEngineSandboxCodeExecutor`).
- **Google Maps & Places APIs**: Provides physical address geocoding and nearby grocery store/specialty market discovery.

### 🛠️ Core Implemented Agent Tools
- `search_recipes`: Searches Firestore database for recipes by tags, prep time, or ingredient constraints.
- `add_recipe`: Stores user-contributed recipes directly into the Firestore collection.
- `scale_recipe_servings`: Dynamically scales recipe ingredient amounts and converts between imperial/metric units.
- `search_external_recipes`: Performs web recipe lookups using Google Custom Search API.
- `geocode_address`: Converts physical addresses into latitude/longitude coordinates via Google Maps API.
- `find_nearby_places`: Locates nearby grocery stores and ingredients markets via Google Places API.
- `generate_recipe_image`: Generates dish images via Imagen 3, saves artifacts for the UI, and uploads public Cloud Storage URLs.
- `generate_recipe_video`: Generates short cooking videos via Gemini Omni, saves artifacts, and uploads public Cloud Storage URLs.
- `PreloadMemoryTool`: Loads remembered user dietary restrictions and allergies into context at the start of each conversation turn.
- `AgentEngineSandboxCodeExecutor`: Runs Python code in a secure sandbox for recipe analytics and scaling math.
- **A2UI Integration**: Formats responses into structured, interactive UI cards (`Card`, `Column`, `Row`, `Text`, `Image`) via `a2ui_callback`.

---

## Project Structure

```
smart-recipe-assistant/
├── agent_demo.gif             # Looping demo recording GIF
├── app/                       # Core agent implementation
│   ├── agent.py               # Root agent definition, system instructions, A2UI & Memory Bank setup
│   ├── tools.py               # Implemented tool logic (Firestore, Storage, Imagen, Omni, Places)
│   ├── a2ui_utils.py          # A2UI callback transformer for structured UI rendering
│   └── fast_api_app.py        # ADK FastAPI backend server entrypoint
├── frontend/                  # Single-page chat UI proxy
│   ├── main.py                # FastAPI proxy connecting to Agent Runtime via A2A protocol
│   ├── requirements.txt       # Frontend proxy dependencies
│   └── static/
│       └── index.html         # Culinary-themed single-page chat UI with prompt chips & A2UI renderer
├── agents-cli-manifest.yaml   # Agent manifest configuration
├── deployment_metadata.json   # Deployment metadata
├── pyproject.toml             # Project dependencies and environment configuration
└── README.md                  # Project documentation
```

---

## Local Setup & Run Instructions

### Prerequisites
- Python 3.11+
- `uv` package manager
- `google-cloud-sdk` (`gcloud`) authenticated to your GCP project

### 1. Run Backend & Agent Engine Dev Server

To run the agent locally with ADK and Vertex AI Memory Bank:

```bash
# Install dependencies
uv sync

# Start the ADK local dev server with Memory Bank URI
uv run adk web . --port 8080 --reload_agents --memory_service_uri=agentengine://<YOUR_MEMORY_BANK_ID>
```

### 2. Run Local Frontend Proxy

To run the culinary-themed single-page chat UI:

```bash
cd frontend

# Install frontend dependencies
pip install -r requirements.txt

# Set environment variables for deployed Agent Runtime resource
export AGENT_ENGINE_RESOURCE_NAME="projects/<PROJECT_ID>/locations/<REGION>/reasoningEngines/<ENGINE_ID>"
export AGENT_DIRECTORY="app"

# Start frontend proxy server
python main.py
```

---

## Deployment Instructions

### Deploy Agent to Vertex AI Agent Runtime

```bash
agents-cli deploy
```

### Deploy Frontend to Cloud Run

```bash
cd frontend
gcloud run deploy smart-recipe-assistant-frontend \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="AGENT_ENGINE_RESOURCE_NAME=$AGENT_ENGINE_RESOURCE_NAME,AGENT_DIRECTORY=app"
```
