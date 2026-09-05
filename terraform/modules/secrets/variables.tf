variable "secret_id" {
  description = "Secret Manager secret ID"
  type        = string
}

variable "secret_value" {
  description = "The secret's value"
  type        = string
  sensitive   = true
}

variable "accessor_member" {
  description = "IAM member granted access to read this secret (e.g. a service account)"
  type        = string
}