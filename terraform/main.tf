terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = "marketradar-prod"
  region  = "us-central1"
}

data "google_project" "project" {}

resource "google_artifact_registry_repository" "marketradar_repo" {
  location      = "us-central1"
  repository_id = "marketradar-repo"
  description   = "MarketRadar container images"
  format        = "DOCKER"
}

resource "google_secret_manager_secret" "openai_api_key" {
  secret_id = "openai-api-key"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "openai_api_key_version" {
  secret      = google_secret_manager_secret.openai_api_key.id
  secret_data = var.openai_api_key
}

resource "google_secret_manager_secret" "newsapi_key" {
  secret_id = "newsapi-key"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "newsapi_key_version" {
  secret      = google_secret_manager_secret.newsapi_key.id
  secret_data = var.newsapi_key
}

resource "google_secret_manager_secret_iam_member" "openai_secret_access" {
  secret_id = google_secret_manager_secret.openai_api_key.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com"
}

resource "google_secret_manager_secret_iam_member" "newsapi_secret_access" {
  secret_id = google_secret_manager_secret.newsapi_key.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com"
}

resource "google_cloud_run_v2_service" "backend" {
  name     = "marketradar-backend"
  location = "us-central1"

  template {
    containers {
      image = "us-central1-docker.pkg.dev/marketradar-prod/marketradar-repo/backend:latest"

      env {
        name = "OPENAI_API_KEY"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.openai_api_key.secret_id
            version = "latest"
          }
        }
      }
      env {
        name = "NEWSAPI_KEY"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.newsapi_key.secret_id
            version = "latest"
          }
        }
      }

      ports {
        container_port = 8080
      }
    }
  }

  depends_on = [
    google_secret_manager_secret_iam_member.openai_secret_access,
    google_secret_manager_secret_iam_member.newsapi_secret_access
  ]
}

resource "google_cloud_run_v2_service_iam_member" "backend_public" {
  location = google_cloud_run_v2_service.backend.location
  name     = google_cloud_run_v2_service.backend.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}