FROM fedora:rawhide AS build-stage

RUN dnf install -y rpm-build rpmdevtools dnf-plugins-core python3-pip nano rust-packaging

WORKDIR /root/rpmbuild

RUN mkdir -p {BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
COPY rulec.spec SPECS/
COPY build.sh   ./
