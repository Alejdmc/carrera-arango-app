# Capa RAW — Datos originales (INMUTABLE)

Este directorio almacena la **fuente original** del proyecto de datos.

## Archivo

- `dataset_sucio_formularios_vehiculos_carrera_arango.csv`

## Reglas

1. **No editar** este archivo manualmente.
2. **No sobrescribir** este archivo.
3. Toda transformación va a `../staging/`.
4. El perfilamiento se ejecuta con `scripts/profile_raw_dataset.py` en modo lectura.

## Origen simulado

El archivo simula una exportación desordenada de formularios de ingreso y salida de Carrera Arango SAS, con errores de calidad puestos a propósito para el ejercicio. En este corte no se regenera ni se edita.
