%global debug_package %{nil}

Name:           python3-rulec
Version:        0.5.2
Release:        1%{?dist}
Summary:        Rule compiler example project

License:        GPLv3
URL:            https://github.com/jw3/example-python-rust-copr
Source:         %{url}/archive/v%{version}/rulec-%{version}.tar.gz

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
Source1: %{crates_source ariadne 0.1.5}
Source2: %{crates_source arrayvec 0.5.2}
Source3: %{crates_source bitvec 0.19.6}
Source4: %{crates_source fapolicy-rules 0.4.1}
Source7: %{crates_source libc 0.2.132}
Source8: %{crates_source memchr 2.3.4}
Source9: %{crates_source nom 6.2.1}
Source14: %{crates_source radium 0.5.3}
Source15: %{crates_source redox_syscall 0.2.16}
Source16: %{crates_source winapi 0.3.9}
Source17: %{crates_source winapi-i686-pc-windows-gnu 0.4.0}
Source18: %{crates_source winapi-x86_64-pc-windows-gnu 0.4.0}
# Overridden to rpms due to Fedora version patching
BuildRequires: rust-paste-devel
BuildRequires: rust-indoc-devel

%global _description %{expand:
                           Rule compiler for fapolicyd.}

%description %_description


%prep
# create a registry in BUILDROOT that is writable in the prep phase
# is this legal??? i doubt it.
CARGO_REG_DIR=%{buildroot}%{cargo_registry}
%{__mkdir} -p ${CARGO_REG_DIR}

# extract the SourceX crates into the writable registry
for c in %{_sourcedir}/*.crate; do %{__tar} xzf ${c} -C ${CARGO_REG_DIR}; done

# appears we must init the checksum file for the crate source downloads
for d in ${CARGO_REG_DIR}/*; do if [ -d $d ] && [ ! -L $d ]; then echo '{"files":{},"package":""}' > "$d/.cargo-checksum.json"; fi ; done

# link the original registry contents so that the official packages are available too
for d in %{cargo_registry}/*; do ln -sf ${d} ${CARGO_REG_DIR}; done

# use the rust2rpm cargo_prep
%cargo_prep

# now we need to tweak the registry location to BUILDROOT before building
sed -i "s#%{cargo_registry}#${CARGO_REG_DIR}#g" .cargo/config
# we also must fix the shared library after the build by stripping the BUILDROOT
sed -i "/\[build\]/a rustflags = [\"--remap-path-prefix\", \"${CARGO_REG_DIR}=%{cargo_registry}\"]" .cargo/config

%autosetup -p1 -n example-python-rust-copr-%{version}
# get rid of the cargo lock, we will use what is available in the registry
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
