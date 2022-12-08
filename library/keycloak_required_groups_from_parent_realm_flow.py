#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
import json

__metaclass__ = type

DOCUMENTATION = r"""
---
module: keycloak_required_groups_from_parent_realm_flow

short_description: manages a flow that enforces group membership for logging in

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: manages a flow that enforces group membership for logging in

options:
    realm:
        description:
            - The realm to create the flow in.
        type: str
        default: master
    flow:
        description:
            - the flowalias to create the required groups flow in
        required: true
        type: str
    subflow:
        description:
            - the subflow within the flowa to create the required groups flow in
        default: same as flowalias
        type: str
    groupchecksflow:
        description:
            - name of the groupchecksflow
        default: {flowalias}-groupchecks
        type: str
    required_groups_from_parent_realm:
        description:
            - list of group names that are required for login
        default: empty
        type: list
        elements: str

extends_documentation_fragment:
- community.general.keycloak

author:
    - Andreas Streichardt (@m0ppers)
"""

EXAMPLES = r"""
- name: "create require-group authentication flow"
  keycloak_required_groups_from_parent_realm_flow:
    auth_keycloak_url: "https://auth.example.com/auth"
    token: "KEYCLOAK_AUTH_TOKEN"
    realm: "master"
    flow: "master-browser-flow"
    subflow: "master-browser-flow forms"
    required_groups_from_parent_realm:
        - group1
        - group2
"""

RETURN = r"""
# These are examples of possible return values, and in general should use other names for return values.
"""

from ansible_collections.community.general.plugins.module_utils.identity.keycloak.keycloak import (
    URL_AUTHENTICATION_EXECUTION_CONFIG,
    KeycloakAPI,
    keycloak_argument_spec,
    get_token,
    open_url,
    quote,
    KeycloakError,
    URL_AUTHENTICATION_FLOW_EXECUTIONS_EXECUTION,
)
from ansible.module_utils.basic import AnsibleModule
import uuid

URL_AUTHENTICATION_EXECUTIONS_ID = (
    "{url}/admin/realms/{realm}/authentication/executions/{id}"
)


class KeycloakAPIExt(KeycloakAPI):
    def delete_execution(self, execution_id, realm="master"):
        """delete an execution on the flow

        :param flowAlias: name of the flow
        :return: HTTPResponse object on success
        """
        try:
            open_url(
                URL_AUTHENTICATION_EXECUTIONS_ID.format(
                    url=self.baseurl, realm=realm, id=quote(execution_id)
                ),
                method="DELETE",
                http_agent=self.http_agent,
                headers=self.restheaders,
                timeout=self.connection_timeout,
                validate_certs=self.validate_certs,
            )
        except Exception as e:
            self.module.fail_json(
                msg="Unable to delete execution %s: %s" % (execution_id, str(e))
            )

    def create_execution_ext(self, provider, flowAlias, realm="master") -> str:
        """Create new execution on the flow

        :param execution: name of execution to create
        :param flowAlias: name of the parent flow
        :return: HTTPResponse object on success
        """
        try:
            newExec = {}
            newExec["provider"] = provider
            # doesn't work
            # newExec["requirement"] = execution["requirement"]
            response = open_url(
                URL_AUTHENTICATION_FLOW_EXECUTIONS_EXECUTION.format(
                    url=self.baseurl, realm=realm, flowalias=quote(flowAlias)
                ),
                method="POST",
                http_agent=self.http_agent,
                headers=self.restheaders,
                data=json.dumps(newExec),
                timeout=self.connection_timeout,
                validate_certs=self.validate_certs,
            )
            location = response.getheader("location")
            if location is None:
                raise Exception(
                    f"Creating execution with provider {provider} below {flowAlias} didn't return a location header containing id"
                )
            last_slash = location.rfind("/")
            if last_slash == -1:
                raise Exception(f"location {location} is expected to contain a slash?!")
            id = location[last_slash + 1 :]
            # check validity of uuid
            uuid.UUID(id)
            return id
        except Exception as e:
            self.module.fail_json(
                msg="Unable to create new execution %s: %s" % (provider, str(e))
            )


def extract_groups_check_execution(executions):
    return next(
        filter(
            lambda execution: "providerId" in execution
            and execution["providerId"] == "require-group-membership",
            executions,
        ),
        None,
    )


def run_module():
    argument_spec = keycloak_argument_spec()

    meta_args = dict(
        realm=dict(type="str", default="master"),
        flow=dict(type="str", required=True),
        subflow=dict(type="str"),
        groupchecksflow=dict(type="str"),
        required_groups_from_parent_realm=dict(type="list", elements="str", default=[]),
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
    flowalias = module.params.get("flow")
    subflowalias = module.params.get("subflow") or flowalias
    groupchecksalias = (
        module.params.get("groupchecksflow") or f"{flowalias}-groupchecks"
    )
    required_groups_from_parent_realm = (
        module.params.get("required_groups_from_parent_realm") or []
    )

    kc = KeycloakAPIExt(module, connection_header)
    flow = kc.get_authentication_flow_by_alias(flowalias, realm)
    if len(flow.keys()) == 0:
        module.fail_json(msg=f"flow {flowalias} not found")

    executions = kc.get_executions_representation({"alias": subflowalias}, realm)
    groupchecks_execution = extract_groups_check_execution(executions)

    if len(required_groups_from_parent_realm) == 0:
        if groupchecks_execution is not None:
            kc.delete_execution(groupchecks_execution["id"], realm)

            result["changed"] = True
            result["msg"] = "groupchecks execution has been deleted"
        module.exit_json(**result)

    # there are some required_groups_from_parent_realm
    msgs = []
    # first check if we need to create the subflow
    if groupchecks_execution is None:
        kc.create_execution_ext("require-group-membership", subflowalias, realm)
        msgs.append("groupchecks execution has been created")
        executions = kc.get_executions_representation({"alias": subflowalias}, realm)
        groupchecks_execution = extract_groups_check_execution(executions)

    kc.add_authenticationConfig_to_execution(
        groupchecks_execution["id"],
        {
            "alias": groupchecksalias,
            "config": {"groups": ",".join(required_groups_from_parent_realm)},
        },
        realm,
    )

    # not possible to find out if something changed
    kc.update_authentication_executions(
        flowalias, {"id": groupchecks_execution["id"], "requirement": "REQUIRED"}, realm
    )

    if len(msgs) > 0:
        result["changed"] = True
        result["msg"] = ",".join(msgs)

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
