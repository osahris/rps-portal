```
git clone --recursive git@gitlab.com:infektiologie-ukkoeln/research-project-suite/research-project-suite.git research-project-suite
cd research-project-suite
ansible-playbook -i environments/local/all.yaml
```

work with git submodules:
```
git submodule init
git submodule update
git submodule foreach git checkout master
```
