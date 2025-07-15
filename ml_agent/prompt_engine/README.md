# Prompt Engine

The **Prompt Engine** is a framework designed to solve the fundamental problem of static prompts in AI agents. Instead of relying on fixed, unchanging prompts, this system enables dynamic prompt configuration based on user questions and predefined prompt components. 

In the context of machine learning workflows, the Prompt Engine allows agents to adapt their prompts depending on the specific ML task the user wants to perform - whether it's data analysis, model training, feature engineering, or any other ML operation. This creates more specialized and context-aware agents through dynamic prompt composition, resulting in more accurate and relevant responses tailored to specific ML scenarios.

The framework provides a structured, hierarchical approach to prompt management through pipelines, stages, and strategies, enabling scalable and maintainable AI-powered automation systems.

## Core Architecture

The Prompt Engine follows a three-tier hierarchy:

```
Orchestrator
    ├── Pipelines (workflows)
    │   ├── Stages (processing phases)
    │   │   ├── Strategies (prompt-driven logic blocks)
```

### Key Components

#### 1. **Strategy** (`prompt_engine.core.strategy`)
The foundational unit of prompt-driven logic. Each strategy represents a specific prompt template or instruction set designed to accomplish a particular task.

**Key Features:**
- **Immutable Design**: Strategies are frozen dataclasses ensuring consistency
- **Unique Identification**: Each strategy has a unique ID (normalized to uppercase)
- **Prompt Container**: Encapsulates the actual prompt text/template
- **Self-Describing**: Includes description for documentation and discovery

**Usage:**
```python
from prompt_engine.core.strategy import Strategy

strategy = Strategy(
    id="data_validation",
    description="Validates input data format and completeness",
    prompt="Check the following data for missing values and format issues: {data}"
)
```

#### 2. **Stage** (`prompt_engine.core.stage`)
A logical grouping of related strategies that represent a distinct phase in a workflow. Stages serve as containers and orchestrators for multiple strategies.

**Key Features:**
- **Strategy Registry**: Manages a collection of strategies with add/remove operations
- **Prompt Retrieval**: Provides access to individual strategy prompts
- **Hierarchical Structure**: Inherits from `Registry[Strategy]` for consistent container behavior
- **Summary Generation**: Offers introspection capabilities for registered strategies

**Usage:**
```python
from prompt_engine.core.stage import Stage

stage = Stage(
    id="data_preprocessing",
    description="Handles data cleaning and preparation tasks"
)

# Register strategies
stage.add_strategies([validation_strategy, cleaning_strategy])

# Retrieve specific prompts
prompt = stage.get_prompt("data_validation")
```

#### 3. **Pipeline** (`prompt_engine.core.pipeline`)
A complete workflow composed of multiple stages executed in sequence. Pipelines represent end-to-end processes for specific domains or use cases.

**Key Features:**
- **Stage Orchestration**: Manages ordered sequences of stages
- **Workflow Definition**: Encapsulates complete business logic flows
- **Registry Pattern**: Inherits from `Registry[Stage]` for consistent management
- **Hierarchical Access**: Provides access to contained stages and their strategies

**Usage:**
```python
from prompt_engine.core.pipeline import Pipeline

pipeline = Pipeline(
    id="data_analysis",
    description="Complete data analysis workflow from ingestion to insights"
)

# Add stages in order
pipeline.add_stages([ingestion_stage, preprocessing_stage, analysis_stage])
```

#### 4. **Orchestrator** (`prompt_engine.core.orchestrator`)
The central coordinator that manages all pipelines, stages, and strategies across the system. It serves as the global registry and provides cross-cutting functionality.

**Key Features:**
- **Global Registry**: Maintains system-wide registries for all components
- **Hierarchical Registration**: Automatically registers stages and strategies when pipelines are added
- **Dynamic Composition**: Enables runtime prompt composition from selected strategies
- **System Introspection**: Provides comprehensive summaries and overviews
- **Cascade Management**: Handles automatic cleanup when components are removed

**Usage:**
```python
from prompt_engine.core.orchestrator import Orchestrator

# Register pipelines (automatically registers stages and strategies)
Orchestrator.add_pipelines([data_pipeline, ml_pipeline])

# Compose prompts from specific strategies
composed_prompt = Orchestrator.get_composed_prompt([
    "data_validation",
    "feature_engineering",
    "model_training"
])

# Get system overview
summary = Orchestrator.get_pipelines_usage_summary()
```

#### 5. **Registry** (`prompt_engine.core.registry`)
A generic base class providing common container functionality for all registry-based components.

**Key Features:**
- **Generic Design**: Type-safe container for any registered item type
- **Consistent Interface**: Standard Python container protocol (len, iter, contains)
- **ID Normalization**: Automatic uppercase conversion for consistent lookup
- **Extensible Foundation**: Base for all registry-enabled components

## Extension and Customization

### Adding New Strategies
Create new strategies by instantiating the `Strategy` class with unique IDs and appropriate prompts:

```python
custom_strategy = Strategy(
    id="custom_analysis",
    description="Performs domain-specific analysis",
    prompt="Analyze the following data using domain expertise: {input}"
)
```

### Building Custom Stages
Extend functionality by creating stages that group related strategies:

```python
custom_stage = Stage(
    id="custom_processing",
    description="Handles specialized processing requirements"
)
custom_stage.add_strategies([strategy1, strategy2, strategy3])
```

### Creating New Pipelines
Design complete workflows by combining stages:

```python
custom_pipeline = Pipeline(
    id="custom_workflow",
    description="End-to-end custom business process"
)
custom_pipeline.add_stages([setup_stage, process_stage, finalize_stage])
```

### Registering with Orchestrator
Make components available system-wide:

```python
Orchestrator.add_pipelines([custom_pipeline])
```

## Usage Patterns

### Basic Prompt Composition
```python
# Register your pipelines
Orchestrator.add_pipelines([my_pipeline])

# Compose prompts from specific strategies
final_prompt = Orchestrator.get_composed_prompt([
    "strategy_1",
    "strategy_2",
    "strategy_3"
])
```

### System Introspection
```python
# Get overview of all pipelines
pipeline_summary = Orchestrator.get_pipelines_usage_summary()

# Get detailed stage information for specific pipelines
stage_details = Orchestrator.get_pipelines_stages_summary(["PIPELINE_1", "PIPELINE_2"])

# Get strategy details for specific stages
strategy_details = Orchestrator.get_stages_strategies_summary(["STAGE_1", "STAGE_2"])
```

### Dynamic Pipeline Management
```python
# Add new pipelines at runtime
Orchestrator.add_pipelines([new_pipeline])

# Remove pipelines and their components
Orchestrator.remove_pipelines([old_pipeline])

# Access complete system state
registry_state = Orchestrator.get_registry()
```

## Design Principles

### Modularity
Each component serves a specific purpose and can be developed, tested, and maintained independently.

### Hierarchical Organization
The three-tier structure (Pipeline → Stage → Strategy) provides clear separation of concerns and logical grouping.

### Extensibility
The registry pattern and generic base classes make it easy to add new components without modifying existing code.

### Immutability
Core components like strategies are immutable, ensuring system stability and predictable behavior.

### Type Safety
Comprehensive use of type hints and Pydantic validation ensures robust runtime behavior.

### Container Protocol
All registry components follow Python's container protocol, providing intuitive iteration and membership testing.

## Best Practices

1. **Unique IDs**: Ensure all component IDs are unique within their scope
2. **Descriptive Names**: Use clear, descriptive IDs and descriptions for better maintainability
3. **Logical Grouping**: Group related strategies into stages and related stages into pipelines
4. **Prompt Templates**: Design reusable prompt templates with clear parameter placeholders
5. **System Registration**: Register pipelines with the Orchestrator for system-wide access
6. **Error Handling**: Handle KeyErrors when accessing non-existent components
7. **Testing**: Test each component level independently before integration

## Error Handling

The system provides clear error messages for common issues:

- `KeyError`: When requesting non-existent components by ID
- `ValidationError`: When providing invalid input types to validated methods
- Component IDs are automatically normalized to uppercase for consistent lookup

## ML-Focused Design

This framework is specifically designed for dynamically configuring prompts related to machine learning problems. It provides a structured approach to organizing and composing ML-specific prompts, enabling systematic prompt management for various ML workflows and tasks.

## Extending for Other ML Tasks

The Prompt Engine architecture is designed to be easily extensible for any machine learning domain or task. To extend the framework for new ML areas:

### 1. **Define New Strategies**
Create domain-specific strategies by implementing new `Strategy` instances with prompts tailored to your ML task:

```python
new_ml_strategy = Strategy(
    id="custom_ml_task",
    description="Handles specific ML operation for your domain",
    prompt="Your specialized ML prompt template here"
)
```

### 2. **Organize into Stages**
Group related strategies into logical processing stages for your ML workflow:

```python
ml_stage = Stage(
    id="custom_ml_stage",
    description="Processing stage for your ML domain"
)
ml_stage.add_strategies([strategy1, strategy2, strategy3])
```

### 3. **Create Domain Pipelines**
Build complete ML workflows by combining stages in the appropriate order:

```python
domain_pipeline = Pipeline(
    id="custom_ml_pipeline",
    description="End-to-end workflow for your ML domain"
)
domain_pipeline.add_stages([preparation_stage, processing_stage, evaluation_stage])
```

### 4. **Register with System**
Make your new ML components available for dynamic prompt composition:

```python
Orchestrator.add_pipelines([domain_pipeline])
```

This modular approach allows you to extend the framework for any ML domain - from computer vision and NLP to time series analysis and reinforcement learning - while maintaining the same consistent interface and dynamic composition capabilities.

## Future Extensibility

The architecture is designed to support:
- Additional component types beyond the current three-tier structure
- Plugin-based extension mechanisms
- Advanced composition patterns and conditional logic
- Integration with external prompt libraries and templates
- Persistence and serialization capabilities
- Cross-domain ML task orchestration