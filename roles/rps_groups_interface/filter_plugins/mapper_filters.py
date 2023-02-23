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
        elif isinstance(val, list) and key in dict2:
            # merge lists too
            dict2[key] = dict2[key] + val
        else:
            if key not in dict2:
                dict2[key] = val

    return dict2


def to_oauth2_docker_service(realm, service_name, keycloak_service_name, base_service):
    name = realm.pop("name")
    client_secret = realm.pop("client_secret")
    cookie_secret = realm.pop("cookie_secret")
    redirect_url = f"https://{service_name}/realms/{name}/oauth2/callback"
    issuer_url = f"https://{keycloak_service_name}/realms/{name}"
    service = _merge_dictionaries(
        base_service,
        {
            "environment": [
                "OAUTH2_PROXY_CLIENT_ID=rps-groups-interface",
                f"OAUTH2_PROXY_UPSTREAMS=http://rps_groups_interface_{name}:3000",
                f"OAUTH2_PROXY_PROXY_PREFIX=/realms/{name}/oauth2",
                f"OAUTH2_PROXY_CLIENT_SECRET={client_secret}",
                f"OAUTH2_PROXY_COOKIE_SECRET={cookie_secret}",
                f"OAUTH2_PROXY_REDIRECT_URL={redirect_url}",
                f"OAUTH2_PROXY_OIDC_ISSUER_URL={issuer_url}",
                f"OAUTH2_PROXY_COOKIE_NAME=oauth2_proxy_{name}",
            ],
            "networks": [f"rps-groups-interface-{name}-realm"],
        },
    )
    # so we can use |items2dict
    return {
        "key": "oauth2_proxy_" + name,
        "value": service,
    }


def to_rps_groups_interface_docker_service(
    realm, service_name, keycloak_service_name, base_service
):
    name = realm.pop("name")
    service = _merge_dictionaries(
        base_service,
        {
            "environment": [
                f"BASE_URL=https://{service_name}/realms/{name}",
                # don't forget trailing slash!
                f"BASE_PATH=/realms/{name}/",
                f"KEYCLOAK_REALM_URL=https://{keycloak_service_name}/admin/realms/{name}",
            ],
            "networks": [f"rps-groups-interface-{name}-realm"],
        },
    )
    # so we can use |items2dict
    return {
        "key": "rps_groups_interface_" + name,
        "value": service,
    }


def to_traefik_router(realm, service_name):
    # so we can use |items2dict
    return {
        "key": f"rps_groups_interface_{realm['name']}",
        "value": {
            "rule": f"Host(`{service_name}`) && PathPrefix(`/realms/{realm['name']}`)",
            "entrypoints": "websecure",
            "service": f"rps_groups_interface_{realm['name']}",
            # "middlewares": [f"rps_groups_interface_{realm['name']}"],
            "tls": {"certresolver": "letsencrypt"},
        },
    }


def to_traefik_service(realm):
    # so we can use |items2dict
    return {
        "key": f"rps_groups_interface_{realm['name']}",
        "value": {
            "loadBalancer": {
                "servers": [{"url": f"http://oauth2_proxy_{realm['name']}:4180"}]
            }
        },
    }


class FilterModule(object):
    def filters(self):
        return {
            "to_oauth2_docker_service": to_oauth2_docker_service,
            "to_rps_groups_interface_docker_service": to_rps_groups_interface_docker_service,
            "to_traefik_service": to_traefik_service,
            "to_traefik_router": to_traefik_router,
            "to_traefik_middleware": to_traefik_middleware,
        }
