# Backup strategy

The collection integrates with the proxmox backup server and installs an additonal service onto the pbs.

This service takes care of k8s namespace backups, patroni dumps and gitlab repositories.

## Example strategy homelab

* Download the proxmox backup server iso image
* Manually create a vm in the proxmox ui with said image (give it a static ip)
* Passthrough usb port for attaching and swapping out external disks
* Go to Administration/Storage/Disks, wipe your external disk, then add it after under Directory/Create: Directory as a removable Datastore
* In the Shell go to /etc/proxmox-backup/datastore.cfg and copy your newly created datastore for later restores (save it to your cloud instance repository)
* Install your ssh key via the ui, create a .ini file with the pbs under the `qemus` host group in your cloud instance repository. Set the hostvar `PXC_REMOVABLE_DATASTORES` to a csv of your datastore names that you want the proxmox cloud backupper to use.
* Run the `pxc.cloud.setup_backup_daemon` playbook with the created ini file
* Deploy the [terraformpxc-backup module](https://github.com/Proxmox-Cloud/terraform-pxc-backup) on as many k8s clusters as you like, to backup k8s namespaces etc.
