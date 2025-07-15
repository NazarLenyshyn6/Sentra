"""
This module defines asynchronous introspection tool for AI agents to discover all registered pipelines in the Prompt Engine.

Agents use this tool when they need to plan prompt composition based on user intent. It returns a summary of all available
ML pipelines (i.e., complete workflows) along with clear descriptions. This enables the agent to:

- Identify which pipeline(s) best match the user’s question.
- Combine pipelines if necessary.
- Reject questions if no relevant pipeline is applicable.

This tool is essential for reasoning and planning before composing dynamic prompts using the Prompt Engine.
"""


from aiq.builder.function_info import FunctionInfo
from aiq.data_models.function import FunctionBaseConfig
from aiq.cli.register_workflow import register_function
from aiq.builder.builder import Builder
from prompt_engine.src.registry.orchestrator import Orchestrator


class GetAvailablePipelinesToolConfig(FunctionBaseConfig, name="get_available_pipelines"):
    """
    Configuration schema for the `get_available_pipelines` tool.

    Inherits:
        FunctionBaseConfig: Base class for AIQ function tool configuration.
    """
    ...


@register_function(config_type=GetAvailablePipelinesToolConfig)
async def get_available_pipelines(
        config: GetAvailablePipelinesToolConfig, builder: Builder
):
    async def _arun(question: str) -> str:
        pipelines_summary = Orchestrator.get_pipelines_usage_summary()
        instructions = (
            "Here is the list of all registered pipelines in the Prompt Engine.\n\n"
            "Instructions:\n"
            "- Select the pipeline(s) that are most relevant to the user's question.\n"
            "- If no single pipeline fully matches, consider combining multiple pipelines.\n"
            "- If none are applicable, respond that the question is outside your scope and only supported pipelines can be handled."
        )
        return f"{pipelines_summary}\n\n{instructions}"
    try:
        yield FunctionInfo.from_fn(_arun,
                                    description=(
                                        "Use this tool to retrieve all available ML pipelines in the Prompt Engine. "
                                        "It helps you understand what pipelines exist so you can select the most appropriate ones "
                                        "based on the user’s question. This tool is essential at the beginning of prompt planning."
                                        )
                                    )
    except GeneratorExit:
        print("The get_available_pipelines tool was exited before completion.")