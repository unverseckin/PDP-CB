from src.models.node import Node
from src.models.benefit import Benefit
from src.models.cluster import Cluster


class Sorting:
    @staticmethod
    def get_sorted_nodes_by_polar_angle(nodes: list[Node]) -> list[Node]:
        """Sort the nodes by polar angle

        Args:
            nodes (list[Node]): The list of nodes

        Returns:
             list[Node]: The list of nodes sorted by polar angle
        """
        return sorted(nodes, key=lambda x: x.polar_angle)

    @staticmethod
    def get_sorted_nodes_by_ascending_demand(nodes: list[Node]) -> list[Node]:
        """Sort the nodes by ascending demand

        Args:
            nodes (list[Node]): The list of nodes

        Returns:
             list[Node]: The list of nodes sorted by ascending demand
        """
        return sorted(nodes, key=lambda x: x.demand)

    @staticmethod
    def get_sorted_nodes_by_descending_demand(nodes: list[Node]) -> list[Node]:
        """Sort the nodes by descending demand

        Args:
            nodes (list[Node]): The list of nodes

        Returns:
            list[Node]: The list of nodes sorted by descending demand
        """
        return sorted(nodes, key=lambda x: x.demand, reverse=True)

    @staticmethod
    def get_sorted_clusters_by_descending_benefit_distances(benefit: list[Benefit]) -> list[Benefit]:
        """Sort the clusters by descending distance

        Args:
            benefit (list[Benefit]): The list of benefits

        Returns:
            list[Saving]: The list of savings sorted by descending benefit distance
        """
        return sorted(benefit, key=lambda x: x.distance, reverse=True)

    @staticmethod
    def get_sorted_clusters_by_ascending_benefit_distances(benefit: list[Benefit]) -> list[Benefit]:
        """Sort the clusters by ascending distance

        Args:
            benefit (list[Benefit]): The list of benefits

        Returns:
            list[Saving]: The list of savings sorted by ascending benefit distance
        """
        return sorted(benefit, key=lambda x: x.distance)

    @staticmethod
    def get_sorted_clusters_by_ascending_seed_node_demand(clusters: list[Cluster]) -> list[Cluster]:
        """Sort the clusters by ascending seed node demand

        Args:
            clusters (list[Cluster]): The list of clusters

        Returns:
            list[Cluster]: The list of clusters sorted by ascending seed node demand
        """
        return sorted(clusters, key=lambda x: x.seed_node.demand)
