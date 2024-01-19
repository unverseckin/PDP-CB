import numpy as np
from dataclasses import dataclass
from copy import deepcopy

from src.models.node import Node
from src.models.vehicle import Vehicle
from src.methods.calculations import Calculations


@dataclass
class TwoOpt:
    """The 2-opt algorithm is a local search algorithm commonly used to improve
    solutions for the Traveling Salesman Problem (TSP). It iteratively performs
    a series of node swaps to reduce the total route distance."""
    @staticmethod
    def two_opt_swap(route: list[Node], index_1: int, index_2: int) -> list[Node]:
        """Swap two nodes in a route

        Args:
            route (list[Node]): The route
            index_1 (int): The index of the first node
            index_2 (int): The index of the second node

        Returns:
             list[Node]: The new route
        """
        new_route = route[:index_1] + route[index_1:index_2 + 1][::-1] + route[index_2 + 1:]
        return new_route

    @staticmethod
    def two_opt(vehicle: Vehicle, distance_matrix: np.ndarray) -> None:
        """Apply the 2-opt algorithm to a route

        Args:
            vehicle (Vehicle): The vehicle
            distance_matrix (np.ndarray): The distance matrix
        """
        route = deepcopy(vehicle.route)
        current_distance = Calculations.calculate_route_distance(nodes=route, distance_matrix=distance_matrix)
        improved = True

        while improved:
            improved = False
            for index_1 in range(0, len(route) - 1):
                for index_2 in range(index_1 + 1, len(route)):
                    new_route = TwoOpt.two_opt_swap(route=route, index_1=index_1, index_2=index_2)

                    if vehicle.is_route_feasible(route=new_route):
                        new_distance = Calculations.calculate_route_distance(nodes=new_route,
                                                                             distance_matrix=distance_matrix)
                        if new_distance < current_distance:
                            route = new_route
                            current_distance = new_distance
                            improved = True

        vehicle.route = route
        vehicle.set_route_sequence()
        vehicle.route_distance = current_distance
