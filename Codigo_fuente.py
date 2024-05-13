from MFIS_Classes import *
import MFIS_Read_Functions as lectura

import skfuzzy as skf
import numpy
from pathlib import Path
import copy

# Constantes

FICHERO_APLICACIONES = Path('./Applications.txt')
FICHERO_INPUTVAR = Path('./InputVarSets.txt')
FICHERO_RESULTADOS = Path('./Resultados.txt')
FICHERO_RIESGOS = Path('./Risks.txt')
FICHERO_REGLAS = Path('./Rules.txt')
VARIABLES_REGLAS = {
}

def escribir_resultado(archivo: Path, resultados: list[dict]):
    # Escribe el resultado en un fichero
    with open(archivo, "w") as outputFile:
        for application in resultados:
            string_de_escritura = f"{application['app_id']}  {application['resultado']}\n"
            outputFile.write(string_de_escritura)




def borrosificacion(aplicacion: Application, lista_varset = list[FuzzySet]) -> dict:
    aplicacion_borrosificada = {
        "app_id": aplicacion.app_id
    }
    # Itero por las variables de la aplicacion
    for variable, valor in aplicacion.data:
        aplicacion_borrosificada[variable] = {}
        # Busco las varset correspondientes
        for varset in lista_varset:
            if varset.variable == variable:
                aplicacion_borrosificada[variable][varset.label] = skf.interp_membership(varset.x, varset.y, valor)
    return aplicacion_borrosificada

def evaluacion_de_reglas(aplicacion_borrosificada: dict, reglas: list[Rule]) -> list[Rule]:
    for regla in reglas:
        valores_antecedentes = []
        for antecedente in regla.antecedents:
            s = antecedente.split('=')
            variable, conjunto = s[0], s[1]
            valores_antecedentes.append(aplicacion_borrosificada[variable][conjunto])
        regla.strength = min(valores_antecedentes)
    return reglas


def main():
    aplicaciones = lectura.readApplicationsFile(FICHERO_APLICACIONES)
    inputvar = list(lectura.readFuzzySetsFile(FICHERO_INPUTVAR).values())
    reglas = lectura.readRulesFile(FICHERO_RIESGOS)
    for aplicacion in aplicaciones:
        aplicacion_borrosificada = borrosificacion(aplicacion)

if __name__ == '__main__':
    main()