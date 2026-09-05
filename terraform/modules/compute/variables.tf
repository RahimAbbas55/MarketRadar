variable "service_name" {
  description = "Cloud Run service name"
  type        = string
}

variable "location" {
  description = "GCP region"
  type        = string
}

variable "image" {
  description = "Container image URL"
  type        = string
}

variable "container_port" {
  description = "Port the container listens on"
  type        = number
  default     = 8080
}

variable "env_vars" {
  description = "Plain environment variables"
  type = list(object({
    name  = string
    value = string
  }))
  default = []
}

variable "secret_env_vars" {
  description = "Environment variables sourced from Secret Manager"
  type = list(object({
    name      = string
    secret_id = string
  }))
  default = []
}