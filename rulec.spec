Name:           python-rulec
Version:        0.1.0
Release:        1%{?dist}
Summary:        Rule compiler example project

License:        GPLv3
URL:            https://github.com/jw3/example-python-rust-copr
Source:         %{url}/archive/v%{version}/rulec-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3dist(wheel)
BuildRequires:  python3dist(setuptools-rust)
BuildRequires:  python3dist(setuptools-rust)
BuildRequires:  python3dist(tox-current-env)

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

%build
%pyproject_wheel

%install
%pyproject_install

%pyproject_save_files rulec

%check

%files -n python3-rulec -f %{pyproject_files}
%doc README.md
%{python3_sitelib}/rulec/

%changelog
