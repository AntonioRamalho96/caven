#!/bin/sh
set -e

rm -rf pkg
mkdir -p pkg/usr/bin
mkdir -p pkg/usr/lib/python3/dist-packages/caven_lib
mkdir -p pkg/DEBIAN

cp -r caven_lib/*.py caven_lib/*.yaml pkg/usr/lib/python3/dist-packages/caven_lib/
cp caven pkg/usr/bin

chmod 755 pkg/usr/bin/caven

cat > pkg/DEBIAN/control <<'EOF'
Package: caven
Version: 1.0.0
Architecture: all
Maintainer: Antonio Ramalho <antonio.ramalho84@gmail.com>
Depends: python3
Description: Caven C/C++ module manager
 A user friendly way to install and use C/C++ code
EOF

cat > pkg/DEBIAN/prerm <<'EOF'
#!/bin/sh
rm -rf /usr/lib/python3/dist-packages/caven_lib/__pycache__
EOF
chmod 755 pkg/DEBIAN/prerm

dpkg-deb --build pkg caven_1.0.0_all.deb