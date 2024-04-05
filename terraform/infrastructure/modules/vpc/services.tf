resource "google_project_service" "compute" {
  service = "compute.googleapis.com"
  project = var.project
}

resource "google_project_service" "container" {
  service = "container.googleapis.com"
  project = var.project
}

resource "google_project_service" "networking" {
  service = "servicenetworking.googleapis.com"
  project = var.project
}