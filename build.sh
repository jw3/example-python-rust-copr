#!/usr/bin/env bash

# ava

spec_file="rulec.spec"

if [[ "$ONLINE" -eq 1 ]]; then
  cd /root/rpmbuild/SOURCES
  spectool -gf "../SPECS/$spec_file"
  cd /root/rpmbuild/SPECS
  dnf builddep "$spec_file" -y
fi

cd /root/rpmbuild/SPECS
rpmbuild -ba "$spec_file"
