variable "instance_name" {
  type = string
}

variable "instance_suffix" {
  type = string
}

variable project_name {
  type    = string
}

variable "region" {
  type    = string
  default = "us-central1"
}

variable "database_version" {
  type    = string
  default = "POSTGRES_15"
}

variable "deletion_protection" {
  type    = bool
  default = false
}

variable "tier" {
  type    = string
  default = "db-f1-micro"
}

variable "edition" {
  type    = string
  default = "ENTERPRISE"
}

variable "disk_size" {
  type    = number
  default = 20
}

variable "disk_autoresize" {
  type    = bool
  default = false
}

variable "activation_policy" {
  type    = string
  default = "ALWAYS"
}

variable "google_compute_network_id" {
  type = string
}

variable "user_labels" {
  type = map(string)
}