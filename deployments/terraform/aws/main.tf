terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.50"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_vpc" "omniflow_vpc" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true
  tags = {
    Name        = "omniflow-vpc"
    Environment = var.environment
  }
}

resource "aws_eks_cluster" "omniflow_eks" {
  name     = "omniflow-cluster-${var.environment}"
  role_arn = "arn:aws:iam::123456789012:role/EKSClusterRole"
  version  = "1.29"

  vpc_config {
    subnet_ids = ["subnet-0a1b2c3d4e", "subnet-0f1g2h3i4j"]
  }
}

resource "aws_db_instance" "omniflow_rds" {
  identifier          = "omniflow-db-${var.environment}"
  allocated_storage   = 100
  max_allocated_storage = 1000
  engine              = "postgres"
  engine_version      = "16.2"
  instance_class      = "db.r6g.xlarge"
  db_name             = "omniflow_db"
  username            = var.db_username
  password            = var.db_password
  skip_final_snapshot = false
  storage_encrypted   = true
}

resource "aws_elasticache_replication_group" "omniflow_redis" {
  replication_group_id          = "omniflow-redis-${var.environment}"
  replication_group_description = "OmniFlow Redis Cluster"
  node_type                     = "cache.r6g.large"
  num_cache_clusters            = 3
  port                          = 6379
  automatic_failover_enabled    = true
  at_rest_encryption_enabled    = true
  transit_encryption_enabled    = true
}
