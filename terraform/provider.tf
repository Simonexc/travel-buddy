provider "google" {
  credentials = file(var.secret_file_path)
  project     = var.project_id
  region      = var.region
}

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.32"
    }
  }

  required_version = ">= 0.13"
}
