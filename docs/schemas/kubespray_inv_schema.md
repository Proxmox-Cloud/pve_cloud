# K8s Kubespray Inventory

**Title:** K8s Kubespray Inventory

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

**Description:** Inventory for deploying k8s clusters via kubespray on PVE.

| Property                                                 | Pattern | Type             | Deprecated | Definition | Title/Description                                                                                                                                                                                                                                                             |
| -------------------------------------------------------- | ------- | ---------------- | ---------- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| + [target_pve](#target_pve )                             | No      | string           | No         | -          | Proxmox cluster name + . + pve cloud domain. This determines the cloud and the proxmox cluster the vms/lxc/k8s luster will be created in.                                                                                                                                     |
| + [stack_name](#stack_name )                             | No      | string           | No         | -          | Your stack name, needs to be unique within the cloud domain.                                                                                                                                                                                                                  |
| + [static_includes](#static_includes )                   | No      | object           | No         | -          | -                                                                                                                                                                                                                                                                             |
| - [include_stacks](#include_stacks )                     | No      | array of object  | No         | -          | Include other stacks into the ansible inventory, from any pve cloud you are connected to. From here you can freely extend and write your own playbooks.                                                                                                                       |
| + [root_ssh_pub_key](#root_ssh_pub_key )                 | No      | string           | No         | -          | trusted root key for the cloud init image.                                                                                                                                                                                                                                    |
| - [pve_ha_group](#pve_ha_group )                         | No      | string           | No         | -          | PVE HA group this vm should be assigned to (optional).                                                                                                                                                                                                                        |
| - [pve_cloud_pytest](#pve_cloud_pytest )                 | No      | object           | No         | -          | Variables object used only in e2e tests.                                                                                                                                                                                                                                      |
| + [qemus](#qemus )                                       | No      | array of object  | No         | -          | Nodes for the cluster in form of qemu vms.                                                                                                                                                                                                                                    |
| - [qemu_default_user](#qemu_default_user )               | No      | string           | No         | -          | User for cinit.                                                                                                                                                                                                                                                               |
| - [qemu_hashed_pw](#qemu_hashed_pw )                     | No      | string           | No         | -          | Pw for default user defaults to hashed 'password' for debian cloud init image. Different cloud init images require different hash methods. You cannot use the same from debian for ubuntu for example.                                                                        |
| - [qemu_base_parameters](#qemu_base_parameters )         | No      | object           | No         | -          | Base parameters applied to all qemus. passed to the proxmox qm cli tool for creating vm.                                                                                                                                                                                      |
| - [qemu_image_url](#qemu_image_url )                     | No      | string           | No         | -          | http(s) download link for cloud init image.                                                                                                                                                                                                                                   |
| - [qemu_keyboard_layout](#qemu_keyboard_layout )         | No      | string           | No         | -          | Keyboard layout for cloudinit.                                                                                                                                                                                                                                                |
| - [qemu_network_config](#qemu_network_config )           | No      | string           | No         | -          | Optional qemu network config as a yaml string that is merged into the cloudinit network config of all qemus.                                                                                                                                                                  |
| - [qemu_global_vars](#qemu_global_vars )                 | No      | object           | No         | -          | Variables that will be applied set for all qemus vms.                                                                                                                                                                                                                         |
| - [plugin](#plugin )                                     | No      | enum (of string) | No         | -          | Id of ansible inventory plugin.                                                                                                                                                                                                                                               |
| - [extra_control_plane_sans](#extra_control_plane_sans ) | No      | array of string  | No         | -          | Extra sans that kubespray will put in kubeapi generated certificates. Original kubespray variable is named supplementary_addresses_in_ssl_keys, <br />but is set via pve cloud kubespray custom inventory. Read the kubernetes page in pve cloud docs for more details.<br /> |
| - [external_domains](#external_domains )                 | No      | array of object  | No         | -          | Domains that will be exposed to the public/external haproxy floating ip via haproxy sni matching to this cluster.                                                                                                                                                             |
| + [cluster_cert_entries](#cluster_cert_entries )         | No      | array of object  | No         | -          | Content for the clusters acme tls certificate. If you have multiple proxmox clusters they need their own haproxy instances for ingress dns to work.                                                                                                                           |
| + [tcp_proxies](#tcp_proxies )                           | No      | array of object  | No         | -          | Raw tcp forwards on the clusters haproxy to k8s services exposed via nodeport.                                                                                                                                                                                                |
| + [ceph_csi_sc_pools](#ceph_csi_sc_pools )               | No      | array of object  | No         | -          | Ceph pools that will be made available to the cluster CSI driver.                                                                                                                                                                                                             |
| - [acme_staging](#acme_staging )                         | No      | boolean          | No         | -          | If set to true will use acme staging directory for issueing certs.                                                                                                                                                                                                            |

## <a name="target_pve"></a>1. Property `K8s Kubespray Inventory > target_pve`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Proxmox cluster name + . + pve cloud domain. This determines the cloud and the proxmox cluster the vms/lxc/k8s luster will be created in.

**Example:**

```json
"proxmox-cluster-a.your-cloud.domain"
```

## <a name="stack_name"></a>2. Property `K8s Kubespray Inventory > stack_name`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Your stack name, needs to be unique within the cloud domain.

## <a name="static_includes"></a>3. Property `K8s Kubespray Inventory > static_includes`

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | Yes         |
| **Additional properties** | Not allowed |

| Property                                             | Pattern | Type   | Deprecated | Definition | Title/Description                                                                                                                                      |
| ---------------------------------------------------- | ------- | ------ | ---------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| + [dhcp_stack](#static_includes_dhcp_stack )         | No      | string | No         | -          | The pve.cloud.sync_kubespray playbook needs the dhcp stack to refresh the configuration after having made static reservations for kubernetes node ips. |
| + [proxy_stack](#static_includes_proxy_stack )       | No      | string | No         | -          | The playbook needs to reload the central clusters haproxy for various forwarding specifications.                                                       |
| + [postgres_stack](#static_includes_postgres_stack ) | No      | string | No         | -          | The playbook needs the pve cloud postgres stack where state and general configuration is stored.                                                       |
| + [bind_stack](#static_includes_bind_stack )         | No      | string | No         | -          | The playbook needs the bind stack to register the general masters recordset and for creating authoritative zones defined in cluster_cert_entries.      |
| - [cache_stack](#static_includes_cache_stack )       | No      | string | No         | -          | Cache stack to mount nfs for kubespray cache and apt cache. Assumes the cache lxc to have the hostname "main". WIP!                                    |

### <a name="static_includes_dhcp_stack"></a>3.1. Property `K8s Kubespray Inventory > static_includes > dhcp_stack`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** The pve.cloud.sync_kubespray playbook needs the dhcp stack to refresh the configuration after having made static reservations for kubernetes node ips.

**Example:**

```json
"dhcp.your-cloud.domain"
```

### <a name="static_includes_proxy_stack"></a>3.2. Property `K8s Kubespray Inventory > static_includes > proxy_stack`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** The playbook needs to reload the central clusters haproxy for various forwarding specifications.

**Example:**

```json
"proxy.your-cloud.domain"
```

### <a name="static_includes_postgres_stack"></a>3.3. Property `K8s Kubespray Inventory > static_includes > postgres_stack`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** The playbook needs the pve cloud postgres stack where state and general configuration is stored.

**Example:**

```json
"patroni.your-cloud.domain"
```

### <a name="static_includes_bind_stack"></a>3.4. Property `K8s Kubespray Inventory > static_includes > bind_stack`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** The playbook needs the bind stack to register the general masters recordset and for creating authoritative zones defined in cluster_cert_entries.

**Example:**

```json
"bind.your-cloud.domain"
```

### <a name="static_includes_cache_stack"></a>3.5. Property `K8s Kubespray Inventory > static_includes > cache_stack`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Cache stack to mount nfs for kubespray cache and apt cache. Assumes the cache lxc to have the hostname "main". WIP!

## <a name="include_stacks"></a>4. Property `K8s Kubespray Inventory > include_stacks`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | No                |

**Description:** Include other stacks into the ansible inventory, from any pve cloud you are connected to. From here you can freely extend and write your own playbooks.

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be               | Description |
| --------------------------------------------- | ----------- |
| [include_stacks items](#include_stacks_items) | -           |

### <a name="include_stacks_items"></a>4.1. K8s Kubespray Inventory > include_stacks > include_stacks items

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

| Property                                                        | Pattern | Type   | Deprecated | Definition | Title/Description                                                                                                                                                                                                                  |
| --------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| + [stack_fqdn](#include_stacks_items_stack_fqdn )               | No      | string | No         | -          | Target stack fqdn to include (stack name + pve_cloud_domain). Will automatically include it from the right pve cluster.                                                                                                            |
| + [host_group](#include_stacks_items_host_group )               | No      | string | No         | -          | This is the name of the hosts group of our ansible inventory the included vms/lxcs will be available under.                                                                                                                        |
| - [qemu_ansible_user](#include_stacks_items_qemu_ansible_user ) | No      | string | No         | -          | User ansible will use to connect, defaults to admin. If you dont want to use debian cinit images you might need to set something else than admin.<br />Ubuntu for example wont work if you set the cloud init user to admin.<br /> |

#### <a name="include_stacks_items_stack_fqdn"></a>4.1.1. Property `K8s Kubespray Inventory > include_stacks > include_stacks items > stack_fqdn`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Target stack fqdn to include (stack name + pve_cloud_domain). Will automatically include it from the right pve cluster.

**Examples:**

```json
"bind.your-other-cloud.domain"
```

```json
"other-k8s.your-other-cloud.domain"
```

#### <a name="include_stacks_items_host_group"></a>4.1.2. Property `K8s Kubespray Inventory > include_stacks > include_stacks items > host_group`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** This is the name of the hosts group of our ansible inventory the included vms/lxcs will be available under.

#### <a name="include_stacks_items_qemu_ansible_user"></a>4.1.3. Property `K8s Kubespray Inventory > include_stacks > include_stacks items > qemu_ansible_user`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** User ansible will use to connect, defaults to admin. If you dont want to use debian cinit images you might need to set something else than admin.
Ubuntu for example wont work if you set the cloud init user to admin.

## <a name="root_ssh_pub_key"></a>5. Property `K8s Kubespray Inventory > root_ssh_pub_key`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** trusted root key for the cloud init image.

## <a name="pve_ha_group"></a>6. Property `K8s Kubespray Inventory > pve_ha_group`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** PVE HA group this vm should be assigned to (optional).

## <a name="pve_cloud_pytest"></a>7. Property `K8s Kubespray Inventory > pve_cloud_pytest`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Variables object used only in e2e tests.

## <a name="qemus"></a>8. Property `K8s Kubespray Inventory > qemus`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | Yes               |

**Description:** Nodes for the cluster in form of qemu vms.

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be | Description |
| ------------------------------- | ----------- |
| [qemus items](#qemus_items)     | -           |

### <a name="qemus_items"></a>8.1. K8s Kubespray Inventory > qemus > qemus items

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

| Property                                         | Pattern | Type                      | Deprecated | Definition | Title/Description                                                                                                                                                       |
| ------------------------------------------------ | ------- | ------------------------- | ---------- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| - [hostname](#qemus_items_hostname )             | No      | string                    | No         | -          | Optional unique hostname for this node, otherwise pet name random name will be generated.                                                                               |
| - [vars](#qemus_items_vars )                     | No      | object                    | No         | -          | Custom variables for this node specifically, might be useful in your own custom playbooks.                                                                              |
| - [target_host](#qemus_items_target_host )       | No      | string                    | No         | -          | Optional specific proxmox host you want to tie this node to on creation. Can of course still be moved afterwards. Cloud domain is implicit and should not be specified. |
| + [parameters](#qemus_items_parameters )         | No      | object                    | No         | -          | In accordance with pve qm cli tool, creation parameters mapped (key equals the --key part and value the passed value).                                                  |
| - [network_config](#qemus_items_network_config ) | No      | string                    | No         | -          | Cinit network config yaml string. Will be the last cfg piece that gets merged into the final cloudinit network config. Can be used for overrides.                       |
| + [disk](#qemus_items_disk )                     | No      | object                    | No         | -          | -                                                                                                                                                                       |
| + [k8s_roles](#qemus_items_k8s_roles )           | No      | array of enum (of string) | No         | -          | String array of k8s roles.                                                                                                                                              |

#### <a name="qemus_items_hostname"></a>8.1.1. Property `K8s Kubespray Inventory > qemus > qemus items > hostname`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Optional unique hostname for this node, otherwise pet name random name will be generated.

#### <a name="qemus_items_vars"></a>8.1.2. Property `K8s Kubespray Inventory > qemus > qemus items > vars`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Custom variables for this node specifically, might be useful in your own custom playbooks.

#### <a name="qemus_items_target_host"></a>8.1.3. Property `K8s Kubespray Inventory > qemus > qemus items > target_host`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Optional specific proxmox host you want to tie this node to on creation. Can of course still be moved afterwards. Cloud domain is implicit and should not be specified.

**Example:**

```json
"proxmox-host-B.proxmox-cluster-A"
```

#### <a name="qemus_items_parameters"></a>8.1.4. Property `K8s Kubespray Inventory > qemus > qemus items > parameters`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | Yes              |
| **Additional properties** | Any type allowed |

**Description:** In accordance with pve qm cli tool, creation parameters mapped (key equals the --key part and value the passed value).

**Example:**

```json
{
    "cores": 1,
    "memory": 1024
}
```

#### <a name="qemus_items_network_config"></a>8.1.5. Property `K8s Kubespray Inventory > qemus > qemus items > network_config`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Cinit network config yaml string. Will be the last cfg piece that gets merged into the final cloudinit network config. Can be used for overrides.

#### <a name="qemus_items_disk"></a>8.1.6. Property `K8s Kubespray Inventory > qemus > qemus items > disk`

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | Yes         |
| **Additional properties** | Not allowed |

| Property                                | Pattern | Type   | Deprecated | Definition | Title/Description                               |
| --------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------------------------------------- |
| + [size](#qemus_items_disk_size )       | No      | string | No         | -          | Size of the vms disk.                           |
| - [options](#qemus_items_disk_options ) | No      | object | No         | -          | Mount options                                   |
| + [pool](#qemus_items_disk_pool )       | No      | string | No         | -          | Ceph pool name the vms disk will be created in. |

##### <a name="qemus_items_disk_size"></a>8.1.6.1. Property `K8s Kubespray Inventory > qemus > qemus items > disk > size`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Size of the vms disk.

**Example:**

```json
"25G"
```

##### <a name="qemus_items_disk_options"></a>8.1.6.2. Property `K8s Kubespray Inventory > qemus > qemus items > disk > options`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Mount options

##### <a name="qemus_items_disk_pool"></a>8.1.6.3. Property `K8s Kubespray Inventory > qemus > qemus items > disk > pool`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Ceph pool name the vms disk will be created in.

#### <a name="qemus_items_k8s_roles"></a>8.1.7. Property `K8s Kubespray Inventory > qemus > qemus items > k8s_roles`

|              |                             |
| ------------ | --------------------------- |
| **Type**     | `array of enum (of string)` |
| **Required** | Yes                         |

**Description:** String array of k8s roles.

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                 | Description |
| ----------------------------------------------- | ----------- |
| [k8s_roles items](#qemus_items_k8s_roles_items) | -           |

##### <a name="qemus_items_k8s_roles_items"></a>8.1.7.1. K8s Kubespray Inventory > qemus > qemus items > k8s_roles > k8s_roles items

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |

Must be one of:
* "master"
* "worker"

## <a name="qemu_default_user"></a>9. Property `K8s Kubespray Inventory > qemu_default_user`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** User for cinit.

## <a name="qemu_hashed_pw"></a>10. Property `K8s Kubespray Inventory > qemu_hashed_pw`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Pw for default user defaults to hashed 'password' for debian cloud init image. Different cloud init images require different hash methods. You cannot use the same from debian for ubuntu for example.

## <a name="qemu_base_parameters"></a>11. Property `K8s Kubespray Inventory > qemu_base_parameters`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Base parameters applied to all qemus. passed to the proxmox qm cli tool for creating vm.

## <a name="qemu_image_url"></a>12. Property `K8s Kubespray Inventory > qemu_image_url`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** http(s) download link for cloud init image.

## <a name="qemu_keyboard_layout"></a>13. Property `K8s Kubespray Inventory > qemu_keyboard_layout`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Keyboard layout for cloudinit.

## <a name="qemu_network_config"></a>14. Property `K8s Kubespray Inventory > qemu_network_config`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Optional qemu network config as a yaml string that is merged into the cloudinit network config of all qemus.

## <a name="qemu_global_vars"></a>15. Property `K8s Kubespray Inventory > qemu_global_vars`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Variables that will be applied set for all qemus vms.

## <a name="plugin"></a>16. Property `K8s Kubespray Inventory > plugin`

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |

**Description:** Id of ansible inventory plugin.

Must be one of:
* "pve.cloud.qemu_inv"
* "pve.cloud.kubespray_inv"

## <a name="extra_control_plane_sans"></a>17. Property `K8s Kubespray Inventory > extra_control_plane_sans`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of string` |
| **Required** | No                |

**Description:** Extra sans that kubespray will put in kubeapi generated certificates. Original kubespray variable is named supplementary_addresses_in_ssl_keys, 
but is set via pve cloud kubespray custom inventory. Read the kubernetes page in pve cloud docs for more details.

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                                   | Description |
| ----------------------------------------------------------------- | ----------- |
| [extra_control_plane_sans items](#extra_control_plane_sans_items) | -           |

### <a name="extra_control_plane_sans_items"></a>17.1. K8s Kubespray Inventory > extra_control_plane_sans > extra_control_plane_sans items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="external_domains"></a>18. Property `K8s Kubespray Inventory > external_domains`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | No                |

**Description:** Domains that will be exposed to the public/external haproxy floating ip via haproxy sni matching to this cluster.

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                   | Description |
| ------------------------------------------------- | ----------- |
| [external_domains items](#external_domains_items) | -           |

### <a name="external_domains_items"></a>18.1. K8s Kubespray Inventory > external_domains > external_domains items

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

| Property                                              | Pattern | Type            | Deprecated | Definition | Title/Description                                                                                                      |
| ----------------------------------------------------- | ------- | --------------- | ---------- | ---------- | ---------------------------------------------------------------------------------------------------------------------- |
| + [zone](#external_domains_items_zone )               | No      | string          | No         | -          | DNS parent zone, should also be the zone that external records are made under in AWS for example.                      |
| - [expose_apex](#external_domains_items_expose_apex ) | No      | boolean         | No         | -          | Expose the apex zone itself. For example if you have zone example.com then example.com will be routed to this cluster. |
| + [names](#external_domains_items_names )             | No      | array of string | No         | -          | -                                                                                                                      |

#### <a name="external_domains_items_zone"></a>18.1.1. Property `K8s Kubespray Inventory > external_domains > external_domains items > zone`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** DNS parent zone, should also be the zone that external records are made under in AWS for example.

#### <a name="external_domains_items_expose_apex"></a>18.1.2. Property `K8s Kubespray Inventory > external_domains > external_domains items > expose_apex`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |

**Description:** Expose the apex zone itself. For example if you have zone example.com then example.com will be routed to this cluster.

#### <a name="external_domains_items_names"></a>18.1.3. Property `K8s Kubespray Inventory > external_domains > external_domains items > names`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of string` |
| **Required** | Yes               |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                    | Description                               |
| -------------------------------------------------- | ----------------------------------------- |
| [names items](#external_domains_items_names_items) | Names of the zone that should be exposed. |

##### <a name="external_domains_items_names_items"></a>18.1.3.1. K8s Kubespray Inventory > external_domains > external_domains items > names > names items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Names of the zone that should be exposed.

**Examples:**

```json
"*"
```

```json
"example-service"
```

```json
"*.subzone"
```

## <a name="cluster_cert_entries"></a>19. Property `K8s Kubespray Inventory > cluster_cert_entries`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | Yes               |

**Description:** Content for the clusters acme tls certificate. If you have multiple proxmox clusters they need their own haproxy instances for ingress dns to work.

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                           | Description |
| --------------------------------------------------------- | ----------- |
| [cluster_cert_entries items](#cluster_cert_entries_items) | -           |

### <a name="cluster_cert_entries_items"></a>19.1. K8s Kubespray Inventory > cluster_cert_entries > cluster_cert_entries items

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

| Property                                                                | Pattern | Type            | Deprecated | Definition | Title/Description                                                                                                                                                    |
| ----------------------------------------------------------------------- | ------- | --------------- | ---------- | ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| + [zone](#cluster_cert_entries_items_zone )                             | No      | string          | No         | -          | DNS parent zone, should be the apex zone in ionos/route53 for dns01 challenge.                                                                                       |
| + [names](#cluster_cert_entries_items_names )                           | No      | array of string | No         | -          | -                                                                                                                                                                    |
| - [authoritative_zone](#cluster_cert_entries_items_authoritative_zone ) | No      | boolean         | No         | -          | This will cause the specified apex zone to be created as an authoritative zone in the proxmox clouds dns server. Ingress dns will only work for authoritative zones. |
| - [apex_zone_san](#cluster_cert_entries_items_apex_zone_san )           | No      | boolean         | No         | -          | Creates additional SAN for the zone, if you have *.example.com you will also get example.com in your certificate. Defaults to false.                                 |

#### <a name="cluster_cert_entries_items_zone"></a>19.1.1. Property `K8s Kubespray Inventory > cluster_cert_entries > cluster_cert_entries items > zone`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** DNS parent zone, should be the apex zone in ionos/route53 for dns01 challenge.

#### <a name="cluster_cert_entries_items_names"></a>19.1.2. Property `K8s Kubespray Inventory > cluster_cert_entries > cluster_cert_entries items > names`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of string` |
| **Required** | Yes               |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                        | Description                                                     |
| ------------------------------------------------------ | --------------------------------------------------------------- |
| [names items](#cluster_cert_entries_items_names_items) | SANs included in the certificate and basis for dns01 challenge. |

##### <a name="cluster_cert_entries_items_names_items"></a>19.1.2.1. K8s Kubespray Inventory > cluster_cert_entries > cluster_cert_entries items > names > names items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** SANs included in the certificate and basis for dns01 challenge.

**Examples:**

```json
"*"
```

```json
"example-service"
```

```json
"*.subzone"
```

#### <a name="cluster_cert_entries_items_authoritative_zone"></a>19.1.3. Property `K8s Kubespray Inventory > cluster_cert_entries > cluster_cert_entries items > authoritative_zone`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |

**Description:** This will cause the specified apex zone to be created as an authoritative zone in the proxmox clouds dns server. Ingress dns will only work for authoritative zones.

#### <a name="cluster_cert_entries_items_apex_zone_san"></a>19.1.4. Property `K8s Kubespray Inventory > cluster_cert_entries > cluster_cert_entries items > apex_zone_san`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |

**Description:** Creates additional SAN for the zone, if you have *.example.com you will also get example.com in your certificate. Defaults to false.

## <a name="tcp_proxies"></a>20. Property `K8s Kubespray Inventory > tcp_proxies`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | Yes               |

**Description:** Raw tcp forwards on the clusters haproxy to k8s services exposed via nodeport.

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be         | Description |
| --------------------------------------- | ----------- |
| [tcp_proxies items](#tcp_proxies_items) | -           |

### <a name="tcp_proxies_items"></a>20.1. K8s Kubespray Inventory > tcp_proxies > tcp_proxies items

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

| Property                                             | Pattern | Type    | Deprecated | Definition | Title/Description                                                                                                    |
| ---------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------------------------------------------------------------------------------------------------------- |
| + [proxy_name](#tcp_proxies_items_proxy_name )       | No      | string  | No         | -          | Simple name for the forward. Will be rendered in haproxy configuration so it shouldnt contain special characters.    |
| + [haproxy_port](#tcp_proxies_items_haproxy_port )   | No      | number  | No         | -          | Frontend port of the proxmox clusters haproxy.                                                                       |
| + [node_port](#tcp_proxies_items_node_port )         | No      | number  | No         | -          | Nodeport of the k8s service.                                                                                         |
| - [proxy_snippet](#tcp_proxies_items_proxy_snippet ) | No      | string  | No         | -          | Additional snippet that will be inserted into the haproxy listen block. Can be used to adjust the forwards settings. |
| - [external](#tcp_proxies_items_external )           | No      | boolean | No         | -          | Will also create a forward on the external floating ip of the proxy not only the internal.                           |

#### <a name="tcp_proxies_items_proxy_name"></a>20.1.1. Property `K8s Kubespray Inventory > tcp_proxies > tcp_proxies items > proxy_name`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Simple name for the forward. Will be rendered in haproxy configuration so it shouldnt contain special characters.

**Examples:**

```json
"gitlab-ssh"
```

```json
"example-postgres"
```

#### <a name="tcp_proxies_items_haproxy_port"></a>20.1.2. Property `K8s Kubespray Inventory > tcp_proxies > tcp_proxies items > haproxy_port`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

**Description:** Frontend port of the proxmox clusters haproxy.

#### <a name="tcp_proxies_items_node_port"></a>20.1.3. Property `K8s Kubespray Inventory > tcp_proxies > tcp_proxies items > node_port`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

**Description:** Nodeport of the k8s service.

#### <a name="tcp_proxies_items_proxy_snippet"></a>20.1.4. Property `K8s Kubespray Inventory > tcp_proxies > tcp_proxies items > proxy_snippet`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Additional snippet that will be inserted into the haproxy listen block. Can be used to adjust the forwards settings.

**Example:**

```json
"# long running tcp connections that only rarely transmit data\n# ssh client connection for example\ntimeout client 1h \ntimeout server 1h \n"
```

#### <a name="tcp_proxies_items_external"></a>20.1.5. Property `K8s Kubespray Inventory > tcp_proxies > tcp_proxies items > external`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |

**Description:** Will also create a forward on the external floating ip of the proxy not only the internal.

## <a name="ceph_csi_sc_pools"></a>21. Property `K8s Kubespray Inventory > ceph_csi_sc_pools`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | Yes               |

**Description:** Ceph pools that will be made available to the cluster CSI driver.

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                     | Description |
| --------------------------------------------------- | ----------- |
| [ceph_csi_sc_pools items](#ceph_csi_sc_pools_items) | -           |

### <a name="ceph_csi_sc_pools_items"></a>21.1. K8s Kubespray Inventory > ceph_csi_sc_pools > ceph_csi_sc_pools items

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

| Property                                                   | Pattern | Type    | Deprecated | Definition | Title/Description                                                                       |
| ---------------------------------------------------------- | ------- | ------- | ---------- | ---------- | --------------------------------------------------------------------------------------- |
| + [name](#ceph_csi_sc_pools_items_name )                   | No      | string  | No         | -          | Name of the pool in the ceph of our PVE cluster.                                        |
| + [default](#ceph_csi_sc_pools_items_default )             | No      | boolean | No         | -          | Whether or not the pool is the default storage class.                                   |
| + [mount_options](#ceph_csi_sc_pools_items_mount_options ) | No      | array   | No         | -          | String array of mount options that will be set in the storage class and applied to pvs. |

#### <a name="ceph_csi_sc_pools_items_name"></a>21.1.1. Property `K8s Kubespray Inventory > ceph_csi_sc_pools > ceph_csi_sc_pools items > name`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Name of the pool in the ceph of our PVE cluster.

#### <a name="ceph_csi_sc_pools_items_default"></a>21.1.2. Property `K8s Kubespray Inventory > ceph_csi_sc_pools > ceph_csi_sc_pools items > default`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

**Description:** Whether or not the pool is the default storage class.

#### <a name="ceph_csi_sc_pools_items_mount_options"></a>21.1.3. Property `K8s Kubespray Inventory > ceph_csi_sc_pools > ceph_csi_sc_pools items > mount_options`

|              |         |
| ------------ | ------- |
| **Type**     | `array` |
| **Required** | Yes     |

**Description:** String array of mount options that will be set in the storage class and applied to pvs.

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | N/A                |

## <a name="acme_staging"></a>22. Property `K8s Kubespray Inventory > acme_staging`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |

**Description:** If set to true will use acme staging directory for issueing certs.

----------------------------------------------------------------------------------------------------------------------------
Generated using [json-schema-for-humans](https://github.com/coveooss/json-schema-for-humans) on 2025-12-04 at 10:50:58 +0000
