# AWS Webhook Infrastructure

Terraform configuration that deploys the webhook component (`app.webhook`)
to AWS as a Lambda function fronted by an API Gateway HTTP API.

## Architecture

```
Hevy webhook ──> API Gateway (HTTP API) ──> Lambda (FastAPI via Mangum) ──> CloudWatch Logs
                   POST /webhook
                   GET  /health
```

- **Lambda** runs the FastAPI app in `src/app/webhook.py` through the
  [Mangum](https://mangum.fastapiexpert.com/) ASGI adapter
  (handler: `app.webhook.handler`, runtime: `python3.12`).
- **API Gateway v2 (HTTP API)** routes `POST /webhook` and `GET /health`
  to the Lambda with a payload format 2.0 proxy integration.
- **CloudWatch** log groups capture Lambda logs and API access logs.

The deployment package is built by `scripts/build_lambda_package.sh`,
which installs the Lambda-only dependencies (`terraform/lambda/requirements.txt`)
for the Lambda runtime platform and copies in `src/app` and `config/`.
Terraform triggers a rebuild automatically whenever the app source,
config, or requirements change.

## Prerequisites

- Terraform >= 1.6
- Python 3 with `pip` (used to build the Lambda package)
- AWS credentials with permission to manage Lambda, API Gateway, IAM,
  and CloudWatch resources (e.g. via `AWS_PROFILE`)

## Usage

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

The webhook subscription URL to register with the Hevy API is:

```bash
echo "$(terraform output -raw webhook_api_endpoint)/webhook"
```

## Variables

| Variable | Default | Purpose |
| -------- | ------- | ------- |
| `aws_region` | `us-west-2` | Deployment region |
| `project_name` | `hevy-api-pull` | Resource name prefix |
| `app_environment` | `prod` | Value of the `ENV` variable in the Lambda (selects the dynaconf config file) |
| `lambda_memory_size` | `256` | Lambda memory (MB) |
| `lambda_timeout` | `10` | Lambda timeout (seconds) |
| `log_retention_days` | `30` | CloudWatch retention for both log groups |

State is local by default; add a `backend` block in `versions.tf` if you
want remote state (e.g. S3).
