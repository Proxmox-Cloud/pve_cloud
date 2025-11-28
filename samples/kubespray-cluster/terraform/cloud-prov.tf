terraform {
  backend "pg" {} # sourced entirely via .envrc
}

locals {
  inventory = yamldecode(file("../kubespray-inv.yaml"))
  pve_inventory = yamldecode(file("${pathexpand("~/.pve-cloud-dyn-inv.yaml")}"))
}

locals {
  kubeconfig = yamldecode(base64decode(var.master_b64_kubeconf))
}

provider "kubernetes" {
  client_certificate = base64decode(local.kubeconfig.users[0].user.client-certificate-data)
  client_key = base64decode(local.kubeconfig.users[0].user.client-key-data)
  host = "https://control-plane-${local.inventory.stack_name}.${var.pve_cloud_domain}:6443" # connect to load balanced control plane
  cluster_ca_certificate = base64decode(local.kubeconfig.clusters[0].cluster.certificate-authority-data)
}

provider "helm" {
  kubernetes = {
    client_certificate = base64decode(local.kubeconfig.users[0].user.client-certificate-data)
    client_key = base64decode(local.kubeconfig.users[0].user.client-key-data)
    host = "https://control-plane-${local.inventory.stack_name}.${var.pve_cloud_domain}:6443" # connect to load balanced control plane
    cluster_ca_certificate = base64decode(local.kubeconfig.clusters[0].cluster.certificate-authority-data)
  }
}
