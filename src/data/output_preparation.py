from src.data.data_preparation import DataPreparation


class Output:
    @staticmethod
    def prepare_output(data: DataPreparation,
                       elapsed_time: float) -> dict:
        """Prepare the output

        Args:
            data (DataPreparation): The data preparation object
            elapsed_time (float): The elapsed time for the algorithm

        Returns:
            output (dict): The output with the following keys:
                total_distance (float): The total distance of the routes
                unassigned_pickups (list[Node]): The list of unassigned pickup ids
                unassigned_deliveries (list[Node]): The list of unassigned delivery ids
                minimum_required_vehicles (int): The minimum required vehicles
                unused_vehicles (int): The number of unused vehicles
                elapsed_time (float): The elapsed time for the algorithm
                routes (list[dict]): The list of routes with the following keys:
                    vehicle_id (int): The id of the vehicle
                    route_distance (float): The distance of the route
                    fulfillment_rate (str): The fulfillment rate of the route
                    route_sequence (list[Node]): The list of node ids in the route
        """
        total_distance = round(sum([vehicle.route_distance for vehicle in data.vehicles]), 2)
        output = {"total_distance": total_distance,
                  "unassigned_pickups": data.unassigned_pickups,
                  "unassigned_deliveries": data.unassigned_deliveries,
                  "minimum_required_vehicles": data.minimum_required_vehicles,
                  "unused_vehicles": data.unused_vehicles,
                  "elapsed_time": f"{round(elapsed_time, 2)} seconds",
                  "routes": []}

        for vehicle in data.vehicles:
            route = {"vehicle_id": vehicle.id,
                     "route_distance": vehicle.route_distance,
                     "capacity_utilization_rate": f"{round(vehicle.fulfillment_rate, 2)} %",
                     "number_of_nodes_visited": len(vehicle.route),
                     "route": vehicle.route_sequence}
            output["routes"].append(route)

        return output
