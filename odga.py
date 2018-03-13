import random
from deap import base
from deap import creator
from deap import tools

i = 5

creator.create("FitnessMin", base=base.Fitness, weights=(-1.0, 1))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("attr_float", random.random)
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attr_float, n=i)

ind1 = toolbox.individual()

print(ind1)


print(ind1.fitness.valid)

mul = toolbox.clone(ind1)

ind2, = tools.mutGaussian(mul, mu=0.0, sigma=0.2, indpb=0.2)


print(mul)