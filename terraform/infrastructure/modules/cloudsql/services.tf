resource "google_project_service" "sqladmin" {
  service = "sqladmin.googleapis.com"
  project = var.project
}
