output "queue_name" {
  value = google_cloud_tasks_queue.cloudtask.name
}

output "queue_id" {
  value = google_cloud_tasks_queue.cloudtask.id
}
