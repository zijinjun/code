import math
from random import random
import matplotlib.pyplot as plt
import numpy as np


def func(x, y):  # the function to be optimized
    n = lambda x, y: math.sin(math.sqrt(x * x + y * y)) ** 2 - 0.5
    d = lambda x, y: (1 + 0.001 * (x * x + y * y)) ** 2
    func = lambda x, y: 0.5 - n(x, y) / d(x, y)
    return func(x, y)


# x is the "x1" in the formula, y is the "x2" in the formula
class SA:
    def __init__(self, func, iter=100, T0=100, Tf=0.01, alpha=0.99):
        self.func = func
        self.iter = iter  # the iteration times of the inner loop,that is L=100
        self.alpha = alpha  # the cooling down factor，alpha=0.99
        self.T0 = T0  # initial temperature T0=100
        self.Tf = Tf  # final temperature Tf=0.01
        self.T = T0  # current temperature
        self.x = [random() * 11 - 5 for i in range(iter)]  # randomly generate 100 values for x
        self.y = [random() * 11 - 5 for i in range(iter)]  # randomly generate 100 values for y
        self.most_best = []
        """
        Function random() will take a real number value ranging from 0 to 1.
        If integer values ranging from 0 to 10 are wanted, we can use (int)random()*11.
        After discarding the demical places of random()*11 ,it will satisfy the needs.
        In this example, the absolute value of x1 and x2 will not exceed 5(including 5 and -5), and the result of (random()*11-5) is an arbitary value in range (-6,6)
        the result of (random()*10-5) is an arbitary value in range (-5,5) which will not be 5 or -5.
        So we times 11 first and use if to select those within range [-5,5] when generating new solutions
        """
        self.history = {'f': [], 'T': []}

    def generate_new(self, x, y):  # Create disturbance to generate new solutions.
        while True:
            x_new = x + self.T * (random() - random())
            y_new = y + self.T * (random() - random())
            if (-5 <= x_new <= 5) & (-5 <= y_new <= 5):
                break  # Repeat until new solutions satisfy the constraints.
        return x_new, y_new

    def Metrospolis(self, f, f_new):  # Metropolis criterion
        if f_new <= f:
            return 1
        else:
            p = math.exp((f - f_new) / self.T)
            if random() < p:
                return 1
            else:
                return 0

    def best(self):  # Obtain the optimal value of the target function
        f_list = []  #  Save the results after every iteration in the list "f_list".
        for i in range(self.iter):
            f = self.func(self.x[i], self.y[i])
            f_list.append(f)
        f_best = min(f_list)

        idx = f_list.index(f_best)
        return f_best, idx  # f_best,idx are the optimal value of the target function and its index in the list at this temperature after L times of iteration, respectively.

    def run(self):
        count = 0
        # The outer loop will stop when the current temperature is lower than the final temperature.
        while self.T > self.Tf:

            # The inner loop will iterate 100 times
            for i in range(self.iter):
                f = self.func(self.x[i], self.y[i])  # "f" is the current optimal value after several iterations.
                x_new, y_new = self.generate_new(self.x[i], self.y[i])  # generate new solutions
                f_new = self.func(x_new, y_new)  # calculate corresponding value of the target function
                if self.Metrospolis(f, f_new):  # 判断是否接受新值 determine whether thw new solution is accepted
                    self.x[i] = x_new  # If accepted, save the solutions in the list "x" and "y".
                    self.y[i] = y_new
            # Iterate L times and save the optimal value and solutions at this temperature
            ft, _ = self.best()
            self.history['f'].append(ft)
            self.history['T'].append(self.T)
            # Temperature lowers at a fixed ratio(cooling down)
            self.T = self.T * self.alpha
            count += 1

            # Obtain the optimal value and solutions
        f_best, idx = self.best()
        print(f"F={f_best}, x={self.x[idx]}, y={self.y[idx]}")


sa = SA(func)
sa.run()

