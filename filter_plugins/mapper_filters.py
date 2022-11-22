from typing import Any
import json


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
    "group": {
        "client_mapper_defaults": {
            "name": "groups",
            "protocol": "openid-connect",
            "protocolMapper": "oidc-group-membership-mapper",
            "config": {
                "full.path": "no",
                "claim.name": "groups",
                "access.token.claim": "true",
                "id.token.claim": "true",
                "userinfo.token.claim": "true",
            },
        },
        "idp_mapper_defaults": {
            "identityProviderMapper": "oidc-advanced-group-idp-mapper",
            "config": {
                "syncMode": "FORCE",
                "are.claim.values.regex": False,
                "attributes": "[]",
            },
        },
    },
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
                "syncMode": "INHERIT",
                "claims": '[{"key":"","value":""}]',
            },
        },
    },
    "role_from_group": {
        "idp_mapper_defaults": {
            "identityProviderMapper": "oidc-advanced-role-idp-mapper",
            "config": {
                "syncMode": "FORCE",
                "are.claim.values.regex": False,
                "attributes": "[]",
            },
        },
    },
}


def to_client_mappers(definitions):
    names = []
    mappers = []
    for definition in definitions:
        mapper = to_client_mapper(definition)
        if mapper["name"] not in names:
            names.append(mapper["name"])
            mappers.append(mapper)
    return mappers


def to_idp_mappers(definitions):
    # no special logic yet
    return map(lambda definition: to_idp_mapper(definition), definitions)


def to_client_mapper(definition: dict[str, Any]):
    t = definition.pop("type")
    name = definition.pop("name")
    if t not in types:
        raise Exception(f"Unknown type {t}")

    # for group import we create a single "groups" mapper. that can not be adjusted
    if t == "group":
        return types[t]["client_mapper_defaults"]
    elif t == "role_from_group":
        return types["group"]["client_mapper_defaults"]
    else:
        # claim.name has to be present in all supported configs
        mapper = _merge_dictionaries(
            {"name": name, "config": {"claim.name": name}},
            definition["client"] if "client" in definition else {},
        )
    # special case for attribute: predefine user.attribute
    if t == "attribute":
        mapper["config"] = mapper["config"] | {"user.attribute": name}
    return _merge_dictionaries(types[t]["client_mapper_defaults"], mapper)


def to_idp_mapper(definition: dict[str, Any]):
    t = definition.pop("type")
    name = definition.pop("name")
    if t not in types:
        raise Exception(f"Unknown type {t}")

    # claim.name has to be present in all supported configs
    mapper = _merge_dictionaries(
        {"name": name, "config": {"claim": name}},
        definition["idp"] if "idp" in definition else {},
    )
    # special case for attribute: predefine user.attribute
    if t == "attribute":
        mapper["config"] = mapper["config"] | {"user.attribute": name}
    elif t == "group":
        mapper["config"] = mapper["config"] | {
            "group": f"/{name}",
            "claims": json.dumps(
                [
                    {
                        "key": "groups",
                        "value": definition["from"] if "from" in definition else name,
                    }
                ]
            ),
        }
    elif t == "role_from_group":
        mapper["config"] = mapper["config"] | {
            "role": name,
            "claims": json.dumps(
                [{"key": "groups", "value": definition["from_group"]}]
            ),
        }
    return _merge_dictionaries(types[t]["idp_mapper_defaults"], mapper)


class FilterModule(object):
    """Keycloak realm helpers"""

    def filters(self):
        return {
            "to_client_mappers": to_client_mappers,
            "to_idp_mappers": to_idp_mappers,
        }
