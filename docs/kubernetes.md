# Kubespray K8S

Our main platform for running workloads is kubernetes. For this the collection contains and integrates with the official kubespray collection.

## Deploying a cluster

Again create custom inventory yaml file following this [cluster schema](schemas/kubespray_inv_schema.md).

Afterwards run the `pve.cloud.sync_kubespray` playbook.

* `config` - for changes to the pve cloud infrastructure (proxy, dns, dhcp)
* `kubespray` - for only triggering the kubespray playbook that sets up the k8s cluster
* `acme` -  for only generating / updating letsencrypt certificates
* `deployments` -  for only installing / upgrading helm core deployments

to temporarily download the kubeconf after creation of the cluster (with expiring access) use:

`pvcli print-kubeconfig --inventory YOUR-KUBESPRAY-INV.yaml`

## Upgrading a cluster

Based on the compatibility table on the starting page, upgrade step by step based on k8s minor versions. You can skip patch versions.

To upgrade simply increment the version of this ansible collection based on the table in your `requirements.yaml`, run `ansible-galaxy install -r requirements.yaml` again and then execute the upgrade playbook `ansible-playbook -i YOUR-KUBESPRAY-INV.yaml pve.cloud.upgrade_kubespray`.

## Custom kubespray vars

to define your own kubespray vars just create `group_vars/all` and `group_vars/k8s_cluster` directories alongside your inventory file.

here are some interesting kubespray settings you might want to set (k8s_cluster vars):

* increase amount of schedulable pods per node (if you have big nodes)
```yaml
kube_network_node_prefix: 22
kubelet_max_pods: 1024
```
* set strict eviction limits, this is a good safe guard for node availability incase you have memory hungry deployments without any requests / limits defined 
```yaml
# this will enable reservations with the default values, see kubespray sample inventory
kube_reserved: true
kube_reserved_cgroups_for_service_slice: kube.slice
kube_reserved_cgroups: "/{{ kube_reserved_cgroups_for_service_slice }}"

system_reserved: true
system_reserved_cgroups_for_service_slice: system.slice
system_reserved_cgroups: "/{{ system_reserved_cgroups_for_service_slice }}"
system_memory_reserved: 1024Mi

eviction_hard:
  memory.available: 1000Mi
```
=> this, in addition to the `adjust_networkd_oom_score` role, will allow k8s nodes to run even if we got memory hungry, ram unlimited deployments. eviction hard and reservations alone are not enough, in oom scenarios it will cause the networkd service to stop working.


## Tls acme certificates

if you set the route53 option in the inventory yaml, you also need to manually create the corresponding tls secrets on one of the pve cluster hosts.

* for aws route53 create `/etc/pve/cloud/secrets/aws-route53-global.json`, this should contain rw access to your route53:
```json
{
  "AWS_ACCESS_KEY_ID": "ACCESS_ID_HERE",
  "AWS_SECRET_ACCESS_KEY": "SECRET_KEY_HERE",
  "AWS_REGION": "REGION"
}
```

* for method `ionos` create `/etc/pve/cloud/secrets/ionos-api-key.json`:
```json
{
  "IONOS_PRAEFIX": "PRAEFIX_HERE",
  "IONOS_VERSCHLUESSELUNG": "SECRET_KEY_HERE"
}
```

afterwards you need to sync those secrets to all hosts in the cloud, you can do that by rerunning the `setup_pve_clusters` playbook - `ansible-playbook -i YOUR-CLOUD-INV.yaml pve.cloud.setup_pve_clusters --tags rsync`. This needs to be done only once! There is no support for multiple dns providers / multiple accounts yet.

## Custom Api SANS

Set the `extra_control_plane_sans` variable to a list of extra sans that you want included in kubeapi certificates. This is needed primarily if you want to expose your cluster to the www to be accessed for example by ArgoCD or Vault under a different hostname than your internal cloud domain. 

This will also cause the haproxy frontend thats dedicated for external control planes to route traffic based on sni.

You will have to create internal and external dns records by yourself, the terraform dns/route53 provider is a good option.

## Terraform

To configure the kubernetes cluster you should create a terraform folder next to your kubespray inventory yaml. 

Also checkout the `pve-cloud-tf` repository for modules to install into your cluster, there you will find samples for easy auth with ssh for terraform into k8s.

## AWX

The playbooks for tls create the initial certificates but do not renew them. Setup the `pve-cloud-awx-cron` repository inside your awx instance as a project and follow the README.md to setup the cron job.