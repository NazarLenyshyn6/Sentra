# Agent Engine

The **Agent Engine** is a specialized AI agent system built on top of the NVIDIA Agent IQ framework, designed to solve the fundamental challenge of dynamic prompt composition in machine learning workflows. Rather than relying on static, pre-written prompts, this system creates intelligent agents capable of dynamically selecting and composing optimal prompts based on user intent and available prompt components.

## Core Philosophy

The Agent Engine addresses a critical limitation in AI agent systems: the inability to adapt prompt strategies to different types of machine learning tasks. Traditional agents use fixed prompts that cannot adjust to the diverse requirements of data analysis, feature engineering, model training, evaluation, and other ML operations. This system introduces **dynamic prompt orchestration** - the ability to intelligently select and compose specialized prompt components in real-time based on the specific ML task at hand.

## Architecture Overview

The Agent Engine implements a **dual-framework architecture**:

### 1. NVIDIA Agent IQ Framework Integration
Provides the underlying infrastructure for:
- **Agent Workflow Management**: Handles agent lifecycle and execution
- **LLM Provider Integration**: Standardized interface for language models
- **Tool Registration System**: Plugin-based architecture for extending functionality
- **Configuration Management**: Unified configuration and validation system

### 2. Custom Prompt Engine Framework
Implements dynamic prompt composition through:
- **Hierarchical Prompt Organization**: Pipeline → Stage → Strategy structure
- **Dynamic Component Selection**: Runtime composition of prompt components
- **ML-Specific Abstractions**: Specialized for machine learning workflows
- **Intelligent Orchestration**: Automated prompt planning and composition

## Core Abstractions

### Agent Workflow System
The agent operates through a **reactive planning model** where it:
1. **Analyzes user intent** to understand the ML task requirements
2. **Discovers available components** in the prompt hierarchy
3. **Plans optimal composition** by selecting relevant pipelines, stages, and strategies
4. **Composes dynamic prompts** that are specifically tailored to the task
5. **Executes the workflow** using the dynamically generated prompt

### Dynamic Prompt Composition
The system employs a **three-tier hierarchical approach**:

#### Pipelines (Workflow Level)
- **Abstract Concept**: Complete end-to-end ML workflows
- **Purpose**: Represent high-level ML processes (e.g., exploratory data analysis, model training pipelines)
- **Behavior**: Contain ordered sequences of processing stages
- **Discovery**: Agents first identify relevant pipelines based on user questions

#### Stages (Process Level)
- **Abstract Concept**: Logical processing phases within workflows
- **Purpose**: Group related ML operations (e.g., data preprocessing, feature engineering, model evaluation)
- **Behavior**: Contain collections of specialized strategies
- **Selection**: Agents choose appropriate stages based on task requirements

#### Strategies (Execution Level)
- **Abstract Concept**: Atomic prompt-driven logic units
- **Purpose**: Implement specific ML operations or analyses
- **Behavior**: Contain specialized prompt templates for targeted tasks
- **Composition**: Agents select and order strategies to build final prompts

### Intelligent Planning Process
The agent follows a **sequential discovery and composition pattern**:

1. **Pipeline Discovery**: Identify ML workflows relevant to the user's question
2. **Stage Selection**: Choose appropriate processing phases from selected pipelines
3. **Strategy Composition**: Select specific prompt strategies in logical order
4. **Prompt Generation**: Compose final dynamic prompt from selected components

## System Components

### Agent Workflow Core (`agent_workflow/`)
- **Configuration Management**: YAML-based workflow configuration
- **Registration System**: Component discovery and initialization
- **Tool Orchestration**: Coordination of prompt composition tools

### Prompt Configuration Tools (`agent_workflow/tools/prompt_configuration/`)
The system implements four specialized tools that enable dynamic prompt composition:

#### Pipeline Options Tool
- **Abstract Function**: ML workflow discovery and selection
- **Purpose**: Enables agents to understand available ML pipelines
- **Behavior**: Returns structured summaries of all registered workflows
- **Integration**: First step in the composition planning process

#### Stage Options Tool
- **Abstract Function**: Process phase introspection and selection
- **Purpose**: Allows agents to explore logical stages within selected pipelines
- **Behavior**: Provides detailed stage descriptions and dependencies
- **Integration**: Second step in the composition planning process

#### Strategy Options Tool
- **Abstract Function**: Atomic component discovery and selection
- **Purpose**: Enables agents to access fine-grained prompt strategies
- **Behavior**: Returns available strategies within selected stages
- **Integration**: Third step in the composition planning process

#### Prompt Composer Tool
- **Abstract Function**: Dynamic prompt generation and assembly
- **Purpose**: Creates final prompts from selected strategy components
- **Behavior**: Composes ordered strategies into coherent prompt instructions
- **Integration**: Final step in the composition planning process

### LLM Provider System (`llm_providers/`)
- **Anthropic Integration**: Specialized configuration for Claude models
- **Framework Compatibility**: LangChain-compatible client registration
- **Security Management**: API key handling and authentication

## Key Design Principles

### Abstraction-Driven Development
The system is built around clear abstractions that separate concerns:
- **Workflow Management**: Handled by NVIDIA Agent IQ framework
- **Prompt Logic**: Managed by custom Prompt Engine framework
- **Component Integration**: Unified through tool registration system

### Hierarchical Composition
The three-tier hierarchy provides:
- **Scalability**: Easy addition of new ML workflows and components
- **Maintainability**: Clear separation of concerns and responsibilities
- **Flexibility**: Dynamic composition of prompt components

### Intelligent Orchestration
The agent operates through:
- **Context-Aware Planning**: Understanding user intent and task requirements
- **Component Discovery**: Systematic exploration of available prompt components
- **Dynamic Assembly**: Real-time composition of specialized prompts

### Framework Integration
The system leverages:
- **Plugin Architecture**: Extensible component registration system
- **Configuration Management**: Unified configuration and validation
- **Tool Integration**: Standardized function tool framework

## Workflow Execution Model

### Agent Initialization
1. **Component Registration**: All tools and LLM providers are registered with AIQ framework
2. **Prompt Engine Loading**: ML-specific pipelines, stages, and strategies are loaded
3. **Workflow Configuration**: Agent behavior is configured through YAML configuration

### Request Processing
1. **User Query Analysis**: Agent analyzes ML-related questions
2. **Component Discovery**: Sequential exploration of pipelines, stages, and strategies
3. **Composition Planning**: Intelligent selection of relevant prompt components
4. **Prompt Generation**: Dynamic assembly of final prompt instructions
5. **Response Generation**: Execution of composed prompt to answer user question

### Dynamic Adaptation
The system adapts to different ML tasks by:
- **Context Recognition**: Understanding the type of ML problem being addressed
- **Component Selection**: Choosing appropriate prompt components for the task
- **Logical Ordering**: Arranging strategies in optimal sequence for coherent prompts
- **Specialized Responses**: Generating task-specific prompt instructions

## Extension and Customization

### Adding New ML Workflows
1. **Define Strategies**: Create prompt strategies for specific ML operations
2. **Organize Stages**: Group related strategies into logical processing phases
3. **Build Pipelines**: Combine stages into complete ML workflows
4. **Register Components**: Add new pipelines to the Prompt Engine orchestrator

### Integrating New LLM Providers
1. **Create Provider Configuration**: Extend LLMBaseConfig for new provider
2. **Implement Client Registration**: Register provider with AIQ framework
3. **Configure Authentication**: Handle API keys and authentication
4. **Update Workflow Configuration**: Add provider to agent configuration

### Extending Tool Functionality
1. **Define Tool Configuration**: Create configuration class extending FunctionBaseConfig
2. **Implement Tool Logic**: Create async function with appropriate business logic
3. **Register with AIQ**: Use register_function decorator for framework integration
4. **Update Agent Configuration**: Add tool to workflow configuration

## Benefits and Capabilities

### Dynamic Prompt Adaptation
- **Task-Specific Prompts**: Generated prompts are tailored to specific ML operations
- **Context Awareness**: System understands the type of ML problem being addressed
- **Intelligent Composition**: Optimal ordering and selection of prompt components

### Scalable Architecture
- **Modular Design**: Easy addition of new ML workflows and components
- **Framework Integration**: Leverages robust NVIDIA Agent IQ infrastructure
- **Plugin System**: Extensible architecture for new functionality

### Specialized ML Focus
- **Domain Expertise**: Built specifically for machine learning workflows
- **Comprehensive Coverage**: Supports diverse ML tasks and operations
- **Intelligent Planning**: Understands ML task requirements and dependencies


## Technical Implementation Details

### Configuration System
- **YAML-Based**: Human-readable configuration files
- **Hierarchical Structure**: Organized configuration for complex systems
- **Validation**: Pydantic-based configuration validation and type safety

### Asynchronous Architecture
- **Non-Blocking Operations**: All tools implemented as async functions
- **Concurrent Processing**: Efficient handling of multiple requests
- **Resource Management**: Proper cleanup and resource management

### Type Safety
- **Comprehensive Typing**: Full type hints throughout the codebase
- **Runtime Validation**: Pydantic models for configuration validation
- **Error Handling**: Proper error handling and user feedback

## Future Extensibility

The architecture is designed to support:
- **Additional ML Domains**: Extension to new areas of machine learning
- **Advanced Composition Patterns**: More sophisticated prompt composition strategies
- **Cross-Domain Integration**: Integration with other AI agent systems
- **Performance Optimization**: Enhanced caching and optimization strategies

## Summary

The Agent Engine represents a significant advancement in AI agent architecture, providing a sophisticated system for dynamic prompt composition in machine learning workflows. By combining the robust infrastructure of NVIDIA Agent IQ with a custom Prompt Engine framework, it creates intelligent agents capable of adapting their behavior to diverse ML tasks through real-time prompt composition.

The system's abstraction-driven design, hierarchical organization, and intelligent orchestration make it both powerful and extensible, providing a foundation for building sophisticated ML-focused AI agents that can adapt to changing requirements and diverse use cases.