import os
import sys
import jsonschema
from ansible.errors import AnsibleParserError
from ansible.utils.display import Display

display = Display()

# inventory schema validation
def recursive_merge(dict1, dict2):
    for key, value in dict2.items():
        if key in dict1:
            if isinstance(dict1[key], dict) and isinstance(value, dict):
                dict1[key] = recursive_merge(dict1[key], value)
            elif isinstance(dict1[key], list) and isinstance(value, list):
                dict1[key] = dict1[key] + value
            else:
                dict1[key] = value
        else:
            dict1[key] = value
    return dict1


def validate_schema(loader, yaml_data, plugin_dir, plugin_name):
    schema = loader.load_from_file(f"{plugin_dir}/{plugin_name}_schema.yaml")
    # validate the inventory with it
    try:
        jsonschema.validate(instance=yaml_data, schema=schema)
    except jsonschema.ValidationError as e:
        raise AnsibleParserError(e.message)
    

def validate_schema_ext(loader, yaml_data, plugin_dir, plugin_name):
    schema = loader.load_from_file(f"{plugin_dir}/{plugin_name}_schema.yaml")

    # try to load playbook specific schema extension
    for arg in sys.argv:
        if arg.startswith("pve.cloud."):
            playbook = arg.split('.')[-1]
            display.v(f"identfied pve cloud playbook {playbook}")
            schema_ext_path = os.path.dirname(os.path.realpath(__file__)) + "/" + playbook + "_schema_ext.yaml"

            if os.path.exists(schema_ext_path):
                display.v(f"merging schema extension {schema_ext_path}")
                # found playbook schema extension, merge it
                schema_ext = loader.load_from_file(schema_ext_path)
                schema = recursive_merge(schema, schema_ext)
                break

    # validate the inventory with it
    try:
        jsonschema.validate(instance=yaml_data, schema=schema)
    except jsonschema.ValidationError as e:
        raise AnsibleParserError(e.message)


