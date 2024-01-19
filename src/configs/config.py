class Instance:
    instances = {1: {"path": 'src/data/input/X-n101-k25.txt',
                     "number_of_customers": 100,
                     "number_of_vehicles": 25,
                     "capacity": 206,
                     "total_demand": 5147},
                 2: {"path": 'src/data/input/X-n251-k28.txt',
                     "number_of_customers": 250,
                     "number_of_vehicles": 28,
                     "capacity": 69,
                     "total_demand": 1867},
                 3: {"path": 'src/data/input/X-n401-k29.txt',
                     "number_of_customers": 400,
                     "number_of_vehicles": 29,
                     "capacity": 745,
                     "total_demand": 21275},
                 4: {"path": 'src/data/input/X-n701-k44.txt',
                     "number_of_customers": 700,
                     "number_of_vehicles": 44,
                     "capacity": 87,
                     "total_demand": 3797}
                 }


class Config:
    MAX_DISTANCE = 9999999
