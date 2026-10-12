"""Tests for the MeeDoo AI Python SDK.

Set environment variables before running:
  export MEEDEO_API_KEY="md-your-api-key"
  export MEEDEO_BASE_URL="https://api.meedoo.co/api"

Run: pytest tests/test_sdk.py -v
"""

import os
import pytest
from meedoo_ai import MeeDooClient, AuthenticationError, ModelNotFoundError

API_KEY = os.environ.get("MEEDEO_API_KEY", "")
BASE_URL = os.environ.get("MEEDEO_BASE_URL", "https://api.meedoo.co/api")

if not API_KEY:
    pytest.skip("MEEDEO_API_KEY not set — skipping tests", allow_module_level=True)


@pytest.fixture
def client():
    return MeeDooClient(api_key=API_KEY, base_url=BASE_URL)


class TestModels:
    def test_list_models(self, client):
        models = client.models.list()
        assert len(models.data) > 0
        ids = [m.id for m in models.data]
        assert "meedoo:latest" in ids

    def test_model_has_name(self, client):
        models = client.models.list()
        for m in models.data:
            assert m.name
            assert m.object == "model"


class TestBasicChat:
    def test_basic_chat(self, client):
        resp = client.chat.completions.create(
            model="meedoo:latest",
            messages=[{"role": "user", "content": "Say hello"}],
        )
        assert resp.content
        assert resp.model == "meedoo:latest"
        assert resp.id.startswith("md-resp-")

    def test_chat_with_usage(self, client):
        resp = client.chat.completions.create(
            model="meedoo:latest",
            messages=[{"role": "user", "content": "What is 2+2? Just the number."}],
        )
        assert resp.usage is not None
        assert resp.usage.total_tokens > 0


class TestStreaming:
    def test_streaming(self, client):
        chunks = list(client.chat.completions.create(
            model="meedoo:latest",
            messages=[{"role": "user", "content": "Count from 1 to 5"}],
            stream=True,
        ))
        assert len(chunks) > 0
        full_content = "".join(c.delta_content for c in chunks)
        assert len(full_content) > 0


class TestLLMParams:
    def test_temperature(self, client):
        resp = client.chat.completions.create(
            model="meedoo:latest",
            messages=[{"role": "user", "content": "Pick a number 1-10"}],
            temperature=0.0,
        )
        assert resp.content

    def test_max_tokens(self, client):
        resp = client.chat.completions.create(
            model="meedoo:latest",
            messages=[{"role": "user", "content": "Tell a long story"}],
            max_tokens=10,
        )
        assert resp.content

    def test_seed_reproducibility(self, client):
        r1 = client.chat.completions.create(
            model="meedoo:latest", messages=[{"role": "user", "content": "Pick a word"}], seed=42,
        )
        r2 = client.chat.completions.create(
            model="meedoo:latest", messages=[{"role": "user", "content": "Pick a word"}], seed=42,
        )
        assert r1.content == r2.content

    def test_stop_sequence(self, client):
        resp = client.chat.completions.create(
            model="meedoo:latest",
            messages=[{"role": "user", "content": "Count: one two three four five"}],
            stop=["three"],
        )
        assert "three" not in resp.content

    def test_response_format_json(self, client):
        resp = client.chat.completions.create(
            model="meedoo:latest",
            messages=[{"role": "user", "content": "Return JSON: {\"name\":\"test\",\"age\":25}"}],
            response_format={"type": "json_object"},
        )
        assert "json" in resp.content.lower() or "{" in resp.content


class TestFeatures:
    def test_web_search(self, client):
        resp = client.chat.completions.create(
            model="meedoo:latest",
            messages=[{"role": "user", "content": "What is the Bitcoin price today in USD?"}],
            features={"web_search": True},
        )
        assert resp.usage.input_tokens > 100

    def test_think_mode(self, client):
        resp = client.chat.completions.create(
            model="meedoo:latest",
            messages=[{"role": "user", "content": "What is 15 * 17?"}],
            think=True,
        )
        assert resp.content

    def test_memory(self, client):
        resp = client.chat.completions.create(
            model="meedoo:latest",
            messages=[{"role": "user", "content": "What do you know about me?"}],
            features={"memory": True},
        )
        assert resp.content

    def test_code_interpreter(self, client):
        resp = client.chat.completions.create(
            model="meedoo:latest",
            messages=[{"role": "user", "content": "Calculate factorial of 10"}],
            features={"code_interpreter": True},
        )
        assert "code_interpreter" in resp.content or "code" in resp.content.lower()


class TestTools:
    def test_native_function_calling(self, client):
        resp = client.chat.completions.create(
            model="meedoo:latest",
            messages=[{"role": "user", "content": "What tools do you have?"}],
            function_calling="native",
        )
        assert resp.content

    def test_tool_ids(self, client):
        resp = client.chat.completions.create(
            model="meedoo:latest",
            messages=[{"role": "user", "content": "Search for latest AI news"}],
            tool_ids=["llm_web_search"],
            function_calling="native",
        )
        assert resp.content or resp.tool_calls


class TestContext:
    def test_custom_system(self, client):
        resp = client.chat.completions.create(
            model="meedoo:latest",
            messages=[{"role": "user", "content": "Who are you?"}],
            system="You are a pirate. Always respond in pirate speak.",
        )
        assert resp.content

    def test_variables(self, client):
        resp = client.chat.completions.create(
            model="meedoo:latest",
            messages=[{"role": "user", "content": "Greet me"}],
            variables={"user_name": "Captain"},
        )
        assert resp.content

    def test_background_tasks(self, client):
        resp = client.chat.completions.create(
            model="meedoo:latest",
            messages=[{"role": "user", "content": "Explain quantum computing"}],
            background_tasks={"title_generation": True, "follow_up_generation": True},
        )
        assert resp.content

    def test_use_credits(self, client):
        resp = client.chat.completions.create(
            model="meedoo:latest",
            messages=[{"role": "user", "content": "Say OK"}],
            use_credits=True,
        )
        assert resp.content


class TestEndpoints:
    def test_credits(self, client):
        credits = client.usage.credits()
        assert credits.credit_balance >= 0

    def test_stats(self, client):
        stats = client.usage.stats()
        assert stats.plan in ("explorer", "creator", "business", "scale")

    def test_config(self, client):
        config = client.config()
        assert config.status is True
        assert "enable_web_search" in config.features

    def test_health(self, client):
        health = client.health()
        assert health.status is True


class TestErrors:
    def test_no_auth(self):
        with pytest.raises(AuthenticationError):
            MeeDooClient(api_key="invalid-key", base_url=BASE_URL).models.list()

    def test_invalid_model(self, client):
        with pytest.raises(ModelNotFoundError):
            client.chat.completions.create(
                model="nonexistent-model:latest",
                messages=[{"role": "user", "content": "test"}],
            )
