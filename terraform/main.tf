provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.app_environment
      ManagedBy   = "terraform"
    }
  }
}

locals {
  repo_root   = abspath("${path.module}/..")
  name_prefix = "${var.project_name}-${var.app_environment}"

  # Hash of everything that goes into the Lambda package, used to
  # trigger a rebuild when the source or dependencies change.
  lambda_source_hash = sha256(join("", concat(
    [for f in sort(fileset("${local.repo_root}/src/app", "**")) : filesha256("${local.repo_root}/src/app/${f}")],
    [for f in sort(fileset("${local.repo_root}/config", "*.yaml")) : filesha256("${local.repo_root}/config/${f}")],
    [
      filesha256("${path.module}/lambda/requirements.txt"),
      filesha256("${path.module}/scripts/build_lambda_package.sh"),
    ],
  )))
}
