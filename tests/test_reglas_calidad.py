"""Casos del corte 1: uno normal y varios límite. No leen el RAW."""

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from reglas_calidad import (  # noqa: E402
    es_fecha_invalida,
    es_kilometraje_invalido,
    es_vin_invalido,
    json_esta_corrupto,
)


class TestReglasCalidad(unittest.TestCase):
    def test_fecha_normal(self):
        self.assertFalse(es_fecha_invalida("2025-08-20"))

    def test_fecha_con_barras_o_centinela(self):
        self.assertTrue(es_fecha_invalida("20/08/2025"))
        self.assertTrue(es_fecha_invalida("SIN_FECHA"))

    def test_kilometraje_normal_y_negativo(self):
        self.assertFalse(es_kilometraje_invalido("434723"))
        self.assertTrue(es_kilometraje_invalido("-438049"))
        self.assertTrue(es_kilometraje_invalido("Desconocido"))

    def test_vin_corto_y_de_largo_suficiente(self):
        self.assertFalse(es_vin_invalido("50R35SSC07K920VRZ"))
        self.assertTrue(es_vin_invalido("SIN_CHASIS"))
        self.assertTrue(es_vin_invalido("ABC123"))

    def test_json_valido_y_truncado(self):
        self.assertFalse(json_esta_corrupto('{"datosGenerales": {"chasis": "X"}}'))
        self.assertTrue(json_esta_corrupto('{"datosGenerales": {'))
        self.assertFalse(json_esta_corrupto(None))


if __name__ == "__main__":
    unittest.main()
