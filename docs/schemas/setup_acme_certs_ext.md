

**Title:** Setup generic acme certs sync job.

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Qemu schema extension for creation of a generic cert sync job.

| Property                                 | Pattern | Type   | Deprecated | Definition | Title/Description |
| ---------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------- |
| - [qemu_global_vars](#qemu_global_vars ) | No      | object | No         | -          | -                 |

## <a name="qemu_global_vars"></a>141. Property `Setup generic acme certs sync job. > qemu_global_vars`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

| Property                                                            | Pattern | Type            | Deprecated | Definition | Title/Description                                                                                                                                 |
| ------------------------------------------------------------------- | ------- | --------------- | ---------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| + [stack_cert_sync_paths](#qemu_global_vars_stack_cert_sync_paths ) | No      | array of object | No         | -          | Paths where we want the stack acme cert to be synced to, including ownership and permission settings.                                             |
| + [stack_cert_entries](#qemu_global_vars_stack_cert_entries )       | No      | array of object | No         | -          | Content for the acme certificate we want to generate and link to the stack. This is the certificate that will be synced to stack_cert_sync_paths. |

### <a name="qemu_global_vars_stack_cert_sync_paths"></a>141.1. Property `Setup generic acme certs sync job. > qemu_global_vars > stack_cert_sync_paths`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | Yes               |

**Description:** Paths where we want the stack acme cert to be synced to, including ownership and permission settings.

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                                              | Description                                                 |
| ---------------------------------------------------------------------------- | ----------------------------------------------------------- |
| [stack_cert_sync_paths items](#qemu_global_vars_stack_cert_sync_paths_items) | Full filesystem paths, including ownership and permissions. |

#### <a name="qemu_global_vars_stack_cert_sync_paths_items"></a>141.1.1. Setup generic acme certs sync job. > qemu_global_vars > stack_cert_sync_paths > stack_cert_sync_paths items

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Full filesystem paths, including ownership and permissions.

| Property                                                        | Pattern | Type   | Deprecated | Definition | Title/Description                                                    |
| --------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | -------------------------------------------------------------------- |
| - [path](#qemu_global_vars_stack_cert_sync_paths_items_path )   | No      | string | No         | -          | Full path to the public PEM certificate to sync, including filename. |
| - [owner](#qemu_global_vars_stack_cert_sync_paths_items_owner ) | No      | string | No         | -          | -                                                                    |
| - [group](#qemu_global_vars_stack_cert_sync_paths_items_group ) | No      | string | No         | -          | -                                                                    |
| - [mode](#qemu_global_vars_stack_cert_sync_paths_items_mode )   | No      | string | No         | -          | Octal mode file permission.                                          |

##### <a name="qemu_global_vars_stack_cert_sync_paths_items_path"></a>141.1.1.1. Property `Setup generic acme certs sync job. > qemu_global_vars > stack_cert_sync_paths > stack_cert_sync_paths items > path`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Full path to the public PEM certificate to sync, including filename.

##### <a name="qemu_global_vars_stack_cert_sync_paths_items_owner"></a>141.1.1.2. Property `Setup generic acme certs sync job. > qemu_global_vars > stack_cert_sync_paths > stack_cert_sync_paths items > owner`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

##### <a name="qemu_global_vars_stack_cert_sync_paths_items_group"></a>141.1.1.3. Property `Setup generic acme certs sync job. > qemu_global_vars > stack_cert_sync_paths > stack_cert_sync_paths items > group`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

##### <a name="qemu_global_vars_stack_cert_sync_paths_items_mode"></a>141.1.1.4. Property `Setup generic acme certs sync job. > qemu_global_vars > stack_cert_sync_paths > stack_cert_sync_paths items > mode`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Octal mode file permission.

### <a name="qemu_global_vars_stack_cert_entries"></a>141.2. Property `Setup generic acme certs sync job. > qemu_global_vars > stack_cert_entries`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | Yes               |

**Description:** Content for the acme certificate we want to generate and link to the stack. This is the certificate that will be synced to stack_cert_sync_paths.

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                                        | Description |
| ---------------------------------------------------------------------- | ----------- |
| [stack_cert_entries items](#qemu_global_vars_stack_cert_entries_items) | -           |

#### <a name="qemu_global_vars_stack_cert_entries_items"></a>141.2.1. Setup generic acme certs sync job. > qemu_global_vars > stack_cert_entries > stack_cert_entries items

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

| Property                                                                               | Pattern | Type            | Deprecated | Definition | Title/Description                                                                                                                                                    |
| -------------------------------------------------------------------------------------- | ------- | --------------- | ---------- | ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| + [zone](#qemu_global_vars_stack_cert_entries_items_zone )                             | No      | string          | No         | -          | DNS parent zone, should be the apex zone in ionos/route53 for dns01 challenge.                                                                                       |
| + [names](#qemu_global_vars_stack_cert_entries_items_names )                           | No      | array of string | No         | -          | -                                                                                                                                                                    |
| - [authoritative_zone](#qemu_global_vars_stack_cert_entries_items_authoritative_zone ) | No      | boolean         | No         | -          | This will cause the specified apex zone to be created as an authoritative zone in the proxmox clouds dns server. Ingress dns will only work for authoritative zones. |
| - [apex_zone_san](#qemu_global_vars_stack_cert_entries_items_apex_zone_san )           | No      | boolean         | No         | -          | Creates additional SAN for the zone, if you have *.example.com you will also get example.com in your certificate. Defaults to false.                                 |

##### <a name="qemu_global_vars_stack_cert_entries_items_zone"></a>141.2.1.1. Property `Setup generic acme certs sync job. > qemu_global_vars > stack_cert_entries > stack_cert_entries items > zone`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** DNS parent zone, should be the apex zone in ionos/route53 for dns01 challenge.

##### <a name="qemu_global_vars_stack_cert_entries_items_names"></a>141.2.1.2. Property `Setup generic acme certs sync job. > qemu_global_vars > stack_cert_entries > stack_cert_entries items > names`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of string` |
| **Required** | Yes               |

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                                       | Description                                                     |
| --------------------------------------------------------------------- | --------------------------------------------------------------- |
| [names items](#qemu_global_vars_stack_cert_entries_items_names_items) | SANs included in the certificate and basis for dns01 challenge. |

###### <a name="qemu_global_vars_stack_cert_entries_items_names_items"></a>141.2.1.2.1. Setup generic acme certs sync job. > qemu_global_vars > stack_cert_entries > stack_cert_entries items > names > names items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** SANs included in the certificate and basis for dns01 challenge.

**Examples:**

```json
"*"
```

```json
"example-service"
```

```json
"*.subzone"
```

##### <a name="qemu_global_vars_stack_cert_entries_items_authoritative_zone"></a>141.2.1.3. Property `Setup generic acme certs sync job. > qemu_global_vars > stack_cert_entries > stack_cert_entries items > authoritative_zone`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |

**Description:** This will cause the specified apex zone to be created as an authoritative zone in the proxmox clouds dns server. Ingress dns will only work for authoritative zones.

##### <a name="qemu_global_vars_stack_cert_entries_items_apex_zone_san"></a>141.2.1.4. Property `Setup generic acme certs sync job. > qemu_global_vars > stack_cert_entries > stack_cert_entries items > apex_zone_san`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |

**Description:** Creates additional SAN for the zone, if you have *.example.com you will also get example.com in your certificate. Defaults to false.

