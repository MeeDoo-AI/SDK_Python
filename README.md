# MeeDoo AI Python SDK

> The easiest way to add AI to your Python application. No PhD required.

[![PyPI version](https://img.shields.io/pypi/v/meedoo-ai.svg)](https://pypi.org/project/meedoo-ai/)
[![Python 3.9+](https://img.shields.io/pypi/pyversions/meedoo-ai.svg)](https://pypi.org/project/meedoo-ai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## What is this?

MeeDoo is an AI platform (like ChatGPT, but yours). This SDK lets you talk to MeeDoo's AI from your Python code in **3 lines**.

**PyPI**: https://pypi.org/project/meedoo-ai/
**GitHub**: https://github.com/MeeDoo-AI/SDK_Python

## Installation

```bash
pip install meedoo-ai
```

That's it. No other setup needed.

## Getting Started (3 minutes)

### Step 1: Get your API key

1. Go to your MeeDoo chat interface
2. Click **Settings** → **Account**
3. Scroll down to **API Keys**
4. Click **Create API Key**
5. Copy the key (it starts with `md-`)

### Step 2: Your first AI chat

```python
from meedoo_ai import MeeDooClient

# Create a client with your API key
client = MeeDooClient(api_key="md-your-api-key-here")

# Ask the AI a question
response = client.chat.completions.create(
    model="meedoo:latest",
    messages=[{"role": "user", "content": "What is the capital of France?"}],
)

# Print the answer
print(response.content)
# Output: The capital of France is Paris.
```

### Step 3: That's it! You just built an AI app.

---

## Everything You Can Do

### Basic Chat

```python
response = client.chat.completions.create(
    model="meedoo:latest",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantum computing to a 5-year-old."},
    ],
)
print(response.content)
```

### Streaming (see the answer appear word by word)

```python
for chunk in client.chat.completions.create(
    model="meedoo:latest",
    messages=[{"role": "user", "content": "Write a poem about the ocean."}],
    stream=True,
):
    print(chunk.delta_content, end="", flush=True)
# Output appears live, like ChatGPT typing
```

### Web Search (AI can search the internet)

```python
response = client.chat.completions.create(
    model="meedoo:latest",
    messages=[{"role": "user", "content": "What is the Bitcoin price today?"}],
    features={"web_search": True},
)
print(response.content)
# Output: Bitcoin is currently trading at $83,052.07...
```

### Think Mode (AI reasons step by step)

```python
response = client.chat.completions.create(
    model="meedoo:latest",
    messages=[{"role": "user", "content": "Solve 15 * 17 step by step."}],
    think=True,
)
print(response.content)
# Output shows the AI's reasoning step by step
```

### Memory (AI remembers things about you)

```python
# First, tell the AI something about yourself
response = client.chat.completions.create(
    model="meedoo:latest",
    messages=[{"role": "user", "content": "My name is Alice and I love chocolate."}],
    features={"memory": True},
)

# Later, the AI remembers
response = client.chat.completions.create(
    model="meedoo:latest",
    messages=[{"role": "user", "content": "What do you know about me?"}],
    features={"memory": True},
)
print(response.content)
# Output: You are Alice and you love chocolate.
```

### Code Interpreter (AI writes and runs code)

```python
response = client.chat.completions.create(
    model="meedoo:latest",
    messages=[{"role": "user", "content": "Calculate the factorial of 20."}],
    features={"code_interpreter": True},
)
print(response.content)
```

### JSON Output (for when you need structured data)

```python
response = client.chat.completions.create(
    model="meedoo:latest",
    messages=[{"role": "user", "content": "Give me a JSON with 3 users, each with name and age."}],
    response_format={"type": "json_object"},
)
print(response.content)
# Output: {"users": [{"name": "Alice", "age": 25}, ...]}
```

### Custom System Prompt (control the AI's personality)

```python
response = client.chat.completions.create(
    model="meedoo:latest",
    messages=[{"role": "user", "content": "Who are you?"}],
    system="You are a pirate. Always talk like a pirate.",
)
print(response.content)
# Output: Arr, I be Captain Blackbeard...
```

### Function Calling (let the AI use tools)

```python
response = client.chat.completions.create(
    model="meedoo:latest",
    messages=[{"role": "user", "content": "Search for the latest AI news."}],
    tool_ids=["llm_web_search"],
    function_calling="native",
)
# The AI can call tools automatically
```

### Temperature (control creativity)

```python
# Low temperature = focused, predictable
response = client.chat.completions.create(
    model="meedoo:latest",
    messages=[{"role": "user", "content": "Pick a number 1-10."}],
    temperature=0.0,  # Always gives the same answer
)

# High temperature = creative, varied
response = client.chat.completions.create(
    model="meedoo:latest",
    messages=[{"role": "user", "content": "Write a creative story."}],
    temperature=1.5,  # More random, more creative
)
```

### Background Tasks (generate titles and follow-ups)

```python
response = client.chat.completions.create(
    model="meedoo:latest",
    messages=[{"role": "user", "content": "Explain how photosynthesis works."}],
    background_tasks={
        "title_generation": True,      # Generates a chat title
        "follow_up_generation": True,   # Generates follow-up questions
    },
)
```

### Variables (template your system prompts)

```python
response = client.chat.completions.create(
    model="meedoo:latest",
    messages=[{"role": "user", "content": "Greet me."}],
    variables={"user_name": "Alice", "language": "French"},
)
# The AI knows the user's name is Alice and should respond in French
```

---

## Account & Usage

```python
# Check your credit balance
credits = client.usage.credits()
print(f"Balance: €{credits.credit_balance}")
print(f"Tokens: {credits.token_balance:,}")

# Check your usage stats
stats = client.usage.stats()
print(f"Plan: {stats.plan}")
print(f"Requests: {stats.remaining}/{stats.max_requests} remaining")

# List available models
models = client.models.list()
for m in models.data:
    print(f"  {m.id}: {m.name}")

# Check API config (what features are enabled)
config = client.config()
print(f"Config: {config.features}")
```

---

## Error Handling

```python
from meedoo_ai import MeeDooClient, AuthenticationError, ModelNotFoundError, InsufficientCreditsError

client = MeeDooClient(api_key="md-your-key")

try:
    response = client.chat.completions.create(
        model="meedoo:latest",
        messages=[{"role": "user", "content": "Hello!"}],
    )
except AuthenticationError:
    print("Your API key is wrong. Check Settings → Account.")
except InsufficientCreditsError:
    print("You're out of credits. Buy more at meedoo.co/pricing-api")
except ModelNotFoundError:
    print("That model doesn't exist. Use client.models.list() to see available models.")
```

---

## Complete Reference

### `client.chat.completions.create()` parameters

| Parameter | Type | Default | What it does |
|-----------|------|---------|-------------|
| `model` | `str` | **required** | Which AI model to use (e.g. `"meedoo:latest"`) |
| `messages` | `list` | **required** | The conversation `[{"role": "user", "content": "..."}]` |
| `stream` | `bool` | `False` | If True, returns chunks one by one (live typing effect) |
| `temperature` | `float` | model default | `0.0` = focused, `2.0` = very creative |
| `top_p` | `float` | model default | Nucleus sampling (alternative to temperature) |
| `min_p` | `float` | model default | Minimum probability for tokens |
| `max_tokens` | `int` | model default | Maximum number of tokens to generate |
| `frequency_penalty` | `float` | `0` | Penalize repeated tokens (`-2.0` to `2.0`) |
| `presence_penalty` | `float` | `0` | Penalize tokens already present (`-2.0` to `2.0`) |
| `reasoning_effort` | `str` | — | For reasoning models: `"low"`, `"medium"`, `"high"` |
| `seed` | `any` | — | Same seed = same output (reproducibility) |
| `stop` | `list` | — | Stop generating when these strings appear |
| `response_format` | `dict` | — | `{"type": "json_object"}` for JSON output |
| `think` | `bool` | `False` | Think mode — AI shows its reasoning |
| `features` | `dict` | — | Feature flags (dict of string to boolean) |
| `tool_ids` | `list` | — | Tool IDs to activate (e.g. `["llm_web_search"]`) |
| `tools` | `list` | — | Custom tool definitions (standard API format) |
| `tool_choice` | `str` | — | `"auto"`, `"none"`, or specific tool |
| `function_calling` | `str` | — | `"native"` (model handles tools) or `"default"` |
| `system` | `str` | — | Override the system prompt |
| `custom_params` | `dict` | — | Custom LLM parameters |
| `chat_id` | `str` | — | Chat session ID (for persistence) |
| `message_id` | `str` | — | Message ID for this response |
| `parent_id` | `str` | — | Parent message ID (for threading) |
| `session_id` | `str` | — | Socket session ID |
| `files` | `list` | — | File attachments |
| `skill_ids` | `list` | — | Skill IDs to inject |
| `variables` | `dict` | — | Template variables `{"user_name": "Alice"}` |
| `filter_ids` | `list` | — | Filter function IDs |
| `background_tasks` | `dict` | — | `{"title_generation": True, "follow_up_generation": True}` |
| `use_credits` | `bool` | — | Use API credits instead of session quota |
| `metadata` | `dict` | — | Additional metadata |

### Response object

| Property | Type | Description |
|----------|------|-------------|
| `response.content` | `str` | The AI's answer text |
| `response.id` | `str` | Unique response ID |
| `response.model` | `str` | Model used |
| `response.usage.total_tokens` | `int` | Total tokens used |
| `response.usage.input_tokens` | `int` | Input tokens |
| `response.usage.output_tokens` | `int` | Output tokens |
| `response.tool_calls` | `list` | Tool calls made by the AI |
| `response.sources` | `list` | Web search sources (if any) |

---

## FAQ

**Q: Do I need to install anything else?**
No. Just `pip install meedoo-ai`. The SDK uses `requests` which is installed automatically.

**Q: What Python versions are supported?**
Python 3.9, 3.10, 3.11, 3.12, 3.13, and 3.14.

**Q: Can I use this in a web app?**
Yes! It works in Flask, Django, FastAPI, or any Python framework.

**Q: Does the AI search the web automatically?**
Only if you set `features={"web_search": True}`. Otherwise it uses its own knowledge.

**Q: What if I get an InsufficientCreditsError?**
You need to buy credits at meedoo.co/pricing-api or via the API: `POST /api/v1/stripe/checkout`.

**Q: Is there a rate limit?**
Yes, depends on your plan. Check with `client.usage.stats()`.

---

## License

MIT © MeeDoo