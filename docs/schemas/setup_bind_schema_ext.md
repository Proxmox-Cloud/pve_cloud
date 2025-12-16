# Bind Dns Inventory

**Title:** Bind Dns Inventory

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** LXC Inventory extension for the setup_bind playbook. This extends the LXC Inventory schema.

| Property         | Pattern | Type            | Deprecated | Definition | Title/Description                                |
| ---------------- | ------- | --------------- | ---------- | ---------- | ------------------------------------------------ |
| - [lxcs](#lxcs ) | No      | array of object | No         | -          | List of lxcs that will be created for the stack. |

## <a name="lxcs"></a>1. Property `Bind Dns Inventory > lxcs`

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

### <a name="lxcs_items"></a>1.1. Bind Dns Inventory > lxcs > lxcs items

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

| Property                    | Pattern | Type   | Deprecated | Definition | Title/Description                                                                                            |
| --------------------------- | ------- | ------ | ---------- | ---------- | ------------------------------------------------------------------------------------------------------------ |
| + [vars](#lxcs_items_vars ) | No      | object | No         | -          | For the dns to work we need to tell the playbooks which lxc will serve as the master and which as the slave. |

#### <a name="lxcs_items_vars"></a>1.1.1. Property `Bind Dns Inventory > lxcs > lxcs items > vars`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | Yes              |
| **Additional properties** | Any type allowed |

**Description:** For the dns to work we need to tell the playbooks which lxc will serve as the master and which as the slave.

| Property                                       | Pattern | Type    | Deprecated | Definition | Title/Description                                                                                                                                                         |
| ---------------------------------------------- | ------- | ------- | ---------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| + [bind_master](#lxcs_items_vars_bind_master ) | No      | boolean | No         | -          | The default pve cloud configured dns uses only a master slave combination. You should create two lxcs,<br />one that has this flag set to true, the other to false.<br /> |

##### <a name="lxcs_items_vars_bind_master"></a>1.1.1.1. Property `Bind Dns Inventory > lxcs > lxcs items > vars > bind_master`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

**Description:** The default pve cloud configured dns uses only a master slave combination. You should create two lxcs,
one that has this flag set to true, the other to false.

----------------------------------------------------------------------------------------------------------------------------
Generated using [json-schema-for-humans](https://github.com/coveooss/json-schema-for-humans) on 2025-12-16 at 21:30:38 +0000
