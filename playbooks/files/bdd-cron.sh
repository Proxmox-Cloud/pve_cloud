#!/bin/bash 

# first we need to figure out the borg base dir from env variables
echo $(/opt/bdd/.venv/bin/brctl get-base-dir)
cd $(/opt/bdd/.venv/bin/brctl get-base-dir)

# process k8s borg archives (one per ns)
if [ -d "borg-k8s" ]; then
  for dir in borg-k8s/*; do
    echo "Processing $dir"

    borg prune -v --list --keep-daily=7 --keep-weekly=4 --keep-monthly=6 $dir

    if [[ "$VERIFY_DATA" == "true" ]]; then
      borg -v check --verify-data $dir
    else
      borg -v check $dir
    fi
  done
fi

# direct borg dirs no nesting
flat_dirs=("borg-nextcloud", "borg-git", "borg-postgres")

for flat_dir in "${flat_dirs[@]}"; do
  if [ -d "$flat_dir" ]; then
      echo "Processing $flat_dir"

      borg prune -v --list --keep-daily=7 --keep-weekly=4 --keep-monthly=6 $dir

      if [[ "$VERIFY_DATA" == "true" ]]; then
        borg -v check --verify-data $flat_dir
      else
        borg -v check $flat_dir
      fi
  fi
done