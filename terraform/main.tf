terraform {
  required_version = ">= 1.5.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_compute_instance" "jenkins_controller" {
  name         = var.instance_name
  machine_type = var.machine_type
  zone         = var.zone

  tags = ["http-server", "${var.instance_name}-http", "${var.instance_name}-https"]

  boot_disk {
    initialize_params {
      image = var.source_image
      size  = var.boot_disk_size_gb
      type  = var.boot_disk_type
    }
  }

  network_interface {
    network = var.vpc_network

    access_config {
      // Ephemeral public IP
    }
  }

  service_account {
    email  = var.service_account_email
    scopes = ["https://www.googleapis.com/auth/cloud-platform"]
  }

  metadata = var.instance_metadata
}

resource "google_compute_firewall" "jenkins_http_https" {
  name    = "${var.instance_name}-allow-http-https"
  network = var.vpc_network

  direction     = "INGRESS"
  priority      = 1000
  target_tags   = google_compute_instance.jenkins_controller.tags
  source_ranges = var.http_https_source_ranges

  allow {
    protocol = "tcp"
    ports    = ["80", "443"]
  }
}

resource "google_compute_firewall" "allow_jenkins_ui" {
  name    = "allow-jenkins-ui"
  network = var.vpc_network

  direction     = "INGRESS"
  priority      = 1000
  target_tags   = ["http-server"]
  source_ranges = var.jenkins_ui_source_ranges

  allow {
    protocol = "tcp"
    ports    = ["8080"]
  }
}

