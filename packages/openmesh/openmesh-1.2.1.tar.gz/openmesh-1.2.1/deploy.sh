#!/bin/bash

# usage:
#   ./deploy.sh [revision]
#
# revision: tag, branch name, or commit to publish. Default is 'master'

revision=${1:-master}

for name in "deploy-sdist" "deploy-3.9-macos-m1" "deploy-3.9-macos" "deploy-3.9-linux" "deploy-3.9-VS2017"
do
  wget "https://gitlab.vci.rwth-aachen.de:9000/OpenMesh/openmesh-python/-/jobs/artifacts/$revision/download?job=$name" -O "$name.zip"
  unzip "$name.zip"
  rm -f "$name.zip"
done

(
cd release
for name in $(find -type f -name "*-linux_*.whl")
do
  echo $name
  newname="$(echo $name | sed -e 's/-linux_/-manylinux1_/')";
  mv $name $newname
done

twine upload *.tar.gz
twine upload *.whl
)
