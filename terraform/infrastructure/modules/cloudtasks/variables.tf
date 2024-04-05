variable "region" {
  type    = string
  default = "us-central1"
}

variable "task_queue_name" {
  type = string
}

variable "max_attempts" {
  type = string
}

variable "min_backoff" {
  type = string
}

variable "max_backoff" {
  type = string
}

variable "max_doublings" {
  type = string
}
