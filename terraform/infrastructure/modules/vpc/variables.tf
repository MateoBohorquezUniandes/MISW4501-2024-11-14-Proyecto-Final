variable "project_name" {
  type = string
}

variable "google_compute_network_name" {
  type = string
}

variable "private_service_connection_name" {
  type = string
}

variable "private_service_connection_peering_range" {
  type = string
}

variable "firewall_source_ranges" {
  type = list(string)
}

variable "firewall_target_tags" {
  type = list(string)
}