terraform {
  required_version = ">= 1.4.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = var.region
}

variable "region" {
  description = "AWS region to deploy the resources"
  type        = string
  default     = "us-west-2"
}

# Generate a random suffix for resource names to avoid collisions
resource "random_id" "rand" {
  byte_length = 4
}

# Example S3 bucket for storing artefacts or reports
resource "aws_s3_bucket" "artifacts" {
  bucket        = "hospital-agent-artifacts-${random_id.rand.hex}"
  force_destroy = true
}

output "artifacts_bucket" {
  value = aws_s3_bucket.artifacts.bucket
}

# Placeholder for additional resources:
# - IAM roles and policies
# - Lambda function packaging the FastAPI app
# - API Gateway to expose the endpoints
# See README.md for guidance on completing this configuration.