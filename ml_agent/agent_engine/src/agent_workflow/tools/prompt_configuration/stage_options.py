"""
This module defines an asynchronous tool for AI agents to introspect the available stages
within selected pipelines in the Prompt Engine.

Agents must call this tool *after selecting the most relevant pipelines* in order to:
- Understand the logical structure of those pipelines.
- Determine which stages are needed to solve the user’s question.
- Prepare for selecting strategies within those stages.
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
            "These are the stages defined in the selected pipelines.\n\n"
            "Instructions:\n"
            "- Carefully review the stages and their descriptions.\n"
            "- Select only the stages relevant to the current user question.\n"
            "- Preserve the original stage order as defined in each pipeline.\n"
            "- If using multiple pipelines, you may combine compatible stages across them.\n"
            "- This step prepares the reasoning path for selecting appropriate strategies."
            "- If none of the stages are applicable to the task, respond that the question is outside your scope "
            "and only supported pipelines and their stages can be handled."
        )
        return f"{pipelines_summary}\n\n{instructions}"
    try:
        yield FunctionInfo.from_fn(_arun,
                                    description=(
                                        "Use this tool after selecting relevant pipelines. "
                                        "It retrieves all stages within those pipelines and provides structured guidance for choosing the right ones.\n\n"
                                        "- Input: a Python `List[str]` of pipeline IDs (in order).\n"
                                        "- Output: summaries of available stages from the selected pipelines.\n"
                                        "- This step is required before selecting strategies, as it defines the intermediate logic blocks needed "
                                        "to construct the final prompt.\n\n"
                                        "**Important:** Only use this tool once pipelines are selected. The output will guide stage selection."
                                        )
                                    )
    except GeneratorExit:
        print("The get_available_stages tool was exited before completion.")