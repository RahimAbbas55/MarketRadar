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

module "registry" {
  source        = "./modules/registry"
  location      = "us-central1"
  repository_id = "marketradar-repo"
  description   = "MarketRadar container images"
}

module "openai_secret" {
  source           = "./modules/secrets"
  secret_id        = "openai-api-key"
  secret_value     = var.openai_api_key
  accessor_member  = "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com"
}

module "newsapi_secret" {
  source           = "./modules/secrets"
  secret_id        = "newsapi-key"
  secret_value     = var.newsapi_key
  accessor_member  = "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com"
}

module "backend" {
  source         = "./modules/compute"
  service_name   = "marketradar-backend"
  location       = "us-central1"
  image          = "us-central1-docker.pkg.dev/marketradar-prod/marketradar-repo/backend:latest"
  container_port = 8080

  secret_env_vars = [
    { name = "OPENAI_API_KEY", secret_id = module.openai_secret.secret_id },
    { name = "NEWSAPI_KEY", secret_id = module.newsapi_secret.secret_id }
  ]

  depends_on = [module.openai_secret, module.newsapi_secret]
}

module "frontend" {
  source         = "./modules/compute"
  service_name   = "marketradar-frontend"
  location       = "us-central1"
  image          = "us-central1-docker.pkg.dev/marketradar-prod/marketradar-repo/frontend:latest"
  container_port = 8080
}