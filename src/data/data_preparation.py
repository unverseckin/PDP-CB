import pandas as pd

from src.models.node import Node
from src.utils.sorting import Sorting
from src.models.location import Location


class DataPreparation:
    def __init__(self, instance: dict, no_of_vehicles: int, no_of_pickups: int, capacity: int):
        self.path = instance.get("path")
        self.no_of_customers = instance.get("number_of_customers")
        self.no_of_pickups = no_of_pickups
        self.no_of_vehicles = no_of_vehicles
        self.capacity = capacity
        self.nodes = []
        self.vehicles = []
        self.depot = []
        self.eligible_pickups = []
        self.eligible_deliveries = []
        self.unassigned_pickups = []
        self.unassigned_deliveries = []
        self.minimum_required_vehicles = 0
        self.unused_vehicles = 0

        DataPreparation.create_nodes(self)
        DataPreparation.set_depot(self)
        DataPreparation.set_eligible_pickups_by_no_of_vehicles(self)
        DataPreparation.set_eligible_deliveries_by_ascending_demand(self)
        DataPreparation.set_minimum_number_of_required_vehicles(self)

    def get_demand_data(self) -> pd.DataFrame:
        """Get demand data from the instance file

        Returns:
            pd.DataFrame: The demand data
        """
        df = pd.read_csv(self.path, delim_whitespace=True)
        start = df.loc[df.NAME == 'NODE_COORD_SECTION'].index[0]
        location_data = pd.read_csv(self.path,
                                    skiprows=start + 2,
                                    delim_whitespace=True,
                                    header=None,
                                    index_col=0,
                                    nrows=self.no_of_customers + 1)
        start = df.loc[df.NAME == 'DEMAND_SECTION'].index[0]
        demand_data = pd.read_csv(self.path,
                                  skiprows=start + 2,
                                  delim_whitespace=True,
                                  header=None,
                                  index_col=0,
                                  nrows=self.no_of_customers + 1)

        data = pd.concat([location_data, demand_data], axis=1)
        data.index -= 1
        return data

    def create_nodes(self) -> None:
        """Create nodes from the demand data
            Node Types: 1 - Depot, 2 - Pickup, 3 - Delivery"""
        demand_data = self.get_demand_data()
        for row in demand_data.itertuples():
            if row.Index == 0:
                depot = Node(id=row.Index,
                             location=Location(lat=row[1], lon=row[2]),
                             demand=row[3],
                             node_type='depot')
                self.nodes.append(depot)
            elif row.Index <= self.no_of_pickups:
                customer = Node(id=row.Index,
                                location=Location(lat=row[1], lon=row[2]),
                                demand=row[3],
                                node_type='pickup')
                self.nodes.append(customer)
            else:
                customer = Node(id=row.Index,
                                location=Location(lat=row[1], lon=row[2]),
                                demand=row[3],
                                node_type='delivery')
                self.nodes.append(customer)

    def set_depot(self) -> None:
        """Set the depot node"""""
        self.depot = [node for node in self.nodes if node.node_type == 'depot'][0]

    def set_eligible_pickups_by_no_of_vehicles(self) -> None:
        """Set the eligible pickups by the number of vehicles"""
        self.eligible_pickups = [node for node in self.nodes if node.node_type == 'pickup']

    def set_eligible_deliveries_by_ascending_demand(self) -> None:
        """Set the eligible deliveries by ascending demand
        Not eligible deliveries are added to the unassigned deliveries list
        """
        demand = 0
        total_capacity = self.capacity * self.no_of_vehicles
        deliveries = [node for node in self.nodes if node.node_type == 'delivery']
        deliveries_sorted_by_demand = Sorting.get_sorted_nodes_by_ascending_demand(nodes=deliveries)
        for node in deliveries_sorted_by_demand:
            if demand + node.demand <= total_capacity:
                self.eligible_deliveries.append(node)
                demand += node.demand
            else:
                self.unassigned_deliveries.append(node.id)

    def set_minimum_number_of_required_vehicles(self) -> None:
        """Set the minimum number of required vehicles based on the eligible deliveries total demand"""
        required_total_capacity = sum([node.demand for node in self.nodes if node.node_type == 'delivery'])
        self.minimum_required_vehicles = required_total_capacity // self.capacity
        if required_total_capacity % self.capacity != 0:
            self.minimum_required_vehicles += 1

    def set_unused_vehicles(self) -> None:
        """Set the unused vehicles"""
        self.unused_vehicles = self.no_of_vehicles - len(self.vehicles)
