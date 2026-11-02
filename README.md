# Carrera Arango App — Corte 1, semana 3

Avance del proyecto integrador para los formularios de ingreso y salida de Carrera Arango SAS. Esta carpeta no es el producto terminado del semestre.

En este corte el código solo lee el RAW y escribe un diagnóstico. No limpia datos y no llena `data/staging/`.

## Estructura

```
carrera-arango-app/
├── data/
│   ├── raw/          # inmutable
│   └── staging/      # vacía hasta las semanas 4 y 5
├── entregables/
│   └── diagnostico_raw_perfilamiento.json
├── scripts/
│   ├── reglas_calidad.py
│   └── profile_raw_dataset.py
├── tests/
│   └── test_reglas_calidad.py
└── README.md
```

## Regla de la capa RAW

El archivo `data/raw/dataset_sucio_formularios_vehiculos_carrera_arango.csv` no se edita. El README de esa carpeta lo describe como una exportación simulada, con errores de calidad puestos a propósito para el ejercicio.

## Cómo ejecutarlo

Desde esta carpeta:

```bash
python3 -m unittest tests/test_reglas_calidad.py
python3 scripts/profile_raw_dataset.py
```

Hace falta Python 3 y pandas (`requirements.txt`). El perfilador imprime el diagnóstico y lo guarda en `entregables/diagnostico_raw_perfilamiento.json`.

## Qué sigue

Semanas 4 y 5: ETL hacia STAGING, archivo de rechazados y las reglas del contrato que este perfilador todavía no aplica (VIN de 17 caracteres con alfabeto restringido, rango de kilometraje y rango de voltaje).
