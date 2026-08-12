"""DAG de referencia para la actividad de Airflow de SS2."""

from __future__ import annotations

from datetime import datetime, timedelta

from airflow.decorators import dag, task
from airflow.exceptions import AirflowFailException
from airflow.operators.python import BranchPythonOperator
from airflow.operators.empty import EmptyOperator


DEFAULT_ARGS = {
    "owner": "fulano_mengano_20200000",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}


@dag(
    dag_id="fulano_mengano_20200000",
    description="TaskFlow, XCom, dependencias, branching y validacion",
    default_args=DEFAULT_ARGS,
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ss2", "ejemplo", "201700703"],
)
def conceptos_basicos():
    inicio = EmptyOperator(task_id="inicio")

    @task
    def crear_datos() -> list[int]:
        """El valor retornado se guarda automáticamente en XCom."""
        return [2, 4, 6, 8, 10]

    @task
    def calcular_promedio(valores: list[int]) -> float:
        if not valores:
            raise AirflowFailException("La lista no puede estar vacía")
        return sum(valores) / len(valores)

    def elegir_ruta(promedio: float) -> str:
        return "promedio_alto" if promedio >= 6 else "promedio_bajo"

    datos = crear_datos()
    promedio = calcular_promedio(datos)
    decidir = BranchPythonOperator(
        task_id="elegir_ruta",
        python_callable=elegir_ruta,
        op_kwargs={"promedio": promedio},
    )
    alto = EmptyOperator(task_id="promedio_alto")
    bajo = EmptyOperator(task_id="promedio_bajo")

    inicio >> datos
    promedio >> decidir >> [alto, bajo]


conceptos_basicos()
