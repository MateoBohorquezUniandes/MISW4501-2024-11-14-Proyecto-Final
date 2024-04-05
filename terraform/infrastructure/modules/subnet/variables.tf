variable "project" {
  type = string
}

variable "region" {
  type    = string
  default = "us-central1"
}

variable "vpn_subnet_name" {
  type = string
}

variable "vpc_network_id" {
  type = string
}

variable "ip_cidr_range" {
  type    = string
  default = "192.168.32.0/19"
}

variable "secondary_ip_range" {
  type    = list(any)
  default = []
}
