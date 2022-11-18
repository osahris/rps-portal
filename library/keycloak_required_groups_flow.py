#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
import json

__metaclass__ = type

DOCUMENTATION = r"""
---
module: my_test

short_description: This is my test module

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This is my longer description explaining my test module.

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


def extract_groups_check_flow(executions, groupchecks_flowname):
    return next(
        filter(
            lambda execution: "authenticationFlow" in execution
            and execution["authenticationFlow"]
            and "displayName" in execution
            and execution["displayName"] == groupchecks_flowname,
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
        required_groups=dict(type="list", elements="str", default=[]),
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
    groupchecksflowalias = (
        module.params.get("groupchecksflow") or f"{flowalias}-groupchecks"
    )
    required_groups = module.params.get("required_groups") or []

    kc = KeycloakAPIExt(module, connection_header)
    flow = kc.get_authentication_flow_by_alias(flowalias, realm)
    if len(flow.keys()) == 0:
        module.fail_json(msg=f"flow {flowalias} not found")

    executions = kc.get_executions_representation({"alias": subflowalias}, realm)
    groupchecks_flow = extract_groups_check_flow(executions, groupchecksflowalias)

    if len(required_groups) == 0:
        if groupchecks_flow is not None:
            kc.delete_execution(groupchecks_flow["id"], realm)
            result["changed"] = True
            result["msg"] = "groupchecks flow has been deleted"
        module.exit_json(**result)

    # there are some required_groups
    msgs = []
    # first check if we need to create the subflow
    if groupchecks_flow is None:
        groupchecks_flow = kc.create_subflow(
            groupchecksflowalias,
            subflowalias,
            realm,
        )
        msgs.append("groupchecks flow has been created")
        executions = kc.get_executions_representation({"alias": subflowalias}, realm)
        groupchecks_flow = extract_groups_check_flow(executions, groupchecksflowalias)

    # not possible to find out if something changed
    kc.update_authentication_executions(
        flowalias, {"id": groupchecks_flow["id"], "requirement": "REQUIRED"}, realm
    )

    required_group_executions = kc.get_executions_representation(
        {"alias": groupchecksflowalias}, realm
    )
    groupcheck_execution_ids = []
    existing_required_groups = []
    required_groupcheck_names = list(
        map(lambda required_group: required_group + "-groupcheck", required_groups)
    )
    for execution in required_group_executions:
        alias = execution.get("alias", "")
        display_name = execution.get("displayName", "")
        authentication_config = execution.get("authenticationConfig", {})
        required_group_config = authentication_config.get("config")
        configured_group = required_group_config.get("group")
        # this will also delete non completely created require groups steps
        if (
            not alias in required_groupcheck_names
            or display_name != "Require Group"
            or configured_group not in required_groups
        ):
            kc.delete_execution(execution["id"], realm)
            msgs.append(
                f"substep `{alias}` with execution id `{execution['id']}` has been deleted"
            )
        else:
            existing_required_groups.append(configured_group)
            # register id because we need to later make sure everything is required
            groupcheck_execution_ids.append(execution["id"])

    missing_required_groups = filter(
        lambda required_group: required_group not in existing_required_groups,
        required_groups,
    )

    for missing_required_group in missing_required_groups:
        # only possible to specify provider. unable to post alias and requirement right away :|
        execution_id = kc.create_execution_ext(
            "require-group", groupchecksflowalias, realm
        )
        # module.fail_json(
        #     URL_AUTHENTICATION_EXECUTION_CONFIG.format(
        #         url=kc.baseurl, realm=realm, id=execution_id
        #     )
        # )
        kc.add_authenticationConfig_to_execution(
            execution_id,
            {
                "alias": missing_required_group + "-groupcheck",
                "config": {"group": missing_required_group},
            },
            realm,
        )
        groupcheck_execution_ids.append(execution_id)
        msgs.append(
            f"required groupcheck for `{missing_required_group}` has been created"
        )

    for execution_id in groupcheck_execution_ids:
        # not possible to find out if something changed
        kc.update_authentication_executions(
            groupchecksflowalias, {"id": execution_id, "requirement": "REQUIRED"}, realm
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
