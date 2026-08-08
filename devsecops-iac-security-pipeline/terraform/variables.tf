variable "aws_region" {
  description = "AWS region used for Terraform planning and policy scanning"
  type        = string
  default     = "us-east-1"
}

variable "secure_bucket_name" {
  description = "Secure S3 bucket name for encrypted and private storage"
  type        = string
  default     = "devsecops-secure-bucket-example"
}

variable "insecure_bucket_name" {
  description = "Intentionally insecure public S3 bucket for scanning examples"
  type        = string
  default     = "devsecops-insecure-public-bucket-example"
}

variable "trusted_cidr" {
  description = "Trusted CIDR block used for secure security group ingress"
  type        = string
  default     = "10.0.0.0/16"
}
