from MFIS_Classes import *
import MFIS_Read_Functions as lectura

import skfuzzy as skf
import numpy
from pathlib import Path
import copy
import matplotlib.pyplot as plt

# Constantes

FICHERO_APLICACIONES = Path('./Applications.txt')
FICHERO_INPUTVAR = Path('./InputVarSets.txt')
FICHERO_RESULTADOS = Path('./Resultados.txt')
FICHERO_RIESGOS = Path('./Risks.txt')
FICHERO_REGLAS = Path('./Rules.txt')

def escribir_resultado(archivo: Path, resultados: list[dict]):
    # Escribe el resultado en un fichero
    with open(archivo, "w") as outputFile:
        for application in resultados:
            string_de_escritura = f"{application['app_id']}  {application['resultado']}\n"
            outputFile.write(string_de_escritura)




def borrosificacion(aplicacion: Application, lista_varset: list[FuzzySet]) -> dict:
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

def calculo_de_consecuente(riesgos: dict[FuzzySet], reglas: list[Rule]) -> tuple[dict]:
    # Calculo de activaciones
    activacion_riskL = 0
    activacion_riskM = 0
    activacion_riskH = 0
    for regla in reglas:
        s = regla.consequent.split('=')
        tipo_riesgo = s[1]
        match tipo_riesgo:
            case 'LowR':
                activacion_riskL = max(regla.strength, activacion_riskL)
            case 'MediumR':
                activacion_riskM = max(regla.strength, activacion_riskM)
            case 'HighR':
                activacion_riskH = max(regla.strength, activacion_riskH)
    # Recorte de funciones
    riesgoL_ajustado = {
        "x" : riesgos['Risk=LowR'].x,
        "y" : numpy.clip(riesgos['Risk=LowR'].y, 0, activacion_riskL)
    }
    riesgoM_ajustado = {
        "x" : riesgos['Risk=MediumR'].x,
        "y" : numpy.clip(riesgos['Risk=MediumR'].y, 0, activacion_riskM)
    }
    riesgoL_ajustado = {
        "x" : riesgos['Risk=HighR'].x,
        "y" : numpy.clip(riesgos['Risk=HighR'].y, 0, activacion_riskH)
    }
    return (riesgoL_ajustado, riesgoM_ajustado, riesgoL_ajustado)

def composicion(funciones_riesgo: tuple[dict]) -> dict:
    # Agregacion
    # Nota: Asumo que todas las funciones de riesgo tienen el mismo rango de x (0, 100)
    funcion_agregada = {
        "x": funciones_riesgo[0]["x"],
        "y": numpy.maximum(funciones_riesgo[0], numpy.maximum(funciones_riesgo[1], funciones_riesgo[2]))
    } 
    return funcion_agregada

def desborrosificacion(x: numpy.ndarray | list | tuple, y: numpy.ndarray | list | tuple):
    return skf.centroid(x, y)

def imprimir_funcion(nombre: str, x: numpy.ndarray | list, y: numpy.ndarray | list, centroide: int) -> None:
    plt.plot(x, y)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(nombre)
    plt.figtext(0.5, 0.02, f'Centroide: {centroide}', ha='center')
    plt.show()

def main():
    aplicaciones: list[Application] = lectura.readApplicationsFile(FICHERO_APLICACIONES)
    inputvar: list[FuzzySet] = list(lectura.readFuzzySetsFile(FICHERO_INPUTVAR).values())
    reglas: list[Rule] = lectura.readRulesFile(FICHERO_REGLAS)
    riesgos: list[FuzzySet] = lectura.readRisksFile(FICHERO_RIESGOS, {})
    resultados: list[dict] = []
    for aplicacion in aplicaciones:
        aplicacion_borrosificada = borrosificacion(aplicacion, inputvar)
        reglas = evaluacion_de_reglas(aplicacion_borrosificada, reglas)
        funciones_ajustadas = calculo_de_consecuente(riesgos, reglas)
        funcion_agregada = composicion(funciones_ajustadas)
        centroide = desborrosificacion(funcion_agregada)
        resultado = {
            "app_id": aplicacion.app_id,
            "centroide": centroide
        }
        imprimir_funcion(aplicacion.app_id, funcion_agregada['x'], funcion_agregada['y'], centroide)
        resultados.append(resultado)
    escribir_resultado(FICHERO_RESULTADOS, resultados)

if __name__ == '__main__':
    main()