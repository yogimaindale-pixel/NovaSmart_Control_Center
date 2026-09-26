# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
from zoneinfo import ZoneInfo

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types


def get_weather(query: str) -> str:
    """Simulates a web search. Use it get information on weather.

    Args:
        query: A string containing the location to get weather information for.

    Returns:
        A string with the simulated weather information for the queried location.
    """
    if "sf" in query.lower() or "san francisco" in query.lower():
        return "It's 60 degrees and foggy."
    return "It's 90 degrees and sunny."


def get_current_time(query: str) -> str:
    """Simulates getting the current time for a city.

    Args:
        city: The name of the city to get the current time for.

    Returns:
        A string with the current time information.
    """
    if "sf" in query.lower() or "san francisco" in query.lower():
        tz_identifier = "America/Los_Angeles"
    else:
        return f"Sorry, I don't have timezone information for query: {query}."

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    return f"The current time for query {query} is {now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}"


import json
import pathlib
from google.adk.agents.callback_context import CallbackContext
from google.adk.code_executors import AgentEngineSandboxCodeExecutor
from google.adk.memory import VertexAiMemoryBankService
from google.adk.tools.preload_memory_tool import PreloadMemoryTool

MEMORY_BANK_ID = "4153334255423848448"


# WRITE: after each turn, send the session to Memory Bank for extraction.
async def generate_memories_callback(callback_context: CallbackContext):
    await callback_context.add_session_to_memory()
    return None


def memory_bank_service_builder():
    return VertexAiMemoryBankService(
        project="qwiklabs-gcp-01-2aad14f2c696",
        location="us-central1",
        agent_engine_id=MEMORY_BANK_ID,
    )

from app.tools import (
    add_recipe,
    find_nearby_places,
    generate_recipe_image,
    generate_recipe_video,
    geocode_address,
    scale_recipe_servings,
    search_external_recipes,
    search_recipes,
)

# Load Agent Engine or Sandbox Resource Name from deployment_metadata.json
_metadata_path = pathlib.Path(__file__).parent.parent / "deployment_metadata.json"
_code_executor = None

if _metadata_path.exists():
    try:
        with open(_metadata_path) as _f:
            _meta = json.load(_f)
        _sandbox_name = _meta.get("sandbox_resource_name")
        _agent_engine_id = _meta.get("remote_agent_runtime_id")
        if _sandbox_name:
            _code_executor = AgentEngineSandboxCodeExecutor(
                sandbox_resource_name=_sandbox_name
            )
        elif _agent_engine_id:
            _code_executor = AgentEngineSandboxCodeExecutor(
                agent_engine_resource_name=_agent_engine_id
            )
    except Exception:
        pass

if _code_executor is None:
    _code_executor = AgentEngineSandboxCodeExecutor()


from a2ui.basic_catalog.provider import BasicCatalog
from a2ui.schema.manager import A2uiSchemaManager

from app.a2ui_utils import a2ui_callback

schema_manager = A2uiSchemaManager(
    version="0.8",
    catalogs=[BasicCatalog.get_config("0.8")],
)

a2ui_instruction = schema_manager.generate_system_prompt(
    role_description=(
        "You are Smart Recipe Assistant, an AI culinary guide that helps users discover recipes, "
        "generate dish images, scale ingredients, locate nearby stores, run Python code for recipe math/analytics, "
        "remember dietary preferences and user facts across sessions, and save recipes to Firestore."
    ),
    workflow_description="Analyze the request and return structured UI when appropriate.",
    ui_description=(
        "Keep every surface tiny and flat: ONE Card > ONE Column > a few Text rows. "
        "Never nest a Card inside a Card. "
        "Use ONLY these components: Card, Column, Row, Text, and Image. Do not use "
        "Table or Heading (unsupported), or Buttons, actions, or forms (they do "
        "nothing in adk web). "
        "You may include one Image component, but only when you have a public https "
        "URL for the image (for example the URL an image tool returns after uploading "
        "to a public bucket). Set the Image url to that exact https link, for example "
        "{\"Image\": {\"url\": {\"literalString\": \"https://...\"}}}. Never point an "
        "Image at a bare filename, an artifact name, or a non-http(s) path. If you do "
        "not have a public URL, add a short Text line noting the image instead. "
        "No markdown in text; use the usageHint property ('h1', 'h2', 'body') for "
        "headings and emphasis. "
        "Output ONLY the raw A2UI JSON array — no prose, and never wrap it in "
        "<a2a_datapart_json> tags or 'kind'/'data'/'metadata' objects.\n\n"
        "ALLERGY & DIETARY MEMORY INSTRUCTIONS:\n"
        "1. Active Memory Tracking: Remember and track all user allergies (e.g. peanuts, shellfish, penicillin, dairy), "
        "dietary restrictions (e.g. gluten-free, vegan, keto, halal), and food dislikes across sessions using Memory Bank.\n"
        "2. Acknowledge & Persist: Whenever the user mentions an allergy or dietary restriction, acknowledge it clearly and "
        "confirm that it will be remembered for future sessions.\n"
        "3. Safety Filtering: Before recommending any recipe, ingredient substitution, or meal plan, ALWAYS check remembered "
        "user allergies/restrictions from preloaded memory. Actively warn the user or filter out any recipes containing their allergens."
    ),
    include_schema=True,
    include_examples=True,
)


root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=a2ui_instruction,
    code_executor=_code_executor,
    tools=[
        get_weather,
        get_current_time,
        search_recipes,
        add_recipe,
        scale_recipe_servings,
        search_external_recipes,
        geocode_address,
        find_nearby_places,
        generate_recipe_image,
        generate_recipe_video,
        PreloadMemoryTool(),
    ],
    after_agent_callback=generate_memories_callback,
    after_model_callback=a2ui_callback,
)

app = App(
    root_agent=root_agent,
    name="app",
)
