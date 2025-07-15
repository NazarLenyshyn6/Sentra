""" This module registers available pipelines into the central Orchestrator. """

from prompt_engine.src.core.orchestrator import Orchestrator
from prompt_engine.src.registry.pipelines.eda import EdaPipeline


Orchestrator.add_pipelines(
    pipelines=[
        EdaPipeline
    ]
)