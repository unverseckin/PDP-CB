from pydantic import Field
from dataclasses import dataclass

from src.models.node import Node


@dataclass
class Vehicle:
    id: int = None
    capacity: int = None
    route: list[Node] = Field(default_factory=list)
    route_sequence: list[int] = Field(default_factory=list)
    total_demand: int = 0
    fulfillment_rate: float = 0
    remaining_capacity: int = 0
    route_distance: float = 0

    def __post_init__(self):
        self.total_demand = sum(node.demand for node in self.route if node.node_type == 'delivery')
        self.remaining_capacity = self.capacity - self.total_demand

    def is_route_feasible(self, route: list[Node]) -> bool:
        """Check if the route is feasible for pickup task to be made

        Returns:
            bool: True if the route is feasible for pickup task to be made, False otherwise
        """
        pickup_node = None
        current_available_capacity = self.remaining_capacity
        for node in route:
            if node.node_type == 'pickup':
                pickup_node = node
                break
            else:
                current_available_capacity += node.demand
        if pickup_node:
            return current_available_capacity >= pickup_node.demand
        return True

    def set_route_sequence(self) -> None:
        """Set the route sequence of the vehicle"""
        self.route_sequence = [node.id for node in self.route]

    def set_fulfilment_rate(self) -> None:
        """Set the fulfilment rate of the vehicle"""
        self.fulfillment_rate = (self.total_demand / self.capacity) * 100
