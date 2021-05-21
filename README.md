```
git clone -b development --recursive git@gitlab.com:idcohorts/rps/research-project-suite.git rps-dev
cd research-project-suite
ansible-playbook -i environments/local/all.yaml
```

work with git submodules:
```
git submodule init
git submodule update
git submodule foreach git checkout master
```
