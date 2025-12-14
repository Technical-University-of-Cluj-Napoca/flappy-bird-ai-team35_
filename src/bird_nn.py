from random import random
from math import exp

def sigmoid(x):
    return 1 / (1 + exp(-x))

class BirdNN:
    weight_num = 4

    def __init__(self):
        self.weights = [random() * 2 - 1 for _ in range(wegith_num)]

    def run(self, inputs: list[float]):
        sum_ = 0
        for i, w in zip(self.weights, inputs):
            sum_ += i * w

        return sigmoid(sum_)

