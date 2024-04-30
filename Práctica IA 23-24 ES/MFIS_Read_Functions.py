#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as skf
from skfuzzy import control as ctrl

from MFIS_Classes import *


def readFuzzySetsFile(fleName):
    """
    This function reads a file containing fuzzy set descriptions
    and returns a dictionary with all of them
    """
    fuzzySetsDict = FuzzySetsDict()  # dictionary to be returned
    inputFile = open(fleName, 'r')
    line = inputFile.readline()
    while line != '':
        fuzzySet = FuzzySet()  # just one fuzzy set
        elementsList = line.split(', ')
        setid = elementsList[0]
        var_label = setid.split('=')
        fuzzySet.var = var_label[0]
        fuzzySet.label = var_label[1]

        xmin = int(elementsList[1])
        xmax = int(elementsList[2])
        a = int(elementsList[3])
        b = int(elementsList[4])
        c = int(elementsList[5])
        d = int(elementsList[6])
        x = np.arange(xmin, xmax, 1)
        y = skf.trapmf(x, [a, b, c, d])
        fuzzySet.x = x
        fuzzySet.y = y
        fuzzySetsDict.update({setid: fuzzySet})

        line = inputFile.readline()
    inputFile.close()
    return fuzzySetsDict


def readRulesFile(filePath):
    inputFile = open(filePath, 'r')
    rules = RuleList()
    line = inputFile.readline()
    while line != '':
        rule = Rule()
        line = line.rstrip()
        elementsList = line.split(', ')
        rule.ruleName = elementsList[0]
        rule.consequent = elementsList[1]
        lhs = []
        for i in range(2, len(elementsList)):
            lhs.append(elementsList[i])
        rule.antecedent = lhs
        rules.append(rule)
        line = inputFile.readline()
    inputFile.close()
    return rules


def readApplicationsFile():
    inputFile = open('Files/Applications.txt', 'r')
    applicationList = []
    line = inputFile.readline()
    while line != '':
        elementsList = line.split(', ')
        app = Application()
        app.appId = elementsList[0]
        app.data = []
        for i in range(1, len(elementsList), 2):
            app.data.append([elementsList[i], int(elementsList[i + 1])])
        applicationList.append(app)
        line = inputFile.readline()
    inputFile.close()
    return applicationList


# Al invocar la función los valores de x me hacen muy grandes hasta 100
# Por lo tanto solo cojo un trozo de la función no sé si vale

def inputs2():
    Age = ctrl.Antecedent(np.arange(0, 101, 1), "Age")
    IncomeLevel = ctrl.Antecedent(np.arange(0, 151, 1), "IncomeLevel")
    Assets = ctrl.Antecedent(np.arange(0, 51, 1), "Assets")
    Amount = ctrl.Antecedent(np.arange(0, 9, 1), "Amount")
    Job = ctrl.Antecedent(np.arange(0, 6, 1), "Job")
    History = ctrl.Antecedent(np.arange(0, 7, 1), "History")
    # Tambien puedo lista=[] voy añadiendo los que no aparece en la lista y luego
    # ejecuto la parte de abajo ir dibujando la gráfica si me dan un fichero y
    # no sé los inputs

    """{'Age=Young': <MFIS_Classes.FuzzySet object at 0x000001EC34266F10>"""
    diccionario = readFuzzySetsFile("InputVarSets.txt")
    # Creo cada una de las gráficas
    for variables in diccionario.values():
        if variables.var == "Age":
            Age[str(variables.label)] = np.interp(Age.universe, variables.x, variables.y)
        if variables.var == "IncomeLevel":
            IncomeLevel[str(variables.label)] = np.interp(IncomeLevel.universe, variables.x, variables.y)
        if variables.var == "Assets":
            Assets[str(variables.label)] = np.interp(Assets.universe, variables.x, variables.y)
        if variables.var == "Amount":
            Amount[str(variables.label)] = np.interp(Amount.universe, variables.x, variables.y)
        if variables.var == "Job":
            Job[str(variables.label)] = np.interp(Job.universe, variables.x, variables.y)
        if variables.var == "History":
            History[str(variables.label)] = np.interp(History.universe, variables.x, variables.y)


def outputs2():
    diccionario = readFuzzySetsFile("Risks.txt")
    Risk = ctrl.Consequent(np.arange(0, 101, 1), "Risk")

    for variables in diccionario.values():
        Risk[str(variables.label)] = np.interp(Risk.universe, variables.x, variables.y)

    Risk.view()
    plt.show()


if __name__ == '__main__':
    # Cargar los conjuntos borrosos desde el archivo InputVarSets.txt
    # fuzzy_sets = readFuzzySetsFile('InputVarSets.txt')
    # print("Fuzzy Sets Loaded:")
    # fuzzy_sets.printFuzzySetsDict()

    # Cargar las reglas desde el archivo Rules.txt
    # rules = readRulesFile('Rules.txt')
    # print("Reglas cargadas:")
    # rules.printRuleList()

    inputs2()
    outputs2()
