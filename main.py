from src.configs.config import Instance
from src.services.service import RoutingService


def main():
    try:
        print("Please provide the following inputs to solve the routing problem")
        print(("1: Instance 1, Total number of nodes: 100, Total demand: 5147"
               "\n2: Instance 2, Total number of nodes: 250, Total demand: 1867"
               "\n3: Instance 3, Total number of nodes: 400, Total demand: 21275"
               "\n4: Instance 4, Total number of nodes: 700, Total demand: 3797"))
        instance = input("Choose an instance number: ")
        no_of_vehicles = input("Number of vehicles: ")
        no_of_pickups = input("Number of pickups: ")
        capacity = input("Vehicle capacity: ")
        use_n_n = input("Enter True for Nearest Neighbor or False for Savings: ")
        use_polar_angle = input("Use polar angle ? (True/False): ")
        output = RoutingService.solve_routing(Instance.instances[instance],
                                              no_of_vehicles=int(no_of_vehicles),
                                              no_of_pickups=int(no_of_pickups),
                                              capacity=int(capacity),
                                              use_n_n=bool(use_n_n),
                                              use_polar_angle=bool(use_polar_angle))

        return output

    except:
        print("Please provide valid inputs")


if __name__ == '__main__':
    main()
