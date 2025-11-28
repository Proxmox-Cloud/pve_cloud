# LXC Inventory

**Title:** LXC Inventory

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

**Description:** Base inventory for creating lxcs for a single stack on PVE.

| Property                                       | Pattern | Type             | Deprecated | Definition | Title/Description                                                                                                        |
| ---------------------------------------------- | ------- | ---------------- | ---------- | ---------- | ------------------------------------------------------------------------------------------------------------------------ |
| + [target_pve](#target_pve )                   | No      | string           | No         | -          | Proxmox cluster name + cloud domain, this is where the lxcs will be created.                                             |
| + [stack_name](#stack_name )                   | No      | string           | No         | -          | Your stack name, needs to be unique within the cloud.                                                                    |
| - [static_includes](#static_includes )         | No      | object           | No         | -          | -                                                                                                                        |
| + [lxcs](#lxcs )                               | No      | array of object  | No         | -          | List of lxcs that will be created for the stack.                                                                         |
| - [include_stacks](#include_stacks )           | No      | array of object  | No         | -          | Include other cloud stacks into the ansible inventory, from any PVE cluster within the cloud you like.                   |
| - [lxc_global_vars](#lxc_global_vars )         | No      | object           | No         | -          | Variables that will be applied to all lxc hosts and are available in playbooks.                                          |
| - [pve_ha_group](#pve_ha_group )               | No      | string           | No         | -          | When set the stack will be added to the corresponding PVE high availability group.                                       |
| - [lxc_base_parameters](#lxc_base_parameters ) | No      | object           | No         | -          | PVE pct cli parameters that will be used for all lxcs.                                                                   |
| - [lxc_os_template](#lxc_os_template )         | No      | string           | No         | -          | \`pveam available --section system\` / run \`pveam update\` for newest, PVE available LXC template (will be downloaded). |
| + [root_ssh_pub_key](#root_ssh_pub_key )       | No      | string           | No         | -          | Public key that will be installed for the root user of all lxcs in the stack.                                            |
| - [pve_cloud_pytest](#pve_cloud_pytest )       | No      | object           | No         | -          | Variables object used only in e2e tests.                                                                                 |
| - [plugin](#plugin )                           | No      | enum (of string) | No         | -          | Id of ansible inventory plugin.                                                                                          |

## <a name="target_pve"></a>1. Property `LXC Inventory > target_pve`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Proxmox cluster name + cloud domain, this is where the lxcs will be created.

## <a name="stack_name"></a>2. Property `LXC Inventory > stack_name`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Your stack name, needs to be unique within the cloud.

## <a name="static_includes"></a>3. Property `LXC Inventory > static_includes`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

## <a name="lxcs"></a>4. Property `LXC Inventory > lxcs`

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

### <a name="lxcs_items"></a>4.1. LXC Inventory > lxcs > lxcs items

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

#### <a name="lxcs_items_hostname"></a>4.1.1. Property `LXC Inventory > lxcs > lxcs items > hostname`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Optional unique hostname for this lxc, otherwise pet name random name will be generated.

#### <a name="lxcs_items_target_host"></a>4.1.2. Property `LXC Inventory > lxcs > lxcs items > target_host`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Pve host to tie this vm to. This is useful to always deploy specifically on a proxmox host.

#### <a name="lxcs_items_vars"></a>4.1.3. Property `LXC Inventory > lxcs > lxcs items > vars`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | Yes              |
| **Additional properties** | Any type allowed |

**Description:** Custom variables for this lxc specifically. Will be usable in playbooks.

| Property                                       | Pattern | Type    | Deprecated | Definition | Title/Description |
| ---------------------------------------------- | ------- | ------- | ---------- | ---------- | ----------------- |
| + [bind_master](#lxcs_items_vars_bind_master ) | No      | boolean | No         | -          | -                 |

##### <a name="lxcs_items_vars_bind_master"></a>4.1.3.1. Property `LXC Inventory > lxcs > lxcs items > vars > bind_master`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

#### <a name="lxcs_items_parameters"></a>4.1.4. Property `LXC Inventory > lxcs > lxcs items > parameters`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | Yes              |
| **Additional properties** | Any type allowed |

**Description:** Parameters that will be passed to pve pct cli tool for lxc creation.

| Property                                   | Pattern | Type    | Deprecated | Definition | Title/Description                            |
| ------------------------------------------ | ------- | ------- | ---------- | ---------- | -------------------------------------------- |
| + [rootfs](#lxcs_items_parameters_rootfs ) | No      | string  | No         | -          | PVE storage for the container disk.          |
| + [cores](#lxcs_items_parameters_cores )   | No      | integer | No         | -          | Number of virtual CPU cores.                 |
| + [memory](#lxcs_items_parameters_memory ) | No      | integer | No         | -          | Memory in bytes, use POW 2.                  |
| + [net0](#lxcs_items_parameters_net0 )     | No      | string  | No         | -          | Configuration for primary network interface. |

##### <a name="lxcs_items_parameters_rootfs"></a>4.1.4.1. Property `LXC Inventory > lxcs > lxcs items > parameters > rootfs`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** PVE storage for the container disk.

##### <a name="lxcs_items_parameters_cores"></a>4.1.4.2. Property `LXC Inventory > lxcs > lxcs items > parameters > cores`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

**Description:** Number of virtual CPU cores.

##### <a name="lxcs_items_parameters_memory"></a>4.1.4.3. Property `LXC Inventory > lxcs > lxcs items > parameters > memory`

|              |           |
| ------------ | --------- |
| **Type**     | `integer` |
| **Required** | Yes       |

**Description:** Memory in bytes, use POW 2.

##### <a name="lxcs_items_parameters_net0"></a>4.1.4.4. Property `LXC Inventory > lxcs > lxcs items > parameters > net0`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Configuration for primary network interface.

**Example:**

```json
"name=eth0,bridge=vmbr0,tag=120,firewall=1,ip=dhcp"
```

## <a name="include_stacks"></a>5. Property `LXC Inventory > include_stacks`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | No                |

**Description:** Include other cloud stacks into the ansible inventory, from any PVE cluster within the cloud you like.

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

### <a name="include_stacks_items"></a>5.1. LXC Inventory > include_stacks > include_stacks items

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

| Property                                                        | Pattern | Type   | Deprecated | Definition | Title/Description                                                                                                       |
| --------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------------------------------------------------------------------------------------------------------------- |
| - [stack_fqdn](#include_stacks_items_stack_fqdn )               | No      | string | No         | -          | Target stack fqdn to include (stack name + pve_cloud_domain). Will automatically include it from the right pve cluster. |
| - [host_group](#include_stacks_items_host_group )               | No      | string | No         | -          | This is the name of the hosts group of our ansible inventory the included vms will be under.                            |
| - [qemu_ansible_user](#include_stacks_items_qemu_ansible_user ) | No      | string | No         | -          | User ansible will use to connect if its a vm, defaults to admin. LXCs are always root.                                  |

#### <a name="include_stacks_items_stack_fqdn"></a>5.1.1. Property `LXC Inventory > include_stacks > include_stacks items > stack_fqdn`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Target stack fqdn to include (stack name + pve_cloud_domain). Will automatically include it from the right pve cluster.

#### <a name="include_stacks_items_host_group"></a>5.1.2. Property `LXC Inventory > include_stacks > include_stacks items > host_group`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** This is the name of the hosts group of our ansible inventory the included vms will be under.

#### <a name="include_stacks_items_qemu_ansible_user"></a>5.1.3. Property `LXC Inventory > include_stacks > include_stacks items > qemu_ansible_user`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** User ansible will use to connect if its a vm, defaults to admin. LXCs are always root.

## <a name="lxc_global_vars"></a>6. Property `LXC Inventory > lxc_global_vars`

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

### <a name="lxc_global_vars_use_alternate_ssh_port"></a>6.1. Property `LXC Inventory > lxc_global_vars > use_alternate_ssh_port`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |

**Description:** Will use 2222 instead of 22 for ssh.

### <a name="lxc_global_vars_install_prom_systemd_exporter"></a>6.2. Property `LXC Inventory > lxc_global_vars > install_prom_systemd_exporter`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |

**Description:** Will install prometheus metrics exporter for systemd. This implements with pve cloud terraform monitoring modules.

## <a name="pve_ha_group"></a>7. Property `LXC Inventory > pve_ha_group`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** When set the stack will be added to the corresponding PVE high availability group.

## <a name="lxc_base_parameters"></a>8. Property `LXC Inventory > lxc_base_parameters`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** PVE pct cli parameters that will be used for all lxcs.

## <a name="lxc_os_template"></a>9. Property `LXC Inventory > lxc_os_template`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** `pveam available --section system` / run `pveam update` for newest, PVE available LXC template (will be downloaded).

## <a name="root_ssh_pub_key"></a>10. Property `LXC Inventory > root_ssh_pub_key`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Public key that will be installed for the root user of all lxcs in the stack.

## <a name="pve_cloud_pytest"></a>11. Property `LXC Inventory > pve_cloud_pytest`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Variables object used only in e2e tests.

## <a name="plugin"></a>12. Property `LXC Inventory > plugin`

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |

**Description:** Id of ansible inventory plugin.

Must be one of:
* "pve.cloud.lxc_inv"

----------------------------------------------------------------------------------------------------------------------------
Generated using [json-schema-for-humans](https://github.com/coveooss/json-schema-for-humans) on 2025-11-28 at 12:39:47 +0000
