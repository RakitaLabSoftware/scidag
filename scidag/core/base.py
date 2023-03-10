import abc
import inspect
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Self

from scidag.core.struct.variable import Variable
from scidag.storage import Storage


class Base(abc.ABC):
    storage: Storage

    @abc.abstractmethod
    async def run(self) -> None:
        """
        Gets inputs from storage runs function and put outputs to storage
        """


class Configurable(abc.ABC):
    storage: Storage

    @abc.abstractmethod
    async def run(self) -> None:
        """
        Gets inputs from storage runs function and put outputs to storage
        """

    @classmethod
    @abc.abstractmethod
    def from_config(cls, cfg: Any) -> Self:
        r"""
        Build :class:`Self` by provided config
        """

    def to_config(self, cfg: Any) -> Any:
        pass


class ANode(Configurable):
    """
    Node of DAG
    """

    name: str
    inputs: dict[str, Variable] | None
    outputs: Variable

    @abc.abstractmethod
    def set_storage(self, storage: Storage) -> None:
        pass

    @abc.abstractmethod
    async def run(self) -> None:
        """
        Gets inputs from storage runs function and put outputs to storage
        """


class AGraph(Base):
    @property
    @abc.abstractmethod
    def all_nodes(self):
        pass

    @abc.abstractmethod
    def get_node(self, node_name: str) -> ANode:
        r"""Get :class:`scidag.Node` by its name"""

    @abc.abstractmethod
    def add(self, node: ANode) -> None:
        r"""Add :class:`scidag.Node` to pool of nodes"""

    @abc.abstractmethod
    def remove(self, node: ANode) -> None:
        r"""Remove :class:`scidag.Node` from this dag"""

    @abc.abstractmethod
    def connect(self, u_node_name: str, v_node_name: str) -> None:
        r"""Add edge between two nodes"""

    @abc.abstractmethod
    def disconnect(self, u_node_name: str, v_node_name: str) -> None:
        r"""Remove edge between two nodes"""

    @abc.abstractmethod
    def get_available_nodes(self, node_name: str) -> list[str] | None:
        r"""
        Shows available tasks to add after this task

        Returns
        -------
        list[str] | None
            Available tasks after this task
        """

    @abc.abstractmethod
    def save(self) -> None:
        r"""Save Current run"""

    @abc.abstractclassmethod
    def __call__(self) -> None:
        """Run dag with logging and saving configuration file"""

    @abc.abstractclassmethod
    async def run(self) -> None:
        pass
