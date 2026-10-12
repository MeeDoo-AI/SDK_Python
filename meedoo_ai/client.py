"""
MeeDoo AI Python SDK — Client

The main client class that provides access to all API endpoints.
"""

import json
import time
from typing import Any, Generator, Optional

import requests

from .exceptions import (
    APIError,
    AuthenticationError,
    InsufficientCreditsError,
    ModelNotFoundError,
    RateLimitError,
)
from .models import (
    ChatCompletion,
    ChatCompletionChunk,
    ConfigResponse,
    CreditsResponse,
    HealthResponse,
    ModelList,
    UsageResponse,
)


class ChatCompletions:
    """Chat completions resource — the core API."""

    def __init__(self, client: "MeeDooClient"):
        self._client = client

    def create(
        self,
        model: str,
        messages: list[dict],
        *,
        stream: bool = False,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        min_p: Optional[float] = None,
        max_tokens: Optional[int] = None,
        max_completion_tokens: Optional[int] = None,
        frequency_penalty: Optional[float] = None,
        presence_penalty: Optional[float] = None,
        reasoning_effort: Optional[str] = None,
        seed: Optional[Any] = None,
        stop: Optional[list[str]] = None,
        logit_bias: Optional[dict] = None,
        response_format: Optional[dict] = None,
        n: Optional[int] = None,
        think: Optional[bool] = None,
        features: Optional[dict] = None,
        tool_ids: Optional[list[str]] = None,
        tool_servers: Optional[list] = None,
        tools: Optional[list] = None,
        tool_choice: Optional[str] = None,
        function_calling: Optional[str] = None,
        stream_response: Optional[bool] = None,
        stream_delta_chunk_size: Optional[int] = None,
        reasoning_tags: Optional[list] = None,
        system: Optional[str] = None,
        custom_params: Optional[dict] = None,
        chat_id: Optional[str] = None,
        message_id: Optional[str] = None,
        parent_id: Optional[str] = None,
        parent_message: Optional[dict] = None,
        session_id: Optional[str] = None,
        files: Optional[list] = None,
        skill_ids: Optional[list] = None,
        variables: Optional[dict] = None,
        filter_ids: Optional[list] = None,
        background_tasks: Optional[dict] = None,
        use_credits: Optional[bool] = None,
        metadata: Optional[dict] = None,
    ) -> ChatCompletion | Generator[ChatCompletionChunk, None, None]:
        """
        Create a chat completion.

        Args:
            model: Model ID (e.g. "meedoo:latest")
            messages: List of message dicts [{"role": "user", "content": "..."}]
            stream: If True, returns a generator yielding ChatCompletionChunk
            temperature: 0.0-2.0, controls randomness
            top_p: 0.0-1.0, nucleus sampling
            min_p: 0.0-1.0, minimum token probability
            max_tokens: Maximum output tokens
            max_completion_tokens: For reasoning models
            frequency_penalty: -2.0 to 2.0
            presence_penalty: -2.0 to 2.0
            reasoning_effort: "low", "medium", "high"
            seed: Random seed for reproducibility
            stop: Stop sequences
            logit_bias: Token bias mapping
            response_format: JSON mode {"type": "json_object"} or schema
            n: Number of completions
            think: Think mode for step-by-step reasoning
            features: {"web_search": True, "memory": True, "code_interpreter": True, ...}
            tool_ids: Tool function IDs to invoke
            tool_servers: Direct tool server connections
            tools: Native function-calling tool specs (standard API format)
            tool_choice: "auto", "none", or specific tool
            function_calling: "native" or "default"
            stream_response: Force streaming on/off
            stream_delta_chunk_size: Streaming chunk size
            reasoning_tags: Custom reasoning tag pairs
            system: Custom system prompt
            custom_params: Custom LLM parameters
            chat_id: Chat session ID
            message_id: Message ID for this response
            parent_id: Parent message ID
            parent_message: Parent message dict
            session_id: Socket session ID
            files: File attachments
            skill_ids: Skill IDs
            variables: Template variables for system prompt
            filter_ids: Filter function IDs
            background_tasks: {"title_generation": True, "follow_up_generation": True, ...}
            use_credits: Use API credits instead of session quota
            metadata: Additional metadata

        Returns:
            ChatCompletion if stream=False, Generator[ChatCompletionChunk] if stream=True

        Raises:
            AuthenticationError: Invalid API key
            InsufficientCreditsError: Not enough credits
            ModelNotFoundError: Model not found
            APIError: Other API errors
        """
        payload: dict = {"model": model, "messages": messages}

        if stream is not None:
            payload["stream"] = stream
        if temperature is not None:
            payload["temperature"] = temperature
        if top_p is not None:
            payload["top_p"] = top_p
        if min_p is not None:
            payload["min_p"] = min_p
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        if max_completion_tokens is not None:
            payload["max_completion_tokens"] = max_completion_tokens
        if frequency_penalty is not None:
            payload["frequency_penalty"] = frequency_penalty
        if presence_penalty is not None:
            payload["presence_penalty"] = presence_penalty
        if reasoning_effort is not None:
            payload["reasoning_effort"] = reasoning_effort
        if seed is not None:
            payload["seed"] = seed
        if stop is not None:
            payload["stop"] = stop
        if logit_bias is not None:
            payload["logit_bias"] = logit_bias
        if response_format is not None:
            payload["response_format"] = response_format
        if n is not None:
            payload["n"] = n
        if think is not None:
            payload["think"] = think
        if features is not None:
            payload["features"] = features
        if tool_ids is not None:
            payload["tool_ids"] = tool_ids
        if tool_servers is not None:
            payload["tool_servers"] = tool_servers
        if tools is not None:
            payload["tools"] = tools
        if tool_choice is not None:
            payload["tool_choice"] = tool_choice
        if function_calling is not None or stream_response is not None or stream_delta_chunk_size is not None or reasoning_tags is not None or system is not None or custom_params is not None:
            params: dict = {}
            if function_calling is not None:
                params["function_calling"] = function_calling
            if stream_response is not None:
                params["stream_response"] = stream_response
            if stream_delta_chunk_size is not None:
                params["stream_delta_chunk_size"] = stream_delta_chunk_size
            if reasoning_tags is not None:
                params["reasoning_tags"] = reasoning_tags
            if system is not None:
                params["system"] = system
            if custom_params is not None:
                params["custom_params"] = custom_params
            payload["params"] = params
        if chat_id is not None:
            payload["chat_id"] = chat_id
        if message_id is not None:
            payload["id"] = message_id
        if parent_id is not None:
            payload["parent_id"] = parent_id
        if parent_message is not None:
            payload["parent_message"] = parent_message
        if session_id is not None:
            payload["session_id"] = session_id
        if files is not None:
            payload["files"] = files
        if skill_ids is not None:
            payload["skill_ids"] = skill_ids
        if variables is not None:
            payload["variables"] = variables
        if filter_ids is not None:
            payload["filter_ids"] = filter_ids
        if background_tasks is not None:
            payload["background_tasks"] = background_tasks
        if use_credits is not None:
            payload["use_credits"] = use_credits
        if metadata is not None:
            payload["metadata"] = metadata

        if stream:
            return self._stream(payload)
        else:
            resp = self._client._post("/chat/completions", payload)
            return ChatCompletion.from_dict(resp)

    def _stream(self, payload: dict) -> Generator[ChatCompletionChunk, None, None]:
        payload["stream"] = True
        url = f"{self._client.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self._client.api_key}",
            "Content-Type": "application/json",
        }
        with requests.post(url, json=payload, headers=headers, stream=True, timeout=self._client.timeout) as resp:
            if resp.status_code == 401:
                raise AuthenticationError("Invalid API key", 401)
            if resp.status_code == 429:
                raise RateLimitError("Rate limit exceeded", 429)
            if resp.status_code >= 400:
                try:
                    body = resp.json()
                except Exception:
                    body = {"detail": resp.text}
                raise APIError(f"API error: {body.get('detail', resp.status_code)}", resp.status_code, body)

            for line in resp.iter_lines():
                if not line:
                    continue
                line_str = line.decode("utf-8") if isinstance(line, bytes) else line
                if line_str.startswith("data: "):
                    data_str = line_str[6:]
                    if data_str.strip() == "[DONE]":
                        break
                    try:
                        chunk_data = json.loads(data_str)
                        yield ChatCompletionChunk.from_dict(chunk_data)
                    except json.JSONDecodeError:
                        continue


class Models:
    """Models resource."""

    def __init__(self, client: "MeeDooClient"):
        self._client = client

    def list(self) -> ModelList:
        resp = self._client._get("/models")
        return ModelList.from_dict(resp)


class Usage:
    """Usage and credits resource."""

    def __init__(self, client: "MeeDooClient"):
        self._client = client

    def credits(self) -> CreditsResponse:
        resp = self._client._get("/v1/usage/credits")
        return CreditsResponse.from_dict(resp)

    def stats(self) -> UsageResponse:
        resp = self._client._get("/v1/usage/stats")
        return UsageResponse.from_dict(resp)


class MeeDooClient:
    """
    Main client for the MeeDoo AI API.

    Args:
        api_key: Your MeeDoo API key (starts with "md-")
        base_url: API base URL (default: https://api.meedoo.co/api)
        timeout: Request timeout in seconds (default: 120)
        max_retries: Max retries on 5xx errors (default: 3)
        retry_delay: Initial retry delay in seconds (default: 1.0)

    Example:
        client = MeeDooClient(api_key="md-xxxx")
        response = client.chat.completions.create(
            model="meedoo:latest",
            messages=[{"role": "user", "content": "Hello!"}],
        )
        print(response.content)
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.meedoo.co/api",
        timeout: int = 120,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ):
        if not api_key:
            raise ValueError("api_key is required")
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        self.chat = _Chat(self)
        self.models = Models(self)
        self.usage = Usage(self)

    def _get_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _get(self, path: str) -> dict:
        url = f"{self.base_url}{path}"
        for attempt in range(self.max_retries + 1):
            try:
                resp = requests.get(url, headers=self._get_headers(), timeout=self.timeout)
                return self._handle_response(resp)
            except requests.exceptions.ConnectionError:
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay * (2 ** attempt))
                else:
                    raise APIError(f"Connection failed after {self.max_retries} retries")

    def _post(self, path: str, payload: dict) -> dict:
        url = f"{self.base_url}{path}"
        for attempt in range(self.max_retries + 1):
            try:
                resp = requests.post(url, json=payload, headers=self._get_headers(), timeout=self.timeout)
                return self._handle_response(resp)
            except requests.exceptions.ConnectionError:
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay * (2 ** attempt))
                else:
                    raise APIError(f"Connection failed after {self.max_retries} retries")

    @staticmethod
    def _handle_response(resp: requests.Response) -> dict:
        if resp.status_code == 200:
            return resp.json()
        if resp.status_code == 401:
            raise AuthenticationError("Invalid API key", 401)
        if resp.status_code == 429:
            raise RateLimitError("Rate limit exceeded", 429)
        if resp.status_code >= 500:
            raise APIError(f"Server error: {resp.status_code}", resp.status_code)
        try:
            body = resp.json()
        except Exception:
            body = {"detail": resp.text}
        detail = body.get("detail", "")
        if "Insufficient API credits" in str(detail):
            raise InsufficientCreditsError(str(detail), 400, body)
        if "Model not found" in str(detail):
            raise ModelNotFoundError(str(detail), 404, body)
        raise APIError(str(detail) or f"HTTP {resp.status_code}", resp.status_code, body)

    def config(self) -> ConfigResponse:
        resp = requests.get(f"{self.base_url}/config", timeout=self.timeout)
        return ConfigResponse.from_dict(resp.json())

    def health(self) -> HealthResponse:
        resp = requests.get(f"{self.base_url.rstrip('/api')}/health", timeout=self.timeout)
        return HealthResponse.from_dict(resp.json())


class _Chat:
    """Namespace wrapper for chat.completions"""
    def __init__(self, client: MeeDooClient):
        self.completions = ChatCompletions(client)