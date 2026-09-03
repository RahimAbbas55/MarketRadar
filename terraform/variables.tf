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