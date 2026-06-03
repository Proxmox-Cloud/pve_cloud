

**Title:** Dynamic local pve cloud schema.

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

**Description:** This is the local schema file for the inventory created by `pvcli connect-cluster` and `pvcli connect-remote-cluster`

| Property                                                                                                                    | Pattern | Type   | Deprecated | Definition | Title/Description       |
| --------------------------------------------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------------- |
| - [^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)(?:\.(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?))*$](#pattern1 ) | Yes     | object | No         | -          | Inventory cloud domain. |

## <a name="pattern1"></a>100. Pattern Property `Dynamic local pve cloud schema. > Inventory cloud domain.`
> All properties whose name matches the regular expression
```^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)(?:\.(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?))*$``` ([Test](https://regex101.com/?regex=%5E%28%3F%3A%5Ba-zA-Z0-9%5D%28%3F%3A%5Ba-zA-Z0-9-%5D%7B0%2C61%7D%5Ba-zA-Z0-9%5D%29%3F%29%28%3F%3A%5C.%28%3F%3A%5Ba-zA-Z0-9%5D%28%3F%3A%5Ba-zA-Z0-9-%5D%7B0%2C61%7D%5Ba-zA-Z0-9%5D%29%3F%29%29%2A%24))
must respect the following conditions

**Title:** Inventory cloud domain.

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

**Description:** The top level keys are the cloud domains that the control node machine is connected to via the `pvcli connect...` commands.

| Property                                                                     | Pattern | Type   | Deprecated | Definition | Title/Description     |
| ---------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | --------------------- |
| - [^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)$](#pattern1_pattern4 ) | Yes     | object | No         | -          | Proxmox cluster name. |

### <a name="pattern1_pattern4"></a>100.1. Pattern Property `Dynamic local pve cloud schema. > Inventory cloud domain. > Proxmox cluster name.`
> All properties whose name matches the regular expression
```^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)$``` ([Test](https://regex101.com/?regex=%5E%28%3F%3A%5Ba-zA-Z0-9%5D%28%3F%3A%5Ba-zA-Z0-9-%5D%7B0%2C61%7D%5Ba-zA-Z0-9%5D%29%3F%29%24))
must respect the following conditions

**Title:** Proxmox cluster name.

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

**Description:** The name of the proxmox cluster (set in the proxmox ui during creation).

| Property                                               | Pattern | Type            | Deprecated | Definition | Title/Description                                                                                                  |
| ------------------------------------------------------ | ------- | --------------- | ---------- | ---------- | ------------------------------------------------------------------------------------------------------------------ |
| - [pve_jump_hosts](#pattern1_pattern4_pve_jump_hosts ) | No      | array of string | No         | -          | Optional ip list of proxmox jump hosts (they will be used cluster wide for accessing other proxmox hosts and vms). |
| + [pve_hosts](#pattern1_pattern4_pve_hosts )           | No      | object          | No         | -          | Hosts in the cluster, should be added via local ip and the --host-iface parameter in \`pvcli connect...\`          |

#### <a name="pattern1_pattern4_pve_jump_hosts"></a>100.1.1. Property `Dynamic local pve cloud schema. > Inventory cloud domain. > Proxmox cluster name. > pve_jump_hosts`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of string` |
| **Required** | No                |

**Description:** Optional ip list of proxmox jump hosts (they will be used cluster wide for accessing other proxmox hosts and vms).

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                                 | Description |
| --------------------------------------------------------------- | ----------- |
| [pve_jump_hosts items](#pattern1_pattern4_pve_jump_hosts_items) | -           |

##### <a name="pattern1_pattern4_pve_jump_hosts_items"></a>100.1.1.1. Dynamic local pve cloud schema. > Inventory cloud domain. > Proxmox cluster name. > pve_jump_hosts > pve_jump_hosts items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

#### <a name="pattern1_pattern4_pve_hosts"></a>100.1.2. Property `Dynamic local pve cloud schema. > Inventory cloud domain. > Proxmox cluster name. > pve_hosts`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | Yes              |
| **Additional properties** | Any type allowed |

**Description:** Hosts in the cluster, should be added via local ip and the --host-iface parameter in `pvcli connect...`

| Property                                                                                        | Pattern | Type   | Deprecated | Definition | Title/Description |
| ----------------------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)$](#pattern1_pattern4_pve_hosts_pattern1 ) | Yes     | object | No         | -          | Proxmox hostname  |

##### <a name="pattern1_pattern4_pve_hosts_pattern1"></a>100.1.2.1. Pattern Property `Dynamic local pve cloud schema. > Inventory cloud domain. > Proxmox cluster name. > pve_hosts > Proxmox hostname`
> All properties whose name matches the regular expression
```^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)$``` ([Test](https://regex101.com/?regex=%5E%28%3F%3A%5Ba-zA-Z0-9%5D%28%3F%3A%5Ba-zA-Z0-9-%5D%7B0%2C61%7D%5Ba-zA-Z0-9%5D%29%3F%29%24))
must respect the following conditions

**Title:** Proxmox hostname

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

| Property                                                              | Pattern | Type   | Deprecated | Definition | Title/Description                                                                                          |
| --------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ---------------------------------------------------------------------------------------------------------- |
| + [ansible_host](#pattern1_pattern4_pve_hosts_pattern1_ansible_host ) | No      | string | No         | -          | IPv4 Address of the host, should be a private ip. For remote hosts, they should be accessed via jumphosts. |
| + [ansible_user](#pattern1_pattern4_pve_hosts_pattern1_ansible_user ) | No      | string | No         | -          | Ansible user to connect to the proxmox with, proxmox uses root per default.                                |

###### <a name="pattern1_pattern4_pve_hosts_pattern1_ansible_host"></a>100.1.2.1.1. Property `Dynamic local pve cloud schema. > Inventory cloud domain. > Proxmox cluster name. > pve_hosts > Proxmox hostname > ansible_host`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** IPv4 Address of the host, should be a private ip. For remote hosts, they should be accessed via jumphosts.

###### <a name="pattern1_pattern4_pve_hosts_pattern1_ansible_user"></a>100.1.2.1.2. Property `Dynamic local pve cloud schema. > Inventory cloud domain. > Proxmox cluster name. > pve_hosts > Proxmox hostname > ansible_user`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Ansible user to connect to the proxmox with, proxmox uses root per default.

