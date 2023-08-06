#!/usr/bin/env python
# Created by "Thieu" at 10:27, 06/03/2022 ----------%                                                                               
#       Email: nguyenthieu2102@gmail.com            %                                                    
#       Github: https://github.com/thieu1995        %                         
# --------------------------------------------------%

from mealpy.bio_based import SMA
from mealpy.evolutionary_based import GA
from mealpy.math_based import CGO
from base_tsp import TravellingSalesmanProblem
import numpy as np


def fitness_function(solution):
    ## For Travelling Salesman Problem, the solution should be a permutation
    ## Lowerbound: [0, 0,...]
    ## Upperbound: [N_cities - 1.11, ....]

    # print(solution)
    # print(solution.astype(int))
    solution = TSP.generate_valid_solution(solution)
    # print(solution)
    obj_value, total_distance = TSP.get_objective_value(solution)
    # print(f"Obj: {obj_value}, Dist: {total_distance}")
    return obj_value


# np.random.seed(10)
N_CITIES = 10
CITY_POSITIONS = np.random.rand(N_CITIES, 2)
TSP = TravellingSalesmanProblem(n_cities=N_CITIES, city_positions=CITY_POSITIONS)

# LB = [-0, ] * TSP.n_cities
# UB = [(N_CITIES - 1.11), ] * N_CITIES
# solution = np.random.uniform(LB, UB)
# fitness_function(solution)

# solution = np.array([1, 5, 9, 7, 8, 0, 2, 4, 6, 3])
# obj_value, total_distance = TSP.get_objective_value(solution)
# print(f"Obj: {obj_value}, dist: {total_distance}")

problem = {
    "fit_func": fitness_function,
    "lb": [-0, ] * TSP.n_cities,
    "ub": [(TSP.n_cities - 1.11), ] * TSP.n_cities,
    "minmax": "min",
    "verbose": True,
}

## Run the algorithm
# model = SMA.BaseSMA(problem, epoch=1000, pop_size=50, pr=0.03)
# model = GA.BaseGA(problem, epoch=10, pop_size=50)
model = CGO.OriginalCGO(problem, epoch=10, pop_size=50)
model.amend_position = TSP.amend_position
model.amend_position = TSP.amend_position
best_position, best_fitness = model.solve()
# print(best_position)
# best_position = TSP.generate_valid_solution(best_position)
obj_value, total_distance = TSP.get_objective_value(best_position)

# print(f"Best position: {best_position}")
print(f"Best position: {best_position}, Total Distance: {total_distance}")

# TSP.plot_solution(best_solution, total_distance)
# list_positions = [solution[0] for solution in model.history.list_global_best[1:]]
# TSP.plot_animate(list_positions)