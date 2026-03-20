# Cloud Architecture

The collection is made of the following artifacts, you can find all the repositories in our github org.

```puml
@startuml

' Top-down hierarchy
top to bottom direction

' Define objects instead of packages
object "py-pve-cloud" as py_pve_cloud {
   * <u>pypi package</u>
   * libary
   * cli tools
   * postgres ORM
}

object "terraform-provider-pxc" as terraform_provider {
  * <u>terraform provider</u>
  * cloud secrets datasources
  * grpc go client
  * grpc py server (using py-pve-cloud)
}

object "terraform-pxc-controller" as controller_module {
  * <u>terraform modules</u>
  * K8s deployments + cron job
  * Admission controller
  * Ingress DNS
  * Namespace watcher
}

object "terraform-pxc-backup" as backup_module {
  * <u>terraform module</u>
  * K8s backup fetcher cron
  * Patroni db dumps
}

object "pve-cloud-controller" as controller_image {
  * <u>docker image</u>
  * admission controller
  * cron, watcher entrypoints
}

object "pve-cloud-backup" as backup_image {
  * <u>docker image</u> (k8s)
  * pypi artifact (pve)
}

object "pve_cloud" as cloud_collection {
  * <u>ansible collection</u> (pxc.cloud)
  * bootstrap playbooks
  * pve inventory plugins
}

object "pve-cloud-schemas" as cloud_schemas {
  * <u>pypi package</u>
  * json/yaml schema defs
  * general validation logic
}

object "pytest-pve-cloud" as pytest_pve_cloud {
  * <u>pypi package</u>
  * tdd testing tools
  * library for e2e
}

' Define edges (dependencies)
py_pve_cloud --> cloud_collection
py_pve_cloud --> controller_image
py_pve_cloud --> pytest_pve_cloud
py_pve_cloud --> terraform_provider
py_pve_cloud --> backup_image

terraform_provider --> controller_module
terraform_provider --> backup_module

controller_image --> controller_module
backup_image --> backup_module
backup_image --> cloud_collection

cloud_schemas --> cloud_collection

@enduml
```

## Terminology

The collection and projects use certain terms to define scope, which enables a lot of implicit behaviour.

* `pve_cloud_domain`: this is the main domain name you select for your cloud instance. Think of it as having one personal aws per domain.
* `target_pve`: this refers to a proxmox cluster within a domain. Its the result of the proxmox cluster name defined in the proxmox ui + `(.)pve_cloud_domain`
* `stack_name`: each set of vms / lxcs you deploy is referred to as a stack. Each kubespray cluster is its own stack also.
* `stack_fqdn`: this referes to the `stack_name` + `(.)pve_cloud_domain` and serves to identify the stack uniquely
