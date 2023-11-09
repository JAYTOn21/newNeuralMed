import math

import numpy as np


class Network:
    weights = []  # матрицы весов слоя
    x = []  # вход слоя
    z = []  # активированный выход слоя
    df = []  # производная функции активации слоя
    deltas = []  # дельты ошибки на каждом слое

    layersN = 0  # число слоёв

    def __init__(self, sizes):
        self.layersN = len(sizes) - 1  # запоминаем число слоёв

        for i in range(1, len(sizes)):
            self.weights.append(np.random.rand(sizes[i], sizes[i - 1]))  # создаём матрицу весовых коэффициентов
            self.x.append(np.zeros(sizes[i - 1]))  # создаём вектор для входа слоя
            self.z.append(np.zeros(sizes[i]))  # создаём вектор для выхода слоя
            self.df.append(np.zeros(sizes[i]))  # создаём вектор для производной слоя
            self.deltas.append(np.zeros(sizes[i]))  # создаём вектор для дельт

    def feedForward(self, inputVals):
        for k in range(self.layersN):
            if k == 0:
                for i in range(len(inputVals)):
                    self.x[k][i] = inputVals[i]
            else:
                for i in range(len(self.z[k - 1])):
                    self.x[k][i] = self.z[k - 1][i]
            for i in range(len(self.weights[k])):
                y = 0.0

                for j in range(len(self.weights[k][0])):
                    y += self.weights[k][i][j] * self.x[k][j]

                # активация с помощью сигмоидальной функции

                self.z[k][i] = 1 / (1 + math.exp(-y))
                self.df[k][i] = self.z[k][i] * (1 - self.z[k][i])

                # активация с помощью гиперболического тангенса
                # self.z[k][i] = math.tanh(y)
                # self.df[k][i] = 1 - pow(self.z[k][i], 2)

                # активация с помощью ReLU
                # L[k].z[i] = y > 0 ? y: 0;
                # L[k].df[i] = y > 0 ? 1: 0;

        return self.z[self.layersN - 1]

    def backward(self, output):
        last = self.layersN - 1

        err = 0

        for i in range(len(output)):
            e = self.z[last][i] - output[i]
            self.deltas[last][i] = e * self.df[last][i]
            err += e * e / 2

        for k in range(last, 0, -1):
            for i in range(len(self.weights[k][0])):
                self.deltas[k - 1][i] = 0

                for j in range(len(self.weights[k])):
                    self.deltas[k - 1][i] += self.weights[k][j][i] * self.deltas[k][j]

                self.deltas[k - 1][i] *= self.df[k - 1][i]

        return err

    def updateWeights(self, alpha):
        for k in range(self.layersN):
            for i in range(len(self.weights[k])):
                for j in range(len(self.weights[k][0])):
                    self.weights[k][i][j] -= alpha * self.deltas[k][i] * self.x[k][j]

    def Train(self, X, Y, alpha, eps, epochs):
        epoch = 1

        error = 0

        for i in range(len(X)):
            self.feedForward(X[i])
            error = self.backward(Y[i])
            self.updateWeights(alpha)

        print(f"epoch: {epoch} error: {error}")

        epoch += 1

        while epoch <= epochs and error > eps:
            error = 0

            for i in range(len(X)):
                self.feedForward(X[i])
                error = self.backward(Y[i])
                self.updateWeights(alpha)

            print(f"epoch: {epoch} error: {error}")

            epoch += 1


uos = [68.978, 44.45, 48.7572, 85.8212, 27.8308, 81.9672]
kv = [8.13953, 14.4, 45, 18.75, 18.42105, 28.66667]
upss = [1018.12, 1630.77, 1130.442, 744.1041, 1952.095, 639.5673]
ilg = [1.56627, 4.03226, 4.03664, 7.076745, 7.519231, 4.483247]
islm = [4.33333, 4.16667, 2.45283, 2.65942, 4.546512, 3.031915]
isnm = [27.667, 10.3333, 5.981132, 3.586957, 5.930233, 6.510638]
liir = [5.1875, 2.0, 1.685722, 0.936436, 1.047228, 1.519742]
Y = [[1.0], [1.0], [0.0], [0.0]]

temp = []
X = []

y_arr = []

vals = [uos, kv, upss, ilg, islm, isnm, liir]

for i in range(7):
    for j in range(6):
        y_arr.append((vals[i][j] - min(vals[i])) / (max(vals[i]) - min(vals[i])))
    vals[i] = y_arr
    y_arr = []

for i in range(6):
    for j in range(7):
        temp.append(vals[j][i])
    X.append(temp)
    temp = []


testX = [X[4], X[5]]
X = [X[0], X[1], X[2], X[3]]


def run():
    net = Network([7, 7, 1])

    net.Train(X, Y, 0.5, 0.000001, 10000)

    testY = [[1.0],
             [0.0]]

    for i in range(2):
        output = net.feedForward(testX[i])
        print(f"X: {testX[i][0]}, Y: {testY[i][0]}, output: {output[0]}")


run()
