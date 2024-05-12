#!/usr/bin/env python3


class FuzzySet:
    def __init__(self, variable, label, x, y):
        self.variable = variable  # Nombre de la variable, ej. 'Age', 'IncomeLevel'
        self.label = label  # Etiqueta del conjunto borroso, ej. 'Young', 'High'
        self.x = x  # Rango de valores de x (universo de discurso)
        self.y = y  # Valores de membresía asociados a x

    def printSet(self):
        print("Variable:  ", self.variable)
        print("Label:     ", self.label)
        print("x coord:   ", self.x)
        print("y coord:   ", self.y)


class FuzzySetsDict(dict):
    def printFuzzySetsDict(self):
        for set_id, fuzzy_set in self.items():
            print("Set ID:    ", set_id)
            fuzzy_set.printSet()


class Rule:
    def __init__(self, rule_name, consequent, antecedents, strength=1.0):
        self.rule_name = rule_name  # Name of the rule
        self.consequent = consequent  # Consequent of the rule (only one set ID)
        self.antecedents = antecedents  # List of antecedents (set IDs)
        self.strength = strength  # Strength of the rule (used in rule evaluation)

    def printRule(self):
        print("Rule Name: ", self.rule_name)
        print("IF        ", self.antecedents)
        print("THEN      ", self.consequent)
        print("Strength: ", self.strength)


class RuleList(list):
    def printRuleList(self):
        for rule in self:
            rule.printRule()


class Application:
    def __init__(self, app_id, data):
        self.app_id = app_id  # Application identifier
        self.data = data  # List of (variable, value) pairs

    def printApplication(self):
        print("App ID: ", self.app_id)
        for var, value in self.data:
            print(f"{var} is {value}")
