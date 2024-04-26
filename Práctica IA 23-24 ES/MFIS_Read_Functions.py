#!/usr/bin/env python3
import numpy as np
import skfuzzy as skf

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


if __name__ == '__main__':
    # Cargar los conjuntos borrosos desde el archivo InputVarSets.txt
    fuzzy_sets = readFuzzySetsFile('InputVarSets.txt')
    print("Fuzzy Sets Loaded:")
    fuzzy_sets.printFuzzySetsDict()

    # Cargar las reglas desde el archivo Rules.txt
    rules = readRulesFile('Rules.txt')
    print("Reglas cargadas:")
    rules.printRuleList()
