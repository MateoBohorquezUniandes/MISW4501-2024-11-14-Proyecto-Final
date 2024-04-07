variable "project" {
  type = string
}
variable "region" {
  type = string
}

variable "task_queue_name" {
  type = string
}

variable "max_attempts" {
  type = number
}

variable "min_backoff" {
  type = string
}

variable "max_backoff" {
  type = string
}

variable "max_retry_duration" {
  type = string
}

variable "max_doublings" {
  type = number
}
