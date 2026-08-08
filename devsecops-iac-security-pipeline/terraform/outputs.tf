output "secure_bucket_name" {
  description = "The secure S3 bucket created by the sample Terraform configuration."
  value       = aws_s3_bucket.secure.bucket
}

output "insecure_bucket_name" {
  description = "The intentionally insecure public S3 bucket used for IaC scan demonstrations."
  value       = aws_s3_bucket.insecure_public_bucket.bucket
}

output "insecure_security_group_id" {
  description = "The security group exposing SSH and RDP to the public internet."
  value       = aws_security_group.insecure_ssh.id
}

output "secure_web_security_group_id" {
  description = "A least-privilege web security group for comparison."
  value       = aws_security_group.secure_web.id
}
