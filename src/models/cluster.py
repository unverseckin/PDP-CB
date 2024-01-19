from pydantic import Field
from dataclasses import dataclass

from src.models.node import Node


@dataclass
class Cluster:
    cluster_no: int = None
    seed_node: Node = None
    nodes: list[Node] = Field(default_factory=list)
    capacity: int = 0
    remaining_capacity: int = 0
    total_demand: int = 0

    def __post_init__(self):
        self.total_demand = sum([node.demand for node in self.nodes])
        self.remaining_capacity = self.capacity - self.total_demand