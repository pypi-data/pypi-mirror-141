from math import sqrt

import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import beta


class Belief:
    """A class storing information about belief and confidence of an alternative.

    Params:
      a, b (float): Parameters for Beta(a,b) distribution that forms the belief about p
      confidence (float): 1 minus standard deviation of belief (high value -> high confidence)
      max_confidence (float): Max confidence value until learning happens (value between [0,1])
      unlearn (bool): If true rebases when a shock hits respective alternative.
    """

    def __init__(self, a=1, b=1, max_confidence=1, unlearn=False):
        self.a = a
        self.b = b
        self.max_confidence = max_confidence
        self.unlearn = unlearn

    def evaluate(self):
        """Returns the quantified belief for making decisions."""
        return np.random.beta(self.a, self.b)

    def get_confidence(self):
        """Returns confidence, i.e. 1 - (normalized s.d.)"""
        sd = sqrt((self.a * self.b) / ((self.a + self.b + 1) * ((self.a + self.b) ** 2)))
        max_sd = sqrt(1 / 12)  # sd is max for U(0,1)
        return (max_sd - sd) / max_sd

    def get_mean_belief(self):
        return self.a / (self.a + self.b)

    def update(self, x):
        """Update belief (= update distribution) and confidence."""
        if self.get_confidence() < self.max_confidence:
            self.a += x
            self.b += (1 - x)

    def unlearn(self):
        """Forget all knowledge, i.e. return to uniform distribution."""
        self.a = 1
        self.b = 1

    def plot(self):
        """Plots the distribution of belief."""
        x = np.linspace(0, 1, 100)
        y = beta.pdf(x, self.a, self.b)
        plt.plot(x, y)
