from src.models.node import Node
from src.models.cluster import Cluster
from src.utils.sorting import Sorting
from src.models.benefit import Benefit
from src.methods.clustering import Clustering


def test_finalize_clusters(monkeypatch):
    clusters = {1: Cluster(cluster_no=1, seed_node=Node(id=1, demand=10, polar_angle=5),
                           nodes=[Node(id=1, demand=10, polar_angle=5)], remaining_capacity=20, capacity=50),
                2: Cluster(cluster_no=2, seed_node=Node(id=2, demand=15, polar_angle=5),
                           nodes=[Node(id=2, demand=15, polar_angle=5)], remaining_capacity=30, capacity=50)}
    nodes = [Node(id=3, demand=5, polar_angle=0.5), Node(id=4, demand=12, polar_angle=0.3)]
    benefit = [Benefit(cluster_no=1, distance=12), Benefit(cluster_no=2, distance=10)]

    benefits = {"node_ids": {3: benefit, 4: benefit}}
    use_n_n = True
    use_polar_angle = True

    def mock_demand_sort(nodes):
        return nodes

    monkeypatch.setattr(Sorting, "get_sorted_nodes_by_descending_demand", mock_demand_sort)

    def mock_ascending_sort(benefit):
        return benefit

    monkeypatch.setattr(Sorting, "get_sorted_clusters_by_ascending_benefit_distances", mock_ascending_sort)

    def mock_descending_sort(benefit):
        return benefit

    monkeypatch.setattr(Sorting, "get_sorted_clusters_by_descending_benefit_distances", mock_descending_sort)

    unassigned_nodes = Clustering.finalize_clusters(clusters, nodes, benefits, use_n_n, use_polar_angle)

    assert len(unassigned_nodes) == 0
    assert clusters[1].remaining_capacity == 23
    assert clusters[2].remaining_capacity == 35
