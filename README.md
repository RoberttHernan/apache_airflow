# Laboratorio colaborativo de Apache Airflow

Repositorio para la dinámica de la semana 4 de Seminario de Sistemas 2. Cada
estudiante propone un DAG mediante un pull request; GitHub valida que el archivo
pueda importarse y, después de la revisión del docente, el DAG se publica en
Cloud Composer.

## Flujo del estudiante

1. Aceptar la invitación enviada por el docente a la organización `SS2-USAC`.
2. Crear una rama desde `main`.
3. Copiar `dags/201700703_dag_ejemplo.py` como
   `dags/<carnet>_dag.py`. El `dag_id` también debe comenzar con el carnet.
4. Abrir un pull request. La comprobación `Validar DAGs` debe finalizar en verde.
5. Corregir y volver a hacer push si la validación falla.
6. El docente revisa y fusiona el PR.

No deben incluirse contraseñas, llaves ni archivos de datos en un DAG.

## Contenido

- `dags/201700703_dag_ejemplo.py`: modelo básico con dependencias, XCom,
  TaskFlow, branching y manejo de errores.
- `.github/workflows/validate-dags.yml`: validación de pull requests.
- `.github/workflows/deploy-airflow.yml`: despliegue controlado al Airflow del curso.

## Prueba local

```bash
python -m pip install -r requirements-dev.txt
pytest
```
