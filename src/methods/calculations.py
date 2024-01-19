import numpy as np
from math import sqrt, atan2, degrees

from src.models.node import Node
from src.models.benefit import Benefit
from src.models.cluster import Cluster


class Calculations:
    @staticmethod
    def calculate_distance(node_1: Node, node_2: Node) -> float:
        """Calculate the Euclidean distance between two nodes

         Args:
            node_1 (Node): The first node
            node_2 (Node): The second node

         Returns:
             float: The Euclidean distance between the two nodes
         """
        return sqrt((node_1.location.lat - node_2.location.lat) ** 2 + (node_1.location.lon - node_2.location.lon) ** 2)

    @staticmethod
    def create_distance_matrix(nodes: list[Node]) -> np.ndarray:
        """Create a distance matrix for the nodes

         Args:
            nodes (list[Node]): The list of nodes

         Returns:
             np.ndarray: The distance matrix
         """
        distance_matrix = np.zeros((len(nodes), len(nodes)))
        for row_index in range(len(nodes)):
            for column_index in range(len(nodes)):
                if row_index == column_index:
                    distance_matrix[row_index][column_index] = 0
                    continue
                distance = Calculations.calculate_distance(node_1=nodes[row_index], node_2=nodes[column_index])
                distance_matrix[row_index][column_index] = distance
                distance_matrix[column_index][row_index] = distance
        return distance_matrix

    @staticmethod
    def calculate_polar_angle(depot: Node, node: Node) -> float:
        """Calculate the polar angle between the depot and the node

         Args:
            depot (Node): The depot node
            node (Node): The node

         Returns:
             float: The polar angle between the depot and the node
         """
        radian = atan2(depot.location.lon - node.location.lon, depot.location.lat - node.location.lat)
        angle = degrees(radian)
        return angle if angle >= 0 else angle + 360

    @staticmethod
    def calculate_saving_for_node(distance_matrix: np.ndarray,
                                  seed_node: Node,
                                  candidate_node: Node,
                                  depot: Node) -> float:
        """Calculate the saved distance for a node

        Args:
            distance_matrix (np.ndarray): The distance matrix
            seed_node (Node): The seed node
            candidate_node (Node): The candidate node
            depot (Node): The depot node

        Returns:
            float: The saved distance for the node
        """
        saving = (distance_matrix[seed_node.id][depot.id]
                  + distance_matrix[depot.id][candidate_node.id]
                  - distance_matrix[seed_node.id][candidate_node.id])
        return saving

    @staticmethod
    def calculate_node_distances(distance_matrix: np.ndarray,
                                 seed_node: Node,
                                 candidate_node: Node) -> float:
        """Calculate the distance between a seed node and a candidate node

        Args:
            distance_matrix (np.ndarray): The distance matrix
            seed_node (Node): The seed node
            candidate_node (Node): The candidate node
        Returns:
            float: The distance between the seed node and the candidate node
        """
        distance = float(distance_matrix[seed_node.id][candidate_node.id])
        return distance

    @staticmethod
    def calculate_savings_benefits(clusters: dict[int, Cluster],
                                   nodes: list[Node],
                                   distance_matrix: np.ndarray,
                                   depot: Node) -> dict[str, dict]:
        """Calculate the Savings benefits for each node

         Args:
            clusters (dict[int, Cluster]): The dictionary of clusters
            nodes (list[Node]): The list of nodes
            distance_matrix (np.ndarray): The distance matrix
            depot (Node): The depot node

         Returns:
             dict[str, dict]: The dictionary of savings
         """
        savings = {"node_ids": {}}
        for node in nodes:
            savings["node_ids"].update({node.id: []})
            for cluster in clusters.values():
                savings["node_ids"][node.id].append(
                    Benefit(cluster_no=cluster.cluster_no,
                            distance=Calculations.calculate_saving_for_node(distance_matrix=distance_matrix,
                                                                            seed_node=cluster.seed_node,
                                                                            candidate_node=node,
                                                                            depot=depot)))
        return savings

    @staticmethod
    def calculate_nearest_neighbors_benefits(clusters: dict[int, Cluster],
                                             nodes: list[Node],
                                             distance_matrix: np.ndarray) -> dict[str, dict]:
        """Calculate the nearest neighbors benefits for each node

        Args:
            clusters (dict[int, Cluster]): The dictionary of clusters
            nodes (list[Node]): The list of nodes
            distance_matrix (np.ndarray): The distance matrix

        Returns:
             dict[str, dict]: The dictionary of nearest neighbors
        """
        neighbors = {"node_ids": {}}
        for node in nodes:
            neighbors["node_ids"].update({node.id: []})
            for cluster in clusters.values():
                neighbors["node_ids"][node.id].append(
                    Benefit(cluster_no=cluster.cluster_no,
                            distance=Calculations.calculate_node_distances(distance_matrix=distance_matrix,
                                                                           seed_node=cluster.seed_node,
                                                                           candidate_node=node)))
        return neighbors

    @staticmethod
    def calculate_route_distance(nodes: list[Node], distance_matrix: np.ndarray) -> int:
        """Calculate the total distance of a route

         Args:
            nodes (list[Node]): The list of nodes
            distance_matrix (np.ndarray): The distance matrix

         Returns:
             int: The total distance of the route
         """
        route_distance = 0
        for index in range(len(nodes)):
            if index == 0:
                route_distance += distance_matrix[0][nodes[index].id]
            else:
                route_distance += distance_matrix[nodes[index - 1].id][nodes[index].id]
        route_distance += distance_matrix[nodes[-1].id][0]
        return route_distance
