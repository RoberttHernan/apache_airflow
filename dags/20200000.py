"""DAG estudiantil migrado a la interfaz pública de Airflow 3."""

from __future__ import annotations

from datetime import datetime, timedelta

from airflow.sdk import dag, task


@dag(
    dag_id="fulano_mengano_20200000",
    description="TaskFlow, XCom, dependencias y branching",
    default_args={
        "owner": "fulano_mengano_20200000",
        "retries": 1,
        "retry_delay": timedelta(minutes=1),
    },
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ss2", "estudiante", "20200000"],
)
def conceptos_basicos():
    @task
    def inicio() -> None:
        print("Iniciando DAG")

    @task
    def crear_datos() -> list[int]:
        return [2, 4, 6, 8, 10]

    @task
    def calcular_promedio(valores: list[int]) -> float:
        if not valores:
            raise ValueError("La lista no puede estar vacía")
        return sum(valores) / len(valores)

    @task.branch
    def elegir_ruta(promedio: float) -> str:
        return "promedio_alto" if promedio >= 6 else "promedio_bajo"

    @task
    def promedio_alto() -> None:
        print("Promedio alto")

    @task
    def promedio_bajo() -> None:
        print("Promedio bajo")

    comienzo = inicio()
    datos = crear_datos()
    promedio = calcular_promedio(datos)
    decidir = elegir_ruta(promedio)
    alto = promedio_alto()
    bajo = promedio_bajo()
    comienzo >> datos
    promedio >> decidir >> [alto, bajo]


conceptos_basicos()
