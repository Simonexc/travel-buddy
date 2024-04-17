resource "google_sql_database_instance" "postgres" {
  name             = "discord-bot-db"
  database_version = "POSTGRES_12"
  region           = var.region

  settings {
    tier = "db-custom-1-3840"
  }
}

resource "google_sql_database" "bot_database" {
  name     = "botdb"
  instance = google_sql_database_instance.postgres.name
}

resource "google_sql_user" "bot_user" {
  name     = "botuser"
  instance = google_sql_database_instance.postgres.name
  password = var.db_password
}
