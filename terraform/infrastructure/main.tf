locals {
  db_tag = "misw450xdb"
  cloudtask_iam_roles = toset([
    "roles/cloudtasks.taskRunner",
    "roles/cloudtasks.enqueuer",
    "roles/cloudtasks.viewer"
  ])
}

module "misw450x_vpn" {
  source                                   = "./modules/vpc"
  project                                  = var.project
  google_compute_network_name              = "misw450x-vpn"
  private_service_connection_name          = "misw450x-internal-db"
  private_service_connection_peering_range = "192.168.0.0/24"
  firewall_source_ranges                   = ["192.168.1.0/24"]
  firewall_target_tags                     = [local.db_tag]
}

module "misw450x-subnet" {
  source  = "./modules/subnet"
  project = var.project
  region  = var.region

  vpn_subnet_name = "misw450x-subnet-k8s"
  vpc_network_id  = module.misw450x_vpn.network_id
  ip_cidr_range   = "192.168.32.0/19"
  secondary_ip_range = [
    {
      ip_cidr_range = "192.168.64.0/21"
      range_name    = "gke-misw450x-k8s-cluster-pods-ea8688ef"
    },
    {
      ip_cidr_range = "192.168.72.0/21"
      range_name    = "gke-misw450x-k8s-cluster-services-ea8688ef"
    },
  ]
}

module "misw450x-gke-static-ip" {
  source  = "./modules/static_ip"
  project = var.project
  name    = "misw450x-k8s-ip"
}

module "misw450x-deportistas-db" {
  source  = "./modules/cloudsql"
  project = var.project
  region  = var.region

  instance_name             = "deportistas"
  instance_suffix           = "misw450x"
  google_compute_network_id = module.misw450x_vpn.network_id
  user_labels               = { "${local.db_tag}" : "" }
  activation_policy         = "NEVER"
}

module "misw450x-sportapp-db" {
  source  = "./modules/cloudsql"
  project = var.project
  region  = var.region

  instance_name             = "sportapp"
  instance_suffix           = "misw450x"
  google_compute_network_id = module.misw450x_vpn.network_id
  user_labels               = { "${local.db_tag}" : "" }
  activation_policy         = "NEVER"
}

module "misw450x_artifact_registry" {
  source        = "./modules/artifactregistry"
  project       = var.project
  location      = var.region
  repository_id = "misw450x-registry"
  description   = "registro de contenedores para sportapp"
}

module "misw450x_usuario_events" {
  source  = "./modules/cloudtasks"
  project = var.project
  region  = var.region

  task_queue_name    = "misw450x-usuarios-integration-events"
  max_doublings      = 1
  max_attempts       = 5
  min_backoff        = "1s"
  max_backoff        = "2s"
  max_retry_duration = "4s"
}

module "misw450x_perfiles_events" {
  source  = "./modules/cloudtasks"
  project = var.project
  region  = var.region

  task_queue_name    = "misw450x-perfiles-integration-events"
  max_doublings      = 1
  max_attempts       = 5
  min_backoff        = "1s"
  max_backoff        = "2s"
  max_retry_duration = "4s"
}

module "cloud_task_service_account" {
  source  = "./modules/service_account"
  project = var.project

  account_id   = "misw450x-cloud-task-enqueuer"
  display_name = "misw450x Cloud Task Enqueuer"
  roles        = local.cloudtask_iam_roles
}
