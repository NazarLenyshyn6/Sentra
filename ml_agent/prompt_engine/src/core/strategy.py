""" 
This module provides an immutable and memory-efficient representation 
of a code-generation strategy used in ML pipelines. Each `Strategy` 
includes a unique identifier, a description explaining its applicability, 
and a prompt snippet that guides code generation.

The `Strategy` class is designed for clarity, immutability, and ease of use 
within larger systems that manage and compose multiple strategies.
"""


from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Strategy:
    """
    Immutable data class representing a code-generation strategy.
    
    Attributes:
        id: Unique strategy identifier. 
            It is automatically converted to uppercase upon initialization.
        description: Explanation of when and why to use this strategy.
        prompt: Instruction or template snippet to generate code.
    """
    
    id: str
    description: str = field(repr=False)
    prompt: str = field(repr=False)
    
    def __post_init__(self):
        """
        Enforce the `id` attribute to be uppercase after initialization.
        """
        object.__setattr__(self, 'id', self.id.upper())
        
    def get_usage_summary(self) -> str:
        """
        Return a concise one-line summary of the strategy for quick reference.

        Returns:
            A formatted string combining the strategy ID and description.
        """
        return f"{self.id:<20} : {self.description}"
