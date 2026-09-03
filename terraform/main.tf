resource "google_cloud_run_v2_service" "backend" {
  name     = "marketradar-backend"
  location = "us-central1"

  template {
    containers {
      image = "us-central1-docker.pkg.dev/marketradar-prod/marketradar-repo/backend:latest"

      env {
        name  = "OPENAI_API_KEY"
        value = var.openai_api_key
      }
      env {
        name  = "NEWSAPI_KEY"
        value = var.newsapi_key
      }

      ports {
        container_port = 8080
      }
    }
  }
}

resource "google_cloud_run_v2_service_iam_member" "backend_public" {
  location = google_cloud_run_v2_service.backend.location
  name     = google_cloud_run_v2_service.backend.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}