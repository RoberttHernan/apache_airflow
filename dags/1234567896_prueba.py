"""Entrega de ejemplo del estudiante con carnet 123456789."""

from __future__ import annotations

from datetime import datetime

import pandas as pd
from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator


@dag(
    dag_id="123456789_analisis_pandas_segunda_vuelta",
    description="Calcula estadísticas sencillas con Pandas",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ss2", "estudiante", "123456789"],
)
def analisis_pandas():
    inicio = EmptyOperator(task_id="inicio")

    @task
    def calcular_estadisticas() -> dict[str, float]:
        notas = pd.Series([65, 72, 81, 90, 92], dtype="float64")
        return {
            "promedio": float(notas.mean()),
            "nota_maxima": float(notas.max()),
            "aprobados": float((notas >= 61).sum()),
        }

    @task
    def mostrar_resultado(resultado: dict[str, float]) -> None:
        print(f"Carnet: 123456789 | Estadísticas: {resultado}")

    estadisticas = calcular_estadisticas()
    fin = mostrar_resultado(estadisticas)
    inicio >> estadisticas >> fin


analisis_pandas()