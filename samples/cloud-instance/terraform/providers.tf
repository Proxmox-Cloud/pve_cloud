terraform {
  backend "pg" {} # sourced entirely via .envrc
}

provider "pxc" {
  inventory = "../cloud-inv.yaml"
  target_cluster = "pve-cluster-name"
}

