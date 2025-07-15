"""
This module defines an asynchronous tool for AI agents to introspect the available strategies 
within selected stages. Agents should call this tool after identifying the most relevant stages 
in order to determine which fine-grained logic units (strategies) should be used to construct 
the final prompt.
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

    This defines the config interface for strategy-level introspection, enabling the AI agent 
    to view all available strategy components within selected stages.

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
            "These are the strategies defined within the selected stages. You must:\n\n"
            "- Carefully examine each listed strategy and its purpose.\n"
            "- Select only the strategies that are directly relevant to the current user question.\n"
            "- Maintain the original stage order when choosing strategies.\n"
            "- If a stage contains multiple strategies, combine only those that are necessary.\n"
            "- The selected strategies will be composed in sequence to create the final dynamic prompt.\n\n"
        )
        return f"{pipelines_summary}\n\n{instructions}"
    try:
        yield FunctionInfo.from_fn(_arun,
                                    description=(
                                        "Use this tool after selecting the stages you want to work with. "
                                        "It returns all available strategies within the given stages, each with descriptions. "
                                        "Use this tool to identify the most suitable strategy components for the user's question. "
                                        "This is a required step before composing the final prompt, as strategies define the atomic "
                                        "logic blocks you will combine to create a fully customized solution."
                                        "**Important:** Only call this tool *after* you've selected the most relevant stages "
                                        "to solve the user's task. The input must be a Python list of stage IDs in the correct order."
                                        )
                                    )
    except GeneratorExit:
        print("The get_available_stages tool was exited before completion.")