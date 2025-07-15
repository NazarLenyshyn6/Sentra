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

    This defines the config interface for the prompt composition stage — the final and 
    most important tool for building a fully dynamic prompt from selected strategy components.

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
                "Use this tool to generate the final composed prompt once you have selected all the necessary strategies. "
                "This is the last and most critical step in the dynamic prompt-building process.\n\n"
                
                "The input must be a Python `List[str]` containing the **IDs of all selected strategies**, arranged in the "
                "**exact order** required to solve the user's question.\n\n"
                
                " This tool must **only be used after** all appropriate strategies have been chosen. Do not call it earlier.\n\n"
                
                " The **order of the strategy IDs matters greatly** — it must reflect the logical execution order. "
                "**Any misordering or omission will break the workflow**, resulting in an invalid or misleading prompt.\n\n"
                
                " This step finalizes your entire reasoning and selection process. The resulting prompt is what the assistant will use "
                "to generate its response. It ties together all logic blocks and defines how the task will be handled.\n\n"
            )
        )
    except GeneratorExit:
        print("The compose_prompt tool was exited before completion.")