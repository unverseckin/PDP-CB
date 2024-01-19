import numpy as np

from src.models.node import Node
from src.models.location import Location
from src.methods.calculations import Calculations


def test_create_distance_matrix(monkeypatch):

    node_1 = Node()
    node_1.location = Location(lon=0, lat=0)
    node_2 = Node()
    node_2.location = Location(lon=3, lat=4)

    nodes = [node_1, node_2]

    def mock_calculate_distance(node_1, node_2):
        return 5

    monkeypatch.setattr(Calculations, "calculate_distance", mock_calculate_distance)

    distance_matrix = Calculations.create_distance_matrix(nodes)

    expected_distance_matrix = np.array([[0, 5], [5, 0]])

    assert np.array_equal(distance_matrix, expected_distance_matrix)
