import math
import pandas as pd
import numpy as np
import time
import random
import csv
import os

import SettingsRun
import SettingsTest


class NetworkTrained:
    weights = []  # матрицы весов слоя
    x = []  # вход слоя
    z = []  # активированный выход слоя
    df = []  # производная функции активации слоя

    layersN = 0  # число слоёв

    def __init__(self, sizes):
        self.layersN = len(sizes) - 1  # запоминаем число слоёв
        pathDir = f"{SettingsRun.folderName}/{SettingsRun.folderName} {SettingsRun.uniqCode}"
        self.errDF = pd.read_csv(f"{pathDir}/errDF.csv")
        weightsFile = open(f'{pathDir}/weights.csv')
        weightsReader = csv.reader(weightsFile, delimiter=',')
        for row in weightsReader:
            if row:
                tmpArr = []
                for i in row:
                    while '  ' in i:
                        i = i.replace('  ', ' ')
                    if i[1] == ' ':
                        i = i[:1] + i[2:]
                    if i[len(i) - 2] == ' ':
                        i = i[:len(i) - 2] + i[len(i) - 1:]
                    iStr = i.replace('[', '').replace(']', '').split(' ')
                    iFloat = np.asarray(iStr, dtype=float)
                    tmpArr.append(iFloat)
                self.weights.append(tmpArr)
        xFile = open(f'{pathDir}/x.csv')
        xReader = csv.reader(xFile, delimiter=',')
        for row in xReader:
            if row:
                row = np.asarray(row, dtype=float)
                self.x.append(row)
        zFile = open(f'{pathDir}/z.csv')
        zReader = csv.reader(zFile, delimiter=',')
        for row in zReader:
            if row:
                row = np.asarray(row, dtype=float)
                self.z.append(row)
        dfFile = open(f'{pathDir}/df.csv')
        dfReader = csv.reader(dfFile, delimiter=',')
        for row in dfReader:
            if row:
                row = np.asarray(row, dtype=float)
                self.df.append(row)

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
                if SettingsRun.ActFun == 0:
                    self.z[k][i] = 1 / (1 + math.exp(-y))
                    self.df[k][i] = self.z[k][i] * (1 - self.z[k][i])
                elif SettingsRun.ActFun == 1:
                    self.z[k][i] = math.tanh(y)
                    self.df[k][i] = 1 - pow(self.z[k][i], 2)
                elif SettingsRun.ActFun == 2:
                    self.z[k][i] = y if y > 0 else 0
                    self.df[k][i] = 1 if y > 0 else 0
        return self.z[self.layersN - 1]


class Network:
    weights = []  # матрицы весов слоя
    x = []  # вход слоя
    z = []  # активированный выход слоя
    df = []  # производная функции активации слоя
    deltas = []  # дельты ошибки на каждом слое
    errDF = []
    layersN = 0  # число слоёв

    def __init__(self, sizes):
        self.layersN = len(sizes) - 1  # запоминаем число слоёв
        self.errDF = pd.DataFrame()

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

                if SettingsTest.ActFun == 0:
                    self.z[k][i] = 1 / (1 + math.exp(-y))
                    self.df[k][i] = self.z[k][i] * (1 - self.z[k][i])
                elif SettingsTest.ActFun == 1:
                    self.z[k][i] = math.tanh(y)
                    self.df[k][i] = 1 - pow(self.z[k][i], 2)
                elif SettingsTest.ActFun == 2:
                    self.z[k][i] = y if y > 0 else 0
                    self.df[k][i] = 1 if y > 0 else 0

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

        self.errDF = self.errDF._append({'epoch': epoch, 'error': error}, ignore_index=True)

        epoch += 1

        while epoch <= epochs and error > eps:
            error = 0

            for i in range(len(X)):
                self.feedForward(X[i])
                error = self.backward(Y[i])
                self.updateWeights(alpha)

            self.errDF = self.errDF._append({'epoch': epoch, 'error': error}, ignore_index=True)

            epoch += 1


def reading():
    df = pd.read_excel('newData.xlsx', dtype=float).round(5)

    temp = []
    resX = []
    resY = []
    X = []
    Y = []

    y_arr = []

    vals = [df['imt'].tolist(), df['choles'].tolist(), df['HDL'].tolist(), df['LDL'].tolist(), df['trigl'].tolist(),
            df['ather'].tolist()]

    for i in range(6):
        for j in range(len(df['imt'].tolist())):
            y_arr.append((vals[i][j] - min(vals[i])) / (max(vals[i]) - min(vals[i])))
        vals[i] = y_arr
        y_arr = []

    for i in range(len(df['imt'].tolist())):
        for j in range(6):
            temp.append(vals[j][i])
        resX.append(temp)
        temp = []

    for i in range(len(df['res'].tolist())):
        if df['res'].tolist()[i] == 3.0:
            resY.append([1.0])
        else:
            resY.append([0.0])

    for i in range(len(resX) - 3):
        X.append(resX[i])
        Y.append(resY[i])
    return X, Y, resX


def train(net, X, Y, alpha, eps, epochs):
    timing = time.time()
    net.Train(X, Y, alpha, eps, epochs)
    print((time.time() - timing).__round__(3))


def result(net):
    return net.errDF


def run(num, net, resX):
    output = net.feedForward(resX[num])
    if (output[0] * 100).round(2) >= 90.0:
        return 1, (output[0] * 100).round(2)
    else:
        return 0, (output[0] * 100).round(2)


# def runHand(inpX):
#     output = net.feedForward(inpX)
#     if (output[0] * 100).round(2) >= 90.0:
#         return 1, (output[0] * 100).round(2)
#     else:
#         return 0, (output[0] * 100).round(2)


def testRun(net2):
    weights = net2.weights
    id = random.randint(1, 100000000)
    NSCount = len(SettingsTest.NS) - 3
    NSInType = SettingsTest.NS[1]
    os.mkdir(f"[6, {NSInType}^{NSCount}, 1] ActFun = {SettingsTest.ActFun} {id}")
    with open(f"[6, {NSInType}^{NSCount}, 1] ActFun = {SettingsTest.ActFun} {id}/weights.csv", "w+") as my_csv:
        newWeights = csv.writer(my_csv, delimiter=',')
        newWeights.writerows(weights)
    with open(f"[6, {NSInType}^{NSCount}, 1] ActFun = {SettingsTest.ActFun} {id}/x.csv", "w+") as my_csv:
        newX = csv.writer(my_csv, delimiter=',')
        newX.writerows(net2.x)
    with open(f"[6, {NSInType}^{NSCount}, 1] ActFun = {SettingsTest.ActFun} {id}/z.csv", "w+") as my_csv:
        newZ = csv.writer(my_csv, delimiter=',')
        newZ.writerows(net2.z)
    with open(f"[6, {NSInType}^{NSCount}, 1] ActFun = {SettingsTest.ActFun} {id}/df.csv", "w+") as my_csv:
        newDf = csv.writer(my_csv, delimiter=',')
        newDf.writerows(net2.df)
    net2.errDF.to_csv(f'[6, {NSInType}^{NSCount}, 1] ActFun = {SettingsTest.ActFun} {id}/errDF.csv', index=False)
    testFile = open(f'[6, {NSInType}^{NSCount}, 1] ActFun = {SettingsTest.ActFun} {id}/[6, {NSInType}^{NSCount}, 1] '
                    f'ActFun = {SettingsTest.ActFun} {id}.txt', "a+")
    testFile.write(f'weigths: {weights} \n {SettingsTest.alpha}, \n {SettingsTest.eps}, \n {SettingsTest.epochs}')
    print(f"{net2.errDF['error'][len(net2.errDF) - 1]}")
