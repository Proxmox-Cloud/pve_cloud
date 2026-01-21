data "pxc_cloud_self" "self" {}

locals {
  cluster_vars = yamldecode(data.pxc_cloud_self.self.cluster_vars)
}

# the cloud controller connects your cluster with the postgres running inside the lxc containers from the cloud-instance directory
# it takes care of automatically synchronizing tls secrets, making dns record based on ingress resources, ...
# additional functionaltity is triggered by setting additional terraform variables defined in the modules spec
module "cloud_controller" {
  source = "Proxmox-Cloud/controller/pxc"
  version = "" # start with the latest and fixate it here
}