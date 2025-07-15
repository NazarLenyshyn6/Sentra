"""
This module defines the RegistryBase class, a generic base for components
that maintain a registry of items identified by string keys.

It provides common container-like behavior such as:
- Normalizing and enforcing uppercase IDs.
- Iteration over registered values.
- Length inspection and membership testing via in.

Designed to be used as a base class or mixin for more specialized registry-based
components such as Stage or Pipeline, enabling DRY, modular design.
"""

from typing import Dict, Generic, TypeVar, Iterator

T = TypeVar("T")


class Registry(Generic[T]):
    """
    A generic base class for registry-backed components.

    This class encapsulates common container behavior for objects that manage
    an internal registry of items (e.g., strategies, stages) indexed by string keys.

    Features:
        - Enforces normalization of the `id` attribute to uppercase.
        - Supports iteration over registered items.
        - Provides length inspection and membership checks using standard Python syntax.

    Type Parameters:
        T: The type of the items stored in the registry (e.g., Strategy, Stage).

    Intended Usage:
        Subclass this base to implement registry-enabled components like `Stage` or `Pipeline`,
        promoting reuse and DRY design across prompt-driven systems.
    """
    
    id: str
    description: str
    _registry: Dict[str, T]

    def __post_init__(self) -> None:
        """
        Normalize the ID to uppercase.
        """
        object.__setattr__(self, "id", self.id.upper())

    def __iter__(self) -> Iterator[T]:
        """
        Allow iteration over the registered items.
        """
        return iter(self._registry.values())

    def __len__(self) -> int:
        """
        Return the number of registered items.
        """
        return len(self._registry)

    def __contains__(self, item_id: str) -> bool:
        """
        Check whether an item with the given ID exists in the registry.
        """
        return item_id.upper() in self._registry
