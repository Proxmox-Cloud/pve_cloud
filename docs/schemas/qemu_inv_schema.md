# VM Inventory

**Title:** VM Inventory

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

**Description:** Inventory for deploying k8s clusters via kubespray on PVE.

| Property                                         | Pattern | Type             | Deprecated | Definition | Title/Description                                                                                                                     |
| ------------------------------------------------ | ------- | ---------------- | ---------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| + [stack_name](#stack_name )                     | No      | string           | No         | -          | Your stack name, needs to be unique within the parent_domain. Will create its own sub zone.                                           |
| + [target_pve](#target_pve )                     | No      | string           | No         | -          | The pve cluster this stack should reside in, defined in ~/.pve-cloud-dyn-inv.yaml via \`pvcli connect-cluster\`                       |
| + [qemus](#qemus )                               | No      | array of object  | No         | -          | Nodes for the cluster in form of qemu vms.                                                                                            |
| - [include_stacks](#include_stacks )             | No      | array of object  | No         | -          | -                                                                                                                                     |
| - [static_includes](#static_includes )           | No      | object           | No         | -          | -                                                                                                                                     |
| + [root_ssh_pub_key](#root_ssh_pub_key )         | No      | string           | No         | -          | Ssh key for qemu_default_user                                                                                                         |
| - [pve_ha_group](#pve_ha_group )                 | No      | string           | No         | -          | PVE HA Group this qemu instance should be assigned to.                                                                                |
| - [qemu_default_user](#qemu_default_user )       | No      | string           | No         | -          | User for cinit.                                                                                                                       |
| - [qemu_hashed_pw](#qemu_hashed_pw )             | No      | string           | No         | -          | The hashed password that will be passed to cloudinit. Use \`mkpasswd --method=SHA-512\` with the fitting method for your cinit image. |
| - [qemu_base_parameters](#qemu_base_parameters ) | No      | object           | No         | -          | Parameters from qm create proxmox cli tool that will be passed to all created qemus.                                                  |
| - [qemu_image_url](#qemu_image_url )             | No      | string           | No         | -          | http(s) download link to the cinit image you want to use.                                                                             |
| - [qemu_keyboard_layout](#qemu_keyboard_layout ) | No      | string           | No         | -          | The keyboard layout, can be and of de, en ....                                                                                        |
| - [qemu_global_vars](#qemu_global_vars )         | No      | object           | No         | -          | Variables that will be applied to all lxc hosts                                                                                       |
| - [pve_cloud_pytest](#pve_cloud_pytest )         | No      | object           | No         | -          | Variables object used only in e2e tests.                                                                                              |
| - [plugin](#plugin )                             | No      | enum (of string) | No         | -          | Id of ansible inventory plugin                                                                                                        |

## <a name="stack_name"></a>1. Property `VM Inventory > stack_name`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Your stack name, needs to be unique within the parent_domain. Will create its own sub zone.

## <a name="target_pve"></a>2. Property `VM Inventory > target_pve`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** The pve cluster this stack should reside in, defined in ~/.pve-cloud-dyn-inv.yaml via `pvcli connect-cluster`

## <a name="qemus"></a>3. Property `VM Inventory > qemus`

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

### <a name="qemus_items"></a>3.1. VM Inventory > qemus > qemus items

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

| Property                                 | Pattern | Type   | Deprecated | Definition | Title/Description                                  |
| ---------------------------------------- | ------- | ------ | ---------- | ---------- | -------------------------------------------------- |
| - [parameters](#qemus_items_parameters ) | No      | object | No         | -          | In accordance with pve qm cli tool, creation args. |
| - [disk](#qemus_items_disk )             | No      | object | No         | -          | -                                                  |

#### <a name="qemus_items_parameters"></a>3.1.1. Property `VM Inventory > qemus > qemus items > parameters`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** In accordance with pve qm cli tool, creation args.

#### <a name="qemus_items_disk"></a>3.1.2. Property `VM Inventory > qemus > qemus items > disk`

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

| Property                                | Pattern | Type   | Deprecated | Definition | Title/Description                               |
| --------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------------------------------------- |
| + [size](#qemus_items_disk_size )       | No      | string | No         | -          | Size of the vms disk.                           |
| - [options](#qemus_items_disk_options ) | No      | object | No         | -          | Mount options                                   |
| + [pool](#qemus_items_disk_pool )       | No      | string | No         | -          | Ceph pool name the vms disk will be created in. |

##### <a name="qemus_items_disk_size"></a>3.1.2.1. Property `VM Inventory > qemus > qemus items > disk > size`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Size of the vms disk.

##### <a name="qemus_items_disk_options"></a>3.1.2.2. Property `VM Inventory > qemus > qemus items > disk > options`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Mount options

##### <a name="qemus_items_disk_pool"></a>3.1.2.3. Property `VM Inventory > qemus > qemus items > disk > pool`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Ceph pool name the vms disk will be created in.

## <a name="include_stacks"></a>4. Property `VM Inventory > include_stacks`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | No                |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be               | Description                                                                     |
| --------------------------------------------- | ------------------------------------------------------------------------------- |
| [include_stacks items](#include_stacks_items) | Include other stacks into the ansible inventory, from any PVE cluster you like. |

### <a name="include_stacks_items"></a>4.1. VM Inventory > include_stacks > include_stacks items

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Include other stacks into the ansible inventory, from any PVE cluster you like.

| Property                                                        | Pattern | Type   | Deprecated | Definition | Title/Description                                                                            |
| --------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | -------------------------------------------------------------------------------------------- |
| - [stack_fqdn](#include_stacks_items_stack_fqdn )               | No      | string | No         | -          | Target stack fqdn to include (stack name + pve_cloud_domain)                                 |
| - [host_group](#include_stacks_items_host_group )               | No      | string | No         | -          | This is the name of the hosts group of our ansible inventory the included vms will be under. |
| - [qemu_ansible_user](#include_stacks_items_qemu_ansible_user ) | No      | string | No         | -          | User ansible will use to connect, defaults to admin.                                         |

#### <a name="include_stacks_items_stack_fqdn"></a>4.1.1. Property `VM Inventory > include_stacks > include_stacks items > stack_fqdn`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Target stack fqdn to include (stack name + pve_cloud_domain)

#### <a name="include_stacks_items_host_group"></a>4.1.2. Property `VM Inventory > include_stacks > include_stacks items > host_group`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** This is the name of the hosts group of our ansible inventory the included vms will be under.

#### <a name="include_stacks_items_qemu_ansible_user"></a>4.1.3. Property `VM Inventory > include_stacks > include_stacks items > qemu_ansible_user`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** User ansible will use to connect, defaults to admin.

## <a name="static_includes"></a>5. Property `VM Inventory > static_includes`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

## <a name="root_ssh_pub_key"></a>6. Property `VM Inventory > root_ssh_pub_key`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Ssh key for qemu_default_user

## <a name="pve_ha_group"></a>7. Property `VM Inventory > pve_ha_group`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** PVE HA Group this qemu instance should be assigned to.

## <a name="qemu_default_user"></a>8. Property `VM Inventory > qemu_default_user`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** User for cinit.

## <a name="qemu_hashed_pw"></a>9. Property `VM Inventory > qemu_hashed_pw`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** The hashed password that will be passed to cloudinit. Use `mkpasswd --method=SHA-512` with the fitting method for your cinit image.

## <a name="qemu_base_parameters"></a>10. Property `VM Inventory > qemu_base_parameters`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Parameters from qm create proxmox cli tool that will be passed to all created qemus.

## <a name="qemu_image_url"></a>11. Property `VM Inventory > qemu_image_url`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** http(s) download link to the cinit image you want to use.

## <a name="qemu_keyboard_layout"></a>12. Property `VM Inventory > qemu_keyboard_layout`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** The keyboard layout, can be and of de, en ....

## <a name="qemu_global_vars"></a>13. Property `VM Inventory > qemu_global_vars`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Variables that will be applied to all lxc hosts

## <a name="pve_cloud_pytest"></a>14. Property `VM Inventory > pve_cloud_pytest`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Variables object used only in e2e tests.

## <a name="plugin"></a>15. Property `VM Inventory > plugin`

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |

**Description:** Id of ansible inventory plugin

Must be one of:
* "pve.cloud.qemu_inv"

----------------------------------------------------------------------------------------------------------------------------
Generated using [json-schema-for-humans](https://github.com/coveooss/json-schema-for-humans) on 2025-11-28 at 12:39:47 +0000
