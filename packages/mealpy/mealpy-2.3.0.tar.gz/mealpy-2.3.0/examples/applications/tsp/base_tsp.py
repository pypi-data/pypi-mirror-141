#!/usr/bin/env python
# Created by "Thieu" at 10:27, 06/03/2022 ----------%                                                                               
#       Email: nguyenthieu2102@gmail.com            %                                                    
#       Github: https://github.com/thieu1995        %                         
# --------------------------------------------------%

import numpy as np
import matplotlib.pyplot as plt


class TravellingSalesmanProblem:
    def __init__(self, n_cities, city_positions):
        self.n_cities = n_cities
        self.city_positions = city_positions

    def create_solution(self):
        position = np.random.permutation(self.n_cities)
        fitness = self.get_fitness_position(position=position)
        return [position, fitness]

    def amend_position(self, solution=None):
        solution_set = set(list(range(0, len(solution))))
        solution_done = np.array([-1, ] * len(solution))
        solution_int = solution.astype(int)
        city_unique, city_counts = np.unique(solution_int, return_counts=True)
        ## Way 2: Random, not stable
        # count_dict = dict(zip(*np.unique(solution_int, return_counts=True)))
        count_dict = dict(zip(city_unique, city_counts))
        for idx, city in enumerate(solution_int):
            if solution_done[idx] != -1:
                continue
            if city in city_unique:
                if city in (solution_set - set(solution_done)):
                    if count_dict[city] == 1:
                        solution_done[idx] = city
                    else:
                        idx_list_city = np.where(solution_int == city)[0]
                        idx_city_keep = np.random.choice(idx_list_city)
                        solution_done[idx_city_keep] = city
                        if idx_city_keep != idx:
                            solution_done[idx] = np.random.choice(list(solution_set - set(solution_done) - set(city_unique)))
                else:
                    solution_done[idx] = np.random.choice(list(solution_set - set(solution_done) - set(city_unique)))
            else:
                solution_done[idx] = np.random.choice(list(solution_set - set(solution_done) - set(city_unique)))
        # print(solution_done)
        return solution_done

    def amend_position(self, position=None):
        return self.amend_position(position)

    def generate_valid_solution(self, solution, strategy="random"):
        solution_set = set(list(range(0, len(solution))))
        solution_done = np.array([-1, ] * len(solution))
        solution_int = solution.astype(int)
        city_unique, city_counts = np.unique(solution_int, return_counts=True)

        ### Way 1: Stable, not random
        for idx, city in enumerate(solution_int):
            if solution_done[idx] != -1:
                continue
            if city in city_unique:
                solution_done[idx] = city
                city_unique = np.where(city_unique == city, -1, city_unique)
            else:
                list_cities_left = list(solution_set - set(city_unique) - set(solution_done))
                # print(list_cities_left)
                solution_done[idx] = list_cities_left[0]
        return solution_done

        ### Way 2: Random, not stable
        ## count_dict = dict(zip(*np.unique(solution_int, return_counts=True)))
        # count_dict = dict(zip(city_unique, city_counts))
        # for idx, city in enumerate(solution_int):
        #     if solution_done[idx] != -1:
        #         continue
        #     if city in city_unique:
        #         if city in (solution_set - set(solution_done)):
        #             if count_dict[city] == 1:
        #                 solution_done[idx] = city
        #             else:
        #                 idx_list_city = np.where(solution_int == city)[0]
        #                 idx_city_keep = np.random.choice(idx_list_city)
        #                 solution_done[idx_city_keep] = city
        #                 if idx_city_keep != idx:
        #                     solution_done[idx] = np.random.choice(list(solution_set - set(solution_done) - set(city_unique)))
        #         else:
        #             solution_done[idx] = np.random.choice(list(solution_set - set(solution_done) - set(city_unique)))
        #     else:
        #         solution_done[idx] = np.random.choice(list(solution_set - set(solution_done) - set(city_unique)))
        # return solution_done

    def get_objective_value(self, solution):
        city_coord = self.city_positions[solution]
        line_x = city_coord[:, 0]
        line_y = city_coord[:, 1]
        total_distance = np.sum(np.sqrt(np.square(np.diff(line_x)) + np.square(np.diff(line_y))))
        obj_value = np.exp(self.n_cities * 2 / total_distance)
        return total_distance, total_distance

    def plot_animate(self, list_positions):
        for epoch, position in enumerate(list_positions):
            solution = self.generate_valid_solution(position)
            obj_value, total_distance = self.get_objective_value(solution)
            city_coord = self.city_positions[solution]
            line_x = city_coord[:, 0]
            line_y = city_coord[:, 1]
            plt.scatter(self.city_positions[:, 0].T, self.city_positions[:, 1].T, s=100, c='k')
            # add text annotation
            for city in range(0, self.n_cities):
                plt.text(self.city_positions[city][0] + 0.025, self.city_positions[city][1] - 0.075,
                         f"{city}", size='medium', color='black', weight='semibold')
            plt.plot(line_x.T, line_y.T, 'r-')
            plt.text(-0.05, -0.05, "Total distance=%.2f" % total_distance, fontdict={'size': 12, 'color': 'red'})
            plt.xlim((-0.1, 1.1))
            plt.ylim((-0.1, 1.1))
            plt.title(f"Epoch: {epoch + 1}, GBest: {solution}")
            plt.show()

    def plot_solution(self, best_solution, total_d):
        city_coord = self.city_positions[best_solution]
        line_x = city_coord[:, 0]
        line_y = city_coord[:, 1]
        plt.scatter(self.city_positions[:, 0].T, self.city_positions[:, 1].T, s=100, c='k')
        # add text annotation
        for city in range(0, self.n_cities):
            plt.text(self.city_positions[city][0] + 0.025, self.city_positions[city][1] - 0.075,
                     f"{city}", size='medium', color='black', weight='semibold')
        plt.plot(line_x.T, line_y.T, 'r-')
        plt.text(-0.05, -0.05, "Total distance=%.2f" % total_d, fontdict={'size': 14, 'color': 'red'})
        plt.xlim((-0.1, 1.1))
        plt.ylim((-0.1, 1.1))
        plt.title(f"Best solution: {best_solution}")
        plt.show()
