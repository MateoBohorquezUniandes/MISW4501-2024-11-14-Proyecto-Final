provider "google" {
  credentials = "gcp_credentials.json"
  region      = var.region
  zone        = var.location
}
