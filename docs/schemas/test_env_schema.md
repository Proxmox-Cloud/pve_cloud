# Schema Docs

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

**Description:** Config / Inventory file for pve cloud e2e tests. Schema is merely a merge from the main schemas of the pve_cloud collection.

| Property                                                                 | Pattern | Type             | Deprecated | Definition | Title/Description                                        |
| ------------------------------------------------------------------------ | ------- | ---------------- | ---------- | ---------- | -------------------------------------------------------- |
| - [plugin](#plugin )                                                     | No      | enum (of string) | No         | -          | Id of ansible inventory plugin, needs to be set exactly. |
| + [pve_test_hosts](#pve_test_hosts )                                     | No      | object           | No         | -          | -                                                        |
| + [pve_test_cloud_domain](#pve_test_cloud_domain )                       | No      | string           | No         | -          | -                                                        |
| + [pve_test_deployments_domain](#pve_test_deployments_domain )           | No      | string           | No         | -          | -                                                        |
| + [pve_test_cluster_name](#pve_test_cluster_name )                       | No      | string           | No         | -          | -                                                        |
| + [pve_test_disk_storage_id](#pve_test_disk_storage_id )                 | No      | string           | No         | -          | -                                                        |
| + [pve_test_ceph_csi_storage_id](#pve_test_ceph_csi_storage_id )         | No      | string           | No         | -          | -                                                        |
| + [pve_test_service_lxcs_nameserver](#pve_test_service_lxcs_nameserver ) | No      | string           | No         | -          | -                                                        |
| - [pve_slop_firewall_ip](#pve_slop_firewall_ip )                         | No      | string           | No         | -          | -                                                        |
| + [pve_test_service_lxcs_gateway](#pve_test_service_lxcs_gateway )       | No      | string           | No         | -          | -                                                        |
| + [pve_test_ssh_pub_key](#pve_test_ssh_pub_key )                         | No      | string           | No         | -          | -                                                        |
| + [pve_test_cloud_inv](#pve_test_cloud_inv )                             | No      | object           | No         | -          | -                                                        |
| - [pve_test_host_vars](#pve_test_host_vars )                             | No      | object           | No         | -          | -                                                        |
| + [pve_test_cloud_inv_cluster](#pve_test_cloud_inv_cluster )             | No      | object           | No         | -          | -                                                        |
| - [pve_test_tf_parameters](#pve_test_tf_parameters )                     | No      | object           | No         | -          | -                                                        |

## <a name="plugin"></a>1. Property `root > plugin`

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |

**Description:** Id of ansible inventory plugin, needs to be set exactly.

Must be one of:
* "pve.cloud.pve_cloud_test_env"

## <a name="pve_test_hosts"></a>2. Property `root > pve_test_hosts`

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | Yes         |
| **Additional properties** | Not allowed |

| Property                            | Pattern | Type   | Deprecated | Definition | Title/Description |
| ----------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [^.*$](#pve_test_hosts_pattern1 ) | Yes     | object | No         | -          | PVE Host name     |

### <a name="pve_test_hosts_pattern1"></a>2.1. Pattern Property `root > pve_test_hosts > PVE Host name`
> All properties whose name matches the regular expression
```^.*$``` ([Test](https://regex101.com/?regex=%5E.%2A%24))
must respect the following conditions

**Title:** PVE Host name

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

| Property                                                 | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| + [ansible_user](#pve_test_hosts_pattern1_ansible_user ) | No      | string | No         | -          | -                 |
| + [ansible_host](#pve_test_hosts_pattern1_ansible_host ) | No      | string | No         | -          | -                 |

#### <a name="pve_test_hosts_pattern1_ansible_user"></a>2.1.1. Property `root > pve_test_hosts > PVE Host name > ansible_user`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

#### <a name="pve_test_hosts_pattern1_ansible_host"></a>2.1.2. Property `root > pve_test_hosts > PVE Host name > ansible_host`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

## <a name="pve_test_cloud_domain"></a>3. Property `root > pve_test_cloud_domain`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

## <a name="pve_test_deployments_domain"></a>4. Property `root > pve_test_deployments_domain`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

## <a name="pve_test_cluster_name"></a>5. Property `root > pve_test_cluster_name`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

## <a name="pve_test_disk_storage_id"></a>6. Property `root > pve_test_disk_storage_id`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

## <a name="pve_test_ceph_csi_storage_id"></a>7. Property `root > pve_test_ceph_csi_storage_id`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

## <a name="pve_test_service_lxcs_nameserver"></a>8. Property `root > pve_test_service_lxcs_nameserver`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

## <a name="pve_slop_firewall_ip"></a>9. Property `root > pve_slop_firewall_ip`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="pve_test_service_lxcs_gateway"></a>10. Property `root > pve_test_service_lxcs_gateway`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

## <a name="pve_test_ssh_pub_key"></a>11. Property `root > pve_test_ssh_pub_key`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

## <a name="pve_test_cloud_inv"></a>12. Property `root > pve_test_cloud_inv`

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | Yes         |
| **Additional properties** | Not allowed |

| Property                                                                          | Pattern | Type            | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------------------- | ------- | --------------- | ---------- | ---------- | ----------------- |
| + [pve_vm_subnet](#pve_test_cloud_inv_pve_vm_subnet )                             | No      | string          | No         | -          | -                 |
| + [bind_master_ip](#pve_test_cloud_inv_bind_master_ip )                           | No      | string          | No         | -          | -                 |
| + [bind_slave_ip](#pve_test_cloud_inv_bind_slave_ip )                             | No      | string          | No         | -          | -                 |
| + [bind_arpa_zone_service_lxcs](#pve_test_cloud_inv_bind_arpa_zone_service_lxcs ) | No      | string          | No         | -          | -                 |
| + [bind_additional_arpa_zones](#pve_test_cloud_inv_bind_additional_arpa_zones )   | No      | array of string | No         | -          | -                 |
| + [bind_zone_admin_email](#pve_test_cloud_inv_bind_zone_admin_email )             | No      | string          | No         | -          | -                 |
| - [bind_forward_zones](#pve_test_cloud_inv_bind_forward_zones )                   | No      | array of object | No         | -          | -                 |
| + [kea_dhcp_main_ip](#pve_test_cloud_inv_kea_dhcp_main_ip )                       | No      | string          | No         | -          | -                 |
| + [kea_dhcp_failover_ip](#pve_test_cloud_inv_kea_dhcp_failover_ip )               | No      | string          | No         | -          | -                 |
| + [kea_dhcp_routers](#pve_test_cloud_inv_kea_dhcp_routers )                       | No      | string          | No         | -          | -                 |
| + [kea_dhcp_pools](#pve_test_cloud_inv_kea_dhcp_pools )                           | No      | array of string | No         | -          | -                 |
| + [kea_dhcp_static_routes](#pve_test_cloud_inv_kea_dhcp_static_routes )           | No      | string          | No         | -          | -                 |

### <a name="pve_test_cloud_inv_pve_vm_subnet"></a>12.1. Property `root > pve_test_cloud_inv > pve_vm_subnet`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

### <a name="pve_test_cloud_inv_bind_master_ip"></a>12.2. Property `root > pve_test_cloud_inv > bind_master_ip`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

### <a name="pve_test_cloud_inv_bind_slave_ip"></a>12.3. Property `root > pve_test_cloud_inv > bind_slave_ip`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

### <a name="pve_test_cloud_inv_bind_arpa_zone_service_lxcs"></a>12.4. Property `root > pve_test_cloud_inv > bind_arpa_zone_service_lxcs`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

### <a name="pve_test_cloud_inv_bind_additional_arpa_zones"></a>12.5. Property `root > pve_test_cloud_inv > bind_additional_arpa_zones`

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

| Each item of this array must be                                                          | Description |
| ---------------------------------------------------------------------------------------- | ----------- |
| [bind_additional_arpa_zones items](#pve_test_cloud_inv_bind_additional_arpa_zones_items) | -           |

#### <a name="pve_test_cloud_inv_bind_additional_arpa_zones_items"></a>12.5.1. root > pve_test_cloud_inv > bind_additional_arpa_zones > bind_additional_arpa_zones items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

### <a name="pve_test_cloud_inv_bind_zone_admin_email"></a>12.6. Property `root > pve_test_cloud_inv > bind_zone_admin_email`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

### <a name="pve_test_cloud_inv_bind_forward_zones"></a>12.7. Property `root > pve_test_cloud_inv > bind_forward_zones`

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

| Each item of this array must be                                          | Description |
| ------------------------------------------------------------------------ | ----------- |
| [bind_forward_zones items](#pve_test_cloud_inv_bind_forward_zones_items) | -           |

#### <a name="pve_test_cloud_inv_bind_forward_zones_items"></a>12.7.1. root > pve_test_cloud_inv > bind_forward_zones > bind_forward_zones items

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

| Property                                                                   | Pattern | Type            | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------------- | ------- | --------------- | ---------- | ---------- | ----------------- |
| - [zone](#pve_test_cloud_inv_bind_forward_zones_items_zone )               | No      | string          | No         | -          | -                 |
| - [nameservers](#pve_test_cloud_inv_bind_forward_zones_items_nameservers ) | No      | array of string | No         | -          | -                 |

##### <a name="pve_test_cloud_inv_bind_forward_zones_items_zone"></a>12.7.1.1. Property `root > pve_test_cloud_inv > bind_forward_zones > bind_forward_zones items > zone`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

##### <a name="pve_test_cloud_inv_bind_forward_zones_items_nameservers"></a>12.7.1.2. Property `root > pve_test_cloud_inv > bind_forward_zones > bind_forward_zones items > nameservers`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of string` |
| **Required** | No                |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                                                     | Description |
| ----------------------------------------------------------------------------------- | ----------- |
| [nameservers items](#pve_test_cloud_inv_bind_forward_zones_items_nameservers_items) | -           |

###### <a name="pve_test_cloud_inv_bind_forward_zones_items_nameservers_items"></a>12.7.1.2.1. root > pve_test_cloud_inv > bind_forward_zones > bind_forward_zones items > nameservers > nameservers items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

### <a name="pve_test_cloud_inv_kea_dhcp_main_ip"></a>12.8. Property `root > pve_test_cloud_inv > kea_dhcp_main_ip`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

### <a name="pve_test_cloud_inv_kea_dhcp_failover_ip"></a>12.9. Property `root > pve_test_cloud_inv > kea_dhcp_failover_ip`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

### <a name="pve_test_cloud_inv_kea_dhcp_routers"></a>12.10. Property `root > pve_test_cloud_inv > kea_dhcp_routers`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

### <a name="pve_test_cloud_inv_kea_dhcp_pools"></a>12.11. Property `root > pve_test_cloud_inv > kea_dhcp_pools`

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

| Each item of this array must be                                  | Description |
| ---------------------------------------------------------------- | ----------- |
| [kea_dhcp_pools items](#pve_test_cloud_inv_kea_dhcp_pools_items) | -           |

#### <a name="pve_test_cloud_inv_kea_dhcp_pools_items"></a>12.11.1. root > pve_test_cloud_inv > kea_dhcp_pools > kea_dhcp_pools items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

### <a name="pve_test_cloud_inv_kea_dhcp_static_routes"></a>12.12. Property `root > pve_test_cloud_inv > kea_dhcp_static_routes`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

## <a name="pve_test_host_vars"></a>13. Property `root > pve_test_host_vars`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

| Property                                | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [^.*$](#pve_test_host_vars_pattern1 ) | Yes     | object | No         | -          | PVE Host name     |

### <a name="pve_test_host_vars_pattern1"></a>13.1. Pattern Property `root > pve_test_host_vars > PVE Host name`
> All properties whose name matches the regular expression
```^.*$``` ([Test](https://regex101.com/?regex=%5E.%2A%24))
must respect the following conditions

**Title:** PVE Host name

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

## <a name="pve_test_cloud_inv_cluster"></a>14. Property `root > pve_test_cloud_inv_cluster`

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | Yes         |
| **Additional properties** | Not allowed |

| Property                                                                                            | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| + [pve_haproxy_floating_ip](#pve_test_cloud_inv_cluster_pve_haproxy_floating_ip )                   | No      | string | No         | -          | -                 |
| + [pve_haproxy_floating_ip_internal](#pve_test_cloud_inv_cluster_pve_haproxy_floating_ip_internal ) | No      | string | No         | -          | -                 |

### <a name="pve_test_cloud_inv_cluster_pve_haproxy_floating_ip"></a>14.1. Property `root > pve_test_cloud_inv_cluster > pve_haproxy_floating_ip`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

### <a name="pve_test_cloud_inv_cluster_pve_haproxy_floating_ip_internal"></a>14.2. Property `root > pve_test_cloud_inv_cluster > pve_haproxy_floating_ip_internal`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

## <a name="pve_test_tf_parameters"></a>15. Property `root > pve_test_tf_parameters`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

----------------------------------------------------------------------------------------------------------------------------
Generated using [json-schema-for-humans](https://github.com/coveooss/json-schema-for-humans) on 2025-11-28 at 12:39:47 +0000
