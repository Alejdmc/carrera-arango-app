"""Reglas de lectura del corte 1.

Solo clasifican un valor. No corrigen el archivo RAW y no escriben STAGING.
El contrato completo (VIN de 17 con alfabeto restringido, voltaje entre 10 y 15,
kilometraje entre 0 y 999999) queda para el ETL de las semanas 4 y 5.
"""

from __future__ import annotations

import json

FECHAS_INVALIDAS = {"SIN_FECHA", "PENDIENTE", "", "nan"}
VIN_CENTINELA = {"SIN_CHASIS", "DUPLICADO_VIN", "nan"}


def es_fecha_invalida(valor) -> bool:
    """True si la fecha no sirve para el perfil de este corte."""
    texto = str(valor)
    return texto in FECHAS_INVALIDAS or "/" in texto


def es_kilometraje_invalido(valor) -> bool:
    """True si el texto trae 'Desconocido', 'km' o empieza por menos."""
    texto = str(valor)
    return "Desconocido" in texto or "km" in texto or texto.startswith("-")


def es_vin_invalido(valor) -> bool:
    """True si es un centinela o tiene menos de 17 caracteres.

    Un VIN de más de 17 caracteres no se marca aquí. Esa regla exacta
    pertenece al contrato y todavía no está aplicada.
    """
    texto = str(valor)
    return texto in VIN_CENTINELA or len(texto) < 17


def json_esta_corrupto(valor) -> bool:
    """True si el texto no es un JSON parseable."""
    if valor is None:
        return False
    try:
        json.loads(valor)
    except (TypeError, json.JSONDecodeError):
        return True
    return False
