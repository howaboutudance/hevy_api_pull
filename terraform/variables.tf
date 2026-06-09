variable "aws_region" {
  description = "AWS region to deploy the webhook infrastructure into."
  type        = string
  default     = "us-west-2"
}

variable "project_name" {
  description = "Name used to prefix all created resources."
  type        = string
  default     = "hevy-api-pull"
}

variable "app_environment" {
  description = "Application environment passed to the app as the ENV variable (selects the dynaconf config file)."
  type        = string
  default     = "prod"
}

variable "lambda_memory_size" {
  description = "Memory (MB) allocated to the webhook Lambda function."
  type        = number
  default     = 256
}

variable "lambda_timeout" {
  description = "Timeout (seconds) for the webhook Lambda function."
  type        = number
  default     = 10
}

variable "log_retention_days" {
  description = "CloudWatch log retention for the Lambda and API Gateway access logs."
  type        = number
  default     = 30
}
