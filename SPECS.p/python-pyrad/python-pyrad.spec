%global pkgname pyrad

Name:		python-pyrad
Version:	2.0
Release:	4%{?dist}
Summary:	Python RADIUS client
Summary(zh_CN.UTF-8): Python RADIUS 客户端
License:	BSD
URL:		https://github.com/wichert/pyrad
Source0:	http://pypi.python.org/packages/source/p/%{pkgname}/%{pkgname}-%{version}.tar.gz
# Cherry-picked from upstream
Patch1:		python-pyrad-0001-Use-a-better-random-generator.patch
BuildRequires:  python2-devel
BuildRequires:	python-nose
BuildRequires:	python-setuptools
BuildRequires:	python-six
BuildRequires:	python-sphinx
Requires:	python-twisted-core
BuildArch:	noarch

%description
pyrad is an implementation of a RADIUS client as described in RFC2865.
It takes care of all the details like building RADIUS packets, sending
them and decoding responses.

%description -l zh_CN.UTF-8
Python RADIUS 客户端。

%prep
%setup -qn %{pkgname}-%{version}
chmod 644 example/acct.py example/auth.py example/server.py
%patch1 -p1 -b .better_rng

%build
%{__python} setup.py build
pushd docs/
make html %{?_smp_mflags}

%install
%{__python} setup.py install --skip-build --root %{buildroot}
magic_rpm_clean.sh

%check
%{__python} setup.py test

%files
%doc CHANGES.txt LICENSE.txt README.rst example docs/.build/html/
%{python_sitelib}/%{pkgname}/
%{python_sitelib}/%{pkgname}-%{version}-*.egg-info/

%changelog
* Tue Sep 08 2015 Liu Di <liudidi@gmail.com> - 2.0-4
- 为 Magic 3.0 重建

* Thu Sep 05 2013 Peter Lemenkov <lemenkov@gmail.com> - 2.0-3
- Better random number generator

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 11 2013 Christopher Meng <rpm@cicku.me> - 2.0-1
- Update to 2.0 version.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Sep  6 2010 Peter Lemenkov <lemenkov@gmail.com> - 1.1-5
- Cleaned up spec-file
- Added %%check section
- Dropped support for fedora > 9

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Apr 11 2009 Peter Lemenkov <lemenkov@gmail.com> - 1.1-2
- Fixed rpmling warning
- Changed 'files' section
- Added missing requires python-twisted-core

* Sat Apr 11 2009 Peter Lemenkov <lemenkov@gmail.com> - 1.1-1
- Initial build

