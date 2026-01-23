#!/usr/bin/python

import json

import requests
from ansible.module_utils.basic import AnsibleModule


def run_module():
    module_args = dict(
        challenge_data_dns=dict(type="list", required=True),
        ionos_cloud_token=dict(type="dict", required=True),
        cleanup=dict(type="bool", required=False, default=False),
    )
    module = AnsibleModule(argument_spec=module_args)

    # get all available zones first
    headers = {"Authorization": f"Bearer {module.params["ionos_cloud_token"]["token"]}"}

    # get zones
    response = requests.get("https://dns.de-fra.ionos.com/zones", headers=headers)
    response.raise_for_status()

    domains = json.loads(response.text)["items"]

    for challenge in module.params["challenge_data_dns"]:
        zone_id = None

        # find zone for challenge
        for domain in domains:
            if challenge["key"].endswith(domain["properties"]["zoneName"]):
                zone_id = domain["id"]

        if zone_id is None:
            raise Exception(f"no zone id could be found for {challenge}")

        if module.params["cleanup"]:
            # find acme records
            response = requests.get(
                f"https://dns.de-fra.ionos.com/zones/{zone_id}/records", headers=headers
            )
            zone_details = json.loads(response.text)

            acme_record_ids = []
            for record in zone_details["items"]:
                if record["properties"]["name"].startswith("_acme-challenge"):
                    acme_record_ids.append(record["id"])

            # delete them
            for record_id in acme_record_ids:
                response = requests.delete(
                    f"https://dns.de-fra.ionos.com/zones/{zone_id}/records/{record_id}",
                    headers=headers,
                )

        else:
            for chal in challenge["value"]:
                # just post the record challenge
                records_body = {
                    "name": challenge["key"],
                    "type": "TXT",
                    "content": chal,
                    "ttl": 120,
                }

                # post txt record
                response = requests.post(
                    f"https://dns.de-fra.ionos.com/zones/{zone_id}/records",
                    json=[records_body],
                    headers=headers,
                )

    result = dict(changed=True)

    module.exit_json(**result)


if __name__ == "__main__":
    run_module()
