output "webhook_api_endpoint" {
  description = "Base URL of the webhook HTTP API. The webhook subscription URL is <endpoint>/webhook."
  value       = aws_apigatewayv2_api.webhook.api_endpoint
}

output "webhook_lambda_function_name" {
  description = "Name of the webhook Lambda function."
  value       = aws_lambda_function.webhook.function_name
}

output "webhook_lambda_log_group" {
  description = "CloudWatch log group for the webhook Lambda function."
  value       = aws_cloudwatch_log_group.webhook_lambda.name
}
