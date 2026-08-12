# Arquitectura propuesta en GCP

```text
Estudiante -> Cloud Run (formulario) -> GitHub API -> invitación a SS2-USAC
Estudiante -> rama + pull request -> GitHub Actions (importa y prueba DAG)
Docente -> aprueba merge -> GitHub Actions + WIF -> bucket de Cloud Composer
Grupo Google de estudiantes -> IAP -> Airflow UI (rol Viewer)
```

## Separación de permisos

- GitHub: los estudiantes son miembros normales, sin rol Owner. `main` se protege:
  PR obligatorio, comprobación `Validar DAGs`, una aprobación y sin force-push.
- Despliegue: sólo el workflow de `main` obtiene una identidad GCP mediante
  Workload Identity Federation. No se guardan llaves JSON en GitHub.
- Composer: el servicio de despliegue recibe acceso de escritura únicamente al
  bucket de DAGs. Los estudiantes no reciben acceso al bucket.
- Interfaz Airflow: crear un Google Group del curso y asignarle acceso a Composer
  y el rol RBAC `Viewer` de Airflow. `Viewer` permite consultar DAGs y ejecuciones,
  pero no disparar, pausar, borrar ni modificar. El docente conserva `User` u
  `Op`; validar los permisos efectivos con una cuenta estudiantil antes de clase.

La pertenencia a GitHub no debe otorgar automáticamente IAM en GCP. Se recomienda
administrar el Google Group desde el listado oficial del curso.

## Componentes

1. Cloud Composer 2 en una red y proyecto del curso.
2. Bucket administrado por Composer para `dags/`.
3. GitHub Actions con Workload Identity Federation y una cuenta de servicio
   limitada al bucket.
4. Cloud Run público para la inscripción; Secret Manager contiene el token.
5. Cloud Logging y alerta sobre respuestas 5xx del servicio de inscripción.

## Despliegue de la página

```bash
gcloud services enable run.googleapis.com secretmanager.googleapis.com artifactregistry.googleapis.com
gcloud builds submit enrollment --tag REGION-docker.pkg.dev/PROJECT/REPO/airflow-enrollment:1
cd infra
terraform init
terraform apply -var project_id=PROJECT -var image=REGION-docker.pkg.dev/PROJECT/REPO/airflow-enrollment:1
printf '%s' "$GITHUB_TOKEN" | gcloud secrets versions add airflow-github-org-token --data-file=-
```

No guardar el token en Terraform, archivos `.tfvars` ni GitHub. Para una clase
grande, añadir Cloud Armor o reCAPTCHA y limitar solicitudes por IP, porque el
endpoint es público.

## Configuración del repositorio

1. Crear el environment `composer-production` con aprobación obligatoria del docente.
2. Definir el secreto `GCP_WORKLOAD_IDENTITY_PROVIDER` y `GCP_SERVICE_ACCOUNT`.
3. Definir la variable `COMPOSER_DAG_BUCKET` con sólo el nombre del bucket.
4. Proteger `main` y exigir el workflow `Validar DAGs`.
5. Desactivar la creación de repositorios por miembros si no es necesaria.

## Criterio de la dinámica

Un PR verde prueba que Airflow puede importar los DAGs, pero no garantiza que
servicios externos, conexiones o datos existan. El docente fusiona el PR, espera
la sincronización de Composer, ejecuta el DAG desde su cuenta y comparte el estado.
Si falla, el estudiante corrige la misma rama o abre un PR de corrección.
