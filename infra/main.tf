terraform {
  required_providers {
    google = { source = "hashicorp/google", version = "~> 6.0" }
  }
}

variable "project_id" {
  type = string
}
variable "region" {
  type    = string
  default = "us-central1"
}
variable "github_org" {
  type    = string
  default = "SS2-USAC"
}
variable "image" {
  type = string
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_service_account" "enrollment" {
  account_id   = "airflow-enrollment"
  display_name = "Airflow student enrollment"
}

resource "google_secret_manager_secret" "github_token" {
  secret_id = "airflow-github-org-token"
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_iam_member" "runtime" {
  secret_id = google_secret_manager_secret.github_token.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.enrollment.email}"
}

resource "google_cloud_run_v2_service" "enrollment" {
  name     = "airflow-inscripcion"
  location = var.region
  template {
    service_account = google_service_account.enrollment.email
    containers {
      image = var.image
      env {
        name  = "GITHUB_ORG"
        value = var.github_org
      }
      env {
        name = "GITHUB_TOKEN"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.github_token.secret_id
            version = "latest"
          }
        }
      }
    }
  }
}

resource "google_cloud_run_v2_service_iam_member" "public" {
  name     = google_cloud_run_v2_service.enrollment.name
  location = google_cloud_run_v2_service.enrollment.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

output "enrollment_url" {
  value = google_cloud_run_v2_service.enrollment.uri
}
