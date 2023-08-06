# pkman
A python package manager inspired by npm.

## Demo
```shell
mkdir my-demo-package && cd my-demo-package
pkman init
# edit package.json
pkx init-pypkg
# if git repo is configured, bind remote branch on remote repository by
pkx gitops init git@host:username/repo branch
# once you finished updating your code, sync code to remote by
pkx gitops update "update-code"

```