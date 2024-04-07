resource "google_artifact_registry_repository" "artifact_registry" {
  project                = var.project
  location               = var.location
  repository_id          = var.repository_id
  description            = var.description
  format                 = var.format
  cleanup_policy_dry_run = true
}
