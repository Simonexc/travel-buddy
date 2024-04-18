resource "google_secret_manager_secret" "db_password_secret" {
  secret_id = "db-password"
  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "db_password" {
  secret      = google_secret_manager_secret.db_password_secret.id
  secret_data = var.db_password
}

resource "google_secret_manager_secret" "project_id_secret" {
  secret_id = "project-id"
  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "project_id" {
  secret      = google_secret_manager_secret.project_id_secret.id
  secret_data = var.project_id
}

resource "google_secret_manager_secret" "region_secret" {
  secret_id = "region"
  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "region" {
  secret      = google_secret_manager_secret.region_secret.id
  secret_data = var.region
}
