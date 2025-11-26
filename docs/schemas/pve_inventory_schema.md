# Schema Docs

- [1. Pattern Property `root > ^.*$`](#pattern1)
  - [1.1. Pattern Property `root > ^.*$ > ^.*$`](#pattern1_pattern3)
    - [1.1.1. Pattern Property `root > ^.*$ > ^.*$ > ^.*$`](#pattern1_pattern3_pattern3)
      - [1.1.1.1. Property `root > ^.*$ > ^.*$ > ^.*$ > ansible_user`](#pattern1_pattern3_pattern3_ansible_user)
      - [1.1.1.2. Property `root > ^.*$ > ^.*$ > ^.*$ > ansible_host`](#pattern1_pattern3_pattern3_ansible_host)
      - [1.1.1.3. Property `root > ^.*$ > ^.*$ > ^.*$ > vars`](#pattern1_pattern3_pattern3_vars)
        - [1.1.1.3.1. Property `root > ^.*$ > ^.*$ > ^.*$ > vars > wol_iface`](#pattern1_pattern3_pattern3_vars_wol_iface)
        - [1.1.1.3.2. Property `root > ^.*$ > ^.*$ > ^.*$ > vars > tso_gso_fix`](#pattern1_pattern3_pattern3_vars_tso_gso_fix)
        - [1.1.1.3.3. Property `root > ^.*$ > ^.*$ > ^.*$ > vars > mac_iface_mapping`](#pattern1_pattern3_pattern3_vars_mac_iface_mapping)
          - [1.1.1.3.3.1. root > ^.*$ > ^.*$ > ^.*$ > vars > mac_iface_mapping > mac_iface_mapping items](#pattern1_pattern3_pattern3_vars_mac_iface_mapping_items)
            - [1.1.1.3.3.1.1. Property `root > ^.*$ > ^.*$ > ^.*$ > vars > mac_iface_mapping > mac_iface_mapping items > mac_addr`](#pattern1_pattern3_pattern3_vars_mac_iface_mapping_items_mac_addr)
            - [1.1.1.3.3.1.2. Property `root > ^.*$ > ^.*$ > ^.*$ > vars > mac_iface_mapping > mac_iface_mapping items > iface`](#pattern1_pattern3_pattern3_vars_mac_iface_mapping_items_iface)

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

**Description:** Inventory file located in user home directory ~/.pve-inventory.yaml, containing all the pve clusters the user has access to via ssh.

| Property             | Pattern | Type   | Deprecated | Definition | Title/Description                                                 |
| -------------------- | ------- | ------ | ---------- | ---------- | ----------------------------------------------------------------- |
| - [^.*$](#pattern1 ) | Yes     | object | No         | -          | The overarching pve cloud domain. Contains multiple pve clusters. |

## <a name="pattern1"></a>1. Pattern Property `root > ^.*$`
> All properties whose name matches the regular expression
```^.*$``` ([Test](https://regex101.com/?regex=%5E.%2A%24))
must respect the following conditions

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** The overarching pve cloud domain. Contains multiple pve clusters.

| Property                      | Pattern | Type   | Deprecated | Definition | Title/Description                                               |
| ----------------------------- | ------- | ------ | ---------- | ---------- | --------------------------------------------------------------- |
| - [^.*$](#pattern1_pattern3 ) | Yes     | object | No         | -          | The identifying pve cluster domain. Synonymous with target_pve. |

### <a name="pattern1_pattern3"></a>1.1. Pattern Property `root > ^.*$ > ^.*$`
> All properties whose name matches the regular expression
```^.*$``` ([Test](https://regex101.com/?regex=%5E.%2A%24))
must respect the following conditions

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

**Description:** The identifying pve cluster domain. Synonymous with target_pve.

| Property                               | Pattern | Type   | Deprecated | Definition | Title/Description               |
| -------------------------------------- | ------- | ------ | ---------- | ---------- | ------------------------------- |
| - [^.*$](#pattern1_pattern3_pattern3 ) | Yes     | object | No         | -          | Hostname of a pve host (short). |

#### <a name="pattern1_pattern3_pattern3"></a>1.1.1. Pattern Property `root > ^.*$ > ^.*$ > ^.*$`
> All properties whose name matches the regular expression
```^.*$``` ([Test](https://regex101.com/?regex=%5E.%2A%24))
must respect the following conditions

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

**Description:** Hostname of a pve host (short).

| Property                                                    | Pattern | Type   | Deprecated | Definition | Title/Description |
| ----------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| + [ansible_user](#pattern1_pattern3_pattern3_ansible_user ) | No      | string | No         | -          | -                 |
| + [ansible_host](#pattern1_pattern3_pattern3_ansible_host ) | No      | string | No         | -          | -                 |
| - [vars](#pattern1_pattern3_pattern3_vars )                 | No      | object | No         | -          | -                 |

##### <a name="pattern1_pattern3_pattern3_ansible_user"></a>1.1.1.1. Property `root > ^.*$ > ^.*$ > ^.*$ > ansible_user`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

##### <a name="pattern1_pattern3_pattern3_ansible_host"></a>1.1.1.2. Property `root > ^.*$ > ^.*$ > ^.*$ > ansible_host`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

##### <a name="pattern1_pattern3_pattern3_vars"></a>1.1.1.3. Property `root > ^.*$ > ^.*$ > ^.*$ > vars`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

| Property                                                                   | Pattern | Type            | Deprecated | Definition | Title/Description                                                                              |
| -------------------------------------------------------------------------- | ------- | --------------- | ---------- | ---------- | ---------------------------------------------------------------------------------------------- |
| - [wol_iface](#pattern1_pattern3_pattern3_vars_wol_iface )                 | No      | string          | No         | -          | Inteface wol should be enabled using ethtool                                                   |
| - [tso_gso_fix](#pattern1_pattern3_pattern3_vars_tso_gso_fix )             | No      | array           | No         | -          | Will turn of network optimizations on old network cards, this assures they can run indefinetly |
| - [mac_iface_mapping](#pattern1_pattern3_pattern3_vars_mac_iface_mapping ) | No      | array of object | No         | -          | -                                                                                              |

###### <a name="pattern1_pattern3_pattern3_vars_wol_iface"></a>1.1.1.3.1. Property `root > ^.*$ > ^.*$ > ^.*$ > vars > wol_iface`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Inteface wol should be enabled using ethtool

###### <a name="pattern1_pattern3_pattern3_vars_tso_gso_fix"></a>1.1.1.3.2. Property `root > ^.*$ > ^.*$ > ^.*$ > vars > tso_gso_fix`

|              |         |
| ------------ | ------- |
| **Type**     | `array` |
| **Required** | No      |

**Description:** Will turn of network optimizations on old network cards, this assures they can run indefinetly

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | N/A                |

###### <a name="pattern1_pattern3_pattern3_vars_mac_iface_mapping"></a>1.1.1.3.3. Property `root > ^.*$ > ^.*$ > ^.*$ > vars > mac_iface_mapping`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | No                |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                                                     | Description |
| ----------------------------------------------------------------------------------- | ----------- |
| [mac_iface_mapping items](#pattern1_pattern3_pattern3_vars_mac_iface_mapping_items) | -           |

###### <a name="pattern1_pattern3_pattern3_vars_mac_iface_mapping_items"></a>1.1.1.3.3.1. root > ^.*$ > ^.*$ > ^.*$ > vars > mac_iface_mapping > mac_iface_mapping items

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

| Property                                                                         | Pattern | Type   | Deprecated | Definition | Title/Description |
| -------------------------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| + [mac_addr](#pattern1_pattern3_pattern3_vars_mac_iface_mapping_items_mac_addr ) | No      | string | No         | -          | -                 |
| + [iface](#pattern1_pattern3_pattern3_vars_mac_iface_mapping_items_iface )       | No      | string | No         | -          | -                 |

###### <a name="pattern1_pattern3_pattern3_vars_mac_iface_mapping_items_mac_addr"></a>1.1.1.3.3.1.1. Property `root > ^.*$ > ^.*$ > ^.*$ > vars > mac_iface_mapping > mac_iface_mapping items > mac_addr`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

###### <a name="pattern1_pattern3_pattern3_vars_mac_iface_mapping_items_iface"></a>1.1.1.3.3.1.2. Property `root > ^.*$ > ^.*$ > ^.*$ > vars > mac_iface_mapping > mac_iface_mapping items > iface`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

----------------------------------------------------------------------------------------------------------------------------
Generated using [json-schema-for-humans](https://github.com/coveooss/json-schema-for-humans) on 2025-10-07 at 09:15:20 +0000
