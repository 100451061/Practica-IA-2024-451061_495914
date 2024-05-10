#!/usr/bin/env python3
import numpy as np
import skfuzzy as skf

from MFIS_Classes import *


class FuzzySet:
    def __init__(self):
        self.var = ""
        self.label = ""
        self.x = []
        self.y = []


class Rule:
    def __init__(self):
        self.ruleName = ""
        self.antecedent = []
        self.consequent = ""


class RuleList(list):
    def printRuleList(self):
        for rule in self:
            print(f"Rule Name: {rule.ruleName} - Antecedent: {rule.antecedent} - Consequent: {rule.consequent}")


class Application:
    def __init__(self):
        self.appId = ""
        self.data = []


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
    inputFile = open('Applications.txt', 'r')
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


def applyRules(rules, inputs):
    output = {}
    for rule in rules:
        match = True
        for antecedent in rule.antecedent:
            var, value = antecedent.split('=')
            print(f"Comparing input value: {inputs.get(var)} with rule condition: {value}")
            if inputs.get(var) != str(value):
                match = False
                break
        if match:
            output[rule.ruleName] = True
    return output


def process_applications(applications, rules):
    results = []
    for app in applications:
        inputs = {}  # Construir un diccionario de entradas para esta solicitud
        for data_item in app.data:
            inputs[data_item[0]] = data_item[1]

        matched_rules = applyRules(rules, inputs)  # Aplicar las reglas al conjunto de entradas

        # Agregar los resultados de esta solicitud a la lista de resultados
        results.append({
            'App ID': app.appId,
            'Matched Rules': matched_rules
        })
    return results


if __name__ == '__main__':
    # Leer las solicitudes del archivo Applications.txt
    applications = readApplicationsFile()

    # Cargar las reglas desde el archivo Rules.txt
    rules = readRulesFile('Rules.txt')

    # Procesar las solicitudes y obtener los resultados
    results = process_applications(applications, rules)

    # Escribir los resultados en un nuevo archivo
    with open('Results.txt', 'w') as f:
        for result in results:
            f.write(f"Application ID: {result['App ID']}\n")
            f.write("Matched Rules:\n")
            for rule_name, matched in result['Matched Rules'].items():
                if matched:
                    f.write(f"- Rule {rule_name}: Activated\n")
            f.write("\n")
