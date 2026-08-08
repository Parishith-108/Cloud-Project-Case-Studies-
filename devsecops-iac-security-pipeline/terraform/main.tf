terraform {
  required_version = ">= 1.2.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region                      = var.aws_region
  access_key                  = "test"
  secret_key                  = "test"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
}

resource "aws_s3_bucket" "secure" {
  bucket = var.secure_bucket_name
  acl    = "private"

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  public_access_block_configuration {
    block_public_acls       = true
    block_public_policy     = true
    ignore_public_acls      = true
    restrict_public_buckets = true
  }

  tags = {
    Name        = "secure-prod-bucket"
    Environment = "secure"
  }
}

resource "aws_s3_bucket" "insecure_public_bucket" {
  bucket = var.insecure_bucket_name
  acl    = "public-read" # intentionally insecure public ACL

  # This resource intentionally leaves off encryption and public access block settings.
  tags = {
    Name        = "insecure-public-bucket"
    Environment = "demo"
  }
}

resource "aws_security_group" "insecure_ssh" {
  name        = "devsecops-open-ssh-rdp"
  description = "Intentionally insecure security group with global SSH and RDP access"

  ingress {
    description = "SSH from anywhere"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "RDP from anywhere"
    from_port   = 3389
    to_port     = 3389
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "insecure-ssh-rdp"
    Environment = "testing"
  }
}

resource "aws_security_group" "secure_web" {
  name        = "devsecops-secure-web"
  description = "Least-privilege security group for web access"

  ingress {
    description = "HTTPS from trusted CIDR"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [var.trusted_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "secure-web-sg"
    Environment = "production"
  }
}
