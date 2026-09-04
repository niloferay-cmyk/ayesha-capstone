"""ollama_integration_snippet.py — W4 activity reference.

Three changes to integrate Ollama into the existing W4 pipeline:

1. Add llama3.2:3b to cost.RATES with (0.0, 0.0) — free.
2. Add _make_client helper to pipeline.py — picks the right backend.
3. Add JSON-mode fallback for tool-calling that fails on Ollama.

Apply these inline to src/pipeline/cost.py and src/pipeline/pipeline.py.
"""
from openai import AsyncOpenAI


# ─── In src/pipeline/cost.py ────────────────────────────────────────────

# Add this entry to your existing RATES dict:
RATES_ADDITION = {
    "llama3.2:3b": (0.0, 0.0),     # input rate, output rate (both $0)
    # Other local models you might try:
    # "llama3.2:8b": (0.0, 0.0),
    # "qwen2.5:7b":  (0.0, 0.0),
    # "mistral:7b":  (0.0, 0.0),
}


# ─── In src/pipeline/pipeline.py — near the top of the file ─────────────

def _make_client(settings):
    """Return an AsyncOpenAI client pointed at the right backend.

    Ollama exposes an OpenAI-compatible endpoint at
    http://localhost:11434/v1 so we can reuse the OpenAI SDK with a
    different base_url.

    Detection: any model name starting with `llama` or `ollama:` is
    routed to Ollama; everything else goes to OpenAI.
    """
    if settings.model.startswith("llama") or settings.model.startswith("ollama:"):
        return AsyncOpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama",  # any string — Ollama doesn't check it
        )
    return AsyncOpenAI(api_key=settings.openai_api_key)


# Then in ask_llm and stream_answer, replace:
#     client = AsyncOpenAI(api_key=settings.openai_api_key)
# With:
#     client = _make_client(settings)


# ─── Tool-calling fallback for local models ─────────────────────────────

async def ask_llm_with_fallback(question, settings):
    """Tool-calling first, JSON-mode if it fails — for local models.

    llama3.2:3b's tool-calling compliance is shaky. If the model
    doesn't call answer_question, fall back to JSON mode which is
    more reliable.
    """
    client = _make_client(settings)

    # Try tool-calling first
    try:
        response = await client.chat.completions.create(
            model=settings.model,
            messages=[{"role": "user", "content": question.question}],
            tools=[ANSWER_QUESTION_TOOL],   # your existing tool spec
            tool_choice={"type": "function",
                          "name": "answer_question"},
        )
        tool_call = response.choices[0].message.tool_calls
        if tool_call:
            return _parse_tool_call(tool_call[0], response.usage,
                                     settings.model)
    except Exception:
        pass  # fall through to JSON mode

    # Fallback: JSON mode
    response = await client.chat.completions.create(
        model=settings.model,
        messages=[
            {"role": "system",
             "content": "Reply with a JSON object: "
                        '{"content": "...", "confidence": 0.0-1.0, "sources": []}'},
            {"role": "user", "content": question.question},
        ],
        response_format={"type": "json_object"},
    )
    return _parse_json_response(response, settings.model)


# Helpers _parse_tool_call, _parse_json_response, ANSWER_QUESTION_TOOL
# are already defined in your W4 pipeline.py — reuse them.
