# Schema Docs

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

**Description:** Config / Inventory file for pve cloud e2e tests.

| Property                                                                 | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| + [pve_test_hosts](#pve_test_hosts )                                     | No      | object | No         | -          | -                 |
| + [pve_test_cloud_domain](#pve_test_cloud_domain )                       | No      | string | No         | -          | -                 |
| + [pve_test_cluster_name](#pve_test_cluster_name )                       | No      | string | No         | -          | -                 |
| + [pve_test_disk_storage_id](#pve_test_disk_storage_id )                 | No      | string | No         | -          | -                 |
| + [pve_test_ceph_csi_storage_id](#pve_test_ceph_csi_storage_id )         | No      | string | No         | -          | -                 |
| + [pve_test_service_lxcs_nameserver](#pve_test_service_lxcs_nameserver ) | No      | string | No         | -          | -                 |
| + [pve_test_service_lxcs_gateway](#pve_test_service_lxcs_gateway )       | No      | string | No         | -          | -                 |
| + [pve_test_ssh_pub_key](#pve_test_ssh_pub_key )                         | No      | string | No         | -          | -                 |
| + [pve_test_cloud_inv](#pve_test_cloud_inv )                             | No      | object | No         | -          | -                 |
| - [pve_test_host_vars](#pve_test_host_vars )                             | No      | object | No         | -          | -                 |
| + [pve_test_cloud_inv_cluster](#pve_test_cloud_inv_cluster )             | No      | object | No         | -          | -                 |
| + [pve_test_deployments_domain](#pve_test_deployments_domain )               | No      | string | No         | -          | -                 |

## <a name="pve_test_hosts"></a>1. Property `root > pve_test_hosts`

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | Yes         |
| **Additional properties** | Not allowed |

| Property                            | Pattern | Type   | Deprecated | Definition | Title/Description |
| ----------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [^.*$](#pve_test_hosts_pattern1 ) | Yes     | object | No         | -          | PVE Host name     |

### <a name="pve_test_hosts_pattern1"></a>1.1. Pattern Property `root > pve_test_hosts > PVE Host name`
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

#### <a name="pve_test_hosts_pattern1_ansible_user"></a>1.1.1. Property `root > pve_test_hosts > PVE Host name > ansible_user`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

#### <a name="pve_test_hosts_pattern1_ansible_host"></a>1.1.2. Property `root > pve_test_hosts > PVE Host name > ansible_host`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

## <a name="pve_test_cloud_domain"></a>2. Property `root > pve_test_cloud_domain`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

## <a name="pve_test_cluster_name"></a>3. Property `root > pve_test_cluster_name`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

## <a name="pve_test_disk_storage_id"></a>4. Property `root > pve_test_disk_storage_id`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

## <a name="pve_test_ceph_csi_storage_id"></a>5. Property `root > pve_test_ceph_csi_storage_id`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

## <a name="pve_test_service_lxcs_nameserver"></a>6. Property `root > pve_test_service_lxcs_nameserver`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

## <a name="pve_test_service_lxcs_gateway"></a>7. Property `root > pve_test_service_lxcs_gateway`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

## <a name="pve_test_ssh_pub_key"></a>8. Property `root > pve_test_ssh_pub_key`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

## <a name="pve_test_cloud_inv"></a>9. Property `root > pve_test_cloud_inv`

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
| + [kea_dhcp_main_ip](#pve_test_cloud_inv_kea_dhcp_main_ip )                       | No      | string          | No         | -          | -                 |
| + [kea_dhcp_failover_ip](#pve_test_cloud_inv_kea_dhcp_failover_ip )               | No      | string          | No         | -          | -                 |
| + [kea_dhcp_routers](#pve_test_cloud_inv_kea_dhcp_routers )                       | No      | string          | No         | -          | -                 |
| + [kea_dhcp_pools](#pve_test_cloud_inv_kea_dhcp_pools )                           | No      | array of string | No         | -          | -                 |
| + [kea_dhcp_static_routes](#pve_test_cloud_inv_kea_dhcp_static_routes )           | No      | string          | No         | -          | -                 |

### <a name="pve_test_cloud_inv_pve_vm_subnet"></a>9.1. Property `root > pve_test_cloud_inv > pve_vm_subnet`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

### <a name="pve_test_cloud_inv_bind_master_ip"></a>9.2. Property `root > pve_test_cloud_inv > bind_master_ip`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

### <a name="pve_test_cloud_inv_bind_slave_ip"></a>9.3. Property `root > pve_test_cloud_inv > bind_slave_ip`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

### <a name="pve_test_cloud_inv_bind_arpa_zone_service_lxcs"></a>9.4. Property `root > pve_test_cloud_inv > bind_arpa_zone_service_lxcs`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

### <a name="pve_test_cloud_inv_bind_additional_arpa_zones"></a>9.5. Property `root > pve_test_cloud_inv > bind_additional_arpa_zones`

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

#### <a name="pve_test_cloud_inv_bind_additional_arpa_zones_items"></a>9.5.1. root > pve_test_cloud_inv > bind_additional_arpa_zones > bind_additional_arpa_zones items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

### <a name="pve_test_cloud_inv_bind_zone_admin_email"></a>9.6. Property `root > pve_test_cloud_inv > bind_zone_admin_email`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

### <a name="pve_test_cloud_inv_kea_dhcp_main_ip"></a>9.7. Property `root > pve_test_cloud_inv > kea_dhcp_main_ip`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

### <a name="pve_test_cloud_inv_kea_dhcp_failover_ip"></a>9.8. Property `root > pve_test_cloud_inv > kea_dhcp_failover_ip`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

### <a name="pve_test_cloud_inv_kea_dhcp_routers"></a>9.9. Property `root > pve_test_cloud_inv > kea_dhcp_routers`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

### <a name="pve_test_cloud_inv_kea_dhcp_pools"></a>9.10. Property `root > pve_test_cloud_inv > kea_dhcp_pools`

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

#### <a name="pve_test_cloud_inv_kea_dhcp_pools_items"></a>9.10.1. root > pve_test_cloud_inv > kea_dhcp_pools > kea_dhcp_pools items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

### <a name="pve_test_cloud_inv_kea_dhcp_static_routes"></a>9.11. Property `root > pve_test_cloud_inv > kea_dhcp_static_routes`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

## <a name="pve_test_host_vars"></a>10. Property `root > pve_test_host_vars`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

| Property                                | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [^.*$](#pve_test_host_vars_pattern1 ) | Yes     | object | No         | -          | PVE Host name     |

### <a name="pve_test_host_vars_pattern1"></a>10.1. Pattern Property `root > pve_test_host_vars > PVE Host name`
> All properties whose name matches the regular expression
```^.*$``` ([Test](https://regex101.com/?regex=%5E.%2A%24))
must respect the following conditions

**Title:** PVE Host name

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

## <a name="pve_test_cloud_inv_cluster"></a>11. Property `root > pve_test_cloud_inv_cluster`

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | Yes         |
| **Additional properties** | Not allowed |

| Property                                                                                            | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| + [pve_haproxy_floating_ip](#pve_test_cloud_inv_cluster_pve_haproxy_floating_ip )                   | No      | string | No         | -          | -                 |
| + [pve_haproxy_floating_ip_internal](#pve_test_cloud_inv_cluster_pve_haproxy_floating_ip_internal ) | No      | string | No         | -          | -                 |

### <a name="pve_test_cloud_inv_cluster_pve_haproxy_floating_ip"></a>11.1. Property `root > pve_test_cloud_inv_cluster > pve_haproxy_floating_ip`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

### <a name="pve_test_cloud_inv_cluster_pve_haproxy_floating_ip_internal"></a>11.2. Property `root > pve_test_cloud_inv_cluster > pve_haproxy_floating_ip_internal`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

## <a name="pve_test_deployments_domain"></a>12. Property `root > pve_test_deployments_domain`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

----------------------------------------------------------------------------------------------------------------------------
Generated using [json-schema-for-humans](https://github.com/coveooss/json-schema-for-humans) on 2025-10-30 at 18:43:11 +0100
