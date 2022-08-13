#!/usr/bin/env bash

cd /root/rpmbuild/SOURCES
spectool -gf ../SPECS/rulec.spec
cd /root/rpmbuild/SPECS
dnf builddep rulec.spec -y
rpmbuild -ba rulec.spec
