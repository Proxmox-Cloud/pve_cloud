

**Title:** VM Inventory

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

**Description:** Inventory for deploying qemu VMs on PVE.

| Property                                         | Pattern | Type             | Deprecated | Definition | Title/Description                                                                                                                                                                                                       |
| ------------------------------------------------ | ------- | ---------------- | ---------- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| + [target_pve](#target_pve )                     | No      | string           | No         | -          | Proxmox cluster name + . + pve cloud domain. This determines the cloud and the proxmox cluster the vms/lxc/k8s luster will be created in.                                                                               |
| + [stack_name](#stack_name )                     | No      | string           | No         | -          | Your stack name, needs to be unique within the cloud domain.                                                                                                                                                            |
| - [static_includes](#static_includes )           | No      | object           | No         | -          | For virtual machines we have the option to define tcp_proxies and ingress_domains. If those are set we need certain static includes.<br />                                                                              |
| - [include_stacks](#include_stacks )             | No      | array of object  | No         | -          | Include other stacks into the ansible inventory, from any pve cloud you are connected to. From here you can freely extend and write your own playbooks.                                                                 |
| + [root_ssh_pub_key](#root_ssh_pub_key )         | No      | string           | No         | -          | trusted root key for the cloud init image.                                                                                                                                                                              |
| - [pve_ha_group](#pve_ha_group )                 | No      | string           | No         | -          | PVE HA group this vm should be assigned to (optional).                                                                                                                                                                  |
| - [target_pve_hosts](#target_pve_hosts )         | No      | array of string  | No         | -          | Array of proxmox hosts in the target pve that are eligible for scheduling. If not specified all online hosts are considered.                                                                                            |
| + [qemus](#qemus )                               | No      | array of object  | No         | -          | List of qemu vms for the stack.                                                                                                                                                                                         |
| - [tcp_proxies](#tcp_proxies )                   | No      | array of object  | No         | -          | Raw tcp forwards on the clusters haproxy to k8s services exposed via nodeport.                                                                                                                                          |
| - [qemu_default_user](#qemu_default_user )       | No      | string           | No         | -          | User for cinit.                                                                                                                                                                                                         |
| - [qemu_hashed_pw](#qemu_hashed_pw )             | No      | string           | No         | -          | Pw for default user defaults to hashed 'password' for debian cloud init image. Different cloud init images require different hash methods. You cannot use the same from debian for ubuntu for example.                  |
| - [qemu_base_parameters](#qemu_base_parameters ) | No      | object           | No         | -          | Base parameters applied to all qemus. passed to the proxmox qm cli tool for creating vm.                                                                                                                                |
| - [qemu_image_url](#qemu_image_url )             | No      | string           | No         | -          | http(s) download link for cloud init image.                                                                                                                                                                             |
| - [qemu_keyboard_layout](#qemu_keyboard_layout ) | No      | string           | No         | -          | Keyboard layout for cloudinit.                                                                                                                                                                                          |
| - [qemu_network_config](#qemu_network_config )   | No      | string           | No         | -          | Optional qemu network config as a yaml string that is merged into the cloudinit network config of all qemus.                                                                                                            |
| - [qemu_global_vars](#qemu_global_vars )         | No      | object           | No         | -          | Variables that will be applied set for all qemus vms.                                                                                                                                                                   |
| - [plugin](#plugin )                             | No      | enum (of string) | No         | -          | Id of ansible inventory plugin                                                                                                                                                                                          |
| - [ingress_domains](#ingress_domains )           | No      | array of object  | No         | -          | Specific non ingress routing, via hostname lookup inside the proxy. This allows easy integration of <br />standalone services like mailcow or other standalone deployments that do their own ingress termination.<br /> |

## <a name="target_pve"></a>38. Property `VM Inventory > target_pve`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Proxmox cluster name + . + pve cloud domain. This determines the cloud and the proxmox cluster the vms/lxc/k8s luster will be created in.

**Example:**

```json
"proxmox-cluster-a.your-cloud.domain"
```

## <a name="stack_name"></a>39. Property `VM Inventory > stack_name`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Your stack name, needs to be unique within the cloud domain.

## <a name="static_includes"></a>40. Property `VM Inventory > static_includes`

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

**Description:** For virtual machines we have the option to define tcp_proxies and ingress_domains. If those are set we need certain static includes.

| Property                                             | Pattern | Type   | Deprecated | Definition | Title/Description                                                                                                                                 |
| ---------------------------------------------------- | ------- | ------ | ---------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| - [dhcp_stack](#static_includes_dhcp_stack )         | No      | string | No         | -          | For interacting with kea reservations.                                                                                                            |
| - [proxy_stack](#static_includes_proxy_stack )       | No      | string | No         | -          | Reloading the proxy.                                                                                                                              |
| - [postgres_stack](#static_includes_postgres_stack ) | No      | string | No         | -          | The playbook needs the pve cloud postgres stack where state and general configuration is stored.                                                  |
| - [bind_stack](#static_includes_bind_stack )         | No      | string | No         | -          | The playbook needs the bind stack to register the general masters recordset and for creating authoritative zones defined in cluster_cert_entries. |

### <a name="static_includes_dhcp_stack"></a>40.1. Property `VM Inventory > static_includes > dhcp_stack`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** For interacting with kea reservations.

**Example:**

```json
"dhcp.your-cloud.domain"
```

### <a name="static_includes_proxy_stack"></a>40.2. Property `VM Inventory > static_includes > proxy_stack`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Reloading the proxy.

**Example:**

```json
"proxy.your-cloud.domain"
```

### <a name="static_includes_postgres_stack"></a>40.3. Property `VM Inventory > static_includes > postgres_stack`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** The playbook needs the pve cloud postgres stack where state and general configuration is stored.

**Example:**

```json
"patroni.your-cloud.domain"
```

### <a name="static_includes_bind_stack"></a>40.4. Property `VM Inventory > static_includes > bind_stack`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** The playbook needs the bind stack to register the general masters recordset and for creating authoritative zones defined in cluster_cert_entries.

**Example:**

```json
"bind.your-cloud.domain"
```

## <a name="include_stacks"></a>41. Property `VM Inventory > include_stacks`

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

### <a name="include_stacks_items"></a>41.1. VM Inventory > include_stacks > include_stacks items

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

#### <a name="include_stacks_items_stack_fqdn"></a>41.1.1. Property `VM Inventory > include_stacks > include_stacks items > stack_fqdn`

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

#### <a name="include_stacks_items_host_group"></a>41.1.2. Property `VM Inventory > include_stacks > include_stacks items > host_group`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** This is the name of the hosts group of our ansible inventory the included vms/lxcs will be available under.

#### <a name="include_stacks_items_qemu_ansible_user"></a>41.1.3. Property `VM Inventory > include_stacks > include_stacks items > qemu_ansible_user`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** User ansible will use to connect, defaults to admin. If you dont want to use debian cinit images you might need to set something else than admin.
Ubuntu for example wont work if you set the cloud init user to admin.

## <a name="root_ssh_pub_key"></a>42. Property `VM Inventory > root_ssh_pub_key`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** trusted root key for the cloud init image.

## <a name="pve_ha_group"></a>43. Property `VM Inventory > pve_ha_group`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** PVE HA group this vm should be assigned to (optional).

## <a name="target_pve_hosts"></a>44. Property `VM Inventory > target_pve_hosts`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of string` |
| **Required** | No                |

**Description:** Array of proxmox hosts in the target pve that are eligible for scheduling. If not specified all online hosts are considered.

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                   | Description                                                                                                                     |
| ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| [target_pve_hosts items](#target_pve_hosts_items) | The hostname of the proxmox host. Just the hostname, no cluster name or cloud domain should be specified, as they are implicit. |

### <a name="target_pve_hosts_items"></a>44.1. VM Inventory > target_pve_hosts > target_pve_hosts items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** The hostname of the proxmox host. Just the hostname, no cluster name or cloud domain should be specified, as they are implicit.

**Example:**

```json
"proxmox-host-a"
```

## <a name="qemus"></a>45. Property `VM Inventory > qemus`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | Yes               |

**Description:** List of qemu vms for the stack.

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

### <a name="qemus_items"></a>45.1. VM Inventory > qemus > qemus items

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

| Property                                         | Pattern | Type   | Deprecated | Definition | Title/Description                                                                                                                                                       |
| ------------------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| - [hostname](#qemus_items_hostname )             | No      | string | No         | -          | Optional unique hostname for this node, otherwise pet name random name will be generated.                                                                               |
| - [vars](#qemus_items_vars )                     | No      | object | No         | -          | Custom variables for this node specifically, might be useful in your own custom playbooks.                                                                              |
| - [target_host](#qemus_items_target_host )       | No      | string | No         | -          | Optional specific proxmox host you want to tie this node to on creation. Can of course still be moved afterwards. Cloud domain is implicit and should not be specified. |
| + [parameters](#qemus_items_parameters )         | No      | object | No         | -          | In accordance with pve qm cli tool, creation parameters mapped (key equals the --key part and value the passed value).                                                  |
| - [network_config](#qemus_items_network_config ) | No      | string | No         | -          | Cinit network config yaml string. Will be the last cfg piece that gets merged into the final cloudinit network config. Can be used for overrides.                       |
| + [disk](#qemus_items_disk )                     | No      | object | No         | -          | -                                                                                                                                                                       |

#### <a name="qemus_items_hostname"></a>45.1.1. Property `VM Inventory > qemus > qemus items > hostname`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Optional unique hostname for this node, otherwise pet name random name will be generated.

#### <a name="qemus_items_vars"></a>45.1.2. Property `VM Inventory > qemus > qemus items > vars`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Custom variables for this node specifically, might be useful in your own custom playbooks.

#### <a name="qemus_items_target_host"></a>45.1.3. Property `VM Inventory > qemus > qemus items > target_host`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Optional specific proxmox host you want to tie this node to on creation. Can of course still be moved afterwards. Cloud domain is implicit and should not be specified.

**Example:**

```json
"proxmox-host-B.proxmox-cluster-A"
```

#### <a name="qemus_items_parameters"></a>45.1.4. Property `VM Inventory > qemus > qemus items > parameters`

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

#### <a name="qemus_items_network_config"></a>45.1.5. Property `VM Inventory > qemus > qemus items > network_config`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Cinit network config yaml string. Will be the last cfg piece that gets merged into the final cloudinit network config. Can be used for overrides.

#### <a name="qemus_items_disk"></a>45.1.6. Property `VM Inventory > qemus > qemus items > disk`

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

##### <a name="qemus_items_disk_size"></a>45.1.6.1. Property `VM Inventory > qemus > qemus items > disk > size`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Size of the vms disk.

**Example:**

```json
"25G"
```

##### <a name="qemus_items_disk_options"></a>45.1.6.2. Property `VM Inventory > qemus > qemus items > disk > options`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Mount options

##### <a name="qemus_items_disk_pool"></a>45.1.6.3. Property `VM Inventory > qemus > qemus items > disk > pool`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Ceph pool name the vms disk will be created in.

## <a name="tcp_proxies"></a>46. Property `VM Inventory > tcp_proxies`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | No                |

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

### <a name="tcp_proxies_items"></a>46.1. VM Inventory > tcp_proxies > tcp_proxies items

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

#### <a name="tcp_proxies_items_proxy_name"></a>46.1.1. Property `VM Inventory > tcp_proxies > tcp_proxies items > proxy_name`

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

#### <a name="tcp_proxies_items_haproxy_port"></a>46.1.2. Property `VM Inventory > tcp_proxies > tcp_proxies items > haproxy_port`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

**Description:** Frontend port of the proxmox clusters haproxy.

#### <a name="tcp_proxies_items_node_port"></a>46.1.3. Property `VM Inventory > tcp_proxies > tcp_proxies items > node_port`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

**Description:** Nodeport of the k8s service.

#### <a name="tcp_proxies_items_proxy_snippet"></a>46.1.4. Property `VM Inventory > tcp_proxies > tcp_proxies items > proxy_snippet`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Additional snippet that will be inserted into the haproxy listen block. Can be used to adjust the forwards settings.

**Example:**

```json
"# long running tcp connections that only rarely transmit data\n# ssh client connection for example\ntimeout client 1h \ntimeout server 1h \n"
```

#### <a name="tcp_proxies_items_external"></a>46.1.5. Property `VM Inventory > tcp_proxies > tcp_proxies items > external`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |

**Description:** Will also create a forward on the external floating ip of the proxy not only the internal.

## <a name="qemu_default_user"></a>47. Property `VM Inventory > qemu_default_user`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** User for cinit.

## <a name="qemu_hashed_pw"></a>48. Property `VM Inventory > qemu_hashed_pw`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Pw for default user defaults to hashed 'password' for debian cloud init image. Different cloud init images require different hash methods. You cannot use the same from debian for ubuntu for example.

## <a name="qemu_base_parameters"></a>49. Property `VM Inventory > qemu_base_parameters`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Base parameters applied to all qemus. passed to the proxmox qm cli tool for creating vm.

## <a name="qemu_image_url"></a>50. Property `VM Inventory > qemu_image_url`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** http(s) download link for cloud init image.

## <a name="qemu_keyboard_layout"></a>51. Property `VM Inventory > qemu_keyboard_layout`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Keyboard layout for cloudinit.

## <a name="qemu_network_config"></a>52. Property `VM Inventory > qemu_network_config`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Optional qemu network config as a yaml string that is merged into the cloudinit network config of all qemus.

## <a name="qemu_global_vars"></a>53. Property `VM Inventory > qemu_global_vars`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Variables that will be applied set for all qemus vms.

## <a name="plugin"></a>54. Property `VM Inventory > plugin`

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |

**Description:** Id of ansible inventory plugin

Must be one of:

* "pxc.cloud.qemu_inv"

## <a name="ingress_domains"></a>55. Property `VM Inventory > ingress_domains`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | No                |

**Description:** Specific non ingress routing, via hostname lookup inside the proxy. This allows easy integration of 
standalone services like mailcow or other standalone deployments that do their own ingress termination.

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                 | Description |
| ----------------------------------------------- | ----------- |
| [ingress_domains items](#ingress_domains_items) | -           |

### <a name="ingress_domains_items"></a>55.1. VM Inventory > ingress_domains > ingress_domains items

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

| Property                                       | Pattern | Type            | Deprecated | Definition | Title/Description                                                                                                                           |
| ---------------------------------------------- | ------- | --------------- | ---------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| - [zone](#ingress_domains_items_zone )         | No      | string          | No         | -          | Internal zone that is registered in bind. In this case the playbooks will make records in bind<br />pointing to the vms of the stack.<br /> |
| - [names](#ingress_domains_items_names )       | No      | array of string | No         | -          | Names of the zone that will be routed to vms of this stack.                                                                                 |
| - [external](#ingress_domains_items_external ) | No      | boolean         | No         | -          | Whether or not the routing will also bind to the external floating ip of our haproxy.<br />                                                 |

#### <a name="ingress_domains_items_zone"></a>55.1.1. Property `VM Inventory > ingress_domains > ingress_domains items > zone`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Internal zone that is registered in bind. In this case the playbooks will make records in bind
pointing to the vms of the stack.

#### <a name="ingress_domains_items_names"></a>55.1.2. Property `VM Inventory > ingress_domains > ingress_domains items > names`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of string` |
| **Required** | No                |

**Description:** Names of the zone that will be routed to vms of this stack.

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                   | Description |
| ------------------------------------------------- | ----------- |
| [names items](#ingress_domains_items_names_items) | -           |

##### <a name="ingress_domains_items_names_items"></a>55.1.2.1. VM Inventory > ingress_domains > ingress_domains items > names > names items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

#### <a name="ingress_domains_items_external"></a>55.1.3. Property `VM Inventory > ingress_domains > ingress_domains items > external`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |

**Description:** Whether or not the routing will also bind to the external floating ip of our haproxy.

