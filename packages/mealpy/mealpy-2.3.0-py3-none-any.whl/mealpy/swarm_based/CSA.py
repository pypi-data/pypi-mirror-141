# !/usr/bin/env python
# Created by "Thieu" at 18:37, 28/05/2021 ----------%
#       Email: nguyenthieu2102@gmail.com            %
#       Github: https://github.com/thieu1995        %
# --------------------------------------------------%

import numpy as np
from copy import deepcopy
from mealpy.optimizer import Optimizer


class BaseCSA(Optimizer):
    """
    The original version of: Cuckoo Search Algorithm (CSA)

    Links:
        1. https://doi.org/10.1109/NABIC.2009.5393690

    Hyper-parameters should fine tuned in approximate range to get faster convergen toward the global optimum:
        + p_a (float): [0.1, 0.7], probability a, default=0.3

    Examples
    ~~~~~~~~
    >>> import numpy as np
    >>> from mealpy.swarm_based.CSA import BaseCSA
    >>>
    >>> def fitness_function(solution):
    >>>     return np.sum(solution**2)
    >>>
    >>> problem_dict1 = {
    >>>     "fit_func": fitness_function,
    >>>     "lb": [-10, -15, -4, -2, -8],
    >>>     "ub": [10, 15, 12, 8, 20],
    >>>     "minmax": "min",
    >>>     "verbose": True,
    >>> }
    >>>
    >>> epoch = 1000
    >>> pop_size = 50
    >>> p_a = 0.3
    >>> model = BaseCSA(problem_dict1, epoch, pop_size, p_a)
    >>> best_position, best_fitness = model.solve()
    >>> print(f"Solution: {best_position}, Fitness: {best_fitness}")

    References
    ~~~~~~~~~~
    [1] Yang, X.S. and Deb, S., 2009, December. Cuckoo search via Lévy flights. In 2009 World
    congress on nature & biologically inspired computing (NaBIC) (pp. 210-214). Ieee.
    """

    def __init__(self, problem, epoch=10000, pop_size=100, p_a=0.3, **kwargs):
        """
        Args:
            problem (dict): The problem dictionary
            epoch (int): maximum number of iterations, default = 10000
            pop_size (int): number of population size, default = 100
            p_a (float): probability a, default=0.3
        """
        super().__init__(problem, kwargs)
        self.epoch = epoch
        self.pop_size = pop_size
        self.p_a = p_a
        self.n_cut = int(self.p_a * self.pop_size)
        self.nfe_per_epoch = self.pop_size + self.n_cut
        self.sort_flag = False

    def evolve(self, epoch):
        """
        The main operations (equations) of algorithm. Inherit from Optimizer class

        Args:
            epoch (int): The current iteration
        """
        pop_new = []
        for i in range(0, self.pop_size):
            ## Generate levy-flight solution
            levy_step = self.get_levy_flight_step(multiplier=0.001, case=-1)
            pos_new = self.pop[i][self.ID_POS] + 1.0 / np.sqrt(epoch + 1) * np.sign(np.random.random() - 0.5) * \
                      levy_step * (self.pop[i][self.ID_POS] - self.g_best[self.ID_POS])
            pos_new = self.amend_position(pos_new)
            pop_new.append([pos_new, None])
        pop_new = self.update_fitness_population(pop_new)
        list_idx_rand = np.random.choice(list(range(0, self.pop_size)), self.pop_size, replace=True)
        for idx in range(self.pop_size):
            if self.compare_agent(self.pop[list_idx_rand[idx]], pop_new[idx]):
                pop_new[idx] = deepcopy(self.pop[list_idx_rand[idx]])

        ## Abandoned some worst nests
        pop = self.get_sorted_strim_population(pop_new, self.pop_size)
        pop_new = []
        for i in range(0, self.n_cut):
            pos_new = np.random.uniform(self.problem.lb, self.problem.ub)
            pos_new = self.amend_position(pos_new)
            pop_new.append([pos_new, None])
        pop_new = self.update_fitness_population(pop_new)
        self.pop = pop[:(self.pop_size - self.n_cut)] + pop_new
