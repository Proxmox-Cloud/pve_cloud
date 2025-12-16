

**Title:** HAProxy Inventory

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** LXC Inventory extension for the setup_proxy playbook. This extends the LXC Inventory schema.

| Property                               | Pattern | Type   | Deprecated | Definition | Title/Description                                                                                                                                       |
| -------------------------------------- | ------- | ------ | ---------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| + [static_includes](#static_includes ) | No      | object | No         | -          | Include other stacks into the ansible inventory, from any pve cloud you are connected to. From here you can freely extend and write your own playbooks. |
| - [lxcs](#lxcs )                       | No      | array  | No         | -          | List of lxcs that will be created for the stack.                                                                                                        |

## <a name="static_includes"></a>13. Property `HAProxy Inventory > static_includes`

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | Yes         |
| **Additional properties** | Not allowed |

**Description:** Include other stacks into the ansible inventory, from any pve cloud you are connected to. From here you can freely extend and write your own playbooks.

| Property                                             | Pattern | Type   | Deprecated | Definition | Title/Description                                                                                                                                                                                                        |
| ---------------------------------------------------- | ------- | ------ | ---------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| + [postgres_stack](#static_includes_postgres_stack ) | No      | string | No         | -          | Stack fqdn for postgres patroni stack. On the presence of the host the playbook will fetch<br />proxy configuration from the database. This is needed so that after the initial setup everything<br />still works.<br /> |

### <a name="static_includes_postgres_stack"></a>13.1. Property `HAProxy Inventory > static_includes > postgres_stack`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Stack fqdn for postgres patroni stack. On the presence of the host the playbook will fetch
proxy configuration from the database. This is needed so that after the initial setup everything
still works.

**Example:**

```json
"patroni.your-cloud.domain"
```

## <a name="lxcs"></a>14. Property `HAProxy Inventory > lxcs`

|              |         |
| ------------ | ------- |
| **Type**     | `array` |
| **Required** | No      |

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

### <a name="lxcs_items"></a>14.1. HAProxy Inventory > lxcs > lxcs items

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

| Property                    | Pattern | Type   | Deprecated | Definition | Title/Description                                                                         |
| --------------------------- | ------- | ------ | ---------- | ---------- | ----------------------------------------------------------------------------------------- |
| + [vars](#lxcs_items_vars ) | No      | object | No         | -          | Our proxy stack needs to know which lxc is the keepalived master and who is the failover. |

#### <a name="lxcs_items_vars"></a>14.1.1. Property `HAProxy Inventory > lxcs > lxcs items > vars`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | Yes              |
| **Additional properties** | Any type allowed |

**Description:** Our proxy stack needs to know which lxc is the keepalived master and who is the failover.

| Property                                                   | Pattern | Type    | Deprecated | Definition | Title/Description                                        |
| ---------------------------------------------------------- | ------- | ------- | ---------- | ---------- | -------------------------------------------------------- |
| + [keepalived_master](#lxcs_items_vars_keepalived_master ) | No      | boolean | No         | -          | One LXC should have this set to true the other to false. |

##### <a name="lxcs_items_vars_keepalived_master"></a>14.1.1.1. Property `HAProxy Inventory > lxcs > lxcs items > vars > keepalived_master`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

**Description:** One LXC should have this set to true the other to false.

