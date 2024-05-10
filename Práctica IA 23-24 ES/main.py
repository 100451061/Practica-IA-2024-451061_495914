import numpy as np
import skfuzzy as fuzz

import MFIS_Read_Functions as read_funcs  # Asegúrate de que el nombre del módulo sea correcto


def processApplication(app, inputFuzzySets, outputFuzzySets, rules):
    # Paso 1: Fuzzificación
    fuzzified_inputs = fuzzify(app, inputFuzzySets)

    # Paso 2: Inferencia
    # Inicializa un arreglo para los resultados de salida basado en el rango x del universo de salida
    x_range = np.linspace(0, 100, max(len(fs.x) for fs in outputFuzzySets.values()))
    app_output = np.zeros_like(x_range)

    for r in rules:
        # 2.1: Calcula la fuerza del antecedente
        antecedent_strength = evaluateAntecedent(r, fuzzified_inputs)
        # 2.2: Recorta el consecuente
        clipped_consequent = clipConsequent(r, outputFuzzySets, antecedent_strength, x_range)
        # 2.3: Acumula la salida
        app_output = np.fmax(app_output, clipped_consequent)  # Acumulación usando el máximo

    # Paso 3: Defuzzificación
    centroid = fuzz.centroid(x_range, app_output)
    return centroid


# Implementa las funciones de ayuda que usan tus datos específicos
def fuzzify(app, inputFuzzySets):
    # Esta función asume que `app` tiene un atributo `data` que es una lista de tuplas (variable, valor)
    fuzzified = {}
    for variable, value in app.data:
        if variable in inputFuzzySets:
            fs = inputFuzzySets[variable]
            # Asumiendo que 'x' y 'y' son arrays en FuzzySet que representan el universo y la función de membresía, respectivamente
            fuzzified[variable] = fuzz.interp_membership(fs.x, fs.y, value)
    return fuzzified


def evaluateAntecedent(rule, fuzzified_inputs):
    # Retorna la fuerza del antecedente basada en la entrada fuzzificada y la regla
    return 0.5


def clipConsequent(rule, outputFuzzySets, strength, x_range):
    # Asegúrate de que la operación clip use el rango x adecuado
    fuzzy_set = outputFuzzySets[rule.consequent]
    # Interpola el y original para que coincida con x_range si es necesario
    interpolated_y = np.interp(x_range, fuzzy_set.x, fuzzy_set.y)
    clipped_consequent = np.clip(interpolated_y, 0, strength)
    return clipped_consequent


def main():
    # Lee los archivos necesarios utilizando funciones del módulo importado
    inputFuzzySets = read_funcs.readFuzzySetsFile("InputVarSets.txt")
    outputFuzzySets = read_funcs.readFuzzySetsFile("Risks.txt")
    rules = read_funcs.readRulesFile('Rules.txt')
    applications = read_funcs.readApplicationsFile('Applications.txt')

    # Procesa todas las aplicaciones y escribe los resultados en un archivo
    with open("Results.txt", "w") as outputFile:
        for application in applications:
            centroid = processApplication(application, inputFuzzySets, outputFuzzySets, rules)
            outputFile.write(application.app_id + " " + str(centroid) + "\n")


if __name__ == "__main__":
    main()
