import math
from copy import deepcopy

from src.models.cluster import Cluster
from src.utils.sorting import Sorting
from src.models.node import Node


class Clustering:
    @staticmethod
    def get_interval(nodes: list[Node], no_of_vehicles: int) -> int:
        """Calculate the interval for the initial clusters

        Args:
            nodes (list[Node]): The list of nodes
            no_of_vehicles (int): The number of vehicles

        Returns:
             int: The interval for the initial clusters
        """
        return math.ceil(len(nodes) / no_of_vehicles)

    @staticmethod
    def get_initial_clusters(nodes: list[Node], interval: int) -> list[list[Node]]:
        """Calculate the initial clusters

        Args:
            nodes (list[Node]): The list of nodes
            interval (int): The interval for the initial clusters

        Returns:
             list[list[Node]]: The initial clusters
        """
        return [nodes[x:x + interval] for x in range(0, len(nodes), interval)]

    @staticmethod
    def set_seed_node(nodes: list[Node]) -> Node:
        """Set the seed node for a cluster

        Args:
            nodes (list[Node]): The list of nodes

        Returns:
             Node: The seed node
        """
        return Sorting.get_sorted_nodes_by_descending_demand(nodes=deepcopy(nodes))[0]

    @staticmethod
    def delete_cluster_nodes(clusters: dict[int, Cluster]) -> None:
        """Delete the nodes from the clusters

         Args:
            clusters (dict[int, Cluster]): The dictionary of clusters
        """
        for cluster in clusters.values():
            cluster.nodes = []
            cluster.nodes.append(cluster.seed_node)
            cluster.total_demand = cluster.seed_node.demand
            cluster.remaining_capacity = cluster.capacity - cluster.total_demand

    @staticmethod
    def initiate_clusters(nodes: list[Node],
                          no_of_vehicles: int,
                          capacity: int) -> tuple[dict[int, Cluster], list[Node]]:
        """Initiate the clusters

        Args:
            nodes (list[Node]): The list of nodes
            no_of_vehicles (int): The number of vehicles
            capacity (int): The capacity of the vehicles

        Returns:
             tuple[dict[int, Cluster], list[Node]]: The dictionary of clusters and the remaining nodes
        """
        clusters = {}
        nodes_sorted_by_polar_angle = Sorting.get_sorted_nodes_by_polar_angle(nodes=deepcopy(nodes))
        interval = Clustering.get_interval(nodes=nodes_sorted_by_polar_angle, no_of_vehicles=no_of_vehicles)
        initial_clusters = Clustering.get_initial_clusters(nodes=nodes_sorted_by_polar_angle, interval=interval)

        for index, cluster in enumerate(initial_clusters):
            seed_node = Clustering.set_seed_node(nodes=cluster)
            clusters.update({index + 1: (Cluster(cluster_no=index + 1,
                                                 seed_node=seed_node,
                                                 nodes=[seed_node],
                                                 capacity=capacity))})
            nodes_sorted_by_polar_angle.remove(seed_node)
        return clusters, nodes_sorted_by_polar_angle

    @staticmethod
    def finalize_clusters(clusters: dict[int, Cluster], nodes: list[Node], benefits: dict, use_n_n: bool,
                          use_polar_angle: bool) -> list[Node]:
        """Finalize the clusters

        Args:
            clusters (dict[int, Cluster]): The dictionary of clusters
            nodes (list[Node]): The list of nodes
            benefits (dict): The dictionary of benefits
            use_n_n (bool): The nearest neighbor flag
            use_polar_angle (bool): The polar angle flag

        Returns:
             list[Node]: The list of unassigned nodes
        """
        assigned_nodes = []
        nodes_sorted_by_demand = Sorting.get_sorted_nodes_by_descending_demand(nodes=deepcopy(nodes))

        for node in nodes_sorted_by_demand:
            if use_n_n:
                sorted_benefits = Sorting.get_sorted_clusters_by_ascending_benefit_distances(
                    benefit=benefits["node_ids"][node.id])
            else:
                sorted_benefits = Sorting.get_sorted_clusters_by_descending_benefit_distances(
                    benefit=benefits["node_ids"][node.id])

            for benefit in sorted_benefits:
                cluster = clusters[benefit.cluster_no]

                if cluster.remaining_capacity >= node.demand:
                    if use_polar_angle:
                        if cluster.seed_node.polar_angle > node.polar_angle:
                            cluster.nodes.insert(0, node)
                        else:
                            cluster.nodes.append(node)
                    else:
                        cluster.nodes.append(node)
                    cluster.remaining_capacity -= node.demand
                    cluster.total_demand += node.demand
                    assigned_nodes.append(node)
                    break

        unassigned_nodes = list(filter(lambda i: i not in assigned_nodes, nodes_sorted_by_demand))
        return unassigned_nodes

    @staticmethod
    def add_pickups_to_clusters(clusters: dict[int, Cluster], nodes: list[Node], benefits: dict, use_n_n: bool) -> list[
        Node]:
        """Add pickups to the clusters

        Args:
            clusters (dict[int, Cluster]): The dictionary of clusters
            nodes (list[Node]): The list of nodes
            benefits (dict): The dictionary of benefits
            use_n_n (bool): The nearest neighbor flag

        Returns:
             list[Node]: The list of unassigned nodes
        """
        assigned_nodes = []
        node_benefits_list = []

        for node, benefit in zip(nodes, benefits["node_ids"].values()):
            if use_n_n:
                sorted_benefits = Sorting.get_sorted_clusters_by_ascending_benefit_distances(benefit=benefit)
            else:
                sorted_benefits = Sorting.get_sorted_clusters_by_descending_benefit_distances(benefit=benefit)

            node_benefits_list.append((node, sorted_benefits))

        sorted_node_benefits_list = sorted(node_benefits_list, key=lambda x: x[1][0].distance, reverse=True)

        for node, sorted_benefits in sorted_node_benefits_list:
            for benefit in sorted_benefits:
                cluster = clusters[benefit.cluster_no]
                if cluster.nodes[-1].node_type != 'pickup':
                    cluster.nodes.append(node)
                    assigned_nodes.append(node)
                    break

        unassigned_nodes = list(filter(lambda i: i not in assigned_nodes, nodes))
        return unassigned_nodes
