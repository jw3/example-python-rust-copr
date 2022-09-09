%global debug_package %{nil}

Name:           python3-rulec
Version:        0.6.0
Release:        1%{?dist}
Summary:        Rule compiler example project

License:        GPLv3
URL:            https://github.com/jw3/example-python-rust-copr
# Source0:        %{url}/archive/v%{version}/%{srcname}-%{version}.tar.gz
# Source1:        %{url}/releases/download/v%{version}/crates.tar.gz
Source0:        rulec.tar.gz
Source1:        crates.tar.gz

Requires: python3-configargparse

BuildArch:      x86_64
BuildRequires:  python3-devel
BuildRequires:  python3dist(wheel)
BuildRequires:  python3dist(setuptools-rust)
BuildRequires:  python3dist(tox-current-env)

BuildRequires: rust-packaging
BuildRequires: rust-autocfg-devel
BuildRequires: rust-bitflags-devel
BuildRequires: rust-cfg-if-devel
BuildRequires: rust-funty-devel
BuildRequires: rust-instant-devel
BuildRequires: rust-lexical-core-devel
BuildRequires: rust-lock_api-devel
BuildRequires: rust-once_cell-devel
BuildRequires: rust-proc-macro-hack-devel
BuildRequires: rust-proc-macro2-devel
BuildRequires: rust-pyo3-devel
BuildRequires: rust-pyo3-build-config-devel
BuildRequires: rust-pyo3-macros-devel
BuildRequires: rust-pyo3-macros-backend-devel
BuildRequires: rust-quote-devel
BuildRequires: rust-ryu-devel
BuildRequires: rust-scopeguard-devel
BuildRequires: rust-serde-devel
BuildRequires: rust-serde_derive-devel
BuildRequires: rust-smallvec-devel
BuildRequires: rust-static_assertions-devel
BuildRequires: rust-syn-devel
BuildRequires: rust-tap-devel
BuildRequires: rust-thiserror-devel
BuildRequires: rust-thiserror-impl-devel
BuildRequires: rust-unicode-ident-devel
BuildRequires: rust-unindent-devel
BuildRequires: rust-version_check-devel
BuildRequires: rust-wyz-devel
BuildRequires: rust-yansi-devel
# Overridden to rpms due to Fedora version patching
BuildRequires: rust-paste-devel
BuildRequires: rust-indoc-devel

%global _description %{expand:
                           Rule compiler for fapolicyd.}

%description %_description


%prep
# the registry location is not writable, so we cant extract the vendored crates
# so link the official package registry into the source dir (aka our new registry)
# bit of a hack, but more elegant that previous attempts ;)
CARGO_REG_DIR=%{_sourcedir}/registry
%{__mkdir} -p ${CARGO_REG_DIR}
for d in %{cargo_registry}/*; do ln -sf ${d} ${CARGO_REG_DIR}; done
%{__tar} xzf %{_sourcedir}/crates.tar.gz -C ${CARGO_REG_DIR}

# use the rust2rpm cargo_prep to update our cargo conf
%cargo_prep

# now we need to tweak the registry location to BUILDROOT before building
sed -i "s#%{cargo_registry}#${CARGO_REG_DIR}#g" .cargo/config
# have to undo the tweak in the shared library, otherwise rpm check will balk
sed -i "/\[build\]/a rustflags = [\"--remap-path-prefix\", \"${CARGO_REG_DIR}=%{cargo_registry}\"]" .cargo/config

%autosetup -p0 -n python3-rulec

# get rid of the cargo lock, we will use whatever is available in the registry
rm Cargo.lock

# for setuptools, set the version of the library to the rpm version
echo %{version} > VERSION

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files rulec

%check

%files -n python3-rulec -f %{pyproject_files}

%doc README.md

%changelog
