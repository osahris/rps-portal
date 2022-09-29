# Installation 

## Ansible Installation
/etc/ansible/ansible.cfg
[defaults]
nocows = 1
stdout_callback = yaml
interpreter_python = auto_silent
retry_files_enabled = False
force_handlers = True

library = /usr/share/ansible/library

The following python packages must be installed:

* pip3 install netaddr
* pip3 install jmespath

```
git clone -b development --recursive git@gitlab.com:idcohorts/rps/research-project-suite.git rps-dev
cd rps-dev
ansible-playbook -i environments/local/ all.yaml
```

work with git submodules:
```
git submodule init
git submodule update
git submodule foreach git checkout master
```

execute ansible playbooks:
```
ansible-playbook -i environments/test/ all.yaml
```



```sh
mkdir -p /usr/share/ansible/library/connection_plugins
cd /usr/share/ansible/library/connection_plugins
git clone https://github.com/chifflier/ansible-lxc-ssh.git
```

Very import to have a vault key for all the sweet secrets. Put the Key file {{somewhere_nice}}. ;)

```sh
export ANSIBLE_VAULT_PASSWORD_FILE={{somewhere_nice}}
```


# Deploy Cohort Explorer

Variables for Cohort Explorer in group_vars
- rps_cohort_explorer_server_name: cohort-explorer.{{dns_suffix}}
- rps_cohort_explorer_git_version: main
- rps_cohort_explorer_repo: https://{{ rps_cohort_explorer_deploy_token }}@gitlab.com/idcohorts/cohortexplorer.git
- rps_cohort_explorer_deploy_token: in **secrets**
- reverse_proxy_server_name: container name for **containers.yaml** role
- reverse_proxy_nginx_vhost_custom: nginx config for **containers.yaml** role


```sh
ansible-playbook -i environments/test/ rps_cohort_explorer.yaml 
ansible-playbook -i environments/test/ rps_cohort_explorer.yaml  --limit rps_cohort_explorer
```

Further Cohort-Explorer Deployment-Todos:

- [ ] deploy cohort explorer theme repo
- [ ] deploy cohort explorer structure repo