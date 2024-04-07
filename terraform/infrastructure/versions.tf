terraform {
  required_version = ">= 1.1"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }

  backend "gcs" {
    bucket      = "tf-state-misw450x"
    prefix      = "terraform/state"
    credentials = "./../key.json"
  }
}
