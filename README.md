# Ansible Collection - pve.cloud

this collection provides tools to build a self hosted cloud environment on pve. it is heavily WIP!

## Docs

todo: move to pipeline

the main documentation resides as mkdocs in the `docs` folder. you can run them locally:

```bash
pip install -r requirements-doc.txt
mkdocs serve
```

### Generate markdown schemas

if you want to work on the documentation / schemas of this collection run the following commands to generate:

```bash
pip install -r requirements-doc.txt
generate-schema-doc --config-file docs-config.yaml plugins/inventory docs/schemas
mkdocs gh-deploy --remote-name github
```

