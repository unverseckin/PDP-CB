# PDP-CB
## A hybrid Pick-up and Delivery Problem solver algorithm
### Introduction
This project is a hybrid algorithm for solving the Pick-up and Delivery Problem (PDP). The algorithm is based on a combination of steps:

1. Sweep clustering to initialize clusters,
2. Constructive heuristics (Nearest Neighbor and Savings algorithm),
3. 2-opt route improvement heuristic.

The algorithm is implemented in Python 3.11 and uses the [Matplotlib](https://matplotlib.org/) library for the visualization of the results. The algorithm is tested on the [Uchoa et al. (2014)](http://vrp.galgos.inf.puc-rio.br/index.php/en/) instances.

### Requirements
```sh
pip install -r requirements.txt
```

### Run
```sh
python main.py
```