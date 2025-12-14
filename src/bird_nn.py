import random
import math
from copy import deepcopy

class BirdBrain:

    def __init__(self, brain=None):
        if brain:
            self.weights = deepcopy(brain.weights)
        else:
            self.weights = [
                random.uniform(-1, 1),
                random.uniform(-1, 1),
                random.uniform(-1, 1),
                random.uniform(-1, 1)
            ]

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + math.exp(-x))

    def decide(self, inputs):
        assert len(inputs) == 4

        weighted_sum = 0.0
        for w, i in zip(self.weights, inputs):
            weighted_sum += w * i

        return BirdBrain.sigmoid(weighted_sum)

    def copy(self):
        return BirdBrain(self)

    def mutate(self, mutation_rate=0.1, mutation_strength=0.1):
        for i in range(len(self.weights)):
            if random.random() < mutation_rate:
                self.weights[i] += random.gauss(0, mutation_strength)

    def distance(self, other):
        return sum(abs(w1 - w2) for w1, w2 in zip(self.weights, other.weights))
