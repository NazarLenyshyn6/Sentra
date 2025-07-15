""" This module registers available pipelines into the central Orchestrator. """

from prompt_engine.core.orchestrator import Orchestrator
from prompt_engine.registry.pipelines.eda import EdaPipeline


Orchestrator.add_pipelines(
    pipelines=[
        EdaPipeline
    ]
)