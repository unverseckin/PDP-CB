import matplotlib.pyplot as plt

from src.models.location import Location
from src.models.cluster import Cluster
from src.data.data_preparation import DataPreparation


class Plotting:
    @staticmethod
    def plot_route(data: DataPreparation, clusters: dict[int, Cluster], header: str) -> None:
        """Plot the routes. If the vehicles are not assigned, it plots the clusters as the initial route(s).

        Args:
            data (DataPreparation): The data preparation object
            clusters (dict[int, Cluster]): The dictionary of clusters
            header (str): The header of the plot
        """
        if data.vehicles:
            nodes_list = [vehicle.route for vehicle in data.vehicles]
        else:
            nodes_list = [cluster.nodes for cluster in clusters.values()]

        fig = plt.figure(figsize=(10, 10))
        fig.suptitle(header, fontsize=14, fontweight='bold')
        ax = fig.add_subplot()
        no_of_vehicles = len(data.vehicles) if data.vehicles else len(clusters)
        ax.set_title(f"Number of nodes: "
                     f"{len(data.nodes) - len(data.unassigned_pickups)- len(data.unassigned_deliveries) - 1} "
                     f"Number of vehicles: {no_of_vehicles}")
        ax.plot(data.depot.location.lon, data.depot.location.lat, color='green', marker='H')
        ax.annotate('DEPOT', (data.depot.location.lon, data.depot.location.lat), color='red')
        colors = ['red', 'green', 'yellow', 'orange', 'purple', 'brown', 'gray', 'olive', 'cyan']

        for nodes in nodes_list:
            for node in nodes:
                if node.node_type == 'pickup':
                    ax.plot(node.location.lon, node.location.lat, color='blue', marker='o')
                    ax.annotate('PICKUP', (node.location.lon, node.location.lat), color='blue')

                ax.plot(node.location.lon, node.location.lat, color='black', marker='.')

                index = nodes.index(node)
                color = colors[nodes_list.index(nodes) % len(colors)]
                if index == 0:

                    Plotting.plot_path(ax=ax, location_1=data.depot.location, location_2=node.location, color=color)
                else:
                    Plotting.plot_path(ax=ax, location_1=nodes[index - 1].location, location_2=node.location, color=color)

            Plotting.plot_path(ax=ax, location_1=nodes[-1].location, location_2=data.depot.location, color=color)

        plt.show()

    @staticmethod
    def plot_path(ax: plt, location_1: Location, location_2: Location, color: str) -> None:
        """Plot the path between two locations

        Args:
            ax (plt): The plot
            location_1 (Location): The first location
            location_2 (Location): The second location
            color (str): The color of the path
        """
        ax.plot([location_1.lon, location_2.lon], [location_1.lat, location_2.lat], color=color)
