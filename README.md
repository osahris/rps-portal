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