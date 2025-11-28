# Cloud Inventory

**Title:** Cloud Inventory

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

**Description:** Definitions for a proxmox cloud.

| Property                                                           | Pattern | Type             | Deprecated | Definition | Title/Description                                                                                                                         |
| ------------------------------------------------------------------ | ------- | ---------------- | ---------- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| + [pve_vm_subnet](#pve_vm_subnet )                                 | No      | string           | No         | -          | Subnet this PVE cluster uses for its VMs.                                                                                                 |
| + [pve_cloud_domain](#pve_cloud_domain )                           | No      | string           | No         | -          | The overarching domain for the cloud. Will also be used for ddns.                                                                         |
| + [pve_clusters](#pve_clusters )                                   | No      | object           | No         | -          | Definitions for specific Proxmox clusters that will be part of the cloud. Keys are hostnames.                                             |
| + [bind_master_ip](#bind_master_ip )                               | No      | string           | No         | -          | IP of the primary bind dns for this cluster, will be statically assigned.                                                                 |
| + [bind_slave_ip](#bind_slave_ip )                                 | No      | string           | No         | -          | IP of the slave bind dns for this cluster.                                                                                                |
| + [bind_arpa_zone_service_lxcs](#bind_arpa_zone_service_lxcs )     | No      | string           | No         | -          | Arpa zone in which service lxcs with static ips will manuall get their reverse dns entries.                                               |
| + [bind_additional_arpa_zones](#bind_additional_arpa_zones )       | No      | array            | No         | -          | Additional arpa zones which should be created and managed in the dns / dhcp ddns.                                                         |
| + [bind_zone_admin_email](#bind_zone_admin_email )                 | No      | string           | No         | -          | Required adminstrator email in bind format for bind zones.                                                                                |
| - [bind_forward_zones](#bind_forward_zones )                       | No      | array of object  | No         | -          | Creates zone in bind and delegation ns records to the specified nameservers.                                                              |
| + [kea_dhcp_main_ip](#kea_dhcp_main_ip )                           | No      | string           | No         | -          | Static assigned ip for the main dhcp server.                                                                                              |
| + [kea_dhcp_failover_ip](#kea_dhcp_failover_ip )                   | No      | string           | No         | -          | Static ip for slave dhcp server.                                                                                                          |
| + [kea_dhcp_routers](#kea_dhcp_routers )                           | No      | string           | No         | -          | option-data for kea dhcp routers. The default route router that the dhcp will communicate.                                                |
| + [kea_dhcp_pools](#kea_dhcp_pools )                               | No      | array of string  | No         | -          | Address pools that the dhcp allocates from. Has to be within pve_vm_subnet cidr.                                                          |
| + [kea_dhcp_static_routes](#kea_dhcp_static_routes )               | No      | string           | No         | -          | classless-static-routes for kea option-data. Extra routes you want the dhcp to communicate, for example to a custom VPN gateway.          |
| - [kea_dhcp_ceph_frontend_subnet](#kea_dhcp_ceph_frontend_subnet ) | No      | string           | No         | -          | Optional cidr definition for a seperate dhcp if the ceph frontend resides on a different interface (map it inside the dhcp lxcs to pve0). |
| - [kea_dhcp_ceph_frontend_pool](#kea_dhcp_ceph_frontend_pool )     | No      | string           | No         | -          | Pool kea definition for ceph frontend ip allocations, this way monitors can have their static block.                                      |
| - [acme_contact](#acme_contact )                                   | No      | string           | No         | -          | Email address to use for acme account creation.                                                                                           |
| - [acme_method](#acme_method )                                     | No      | enum (of string) | No         | -          | PVE Cloud included method for solving dns01 challenges.                                                                                   |
| - [pve_cloud_pytest](#pve_cloud_pytest )                           | No      | object           | No         | -          | Variables object used only in e2e tests.                                                                                                  |
| - [plugin](#plugin )                                               | No      | enum (of string) | No         | -          | Id of ansible inventory plugin, needs to be set exactly.                                                                                  |

## <a name="pve_vm_subnet"></a>1. Property `Cloud Inventory > pve_vm_subnet`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Subnet this PVE cluster uses for its VMs.

## <a name="pve_cloud_domain"></a>2. Property `Cloud Inventory > pve_cloud_domain`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** The overarching domain for the cloud. Will also be used for ddns.

## <a name="pve_clusters"></a>3. Property `Cloud Inventory > pve_clusters`

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | Yes         |
| **Additional properties** | Not allowed |

**Description:** Definitions for specific Proxmox clusters that will be part of the cloud. Keys are hostnames.

| Property                          | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [^.*$](#pve_clusters_pattern1 ) | Yes     | object | No         | -          | PVE cluster fqdn  |

### <a name="pve_clusters_pattern1"></a>3.1. Pattern Property `Cloud Inventory > pve_clusters > PVE cluster fqdn`
> All properties whose name matches the regular expression
```^.*$``` ([Test](https://regex101.com/?regex=%5E.%2A%24))
must respect the following conditions

**Title:** PVE cluster fqdn

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

**Description:** Fully quantified name for the cluster.

| Property                                                                                       | Pattern | Type                      | Deprecated | Definition | Title/Description                                                                                                                            |
| ---------------------------------------------------------------------------------------------- | ------- | ------------------------- | ---------- | ---------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| - [pve_haproxy_floating_ip](#pve_clusters_pattern1_pve_haproxy_floating_ip )                   | No      | string                    | No         | -          | Floating ip of our central cluster HAProxy.                                                                                                  |
| - [pve_haproxy_floating_ip_internal](#pve_clusters_pattern1_pve_haproxy_floating_ip_internal ) | No      | string                    | No         | -          | Floating ip that is exclusively accessible from inside the cloud / location. External forwardings should be made to pve_haproxy_floating_ip. |
| + [pve_unique_cloud_services](#pve_clusters_pattern1_pve_unique_cloud_services )               | No      | array of enum (of string) | No         | -          | Unique service the cluster provides for its cloud. Unique in the sense that only one cluster may provide each of the services.               |
| - [pve_host_vars](#pve_clusters_pattern1_pve_host_vars )                                       | No      | object                    | No         | -          | Optional variables that will be specifically set for a pve host. Key is the simple host name.                                                |

#### <a name="pve_clusters_pattern1_pve_haproxy_floating_ip"></a>3.1.1. Property `Cloud Inventory > pve_clusters > PVE cluster fqdn > pve_haproxy_floating_ip`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Floating ip of our central cluster HAProxy.

#### <a name="pve_clusters_pattern1_pve_haproxy_floating_ip_internal"></a>3.1.2. Property `Cloud Inventory > pve_clusters > PVE cluster fqdn > pve_haproxy_floating_ip_internal`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Floating ip that is exclusively accessible from inside the cloud / location. External forwardings should be made to pve_haproxy_floating_ip.

#### <a name="pve_clusters_pattern1_pve_unique_cloud_services"></a>3.1.3. Property `Cloud Inventory > pve_clusters > PVE cluster fqdn > pve_unique_cloud_services`

|              |                             |
| ------------ | --------------------------- |
| **Type**     | `array of enum (of string)` |
| **Required** | Yes                         |

**Description:** Unique service the cluster provides for its cloud. Unique in the sense that only one cluster may provide each of the services.

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                                                           | Description |
| ----------------------------------------------------------------------------------------- | ----------- |
| [pve_unique_cloud_services items](#pve_clusters_pattern1_pve_unique_cloud_services_items) | -           |

##### <a name="pve_clusters_pattern1_pve_unique_cloud_services_items"></a>3.1.3.1. Cloud Inventory > pve_clusters > PVE cluster fqdn > pve_unique_cloud_services > pve_unique_cloud_services items

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |

Must be one of:
* "dns"
* "dhcp"
* "psql-state"

#### <a name="pve_clusters_pattern1_pve_host_vars"></a>3.1.4. Property `Cloud Inventory > pve_clusters > PVE cluster fqdn > pve_host_vars`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Optional variables that will be specifically set for a pve host. Key is the simple host name.

| Property                                                                       | Pattern | Type            | Deprecated | Definition | Title/Description                                                                                                                                                                        |
| ------------------------------------------------------------------------------ | ------- | --------------- | ---------- | ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| - [wol_iface](#pve_clusters_pattern1_pve_host_vars_wol_iface )                 | No      | string          | No         | -          | Inteface wol should be enabled using ethtool.                                                                                                                                            |
| - [tso_gso_fix](#pve_clusters_pattern1_pve_host_vars_tso_gso_fix )             | No      | array           | No         | -          | Will turn of network optimizations on old network cards, this assures they can run indefinetly. Will only take effect with the e1000_driver_fix playbook.                                |
| - [mac_iface_mapping](#pve_clusters_pattern1_pve_host_vars_mac_iface_mapping ) | No      | array of object | No         | -          | Map mac addresses to interface names, will be picked up by setup playbooks. This will actually change the interfaces names on the host aswell as try to replace /etc/network/interfaces. |

##### <a name="pve_clusters_pattern1_pve_host_vars_wol_iface"></a>3.1.4.1. Property `Cloud Inventory > pve_clusters > PVE cluster fqdn > pve_host_vars > wol_iface`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Inteface wol should be enabled using ethtool.

##### <a name="pve_clusters_pattern1_pve_host_vars_tso_gso_fix"></a>3.1.4.2. Property `Cloud Inventory > pve_clusters > PVE cluster fqdn > pve_host_vars > tso_gso_fix`

|              |         |
| ------------ | ------- |
| **Type**     | `array` |
| **Required** | No      |

**Description:** Will turn of network optimizations on old network cards, this assures they can run indefinetly. Will only take effect with the e1000_driver_fix playbook.

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | N/A                |

##### <a name="pve_clusters_pattern1_pve_host_vars_mac_iface_mapping"></a>3.1.4.3. Property `Cloud Inventory > pve_clusters > PVE cluster fqdn > pve_host_vars > mac_iface_mapping`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | No                |

**Description:** Map mac addresses to interface names, will be picked up by setup playbooks. This will actually change the interfaces names on the host aswell as try to replace /etc/network/interfaces.

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                                                         | Description |
| --------------------------------------------------------------------------------------- | ----------- |
| [mac_iface_mapping items](#pve_clusters_pattern1_pve_host_vars_mac_iface_mapping_items) | -           |

###### <a name="pve_clusters_pattern1_pve_host_vars_mac_iface_mapping_items"></a>3.1.4.3.1. Cloud Inventory > pve_clusters > PVE cluster fqdn > pve_host_vars > mac_iface_mapping > mac_iface_mapping items

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

| Property                                                                             | Pattern | Type   | Deprecated | Definition | Title/Description                                                                 |
| ------------------------------------------------------------------------------------ | ------- | ------ | ---------- | ---------- | --------------------------------------------------------------------------------- |
| + [mac_addr](#pve_clusters_pattern1_pve_host_vars_mac_iface_mapping_items_mac_addr ) | No      | string | No         | -          | Network device mac address.                                                       |
| + [iface](#pve_clusters_pattern1_pve_host_vars_mac_iface_mapping_items_iface )       | No      | string | No         | -          | Interface name that will be assigned to the device. Default name will be removed! |

###### <a name="pve_clusters_pattern1_pve_host_vars_mac_iface_mapping_items_mac_addr"></a>3.1.4.3.1.1. Property `Cloud Inventory > pve_clusters > PVE cluster fqdn > pve_host_vars > mac_iface_mapping > mac_iface_mapping items > mac_addr`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Network device mac address.

###### <a name="pve_clusters_pattern1_pve_host_vars_mac_iface_mapping_items_iface"></a>3.1.4.3.1.2. Property `Cloud Inventory > pve_clusters > PVE cluster fqdn > pve_host_vars > mac_iface_mapping > mac_iface_mapping items > iface`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Interface name that will be assigned to the device. Default name will be removed!

## <a name="bind_master_ip"></a>4. Property `Cloud Inventory > bind_master_ip`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** IP of the primary bind dns for this cluster, will be statically assigned.

## <a name="bind_slave_ip"></a>5. Property `Cloud Inventory > bind_slave_ip`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** IP of the slave bind dns for this cluster.

## <a name="bind_arpa_zone_service_lxcs"></a>6. Property `Cloud Inventory > bind_arpa_zone_service_lxcs`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Arpa zone in which service lxcs with static ips will manuall get their reverse dns entries.

## <a name="bind_additional_arpa_zones"></a>7. Property `Cloud Inventory > bind_additional_arpa_zones`

|              |         |
| ------------ | ------- |
| **Type**     | `array` |
| **Required** | Yes     |

**Description:** Additional arpa zones which should be created and managed in the dns / dhcp ddns.

**Example:**

```json
"1.168.192.in-addr.arpa"
```

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | N/A                |

## <a name="bind_zone_admin_email"></a>8. Property `Cloud Inventory > bind_zone_admin_email`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Required adminstrator email in bind format for bind zones.

**Example:**

```json
"admin.example.com."
```

## <a name="bind_forward_zones"></a>9. Property `Cloud Inventory > bind_forward_zones`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | No                |

**Description:** Creates zone in bind and delegation ns records to the specified nameservers.

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                       | Description |
| ----------------------------------------------------- | ----------- |
| [bind_forward_zones items](#bind_forward_zones_items) | -           |

### <a name="bind_forward_zones_items"></a>9.1. Cloud Inventory > bind_forward_zones > bind_forward_zones items

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

| Property                                                | Pattern | Type            | Deprecated | Definition | Title/Description |
| ------------------------------------------------------- | ------- | --------------- | ---------- | ---------- | ----------------- |
| - [zone](#bind_forward_zones_items_zone )               | No      | string          | No         | -          | -                 |
| - [nameservers](#bind_forward_zones_items_nameservers ) | No      | array of string | No         | -          | -                 |

#### <a name="bind_forward_zones_items_zone"></a>9.1.1. Property `Cloud Inventory > bind_forward_zones > bind_forward_zones items > zone`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

#### <a name="bind_forward_zones_items_nameservers"></a>9.1.2. Property `Cloud Inventory > bind_forward_zones > bind_forward_zones items > nameservers`

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

| Each item of this array must be                                  | Description |
| ---------------------------------------------------------------- | ----------- |
| [nameservers items](#bind_forward_zones_items_nameservers_items) | -           |

##### <a name="bind_forward_zones_items_nameservers_items"></a>9.1.2.1. Cloud Inventory > bind_forward_zones > bind_forward_zones items > nameservers > nameservers items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="kea_dhcp_main_ip"></a>10. Property `Cloud Inventory > kea_dhcp_main_ip`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Static assigned ip for the main dhcp server.

## <a name="kea_dhcp_failover_ip"></a>11. Property `Cloud Inventory > kea_dhcp_failover_ip`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Static ip for slave dhcp server.

## <a name="kea_dhcp_routers"></a>12. Property `Cloud Inventory > kea_dhcp_routers`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** option-data for kea dhcp routers. The default route router that the dhcp will communicate.

## <a name="kea_dhcp_pools"></a>13. Property `Cloud Inventory > kea_dhcp_pools`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of string` |
| **Required** | Yes               |

**Description:** Address pools that the dhcp allocates from. Has to be within pve_vm_subnet cidr.

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be               | Description                        |
| --------------------------------------------- | ---------------------------------- |
| [kea_dhcp_pools items](#kea_dhcp_pools_items) | IPV4 Address range in keas format. |

### <a name="kea_dhcp_pools_items"></a>13.1. Cloud Inventory > kea_dhcp_pools > kea_dhcp_pools items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** IPV4 Address range in keas format.

**Example:**

```json
"192.168.1.2 - 192.168.1.199"
```

## <a name="kea_dhcp_static_routes"></a>14. Property `Cloud Inventory > kea_dhcp_static_routes`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** classless-static-routes for kea option-data. Extra routes you want the dhcp to communicate, for example to a custom VPN gateway.

**Example:**

```json
"0.0.0.0/0 - 192.168.1.1, 10.0.2.0/24 - 192.168.1.217"
```

## <a name="kea_dhcp_ceph_frontend_subnet"></a>15. Property `Cloud Inventory > kea_dhcp_ceph_frontend_subnet`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Optional cidr definition for a seperate dhcp if the ceph frontend resides on a different interface (map it inside the dhcp lxcs to pve0).

**Example:**

```json
"10.255.42.0/23"
```

## <a name="kea_dhcp_ceph_frontend_pool"></a>16. Property `Cloud Inventory > kea_dhcp_ceph_frontend_pool`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Pool kea definition for ceph frontend ip allocations, this way monitors can have their static block.

**Example:**

```json
"10.255.42.17 - 10.255.43.254"
```

## <a name="acme_contact"></a>17. Property `Cloud Inventory > acme_contact`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Email address to use for acme account creation.

## <a name="acme_method"></a>18. Property `Cloud Inventory > acme_method`

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |

**Description:** PVE Cloud included method for solving dns01 challenges.

Must be one of:
* "route53"
* "ionos"

## <a name="pve_cloud_pytest"></a>19. Property `Cloud Inventory > pve_cloud_pytest`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Variables object used only in e2e tests.

## <a name="plugin"></a>20. Property `Cloud Inventory > plugin`

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |

**Description:** Id of ansible inventory plugin, needs to be set exactly.

Must be one of:
* "pve.cloud.pve_cloud_inv"

----------------------------------------------------------------------------------------------------------------------------
Generated using [json-schema-for-humans](https://github.com/coveooss/json-schema-for-humans) on 2025-11-28 at 19:22:12 +0000
