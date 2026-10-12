"""
MeeDoo AI Python SDK
A complete SDK for the MeeDoo AI Chat Completions API.

Usage:
    from meedoo_ai import MeeDooClient

    client = MeeDooClient(api_key="md-xxxx")
    response = client.chat.completions.create(
        model="meedoo:latest",
        messages=[{"role": "user", "content": "Hello!"}],
        features={"web_search": True},
        think=True,
    )
    print(response.choices[0].message.content)
"""

from .client import MeeDooClient
from .models import (
    ChatCompletion,
    ChatCompletionChunk,
    Model,
    ModelList,
    UsageResponse,
    CreditsResponse,
    ConfigResponse,
    HealthResponse,
)
from .exceptions import (
    MeeDooError,
    AuthenticationError,
    RateLimitError,
    InsufficientCreditsError,
    ModelNotFoundError,
    APIError,
)

__version__ = "1.0.2"
__all__ = [
    "MeeDooClient",
    "ChatCompletion",
    "ChatCompletionChunk",
    "Model",
    "ModelList",
    "UsageResponse",
    "CreditsResponse",
    "ConfigResponse",
    "HealthResponse",
    "MeeDooError",
    "AuthenticationError",
    "RateLimitError",
    "InsufficientCreditsError",
    "ModelNotFoundError",
    "APIError",
]