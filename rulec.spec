%global debug_package %{nil}

Name:           python-rulec
Version:        0.3.2
Release:        1%{?dist}
Summary:        Rule compiler example project

License:        GPLv3
URL:            https://github.com/jw3/example-python-rust-copr
Source:         %{url}/archive/v%{version}/rulec-%{version}.tar.gz

BuildArch:      x86_64
BuildRequires:  python3-devel
BuildRequires:  python3dist(wheel)
BuildRequires:  python3dist(setuptools-rust)
BuildRequires:  python3dist(tox-current-env)

BuildRequires:  rust-packaging
BuildRequires: rust-autocfg-devel
BuildRequires: rust-bitflags-devel
BuildRequires: rust-byteorder-devel
BuildRequires: rust-cc-devel
BuildRequires: rust-cfg-if-devel
BuildRequires: rust-instant-devel
BuildRequires: rust-libc-devel
BuildRequires: rust-lock_api-devel
BuildRequires: rust-once_cell-devel
BuildRequires: rust-pkg-config-devel
BuildRequires: rust-proc-macro-hack-devel
BuildRequires: rust-proc-macro2-devel
BuildRequires: rust-pyo3-devel
BuildRequires: rust-pyo3-build-config-devel
BuildRequires: rust-pyo3-macros-devel
BuildRequires: rust-pyo3-macros-backend-devel
BuildRequires: rust-quote-devel
BuildRequires: rust-scopeguard-devel
BuildRequires: rust-smallvec-devel
BuildRequires: rust-syn-devel
BuildRequires: rust-unicode-ident-devel
BuildRequires: rust-unindent-devel
BuildRequires: rust-yansi-devel
Source1: %{crates_source ariadne 0.1.5}
Source4: %{crates_source lmdb-rkv 0.14.0}
Source5: %{crates_source lmdb-rkv-sys 0.11.2}
Source6: %{crates_source parking_lot 0.11.2}
Source7: %{crates_source parking_lot_core 0.8.5}
Source10: %{crates_source redox_syscall 0.2.16}
Source11: %{crates_source winapi 0.3.9}
Source12: %{crates_source winapi-i686-pc-windows-gnu 0.4.0}
Source13: %{crates_source winapi-x86_64-pc-windows-gnu 0.4.0}
# Overridden to rpms due to Fedora version patching
BuildRequires: rust-paste-devel
BuildRequires: rust-indoc-devel

%global _description %{expand:
                           Rule compiler for fapolicyd.}

%description %_description

%package -n python3-rulec
Summary:        %{summary}

%description -n python3-rulec %_description

%prep
mkdir -p %{cargo_registry}
for c in %{_sourcedir}/*.crate; do tar xzf ${c} -C %{cargo_registry}; done
for d in %{cargo_registry}/*; do echo '{"files":{},"package":""}' > "$d/.cargo-checksum.json"; done

%cargo_prep
%autosetup -p1 -n example-python-rust-copr-%{version}
rm Cargo.lock

%generate_buildrequires
%pyproject_buildrequires

%build
export VERSION=%{version}
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files rulec

%check

%files -n python3-rulec -f %{pyproject_files}

%doc README.md

%changelog
