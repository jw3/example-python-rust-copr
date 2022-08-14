%global debug_package %{nil}

Name:           python-rulec
Version:        0.3.1
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
Source1: %{crates_source ariadne 0.1.5}
Source2: %{crates_source autocfg 1.1.0}
Source3: %{crates_source bitflags 1.3.2}
Source4: %{crates_source byteorder 1.4.3}
Source5: %{crates_source cc 1.0.73}
Source6: %{crates_source cfg-if 1.0.0}
Source7: %{crates_source indoc 0.3.6}
Source8: %{crates_source indoc-impl 0.3.6}
Source9: %{crates_source instant 0.1.12}
Source10: %{crates_source libc 0.2.127}
Source11: %{crates_source lmdb-rkv 0.14.0}
Source12: %{crates_source lmdb-rkv-sys 0.11.2}
Source13: %{crates_source lock_api 0.4.7}
Source14: %{crates_source once_cell 1.13.0}
Source15: %{crates_source parking_lot 0.11.2}
Source16: %{crates_source parking_lot_core 0.8.5}
Source17: %{crates_source paste 0.1.18}
Source18: %{crates_source paste-impl 0.1.18}
Source19: %{crates_source pkg-config 0.3.25}
Source20: %{crates_source proc-macro-hack 0.5.19}
Source21: %{crates_source proc-macro2 1.0.43}
Source22: %{crates_source pyo3 0.15.2}
Source23: %{crates_source pyo3-build-config 0.15.2}
Source24: %{crates_source pyo3-macros 0.15.2}
Source25: %{crates_source pyo3-macros-backend 0.15.2}
Source26: %{crates_source quote 1.0.21}
Source27: %{crates_source redox_syscall 0.2.16}
Source28: %{crates_source scopeguard 1.1.0}
Source29: %{crates_source smallvec 1.9.0}
Source30: %{crates_source syn 1.0.99}
Source31: %{crates_source unicode-ident 1.0.3}
Source32: %{crates_source unindent 0.1.10}
Source33: %{crates_source winapi 0.3.9}
Source34: %{crates_source winapi-i686-pc-windows-gnu 0.4.0}
Source35: %{crates_source winapi-x86_64-pc-windows-gnu 0.4.0}
Source36: %{crates_source yansi 0.5.1}


%global _description %{expand:
                           Rule compiler for fapolicyd.}

%description %_description

%package -n python3-rulec
Summary:        %{summary}

%description -n python3-rulec %_description

%prep
%cargo_prep
mkdir -p %{cargo_registry}
for c in %{_sourcedir}/*.crate; do tar xzf ${c} -C %{cargo_registry}; done
for d in %{cargo_registry}/*; do echo '{"files":{},"package":""}' > "$d/.cargo-checksum.json"; done

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
