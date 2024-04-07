resource "google_service_account" "cloudtask_sa" {
  project      = var.project
  account_id   = var.account_id
  display_name = var.display_name
}

resource "google_project_iam_binding" "cloudtask_sa_roles" {
  for_each = var.roles
  role     = each.value

  project = var.project
  members = [
    "serviceAccount:${google_service_account.cloudtask_sa.email}"
  ]
}
