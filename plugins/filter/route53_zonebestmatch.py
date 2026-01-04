DOCUMENTATION = r"""
name: route53_zonebestmatch
short_description: Finds the best matching zone for a domain in route53
"""

from ansible.errors import AnsibleError


class FilterModule(object):
    def filters(self):
        return {"route53_zonebestmatch": self.route53_zonebestmatch}

    def route53_zonebestmatch(self, domain, zonelist):
        zones = []
        target_labels = domain.rstrip(".").split(".")

        for zone in zonelist:
            if zone["config"]["private_zone"]:
                continue

            candidate_labels = zone["name"].rstrip(".").split(".")
            if candidate_labels == target_labels[-len(candidate_labels) :]:
                zones.append((zone["name"], zone["id"].removeprefix("/hostedzone/")))

        if not zones:
            raise AnsibleError(
                "Unable to find a matching zone in zonelist for domain: %s" % domain
            )

        zones.sort(key=lambda z: len(z[0]), reverse=True)
        return zones[0][1]
