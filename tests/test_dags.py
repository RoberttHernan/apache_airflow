from airflow.models.dagbag import DagBag


def test_all_dags_import_without_errors():
    dag_bag = DagBag(dag_folder="dags", include_examples=False)
    assert dag_bag.import_errors == {}


def test_example_dag_has_expected_tasks():
    dag_bag = DagBag(dag_folder="dags", include_examples=False)
    dag = dag_bag.get_dag("201700703_conceptos_basicos")
    assert dag is not None
    assert len(dag.tasks) == 6
