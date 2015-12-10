%global with_python3 1

%global reqs() %1-idna >= 2.0 %1-pyasn1 %1-six >= 1.4.1 %1-cffi >= 0.8
%global breqs() %1-setuptools %1-pretend %1-iso8601 %1-cryptography-vectors = %{version}

Name:           python-cryptography
Version:	1.1
Release:	3%{?dist}
Summary:        PyCA's cryptography library
Summary(zh_CN.UTF-8): PyCA 的加密库

Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        ASL 2.0 or BSD
URL:            https://cryptography.io/en/latest/
Source0:        https://pypi.python.org/packages/source/c/cryptography/cryptography-%{version}.tar.gz

BuildRequires:  openssl-devel
Requires:       openssl

BuildRequires:  python2-devel
BuildRequires:  pytest %breqs python
BuildRequires:  python-enum34 python-ipaddress %reqs python
Requires:       python-enum34 python-ipaddress %reqs python

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-pytest %breqs python3
BuildRequires:  %reqs python3
%endif


%description
cryptography is a package designed to expose cryptographic primitives and
recipes to Python developers.

%description -l zh_CN.UTF-8
PyCA 的加密库。

%if 0%{?with_python3}
%package -n  python3-cryptography
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Summary:        PyCA's cryptography library
Summary(zh_CN.UTF-8): PyCA 的加密库（Python3）

Requires:       openssl
Requires:       %reqs python3

%description -n python3-cryptography
cryptography is a package designed to expose cryptographic primitives and
recipes to Python developers.
%description -n python3-cryptography -l zh_CN.UTF-8
PyCA 的加密库（Python3）。
%endif

%prep
%setup -q -n cryptography-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!/usr/bin/python|#!%{__python3}|'
%endif

%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif


%install
# Actually other *.c and *.h are appropriate
# see https://github.com/pyca/cryptography/issues/1463
find . -name .keep -print -delete

%{__python2} setup.py install --skip-build --prefix=%{_prefix} --root %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --prefix=%{_prefix} --root %{buildroot}
popd
%endif
magic_rpm_clean.sh

%check
%{__python} setup.py test

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif


%files
%doc LICENSE LICENSE.APACHE LICENSE.BSD README.rst docs
%{python_sitearch}/*


%if 0%{?with_python3}
%files -n python3-cryptography
%doc LICENSE LICENSE.APACHE LICENSE.BSD README.rst docs
%{python3_sitearch}/*
%endif


%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.1-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.1-2
- 更新到 1.1

* Sun Aug 23 2015 Liu Di <liudidi@gmail.com> - 1.0-3
- 为 Magic 3.0 重建

* Sun Aug 16 2015 Liu Di <liudidi@gmail.com> - 1.0-2
- 为 Magic 3.0 重建

* Wed Aug 12 2015 Nathaniel McCallum <npmccallum@redhat.com> - 1.0-1
- New upstream release

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 14 2015 Nathaniel McCallum <npmccallum@redhat.com> - 0.9-1
- New upstream release
- Run tests on RHEL
- New deps: python-idna, python-ipaddress

* Fri Apr 17 2015 Nathaniel McCallum <npmccallum@redhat.com> - 0.8.2-1
- New upstream release
- Add python3-pyasn1 Requires (#1211073)

* Tue Apr 14 2015 Matej Cepl <mcepl@redhat.com> - 0.8-2
- Add python-pyasn1 Requires (#1211073)

* Fri Mar 13 2015 Nathaniel McCallum <npmccallum@redhat.com> - 0.8-1
- New upstream release
- Remove upstreamed patch

* Wed Mar 04 2015 Nathaniel McCallum <npmccallum@redhat.com> - 0.7.2-2
- Add python3-cryptography-vectors build requires
- Add python-enum34 requires

* Tue Feb 03 2015 Nathaniel McCallum <npmccallum@redhat.com> - 0.7.2-1
- New upstream release. BSD is now an optional license.
- Fix test running on python3
- Add upstream patch to fix test paths

* Fri Nov 07 2014 Matej Cepl <mcepl@redhat.com> - 0.6.1-2
- Fix requires, for reasons why other development files were not
  eliminated see https://github.com/pyca/cryptography/issues/1463.

* Wed Nov 05 2014 Matej Cepl <mcepl@redhat.com> - 0.6.1-1
- New upstream release.

* Sun Jun 29 2014 Terry Chia <terrycwk1994@gmail.com> 0.4-1
- initial version
