resource "google_sql_database_instance" "database" {
  project = var.project_name
  name                = "${var.instance_name}-${var.instance_suffix}-db"
  region              = var.region
  database_version    = var.database_version
  deletion_protection = var.deletion_protection

  settings {
    tier    = var.tier
    edition = var.edition

    disk_size       = var.disk_size
    disk_autoresize = var.disk_autoresize

    activation_policy = var.activation_policy

    ip_configuration {
      ipv4_enabled                                  = false
      private_network                               = var.google_compute_network_id
      enable_private_path_for_google_cloud_services = true
    }

    backup_configuration {
      enabled = false
    }

    user_labels = var.user_labels
  }

  depends_on = [ google_project_service.sqladmin ]
}
