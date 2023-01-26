#!/usr/bin/elvish

var name = $args[0]
var branch = $args[1]
var target = roles/$name
var url = git@gitlab.com:idcohorts/rps/ansible-role-$name.git

git remote add -f import-$name $url
#git branch import-$name
#git checkout import-$name
git merge -s ours --no-commit --allow-unrelated-histories import-$name/$branch
git read-tree --prefix=$target -u import-$name/$branch":"
git commit -m "merge in "$name" role from "$url
