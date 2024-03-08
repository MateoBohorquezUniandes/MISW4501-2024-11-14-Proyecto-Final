resource "google_container_cluster" "k8s_misw_sportapp" {
  name     = "cluster-k8s-misw-sportapp"
  location = var.location

  remove_default_node_pool = true
  initial_node_count = 1

  network = google_compute_network.vpn_sportapp
  subnetwork = google_compute_subnetwork.subnet_k8s_sportapp
  networking_mode = "VPC_NATIVE"

  node_locations = [
    "us-central-1-b"
  ]

  addons_config {
    http_load_balancing {
      disabled = true
    }
    horizontal_pod_autoscaling {
      disabled = false
    }
  }

  release_channel {
    channel = "regular"
  }

  ip_allocation_policy {
    cluster_secondary_range_name = "secondary-subnet-k8s-nodes"
    services_secondary_range_name = "secondary-subnet-k8s-services"
  }

  private_cluster_config {
    enable_private_nodes = true
  }
}
