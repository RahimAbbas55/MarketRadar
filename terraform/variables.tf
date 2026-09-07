variable "environment" {
  description = "Deployment environment (dev, staging, or prod)"
  type        = string

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "environment must be one of: \"dev\", \"staging\", \"prod\"."
  }
}

variable "openai_api_key" {
  description = "OpenAI API key for the agent"
  type        = string
  sensitive   = true
}

variable "newsapi_key" {
  description = "NewsAPI key for market news search"
  type        = string
  sensitive   = true
}