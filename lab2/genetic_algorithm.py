from matplotlib import pyplot as plt
import numpy as np
import random


class Solver():
    def __init__(self, population_size, pc, pm, budget=10000):
        self.population_size = population_size
        self.pc = pc
        self.pm = pm
        self.t_max = int(budget / population_size)

    def get_parameters(self):
        return {"population size": self.population_size, "crossover probability": self.pc,
                "mutate probability": self.pm, "iterations": self.t_max}

    def set_parameters(self, new_population_size, new_pc, new_pm, new_budget=10000):
        self.population_size = new_population_size
        self.pc = new_pc
        self.pm = new_pm
        self.t_max = int(new_budget / new_population_size)


    def profit_function(self, engine_vector):
        height = 200
        speed = 0
        mass = 200 + sum(engine_vector)
        for element in engine_vector:
            if element == 1:
                mass -= 1
                acceleration = 45 / mass
            else:
                acceleration = 0
            acceleration -= 0.09
            speed += acceleration
            height += speed
        if height < 2 and abs(speed) < 2:
            return 2000 - sum(engine_vector)
        else:
            return -1000

    def make_population(self, bits_number=200):
        population = []
        for i in range(self.population_size):
            population.append([random.randint(0, 1) for j in range(bits_number)])
        return population


    def evaluate(self, population):
        evaluation = []
        for i in range(len(population)):
            evaluation.append(self.profit_function(population[i]) + 2000) # tu dodałe 2000 jako C
        return evaluation

    def roulette_selection(self, population, evaluation):
        probability = []
        for i in range(len(population)):
            probability.append(evaluation[i] / sum(evaluation))
        selected = np.random.default_rng().choice(population, len(population), p=probability)
        return selected


    def crossover(self, parent1, parent2):
        random_number = random.uniform(0, 1)
        if random_number < self.pc:
            n = random.randint(1, 200)
            child1 = np.concatenate((parent1[:n], parent2[n:]))
            child2 = np.concatenate((parent2[:n], parent1[n:]))
            return child1, child2
        else:
            return parent1, parent2

    def mutate(self, member):
        for i in range(len(member)):
            random_number = random.uniform(0, 1)
            if random_number < self.pm:
                member[i] = 1 if member[i] == 0 else 0
        return member


    def cross_and_mut(self, selected):
        new_population = []
        for i in range(0, len(selected), 2):
            parent1, parent2 = selected[i], selected[i+1]
            child1, child2 = self.crossover(parent1, parent2)
            new_population.append(self.mutate(child1))
            new_population.append(self.mutate(child2))
        return new_population


    def find_best(self, evaluation, population):
        max_index = evaluation.index(max(evaluation))
        best_value = evaluation[max_index]
        return best_value, population[max_index]


    def genetic_algorithm(self, bits_number=200):
        t = 0
        population = self.make_population(bits_number)
        evaluation = self.evaluate(population)
        best_for_now = self.find_best(evaluation, population)
        mean = sum(evaluation) / len(evaluation)
        best_history = [best_for_now]
        mean_history = [mean]
        while t < self.t_max:
            selected = self.roulette_selection(population, evaluation)
            new_pop = self.cross_and_mut(selected)
            evaluation = self.evaluate(new_pop)
            new_best = self.find_best(evaluation, new_pop)
            if new_best[0] > best_for_now[0]:
                best_for_now = new_best
            best_history.append(best_for_now)
            mean_history.append(sum(evaluation) / len(evaluation))
            population = new_pop
            t += 1
        return best_for_now, best_history, mean_history


def mean(solver, t=25):
    list = []
    for i in range(t):
        list.append(solver.genetic_algorithm()[2])
    return (np.array(list).sum(axis=0) / t) - 2000



def make_plots(p, pc, pm, type):
    for i in range(4):
        if type == 1:
            solver = Solver(p[i], pc, pm)
        elif type == 2:
            solver = Solver(p, pc[i], pm)
        else:
            solver = Solver(p, pc, pm[i])
        y = mean(solver)
        x = np.arange(len(y))
        plt.figure(figsize=(20, 10))
        plt.scatter(x, y)
        if type == 1:
            plt.title(f"Population size: {p[i]}, Crossover probability: {pc*100}%, Mutation probability: {pm*100}%")
        elif type ==2:
            plt.title(f"Population size: {p}, Crossover probability: {pc[i]*100}%, Mutation probability: {pm*100}%")
        else:
            plt.title(f"Population size: {p}, Crossover probability: {pc*100}%, Mutation probability: {pm[i]*100}%")
        plt.xlabel("Algorithm generation")
        plt.ylabel("Avarage profit")
        plt.grid(b=True)
        # plt.savefig(f"plot{i}p.png")

    plt.show()

def main():

    population_list = [20, 50, 100, 200]
    pc_list = [0.01, 0.1, 0.5, 0.9]
    pm_list = [0.001, 0.025, 0.1, 0.3]
    # make_plots(population_list, 0.1, 0.025, 1)



if __name__ == "__main__":
    main()