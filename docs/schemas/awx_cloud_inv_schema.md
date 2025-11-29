# AWX Cron Inventory

**Title:** AWX Cron Inventory

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

| Property                         | Pattern | Type             | Deprecated | Definition | Title/Description                                                                                                                                    |
| -------------------------------- | ------- | ---------------- | ---------- | ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| + [target_pve](#target_pve )     | No      | string           | No         | -          | -                                                                                                                                                    |
| + [plugin](#plugin )             | No      | enum (of string) | No         | -          | Id of ansible inventory plugin.                                                                                                                      |
| + [pve_clusters](#pve_clusters ) | No      | object           | No         | -          | Copy of the inventory file located in user home directory ~/.pve-cloud-dyn-inv.yaml, containing all the pve clusters the user has access to via ssh. |

## <a name="target_pve"></a>1. Property `AWX Cron Inventory > target_pve`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

## <a name="plugin"></a>2. Property `AWX Cron Inventory > plugin`

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | Yes                |

**Description:** Id of ansible inventory plugin.

Must be one of:
* "pve.cloud.awx_cloud_inv"

## <a name="pve_clusters"></a>3. Property `AWX Cron Inventory > pve_clusters`

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | Yes         |
| **Additional properties** | Not allowed |

**Description:** Copy of the inventory file located in user home directory ~/.pve-cloud-dyn-inv.yaml, containing all the pve clusters the user has access to via ssh.

| Property                          | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [^.*$](#pve_clusters_pattern1 ) | Yes     | object | No         | -          | PVE cluster fqdn  |

### <a name="pve_clusters_pattern1"></a>3.1. Pattern Property `AWX Cron Inventory > pve_clusters > PVE cluster fqdn`
> All properties whose name matches the regular expression
```^.*$``` ([Test](https://regex101.com/?regex=%5E.%2A%24))
must respect the following conditions

**Title:** PVE cluster fqdn

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

**Description:** The identifying cluster domain. Synonymous with target_pve. Will be appended to stack_name(s).

| Property                                   | Pattern | Type   | Deprecated | Definition | Title/Description |
| ------------------------------------------ | ------- | ------ | ---------- | ---------- | ----------------- |
| - [^.*$](#pve_clusters_pattern1_pattern4 ) | Yes     | object | No         | -          | PVE Node Hostname |

#### <a name="pve_clusters_pattern1_pattern4"></a>3.1.1. Pattern Property `AWX Cron Inventory > pve_clusters > PVE cluster fqdn > PVE Node Hostname`
> All properties whose name matches the regular expression
```^.*$``` ([Test](https://regex101.com/?regex=%5E.%2A%24))
must respect the following conditions

**Title:** PVE Node Hostname

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

**Description:** Hostname of a pve host (short).

| Property                                                        | Pattern | Type   | Deprecated | Definition | Title/Description |
| --------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| + [ansible_user](#pve_clusters_pattern1_pattern4_ansible_user ) | No      | string | No         | -          | -                 |
| + [ansible_host](#pve_clusters_pattern1_pattern4_ansible_host ) | No      | string | No         | -          | -                 |

##### <a name="pve_clusters_pattern1_pattern4_ansible_user"></a>3.1.1.1. Property `AWX Cron Inventory > pve_clusters > PVE cluster fqdn > PVE Node Hostname > ansible_user`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

##### <a name="pve_clusters_pattern1_pattern4_ansible_host"></a>3.1.1.2. Property `AWX Cron Inventory > pve_clusters > PVE cluster fqdn > PVE Node Hostname > ansible_host`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

----------------------------------------------------------------------------------------------------------------------------
Generated using [json-schema-for-humans](https://github.com/coveooss/json-schema-for-humans) on 2025-11-29 at 23:48:23 +0000
