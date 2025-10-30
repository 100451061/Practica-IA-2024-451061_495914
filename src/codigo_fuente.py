from pathlib import Path

import matplotlib.pyplot as plt
import numpy
import skfuzzy as skf

import MFIS_Read_Functions_Modificado as lectura
from MFIS_Classes_Modificado import *

# Directorio base
BASE_DIR = Path(__file__).resolve().parent.parent


# Constantes

# Archivos de datos dentro de /data
FICHERO_APLICACIONES = BASE_DIR / 'data' / 'Applications.txt'
FICHERO_INPUTVAR = BASE_DIR / 'data' / 'InputVarSets.txt'
FICHERO_RESULTADOS = BASE_DIR / 'data' / 'Resultados.txt'
FICHERO_RIESGOS = BASE_DIR / 'data' / 'Risks.txt'
FICHERO_REGLAS = BASE_DIR / 'data' / 'Rules.txt'

# Carpeta para los gráficos
DIRECTORIO_PLOTS = BASE_DIR / 'plots'


def escribir_resultado(archivo: Path, resultados: list[dict]):
    # Escribe el resultado en un fichero
    with open(archivo, "w") as outputFile:
        for app_id, centroide in resultados.items():
            string_de_escritura = f"{app_id}  {centroide}\n"
            outputFile.write(string_de_escritura)


def borrosificacion(aplicacion: Application, lista_varset: dict) -> dict:
    aplicacion_borrosificada = {"app_id": aplicacion.app_id}
    # Itero por las variables de la aplicacion
    for variable, valor in aplicacion.data:
        aplicacion_borrosificada[variable] = {}
        # Busco las varset correspondientes
        for varset in lista_varset.values():
            if varset.variable == variable:
                aplicacion_borrosificada[variable][varset.label] = skf.interp_membership(varset.x, varset.y, valor)
    return aplicacion_borrosificada


def evaluacion_de_reglas(aplicacion_borrosificada: dict, reglas: dict) -> dict:
    for regla in reglas.values():
        valores_antecedentes = []
        for antecedente in regla.antecedents:
            s = antecedente.split('=')
            variable, conjunto = s[0], s[1]
            valores_antecedentes.append(aplicacion_borrosificada[variable][conjunto])
        regla.strength = min(valores_antecedentes)
    return reglas


def calculo_de_consecuente(riesgos: dict, reglas: dict) -> tuple[dict]:
    # Calculo de activaciones
    activacion_riskL = 0
    activacion_riskM = 0
    activacion_riskH = 0
    for regla in reglas.values():
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
    riesgoL_ajustado = {"x": riesgos['LowR'].x,
                        "y": numpy.clip(riesgos['LowR'].y, 0, activacion_riskL)}
    riesgoM_ajustado = {"x": riesgos['MediumR'].x,
                        "y": numpy.clip(riesgos['MediumR'].y, 0, activacion_riskM)}
    riesgoH_ajustado = {"x": riesgos['HighR'].x,
                        "y": numpy.clip(riesgos['HighR'].y, 0, activacion_riskH)}
    return (riesgoL_ajustado, riesgoM_ajustado, riesgoH_ajustado)


def composicion(funciones_riesgo: tuple[dict]) -> dict:
    # Agregacion
    # Nota: Asumo que todas las funciones de riesgo tienen el mismo rango de x (0, 100)
    funcion_agregada = {"x": funciones_riesgo[0]["x"],
                        "y": numpy.maximum(funciones_riesgo[0]["y"], numpy.maximum(funciones_riesgo[1]["y"], funciones_riesgo[2]["y"]))}
    return funcion_agregada


def desborrosificacion(x: numpy.ndarray | list | tuple, y: numpy.ndarray | list | tuple):
    return skf.centroid(x, y)


def imprimir_funcion(nombre: str, x: numpy.ndarray | list, y: numpy.ndarray | list, centroide: int) -> None:
    plt.clf()
    plt.plot(x, y)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(nombre)
    plt.figtext(0.5, 0.0, f'Centroide: {centroide}', ha='center')
    if not DIRECTORIO_PLOTS.exists():
        DIRECTORIO_PLOTS.mkdir(exist_ok=True)
    plt.savefig(DIRECTORIO_PLOTS / (nombre + '.svg'), format='svg')


def main():
    aplicaciones: dict = lectura.readApplicationsFile(FICHERO_APLICACIONES)
    inputvar: dict = lectura.readFuzzySetsFile(FICHERO_INPUTVAR)
    reglas: dict = lectura.readRulesFile(FICHERO_REGLAS)
    riesgos: dict = lectura.readRisksFile(FICHERO_RIESGOS)
    resultados: dict = {}
    for aplicacion in aplicaciones.values():
        aplicacion_borrosificada = borrosificacion(aplicacion, inputvar)
        reglas = evaluacion_de_reglas(aplicacion_borrosificada, reglas)
        funciones_ajustadas = calculo_de_consecuente(riesgos, reglas)
        funcion_agregada = composicion(funciones_ajustadas)
        centroide = desborrosificacion(funcion_agregada["x"], funcion_agregada["y"])
        resultados[aplicacion.app_id] = centroide
        imprimir_funcion(aplicacion.app_id, funcion_agregada['x'], funcion_agregada['y'], centroide)
    escribir_resultado(FICHERO_RESULTADOS, resultados)


if __name__ == '__main__':
    main()
