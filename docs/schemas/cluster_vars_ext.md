

**Title:** Cluster vars extension.

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Cluster vars extension for custom schema based on functions in validate.py and pve_cloud_inv.py dynamic inventory.

| Property                                                         | Pattern | Type   | Deprecated | Definition | Title/Description                                                                |
| ---------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | -------------------------------------------------------------------------------- |
| + [pve_cloud_collection_version](#pve_cloud_collection_version ) | No      | string | No         | -          | Dynamic property set by pve_cloud_inv for validation of the collections version. |
| + [py_pve_cloud_version](#py_pve_cloud_version )                 | No      | string | No         | -          | Dynamic property for validation of the core python pve cloud library in use.     |
| + [pve_cluster_name](#pve_cluster_name )                         | No      | string | No         | -          | Self reference of the cluster name for convinient access.                        |

## <a name="pve_cloud_collection_version"></a>41. Property `Cluster vars extension. > pve_cloud_collection_version`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Dynamic property set by pve_cloud_inv for validation of the collections version.

## <a name="py_pve_cloud_version"></a>42. Property `Cluster vars extension. > py_pve_cloud_version`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Dynamic property for validation of the core python pve cloud library in use.

## <a name="pve_cluster_name"></a>43. Property `Cluster vars extension. > pve_cluster_name`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Self reference of the cluster name for convinient access.

