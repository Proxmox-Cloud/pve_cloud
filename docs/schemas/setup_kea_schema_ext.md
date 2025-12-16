

**Title:** General DHCP Inventory

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** LXC Inventory extension for the setup_kea playbook. This extends the LXC Inventory schema.

| Property         | Pattern | Type            | Deprecated | Definition | Title/Description                                |
| ---------------- | ------- | --------------- | ---------- | ---------- | ------------------------------------------------ |
| - [lxcs](#lxcs ) | No      | array of object | No         | -          | List of lxcs that will be created for the stack. |

## <a name="lxcs"></a>19. Property `General DHCP Inventory > lxcs`

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

### <a name="lxcs_items"></a>19.1. General DHCP Inventory > lxcs > lxcs items

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

| Property                                | Pattern | Type   | Deprecated | Definition | Title/Description                                                                                              |
| --------------------------------------- | ------- | ------ | ---------- | ---------- | -------------------------------------------------------------------------------------------------------------- |
| - [parameters](#lxcs_items_parameters ) | No      | object | No         | -          | Besides the default lxc parameters you have to define the network interfaces with a certain pattern.           |
| + [vars](#lxcs_items_vars )             | No      | object | No         | -          | For the dhcp to work we need to tell the playbooks which lxc will serve as the main and which as the failover. |

#### <a name="lxcs_items_parameters"></a>19.1.1. Property `General DHCP Inventory > lxcs > lxcs items > parameters`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Besides the default lxc parameters you have to define the network interfaces with a certain pattern.

| Property                               | Pattern | Type   | Deprecated | Definition | Title/Description                                                                                                                                                                               |
| -------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| - [net0](#lxcs_items_parameters_net0 ) | No      | object | No         | -          | Network interface the dhcp will serve on. This has to be named "pve" instead of the normal eth0 for the dhcp playbooks to work,<br />they configure kea to listen on this interface name.<br /> |

##### <a name="lxcs_items_parameters_net0"></a>19.1.1.1. Property `General DHCP Inventory > lxcs > lxcs items > parameters > net0`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Network interface the dhcp will serve on. This has to be named "pve" instead of the normal eth0 for the dhcp playbooks to work,
they configure kea to listen on this interface name.

| Restrictions                      |                                                                           |
| --------------------------------- | ------------------------------------------------------------------------- |
| **Must match regular expression** | ```\bname=pve\b``` [Test](https://regex101.com/?regex=%5Cbname%3Dpve%5Cb) |

#### <a name="lxcs_items_vars"></a>19.1.2. Property `General DHCP Inventory > lxcs > lxcs items > vars`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | Yes              |
| **Additional properties** | Any type allowed |

**Description:** For the dhcp to work we need to tell the playbooks which lxc will serve as the main and which as the failover.

| Property                                           | Pattern | Type    | Deprecated | Definition | Title/Description                                                                                            |
| -------------------------------------------------- | ------- | ------- | ---------- | ---------- | ------------------------------------------------------------------------------------------------------------ |
| + [kea_dhcp_main](#lxcs_items_vars_kea_dhcp_main ) | No      | boolean | No         | -          | Determines the lxc that will be the dhcp master instance. One lxc should be set to true, the other to false. |

##### <a name="lxcs_items_vars_kea_dhcp_main"></a>19.1.2.1. Property `General DHCP Inventory > lxcs > lxcs items > vars > kea_dhcp_main`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

**Description:** Determines the lxc that will be the dhcp master instance. One lxc should be set to true, the other to false.

