# Should not build for Python 3 for Fedora releases that provide
# Python 3.4 (Fedora 22 or higher?).
%global with_python3 1

Name:           python-enum34
Version:        1.0.4
Release:        6%{?dist}
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Summary:        Backport of Python 3.4 Enum
Summary(zh_CN.UTF-8): Pyhton 3.4 Enum 的 Backport
License:        BSD
BuildArch:      noarch
URL:            https://pypi.python.org/pypi/enum34
Source0:        https://pypi.python.org/packages/source/e/enum34/enum34-%{version}.tar.gz

BuildRequires:  python2-devel python-setuptools
%if 0%{?with_python3}
BuildRequires:  python3-devel python3-setuptools
%endif # if with_python3

%description
Python 3.4 introduced official support for enumerations.  This is a
backport of that feature to Python 3.3, 3.2, 3.1, 2.7, 2.5, 2.5, and 2.4.

An enumeration is a set of symbolic names (members) bound to unique,
constant values. Within an enumeration, the members can be compared by
identity, and the enumeration itself can be iterated over.

This module defines two enumeration classes that can be used to define
unique sets of names and values: Enum and IntEnum. It also defines one
decorator, unique, that ensures only unique member names are present
in an enumeration.

%description -l zh_CN.UTF-8
Pyhton 3.4 Enum 的 Backport。

%if 0%{?with_python3}
%package -n python3-enum34
Summary:        Backport of Python 3.4 Enum
Summary(zh_CN.UTF-8): Pyhton 3.4 Enum 的 Backport
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库

%description -n python3-enum34
Python 3.4 introduced official support for enumerations.  This is a
backport of that feature to Python 3.3, 3.2, 3.1, 2.7, 2.5, 2.5, and 2.4.

An enumeration is a set of symbolic names (members) bound to unique,
constant values. Within an enumeration, the members can be compared by
identity, and the enumeration itself can be iterated over.

This module defines two enumeration classes that can be used to define
unique sets of names and values: Enum and IntEnum. It also defines one
decorator, unique, that ensures only unique member names are present
in an enumeration.

%description -n python3-enum34 -l zh_CN.UTF-8
Pyhton 3.4 Enum 的 Backport。
%endif # with_python3

%prep
%setup -q -n enum34-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%{__python2} setup.py build

%check
pushd %{buildroot}/%{python2_sitelib}
%{__python2} enum/test_enum.py
popd
%if 0%{?with_python3}
pushd %{buildroot}/%{python3_sitelib}
%{__python3} enum/test_enum.py
popd
%endif # with_python3

%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
# remove docs from sitelib, we'll put them in doc dir instead
rm -rf %{buildroot}%{python3_sitelib}/enum/{LICENSE,README,doc}
popd
%endif # with_python3
%{__python2} setup.py install --skip-build --root %{buildroot}
# remove docs from sitelib, we'll put them in doc dir instead
rm -rf %{buildroot}%{python2_sitelib}/enum/{LICENSE,README,doc}
magic_rpm_clean.sh

%files
%doc PKG-INFO enum/LICENSE enum/README enum/doc/enum.rst
%{python2_sitelib}/*

%if 0%{?with_python3}
%files -n python3-enum34
%doc PKG-INFO enum/LICENSE enum/README enum/doc/enum.rst
%{python3_sitelib}/*
%endif # with_python3

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.0.4-6
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.0.4-5
- 为 Magic 3.0 重建

* Wed Sep 02 2015 Liu Di <liudidi@gmail.com> - 1.0.4-4
- 为 Magic 3.0 重建

* Mon Aug 17 2015 Liu Di <liudidi@gmail.com> - 1.0.4-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 08 2015 Eric Smith <brouhaha@fedoraproject.org> 1.0.4-1
- Updated to latest upstream.

* Mon Jul 21 2014 Matěj Cepl <mcepl@redhat.com> - 1.0-4
- No, we don’t have python3 in RHEL-7 :'(

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon May 26 2014 Eric Smith <brouhaha@fedoraproject.org> 1.0-1
- Updated to latest upstream.

* Mon Mar 17 2014 Eric Smith <brouhaha@fedoraproject.org> 0.9.23-1
- Updated to latest upstream.
- Spec updated per review comments (#1033975).

* Sun Nov 24 2013 Eric Smith <brouhaha@fedoraproject.org> 0.9.19-1
- Initial version.
