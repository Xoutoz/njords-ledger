terraform {
  required_providers {
    google = {
        source  = "hashicorp/google"
        version = "4.51.0"
    }
  }
}

provider "google" {
    project = "xoutoz-accounting"
    region  = "europe-west1"
}