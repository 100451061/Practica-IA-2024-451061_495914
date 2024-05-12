import unittest
from Codigo_fuente import *
from MFIS_Classes import *
from MFIS_Read_Functions import *

class Test(unittest.TestCase):
    def test_borrosificacion(self):
        aplicacion = Application("0001", [])
        aplicacion.data = [
            ("Age", "35"),
            ("IncomeLevel", "82"),
            ("Assets", "38"),
            ("Amount", "8"),
            ("Job", "0"),
            ("History", "1")
        ]
        esperado = { 
            'app_id': '0001',
            'Age': {'Young': 0.5, 'Adult': 1.0, 'Elder': 0.0},
            'IncomeLevel': {'Low': 0.0, 'Med': 0.0, 'Hig': 1.0},
            'Assets': {'Scarce': 0.0, 'Moderate': 0.0, 'Abundant': 1.0},
            'Amount': {'Small': 0.0, 'Medium': 0.0, 'Big': 0.0, 'VeryBig': 1.0},
            'Job': {'Unstable': 1.0, 'Stable': 0.0},
            'History': {'Poor': 1.0, 'Standard': 0.0, 'Good': 0.0}
        } # No he comprobado si esto esta bien
        resultado = borrosificacion(aplicacion, list(readFuzzySetsFile(FICHERO_INPUTVAR).values()))
        self.assertEqual(esperado, resultado)

if __name__ == '__main__':
    unittest.main()