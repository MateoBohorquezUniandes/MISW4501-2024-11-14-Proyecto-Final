output "network_name" {
  value = google_compute_network.network.name
}

output "network_id" {
  value = google_compute_network.network.id
}

output "global_private_ip_address_name" {
  value = google_compute_global_address.global_private_ip_address.name
}

output "global_private_ip_address_id" {
  value = google_compute_global_address.global_private_ip_address.id
}

output "private_service_connection_id" {
  value = google_service_networking_connection.private_service_connection.id
}
