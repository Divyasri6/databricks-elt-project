variable "boot_disk_size_gb" {
  description = "Boot disk size in GB."
  type        = number
  default     = 20
}

variable "boot_disk_type" {
  description = "Boot disk type."
  type        = string
  default     = "pd-balanced"
}

variable "http_https_source_ranges" {
  description = "Allowed source ranges for HTTP/HTTPS traffic."
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "jenkins_ui_source_ranges" {
  description = "Allowed source ranges for Jenkins UI traffic."
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "instance_metadata" {
  description = "Metadata to add to the instance."
  type        = map(string)
  default     = {}
}

variable "instance_name" {
  description = "Name of the Jenkins controller instance."
  type        = string
  default     = "jenkins-controller"
}

variable "machine_type" {
  description = "Machine type for the instance."
  type        = string
  default     = "e2-small"
}

variable "project_id" {
  description = "GCP project ID where resources will be created."
  type        = string
}

variable "region" {
  description = "Region for the GCE instance."
  type        = string
  default     = "us-central1"
}

variable "service_account_email" {
  description = "Service account email to attach to the instance."
  type        = string
  default     = "default"
}

variable "source_image" {
  description = "Source image for the boot disk."
  type        = string
  default     = "projects/debian-cloud/global/images/family/debian-11"
}

variable "vpc_network" {
  description = "VPC network self link or name."
  type        = string
  default     = "default"
}

variable "zone" {
  description = "Zone for the GCE instance."
  type        = string
  default     = "us-central1-a"
}

