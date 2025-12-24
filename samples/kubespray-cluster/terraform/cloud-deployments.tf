data "pxc_cluster_vars" "cvars" {}

locals {
  cluster_vars = yamldecode(data.pxc_cluster_vars.cvars.vars)
}

# the cloud controller connects your cluster with the postgres running inside the lxc containers from the cloud-instance directory
# it takes care of automatically synchronizing tls secrets, making dns record based on ingress resources, ...
# additional functionaltity is triggered by setting additional terraform variables defined in the modules spec
module "cloud_controller" {
  source = "Proxmox-Cloud/controller/pxc"
  version = "" # start with the latest and fixate it here
  k8s_stack_fqdn = "${local.inventory.stack_name}.${local.cluster_vars.pve_cloud_domain}"

  cluster_cert_entries = local.inventory.cluster_cert_entries
  external_domains = local.inventory.external_domains
}