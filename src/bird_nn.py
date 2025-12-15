import random
import math
from utils import clamp
from copy import deepcopy
from pipe import Pipes
from flappy import Flappy

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
                self.weights[i] = clamp(self.weights[i], -1, 1)


    def distance(self, other):
        return sum(abs(w1 - w2) for w1, w2 in zip(self.weights, other.weights))

class BrainyBird:
    def __init__(self, bird=None, brain=None):
        if bird is None:
            self.bird = Flappy()
        else:
            self.bird = bird

        if brain is None:
            self.brain = BirdBrain()
        else:
            self.brain = brain

        self.alive = True
        self.fitness = 0.0

    def physics_update(self, delta: float, pipes: Pipes):
        (x, up_y), (_, down_y) = pipes.next_pipes(self.bird)
        res = self.brain.decide([x, self.bird.y - up_y - Pipes.sprite_height, down_y - self.bird.y, 1])
        self.bird.physics_update(delta, jump=res >= 0.75)
        self.fitness += delta

    def die(self):
        self.alive = False

    def draw(self, screen):
        self.bird.draw(screen)

    def clone(self):
        return BrainyBird(brain=self.brain.copy())
