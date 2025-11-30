# Kubespray K8S

The collection contains and integrates with the official kubespray collection.

It is recommended to create a seperate repository per kubernetes cluster, or aleast put the cluster inventory file into a seperate folder.

Checkout the `kubespray-cluster` dir in the [samples directory](https://github.com/Proxmox-Cloud/pve_cloud/tree/master/samples) for a quick idea on how to setup!

## Deploying a cluster

Again create custom inventory yaml file following this [k8s cluster schema](schemas/kubespray_inv_schema.md).

Afterwards run the `pve.cloud.sync_kubespray` playbook, this will fully create VMs, setup kubespray, initialize TLS Certificates and deploy core kubernetes helm charts (Ceph CSI, Ingress).

To get kubeconf after creation of the cluster for cli/ide access (expiring) use:

`pvcli print-kubeconfig --inventory YOUR-KUBESPRAY-INV.yaml`


## TLS ACME Certificates

This collection doesn't use kubernetes certmanager for TLS certificates, but instead comes with an external centralised solution. 

Initially certificates are generated via ansible roles, integrated into the collection. The update process afterwards is handled via [AWX cron jobs](https://github.com/Proxmox-Cloud/pve-cloud-awx-cron). Use the awx helm chart via terraform to deploy your own instance.

### DNS Provider Secrets

At the moment the collection supports ionos and aws route53 for dynamically solving dns01 challenges and obtaining certificates.

You need to create secret files inside the clouds secret folder on your proxmox cluster:

* for aws route53 create `/etc/pve/cloud/secrets/aws-route53-global.json`, this should contain read / write access to your route53:
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

Afterwards you need to sync those secrets to all hosts in the cloud, you can do that by rerunning the `setup_pve_clusters` playbook - `ansible-playbook -i YOUR-CLOUD-INV.yaml pve.cloud.setup_pve_clusters --tags rsync`. This needs to be done only once! There is no support for multiple dns providers / multiple accounts yet.

You are welcome to create and submit a MR with your own roles / logic for other providers!


## Upgrading a cluster

Upgrading the cluster is as simple as updating the version tag reference of this collection.

You can skip to the latest patch version, but shouldn't skip minor versions as they are tied to kubespray updates. After updating the cloud collection version in your requirements.yaml, you have to run `ansible-galaxy install -r requirements.yaml` and `pip install -r ~/.ansible/collections/ansible_collections/pve/cloud/meta/ee-requirements.txt` again.

Then run the upgrade playbook `ansible-playbook -i YOUR-KUBESPRAY-INV.yaml pve.cloud.upgrade_kubespray`.

Right now kubespray is tightly coupled with the entire collection, meaning you have to update the collection a minor version, then update all your clusters, then the collection again and so forth. In the future this will be split to make it more versatile. There is a version lock for the collection that will prevent you from doing updates, if you do this in any other order.

## Custom kubespray vars

To define your own kubespray vars just create `group_vars/all` and `group_vars/k8s_cluster` directories alongside your inventory file.

Here are some interesting kubespray settings you might want to set (k8s_cluster vars):

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
=> this, in addition to the `adjust_networkd_oom_score` role, will allow k8s nodes to run even if we got memory hungry, ram hogging deployments. eviction hard and reservations alone are not enough, in oom scenarios it will cause the networkd service to stop working.


## Exposing K8S Controlplane API

If you want to expose your kubenetes clusters controlplane to integrate with external running services, you can set additional SANs that will be generated and inserted by kubespray into the kubeapi certificates, by listing them in your kubespray inventory file under `extra_control_plane_sans` as simple strings.

Adding SANs there will also configure the pve cloud haproxy to route any control plane traffic (6443) on its external ip to respecive cluster.

DNS Records for these SANs have to be created manually (for internal and external DNS servers), for that use terraforms dns, route53 and ionos provider.

## Terraform

After you deployed your first kubernetes cluster, further deployments and configuration is handled almost exclusively via terraform.

Checkout the [pve-cloud-tf repository](https://github.com/Proxmox-Cloud/pve-cloud-tf), for core pve cloud related deployments.
