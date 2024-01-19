from src.configs.config import Instance
from src.services.service import RoutingService


def main():
    output = RoutingService.solve_routing(Instance.instance_2,
                                          no_of_vehicles=1,
                                          no_of_pickups=1,
                                          capacity=1867,
                                          n_n=True)

    return output


if __name__ == '__main__':
    main()
