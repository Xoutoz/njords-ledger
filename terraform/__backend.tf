terraform {
    backend "gcs" {
        bucket  = "xoutoz-personal-accounting-tf"
        prefix  = "terraform/state"
    }
}