resource "google_spanner_instance" "spanner_instance" {
  config       = "regional-${var.region}"
  display_name = var.spanner_name
  autoscaling_config {
    autoscaling_limits {
      // Define the minimum and maximum compute capacity allocated to the instance
      // Either use nodes or processing units to specify the limits,
      // but should use the same unit to set both the min_limit and max_limit.
      max_nodes  = 3
      min_nodes = 1
    }
    autoscaling_targets {
      high_priority_cpu_utilization_percent = 75
      storage_utilization_percent           = 90
    }
  }
}

resource "google_spanner_database" "spanner_database" {
  instance                 = google_spanner_instance.spanner_instance.name
  name                     = var.spanner_database_name
  version_retention_period = "3d"
  deletion_protection      = false
  database_dialect         = "POSTGRESQL"
}
