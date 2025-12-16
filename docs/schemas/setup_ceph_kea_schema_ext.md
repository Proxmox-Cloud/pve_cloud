

**Title:** Ceph DHCP Inventory

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** LXC Inventory extension for the setup_ceph_kea playbook. This extends the LXC Inventory schema.

| Property         | Pattern | Type            | Deprecated | Definition | Title/Description                                |
| ---------------- | ------- | --------------- | ---------- | ---------- | ------------------------------------------------ |
| - [lxcs](#lxcs ) | No      | array of object | No         | -          | List of lxcs that will be created for the stack. |

## <a name="lxcs"></a>63. Property `Ceph DHCP Inventory > lxcs`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | No                |

**Description:** List of lxcs that will be created for the stack.

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be | Description |
| ------------------------------- | ----------- |
| [lxcs items](#lxcs_items)       | -           |

### <a name="lxcs_items"></a>63.1. Ceph DHCP Inventory > lxcs > lxcs items

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

| Property                                | Pattern | Type   | Deprecated | Definition | Title/Description                                                                                    |
| --------------------------------------- | ------- | ------ | ---------- | ---------- | ---------------------------------------------------------------------------------------------------- |
| - [parameters](#lxcs_items_parameters ) | No      | object | No         | -          | Besides the default lxc parameters you have to define the network interfaces with a certain pattern. |
| + [vars](#lxcs_items_vars )             | No      | object | No         | -          | The standalone ceph dhcp needs to know pool and subnet for assigning ips.                            |

#### <a name="lxcs_items_parameters"></a>63.1.1. Property `Ceph DHCP Inventory > lxcs > lxcs items > parameters`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Besides the default lxc parameters you have to define the network interfaces with a certain pattern.

| Property                               | Pattern | Type   | Deprecated | Definition | Title/Description                                                                                                                                                                                                                                                                                                         |
| -------------------------------------- | ------- | ------ | ---------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| - [net1](#lxcs_items_parameters_net1 ) | No      | object | No         | -          | This dhcp is exclusively for use with a seperate network for ceph frontend communication.<br />Ceph monitors are usually static and kubernetes nodes that use the csi driver need to<br />be able to communicate them. The interface needs to be named "cephfe" as this is how the<br />kea dhcp config is written.<br /> |

##### <a name="lxcs_items_parameters_net1"></a>63.1.1.1. Property `Ceph DHCP Inventory > lxcs > lxcs items > parameters > net1`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** This dhcp is exclusively for use with a seperate network for ceph frontend communication.
Ceph monitors are usually static and kubernetes nodes that use the csi driver need to
be able to communicate them. The interface needs to be named "cephfe" as this is how the
kea dhcp config is written.

| Restrictions                      |                                                                                 |
| --------------------------------- | ------------------------------------------------------------------------------- |
| **Must match regular expression** | ```\bname=cephfe\b``` [Test](https://regex101.com/?regex=%5Cbname%3Dcephfe%5Cb) |

#### <a name="lxcs_items_vars"></a>63.1.2. Property `Ceph DHCP Inventory > lxcs > lxcs items > vars`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | Yes              |
| **Additional properties** | Any type allowed |

**Description:** The standalone ceph dhcp needs to know pool and subnet for assigning ips.

| Property                                                                           | Pattern | Type   | Deprecated | Definition | Title/Description                                                                                                                    |
| ---------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| + [kea_dhcp_ceph_frontend_subnet](#lxcs_items_vars_kea_dhcp_ceph_frontend_subnet ) | No      | string | No         | -          | Optional definition for a seperate dhcp if the ceph frontend resides on a different interface (map it inside the dhcp lxcs to pve0). |
| + [kea_dhcp_ceph_frontend_pool](#lxcs_items_vars_kea_dhcp_ceph_frontend_pool )     | No      | string | No         | -          | Pool for ceph frontend ip allocations, this way monitors can have their static block.                                                |

##### <a name="lxcs_items_vars_kea_dhcp_ceph_frontend_subnet"></a>63.1.2.1. Property `Ceph DHCP Inventory > lxcs > lxcs items > vars > kea_dhcp_ceph_frontend_subnet`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Optional definition for a seperate dhcp if the ceph frontend resides on a different interface (map it inside the dhcp lxcs to pve0).

**Example:**

```json
"10.0.255.0/24"
```

##### <a name="lxcs_items_vars_kea_dhcp_ceph_frontend_pool"></a>63.1.2.2. Property `Ceph DHCP Inventory > lxcs > lxcs items > vars > kea_dhcp_ceph_frontend_pool`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Pool for ceph frontend ip allocations, this way monitors can have their static block.

**Example:**

```json
"10.0.255.40 - 10.0.255.254"
```

