import time
from copy import deepcopy

from src.visuals.graph import Plotting
from src.utils.sorting import Sorting
from src.models.vehicle import Vehicle
from src.methods.two_opt import TwoOpt
from src.methods.clustering import Clustering
from src.data.output_preparation import Output
from src.methods.calculations import Calculations
from src.data.data_preparation import DataPreparation


class RoutingService:
    @staticmethod
    def solve_routing(instance: dict,
                      no_of_vehicles: int,
                      no_of_pickups: int,
                      capacity: int,
                      use_n_n: bool,
                      use_polar_angle: bool = True) -> dict:
        """Solve the routing problem

        Args:
            instance (dict): The instance
            no_of_vehicles (int): The number of vehicles
            no_of_pickups (int): The number of pickups
            capacity (int): The capacity of the vehicles
            use_n_n (bool): The nearest neighbor flag
            use_polar_angle (bool): The polar angle flag

        Returns:
            output (dict): The output with the prepared solution information
        """
        t_start = time.perf_counter()
        data = DataPreparation(instance=instance,
                               no_of_vehicles=no_of_vehicles,
                               no_of_pickups=no_of_pickups,
                               capacity=capacity)

        distance_matrix = Calculations.create_distance_matrix(nodes=data.nodes)

        for node in data.nodes:
            if node.node_type != 'depot':
                node.polar_angle = Calculations.calculate_polar_angle(depot=data.depot, node=node)

        clusters, remaining_deliveries = Clustering.initiate_clusters(nodes=data.eligible_deliveries,
                                                                      no_of_vehicles=data.no_of_vehicles,
                                                                      capacity=data.capacity)

        if use_n_n:
            benefits = Calculations.calculate_nearest_neighbors_benefits(clusters=clusters, nodes=remaining_deliveries,
                                                                         distance_matrix=distance_matrix)
        else:
            benefits = Calculations.calculate_savings_benefits(clusters=clusters, nodes=remaining_deliveries,
                                                               distance_matrix=distance_matrix, depot=data.depot)

        unassigned_deliveries = Clustering.finalize_clusters(clusters=clusters, nodes=remaining_deliveries,
                                                             benefits=benefits, use_n_n=use_n_n,
                                                             use_polar_angle=use_polar_angle)
        Plotting.plot_route(data=data, clusters=clusters, header="Initial Route(s)")
        if not unassigned_deliveries:
            empty_clusters = [cluster for cluster in clusters.values() if len(cluster.nodes) == 1]

            if empty_clusters:

                sorted_empty_clusters = Sorting.get_sorted_clusters_by_ascending_seed_node_demand(
                    clusters=empty_clusters)

                for cluster in sorted_empty_clusters:
                    temporary_clusters = deepcopy(clusters)
                    Clustering.delete_cluster_nodes(clusters=temporary_clusters)
                    temporary_remaining_deliveries = deepcopy(remaining_deliveries)
                    temporary_remaining_deliveries.append(cluster.seed_node)
                    del temporary_clusters[cluster.cluster_no]

                    if use_n_n:
                        new_benefits = Calculations.calculate_nearest_neighbors_benefits(clusters=temporary_clusters,
                                                                                         nodes=temporary_remaining_deliveries,
                                                                                         distance_matrix=distance_matrix)
                    else:
                        new_benefits = Calculations.calculate_savings_benefits(clusters=temporary_clusters,
                                                                               nodes=temporary_remaining_deliveries,
                                                                               distance_matrix=distance_matrix,
                                                                               depot=data.depot)

                    new_unassigned_deliveries = Clustering.finalize_clusters(clusters=temporary_clusters,
                                                                             nodes=temporary_remaining_deliveries,
                                                                             benefits=new_benefits, use_n_n=use_n_n,
                                                                             use_polar_angle=use_polar_angle)

                    if new_unassigned_deliveries:
                        continue
                    else:
                        clusters = temporary_clusters
                        remaining_deliveries = temporary_remaining_deliveries
                        unassigned_deliveries = new_unassigned_deliveries

        if use_n_n:
            benefits_for_pickups = Calculations.calculate_nearest_neighbors_benefits(clusters=clusters,
                                                                                     nodes=data.eligible_pickups,
                                                                                     distance_matrix=distance_matrix)
        else:
            benefits_for_pickups = Calculations.calculate_savings_benefits(clusters=clusters,
                                                                           nodes=data.eligible_pickups,
                                                                           distance_matrix=distance_matrix,
                                                                           depot=data.depot)

        unassigned_pickups = Clustering.add_pickups_to_clusters(clusters=clusters, nodes=data.eligible_pickups,
                                                                benefits=benefits_for_pickups, use_n_n=use_n_n)

        for index, cluster in enumerate(clusters.values()):
            vehicle = Vehicle(id=index + 1,  capacity=cluster.capacity, route=cluster.nodes,
                              total_demand=cluster.total_demand, remaining_capacity=cluster.remaining_capacity)
            data.vehicles.append(vehicle)
            vehicle.set_route_sequence()
            vehicle.set_fulfilment_rate()
            vehicle.route_distance = Calculations.calculate_route_distance(nodes=vehicle.route,
                                                                           distance_matrix=distance_matrix)

        for vehicle in data.vehicles:
            TwoOpt.two_opt(vehicle=vehicle, distance_matrix=distance_matrix)

        t_end = time.perf_counter()
        elapsed_time = t_end - t_start
        data.unassigned_pickups = [node.id for node in unassigned_pickups]
        data.unassigned_deliveries += [node.id for node in unassigned_deliveries]
        data.set_unused_vehicles()
        output = Output.prepare_output(data=data, elapsed_time=elapsed_time)
        print(output)
        Plotting.plot_route(data=data, clusters=clusters, header="Final Route(s)")

        return output
