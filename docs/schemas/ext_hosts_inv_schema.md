

**Title:** External Hosts Inventory

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

**Description:** Generic inventory file for accessing external, non proxmox cloud hosts in a proxmox cloud context.

| Property                                       | Pattern | Type             | Deprecated | Definition | Title/Description                                                                                                                             |
| ---------------------------------------------- | ------- | ---------------- | ---------- | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| + [pve_cloud_domain](#pve_cloud_domain )       | No      | string           | No         | -          | Cloud domain to connect to.                                                                                                                   |
| + [target_cluster](#target_cluster )           | No      | string           | No         | -          | Target cluster we want to use inside the cloud (proxmox cluster name).                                                                        |
| + [external_stack_name](#external_stack_name ) | No      | string           | No         | -          | General stack name of this external inventory / project.                                                                                      |
| - [plugin](#plugin )                           | No      | enum (of string) | No         | -          | Id of ansible inventory plugin, needs to be set exactly.                                                                                      |
| - [host_groups](#host_groups )                 | No      | object           | No         | -          | Generic ansible hosts.                                                                                                                        |
| - [typed_host_groups](#typed_host_groups )     | No      | object           | No         | -          | Specialized hosts / groups with typed vars needed for running specific pxc playbooks that are available for external non proxmox hosts.<br /> |

## <a name="pve_cloud_domain"></a>1. Property `External Hosts Inventory > pve_cloud_domain`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Cloud domain to connect to.

**Example:**

```json
"your-cloud.example.com"
```

## <a name="target_cluster"></a>2. Property `External Hosts Inventory > target_cluster`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Target cluster we want to use inside the cloud (proxmox cluster name).

## <a name="external_stack_name"></a>3. Property `External Hosts Inventory > external_stack_name`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** General stack name of this external inventory / project.

## <a name="plugin"></a>4. Property `External Hosts Inventory > plugin`

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |

**Description:** Id of ansible inventory plugin, needs to be set exactly.

Must be one of:

* "pxc.cloud.ext_hosts_inv"

## <a name="host_groups"></a>5. Property `External Hosts Inventory > host_groups`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Generic ansible hosts.

## <a name="typed_host_groups"></a>6. Property `External Hosts Inventory > typed_host_groups`

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

**Description:** Specialized hosts / groups with typed vars needed for running specific pxc playbooks that are available for external non proxmox hosts.

| Property                                             | Pattern | Type   | Deprecated | Definition | Title/Description                                                                                             |
| ---------------------------------------------------- | ------- | ------ | ---------- | ---------- | ------------------------------------------------------------------------------------------------------------- |
| - [k0s_edge](#typed_host_groups_k0s_edge )           | No      | object | No         | -          | K0s edge system on apt compatible systems (debian, ubuntu). Currently only supports single node edge systems. |
| - [backup_daemon](#typed_host_groups_backup_daemon ) | No      | object | No         | -          | External host to turn into a backup server for proxmox cloud kubernetes systems.                              |

### <a name="typed_host_groups_k0s_edge"></a>6.1. Property `External Hosts Inventory > typed_host_groups > k0s_edge`

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

**Description:** K0s edge system on apt compatible systems (debian, ubuntu). Currently only supports single node edge systems.

| Property                                                | Pattern | Type   | Deprecated | Definition | Title/Description                               |
| ------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------------------------------------- |
| + [k0s_single](#typed_host_groups_k0s_edge_k0s_single ) | No      | object | No         | -          | Host that will be installed as k0s single node. |

#### <a name="typed_host_groups_k0s_edge_k0s_single"></a>6.1.1. Property `External Hosts Inventory > typed_host_groups > k0s_edge > k0s_single`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | Yes              |
| **Additional properties** | Any type allowed |

**Description:** Host that will be installed as k0s single node.

| Property                                                                                   | Pattern | Type    | Deprecated | Definition | Title/Description                                                                                                                                                               |
| ------------------------------------------------------------------------------------------ | ------- | ------- | ---------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| + [ansible_host](#typed_host_groups_k0s_edge_k0s_single_ansible_host )                     | No      | string  | No         | -          | -                                                                                                                                                                               |
| + [ansible_user](#typed_host_groups_k0s_edge_k0s_single_ansible_user )                     | No      | string  | No         | -          | -                                                                                                                                                                               |
| - [k0s_conf_local_path](#typed_host_groups_k0s_edge_k0s_single_k0s_conf_local_path )       | No      | string  | No         | -          | Local path on the control node for k0s.yaml config that should be used for the install process.                                                                                 |
| - [k0s_install_args](#typed_host_groups_k0s_edge_k0s_single_k0s_install_args )             | No      | object  | No         | -          | Additional args in key value format that will be rendered as --$KEY='$VALUE' and passed to the k0s install command.                                                             |
| - [zfs_containerd_dataset](#typed_host_groups_k0s_edge_k0s_single_zfs_containerd_dataset ) | No      | boolean | No         | -          | When set to true will create / move existing containerd directory of /var/lib/k0s/containerd to a zfs dataset. Setting this retroactively will stop and restart all containers. |
| + [zpool_csi_parameters](#typed_host_groups_k0s_edge_k0s_single_zpool_csi_parameters )     | No      | object  | No         | -          | Check pxc.cloud.kubespray_inv schema for detailed descriptions of these parameters.                                                                                             |

##### <a name="typed_host_groups_k0s_edge_k0s_single_ansible_host"></a>6.1.1.1. Property `External Hosts Inventory > typed_host_groups > k0s_edge > k0s_single > ansible_host`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

##### <a name="typed_host_groups_k0s_edge_k0s_single_ansible_user"></a>6.1.1.2. Property `External Hosts Inventory > typed_host_groups > k0s_edge > k0s_single > ansible_user`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

##### <a name="typed_host_groups_k0s_edge_k0s_single_k0s_conf_local_path"></a>6.1.1.3. Property `External Hosts Inventory > typed_host_groups > k0s_edge > k0s_single > k0s_conf_local_path`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Local path on the control node for k0s.yaml config that should be used for the install process.

##### <a name="typed_host_groups_k0s_edge_k0s_single_k0s_install_args"></a>6.1.1.4. Property `External Hosts Inventory > typed_host_groups > k0s_edge > k0s_single > k0s_install_args`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Additional args in key value format that will be rendered as --$KEY='$VALUE' and passed to the k0s install command.

##### <a name="typed_host_groups_k0s_edge_k0s_single_zfs_containerd_dataset"></a>6.1.1.5. Property `External Hosts Inventory > typed_host_groups > k0s_edge > k0s_single > zfs_containerd_dataset`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |

**Description:** When set to true will create / move existing containerd directory of /var/lib/k0s/containerd to a zfs dataset. Setting this retroactively will stop and restart all containers.

##### <a name="typed_host_groups_k0s_edge_k0s_single_zpool_csi_parameters"></a>6.1.1.6. Property `External Hosts Inventory > typed_host_groups > k0s_edge > k0s_single > zpool_csi_parameters`

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | Yes         |
| **Additional properties** | Not allowed |

**Description:** Check pxc.cloud.kubespray_inv schema for detailed descriptions of these parameters.

| Property                                                                                          | Pattern | Type            | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------------------------------- | ------- | --------------- | ---------- | ---------- | ----------------- |
| + [pool_properties](#typed_host_groups_k0s_edge_k0s_single_zpool_csi_parameters_pool_properties ) | No      | object          | No         | -          | -                 |
| + [vdevs](#typed_host_groups_k0s_edge_k0s_single_zpool_csi_parameters_vdevs )                     | No      | array of object | No         | -          | -                 |

###### <a name="typed_host_groups_k0s_edge_k0s_single_zpool_csi_parameters_pool_properties"></a>6.1.1.6.1. Property `External Hosts Inventory > typed_host_groups > k0s_edge > k0s_single > zpool_csi_parameters > pool_properties`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | Yes              |
| **Additional properties** | Any type allowed |

###### <a name="typed_host_groups_k0s_edge_k0s_single_zpool_csi_parameters_vdevs"></a>6.1.1.6.2. Property `External Hosts Inventory > typed_host_groups > k0s_edge > k0s_single > zpool_csi_parameters > vdevs`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | Yes               |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                                                        | Description |
| -------------------------------------------------------------------------------------- | ----------- |
| [vdevs items](#typed_host_groups_k0s_edge_k0s_single_zpool_csi_parameters_vdevs_items) | -           |

###### <a name="typed_host_groups_k0s_edge_k0s_single_zpool_csi_parameters_vdevs_items"></a>6.1.1.6.2.1. External Hosts Inventory > typed_host_groups > k0s_edge > k0s_single > zpool_csi_parameters > vdevs > vdevs items

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

| Property                                                                                  | Pattern | Type            | Deprecated | Definition | Title/Description |
| ----------------------------------------------------------------------------------------- | ------- | --------------- | ---------- | ---------- | ----------------- |
| + [disks](#typed_host_groups_k0s_edge_k0s_single_zpool_csi_parameters_vdevs_items_disks ) | No      | array of string | No         | -          | -                 |
| - [role](#typed_host_groups_k0s_edge_k0s_single_zpool_csi_parameters_vdevs_items_role )   | No      | string          | No         | -          | -                 |
| - [type](#typed_host_groups_k0s_edge_k0s_single_zpool_csi_parameters_vdevs_items_type )   | No      | string          | No         | -          | -                 |

###### <a name="typed_host_groups_k0s_edge_k0s_single_zpool_csi_parameters_vdevs_items_disks"></a>6.1.1.6.2.1.1. Property `External Hosts Inventory > typed_host_groups > k0s_edge > k0s_single > zpool_csi_parameters > vdevs > vdevs items > disks`

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

| Each item of this array must be                                                                    | Description |
| -------------------------------------------------------------------------------------------------- | ----------- |
| [disks items](#typed_host_groups_k0s_edge_k0s_single_zpool_csi_parameters_vdevs_items_disks_items) | -           |

###### <a name="typed_host_groups_k0s_edge_k0s_single_zpool_csi_parameters_vdevs_items_disks_items"></a>6.1.1.6.2.1.1.1. External Hosts Inventory > typed_host_groups > k0s_edge > k0s_single > zpool_csi_parameters > vdevs > vdevs items > disks > disks items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

###### <a name="typed_host_groups_k0s_edge_k0s_single_zpool_csi_parameters_vdevs_items_role"></a>6.1.1.6.2.1.2. Property `External Hosts Inventory > typed_host_groups > k0s_edge > k0s_single > zpool_csi_parameters > vdevs > vdevs items > role`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

###### <a name="typed_host_groups_k0s_edge_k0s_single_zpool_csi_parameters_vdevs_items_type"></a>6.1.1.6.2.1.3. Property `External Hosts Inventory > typed_host_groups > k0s_edge > k0s_single > zpool_csi_parameters > vdevs > vdevs items > type`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

### <a name="typed_host_groups_backup_daemon"></a>6.2. Property `External Hosts Inventory > typed_host_groups > backup_daemon`

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

**Description:** External host to turn into a backup server for proxmox cloud kubernetes systems.

| Property                                                     | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| + [bdd_server](#typed_host_groups_backup_daemon_bdd_server ) | No      | object | No         | -          | -                 |

#### <a name="typed_host_groups_backup_daemon_bdd_server"></a>6.2.1. Property `External Hosts Inventory > typed_host_groups > backup_daemon > bdd_server`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | Yes              |
| **Additional properties** | Any type allowed |

| Property                                                                                          | Pattern | Type   | Deprecated | Definition | Title/Description                                                                                                                                                                                                         |
| ------------------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| + [ansible_host](#typed_host_groups_backup_daemon_bdd_server_ansible_host )                       | No      | string | No         | -          | -                                                                                                                                                                                                                         |
| + [ansible_user](#typed_host_groups_backup_daemon_bdd_server_ansible_user )                       | No      | string | No         | -          | -                                                                                                                                                                                                                         |
| - [use_existing_zpool](#typed_host_groups_backup_daemon_bdd_server_use_existing_zpool )           | No      | object | No         | -          | When this is specified the backup server will use the existing pool and create its own sub dataset for storing backups at<br />$EXISTING_POOL/sub-bdd.<br />                                                              |
| - [zpool_backup_parameters](#typed_host_groups_backup_daemon_bdd_server_zpool_backup_parameters ) | No      | object | No         | -          | Check pxc.cloud.kubespray_inv schema for detailed descriptions of these parameters. The playbook will create the core<br />pool named tank-bdd and will create a sub dataset for any stack that send backups to it.<br /> |

##### <a name="typed_host_groups_backup_daemon_bdd_server_ansible_host"></a>6.2.1.1. Property `External Hosts Inventory > typed_host_groups > backup_daemon > bdd_server > ansible_host`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

##### <a name="typed_host_groups_backup_daemon_bdd_server_ansible_user"></a>6.2.1.2. Property `External Hosts Inventory > typed_host_groups > backup_daemon > bdd_server > ansible_user`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

##### <a name="typed_host_groups_backup_daemon_bdd_server_use_existing_zpool"></a>6.2.1.3. Property `External Hosts Inventory > typed_host_groups > backup_daemon > bdd_server > use_existing_zpool`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** When this is specified the backup server will use the existing pool and create its own sub dataset for storing backups at
$EXISTING_POOL/sub-bdd.

| Property                                                                                 | Pattern | Type   | Deprecated | Definition | Title/Description                  |
| ---------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ---------------------------------- |
| + [pool_name](#typed_host_groups_backup_daemon_bdd_server_use_existing_zpool_pool_name ) | No      | string | No         | -          | Name of the existing zpool to use. |

###### <a name="typed_host_groups_backup_daemon_bdd_server_use_existing_zpool_pool_name"></a>6.2.1.3.1. Property `External Hosts Inventory > typed_host_groups > backup_daemon > bdd_server > use_existing_zpool > pool_name`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Name of the existing zpool to use.

##### <a name="typed_host_groups_backup_daemon_bdd_server_zpool_backup_parameters"></a>6.2.1.4. Property `External Hosts Inventory > typed_host_groups > backup_daemon > bdd_server > zpool_backup_parameters`

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

**Description:** Check pxc.cloud.kubespray_inv schema for detailed descriptions of these parameters. The playbook will create the core
pool named tank-bdd and will create a sub dataset for any stack that send backups to it.

| Property                                                                                                  | Pattern | Type            | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------------------------------------------- | ------- | --------------- | ---------- | ---------- | ----------------- |
| + [pool_properties](#typed_host_groups_backup_daemon_bdd_server_zpool_backup_parameters_pool_properties ) | No      | object          | No         | -          | -                 |
| + [vdevs](#typed_host_groups_backup_daemon_bdd_server_zpool_backup_parameters_vdevs )                     | No      | array of object | No         | -          | -                 |

###### <a name="typed_host_groups_backup_daemon_bdd_server_zpool_backup_parameters_pool_properties"></a>6.2.1.4.1. Property `External Hosts Inventory > typed_host_groups > backup_daemon > bdd_server > zpool_backup_parameters > pool_properties`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | Yes              |
| **Additional properties** | Any type allowed |

###### <a name="typed_host_groups_backup_daemon_bdd_server_zpool_backup_parameters_vdevs"></a>6.2.1.4.2. Property `External Hosts Inventory > typed_host_groups > backup_daemon > bdd_server > zpool_backup_parameters > vdevs`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | Yes               |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                                                                | Description |
| ---------------------------------------------------------------------------------------------- | ----------- |
| [vdevs items](#typed_host_groups_backup_daemon_bdd_server_zpool_backup_parameters_vdevs_items) | -           |

###### <a name="typed_host_groups_backup_daemon_bdd_server_zpool_backup_parameters_vdevs_items"></a>6.2.1.4.2.1. External Hosts Inventory > typed_host_groups > backup_daemon > bdd_server > zpool_backup_parameters > vdevs > vdevs items

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

| Property                                                                                          | Pattern | Type            | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------------------------------- | ------- | --------------- | ---------- | ---------- | ----------------- |
| + [disks](#typed_host_groups_backup_daemon_bdd_server_zpool_backup_parameters_vdevs_items_disks ) | No      | array of string | No         | -          | -                 |
| - [role](#typed_host_groups_backup_daemon_bdd_server_zpool_backup_parameters_vdevs_items_role )   | No      | string          | No         | -          | -                 |
| - [type](#typed_host_groups_backup_daemon_bdd_server_zpool_backup_parameters_vdevs_items_type )   | No      | string          | No         | -          | -                 |

###### <a name="typed_host_groups_backup_daemon_bdd_server_zpool_backup_parameters_vdevs_items_disks"></a>6.2.1.4.2.1.1. Property `External Hosts Inventory > typed_host_groups > backup_daemon > bdd_server > zpool_backup_parameters > vdevs > vdevs items > disks`

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

| Each item of this array must be                                                                            | Description |
| ---------------------------------------------------------------------------------------------------------- | ----------- |
| [disks items](#typed_host_groups_backup_daemon_bdd_server_zpool_backup_parameters_vdevs_items_disks_items) | -           |

###### <a name="typed_host_groups_backup_daemon_bdd_server_zpool_backup_parameters_vdevs_items_disks_items"></a>6.2.1.4.2.1.1.1. External Hosts Inventory > typed_host_groups > backup_daemon > bdd_server > zpool_backup_parameters > vdevs > vdevs items > disks > disks items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

###### <a name="typed_host_groups_backup_daemon_bdd_server_zpool_backup_parameters_vdevs_items_role"></a>6.2.1.4.2.1.2. Property `External Hosts Inventory > typed_host_groups > backup_daemon > bdd_server > zpool_backup_parameters > vdevs > vdevs items > role`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

###### <a name="typed_host_groups_backup_daemon_bdd_server_zpool_backup_parameters_vdevs_items_type"></a>6.2.1.4.2.1.3. Property `External Hosts Inventory > typed_host_groups > backup_daemon > bdd_server > zpool_backup_parameters > vdevs > vdevs items > type`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

