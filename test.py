import unittest
from Codigo_fuente import *
from MFIS_Classes import *
from MFIS_Read_Functions import *

class Test(unittest.TestCase):
    def helper_borrosificacion(self, aplicacion: Application, esperado: dict):
        resultado = borrosificacion(aplicacion, readFuzzySetsFile(FICHERO_INPUTVAR))
        self.assertEqual(esperado, resultado)
        return resultado
    
    def helper_evaluacion_reglas(self, aplicacion_borrosificada: dict, esperado: dict):
        reglas = lectura.readRulesFile(FICHERO_REGLAS)
        reglas = evaluacion_de_reglas(aplicacion_borrosificada, reglas)
        resultado = {}
        for i in reglas.values():
            resultado[i.rule_name] = i.strength
        for regla in reglas.values():
            try:
                if regla.rule_name in esperado.keys():
                    self.assertEqual(resultado[regla.rule_name], esperado[regla.rule_name])
                else:
                    self.assertEqual(resultado[regla.rule_name], 0)
            except AssertionError as e:
                print(f"{regla.rule_name}")
                raise 
        return reglas

    def test(self):
        datos_testeo = {
            "0001": { 
                "iniciales": [
                    ("Age", "35"),
                    ("IncomeLevel", "82"),
                    ("Assets", "38"),
                    ("Amount", "8"),
                    ("Job", "0"),
                    ("History", "1")
                    ],
                "borrosificado": { 
                    'app_id': '0001',
                    'Age': {'Young': 0.5, 'Adult': 1.0, 'Elder': 0.0},
                    'IncomeLevel': {'Low': 0.0, 'Med': 0.0, 'Hig': 1.0},
                    'Assets': {'Scarce': 0.0, 'Moderate': 0.0, 'Abundant': 1.0},
                    'Amount': {'Small': 0.0, 'Medium': 0.0, 'Big': 0.0, 'VeryBig': 1.0},
                    'Job': {'Unstable': 1.0, 'Stable': 0.0},
                    'History': {'Poor': 1.0, 'Standard': 0.0, 'Good': 0.0}
                },
                "reglas": {"Rule24": 0.5,
                           "Rule25": 0.5,
                           "Rule26": 0.5}
            }
        }
        for id, datos in datos_testeo.items():
            aplicacion = Application(id, datos["iniciales"])
            borrosificado = self.helper_borrosificacion(aplicacion, datos["borrosificado"])
            reglas = self.helper_evaluacion_reglas(borrosificado, datos["reglas"])



if __name__ == '__main__':
    unittest.main()