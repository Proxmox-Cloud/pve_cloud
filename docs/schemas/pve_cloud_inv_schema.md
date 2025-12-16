# Cloud Inventory

**Title:** Cloud Inventory

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

**Description:** Definitions for a proxmox cloud, setup of proxmox clusters.

| Property                                                       | Pattern | Type             | Deprecated | Definition | Title/Description                                                                                                                                                                                                 |
| -------------------------------------------------------------- | ------- | ---------------- | ---------- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| + [pve_vm_subnet](#pve_vm_subnet )                             | No      | string           | No         | -          | Subnet this PVE cluster uses for its VMs.                                                                                                                                                                         |
| + [pve_cloud_domain](#pve_cloud_domain )                       | No      | string           | No         | -          | The overarching domain for the cloud. Will also be used for ddns.                                                                                                                                                 |
| + [kea_dhcp_main_ip](#kea_dhcp_main_ip )                       | No      | string           | No         | -          | Static assigned ip for the main dhcp server. This has to match your dhcp lxc inventory file!                                                                                                                      |
| + [kea_dhcp_failover_ip](#kea_dhcp_failover_ip )               | No      | string           | No         | -          | Static ip for slave dhcp server. This has to match your dhcp lxc inventory file!                                                                                                                                  |
| + [kea_dhcp_routers](#kea_dhcp_routers )                       | No      | string           | No         | -          | option-data for kea dhcp routers. The default route router that the dhcp will communicate.                                                                                                                        |
| + [kea_dhcp_pools](#kea_dhcp_pools )                           | No      | array of string  | No         | -          | Address pools that the dhcp allocates from. Has to be within pve_vm_subnet cidr.                                                                                                                                  |
| + [kea_dhcp_static_routes](#kea_dhcp_static_routes )           | No      | string           | No         | -          | classless-static-routes for kea option-data. You can pass comma seperated extra routes you want the dhcp to communicate, for example to a custom VPN gateway.<br />                                               |
| + [bind_master_ip](#bind_master_ip )                           | No      | string           | No         | -          | IP of the primary bind dns for this cluster, will be statically assigned. Has to match your bind lxc inventory file!                                                                                              |
| + [bind_slave_ip](#bind_slave_ip )                             | No      | string           | No         | -          | IP of the slave bind dns for this cluster. Has to match your bind lxc inventory file!                                                                                                                             |
| + [bind_arpa_zone_service_lxcs](#bind_arpa_zone_service_lxcs ) | No      | string           | No         | -          | Arpa zone in which service lxcs with static ips will manuall get their reverse dns entries.                                                                                                                       |
| + [bind_additional_arpa_zones](#bind_additional_arpa_zones )   | No      | array of string  | No         | -          | Additional arpa zones which should be created and managed in the dns / dhcp ddns.                                                                                                                                 |
| + [pve_clusters](#pve_clusters )                               | No      | object           | No         | -          | Definitions for specific Proxmox clusters that will be part of the cloud. Keys are hostnames.                                                                                                                     |
| + [bind_zone_admin_email](#bind_zone_admin_email )             | No      | string           | No         | -          | Required adminstrator email in bind format for bind zones.                                                                                                                                                        |
| - [bind_forward_zones](#bind_forward_zones )                   | No      | array of object  | No         | -          | Creates zone in bind and delegation ns records to the specified nameservers. This is very useful if you have other nameservers with <br />their own authoritative zones you want resolved within the cloud.<br /> |
| - [acme_contact](#acme_contact )                               | No      | string           | No         | -          | Email address to use for acme account creation.                                                                                                                                                                   |
| - [acme_method](#acme_method )                                 | No      | enum (of string) | No         | -          | PVE Cloud included method for solving dns01 challenges. You need to have created the appropriate secrets under /etc/pve/cloud on your proxmox cluster.<br />                                                      |
| - [plugin](#plugin )                                           | No      | enum (of string) | No         | -          | Id of ansible inventory plugin, needs to be set exactly.                                                                                                                                                          |

## <a name="pve_vm_subnet"></a>1. Property `Cloud Inventory > pve_vm_subnet`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Subnet this PVE cluster uses for its VMs.

**Example:**

```json
"192.168.10.0/24"
```

## <a name="pve_cloud_domain"></a>2. Property `Cloud Inventory > pve_cloud_domain`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** The overarching domain for the cloud. Will also be used for ddns.

**Example:**

```json
"your-cloud.example.com"
```

## <a name="kea_dhcp_main_ip"></a>3. Property `Cloud Inventory > kea_dhcp_main_ip`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Static assigned ip for the main dhcp server. This has to match your dhcp lxc inventory file!

**Example:**

```json
"192.168.1.2"
```

## <a name="kea_dhcp_failover_ip"></a>4. Property `Cloud Inventory > kea_dhcp_failover_ip`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Static ip for slave dhcp server. This has to match your dhcp lxc inventory file!

**Example:**

```json
"192.168.1.3"
```

## <a name="kea_dhcp_routers"></a>5. Property `Cloud Inventory > kea_dhcp_routers`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** option-data for kea dhcp routers. The default route router that the dhcp will communicate.

## <a name="kea_dhcp_pools"></a>6. Property `Cloud Inventory > kea_dhcp_pools`

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

### <a name="kea_dhcp_pools_items"></a>6.1. Cloud Inventory > kea_dhcp_pools > kea_dhcp_pools items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** IPV4 Address range in keas format.

**Example:**

```json
"192.168.1.30 - 192.168.1.254"
```

## <a name="kea_dhcp_static_routes"></a>7. Property `Cloud Inventory > kea_dhcp_static_routes`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** classless-static-routes for kea option-data. You can pass comma seperated extra routes you want the dhcp to communicate, for example to a custom VPN gateway.

**Example:**

```json
"0.0.0.0/0 - 192.168.1.1, 10.0.0.1/24 - 192.168.1.20"
```

## <a name="bind_master_ip"></a>8. Property `Cloud Inventory > bind_master_ip`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** IP of the primary bind dns for this cluster, will be statically assigned. Has to match your bind lxc inventory file!

**Example:**

```json
"192.168.1.4"
```

## <a name="bind_slave_ip"></a>9. Property `Cloud Inventory > bind_slave_ip`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** IP of the slave bind dns for this cluster. Has to match your bind lxc inventory file!

**Example:**

```json
"192.168.1.5"
```

## <a name="bind_arpa_zone_service_lxcs"></a>10. Property `Cloud Inventory > bind_arpa_zone_service_lxcs`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Arpa zone in which service lxcs with static ips will manuall get their reverse dns entries.

**Example:**

```json
"1.168.192.in-addr.arpa"
```

## <a name="bind_additional_arpa_zones"></a>11. Property `Cloud Inventory > bind_additional_arpa_zones`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of string` |
| **Required** | Yes               |

**Description:** Additional arpa zones which should be created and managed in the dns / dhcp ddns.

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                                       | Description |
| --------------------------------------------------------------------- | ----------- |
| [bind_additional_arpa_zones items](#bind_additional_arpa_zones_items) | -           |

### <a name="bind_additional_arpa_zones_items"></a>11.1. Cloud Inventory > bind_additional_arpa_zones > bind_additional_arpa_zones items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="pve_clusters"></a>12. Property `Cloud Inventory > pve_clusters`

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | Yes         |
| **Additional properties** | Not allowed |

**Description:** Definitions for specific Proxmox clusters that will be part of the cloud. Keys are hostnames.

| Property                                                                                                                                 | Pattern | Type   | Deprecated | Definition | Title/Description                           |
| ---------------------------------------------------------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ------------------------------------------- |
| - [^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)(?:\.(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?))*$](#pve_clusters_pattern1 ) | Yes     | object | No         | -          | Cloud config for specific proxmox clusters. |

### <a name="pve_clusters_pattern1"></a>12.1. Pattern Property `Cloud Inventory > pve_clusters > Cloud config for specific proxmox clusters.`
> All properties whose name matches the regular expression
```^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)(?:\.(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?))*$``` ([Test](https://regex101.com/?regex=%5E%28%3F%3A%5Ba-zA-Z0-9%5D%28%3F%3A%5Ba-zA-Z0-9-%5D%7B0%2C61%7D%5Ba-zA-Z0-9%5D%29%3F%29%28%3F%3A%5C.%28%3F%3A%5Ba-zA-Z0-9%5D%28%3F%3A%5Ba-zA-Z0-9-%5D%7B0%2C61%7D%5Ba-zA-Z0-9%5D%29%3F%29%29%2A%24))
must respect the following conditions

**Title:** Cloud config for specific proxmox clusters.

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

**Description:** This object contains configuration parameters for a proxmox cluster within a proxmox cloud.

| Property                                                                                       | Pattern | Type                      | Deprecated | Definition | Title/Description                                                                                                                                                                                                                                                                                                                                                                            |
| ---------------------------------------------------------------------------------------------- | ------- | ------------------------- | ---------- | ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| - [pve_haproxy_floating_ip_internal](#pve_clusters_pattern1_pve_haproxy_floating_ip_internal ) | No      | string                    | No         | -          | Floating ip that is exclusively accessible from inside the cloud / location. External forwardings should be made to pve_haproxy_floating_ip_external.<br />Inside the cloud if you define a certificate entry, some nodeport forward or default kubeapi access, this will all be available automatically on this ip.<br />                                                                   |
| - [pve_haproxy_floating_ip_external](#pve_clusters_pattern1_pve_haproxy_floating_ip_external ) | No      | string                    | No         | -          | Floating ip of our central cluster HAProxy.                                                                                                                                                                                                                                                                                                                                                  |
| + [pve_unique_cloud_services](#pve_clusters_pattern1_pve_unique_cloud_services )               | No      | array of enum (of string) | No         | -          | Unique service the cluster provides for its cloud. Unique in the sense that only one cluster may provide each of the services for the entire cloud.<br />Services like haproxy and backup servers can and should be provided by multiple clusters. <br />                                                                                                                                    |
| - [pve_host_vars](#pve_clusters_pattern1_pve_host_vars )                                       | No      | object                    | No         | -          | Optional variables that will be specifically set for a pve host. Key is the simple host name. <br />This can be used to build your specialized pve cluster setup playbooks. You can do things like<br />wakeonlan, driver and network configuration with these easily. Simply create your own playbook and<br />run it even before the pxc.cloud.setup_pve_clusters on this inventory.<br /> |

#### <a name="pve_clusters_pattern1_pve_haproxy_floating_ip_internal"></a>12.1.1. Property `Cloud Inventory > pve_clusters > Cloud config for specific proxmox clusters. > pve_haproxy_floating_ip_internal`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Floating ip that is exclusively accessible from inside the cloud / location. External forwardings should be made to pve_haproxy_floating_ip_external.
Inside the cloud if you define a certificate entry, some nodeport forward or default kubeapi access, this will all be available automatically on this ip.

**Example:**

```json
"192.168.10.6"
```

#### <a name="pve_clusters_pattern1_pve_haproxy_floating_ip_external"></a>12.1.2. Property `Cloud Inventory > pve_clusters > Cloud config for specific proxmox clusters. > pve_haproxy_floating_ip_external`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Floating ip of our central cluster HAProxy.

**Example:**

```json
"192.168.10.7"
```

#### <a name="pve_clusters_pattern1_pve_unique_cloud_services"></a>12.1.3. Property `Cloud Inventory > pve_clusters > Cloud config for specific proxmox clusters. > pve_unique_cloud_services`

|              |                             |
| ------------ | --------------------------- |
| **Type**     | `array of enum (of string)` |
| **Required** | Yes                         |

**Description:** Unique service the cluster provides for its cloud. Unique in the sense that only one cluster may provide each of the services for the entire cloud.
Services like haproxy and backup servers can and should be provided by multiple clusters. 

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

##### <a name="pve_clusters_pattern1_pve_unique_cloud_services_items"></a>12.1.3.1. Cloud Inventory > pve_clusters > Cloud config for specific proxmox clusters. > pve_unique_cloud_services > pve_unique_cloud_services items

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |

Must be one of:
* "dns"
* "dhcp"
* "psql-state"

#### <a name="pve_clusters_pattern1_pve_host_vars"></a>12.1.4. Property `Cloud Inventory > pve_clusters > Cloud config for specific proxmox clusters. > pve_host_vars`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Optional variables that will be specifically set for a pve host. Key is the simple host name. 
This can be used to build your specialized pve cluster setup playbooks. You can do things like
wakeonlan, driver and network configuration with these easily. Simply create your own playbook and
run it even before the pxc.cloud.setup_pve_clusters on this inventory.

| Property                                                             | Pattern | Type    | Deprecated | Definition | Title/Description                                                                                                                                                     |
| -------------------------------------------------------------------- | ------- | ------- | ---------- | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| - [disable_ipmi](#pve_clusters_pattern1_pve_host_vars_disable_ipmi ) | No      | boolean | No         | -          | If specified will disable the openipmi power managemend systemd service. This might fail on proxmox<br />hosts that dont support it and clutters up monitoring.<br /> |
| - [](#pve_clusters_pattern1_pve_host_vars_additionalProperties )     | No      | object  | No         | -          | -                                                                                                                                                                     |

##### <a name="pve_clusters_pattern1_pve_host_vars_disable_ipmi"></a>12.1.4.1. Property `Cloud Inventory > pve_clusters > Cloud config for specific proxmox clusters. > pve_host_vars > disable_ipmi`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |

**Description:** If specified will disable the openipmi power managemend systemd service. This might fail on proxmox
hosts that dont support it and clutters up monitoring.

## <a name="bind_zone_admin_email"></a>13. Property `Cloud Inventory > bind_zone_admin_email`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Required adminstrator email in bind format for bind zones.

**Example:**

```json
"admin.example.com."
```

## <a name="bind_forward_zones"></a>14. Property `Cloud Inventory > bind_forward_zones`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | No                |

**Description:** Creates zone in bind and delegation ns records to the specified nameservers. This is very useful if you have other nameservers with 
their own authoritative zones you want resolved within the cloud.

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

### <a name="bind_forward_zones_items"></a>14.1. Cloud Inventory > bind_forward_zones > bind_forward_zones items

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

| Property                                                | Pattern | Type            | Deprecated | Definition | Title/Description |
| ------------------------------------------------------- | ------- | --------------- | ---------- | ---------- | ----------------- |
| - [zone](#bind_forward_zones_items_zone )               | No      | string          | No         | -          | -                 |
| - [nameservers](#bind_forward_zones_items_nameservers ) | No      | array of string | No         | -          | -                 |

#### <a name="bind_forward_zones_items_zone"></a>14.1.1. Property `Cloud Inventory > bind_forward_zones > bind_forward_zones items > zone`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

#### <a name="bind_forward_zones_items_nameservers"></a>14.1.2. Property `Cloud Inventory > bind_forward_zones > bind_forward_zones items > nameservers`

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

##### <a name="bind_forward_zones_items_nameservers_items"></a>14.1.2.1. Cloud Inventory > bind_forward_zones > bind_forward_zones items > nameservers > nameservers items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="acme_contact"></a>15. Property `Cloud Inventory > acme_contact`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Email address to use for acme account creation.

**Example:**

```json
"acme@example.com"
```

## <a name="acme_method"></a>16. Property `Cloud Inventory > acme_method`

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |

**Description:** PVE Cloud included method for solving dns01 challenges. You need to have created the appropriate secrets under /etc/pve/cloud on your proxmox cluster.

Must be one of:
* "route53"
* "ionos"

## <a name="plugin"></a>17. Property `Cloud Inventory > plugin`

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |

**Description:** Id of ansible inventory plugin, needs to be set exactly.

Must be one of:
* "pxc.cloud.pve_cloud_inv"

----------------------------------------------------------------------------------------------------------------------------
Generated using [json-schema-for-humans](https://github.com/coveooss/json-schema-for-humans) on 2025-12-16 at 21:30:38 +0000
