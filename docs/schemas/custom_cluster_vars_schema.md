

**Title:** Cluster vars extension.

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

**Description:** Cluster vars extension for custom schema based on functions in validate.py and pve_cloud_inv.py dynamic inventory.

| Property                                                                 | Pattern | Type                      | Deprecated | Definition | Title/Description                                                                                                                                                                                                                                                                                                          |
| ------------------------------------------------------------------------ | ------- | ------------------------- | ---------- | ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| + [pve_vm_subnet](#pve_vm_subnet )                                       | No      | string                    | No         | -          | Subnet this PVE cluster uses for its VMs.                                                                                                                                                                                                                                                                                  |
| + [pve_cloud_domain](#pve_cloud_domain )                                 | No      | string                    | No         | -          | The overarching domain for the cloud. Will also be used for ddns.                                                                                                                                                                                                                                                          |
| + [kea_dhcp_main_ip](#kea_dhcp_main_ip )                                 | No      | string                    | No         | -          | Static assigned ip for the main dhcp server. This has to match your dhcp lxc inventory file!                                                                                                                                                                                                                               |
| + [kea_dhcp_failover_ip](#kea_dhcp_failover_ip )                         | No      | string                    | No         | -          | Static ip for slave dhcp server. This has to match your dhcp lxc inventory file!                                                                                                                                                                                                                                           |
| + [kea_dhcp_routers](#kea_dhcp_routers )                                 | No      | string                    | No         | -          | option-data for kea dhcp routers. The default route router that the dhcp will communicate.                                                                                                                                                                                                                                 |
| + [kea_dhcp_pools](#kea_dhcp_pools )                                     | No      | array of string           | No         | -          | Address pools that the dhcp allocates from. Has to be within pve_vm_subnet cidr.                                                                                                                                                                                                                                           |
| + [kea_dhcp_static_routes](#kea_dhcp_static_routes )                     | No      | string                    | No         | -          | classless-static-routes for kea option-data. You can pass comma seperated extra routes you want the dhcp to communicate, for example to a custom VPN gateway.<br />                                                                                                                                                        |
| + [bind_master_ip](#bind_master_ip )                                     | No      | string                    | No         | -          | IP of the primary bind dns for this cluster, will be statically assigned. Has to match your bind lxc inventory file!                                                                                                                                                                                                       |
| + [bind_slave_ip](#bind_slave_ip )                                       | No      | string                    | No         | -          | IP of the slave bind dns for this cluster. Has to match your bind lxc inventory file!                                                                                                                                                                                                                                      |
| + [bind_arpa_zone_service_lxcs](#bind_arpa_zone_service_lxcs )           | No      | string                    | No         | -          | Arpa zone in which service lxcs with static ips will manuall get their reverse dns entries.                                                                                                                                                                                                                                |
| + [bind_additional_arpa_zones](#bind_additional_arpa_zones )             | No      | array of string           | No         | -          | Additional arpa zones which should be created and managed in the dns / dhcp ddns.                                                                                                                                                                                                                                          |
| + [pve_clusters](#pve_clusters )                                         | No      | object                    | No         | -          | Definitions for specific Proxmox clusters that will be part of the cloud. Keys are hostnames.                                                                                                                                                                                                                              |
| + [bind_zone_admin_email](#bind_zone_admin_email )                       | No      | string                    | No         | -          | Required adminstrator email in bind format for bind zones.                                                                                                                                                                                                                                                                 |
| - [bind_forward_zones](#bind_forward_zones )                             | No      | array of object           | No         | -          | Allows forwarding of specific zones to specific nameservers. This is useful for domains that are not owned by this cloud. For delegating sub zones <br />resort to the terraform dns provider alongside the kubernetes cluster that declares the parent zone in its inventory file.<br />                                  |
| - [acme_contact](#acme_contact )                                         | No      | string                    | No         | -          | Email address to use for acme account creation.                                                                                                                                                                                                                                                                            |
| - [acme_method](#acme_method )                                           | No      | enum (of string)          | No         | -          | PVE Cloud included method for solving dns01 challenges. You need to have created the appropriate cloud secrets created.<br />                                                                                                                                                                                              |
| - [plugin](#plugin )                                                     | No      | enum (of string)          | No         | -          | Id of ansible inventory plugin, needs to be set exactly.                                                                                                                                                                                                                                                                   |
| - [pve_haproxy_floating_ip_internal](#pve_haproxy_floating_ip_internal ) | No      | string                    | No         | -          | Floating ip that is exclusively accessible from inside the cloud / location. External forwardings should be made to pve_haproxy_floating_ip_external.<br />Inside the cloud if you define a certificate entry, some nodeport forward or default kubeapi access, this will all be available automatically on this ip.<br /> |
| - [pve_haproxy_floating_ip_external](#pve_haproxy_floating_ip_external ) | No      | string                    | No         | -          | Floating ip of our central cluster HAProxy.                                                                                                                                                                                                                                                                                |
| - [pve_unique_cloud_services](#pve_unique_cloud_services )               | No      | array of enum (of string) | No         | -          | Unique service the cluster provides for its cloud. Unique in the sense that only one cluster may provide each of the services for the entire cloud.<br />Services like haproxy and backup servers can and should be provided by multiple clusters. <br />                                                                  |
| - [pve_host_vars](#pve_host_vars )                                       | No      | object                    | No         | -          | Optional variables that will be specifically set for a pve host. Key is the simple host name.<br />                                                                                                                                                                                                                        |
| + [pve_cloud_collection_version](#pve_cloud_collection_version )         | No      | string                    | No         | -          | Dynamic property set by pve_cloud_inv for validation of the collections version.                                                                                                                                                                                                                                           |
| + [py_pve_cloud_version](#py_pve_cloud_version )                         | No      | string                    | No         | -          | Dynamic property for validation of the core python pve cloud library in use.                                                                                                                                                                                                                                               |
| + [pve_cluster_name](#pve_cluster_name )                                 | No      | string                    | No         | -          | Self reference of the cluster name for convinient access.                                                                                                                                                                                                                                                                  |

## <a name="pve_vm_subnet"></a>109. Property `Cluster vars extension. > pve_vm_subnet`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Subnet this PVE cluster uses for its VMs.

**Example:**

```json
"192.168.10.0/24"
```

## <a name="pve_cloud_domain"></a>110. Property `Cluster vars extension. > pve_cloud_domain`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** The overarching domain for the cloud. Will also be used for ddns.

**Example:**

```json
"your-cloud.example.com"
```

## <a name="kea_dhcp_main_ip"></a>111. Property `Cluster vars extension. > kea_dhcp_main_ip`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Static assigned ip for the main dhcp server. This has to match your dhcp lxc inventory file!

**Example:**

```json
"192.168.1.2"
```

## <a name="kea_dhcp_failover_ip"></a>112. Property `Cluster vars extension. > kea_dhcp_failover_ip`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Static ip for slave dhcp server. This has to match your dhcp lxc inventory file!

**Example:**

```json
"192.168.1.3"
```

## <a name="kea_dhcp_routers"></a>113. Property `Cluster vars extension. > kea_dhcp_routers`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** option-data for kea dhcp routers. The default route router that the dhcp will communicate.

## <a name="kea_dhcp_pools"></a>114. Property `Cluster vars extension. > kea_dhcp_pools`

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

### <a name="kea_dhcp_pools_items"></a>114.1. Cluster vars extension. > kea_dhcp_pools > kea_dhcp_pools items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** IPV4 Address range in keas format.

**Example:**

```json
"192.168.1.30 - 192.168.1.254"
```

## <a name="kea_dhcp_static_routes"></a>115. Property `Cluster vars extension. > kea_dhcp_static_routes`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** classless-static-routes for kea option-data. You can pass comma seperated extra routes you want the dhcp to communicate, for example to a custom VPN gateway.

**Example:**

```json
"0.0.0.0/0 - 192.168.1.1, 10.0.0.1/24 - 192.168.1.20"
```

## <a name="bind_master_ip"></a>116. Property `Cluster vars extension. > bind_master_ip`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** IP of the primary bind dns for this cluster, will be statically assigned. Has to match your bind lxc inventory file!

**Example:**

```json
"192.168.1.4"
```

## <a name="bind_slave_ip"></a>117. Property `Cluster vars extension. > bind_slave_ip`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** IP of the slave bind dns for this cluster. Has to match your bind lxc inventory file!

**Example:**

```json
"192.168.1.5"
```

## <a name="bind_arpa_zone_service_lxcs"></a>118. Property `Cluster vars extension. > bind_arpa_zone_service_lxcs`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Arpa zone in which service lxcs with static ips will manuall get their reverse dns entries.

**Example:**

```json
"1.168.192.in-addr.arpa"
```

## <a name="bind_additional_arpa_zones"></a>119. Property `Cluster vars extension. > bind_additional_arpa_zones`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of string` |
| **Required** | Yes               |

**Description:** Additional arpa zones which should be created and managed in the dns / dhcp ddns.

**Examples:**

```json
"2.168.192.in-addr.arpa"
```

```json
"3.168.192.in-addr.arpa"
```

```json
"0.10-in-addr.arpa"
```

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

### <a name="bind_additional_arpa_zones_items"></a>119.1. Cluster vars extension. > bind_additional_arpa_zones > bind_additional_arpa_zones items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="pve_clusters"></a>120. Property `Cluster vars extension. > pve_clusters`

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | Yes         |
| **Additional properties** | Not allowed |

**Description:** Definitions for specific Proxmox clusters that will be part of the cloud. Keys are hostnames.

| Property                                                                                                                                 | Pattern | Type   | Deprecated | Definition | Title/Description                           |
| ---------------------------------------------------------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ------------------------------------------- |
| - [^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)(?:\.(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?))*$](#pve_clusters_pattern1 ) | Yes     | object | No         | -          | Cloud config for specific proxmox clusters. |

### <a name="pve_clusters_pattern1"></a>120.1. Pattern Property `Cluster vars extension. > pve_clusters > Cloud config for specific proxmox clusters.`
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

| Property                                                                                       | Pattern | Type                      | Deprecated | Definition | Title/Description                                                                                                                                                                                                                                                                                                          |
| ---------------------------------------------------------------------------------------------- | ------- | ------------------------- | ---------- | ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| - [pve_haproxy_floating_ip_internal](#pve_clusters_pattern1_pve_haproxy_floating_ip_internal ) | No      | string                    | No         | -          | Floating ip that is exclusively accessible from inside the cloud / location. External forwardings should be made to pve_haproxy_floating_ip_external.<br />Inside the cloud if you define a certificate entry, some nodeport forward or default kubeapi access, this will all be available automatically on this ip.<br /> |
| - [pve_haproxy_floating_ip_external](#pve_clusters_pattern1_pve_haproxy_floating_ip_external ) | No      | string                    | No         | -          | Floating ip of our central cluster HAProxy.                                                                                                                                                                                                                                                                                |
| + [pve_unique_cloud_services](#pve_clusters_pattern1_pve_unique_cloud_services )               | No      | array of enum (of string) | No         | -          | Unique service the cluster provides for its cloud. Unique in the sense that only one cluster may provide each of the services for the entire cloud.<br />Services like haproxy and backup servers can and should be provided by multiple clusters. <br />                                                                  |
| - [pve_host_vars](#pve_clusters_pattern1_pve_host_vars )                                       | No      | object                    | No         | -          | Optional variables that will be specifically set for a pve host. Key is the simple host name.<br />                                                                                                                                                                                                                        |

#### <a name="pve_clusters_pattern1_pve_haproxy_floating_ip_internal"></a>120.1.1. Property `Cluster vars extension. > pve_clusters > Cloud config for specific proxmox clusters. > pve_haproxy_floating_ip_internal`

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

#### <a name="pve_clusters_pattern1_pve_haproxy_floating_ip_external"></a>120.1.2. Property `Cluster vars extension. > pve_clusters > Cloud config for specific proxmox clusters. > pve_haproxy_floating_ip_external`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Floating ip of our central cluster HAProxy.

**Example:**

```json
"192.168.10.7"
```

#### <a name="pve_clusters_pattern1_pve_unique_cloud_services"></a>120.1.3. Property `Cluster vars extension. > pve_clusters > Cloud config for specific proxmox clusters. > pve_unique_cloud_services`

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

##### <a name="pve_clusters_pattern1_pve_unique_cloud_services_items"></a>120.1.3.1. Cluster vars extension. > pve_clusters > Cloud config for specific proxmox clusters. > pve_unique_cloud_services > pve_unique_cloud_services items

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |

Must be one of:

* "dns"
* "dhcp"
* "psql-state"

#### <a name="pve_clusters_pattern1_pve_host_vars"></a>120.1.4. Property `Cluster vars extension. > pve_clusters > Cloud config for specific proxmox clusters. > pve_host_vars`

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

**Description:** Optional variables that will be specifically set for a pve host. Key is the simple host name.

| Property                                                                                                | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)$](#pve_clusters_pattern1_pve_host_vars_pattern1 ) | Yes     | object | No         | -          | Proxmox hostname  |

##### <a name="pve_clusters_pattern1_pve_host_vars_pattern1"></a>120.1.4.1. Pattern Property `Cluster vars extension. > pve_clusters > Cloud config for specific proxmox clusters. > pve_host_vars > Proxmox hostname`
> All properties whose name matches the regular expression
```^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)$``` ([Test](https://regex101.com/?regex=%5E%28%3F%3A%5Ba-zA-Z0-9%5D%28%3F%3A%5Ba-zA-Z0-9-%5D%7B0%2C61%7D%5Ba-zA-Z0-9%5D%29%3F%29%24))
must respect the following conditions

**Title:** Proxmox hostname

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

| Property                                                                                                              | Pattern | Type            | Deprecated | Definition | Title/Description                                                                                                                                                                                                                                                                                                                                                                        |
| --------------------------------------------------------------------------------------------------------------------- | ------- | --------------- | ---------- | ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| - [pve_corosync_vote](#pve_clusters_pattern1_pve_host_vars_pattern1_pve_corosync_vote )                               | No      | boolean         | No         | -          | Set this to false to remove the corosync vote of this proxmox host, this ideal for hosts<br />that get booted up conditionally. Defaults to true.<br />                                                                                                                                                                                                                                  |
| - [install_btrfs_root_prom_exporter](#pve_clusters_pattern1_pve_host_vars_pattern1_install_btrfs_root_prom_exporter ) | No      | boolean         | No         | -          | Set this to true if you installed the os on btrfs. This will install a prometheus exporter for btrfs aswell as enable degraded booting.<br />                                                                                                                                                                                                                                            |
| - [install_log2ram](#pve_clusters_pattern1_pve_host_vars_pattern1_install_log2ram )                                   | No      | boolean         | No         | -          | This will install log2ram, moving logs to ram. If you are using the same disks for the os aswell as virtual machines, you should enable it,<br />to ensure proxmox doesnt freeze up because of vm disk usage.<br />                                                                                                                                                                      |
| - [disable_ipmi](#pve_clusters_pattern1_pve_host_vars_pattern1_disable_ipmi )                                         | No      | boolean         | No         | -          | If specified will disable the openipmi power managemend systemd service. This might fail on proxmox<br />hosts that dont support it and clutters up monitoring.<br />                                                                                                                                                                                                                    |
| - [zfs_scan_error_as_warn](#pve_clusters_pattern1_pve_host_vars_pattern1_zfs_scan_error_as_warn )                     | No      | boolean         | No         | -          | If specified will set SuccessExitStatus=1 for zfs-import-scan systemd service. When using zfs localpv passthrough of disks for openebs,<br />this scan service will continually fail because it tries to scan and import the disk owned by the kubernetes vm. zpool import (slop machine output)<br />does not crash / stop on failing to import a device but will continue going.<br /> |
| - [wol](#pve_clusters_pattern1_pve_host_vars_pattern1_wol )                                                           | No      | object          | No         | -          | Definition for wakeonlan network interface. Will use ethtool and post-up commands to keep it enabled on the nic.<br />You also might have to adjust settings in the bios, enable WoL there and also tune the power options for receiving the<br />magic package. Turn off settings like low power soft off, then you can use \`wakeonlan MAC_ADDR\` to boot your host.<br />             |
| - [net_offloading_fixxes](#pve_clusters_pattern1_pve_host_vars_pattern1_net_offloading_fixxes )                       | No      | array of object | No         | -          | Disable pesky network offloaing features that break upon virtualization.                                                                                                                                                                                                                                                                                                                 |

###### <a name="pve_clusters_pattern1_pve_host_vars_pattern1_pve_corosync_vote"></a>120.1.4.1.1. Property `Cluster vars extension. > pve_clusters > Cloud config for specific proxmox clusters. > pve_host_vars > Proxmox hostname > pve_corosync_vote`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |

**Description:** Set this to false to remove the corosync vote of this proxmox host, this ideal for hosts
that get booted up conditionally. Defaults to true.

###### <a name="pve_clusters_pattern1_pve_host_vars_pattern1_install_btrfs_root_prom_exporter"></a>120.1.4.1.2. Property `Cluster vars extension. > pve_clusters > Cloud config for specific proxmox clusters. > pve_host_vars > Proxmox hostname > install_btrfs_root_prom_exporter`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |

**Description:** Set this to true if you installed the os on btrfs. This will install a prometheus exporter for btrfs aswell as enable degraded booting.

###### <a name="pve_clusters_pattern1_pve_host_vars_pattern1_install_log2ram"></a>120.1.4.1.3. Property `Cluster vars extension. > pve_clusters > Cloud config for specific proxmox clusters. > pve_host_vars > Proxmox hostname > install_log2ram`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |

**Description:** This will install log2ram, moving logs to ram. If you are using the same disks for the os aswell as virtual machines, you should enable it,
to ensure proxmox doesnt freeze up because of vm disk usage.

###### <a name="pve_clusters_pattern1_pve_host_vars_pattern1_disable_ipmi"></a>120.1.4.1.4. Property `Cluster vars extension. > pve_clusters > Cloud config for specific proxmox clusters. > pve_host_vars > Proxmox hostname > disable_ipmi`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |

**Description:** If specified will disable the openipmi power managemend systemd service. This might fail on proxmox
hosts that dont support it and clutters up monitoring.

###### <a name="pve_clusters_pattern1_pve_host_vars_pattern1_zfs_scan_error_as_warn"></a>120.1.4.1.5. Property `Cluster vars extension. > pve_clusters > Cloud config for specific proxmox clusters. > pve_host_vars > Proxmox hostname > zfs_scan_error_as_warn`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |

**Description:** If specified will set SuccessExitStatus=1 for zfs-import-scan systemd service. When using zfs localpv passthrough of disks for openebs,
this scan service will continually fail because it tries to scan and import the disk owned by the kubernetes vm. zpool import (slop machine output)
does not crash / stop on failing to import a device but will continue going.

###### <a name="pve_clusters_pattern1_pve_host_vars_pattern1_wol"></a>120.1.4.1.6. Property `Cluster vars extension. > pve_clusters > Cloud config for specific proxmox clusters. > pve_host_vars > Proxmox hostname > wol`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Definition for wakeonlan network interface. Will use ethtool and post-up commands to keep it enabled on the nic.
You also might have to adjust settings in the bios, enable WoL there and also tune the power options for receiving the
magic package. Turn off settings like low power soft off, then you can use `wakeonlan MAC_ADDR` to boot your host.

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description                                      |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ------------------------------------------------------ |
| - [iface](#pve_clusters_pattern1_pve_host_vars_pattern1_wol_iface )   | No      | string | No         | -          | The interface for which wakeonlan should be activated. |
| - [bridge](#pve_clusters_pattern1_pve_host_vars_pattern1_wol_bridge ) | No      | string | No         | -          | The bridge that gets the post-up definition for wol.   |

###### <a name="pve_clusters_pattern1_pve_host_vars_pattern1_wol_iface"></a>120.1.4.1.6.1. Property `Cluster vars extension. > pve_clusters > Cloud config for specific proxmox clusters. > pve_host_vars > Proxmox hostname > wol > iface`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** The interface for which wakeonlan should be activated.

###### <a name="pve_clusters_pattern1_pve_host_vars_pattern1_wol_bridge"></a>120.1.4.1.6.2. Property `Cluster vars extension. > pve_clusters > Cloud config for specific proxmox clusters. > pve_host_vars > Proxmox hostname > wol > bridge`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** The bridge that gets the post-up definition for wol.

###### <a name="pve_clusters_pattern1_pve_host_vars_pattern1_net_offloading_fixxes"></a>120.1.4.1.7. Property `Cluster vars extension. > pve_clusters > Cloud config for specific proxmox clusters. > pve_host_vars > Proxmox hostname > net_offloading_fixxes`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | No                |

**Description:** Disable pesky network offloaing features that break upon virtualization.

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                                                                          | Description |
| -------------------------------------------------------------------------------------------------------- | ----------- |
| [net_offloading_fixxes items](#pve_clusters_pattern1_pve_host_vars_pattern1_net_offloading_fixxes_items) | -           |

###### <a name="pve_clusters_pattern1_pve_host_vars_pattern1_net_offloading_fixxes_items"></a>120.1.4.1.7.1. Cluster vars extension. > pve_clusters > Cloud config for specific proxmox clusters. > pve_host_vars > Proxmox hostname > net_offloading_fixxes > net_offloading_fixxes items

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

| Property                                                                                                          | Pattern | Type            | Deprecated | Definition | Title/Description                                                                                         |
| ----------------------------------------------------------------------------------------------------------------- | ------- | --------------- | ---------- | ---------- | --------------------------------------------------------------------------------------------------------- |
| - [iface](#pve_clusters_pattern1_pve_host_vars_pattern1_net_offloading_fixxes_items_iface )                       | No      | string          | No         | -          | The interface for which to disable specified network offloading features.                                 |
| - [bridge](#pve_clusters_pattern1_pve_host_vars_pattern1_net_offloading_fixxes_items_bridge )                     | No      | string          | No         | -          | The bridge that gets the post-up definition for applying the fix that will receive the post-up directive. |
| - [disable_features](#pve_clusters_pattern1_pve_host_vars_pattern1_net_offloading_fixxes_items_disable_features ) | No      | array of string | No         | -          | List of network features to disable for the interface.                                                    |

###### <a name="pve_clusters_pattern1_pve_host_vars_pattern1_net_offloading_fixxes_items_iface"></a>120.1.4.1.7.1.1. Property `Cluster vars extension. > pve_clusters > Cloud config for specific proxmox clusters. > pve_host_vars > Proxmox hostname > net_offloading_fixxes > net_offloading_fixxes items > iface`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** The interface for which to disable specified network offloading features.

###### <a name="pve_clusters_pattern1_pve_host_vars_pattern1_net_offloading_fixxes_items_bridge"></a>120.1.4.1.7.1.2. Property `Cluster vars extension. > pve_clusters > Cloud config for specific proxmox clusters. > pve_host_vars > Proxmox hostname > net_offloading_fixxes > net_offloading_fixxes items > bridge`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** The bridge that gets the post-up definition for applying the fix that will receive the post-up directive.

###### <a name="pve_clusters_pattern1_pve_host_vars_pattern1_net_offloading_fixxes_items_disable_features"></a>120.1.4.1.7.1.3. Property `Cluster vars extension. > pve_clusters > Cloud config for specific proxmox clusters. > pve_host_vars > Proxmox hostname > net_offloading_fixxes > net_offloading_fixxes items > disable_features`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of string` |
| **Required** | No                |

**Description:** List of network features to disable for the interface.

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                                                                                            | Description |
| -------------------------------------------------------------------------------------------------------------------------- | ----------- |
| [disable_features items](#pve_clusters_pattern1_pve_host_vars_pattern1_net_offloading_fixxes_items_disable_features_items) | -           |

###### <a name="pve_clusters_pattern1_pve_host_vars_pattern1_net_offloading_fixxes_items_disable_features_items"></a>120.1.4.1.7.1.3.1. Cluster vars extension. > pve_clusters > Cloud config for specific proxmox clusters. > pve_host_vars > Proxmox hostname > net_offloading_fixxes > net_offloading_fixxes items > disable_features > disable_features items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Examples:**

```json
"tso"
```

```json
"gso"
```

```json
"gro"
```

## <a name="bind_zone_admin_email"></a>121. Property `Cluster vars extension. > bind_zone_admin_email`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Required adminstrator email in bind format for bind zones.

**Example:**

```json
"admin.example.com."
```

## <a name="bind_forward_zones"></a>122. Property `Cluster vars extension. > bind_forward_zones`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | No                |

**Description:** Allows forwarding of specific zones to specific nameservers. This is useful for domains that are not owned by this cloud. For delegating sub zones 
resort to the terraform dns provider alongside the kubernetes cluster that declares the parent zone in its inventory file.

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

### <a name="bind_forward_zones_items"></a>122.1. Cluster vars extension. > bind_forward_zones > bind_forward_zones items

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

| Property                                                | Pattern | Type            | Deprecated | Definition | Title/Description |
| ------------------------------------------------------- | ------- | --------------- | ---------- | ---------- | ----------------- |
| - [zone](#bind_forward_zones_items_zone )               | No      | string          | No         | -          | -                 |
| - [nameservers](#bind_forward_zones_items_nameservers ) | No      | array of string | No         | -          | -                 |

#### <a name="bind_forward_zones_items_zone"></a>122.1.1. Property `Cluster vars extension. > bind_forward_zones > bind_forward_zones items > zone`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

#### <a name="bind_forward_zones_items_nameservers"></a>122.1.2. Property `Cluster vars extension. > bind_forward_zones > bind_forward_zones items > nameservers`

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

##### <a name="bind_forward_zones_items_nameservers_items"></a>122.1.2.1. Cluster vars extension. > bind_forward_zones > bind_forward_zones items > nameservers > nameservers items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="acme_contact"></a>123. Property `Cluster vars extension. > acme_contact`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Email address to use for acme account creation.

**Example:**

```json
"acme@example.com"
```

## <a name="acme_method"></a>124. Property `Cluster vars extension. > acme_method`

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |

**Description:** PVE Cloud included method for solving dns01 challenges. You need to have created the appropriate cloud secrets created.

Must be one of:

* "route53"
* "ionos"
* "ionos_cloud"

## <a name="plugin"></a>125. Property `Cluster vars extension. > plugin`

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |

**Description:** Id of ansible inventory plugin, needs to be set exactly.

Must be one of:

* "pxc.cloud.pve_cloud_inv"

## <a name="pve_haproxy_floating_ip_internal"></a>126. Property `Cluster vars extension. > pve_haproxy_floating_ip_internal`

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

## <a name="pve_haproxy_floating_ip_external"></a>127. Property `Cluster vars extension. > pve_haproxy_floating_ip_external`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Floating ip of our central cluster HAProxy.

**Example:**

```json
"192.168.10.7"
```

## <a name="pve_unique_cloud_services"></a>128. Property `Cluster vars extension. > pve_unique_cloud_services`

|              |                             |
| ------------ | --------------------------- |
| **Type**     | `array of enum (of string)` |
| **Required** | No                          |

**Description:** Unique service the cluster provides for its cloud. Unique in the sense that only one cluster may provide each of the services for the entire cloud.
Services like haproxy and backup servers can and should be provided by multiple clusters. 

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                                     | Description |
| ------------------------------------------------------------------- | ----------- |
| [pve_unique_cloud_services items](#pve_unique_cloud_services_items) | -           |

### <a name="pve_unique_cloud_services_items"></a>128.1. Cluster vars extension. > pve_unique_cloud_services > pve_unique_cloud_services items

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |

Must be one of:

* "dns"
* "dhcp"
* "psql-state"

## <a name="pve_host_vars"></a>129. Property `Cluster vars extension. > pve_host_vars`

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

**Description:** Optional variables that will be specifically set for a pve host. Key is the simple host name.

| Property                                                                          | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)$](#pve_host_vars_pattern1 ) | Yes     | object | No         | -          | Proxmox hostname  |

### <a name="pve_host_vars_pattern1"></a>129.1. Pattern Property `Cluster vars extension. > pve_host_vars > Proxmox hostname`
> All properties whose name matches the regular expression
```^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)$``` ([Test](https://regex101.com/?regex=%5E%28%3F%3A%5Ba-zA-Z0-9%5D%28%3F%3A%5Ba-zA-Z0-9-%5D%7B0%2C61%7D%5Ba-zA-Z0-9%5D%29%3F%29%24))
must respect the following conditions

**Title:** Proxmox hostname

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

| Property                                                                                        | Pattern | Type            | Deprecated | Definition | Title/Description                                                                                                                                                                                                                                                                                                                                                                        |
| ----------------------------------------------------------------------------------------------- | ------- | --------------- | ---------- | ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| - [pve_corosync_vote](#pve_host_vars_pattern1_pve_corosync_vote )                               | No      | boolean         | No         | -          | Set this to false to remove the corosync vote of this proxmox host, this ideal for hosts<br />that get booted up conditionally. Defaults to true.<br />                                                                                                                                                                                                                                  |
| - [install_btrfs_root_prom_exporter](#pve_host_vars_pattern1_install_btrfs_root_prom_exporter ) | No      | boolean         | No         | -          | Set this to true if you installed the os on btrfs. This will install a prometheus exporter for btrfs aswell as enable degraded booting.<br />                                                                                                                                                                                                                                            |
| - [install_log2ram](#pve_host_vars_pattern1_install_log2ram )                                   | No      | boolean         | No         | -          | This will install log2ram, moving logs to ram. If you are using the same disks for the os aswell as virtual machines, you should enable it,<br />to ensure proxmox doesnt freeze up because of vm disk usage.<br />                                                                                                                                                                      |
| - [disable_ipmi](#pve_host_vars_pattern1_disable_ipmi )                                         | No      | boolean         | No         | -          | If specified will disable the openipmi power managemend systemd service. This might fail on proxmox<br />hosts that dont support it and clutters up monitoring.<br />                                                                                                                                                                                                                    |
| - [zfs_scan_error_as_warn](#pve_host_vars_pattern1_zfs_scan_error_as_warn )                     | No      | boolean         | No         | -          | If specified will set SuccessExitStatus=1 for zfs-import-scan systemd service. When using zfs localpv passthrough of disks for openebs,<br />this scan service will continually fail because it tries to scan and import the disk owned by the kubernetes vm. zpool import (slop machine output)<br />does not crash / stop on failing to import a device but will continue going.<br /> |
| - [wol](#pve_host_vars_pattern1_wol )                                                           | No      | object          | No         | -          | Definition for wakeonlan network interface. Will use ethtool and post-up commands to keep it enabled on the nic.<br />You also might have to adjust settings in the bios, enable WoL there and also tune the power options for receiving the<br />magic package. Turn off settings like low power soft off, then you can use \`wakeonlan MAC_ADDR\` to boot your host.<br />             |
| - [net_offloading_fixxes](#pve_host_vars_pattern1_net_offloading_fixxes )                       | No      | array of object | No         | -          | Disable pesky network offloaing features that break upon virtualization.                                                                                                                                                                                                                                                                                                                 |

#### <a name="pve_host_vars_pattern1_pve_corosync_vote"></a>129.1.1. Property `Cluster vars extension. > pve_host_vars > Proxmox hostname > pve_corosync_vote`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |

**Description:** Set this to false to remove the corosync vote of this proxmox host, this ideal for hosts
that get booted up conditionally. Defaults to true.

#### <a name="pve_host_vars_pattern1_install_btrfs_root_prom_exporter"></a>129.1.2. Property `Cluster vars extension. > pve_host_vars > Proxmox hostname > install_btrfs_root_prom_exporter`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |

**Description:** Set this to true if you installed the os on btrfs. This will install a prometheus exporter for btrfs aswell as enable degraded booting.

#### <a name="pve_host_vars_pattern1_install_log2ram"></a>129.1.3. Property `Cluster vars extension. > pve_host_vars > Proxmox hostname > install_log2ram`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |

**Description:** This will install log2ram, moving logs to ram. If you are using the same disks for the os aswell as virtual machines, you should enable it,
to ensure proxmox doesnt freeze up because of vm disk usage.

#### <a name="pve_host_vars_pattern1_disable_ipmi"></a>129.1.4. Property `Cluster vars extension. > pve_host_vars > Proxmox hostname > disable_ipmi`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |

**Description:** If specified will disable the openipmi power managemend systemd service. This might fail on proxmox
hosts that dont support it and clutters up monitoring.

#### <a name="pve_host_vars_pattern1_zfs_scan_error_as_warn"></a>129.1.5. Property `Cluster vars extension. > pve_host_vars > Proxmox hostname > zfs_scan_error_as_warn`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |

**Description:** If specified will set SuccessExitStatus=1 for zfs-import-scan systemd service. When using zfs localpv passthrough of disks for openebs,
this scan service will continually fail because it tries to scan and import the disk owned by the kubernetes vm. zpool import (slop machine output)
does not crash / stop on failing to import a device but will continue going.

#### <a name="pve_host_vars_pattern1_wol"></a>129.1.6. Property `Cluster vars extension. > pve_host_vars > Proxmox hostname > wol`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Definition for wakeonlan network interface. Will use ethtool and post-up commands to keep it enabled on the nic.
You also might have to adjust settings in the bios, enable WoL there and also tune the power options for receiving the
magic package. Turn off settings like low power soft off, then you can use `wakeonlan MAC_ADDR` to boot your host.

| Property                                        | Pattern | Type   | Deprecated | Definition | Title/Description                                      |
| ----------------------------------------------- | ------- | ------ | ---------- | ---------- | ------------------------------------------------------ |
| - [iface](#pve_host_vars_pattern1_wol_iface )   | No      | string | No         | -          | The interface for which wakeonlan should be activated. |
| - [bridge](#pve_host_vars_pattern1_wol_bridge ) | No      | string | No         | -          | The bridge that gets the post-up definition for wol.   |

##### <a name="pve_host_vars_pattern1_wol_iface"></a>129.1.6.1. Property `Cluster vars extension. > pve_host_vars > Proxmox hostname > wol > iface`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** The interface for which wakeonlan should be activated.

##### <a name="pve_host_vars_pattern1_wol_bridge"></a>129.1.6.2. Property `Cluster vars extension. > pve_host_vars > Proxmox hostname > wol > bridge`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** The bridge that gets the post-up definition for wol.

#### <a name="pve_host_vars_pattern1_net_offloading_fixxes"></a>129.1.7. Property `Cluster vars extension. > pve_host_vars > Proxmox hostname > net_offloading_fixxes`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | No                |

**Description:** Disable pesky network offloaing features that break upon virtualization.

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                                                    | Description |
| ---------------------------------------------------------------------------------- | ----------- |
| [net_offloading_fixxes items](#pve_host_vars_pattern1_net_offloading_fixxes_items) | -           |

##### <a name="pve_host_vars_pattern1_net_offloading_fixxes_items"></a>129.1.7.1. Cluster vars extension. > pve_host_vars > Proxmox hostname > net_offloading_fixxes > net_offloading_fixxes items

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

| Property                                                                                    | Pattern | Type            | Deprecated | Definition | Title/Description                                                                                         |
| ------------------------------------------------------------------------------------------- | ------- | --------------- | ---------- | ---------- | --------------------------------------------------------------------------------------------------------- |
| - [iface](#pve_host_vars_pattern1_net_offloading_fixxes_items_iface )                       | No      | string          | No         | -          | The interface for which to disable specified network offloading features.                                 |
| - [bridge](#pve_host_vars_pattern1_net_offloading_fixxes_items_bridge )                     | No      | string          | No         | -          | The bridge that gets the post-up definition for applying the fix that will receive the post-up directive. |
| - [disable_features](#pve_host_vars_pattern1_net_offloading_fixxes_items_disable_features ) | No      | array of string | No         | -          | List of network features to disable for the interface.                                                    |

###### <a name="pve_host_vars_pattern1_net_offloading_fixxes_items_iface"></a>129.1.7.1.1. Property `Cluster vars extension. > pve_host_vars > Proxmox hostname > net_offloading_fixxes > net_offloading_fixxes items > iface`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** The interface for which to disable specified network offloading features.

###### <a name="pve_host_vars_pattern1_net_offloading_fixxes_items_bridge"></a>129.1.7.1.2. Property `Cluster vars extension. > pve_host_vars > Proxmox hostname > net_offloading_fixxes > net_offloading_fixxes items > bridge`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** The bridge that gets the post-up definition for applying the fix that will receive the post-up directive.

###### <a name="pve_host_vars_pattern1_net_offloading_fixxes_items_disable_features"></a>129.1.7.1.3. Property `Cluster vars extension. > pve_host_vars > Proxmox hostname > net_offloading_fixxes > net_offloading_fixxes items > disable_features`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of string` |
| **Required** | No                |

**Description:** List of network features to disable for the interface.

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                                                                      | Description |
| ---------------------------------------------------------------------------------------------------- | ----------- |
| [disable_features items](#pve_host_vars_pattern1_net_offloading_fixxes_items_disable_features_items) | -           |

###### <a name="pve_host_vars_pattern1_net_offloading_fixxes_items_disable_features_items"></a>129.1.7.1.3.1. Cluster vars extension. > pve_host_vars > Proxmox hostname > net_offloading_fixxes > net_offloading_fixxes items > disable_features > disable_features items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Examples:**

```json
"tso"
```

```json
"gso"
```

```json
"gro"
```

## <a name="pve_cloud_collection_version"></a>130. Property `Cluster vars extension. > pve_cloud_collection_version`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Dynamic property set by pve_cloud_inv for validation of the collections version.

## <a name="py_pve_cloud_version"></a>131. Property `Cluster vars extension. > py_pve_cloud_version`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Dynamic property for validation of the core python pve cloud library in use.

## <a name="pve_cluster_name"></a>132. Property `Cluster vars extension. > pve_cluster_name`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Self reference of the cluster name for convinient access.

