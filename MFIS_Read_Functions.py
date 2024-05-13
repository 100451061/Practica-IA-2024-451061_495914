from pathlib import Path

import numpy as np
import skfuzzy as fuzz

from MFIS_Classes import FuzzySet, Rule, Application


def readFuzzySetsFile(fileName: str | Path) -> dict[str, FuzzySet]:
    fuzzySetsDict = {}
    with open(fileName, 'r') as file:
        for line in file:
            elements = line.strip().split(', ')
            set_id = elements[0]
            var_label = set_id.split('=')
            variable = var_label[0]
            label = var_label[1]
            xmin = int(elements[1])
            xmax = int(elements[2])
            points = list(map(int, elements[3:]))
            x = np.arange(xmin, xmax + 1)
            if len(points) == 3:
                y = fuzz.trimf(x, points)
            elif len(points) == 4:
                y = fuzz.trapmf(x, points)
            else:
                continue  # o manejar error
            fuzzySet = FuzzySet(variable, label, x, y)
            fuzzySetsDict[set_id] = fuzzySet
    return fuzzySetsDict


def readRisksFile(fileName: str | Path) -> dict[str, FuzzySet]:
    variables = {}
    with open(fileName, 'r') as file:
        for line in file:
            parts = line.strip().split(', ')
            risk_name = parts[0].split('=')
            xmin = int(parts[1])
            xmax = int(parts[2])
            points = list(map(int, parts[3:]))
            x = np.arange(xmin, xmax + 1)
            y = fuzz.trapmf(x, points)
            variables[risk_name[1]] = FuzzySet(risk_name[0], risk_name[1], x, y)  # Ajustado según la nueva definición
    return variables


def readRulesFile(fileName: str | Path) -> dict[str, Rule]:
    rules = {}
    with open(fileName, 'r') as file:
        for line in file:
            elements = line.strip().split(', ')
            rule_name = elements[0]
            consequent = elements[1]
            antecedents = elements[2:]
            rule = Rule(rule_name, consequent, antecedents)
            rules[rule_name] = rule
    return rules


def readApplicationsFile(fileName: str | Path) -> dict[str, Application]:
    applications = {}
    with open(fileName, 'r') as file:
        for line in file:
            elements = line.strip().split(', ')
            app_id = elements[0]
            data = [(elements[i], int(elements[i + 1])) for i in range(1, len(elements), 2)]
            application = Application(app_id, data)
            applications[app_id] = application
    return applications
