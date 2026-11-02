#!/usr/bin/env python3
"""Perfilamiento básico del archivo RAW.

Lee data/raw y escribe el diagnóstico en entregables/.
No modifica el CSV original y no llena data/staging/.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from reglas_calidad import (
    es_fecha_invalida,
    es_kilometraje_invalido,
    es_vin_invalido,
    json_esta_corrupto,
)

BASE = Path(__file__).resolve().parents[1]
RAW_PATH = BASE / "data" / "raw" / "dataset_sucio_formularios_vehiculos_carrera_arango.csv"
OUT_PATH = BASE / "entregables" / "diagnostico_raw_perfilamiento.json"


def construir_reporte(df: pd.DataFrame, tamano_mb: float, nombre_archivo: str) -> dict:
    nulos = {
        columna: round(df[columna].isna().mean() * 100, 2)
        for columna in df.columns[:12]
    }
    fechas_invalidas = df["fecha_ingreso"].map(es_fecha_invalida)
    km_invalido = df["kilometraje"].map(es_kilometraje_invalido)
    vin_invalido = df["chasis_vin"].map(es_vin_invalido)

    muestra_json = df["data_json_supabase"].dropna().head(2000)
    corruptos = sum(1 for valor in muestra_json if json_esta_corrupto(valor))
    base_json = min(2000, int(muestra_json.shape[0]))

    return {
        "archivo": nombre_archivo,
        "registros": int(len(df)),
        "columnas": int(len(df.columns)),
        "tamano_mb": tamano_mb,
        "nulos_por_columna_pct": nulos,
        "fecha_ingreso_invalida_pct": round(float(fechas_invalidas.mean()) * 100, 2),
        "kilometraje_invalido_pct": round(float(km_invalido.mean()) * 100, 2),
        "chasis_vin_invalido_pct": round(float(vin_invalido.mean()) * 100, 2),
        "id_registro_duplicados": int(df["id_registro"].duplicated(keep=False).sum()),
        "tipo_formulario_distribucion": df["tipo_formulario"].value_counts().head(10).to_dict(),
        "ciudad_top_10": df["ciudad"].value_counts().head(10).to_dict(),
        "marca_distribucion": df["marca"].value_counts().to_dict(),
        "json_corrupto_muestra_pct": round(corruptos / base_json * 100, 2) if base_json else 0.0,
    }


def main() -> None:
    df = pd.read_csv(RAW_PATH, low_memory=False)
    tamano_mb = round(RAW_PATH.stat().st_size / (1024 * 1024), 2)
    reporte = construir_reporte(df, tamano_mb, RAW_PATH.name)
    OUT_PATH.write_text(json.dumps(reporte, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(reporte, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
