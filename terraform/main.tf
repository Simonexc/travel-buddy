resource "google_compute_instance_template" "bot" {
  name         = "discord-bot"
  machine_type = var.machine_type
  region       = var.region

  disk {
    source_image = "debian-cloud/debian-11"
    auto_delete  = true
    boot         = true
  }

  network_interface {
    network = "default"
    access_config {}
  }

  service_account {
    scopes = ["cloud-platform"]
  }

  metadata_startup_script = file("startup.sh")
}

resource "google_compute_region_instance_group_manager" "bot" {
  base_instance_name = "discord-bot"
  name               = "discord-bot-group"
  region             = var.region

  version {
    instance_template = google_compute_instance_template.bot.self_link
  }
  target_size        = 1  # Sets the initial size but does not manage autoscaling
  depends_on = [google_compute_instance_template.bot]
}

resource "google_compute_region_autoscaler" "bot" {
  name   = "discord-bot-autoscaler"
  target = google_compute_region_instance_group_manager.bot.self_link
  region = var.region

  autoscaling_policy {
    min_replicas    = 1
    max_replicas    = var.max_replicas
    cooldown_period = 60

    cpu_utilization {
      target = 0.5  # Target CPU utilization of 50%
    }
  }
    depends_on = [google_compute_region_instance_group_manager.bot]
}
