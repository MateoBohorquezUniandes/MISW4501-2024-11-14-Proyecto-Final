resource "google_compute_subnetwork" "subnet" {
  project = var.project
  name   = var.vpn_subnet_name
  region = var.region

  network                  = var.vpc_network_id
  ip_cidr_range            = var.ip_cidr_range
  private_ip_google_access = true

  secondary_ip_range = var.secondary_ip_range
}
