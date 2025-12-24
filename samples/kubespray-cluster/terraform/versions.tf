terraform {
  required_providers {
    helm = {
      source = "hashicorp/helm"
      version = ""
    }
    kubernetes = {
      source = "hashicorp/kubernetes"
      version = "" # start with the latest and fixate it here
    }
    pxc = {
      source = "Proxmox-Cloud/pxc"
      version = ""
    }
  }
}