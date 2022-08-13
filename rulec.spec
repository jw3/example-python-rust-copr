%global debug_package %{nil}

Name:           python-rulec
Version:        0.2.1
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
BuildRequires:  rust-pyo3+default-devel
BuildRequires:  rust-pyo3+abi3-py36-devel

BuildRequires:  rust-packaging

%global _description %{expand:
                           Rule compiler for fapolicyd.}

%description %_description

%package -n python3-rulec
Summary:        %{summary}

%description -n python3-rulec %_description

%prep
touch setup.cfg
%autosetup -p1 -n example-python-rust-copr-%{version}

%generate_buildrequires
%pyproject_buildrequires

%cargo_prep
%cargo_generate_buildrequires

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
