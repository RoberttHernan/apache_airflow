# Laboratorio colaborativo de Apache Airflow

Repositorio para la dinámica de la semana 4 de Seminario de Sistemas 2. Cada
estudiante propone un DAG mediante un pull request; GitHub valida que el archivo
pueda importarse y, después de la revisión del docente, el DAG se publica en
Cloud Composer.

## Flujo del estudiante

1. Abrir la página de inscripción y escribir el usuario de GitHub.
2. Aceptar la invitación enviada por GitHub a la organización `SS2-USAC`.
3. Crear una rama desde `main`.
4. Copiar `dags/201700703_dag_ejemplo.py` como
   `dags/<carnet>_dag.py`. El `dag_id` también debe comenzar con el carnet.
5. Abrir un pull request. La comprobación `Validar DAGs` debe finalizar en verde.
6. Corregir y volver a hacer push si la validación falla.
7. El docente revisa y fusiona el PR. La publicación a Composer se realiza sólo
   desde `main` y requiere aprobación del entorno `composer-production`.

No deben incluirse contraseñas, llaves ni archivos de datos en un DAG.

## Contenido

- `dags/201700703_dag_ejemplo.py`: modelo básico con dependencias, XCom,
  TaskFlow, branching y manejo de errores.
- `enrollment/`: página y API para solicitar una invitación a GitHub.
- `.github/workflows/validate-dags.yml`: validación de pull requests.
- `.github/workflows/deploy-composer.yml`: sincronización controlada a Composer.
- `infra/`: infraestructura de la página de inscripción en GCP.
- `docs/arquitectura-gcp.md`: arquitectura, permisos y puesta en marcha.

## Prueba local

```bash
python -m pip install -r requirements-dev.txt
pytest
```

Para probar la inscripción localmente:

```bash
cd enrollment
python -m pip install -r requirements.txt
set GITHUB_ORG=SS2-USAC
set GITHUB_TOKEN=token_de_prueba
uvicorn app:app --reload
```

El token debe ser de corta duración. En producción se recomienda una GitHub App
con permiso de escritura en miembros de la organización; si se usa un fine-grained
PAT, debe guardarse únicamente en Secret Manager.
