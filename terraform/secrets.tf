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
