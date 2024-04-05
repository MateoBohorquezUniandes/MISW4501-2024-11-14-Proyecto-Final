locals {
  db_tag = "misw450xdb"
}

module "misw450x_vpn" {
  source                                   = "./modules/vpc"
  project_name                             = var.project_name
  google_compute_network_name              = "misw450x-vpn"
  private_service_connection_name          = "misw450x-internal-db"
  private_service_connection_peering_range = "192.168.0.0/24"
  firewall_source_ranges                   = ["192.168.1.0/24"]
  firewall_target_tags                     = [local.db_tag]
}

module "misw450x-subnet" {
  source          = "./modules/subnet"
  project_name    = var.project_name
  region          = var.region
  vpn_subnet_name = "misw450x-subnet-k8s"
  vpc_network_id  = module.misw450x_vpn.network_id
  ip_cidr_range   = "192.168.32.0/19"
}

module "misw450x-deportistas-db" {
  source                    = "./modules/cloudsql"
  project_name              = var.project_name
  region                    = var.region
  instance_name             = "deportistas"
  instance_suffix           = "misw450x"
  google_compute_network_id = module.misw450x_vpn.network_id
  user_labels               = { "${local.db_tag}" : "" }
  activation_policy         = "NEVER"
}
