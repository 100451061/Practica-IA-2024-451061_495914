import skfuzzy as fuzz

import MFIS_Read_Functions as read_funcs


def main():
    # Cargar las variables generales
    variables = read_funcs.readFuzzySetsFile('InputVarSets.txt')

    # Cargar definiciones de riesgo
    variables = read_funcs.readRisksFile('Risks.txt', variables)

    print("Variables cargadas:", variables.keys())  # Verificar las claves cargadas

    # Continuar con el proceso...


def fuzzify(inputs, variables):
    fuzzified = {}
    for var, value in inputs:
        if var in variables:
            x = variables[var].x
            y = variables[var].y
            fuzzified[var] = fuzz.interp_membership(x, y, value)
    return fuzzified


def evaluate_rules(fuzzified_inputs, rules):
    output_sets = {}
    for rule in rules:
        min_degree = min(fuzzified_inputs.get(antecedent, 0) for antecedent in rule.antecedents)
        consequent_var = rule.consequent.split('=')[1]
        if consequent_var not in output_sets:
            output_sets[consequent_var] = []
        output_sets[consequent_var].append(min_degree)
    return output_sets


def aggregate_outputs(output_sets):
    aggregated = {}
    for risk_level, memberships in output_sets.items():
        aggregated[risk_level] = max(memberships)
    return aggregated


def defuzzify(aggregated_outputs, variables):
    risk_levels = {}
    for key, val in aggregated_outputs.items():
        if key in variables:
            risk_levels[key] = fuzz.defuzz(variables[key].x, variables[key].y, 'centroid')
        else:
            print(f"Advertencia: clave '{key}' no encontrada en variables, no se puede defuzzificar.")
    return risk_levels


def process_application(app, variables, rules):
    inputs = [(data[0], data[1]) for data in app.data]
    fuzzified_inputs = fuzzify(inputs, variables)
    output_sets = evaluate_rules(fuzzified_inputs, rules)
    aggregated_outputs = aggregate_outputs(output_sets)
    risk_levels = defuzzify(aggregated_outputs, variables)
    return risk_levels


if __name__ == "__main__":
    main()
