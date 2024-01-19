import matplotlib.pyplot as plt

from src.models.cluster import Cluster
from src.data.data_preparation import DataPreparation


class Plotting:
    @staticmethod
    def plot_route(data: DataPreparation, clusters: dict[int, Cluster], header: str) -> None:
        """Plot the routes. If the vehicles are not assigned, it plots the clusters as the initial route(s).

        Args:
            data (DataPreparation): The data preparation object
            clusters (dict[int, Cluster]): The dictionary of clusters
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
                if index == 0:
                    x = []
                    y = []
                    x.append(data.depot.location.lon)
                    x.append(node.location.lon)
                    y.append(data.depot.location.lat)
                    y.append(node.location.lat)
                    ax.plot(x, y, color=colors[nodes_list.index(nodes) % len(colors)])
                    ax.annotate(str(node.id), (node.location.lon, node.location.lat), color='black')
                else:
                    x = []
                    y = []
                    x.append(nodes[index - 1].location.lon)
                    x.append(node.location.lon)
                    y.append(nodes[index - 1].location.lat)
                    y.append(node.location.lat)
                    ax.plot(x, y, color=colors[nodes_list.index(nodes) % len(colors)])

            x = []
            y = []
            x.append(nodes[-1].location.lon)
            x.append(data.depot.location.lon)
            y.append(nodes[-1].location.lat)
            y.append(data.depot.location.lat)
            ax.plot(x, y, color=colors[nodes_list.index(nodes) % len(colors)])

        plt.show()
