# VM Inventory

**Title:** VM Inventory

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

**Description:** Inventory for deploying qemu VMs on PVE.

| Property                                         | Pattern | Type             | Deprecated | Definition | Title/Description                                                                                                                                                                                      |
| ------------------------------------------------ | ------- | ---------------- | ---------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| + [target_pve](#target_pve )                     | No      | string           | No         | -          | Proxmox cluster name + . + pve cloud domain. This determines the cloud and the proxmox cluster the vms/lxc/k8s luster will be created in.                                                              |
| + [stack_name](#stack_name )                     | No      | string           | No         | -          | Your stack name, needs to be unique within the cloud domain.                                                                                                                                           |
| - [static_includes](#static_includes )           | No      | object           | No         | -          | -                                                                                                                                                                                                      |
| - [include_stacks](#include_stacks )             | No      | array of object  | No         | -          | Include other stacks into the ansible inventory, from any pve cloud you are connected to. From here you can freely extend and write your own playbooks.                                                |
| + [root_ssh_pub_key](#root_ssh_pub_key )         | No      | string           | No         | -          | trusted root key for the cloud init image.                                                                                                                                                             |
| - [pve_ha_group](#pve_ha_group )                 | No      | string           | No         | -          | PVE HA group this vm should be assigned to (optional).                                                                                                                                                 |
| - [pve_cloud_pytest](#pve_cloud_pytest )         | No      | object           | No         | -          | Variables object used only in e2e tests.                                                                                                                                                               |
| + [qemus](#qemus )                               | No      | array of object  | No         | -          | List of qemu vms for the stack.                                                                                                                                                                        |
| - [qemu_default_user](#qemu_default_user )       | No      | string           | No         | -          | User for cinit.                                                                                                                                                                                        |
| - [qemu_hashed_pw](#qemu_hashed_pw )             | No      | string           | No         | -          | Pw for default user defaults to hashed 'password' for debian cloud init image. Different cloud init images require different hash methods. You cannot use the same from debian for ubuntu for example. |
| - [qemu_base_parameters](#qemu_base_parameters ) | No      | object           | No         | -          | Base parameters applied to all qemus. passed to the proxmox qm cli tool for creating vm.                                                                                                               |
| - [qemu_image_url](#qemu_image_url )             | No      | string           | No         | -          | http(s) download link for cloud init image.                                                                                                                                                            |
| - [qemu_keyboard_layout](#qemu_keyboard_layout ) | No      | string           | No         | -          | Keyboard layout for cloudinit.                                                                                                                                                                         |
| - [qemu_network_config](#qemu_network_config )   | No      | string           | No         | -          | Optional qemu network config as a yaml string that is merged into the cloudinit network config of all qemus.                                                                                           |
| - [qemu_global_vars](#qemu_global_vars )         | No      | object           | No         | -          | Variables that will be applied set for all qemus vms.                                                                                                                                                  |
| - [plugin](#plugin )                             | No      | enum (of string) | No         | -          | Id of ansible inventory plugin                                                                                                                                                                         |

## <a name="target_pve"></a>1. Property `VM Inventory > target_pve`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Proxmox cluster name + . + pve cloud domain. This determines the cloud and the proxmox cluster the vms/lxc/k8s luster will be created in.

**Example:**

```json
"proxmox-cluster-a.your-cloud.domain"
```

## <a name="stack_name"></a>2. Property `VM Inventory > stack_name`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Your stack name, needs to be unique within the cloud domain.

## <a name="static_includes"></a>3. Property `VM Inventory > static_includes`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

## <a name="include_stacks"></a>4. Property `VM Inventory > include_stacks`

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

### <a name="include_stacks_items"></a>4.1. VM Inventory > include_stacks > include_stacks items

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

#### <a name="include_stacks_items_stack_fqdn"></a>4.1.1. Property `VM Inventory > include_stacks > include_stacks items > stack_fqdn`

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

#### <a name="include_stacks_items_host_group"></a>4.1.2. Property `VM Inventory > include_stacks > include_stacks items > host_group`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** This is the name of the hosts group of our ansible inventory the included vms/lxcs will be available under.

#### <a name="include_stacks_items_qemu_ansible_user"></a>4.1.3. Property `VM Inventory > include_stacks > include_stacks items > qemu_ansible_user`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** User ansible will use to connect, defaults to admin. If you dont want to use debian cinit images you might need to set something else than admin.
Ubuntu for example wont work if you set the cloud init user to admin.

## <a name="root_ssh_pub_key"></a>5. Property `VM Inventory > root_ssh_pub_key`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** trusted root key for the cloud init image.

## <a name="pve_ha_group"></a>6. Property `VM Inventory > pve_ha_group`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** PVE HA group this vm should be assigned to (optional).

## <a name="pve_cloud_pytest"></a>7. Property `VM Inventory > pve_cloud_pytest`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Variables object used only in e2e tests.

## <a name="qemus"></a>8. Property `VM Inventory > qemus`

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

### <a name="qemus_items"></a>8.1. VM Inventory > qemus > qemus items

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

#### <a name="qemus_items_hostname"></a>8.1.1. Property `VM Inventory > qemus > qemus items > hostname`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Optional unique hostname for this node, otherwise pet name random name will be generated.

#### <a name="qemus_items_vars"></a>8.1.2. Property `VM Inventory > qemus > qemus items > vars`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Custom variables for this node specifically, might be useful in your own custom playbooks.

#### <a name="qemus_items_target_host"></a>8.1.3. Property `VM Inventory > qemus > qemus items > target_host`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Optional specific proxmox host you want to tie this node to on creation. Can of course still be moved afterwards. Cloud domain is implicit and should not be specified.

**Example:**

```json
"proxmox-host-B.proxmox-cluster-A"
```

#### <a name="qemus_items_parameters"></a>8.1.4. Property `VM Inventory > qemus > qemus items > parameters`

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

#### <a name="qemus_items_network_config"></a>8.1.5. Property `VM Inventory > qemus > qemus items > network_config`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Cinit network config yaml string. Will be the last cfg piece that gets merged into the final cloudinit network config. Can be used for overrides.

#### <a name="qemus_items_disk"></a>8.1.6. Property `VM Inventory > qemus > qemus items > disk`

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

##### <a name="qemus_items_disk_size"></a>8.1.6.1. Property `VM Inventory > qemus > qemus items > disk > size`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Size of the vms disk.

**Example:**

```json
"25G"
```

##### <a name="qemus_items_disk_options"></a>8.1.6.2. Property `VM Inventory > qemus > qemus items > disk > options`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Mount options

##### <a name="qemus_items_disk_pool"></a>8.1.6.3. Property `VM Inventory > qemus > qemus items > disk > pool`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Ceph pool name the vms disk will be created in.

## <a name="qemu_default_user"></a>9. Property `VM Inventory > qemu_default_user`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** User for cinit.

## <a name="qemu_hashed_pw"></a>10. Property `VM Inventory > qemu_hashed_pw`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Pw for default user defaults to hashed 'password' for debian cloud init image. Different cloud init images require different hash methods. You cannot use the same from debian for ubuntu for example.

## <a name="qemu_base_parameters"></a>11. Property `VM Inventory > qemu_base_parameters`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Base parameters applied to all qemus. passed to the proxmox qm cli tool for creating vm.

## <a name="qemu_image_url"></a>12. Property `VM Inventory > qemu_image_url`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** http(s) download link for cloud init image.

## <a name="qemu_keyboard_layout"></a>13. Property `VM Inventory > qemu_keyboard_layout`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Keyboard layout for cloudinit.

## <a name="qemu_network_config"></a>14. Property `VM Inventory > qemu_network_config`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Optional qemu network config as a yaml string that is merged into the cloudinit network config of all qemus.

## <a name="qemu_global_vars"></a>15. Property `VM Inventory > qemu_global_vars`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Variables that will be applied set for all qemus vms.

## <a name="plugin"></a>16. Property `VM Inventory > plugin`

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |

**Description:** Id of ansible inventory plugin

Must be one of:
* "pve.cloud.qemu_inv"

----------------------------------------------------------------------------------------------------------------------------
Generated using [json-schema-for-humans](https://github.com/coveooss/json-schema-for-humans) on 2025-12-04 at 10:50:57 +0000
