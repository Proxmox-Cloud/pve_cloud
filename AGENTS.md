# Agent Instructions

This is the ansible collection at the heart of the Proxmox Cloud project.

## Testing

You should write and use existing tests. For this use the pxc-integration (Integration Testing Proxmox Cloud) skill.

## Creating Ansible Roles

Creating roles should always be done using `ansible-galaxy init ROLE_NAME` inside the `roles/` directory of this collection:

```bash
cd roles
ansible-galaxy init ROLE_NAME
```

