resource "google_cloud_tasks_queue" "cloudtask" {
  name     = var.task_queue_name
  location = var.region

  retry_config {
    max_attempts  = var.max_attempts
    min_backoff   = var.min_backoff
    max_backoff   = var.max_backoff
    max_doublings = var.max_doublings
  }

  stackdriver_logging_config {
    sampling_ratio = 0.0
  }
}
