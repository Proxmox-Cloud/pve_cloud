# the cloud controller connects your cluster with the postgres running inside the lxc containers from the cloud-instance directory
# it takes care of automatically synchronizing tls secrets, making dns record based on ingress resources, ...
# additional functionaltity is triggered by setting additional terraform variables defined in the modules spec
module "cloud_controller" {
  source = "git@github.com:Proxmox-Cloud/pve-cloud-tf.git//modules/controller?ref=$NEWEST_TAG"
  k8s_stack_fqdn = "${local.inventory.stack_name}.${var.pve_cloud_domain}"
  pg_conn_str = var.pve_cloud_pg_cstr
  
  bind_master_ip = var.bind_master_ip
  bind_dns_update_key = var.bind_internal_key
  internal_proxy_floating_ip = var.cluster_proxy_ip

  cluster_cert_entries = local.inventory.cluster_cert_entries
}