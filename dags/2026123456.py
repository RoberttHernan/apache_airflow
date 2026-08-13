"""DAG de referencia compatible con la interfaz pública de Airflow 3."""

from __future__ import annotations

from datetime import datetime, timedelta

from airflow.sdk import dag, task


DEFAULT_ARGS = {
    "owner": "20260000",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}


@dag(
    dag_id="20260000",
    description="TaskFlow, XCom, dependencias, branching y validación",
    default_args=DEFAULT_ARGS,
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ss2", "ejemplo", "201700703"],
)
def conceptos_basicos():
    @task
    def inicio() -> None:
        print("Iniciando DAG de ejemplo")

    @task
    def crear_datos() -> list[int]:
        """El retorno se almacena automáticamente como XCom."""
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
        print("El promedio es alto")

    @task
    def promedio_bajo() -> None:
        print("El promedio es bajo")

    comienzo = inicio()
    datos = crear_datos()
    promedio = calcular_promedio(datos)
    decidir = elegir_ruta(promedio)
    alto = promedio_alto()
    bajo = promedio_bajo()

    comienzo >> datos
    promedio >> decidir >> [alto, bajo]


conceptos_basicos()
