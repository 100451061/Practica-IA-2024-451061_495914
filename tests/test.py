#!/usr/bin/env python3
import sys
from pathlib import Path

# Añadimos la ruta de src/ al path
sys.path.append(str(Path(__file__).resolve().parent.parent / 'src'))

import unittest
from skfuzzy import control as ctrl
from codigo_fuente import *


class Test(unittest.TestCase):
    @staticmethod
    def helper_esperado(aplicacion: Application) -> float:
        list_set: dict[str, FuzzySet] = lectura.readFuzzySetsFile(FICHERO_INPUTVAR)
        procesadas = {}
        for set in list_set.values():
            if set.variable not in procesadas.keys():
                procesadas[set.variable] = ctrl.Antecedent(set.x, set.variable)
        for set in list_set.values():
            procesadas[set.variable][set.label] = set.y
        riesgos = lectura.readRisksFile(FICHERO_RIESGOS)
        for nombre, riesgo in riesgos.items():
            if riesgo.variable not in procesadas.keys():
                procesadas[riesgo.variable] = ctrl.Consequent(riesgo.x, riesgo.variable)
            procesadas[riesgo.variable][nombre] = riesgo.y
        reglas: dict[str, Rule] = lectura.readRulesFile(FICHERO_REGLAS)
        reglas_procesadas = {}
        for nombre, regla in reglas.items():
            consecuente = regla.consequent.split('=')
            antecedentes = None
            for antecedente in regla.antecedents:
                s = antecedente.split("=")
                if not antecedentes:
                    antecedentes = procesadas[s[0]][s[1]]
                else:
                    antecedentes &= procesadas[s[0]][s[1]]
            reglas_procesadas[nombre] = ctrl.Rule(antecedentes, procesadas[consecuente[0]][consecuente[1]])
        riesgo_ctrl = ctrl.ControlSystem(reglas_procesadas.values())
        riesgo_output = ctrl.ControlSystemSimulation(riesgo_ctrl)
        for datos in aplicacion.data:
            riesgo_output.input[datos[0]] = datos[1]
        riesgo_output.compute()
        return riesgo_output.output['Risk']

    def test(self):
        aplicaciones: dict = lectura.readApplicationsFile(FICHERO_APLICACIONES)
        inputvar: dict = lectura.readFuzzySetsFile(FICHERO_INPUTVAR)
        reglas: dict = lectura.readRulesFile(FICHERO_REGLAS)
        riesgos: dict = lectura.readRisksFile(FICHERO_RIESGOS)
        for aplicacion in aplicaciones.values():
            aplicacion_borrosificada = borrosificacion(aplicacion, inputvar)
            reglas = evaluacion_de_reglas(aplicacion_borrosificada, reglas)
            funciones_ajustadas = calculo_de_consecuente(riesgos, reglas)
            funcion_agregada = composicion(funciones_ajustadas)
            centroide = desborrosificacion(funcion_agregada["x"], funcion_agregada["y"])
            # Los resultados difieren en algunas centesimas a veces
            self.assertEqual(round(self.helper_esperado(aplicacion), 1), round(centroide, 1))


if __name__ == '__main__':
    unittest.main()
