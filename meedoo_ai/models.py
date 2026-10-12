"""Data models for the MeeDoo AI SDK."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class Usage:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    total_duration_ms: int = 0
    prompt_eval_duration_ms: int = 0
    completion_duration_ms: int = 0
    load_duration_ms: int = 0
    tokens_per_second: float = 0.0
    prompt_tokens_per_second: float = 0.0
    total_tokens_per_second: float = 0.0
    reasoning_tokens: int = 0

    @classmethod
    def from_dict(cls, d: dict) -> "Usage":
        details = d.get("completion_tokens_details", {})
        return cls(
            prompt_tokens=d.get("prompt_tokens", 0),
            completion_tokens=d.get("completion_tokens", 0),
            total_tokens=d.get("total_tokens", 0),
            input_tokens=d.get("input_tokens", 0),
            output_tokens=d.get("output_tokens", 0),
            total_duration_ms=d.get("total_duration_ms", 0),
            prompt_eval_duration_ms=d.get("prompt_eval_duration_ms", 0),
            completion_duration_ms=d.get("completion_duration_ms", 0),
            load_duration_ms=d.get("load_duration_ms", 0),
            tokens_per_second=d.get("tokens_per_second", 0),
            prompt_tokens_per_second=d.get("prompt_tokens_per_second", 0),
            total_tokens_per_second=d.get("total_tokens_per_second", 0),
            reasoning_tokens=details.get("reasoning_tokens", 0),
        )


@dataclass
class Message:
    role: str
    content: str = ""
    tool_calls: list = field(default_factory=list)
    tool_call_id: Optional[str] = None

    @classmethod
    def from_dict(cls, d: dict) -> "Message":
        return cls(
            role=d.get("role", "user"),
            content=d.get("content", ""),
            tool_calls=d.get("tool_calls", []),
            tool_call_id=d.get("tool_call_id"),
        )

    def to_dict(self) -> dict:
        d = {"role": self.role, "content": self.content}
        if self.tool_calls:
            d["tool_calls"] = self.tool_calls
        if self.tool_call_id:
            d["tool_call_id"] = self.tool_call_id
        return d


@dataclass
class Choice:
    index: int = 0
    finish_reason: Optional[str] = None
    message: Optional[Message] = None
    delta: Optional[dict] = None

    @classmethod
    def from_dict(cls, d: dict) -> "Choice":
        msg = d.get("message")
        return cls(
            index=d.get("index", 0),
            finish_reason=d.get("finish_reason"),
            message=Message.from_dict(msg) if msg else None,
            delta=d.get("delta"),
        )


@dataclass
class ToolCall:
    id: str = ""
    type: str = "function"
    function: dict = field(default_factory=dict)


@dataclass
class ChatCompletion:
    id: str = ""
    model: str = ""
    object: str = "chat.completion"
    created: int = 0
    choices: list[Choice] = field(default_factory=list)
    usage: Optional[Usage] = None
    sources: Optional[list] = None
    judge: Optional[dict] = None

    @classmethod
    def from_dict(cls, d: dict) -> "ChatCompletion":
        return cls(
            id=d.get("id", ""),
            model=d.get("model", ""),
            object=d.get("object", "chat.completion"),
            created=d.get("created", 0),
            choices=[Choice.from_dict(c) for c in d.get("choices", [])],
            usage=Usage.from_dict(d["usage"]) if d.get("usage") else None,
            sources=d.get("sources"),
            judge=d.get("judge"),
        )

    @property
    def content(self) -> str:
        if self.choices and self.choices[0].message:
            return self.choices[0].message.content
        return ""

    @property
    def tool_calls(self) -> list:
        if self.choices and self.choices[0].message:
            return self.choices[0].message.tool_calls
        return []


@dataclass
class ChatCompletionChunk:
    id: str = ""
    model: str = ""
    object: str = "chat.completion.chunk"
    created: int = 0
    choices: list[Choice] = field(default_factory=list)
    usage: Optional[Usage] = None
    sources: Optional[list] = None

    @classmethod
    def from_dict(cls, d: dict) -> "ChatCompletionChunk":
        return cls(
            id=d.get("id", ""),
            model=d.get("model", ""),
            object=d.get("object", "chat.completion.chunk"),
            created=d.get("created", 0),
            choices=[Choice.from_dict(c) for c in d.get("choices", [])],
            usage=Usage.from_dict(d["usage"]) if d.get("usage") else None,
            sources=d.get("sources"),
        )

    @property
    def delta_content(self) -> str:
        if self.choices and self.choices[0].delta:
            return self.choices[0].delta.get("content", "")
        return ""

    @property
    def delta_tool_calls(self) -> list:
        if self.choices and self.choices[0].delta:
            return self.choices[0].delta.get("tool_calls", [])
        return []

    @property
    def is_done(self) -> bool:
        return any(c.finish_reason == "stop" for c in self.choices)


@dataclass
class Model:
    id: str = ""
    name: str = ""
    object: str = "model"
    created: int = 0
    owned_by: str = ""
    connection_type: str = ""
    info: dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: dict) -> "Model":
        return cls(
            id=d.get("id", ""),
            name=d.get("name", ""),
            object=d.get("object", "model"),
            created=d.get("created", 0),
            owned_by=d.get("owned_by", ""),
            connection_type=d.get("connection_type", ""),
            info=d.get("info", {}),
        )


@dataclass
class ModelList:
    data: list[Model] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> "ModelList":
        return cls(data=[Model.from_dict(m) for m in d.get("data", [])])


@dataclass
class CreditsResponse:
    credit_balance: float = 0.0
    token_balance: int = 0

    @classmethod
    def from_dict(cls, d: dict) -> "CreditsResponse":
        return cls(
            credit_balance=d.get("credit_balance", 0.0),
            token_balance=d.get("token_balance", 0),
        )


@dataclass
class UsageResponse:
    current_requests: int = 0
    max_requests: int = 0
    remaining: int = 0
    plan: str = ""
    quota_reset_at: Optional[str] = None
    chat_session: dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: dict) -> "UsageResponse":
        return cls(
            current_requests=d.get("current_requests", 0),
            max_requests=d.get("max_requests", 0),
            remaining=d.get("remaining", 0),
            plan=d.get("plan", ""),
            quota_reset_at=d.get("quota_reset_at"),
            chat_session=d.get("chat_session", {}),
        )


@dataclass
class ConfigResponse:
    status: bool = True
    name: str = ""
    version: str = ""
    features: dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: dict) -> "ConfigResponse":
        return cls(
            status=d.get("status", True),
            name=d.get("name", ""),
            version=d.get("version", ""),
            features=d.get("features", {}),
        )


@dataclass
class HealthResponse:
    status: bool = True

    @classmethod
    def from_dict(cls, d: dict) -> "HealthResponse":
        return cls(status=d.get("status", True))


@dataclass
class JudgeStatus:
    enabled: bool = False
    healthy: bool = False
    url: str = ""
    model: str = ""

    @classmethod
    def from_dict(cls, d: dict) -> "JudgeStatus":
        return cls(
            enabled=d.get("enabled", False),
            healthy=d.get("healthy", False),
            url=d.get("url", ""),
            model=d.get("model", ""),
        )


@dataclass
class JudgeResult:
    result: dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: dict) -> "JudgeResult":
        return cls(result=d)