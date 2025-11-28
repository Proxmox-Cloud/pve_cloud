# K8S Kubespray Inv.

**Title:** K8S Kubespray Inv.

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

**Description:** Inventory for deploying k8s clusters via kubespray on PVE.

| Property                                                 | Pattern | Type             | Deprecated | Definition | Title/Description                                                                                                                                                                                                                                               |
| -------------------------------------------------------- | ------- | ---------------- | ---------- | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| + [target_pve](#target_pve )                             | No      | string           | No         | -          | The pve cluster this stack should reside in, defined in ~/.pve-cloud-dyn-inv.yaml via \`pvcli connect-cluster\`                                                                                                                                                 |
| + [stack_name](#stack_name )                             | No      | string           | No         | -          | Your stack name, needs to be unique within the cloud domain. Will create its own sub zone.                                                                                                                                                                      |
| - [extra_control_plane_sans](#extra_control_plane_sans ) | No      | array of string  | No         | -          | Extra sans that kubespray will put in kubeapi generated certificates. Original kubespray variable is named supplementary_addresses_in_ssl_keys, <br />but is set via kubespray custom inventory. Read kubernetes page in pve cloud docs for more details.<br /> |
| - [external_domains](#external_domains )                 | No      | array of object  | No         | -          | Domains that will be exposed to the public proxies floating ip via haproxy routing rules.                                                                                                                                                                       |
| + [cluster_cert_entries](#cluster_cert_entries )         | No      | array of object  | No         | -          | Content for the clusters certificate. Internal routing is handled by ingress dns!                                                                                                                                                                               |
| + [tcp_proxies](#tcp_proxies )                           | No      | array of object  | No         | -          | TCP forwards to this cluster on the pve cluster proxy.                                                                                                                                                                                                          |
| + [static_includes](#static_includes )                   | No      | object           | No         | -          | -                                                                                                                                                                                                                                                               |
| - [include_stacks](#include_stacks )                     | No      | array of object  | No         | -          | Include other stacks into the ansible inventory, from any PVE cluster you like.                                                                                                                                                                                 |
| + [qemus](#qemus )                                       | No      | array of object  | No         | -          | Nodes for the cluster in form of qemu vms.                                                                                                                                                                                                                      |
| + [ceph_csi_sc_pools](#ceph_csi_sc_pools )               | No      | array of object  | No         | -          | Ceph pools that will be made available to the cluster CSI driver.                                                                                                                                                                                               |
| + [root_ssh_pub_key](#root_ssh_pub_key )                 | No      | string           | No         | -          | trusted root key for the cloud init image.                                                                                                                                                                                                                      |
| - [pve_ha_group](#pve_ha_group )                         | No      | string           | No         | -          | PVE HA group this vm should be assigned to (optional).                                                                                                                                                                                                          |
| - [qemu_hashed_pw](#qemu_hashed_pw )                     | No      | string           | No         | -          | Pw for default user defaults to hashed 'password' for debian cloud init image.                                                                                                                                                                                  |
| - [qemu_base_parameters](#qemu_base_parameters )         | No      | object           | No         | -          | Base parameters passed to the proxmox qm cli tool for creating vm                                                                                                                                                                                               |
| - [qemu_image_url](#qemu_image_url )                     | No      | string           | No         | -          | http(s) download link for cloud init image.                                                                                                                                                                                                                     |
| - [qemu_keyboard_layout](#qemu_keyboard_layout )         | No      | string           | No         | -          | Keyboard layout for cloudinit.                                                                                                                                                                                                                                  |
| - [qemu_network_config](#qemu_network_config )           | No      | string           | No         | -          | Optional qemu network config as a yaml string that is merged into the cloudinit network config of all qemus.                                                                                                                                                    |
| - [acme_staging](#acme_staging )                         | No      | boolean          | No         | -          | If set to true will use acme staging directory for issueing certs.                                                                                                                                                                                              |
| - [plugin](#plugin )                                     | No      | enum (of string) | No         | -          | Id of ansible inventory plugin.                                                                                                                                                                                                                                 |
| - [pve_cloud_pytest](#pve_cloud_pytest )                 | No      | object           | No         | -          | Variables object used only in e2e tests.                                                                                                                                                                                                                        |
| - [qemu_global_vars](#qemu_global_vars )                 | No      | object           | No         | -          | Variables that will be applied to all lxc hosts.                                                                                                                                                                                                                |

## <a name="target_pve"></a>1. Property `K8S Kubespray Inv. > target_pve`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** The pve cluster this stack should reside in, defined in ~/.pve-cloud-dyn-inv.yaml via `pvcli connect-cluster`

## <a name="stack_name"></a>2. Property `K8S Kubespray Inv. > stack_name`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Your stack name, needs to be unique within the cloud domain. Will create its own sub zone.

## <a name="extra_control_plane_sans"></a>3. Property `K8S Kubespray Inv. > extra_control_plane_sans`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of string` |
| **Required** | No                |

**Description:** Extra sans that kubespray will put in kubeapi generated certificates. Original kubespray variable is named supplementary_addresses_in_ssl_keys, 
but is set via kubespray custom inventory. Read kubernetes page in pve cloud docs for more details.

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                                   | Description |
| ----------------------------------------------------------------- | ----------- |
| [extra_control_plane_sans items](#extra_control_plane_sans_items) | -           |

### <a name="extra_control_plane_sans_items"></a>3.1. K8S Kubespray Inv. > extra_control_plane_sans > extra_control_plane_sans items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

## <a name="external_domains"></a>4. Property `K8S Kubespray Inv. > external_domains`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | No                |

**Description:** Domains that will be exposed to the public proxies floating ip via haproxy routing rules.

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                   | Description |
| ------------------------------------------------- | ----------- |
| [external_domains items](#external_domains_items) | -           |

### <a name="external_domains_items"></a>4.1. K8S Kubespray Inv. > external_domains > external_domains items

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

| Property                                            | Pattern | Type            | Deprecated | Definition | Title/Description                                                                                 |
| --------------------------------------------------- | ------- | --------------- | ---------- | ---------- | ------------------------------------------------------------------------------------------------- |
| + [zone](#external_domains_items_zone )             | No      | string          | No         | -          | DNS parent zone, should also be the zone that external records are made under in AWS for example. |
| - [expose_tld](#external_domains_items_expose_tld ) | No      | boolean         | No         | -          | Expose the top level domain itself.                                                               |
| + [names](#external_domains_items_names )           | No      | array of string | No         | -          | -                                                                                                 |

#### <a name="external_domains_items_zone"></a>4.1.1. Property `K8S Kubespray Inv. > external_domains > external_domains items > zone`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** DNS parent zone, should also be the zone that external records are made under in AWS for example.

#### <a name="external_domains_items_expose_tld"></a>4.1.2. Property `K8S Kubespray Inv. > external_domains > external_domains items > expose_tld`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |

**Description:** Expose the top level domain itself.

#### <a name="external_domains_items_names"></a>4.1.3. Property `K8S Kubespray Inv. > external_domains > external_domains items > names`

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

| Each item of this array must be                    | Description                 |
| -------------------------------------------------- | --------------------------- |
| [names items](#external_domains_items_names_items) | Hostname part (host + zone) |

##### <a name="external_domains_items_names_items"></a>4.1.3.1. K8S Kubespray Inv. > external_domains > external_domains items > names > names items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Hostname part (host + zone)

## <a name="cluster_cert_entries"></a>5. Property `K8S Kubespray Inv. > cluster_cert_entries`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | Yes               |

**Description:** Content for the clusters certificate. Internal routing is handled by ingress dns!

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                           | Description |
| --------------------------------------------------------- | ----------- |
| [cluster_cert_entries items](#cluster_cert_entries_items) | -           |

### <a name="cluster_cert_entries_items"></a>5.1. K8S Kubespray Inv. > cluster_cert_entries > cluster_cert_entries items

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

| Property                                                                | Pattern | Type            | Deprecated | Definition | Title/Description                                                                                                                    |
| ----------------------------------------------------------------------- | ------- | --------------- | ---------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| + [zone](#cluster_cert_entries_items_zone )                             | No      | string          | No         | -          | DNS parent zone, should coincide with tld for dns01 challenge.                                                                       |
| + [names](#cluster_cert_entries_items_names )                           | No      | array of string | No         | -          | -                                                                                                                                    |
| - [authoritative_zone](#cluster_cert_entries_items_authoritative_zone ) | No      | boolean         | No         | -          | Create authoritative zone inside of pve cloud bind dns.                                                                              |
| - [apex_zone_san](#cluster_cert_entries_items_apex_zone_san )           | No      | boolean         | No         | -          | Creates additional SAN for the zone, if you have *.example.com you will also get example.com in your certificate. Defaults to false. |

#### <a name="cluster_cert_entries_items_zone"></a>5.1.1. Property `K8S Kubespray Inv. > cluster_cert_entries > cluster_cert_entries items > zone`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** DNS parent zone, should coincide with tld for dns01 challenge.

#### <a name="cluster_cert_entries_items_names"></a>5.1.2. Property `K8S Kubespray Inv. > cluster_cert_entries > cluster_cert_entries items > names`

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

| Each item of this array must be                        | Description                 |
| ------------------------------------------------------ | --------------------------- |
| [names items](#cluster_cert_entries_items_names_items) | Hostname part (host + zone) |

##### <a name="cluster_cert_entries_items_names_items"></a>5.1.2.1. K8S Kubespray Inv. > cluster_cert_entries > cluster_cert_entries items > names > names items

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Hostname part (host + zone)

#### <a name="cluster_cert_entries_items_authoritative_zone"></a>5.1.3. Property `K8S Kubespray Inv. > cluster_cert_entries > cluster_cert_entries items > authoritative_zone`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |

**Description:** Create authoritative zone inside of pve cloud bind dns.

#### <a name="cluster_cert_entries_items_apex_zone_san"></a>5.1.4. Property `K8S Kubespray Inv. > cluster_cert_entries > cluster_cert_entries items > apex_zone_san`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |

**Description:** Creates additional SAN for the zone, if you have *.example.com you will also get example.com in your certificate. Defaults to false.

## <a name="tcp_proxies"></a>6. Property `K8S Kubespray Inv. > tcp_proxies`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | Yes               |

**Description:** TCP forwards to this cluster on the pve cluster proxy.

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be         | Description |
| --------------------------------------- | ----------- |
| [tcp_proxies items](#tcp_proxies_items) | -           |

### <a name="tcp_proxies_items"></a>6.1. K8S Kubespray Inv. > tcp_proxies > tcp_proxies items

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

| Property                                             | Pattern | Type    | Deprecated | Definition | Title/Description                                                                                     |
| ---------------------------------------------------- | ------- | ------- | ---------- | ---------- | ----------------------------------------------------------------------------------------------------- |
| + [proxy_name](#tcp_proxies_items_proxy_name )       | No      | string  | No         | -          | Name of the proxy port. Should be unique for the stack.                                               |
| + [haproxy_port](#tcp_proxies_items_haproxy_port )   | No      | number  | No         | -          | Port on the haproxy frontend that listens.                                                            |
| + [node_port](#tcp_proxies_items_node_port )         | No      | number  | No         | -          | Port on the nodes, usually via K8S NodePort                                                           |
| - [proxy_snippet](#tcp_proxies_items_proxy_snippet ) | No      | string  | No         | -          | additional snippet that will be inserted into the haproxy listen block. Can be used for custom logic. |
| - [external](#tcp_proxies_items_external )           | No      | boolean | No         | -          | Will bind to the external floating ip aswell.                                                         |

#### <a name="tcp_proxies_items_proxy_name"></a>6.1.1. Property `K8S Kubespray Inv. > tcp_proxies > tcp_proxies items > proxy_name`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Name of the proxy port. Should be unique for the stack.

#### <a name="tcp_proxies_items_haproxy_port"></a>6.1.2. Property `K8S Kubespray Inv. > tcp_proxies > tcp_proxies items > haproxy_port`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

**Description:** Port on the haproxy frontend that listens.

#### <a name="tcp_proxies_items_node_port"></a>6.1.3. Property `K8S Kubespray Inv. > tcp_proxies > tcp_proxies items > node_port`

|              |          |
| ------------ | -------- |
| **Type**     | `number` |
| **Required** | Yes      |

**Description:** Port on the nodes, usually via K8S NodePort

#### <a name="tcp_proxies_items_proxy_snippet"></a>6.1.4. Property `K8S Kubespray Inv. > tcp_proxies > tcp_proxies items > proxy_snippet`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** additional snippet that will be inserted into the haproxy listen block. Can be used for custom logic.

#### <a name="tcp_proxies_items_external"></a>6.1.5. Property `K8S Kubespray Inv. > tcp_proxies > tcp_proxies items > external`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |

**Description:** Will bind to the external floating ip aswell.

## <a name="static_includes"></a>7. Property `K8S Kubespray Inv. > static_includes`

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | Yes         |
| **Additional properties** | Not allowed |

| Property                                             | Pattern | Type   | Deprecated | Definition | Title/Description                                                                                              |
| ---------------------------------------------------- | ------- | ------ | ---------- | ---------- | -------------------------------------------------------------------------------------------------------------- |
| + [dhcp_stack](#static_includes_dhcp_stack )         | No      | string | No         | -          | Stack fqdn of dhcp stack where reservations for node ips should be made.                                       |
| + [proxy_stack](#static_includes_proxy_stack )       | No      | string | No         | -          | Stack fqdn of haproxy stack where ingress and proxy rules should be configured.                                |
| + [postgres_stack](#static_includes_postgres_stack ) | No      | string | No         | -          | Stack fqdn of postgres stack where state and general configuration of our pve cloud is stored.                 |
| + [bind_stack](#static_includes_bind_stack )         | No      | string | No         | -          | Stack fqdn of bind servers, where create_bind_zone: true ingress_domain zones will be created.                 |
| - [cache_stack](#static_includes_cache_stack )       | No      | string | No         | -          | Cache stack to mount nfs for kubespray cache and apt cache. Assumes the cache lxc to have the hostname "main". |

### <a name="static_includes_dhcp_stack"></a>7.1. Property `K8S Kubespray Inv. > static_includes > dhcp_stack`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Stack fqdn of dhcp stack where reservations for node ips should be made.

### <a name="static_includes_proxy_stack"></a>7.2. Property `K8S Kubespray Inv. > static_includes > proxy_stack`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Stack fqdn of haproxy stack where ingress and proxy rules should be configured.

### <a name="static_includes_postgres_stack"></a>7.3. Property `K8S Kubespray Inv. > static_includes > postgres_stack`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Stack fqdn of postgres stack where state and general configuration of our pve cloud is stored.

### <a name="static_includes_bind_stack"></a>7.4. Property `K8S Kubespray Inv. > static_includes > bind_stack`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Stack fqdn of bind servers, where create_bind_zone: true ingress_domain zones will be created.

### <a name="static_includes_cache_stack"></a>7.5. Property `K8S Kubespray Inv. > static_includes > cache_stack`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Cache stack to mount nfs for kubespray cache and apt cache. Assumes the cache lxc to have the hostname "main".

## <a name="include_stacks"></a>8. Property `K8S Kubespray Inv. > include_stacks`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | No                |

**Description:** Include other stacks into the ansible inventory, from any PVE cluster you like.

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be               | Description |
| --------------------------------------------- | ----------- |
| [include_stacks items](#include_stacks_items) | -           |

### <a name="include_stacks_items"></a>8.1. K8S Kubespray Inv. > include_stacks > include_stacks items

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

| Property                                                        | Pattern | Type   | Deprecated | Definition | Title/Description                                                                                                       |
| --------------------------------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------------------------------------------------------------------------------------------------------------- |
| + [stack_fqdn](#include_stacks_items_stack_fqdn )               | No      | string | No         | -          | Target stack fqdn to include (stack name + pve_cloud_domain). Will automatically include it from the right pve cluster. |
| + [host_group](#include_stacks_items_host_group )               | No      | string | No         | -          | This is the name of the hosts group of our ansible inventory the included vms will be under.                            |
| - [qemu_ansible_user](#include_stacks_items_qemu_ansible_user ) | No      | string | No         | -          | User ansible will use to connect, defaults to admin.                                                                    |

#### <a name="include_stacks_items_stack_fqdn"></a>8.1.1. Property `K8S Kubespray Inv. > include_stacks > include_stacks items > stack_fqdn`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Target stack fqdn to include (stack name + pve_cloud_domain). Will automatically include it from the right pve cluster.

#### <a name="include_stacks_items_host_group"></a>8.1.2. Property `K8S Kubespray Inv. > include_stacks > include_stacks items > host_group`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** This is the name of the hosts group of our ansible inventory the included vms will be under.

#### <a name="include_stacks_items_qemu_ansible_user"></a>8.1.3. Property `K8S Kubespray Inv. > include_stacks > include_stacks items > qemu_ansible_user`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** User ansible will use to connect, defaults to admin.

## <a name="qemus"></a>9. Property `K8S Kubespray Inv. > qemus`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | Yes               |

**Description:** Nodes for the cluster in form of qemu vms.

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be | Description |
| ------------------------------- | ----------- |
| [qemus items](#qemus_items)     | -           |

### <a name="qemus_items"></a>9.1. K8S Kubespray Inv. > qemus > qemus items

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

| Property                                         | Pattern | Type   | Deprecated | Definition | Title/Description                                                                                                      |
| ------------------------------------------------ | ------- | ------ | ---------- | ---------- | ---------------------------------------------------------------------------------------------------------------------- |
| - [hostname](#qemus_items_hostname )             | No      | string | No         | -          | Optional unique hostname for this node, otherwise pet name random name will be generated.                              |
| - [vars](#qemus_items_vars )                     | No      | object | No         | -          | Custom variables for this node specifically.                                                                           |
| + [k8s_roles](#qemus_items_k8s_roles )           | No      | array  | No         | -          | String array of k8s roles (master/worker)                                                                              |
| - [target_host](#qemus_items_target_host )       | No      | string | No         | -          | Pve host to tie this vm to.                                                                                            |
| + [parameters](#qemus_items_parameters )         | No      | object | No         | -          | In accordance with pve qm cli tool, creation args.                                                                     |
| - [network_config](#qemus_items_network_config ) | No      | string | No         | -          | Cinit network config yaml string. Will be the last cfg piece that gets merged into the final cloudinit network config. |
| + [disk](#qemus_items_disk )                     | No      | object | No         | -          | -                                                                                                                      |

#### <a name="qemus_items_hostname"></a>9.1.1. Property `K8S Kubespray Inv. > qemus > qemus items > hostname`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Optional unique hostname for this node, otherwise pet name random name will be generated.

#### <a name="qemus_items_vars"></a>9.1.2. Property `K8S Kubespray Inv. > qemus > qemus items > vars`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Custom variables for this node specifically.

#### <a name="qemus_items_k8s_roles"></a>9.1.3. Property `K8S Kubespray Inv. > qemus > qemus items > k8s_roles`

|              |         |
| ------------ | ------- |
| **Type**     | `array` |
| **Required** | Yes     |

**Description:** String array of k8s roles (master/worker)

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | N/A                |

#### <a name="qemus_items_target_host"></a>9.1.4. Property `K8S Kubespray Inv. > qemus > qemus items > target_host`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Pve host to tie this vm to.

#### <a name="qemus_items_parameters"></a>9.1.5. Property `K8S Kubespray Inv. > qemus > qemus items > parameters`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | Yes              |
| **Additional properties** | Any type allowed |

**Description:** In accordance with pve qm cli tool, creation args.

#### <a name="qemus_items_network_config"></a>9.1.6. Property `K8S Kubespray Inv. > qemus > qemus items > network_config`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Cinit network config yaml string. Will be the last cfg piece that gets merged into the final cloudinit network config.

#### <a name="qemus_items_disk"></a>9.1.7. Property `K8S Kubespray Inv. > qemus > qemus items > disk`

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | Yes         |
| **Additional properties** | Not allowed |

| Property                                | Pattern | Type   | Deprecated | Definition | Title/Description                               |
| --------------------------------------- | ------- | ------ | ---------- | ---------- | ----------------------------------------------- |
| + [size](#qemus_items_disk_size )       | No      | string | No         | -          | Size of the vms disk.                           |
| - [options](#qemus_items_disk_options ) | No      | object | No         | -          | Mount options                                   |
| + [pool](#qemus_items_disk_pool )       | No      | string | No         | -          | Ceph pool name the vms disk will be created in. |

##### <a name="qemus_items_disk_size"></a>9.1.7.1. Property `K8S Kubespray Inv. > qemus > qemus items > disk > size`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Size of the vms disk.

##### <a name="qemus_items_disk_options"></a>9.1.7.2. Property `K8S Kubespray Inv. > qemus > qemus items > disk > options`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Mount options

##### <a name="qemus_items_disk_pool"></a>9.1.7.3. Property `K8S Kubespray Inv. > qemus > qemus items > disk > pool`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Ceph pool name the vms disk will be created in.

## <a name="ceph_csi_sc_pools"></a>10. Property `K8S Kubespray Inv. > ceph_csi_sc_pools`

|              |                   |
| ------------ | ----------------- |
| **Type**     | `array of object` |
| **Required** | Yes               |

**Description:** Ceph pools that will be made available to the cluster CSI driver.

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | See below          |

| Each item of this array must be                     | Description |
| --------------------------------------------------- | ----------- |
| [ceph_csi_sc_pools items](#ceph_csi_sc_pools_items) | -           |

### <a name="ceph_csi_sc_pools_items"></a>10.1. K8S Kubespray Inv. > ceph_csi_sc_pools > ceph_csi_sc_pools items

|                           |             |
| ------------------------- | ----------- |
| **Type**                  | `object`    |
| **Required**              | No          |
| **Additional properties** | Not allowed |

| Property                                                   | Pattern | Type    | Deprecated | Definition | Title/Description                                                                       |
| ---------------------------------------------------------- | ------- | ------- | ---------- | ---------- | --------------------------------------------------------------------------------------- |
| + [name](#ceph_csi_sc_pools_items_name )                   | No      | string  | No         | -          | Name of the pool in the ceph of our PVE cluster.                                        |
| + [default](#ceph_csi_sc_pools_items_default )             | No      | boolean | No         | -          | Whether or not the pool is the default storage class.                                   |
| + [mount_options](#ceph_csi_sc_pools_items_mount_options ) | No      | array   | No         | -          | String array of mount options that will be set in the storage class and applied to pvs. |

#### <a name="ceph_csi_sc_pools_items_name"></a>10.1.1. Property `K8S Kubespray Inv. > ceph_csi_sc_pools > ceph_csi_sc_pools items > name`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** Name of the pool in the ceph of our PVE cluster.

#### <a name="ceph_csi_sc_pools_items_default"></a>10.1.2. Property `K8S Kubespray Inv. > ceph_csi_sc_pools > ceph_csi_sc_pools items > default`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | Yes       |

**Description:** Whether or not the pool is the default storage class.

#### <a name="ceph_csi_sc_pools_items_mount_options"></a>10.1.3. Property `K8S Kubespray Inv. > ceph_csi_sc_pools > ceph_csi_sc_pools items > mount_options`

|              |         |
| ------------ | ------- |
| **Type**     | `array` |
| **Required** | Yes     |

**Description:** String array of mount options that will be set in the storage class and applied to pvs.

|                      | Array restrictions |
| -------------------- | ------------------ |
| **Min items**        | N/A                |
| **Max items**        | N/A                |
| **Items unicity**    | False              |
| **Additional items** | False              |
| **Tuple validation** | N/A                |

## <a name="root_ssh_pub_key"></a>11. Property `K8S Kubespray Inv. > root_ssh_pub_key`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | Yes      |

**Description:** trusted root key for the cloud init image.

## <a name="pve_ha_group"></a>12. Property `K8S Kubespray Inv. > pve_ha_group`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** PVE HA group this vm should be assigned to (optional).

## <a name="qemu_hashed_pw"></a>13. Property `K8S Kubespray Inv. > qemu_hashed_pw`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Pw for default user defaults to hashed 'password' for debian cloud init image.

## <a name="qemu_base_parameters"></a>14. Property `K8S Kubespray Inv. > qemu_base_parameters`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Base parameters passed to the proxmox qm cli tool for creating vm

## <a name="qemu_image_url"></a>15. Property `K8S Kubespray Inv. > qemu_image_url`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** http(s) download link for cloud init image.

## <a name="qemu_keyboard_layout"></a>16. Property `K8S Kubespray Inv. > qemu_keyboard_layout`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Keyboard layout for cloudinit.

## <a name="qemu_network_config"></a>17. Property `K8S Kubespray Inv. > qemu_network_config`

|              |          |
| ------------ | -------- |
| **Type**     | `string` |
| **Required** | No       |

**Description:** Optional qemu network config as a yaml string that is merged into the cloudinit network config of all qemus.

## <a name="acme_staging"></a>18. Property `K8S Kubespray Inv. > acme_staging`

|              |           |
| ------------ | --------- |
| **Type**     | `boolean` |
| **Required** | No        |

**Description:** If set to true will use acme staging directory for issueing certs.

## <a name="plugin"></a>19. Property `K8S Kubespray Inv. > plugin`

|              |                    |
| ------------ | ------------------ |
| **Type**     | `enum (of string)` |
| **Required** | No                 |

**Description:** Id of ansible inventory plugin.

Must be one of:
* "pve.cloud.kubespray_inv"

## <a name="pve_cloud_pytest"></a>20. Property `K8S Kubespray Inv. > pve_cloud_pytest`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Variables object used only in e2e tests.

## <a name="qemu_global_vars"></a>21. Property `K8S Kubespray Inv. > qemu_global_vars`

|                           |                  |
| ------------------------- | ---------------- |
| **Type**                  | `object`         |
| **Required**              | No               |
| **Additional properties** | Any type allowed |

**Description:** Variables that will be applied to all lxc hosts.

----------------------------------------------------------------------------------------------------------------------------
Generated using [json-schema-for-humans](https://github.com/coveooss/json-schema-for-humans) on 2025-11-28 at 22:52:22 +0000
