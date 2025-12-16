# General DHCP Inventory

**Title:** General DHCP Inventory

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

**Description:** LXC Inventory extension for the setup_kea playbook.

| Property                                       | Pattern | Type             | Deprecated | Definition | Title/Description                                                                                                                                       |
| ---------------------------------------------- | ------- | ---------------- | ---------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| + [target_pve](#target_pve )                   | No      | string           | No         | -          | Proxmox cluster name + . + pve cloud domain. This determines the cloud and the proxmox cluster the vms/lxc/k8s luster will be created in.               |
| + [stack_name](#stack_name )                   | No      | string           | No         | -          | Your stack name, needs to be unique within the cloud domain.                                                                                            |
| - [static_includes](#static_includes )         | No      | object           | No         | -          | -                                                                                                                                                       |
| - [include_stacks](#include_stacks )           | No      | array of object  | No         | -          | Include other stacks into the ansible inventory, from any pve cloud you are connected to. From here you can freely extend and write your own playbooks. |
| + [root_ssh_pub_key](#root_ssh_pub_key )       | No      | string           | No         | -          | trusted root key for the cloud init image.                                                                                                              |
| - [pve_ha_group](#pve_ha_group )               | No      | string           | No         | -          | PVE HA group this vm should be assigned to (optional).                                                                                                  |
| - [target_pve_hosts](#target_pve_hosts )       | No      | array of string  | No         | -          | Array of proxmox hosts in the target pve that are eligible for scheduling. If not specified all online hosts are considered.                            |
| + [lxcs](#lxcs )                               | No      | array of object  | No         | -          | List of lxcs that will be created for the stack.                                                                                                        |
| - [lxc_global_vars](#lxc_global_vars )         | No      | object           | No         | -          | Variables that will be applied to all lxc hosts and are available in playbooks.                                                                         |
| - [lxc_base_parameters](#lxc_base_parameters ) | No      | object           | No         | -          | PVE pct cli parameters that will be used for all lxcs.                                                                                                  |
| - [lxc_os_template](#lxc_os_template )         | No      | string           | No         | -          | \`pveam available --section system\` / run \`pveam update\` for newest, PVE available LXC template (will be downloaded).                                |
| - [plugin](#plugin )                           | No      | enum (of string) | No         | -          | Id of ansible inventory plugin.                                                                                                                         |

## <a name="target_pve"></a>1. Property `General DHCP Inventory > target_pve`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Proxmox cluster name + . + pve cloud domain. This determines the cloud and the proxmox cluster the vms/lxc/k8s luster will be created in.

**Example:**

```json
"proxmox-cluster-a.your-cloud.domain"
```

## <a name="stack_name"></a>2. Property `General DHCP Inventory > stack_name`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Your stack name, needs to be unique within the cloud domain.

## <a name="static_includes"></a>3. Property `General DHCP Inventory > static_includes`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

## <a name="include_stacks"></a>4. Property `General DHCP Inventory > include_stacks`

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

### <a name="include_stacks_items"></a>4.1. General DHCP Inventory > include_stacks > include_stacks items

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

#### <a name="include_stacks_items_stack_fqdn"></a>4.1.1. Property `General DHCP Inventory > include_stacks > include_stacks items > stack_fqdn`

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

#### <a name="include_stacks_items_host_group"></a>4.1.2. Property `General DHCP Inventory > include_stacks > include_stacks items > host_group`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** This is the name of the hosts group of our ansible inventory the included vms/lxcs will be available under.

#### <a name="include_stacks_items_qemu_ansible_user"></a>4.1.3. Property `General DHCP Inventory > include_stacks > include_stacks items > qemu_ansible_user`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** User ansible will use to connect, defaults to admin. If you dont want to use debian cinit images you might need to set something else than admin.
Ubuntu for example wont work if you set the cloud init user to admin.

## <a name="root_ssh_pub_key"></a>5. Property `General DHCP Inventory > root_ssh_pub_key`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** trusted root key for the cloud init image.

## <a name="pve_ha_group"></a>6. Property `General DHCP Inventory > pve_ha_group`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** PVE HA group this vm should be assigned to (optional).

## <a name="target_pve_hosts"></a>7. Property `General DHCP Inventory > target_pve_hosts`

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

### <a name="target_pve_hosts_items"></a>7.1. General DHCP Inventory > target_pve_hosts > target_pve_hosts items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** The hostname of the proxmox host. Just the hostname, no cluster name or cloud domain should be specified, as they are implicit.

**Example:**

```json
"proxmox-host-a"
```

## <a name="lxcs"></a>8. Property `General DHCP Inventory > lxcs`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | Yes               |

**Description:** List of lxcs that will be created for the stack.

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be | Description |
| ------------------------------- | ----------- |
| [lxcs items](#lxcs_items)       | -           |

### <a name="lxcs_items"></a>8.1. General DHCP Inventory > lxcs > lxcs items

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

| Property                                  | Pattern | Type   | Deprecated | Definition | Title/Description                                                                           |
| ----------------------------------------- | ------- | ------ | ---------- | ---------- | ------------------------------------------------------------------------------------------- |
| - [hostname](#lxcs_items_hostname )       | No      | string | No         | -          | Optional unique hostname for this lxc, otherwise pet name random name will be generated.    |
| - [target_host](#lxcs_items_target_host ) | No      | string | No         | -          | Pve host to tie this vm to. This is useful to always deploy specifically on a proxmox host. |
| + [vars](#lxcs_items_vars )               | No      | object | No         | -          | Custom variables for this lxc specifically. Will be usable in playbooks.                    |
| + [parameters](#lxcs_items_parameters )   | No      | object | No         | -          | Parameters that will be passed to pve pct cli tool for lxc creation.                        |

#### <a name="lxcs_items_hostname"></a>8.1.1. Property `General DHCP Inventory > lxcs > lxcs items > hostname`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Optional unique hostname for this lxc, otherwise pet name random name will be generated.

#### <a name="lxcs_items_target_host"></a>8.1.2. Property `General DHCP Inventory > lxcs > lxcs items > target_host`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Pve host to tie this vm to. This is useful to always deploy specifically on a proxmox host.

#### <a name="lxcs_items_vars"></a>8.1.3. Property `General DHCP Inventory > lxcs > lxcs items > vars`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | Yes              |
| **Additional properties** | Any type allowed |

**Description:** Custom variables for this lxc specifically. Will be usable in playbooks.

| Property                                           | Pattern | Type    | Deprecated | Definition | Title/Description                                                                                            |
| -------------------------------------------------- | ------- | ------- | ---------- | ---------- | ------------------------------------------------------------------------------------------------------------ |
| + [kea_dhcp_main](#lxcs_items_vars_kea_dhcp_main ) | No      | boolean | No         | -          | Determines the lxc that will be the dhcp master instance. One lxc should be set to true, the other to false. |

##### <a name="lxcs_items_vars_kea_dhcp_main"></a>8.1.3.1. Property `General DHCP Inventory > lxcs > lxcs items > vars > kea_dhcp_main`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

**Description:** Determines the lxc that will be the dhcp master instance. One lxc should be set to true, the other to false.

#### <a name="lxcs_items_parameters"></a>8.1.4. Property `General DHCP Inventory > lxcs > lxcs items > parameters`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | Yes              |
| **Additional properties** | Any type allowed |

**Description:** Parameters that will be passed to pve pct cli tool for lxc creation.

| Property                                   | Pattern | Type    | Deprecated | Definition | Title/Description                                                                                                                                                                               |
| ------------------------------------------ | ------- | ------- | ---------- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| + [rootfs](#lxcs_items_parameters_rootfs ) | No      | string  | No         | -          | PVE storage for the container disk.                                                                                                                                                             |
| + [cores](#lxcs_items_parameters_cores )   | No      | integer | No         | -          | Number of virtual CPU cores.                                                                                                                                                                    |
| + [memory](#lxcs_items_parameters_memory ) | No      | integer | No         | -          | Memory in bytes, use POW 2.                                                                                                                                                                     |
| + [net0](#lxcs_items_parameters_net0 )     | No      | string  | No         | -          | Network interface the dhcp will serve on. This has to be named "pve" instead of the normal eth0 for the dhcp playbooks to work,<br />they configure kea to listen on this interface name.<br /> |

##### <a name="lxcs_items_parameters_rootfs"></a>8.1.4.1. Property `General DHCP Inventory > lxcs > lxcs items > parameters > rootfs`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** PVE storage for the container disk.

##### <a name="lxcs_items_parameters_cores"></a>8.1.4.2. Property `General DHCP Inventory > lxcs > lxcs items > parameters > cores`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

**Description:** Number of virtual CPU cores.

##### <a name="lxcs_items_parameters_memory"></a>8.1.4.3. Property `General DHCP Inventory > lxcs > lxcs items > parameters > memory`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

**Description:** Memory in bytes, use POW 2.

##### <a name="lxcs_items_parameters_net0"></a>8.1.4.4. Property `General DHCP Inventory > lxcs > lxcs items > parameters > net0`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Network interface the dhcp will serve on. This has to be named "pve" instead of the normal eth0 for the dhcp playbooks to work,
they configure kea to listen on this interface name.

**Example:**

```json
"name=eth0,bridge=vmbr0,tag=120,firewall=1,ip=dhcp"
```

| Restrictions                      |                                                                                                                                                                |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Must match regular expression** | ```\bname=pve\b``` [Test](https://regex101.com/?regex=%5Cbname%3Dpve%5Cb&testString=%22name%3Deth0%2Cbridge%3Dvmbr0%2Ctag%3D120%2Cfirewall%3D1%2Cip%3Ddhcp%22) |

## <a name="lxc_global_vars"></a>9. Property `General DHCP Inventory > lxc_global_vars`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Variables that will be applied to all lxc hosts and are available in playbooks.

| Property                                                                           | Pattern | Type    | Deprecated | Definition | Title/Description                                                                                                  |
| ---------------------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | ------------------------------------------------------------------------------------------------------------------ |
| - [use_alternate_ssh_port](#lxc_global_vars_use_alternate_ssh_port )               | No      | boolean | No         | -          | Will use 2222 instead of 22 for ssh.                                                                               |
| - [install_prom_systemd_exporter](#lxc_global_vars_install_prom_systemd_exporter ) | No      | boolean | No         | -          | Will install prometheus metrics exporter for systemd. This implements with pve cloud terraform monitoring modules. |
| - [](#lxc_global_vars_additionalProperties )                                       | No      | object  | No         | -          | -                                                                                                                  |

### <a name="lxc_global_vars_use_alternate_ssh_port"></a>9.1. Property `General DHCP Inventory > lxc_global_vars > use_alternate_ssh_port`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |

**Description:** Will use 2222 instead of 22 for ssh.

### <a name="lxc_global_vars_install_prom_systemd_exporter"></a>9.2. Property `General DHCP Inventory > lxc_global_vars > install_prom_systemd_exporter`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |

**Description:** Will install prometheus metrics exporter for systemd. This implements with pve cloud terraform monitoring modules.

## <a name="lxc_base_parameters"></a>10. Property `General DHCP Inventory > lxc_base_parameters`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** PVE pct cli parameters that will be used for all lxcs.

## <a name="lxc_os_template"></a>11. Property `General DHCP Inventory > lxc_os_template`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** `pveam available --section system` / run `pveam update` for newest, PVE available LXC template (will be downloaded).

## <a name="plugin"></a>12. Property `General DHCP Inventory > plugin`

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |

**Description:** Id of ansible inventory plugin.

Must be one of:
* "pxc.cloud.lxc_inv"

----------------------------------------------------------------------------------------------------------------------------
Generated using [json-schema-for-humans](https://github.com/coveooss/json-schema-for-humans) on 2025-12-16 at 01:59:14 +0000
