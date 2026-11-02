# Capa STAGING / SILVER — Datos en transformación

Directorio reservado para las **próximas semanas** del proyecto (semanas 4 y 5).

Aquí se almacenarán:

- Archivos CSV/Parquet limpios después del ETL.
- Registros rechazados o en cuarentena (`rejected/`).
- Logs de transformación.

## Estado actual

Vacío — pendiente de implementar pipeline de limpieza a partir del RAW.

## Entrada esperada

`../raw/dataset_sucio_formularios_vehiculos_carrera_arango.csv`

## Salida esperada (semana 4+)

- `formularios_staging_limpio.csv`
- `formularios_rechazados.csv`
- `transform_log.json`
