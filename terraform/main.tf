locals {
  bq_schema = "${path.root}/files/expenses-bq-table-schema.json"
  pubsub_schema = "${path.root}/files/expenses-pubsub-topic-schema.json"
}

## GCP PROJECT DATA
data "google_project" "project" { }


## BIGQUERY RESOURCES
resource "google_bigquery_dataset" "main" {
  dataset_id  = "main"
  description = "Accounting dataset"
  location    = "europe-west1"
}

resource "google_bigquery_table" "expenses" {
  dataset_id = google_bigquery_dataset.main.dataset_id
  table_id   = "expenses"

  time_partitioning {
    type          = "DAY"
    expiration_ms = 94670778000
    field         = "date"
  }

  schema = file(local.bq_schema)

  deletion_protection = false
}


## PUBSUB RESOURCES
resource "google_pubsub_schema" "expenses_message_schema" {
  name = "expenses-schema"
  type = "AVRO"
  definition = file(local.pubsub_schema)
}

resource "google_pubsub_topic" "expenses_topic" {
  name = "publish-expenses"

  schema_settings {
    schema = google_pubsub_schema.expenses_message_schema.id
    encoding = "JSON"
  }
  
  depends_on = [google_pubsub_schema.expenses_message_schema]
}

resource "google_pubsub_subscription" "expenses_bq_subscription" {
  name  = "publish-expenses-subscription"
  topic = google_pubsub_topic.expenses_topic.name

  bigquery_config {
    table = "${google_bigquery_table.expenses.project}.${google_bigquery_table.expenses.dataset_id}.${google_bigquery_table.expenses.table_id}"
    use_topic_schema = true
  }

  depends_on = [google_bigquery_table.expenses, google_project_iam_member.editor]
}


## SA PERMISSIONS
resource "google_project_iam_member" "editor" {
  project = data.google_project.project.project_id
  role   = "roles/bigquery.dataEditor"
  member = "serviceAccount:service-${data.google_project.project.number}@gcp-sa-pubsub.iam.gserviceaccount.com"
}