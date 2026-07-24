

**Title:** External Hosts Inventory

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

**Description:** Generic inventory file for accessing external, non proxmox cloud hosts in a proxmox cloud context.

| Property                                 | Pattern | Type             | Deprecated | Definition | Title/Description                                                      |
| ---------------------------------------- | ------- | ---------------- | ---------- | ---------- | ---------------------------------------------------------------------- |
| + [pve_cloud_domain](#pve_cloud_domain ) | No      | string           | No         | -          | Cloud domain to connect to.                                            |
| + [target_cluster](#target_cluster )     | No      | string           | No         | -          | Target cluster we want to use inside the cloud (proxmox cluster name). |
| - [plugin](#plugin )                     | No      | enum (of string) | No         | -          | Id of ansible inventory plugin, needs to be set exactly.               |
| + [host_groups](#host_groups )           | No      | object           | No         | -          | Generic ansible hosts.                                                 |

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

## <a name="plugin"></a>3. Property `External Hosts Inventory > plugin`

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |

**Description:** Id of ansible inventory plugin, needs to be set exactly.

Must be one of:

* "pxc.cloud.ext_hosts_inv"

## <a name="host_groups"></a>4. Property `External Hosts Inventory > host_groups`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | Yes              |
| **Additional properties** | Any type allowed |

**Description:** Generic ansible hosts.

