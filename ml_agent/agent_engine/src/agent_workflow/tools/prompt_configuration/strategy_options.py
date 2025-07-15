"""
This module defines an asynchronous tool for AI agents to introspect the available strategies
within selected stages of a pipeline.

Agents must call this tool *after selecting the most relevant stages*. It returns all available
fine-grained logic units (strategies) within those stages, allowing the agent to choose the exact
building blocks needed to construct the final dynamic prompt.
"""


from typing import List

from aiq.builder.function_info import FunctionInfo
from aiq.data_models.function import FunctionBaseConfig
from aiq.cli.register_workflow import register_function
from aiq.builder.builder import Builder
from prompt_engine.src.registry.orchestrator import Orchestrator


class GetAvailableStrategiesToolConfig(FunctionBaseConfig, name="get_available_strategies"):
    """
    Configuration schema for the `get_available_strategies` tool.

    Inherits:
        FunctionBaseConfig: Base class for AIQ function tool configuration.
    """
    ...


@register_function(config_type=GetAvailableStrategiesToolConfig)
async def get_available_strategies(
        config: GetAvailableStrategiesToolConfig, builder: Builder
):
    async def _arun(stages_id: List[str]) -> str:
        pipelines_summary = Orchestrator.get_stages_strategies_summary(stages_id)
        instructions = (
            "These are the strategies defined within the selected stages.\n\n"
            "Instructions:\n"
            "- Review each strategy and its description carefully.\n"
            "- Select only the strategies directly relevant to solving the user’s question.\n"
            "- Follow the original stage order when arranging selected strategies.\n"
            "- If a stage contains multiple strategies, combine only those strictly necessary.\n"
            "- The selected strategies will later be passed to the prompt composer in exact sequence."
            "- If none of the strategies are applicable, respond that the question is outside your scope "
            "and only supported pipelines, stages, and strategies can be handled.\n"
        )
        return f"{pipelines_summary}\n\n{instructions}"
    try:
        yield FunctionInfo.from_fn(_arun,
                                    description=(
                                        "Use this tool after selecting the stages for the current task. "
                                        "It retrieves all strategy components defined within those stages.\n\n"
                                        "- Input: a Python `List[str]` of stage IDs (in logical order).\n"
                                        "- Output: summaries of available strategies tied to those stages.\n"
                                        "- This step is required before using the prompt composer tool, as strategies define "
                                        "the concrete logic units used to dynamically answer the user's question.\n\n"
                                        "**Important:** Only call this tool *after* selecting the most relevant stages for the task."
                                        )
                                    )
    except GeneratorExit:
        print("The get_available_stages tool was exited before completion.")