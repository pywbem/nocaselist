%global srcname nocaselist

Name:           python-%{srcname}
Version:        1.0.4
Release:        1%{?dist}
Summary:        A case-insensitive list for Python

License:        ASL 2.0
URL:            https://github.com/pywbem/nocaselist
Source0:        %{pypi_source}
BuildArch:      noarch

%global _description %{expand:
Python class 'NocaseList' is a case-insensitive list that preserves the
lexical case of its items.

It supports the functionality of the built-in 'list' class of Python 3.8 on
all Python versions it supports (except for being case-insensitive, of course).
This includes the 'clear()' and 'copy()' methods added in Python 3.3 to the
built-in 'list' class.}

%description %{_description}

%package -n python%{python3_pkgversion}-%{srcname}
Summary:        %{summary}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
# Test deps
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  python%{python3_pkgversion}-six

%description -n python%{python3_pkgversion}-%{srcname} %{_description}

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install

%check
%{python3} setup.py test

%files -n python%{python3_pkgversion}-%{srcname}
%license LICENSE
%doc README.md
%{python3_sitelib}/%{srcname}*.egg-info/
%{python3_sitelib}/%{srcname}/

%changelog
* Sat Jul 17 2021 Andreas Maier <andreas.r.maier@gmx.de> 1.0.4-1
- Bumped version to 1.0.4
- Removed duplicate BuildRequires statements
- Changed Python package references to use python3_pkgversion

* Thu Sep 17 2020 Andreas Maier <andreas.r.maier@gmx.de> 1.0.2-1
- Initial packaging for package review
