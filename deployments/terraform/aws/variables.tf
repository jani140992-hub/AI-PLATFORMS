variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "environment" {
  type    = string
  default = "production"
}

variable "vpc_cidr" {
  type    = string
  default = "10.0.0.0/16"
}

variable "db_username" {
  type    = string
  default = "omniflow"
}

variable "db_password" {
  type      = string
  default   = "secure-db-password-vault"
  sensitive = true
}
