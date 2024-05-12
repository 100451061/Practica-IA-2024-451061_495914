from MFIS_Classes import *
import MFIS_Read_Functions as lectura

import skfuzzy as skf
import numpy
from pathlib import Path

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

def main():
    aplicaciones = lectura.readApplicationsFile(FICHERO_APLICACIONES)
    inputvar = list(lectura.readFuzzySetsFile(FICHERO_INPUTVAR).values())
    reglas = lectura.readRulesFile(FICHERO_RIESGOS)
    print(inputvar)
    for aplicacion in aplicaciones:
        try:
            aplicacion_borrosificada = borrosificacion(aplicacion)
        except:
            continue

if __name__ == '__main__':
    main()