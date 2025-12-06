# all of these variables are filled automatically via .envrc
# from eval pvcli. They are used by pve-cloud-tf modules and to init
# providers
variable "pve_cloud_domain" {
  type = string
  description = "The cloud domain this cluster is a part of."
}

variable "cluster_proxy_ip" {
  type = string
  description = "The internal floating ip of our haproxy stack."
}

variable "pve_host" {
  type = string
  description = "Returns the host ip of an online proxmox host from the target_pve cluster. Useful for interacting with the api and to fetch pve cloud secrets via ssh external provider."
}

variable "pve_cloud_pg_cstr" {
  type = string
  description = "Patroni postgres stack connection string => passed down to deployments."
}

variable "master_b64_kubeconf" {
  type = string
  description = "Kubeconfig from master fetched via ssh => init providers."
}

variable "bind_master_ip" {
  type = string
  description = "IP of central DNS server of the cloud => passed down and can be used to init dns provider."
}

variable "bind_internal_key" {
  type = string
  description = "Default key that allows making records to all zones declared as authoritative in the kubespray inv file."
}