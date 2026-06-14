#!/bin/bash
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd $SCRIPT_DIR/..

echo "Removing caven"
yes | sudo apt remove caven || echo "Caven was not installed"

echo "Installing caven from debian package"
./build_debian_package.sh
sudo dpkg -i caven_1.0.0_all.deb

echo "Creating and activating env"
rm -rf .caven_env
caven env -p .
source .caven_env/activate

echo "Installing module with dependencies"
caven install -s ./tst/calculator

echo "Uninstalling module" 
caven install -u my_module

echo "Install something from GH"
caven install -s gh:AntonioRamalho96/caven_my_module

echo "Delete created env"
source .caven_env/deactivate
rm -rf .caven_env