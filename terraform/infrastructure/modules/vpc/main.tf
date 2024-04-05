resource "google_compute_network" "network" {
  project = var.project
  name    = var.google_compute_network_name

  mtu                             = 1460
  routing_mode                    = "REGIONAL"
  auto_create_subnetworks         = false
  delete_default_routes_on_create = false

  depends_on = [
    google_project_service.compute,
    google_project_service.container
  ]
}


resource "google_compute_global_address" "global_private_ip_address" {
  project = var.project
  network = google_compute_network.network.name

  name    = var.private_service_connection_name
  purpose = "VPC_PEERING"

  address_type  = "INTERNAL"
  address       = split("/", var.private_service_connection_peering_range)[0]
  prefix_length = split("/", var.private_service_connection_peering_range)[1]
}

resource "google_service_networking_connection" "private_service_connection" {
  network                 = google_compute_network.network.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.global_private_ip_address.name]

  depends_on = [ google_project_service.networking ]
}

resource "google_compute_firewall" "allow_ingress_rule" {
  project   = var.project
  name      = "${google_compute_global_address.global_private_ip_address.name}-allow-ssh"
  network   = google_compute_network.network.name
  direction = "INGRESS"
  allow {
    protocol = "tcp"
    ports    = ["5432"]
  }

  source_ranges = var.firewall_source_ranges
  target_tags   = var.firewall_target_tags
}
