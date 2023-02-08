#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
import json
from ansible_collections.community.general.plugins.module_utils.identity.keycloak.keycloak import (
    URL_CLIENTS,
    KeycloakAPI,
    keycloak_argument_spec,
    get_token,
    open_url,
    quote,
    KeycloakError,
)
from ansible.module_utils.common.text.converters import to_native


__metaclass__ = type

DOCUMENTATION = r"""
---
module: associated_roles

short_description: adds associated roles to a role

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: adds associated roles to a role

options:
    name:
        description: This is the message to send to the test module.
        required: true
        type: str
    new:
        description:
            - Control to demo if the result of this module is changed or not.
            - Parameter description can be a list as well.
        required: false
        type: bool
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - my_namespace.my_collection.my_doc_fragment_name

author:
    - Your Name (@yourGitHubHandle)
"""

EXAMPLES = r"""
# Pass in a message
- name: Test with a message
  my_namespace.my_collection.my_test:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_namespace.my_collection.my_test:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_namespace.my_collection.my_test:
    name: fail me
"""

RETURN = r"""
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
"""

from ansible.module_utils.basic import AnsibleModule


class KeycloakAPIExt(KeycloakAPI):
    def get_clients_filtered(self, realm="master", filter=""):
        """Obtains client representations for clients in a realm

        :param realm: realm to be queried
        :param filter: if defined, only the client with clientId specified in the filter is returned
        :return: list of dicts of client representations
        """
        clientlist_url = URL_CLIENTS.format(url=self.baseurl, realm=realm)
        clientlist_url += "?q=%s" % quote(filter)

        try:
            return json.loads(
                to_native(
                    open_url(
                        clientlist_url,
                        http_agent=self.http_agent,
                        method="GET",
                        headers=self.restheaders,
                        timeout=self.connection_timeout,
                        validate_certs=self.validate_certs,
                    ).read()
                )
            )
        except ValueError as e:
            self.module.fail_json(
                msg="API returned incorrect JSON when trying to obtain list of clients for realm %s: %s"
                % (realm, str(e))
            )
        except Exception as e:
            self.module.fail_json(
                msg="Could not obtain list of clients for realm %s: %s"
                % (realm, str(e))
            )


def run_module():
    argument_spec = keycloak_argument_spec()

    meta_args = dict(
        realm=dict(type="str", default="master"),
        role_name=dict(type="str", required=True),
        associated_roles=dict(type="list", elements="str", default=[]),
    )

    argument_spec.update(meta_args)

    module = AnsibleModule(
        argument_spec=argument_spec,
        # for now we don't support check mode
        supports_check_mode=False,
        required_one_of=([["token", "auth_realm", "auth_username", "auth_password"]]),
        required_together=([["auth_realm", "auth_username", "auth_password"]]),
    )
    if module.check_mode:
        module.exit_json(**result)

    result = dict(changed=False, msg="", flow={})
    # Obtain access token, initialize API
    try:
        connection_header = get_token(module.params)
    except KeycloakError as e:
        module.fail_json(msg=str(e))

    realm = module.params.get("realm")
    role_name = module.params.get("role_name")
    associated_roles = module.params.get("associated_roles")

    kc = KeycloakAPIExt(module, connection_header)
    role = kc.get_realm_role(role_name, realm)
    if role is None:
        module.fail_json(msg=f"role {role_name} doesn't exist in realm {realm}")

    # that is how keycloak calls it
    role_mapping = []

    for associated_role in associated_roles:
        client_id, client_role_name = associated_role.split(".", 2)
        client = next(
            filter(
                lambda client: "clientId" in client and client["clientId"] == client_id,
                kc.get_clients_filtered(realm, client_id),
            )
        )
        if client is None:
            module.fail_json(msg=f"client {client_id} doesn't exist in realm {realm}")

        client_keycloak_id = client["id"]
        client_role_id = kc.get_client_role_id_by_name(
            client_keycloak_id, client_role_name, realm
        )
        if client_role_id is None:
            module.fail_json(
                msg=f"associated role {associated_role} doesn't exist in realm {realm}"
            )
        role_mapping.append({"id": client_role_id})

    kc.add_client_roles_by_id_composite_rolemapping(role["id"], role_mapping, realm)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
