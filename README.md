# Installation 

## Ansible Installation
Install by pip3

````sh
python3 -m pip install --user ansible
```

/etc/ansible/ansible.cfg


> [defaults]
> nocows = 1
> stdout_callback = yaml
> interpreter_python = auto_silent
> retry_files_enabled = False
> force_handlers = True

> library = /usr/share/ansible/library

The following python packages must be installed:

* pip3 install netaddr
* pip3 install jmespath

```sh
git clone -b development --recursive git@gitlab.com:idcohorts/rps/research-project-suite.git rps-dev
cd rps-dev
ansible-playbook -i environments/local/ all.yaml
```

work with git submodules:
```sh
git submodule init
git submodule update
git submodule foreach git checkout master
```

execute ansible playbooks:
```sh
ansible-playbook -i environments/test/ all.yaml
```


Please note, you have to add the connection_plugins for LXC Reverse Proxy to work.


```sh
mkdir -p /usr/share/ansible/library/connection_plugins
cd /usr/share/ansible/library/connection_plugins
git clone https://github.com/chifflier/ansible-lxc-ssh.git
```

Very import to have a vault key for all the sweet secrets. Put the Key file {{somewhere_nice}}. ;)

```sh
export ANSIBLE_VAULT_PASSWORD_FILE={{somewhere_nice}}
```

# Usage

## Initialize connection
Befor start with a new project, please execute the following to initialize the connection to the reverse proxy:
```sh
ansible-playbook -i rps-{{project_name}}/inventory/ rps-dev/rps_header_servers.yaml --limit rps_header_servers
```

# Deploy the header
Hints:
- you can change the git branch by setting the header_version in the group_var

```sh
ansible-playbook -i rps-{{project_name}}/inventory/ rps-dev/containers.yaml
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
