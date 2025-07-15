"""
This module defines the final and most critical tool in the dynamic prompt-building process: 
the prompt composer. It takes a strictly ordered list of strategies and generates the final 
dynamic prompt that will be used to answer the user’s question.
"""


from typing import List

from aiq.builder.function_info import FunctionInfo
from aiq.data_models.function import FunctionBaseConfig
from aiq.cli.register_workflow import register_function
from aiq.builder.builder import Builder
from prompt_engine.src.registry.orchestrator import Orchestrator


class PromptComposerToolConfig(FunctionBaseConfig, name="compose_prompt"):
    """
    Configuration schema for the `compose_prompt` tool.

    Inherits:
        FunctionBaseConfig: Base class for AIQ function tool configuration.
    """
    ...


@register_function(config_type=PromptComposerToolConfig)
async def compose_prompt(
        config: PromptComposerToolConfig, builder: Builder
):
    async def _arun(strategies_id: List[str]) -> str:
        composed_prompt = Orchestrator.compose_prompt(strategies_id)
        return composed_prompt

    try:
        yield FunctionInfo.from_fn(
            _arun,
            description=(
                "Use this tool to compose the final dynamic prompt after selecting all relevant strategies.\n\n"
                "- Input: a Python `List[str]` of strategy IDs, in the **exact logical order** required.\n"
                "- This tool must be called only **after all planning and strategy selection is complete**.\n"
                "- The **order of strategies is critical**. Any misordering will result in a broken or invalid prompt.\n\n"
                "The composed prompt is the final output of the planning process and will be used to answer the user’s question. "
                "It integrates all selected components and determines the behavior of the resulting prompt."
            )
        )
    except GeneratorExit:
        print("The compose_prompt tool was exited before completion.")