terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }

  backend "gcs" {
    bucket = "marketradar-tfstate"
    prefix = "marketradar/state"
  }
}

provider "google" {
  project = "marketradar-prod"
  region  = "us-central1"
}

data "google_project" "project" {}

locals {
  name_suffix = var.environment == "prod" ? "" : "-${var.environment}"
}

module "registry" {
  source        = "./modules/registry"
  location      = "us-central1"
  repository_id = "marketradar-repo${local.name_suffix}"
  description   = "MarketRadar container images (${var.environment})"
}

module "openai_secret" {
  source          = "./modules/secrets"
  secret_id       = "openai-api-key${local.name_suffix}"
  secret_value    = var.openai_api_key
  accessor_member = "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com"
}

module "newsapi_secret" {
  source          = "./modules/secrets"
  secret_id       = "newsapi-key${local.name_suffix}"
  secret_value    = var.newsapi_key
  accessor_member = "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com"
}

module "backend" {
  source         = "./modules/compute"
  service_name   = "marketradar-backend${local.name_suffix}"
  location       = "us-central1"
  image          = "us-central1-docker.pkg.dev/marketradar-prod/marketradar-repo${local.name_suffix}/backend:latest"
  container_port = 8080

  secret_env_vars = [
    { name = "OPENAI_API_KEY", secret_id = module.openai_secret.secret_id },
    { name = "NEWSAPI_KEY", secret_id = module.newsapi_secret.secret_id }
  ]

  depends_on = [module.openai_secret, module.newsapi_secret]
}

module "frontend" {
  source         = "./modules/compute"
  service_name   = "marketradar-frontend${local.name_suffix}"
  location       = "us-central1"
  image          = "us-central1-docker.pkg.dev/marketradar-prod/marketradar-repo${local.name_suffix}/frontend:latest"
  container_port = 8080
}