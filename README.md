The following python packages must be installed:

* pip3 install netaddr
* pip3 install jmespath

```
git clone -b development --recursive git@gitlab.com:idcohorts/rps/research-project-suite.git rps-dev
cd rps-dev
ansible-playbook -i environments/local/all.yaml
```

work with git submodules:
```
git submodule init
git submodule update
git submodule foreach git checkout master
```

execute ansible playbooks:
```
ansible-playbook -i environments/test/ containers.yaml
```
