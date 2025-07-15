"""
This module defines an asynchronous tool for AI agents to introspect the available stages 
within selected pipelines. Agents can call this tool after identifying the most relevant 
pipelines, in order to determine which stages are appropriate for answering the user's question.
"""

from typing import List

from aiq.builder.function_info import FunctionInfo
from aiq.data_models.function import FunctionBaseConfig
from aiq.cli.register_workflow import register_function
from aiq.builder.builder import Builder
from prompt_engine.src.registry.orchestrator import Orchestrator

class GetAvailableStagesToolConfig(FunctionBaseConfig, name="get_available_stages"):
    """
    Configuration schema for the `get_available_stages` tool.

    This defines the config interface for stage introspection within selected pipelines, 
    enabling dynamic analysis planning.

    Inherits:
        FunctionBaseConfig: Base class for AIQ function tool configuration.
    """
    ...

@register_function(config_type=GetAvailableStagesToolConfig)
async def get_available_stages(
        config: GetAvailableStagesToolConfig, builder: Builder
):
    async def _arun(pipelines_id: List[str]) -> str:
        pipelines_summary = Orchestrator.get_pipelines_stages_summary(pipelines_id)
        instructions = (
            "These are the stages defined in the selected pipelines. You must:\n\n"
            "- Carefully review the listed stages and their descriptions.\n"
            "- Select only the stages that are relevant to the current user question.\n"
            "- Maintain the original order of stages as defined in the pipelines.\n"
            "- If multiple pipelines were selected, you may combine compatible stages across them.\n"
            "- This step is essential to narrow down the exact logic blocks (strategies) for the final prompt.\n\n"
        )
        return f"{pipelines_summary}\n\n{instructions}"
    try:
        yield FunctionInfo.from_fn(_arun,
                                    description=(
                                        "Use this tool after selecting the pipelines you want to work with. "
                                        "It returns all the stages defined within the specified pipelines, along with descriptions. "
                                        "Use it to decide which stages are best suited to the current user task. "
                                        "This is a required step before selecting strategies, as it helps you break down the "
                                        "workflow into meaningful phases aligned with the question."
                                        "**Important:** Only call this tool *after* you've selected the most relevant pipelines "
                                        "for the user’s task. The input must be a Python list of pipeline IDs in the correct order."
                                        )
                                    )
    except GeneratorExit:
        print("The get_available_stages tool was exited before completion.")