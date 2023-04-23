terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  credentials = file(var.tf_credentials)
  project     = "xoutoz-accounting"
  region      = "europe-west1"
}