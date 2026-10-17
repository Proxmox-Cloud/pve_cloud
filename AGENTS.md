# Agent Instructions

For instructions on how to execute integration tests, read the pxc-integration (Proxmox Cloud Integration Testing) skill.

## Creating Ansible Roles

Creating roles should always be done using `ansible-galaxy init ROLE_NAME` inside the `roles/` directory of this collection:

```bash
cd roles
ansible-galaxy init ROLE_NAME
```

