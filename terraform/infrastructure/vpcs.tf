resource "google_compute_network" "vpn_sportapp" {
  project = var.project_name
  name    = "vpn-misw-sportapp"

  routing_mode                    = "REGIONAL"
  auto_create_subnetworks         = false
  mtu                             = 1460
  delete_default_routes_on_create = false

  depends_on = [
    google_project_service.compute,
    google_project_service.container
  ]
}


resource "google_compute_subnetwork" "subnet_k8s_sportapp" {
  name   = "subnet-misw-sportapp-k8"
  region = var.region

  network                  = google_compute_network.vpn_sportapp.id
  ip_cidr_range            = "192.168.32.0/19"
  private_ip_google_access = true

  secondary_ip_range = [{
    range_name    = "secondary-subnet-k8s-nodes"
    ip_cidr_range = "192.168.64.0/21"
    }, {
    range_name    = "secondary-subnet-k8s-services"
    ip_cidr_range = "192.168.72.0/21"
  }]
}
