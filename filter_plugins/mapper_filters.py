from typing import Any


def _merge_dictionaries(dict1, dict2):
    """
    Recursive merge dictionaries.

    :param dict1: Base dictionary to merge.
    :param dict2: Dictionary to merge on top of base dictionary.
    :return: Merged dictionary
    """
    for key, val in dict1.items():
        if isinstance(val, dict):
            dict2_node = dict2.setdefault(key, {})
            _merge_dictionaries(val, dict2_node)
        else:
            if key not in dict2:
                dict2[key] = val

    return dict2


types = {
    # "groups": {
    #     "client_mapper_defaults": {
    #         "protocol": "openid-connect",
    #         "protocolMapper": "oidc-group-membership-mapper",
    #         "config": {"full.path": "no"},
    #     }
    # },
    "attribute": {
        "client_mapper_defaults": {
            "protocol": "openid-connect",
            "protocolMapper": "oidc-usermodel-attribute-mapper",
            "config": {
                "access.token.claim": "true",
                "aggregate.attrs": "false",
                "id.token.claim": "true",
                "jsonType.label": "",
                "multivalued": "false",
                "userinfo.token.claim": "true",
            },
        },
        "idp_mapper_defaults": {
            "identityProviderMapper": "oidc-user-attribute-idp-mapper",
            "config": {
                "are.claim.values.regex": False,
                "attributes": "[]",
                "claims": '[{"key":"","value":""}]',
                "syncMode": "INHERIT",
            },
        },
    },
}


def to_client_mapper(definition: dict[str, Any]):
    t = definition.pop("type")
    name = definition.pop("name")
    if t not in types:
        raise Exception(f"Unknown type {t}")

    # claim.name has to be present in all supported configs
    definition = _merge_dictionaries(
        {"name": name, "config": {"claim.name": name}},
        definition["client"] if "client" in definition else {},
    )
    # special case for attribute: predefine user.attribute
    if t == "attribute":
        definition["config"] = definition["config"] | {"user.attribute": name}
    return _merge_dictionaries(types[t]["client_mapper_defaults"], definition)


def to_idp_mapper(definition: dict[str, Any]):
    t = definition.pop("type")
    name = definition.pop("name")
    if t not in types:
        raise Exception(f"Unknown type {t}")

    # claim.name has to be present in all supported configs
    definition = _merge_dictionaries(
        {"name": name, "config": {"claim": name}},
        definition["idp"] if "idp" in definition else {},
    )
    # special case for attribute: predefine user.attribute
    if t == "attribute":
        definition["config"] = definition["config"] | {"user.attribute": name}
    return _merge_dictionaries(types[t]["idp_mapper_defaults"], definition)


class FilterModule(object):
    """Keycloak realm helpers"""

    def filters(self):
        return {"to_client_mapper": to_client_mapper, "to_idp_mapper": to_idp_mapper}
