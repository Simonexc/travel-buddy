variable "project_id" {
  description = "The GCP project ID."
}

variable "region" {
  description = "The GCP region where resources will be deployed."
  default     = "europe-central2"
}

variable "zone" {
  description = "The GCP zone where resources will be deployed (single letter descriptor based on region)."
  default     = "a"
}

variable "db_password" {
  description = "The password for the database user."
  sensitive   = true
}

variable "secret_file_path" {
  description = "The path to the secret file from GCP."
}

variable "machine_type" {
  description = "The machine type for the discord bot."
  default     = "e2-medium"
}

variable "max_replicas" {
  description = "The maximum number of replicas for the discord bot."
  default     = 10
}
