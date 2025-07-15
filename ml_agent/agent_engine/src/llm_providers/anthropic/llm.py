"""
This module defines configuration and registration logic for using Anthropic-hosted
language models (e.g., Claude) within the AIQ workflow framework. It supports:
- Provider registration for Anthropic.
- LangChain-compatible client registration.
- Secure usage of API keys via config or environment variables.
"""

from pydantic import Field, ConfigDict
from aiq.builder.builder import Builder
from aiq.data_models.llm import LLMBaseConfig
from aiq.builder.llm import LLMProviderInfo
from aiq.cli.register_workflow import register_llm_provider, register_llm_client
from aiq.builder.framework_enum import LLMFrameworkEnum


class AnthropicModelConfig(LLMBaseConfig, name="anthropic"):
    """
    Configuration class for Anthropic LLM provider.

    Attributes:
        anthropic_api_key: API key used to authenticate with Anthropic.
        model: Name of the Anthropic-hosted model to use (e.g., "claude-3").
        temperature: Sampling temperature for model output generation. Range: [0.0, 1.0].
        max_tokens: Maximum number of tokens to generate in the response.
    """

    model_config = ConfigDict(protected_namespaces=())

    anthropic_api_key: str | None = Field(
        default=None,
        description="Anthropic API key to interact with hosted model."
    )
    model: str | None = Field(
        default=None,
        description="The Anthropic hosted model name."
    )
    temperature: float = Field(
        default=0.0,
        description="Sampling temperature in [0, 1]."
    )
    max_tokens: int = Field(
        default=3000,
        description="The max number of tokens for the request."
    )


@register_llm_provider(config_type=AnthropicModelConfig)
async def anthropic_llm(config: AnthropicModelConfig, builder: Builder):
    """
    Registers Anthropic as a supported LLM provider.

    Args:
        config: Configuration for the Anthropic provider.
        builder: Builder object used for workflow construction.

    Yields:
        LLMProviderInfo: Metadata describing this LLM provider.
    """
    yield LLMProviderInfo(
        config=config,
        description="An Anthropic model for use with an LLM client."
    )


@register_llm_client(config_type=AnthropicModelConfig, wrapper_type=LLMFrameworkEnum.LANGCHAIN)
async def anthropic_langchain(config: AnthropicModelConfig, builder: Builder):
    """
    Registers a LangChain-compatible client for the Anthropic model.

    Args:
        config: Configuration for the Anthropic client.
        builder: Builder object used to construct workflows.

    Yields:
        ChatAnthropic: A LangChain-compatible wrapper around the Anthropic model.
    """
    from langchain_anthropic import ChatAnthropic
    import os

    # Fallback to environment variable if API key is not provided explicitly
    config.anthropic_api_key = config.anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")

    yield ChatAnthropic(
        **config.model_dump(
            exclude={"type"},
            by_alias=True
        )
    )
