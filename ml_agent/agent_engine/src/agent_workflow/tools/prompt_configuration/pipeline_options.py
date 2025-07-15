""" 
This module defines an asynchronous tool for AI agents to introspect the Prompt Engine's 
registered pipelines. Agents can call this tool when they need to understand what ML 
workflows are available in the system.
"""


from aiq.builder.function_info import FunctionInfo
from aiq.data_models.function import FunctionBaseConfig
from aiq.cli.register_workflow import register_function
from aiq.builder.builder import Builder
from prompt_engine.src.registry.orchestrator import Orchestrator

class GetAvailablePipelinesToolConfig(FunctionBaseConfig, name="get_available_pipelines"):
    """
    Configuration schema for the `get_available_pipelines` tool.

    This defines the config interface for the pipeline introspection tool, enabling it
    to be registered and used within the AIQ toolchain.

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
            "Here is the list of all available pipelines. You must:\n\n"
            "- Choose the most relevant pipeline(s) to the current user question.\n"
            "- If one pipeline is not enough, combine multiple pipelines to fully answer the question.\n"
            "- If the question is outside the scope of all pipelines, inform the user you cannot answer it "
            "and only support questions related to the available workflows."
        )
        return f"{pipelines_summary}\n\n{instructions}"
    try:
        yield FunctionInfo.from_fn(_arun,
                                    description=(
                                        "Use this tool when you need to know which pipelines are available."
                                        "This tool will return all registered pipelines along with explanations for each, "
                                        "so you can select the most suitable ones based on the current user's question. "
                                        "It's especially useful when planning how to approach a task or deciding which ML "
                                        "workflow to run in response to the user’s intent."
                                        )
                                    )
    except GeneratorExit:
        print("The get_available_pipelines tool was exited before completion.")