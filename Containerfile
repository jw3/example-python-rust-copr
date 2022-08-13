FROM fedora:rawhide AS build-stage

RUN dnf install -y rpm-build rpmdevtools dnf-plugins-core python3-pip nano

RUN mkdir -p /root/rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
COPY rulec.spec /root/rpmbuild/SPECS/

WORKDIR /root/rpmbuild
COPY build.sh .
