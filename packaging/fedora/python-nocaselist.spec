%global srcname nocaselist

Name:           python-%{srcname}
Version:        1.0.2
Release:        1%{?dist}
Summary:        A case-insensitive list for Python

License:        ASL 2.0
URL:            https://github.com/pywbem/nocaselist
Source:         %{pypi_source}

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)

# Test deps
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(six)

%global _description %{expand:
Python class 'NocaseList' is a case-insensitive list that preserves the
lexical case of its items.

It supports the functionality of the built-in 'list' class of Python 3.8 on
all Python versions it supports (except for being case-insensitive, of course).
This includes the 'clear()' and 'copy()' methods added in Python 3.3 to the
built-in 'list' class.}

%description %{_description}

%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)
# Test deps
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(six)

%description -n python3-%{srcname} %_description

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%check
%{python3} setup.py test

%files -n python3-%{srcname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{srcname}*.egg-info/
%{python3_sitelib}/%{srcname}/

%changelog
* Thu Sep 17 2020 Andreas Maier <andreas.r.maier@gmx.de> 1.0.2-1
- Initial packaging
