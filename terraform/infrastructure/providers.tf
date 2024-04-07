provider "google" {
  credentials = "./../key.json"
  region      = var.region
  zone        = var.location
}
