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

resource "google_artifact_registry_repository" "marketradar_repo" {
  location      = "us-central1"
  repository_id = "marketradar-repo"
  description   = "MarketRadar container images"
  format        = "DOCKER"
}