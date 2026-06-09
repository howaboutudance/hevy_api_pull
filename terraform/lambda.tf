# Build the Lambda deployment package (dependencies + app source) whenever
# the source hash changes.
resource "null_resource" "lambda_build" {
  triggers = {
    source_hash = local.lambda_source_hash
  }

  provisioner "local-exec" {
    command = "${path.module}/scripts/build_lambda_package.sh"
  }
}

data "archive_file" "webhook_lambda" {
  type        = "zip"
  source_dir  = "${path.module}/build/package"
  output_path = "${path.module}/build/webhook_lambda.zip"

  depends_on = [null_resource.lambda_build]
}

resource "aws_iam_role" "webhook_lambda" {
  name = "${local.name_prefix}-webhook-lambda"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Action    = "sts:AssumeRole"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "webhook_lambda_logs" {
  role       = aws_iam_role.webhook_lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_cloudwatch_log_group" "webhook_lambda" {
  name              = "/aws/lambda/${local.name_prefix}-webhook"
  retention_in_days = var.log_retention_days
}

resource "aws_lambda_function" "webhook" {
  function_name = "${local.name_prefix}-webhook"
  role          = aws_iam_role.webhook_lambda.arn

  filename         = data.archive_file.webhook_lambda.output_path
  source_code_hash = data.archive_file.webhook_lambda.output_base64sha256

  runtime       = "python3.12"
  architectures = ["x86_64"]
  handler       = "app.webhook.handler"

  memory_size = var.lambda_memory_size
  timeout     = var.lambda_timeout

  environment {
    variables = {
      ENV = var.app_environment
    }
  }

  depends_on = [
    aws_iam_role_policy_attachment.webhook_lambda_logs,
    aws_cloudwatch_log_group.webhook_lambda,
  ]
}
