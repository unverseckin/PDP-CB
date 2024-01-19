import numpy as np

from src.models.node import Node
from src.models.vehicle import Vehicle
from src.methods.two_opt import TwoOpt
from src.methods.calculations import Calculations


def test_two_opt(monkeypatch):

    node_1 = Node(id=1, node_type='pickup', demand=10)
    node_2 = Node(id=2, node_type='delivery', demand=10)
    vehicle = Vehicle(route=[node_1, node_2], route_distance=100, capacity=20)

    def mock_two_opt_swap(route, index_1, index_2):
        return [node_1, node_2]

    monkeypatch.setattr(TwoOpt, "two_opt_swap", mock_two_opt_swap)

    def mock_calculate_route_distance(nodes, distance_matrix):
        return 50

    monkeypatch.setattr(Calculations, "calculate_route_distance", mock_calculate_route_distance)

    def mock_is_route_feasible(self, route):
        return True

    monkeypatch.setattr(Vehicle, "is_route_feasible", mock_is_route_feasible)

    def mock_set_route_sequence(self):
        return [2, 1]

    monkeypatch.setattr(Vehicle, "set_route_sequence", mock_set_route_sequence)

    TwoOpt.two_opt(vehicle, np.array([[0, 5], [5, 0]]))

    assert vehicle.route == [node_1, node_2]
    assert vehicle.route_distance == 50
