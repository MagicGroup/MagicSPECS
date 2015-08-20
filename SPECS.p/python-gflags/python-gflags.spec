%global upstream_name gflags

Name:           python-%{upstream_name}
Version:        2.0
Release:        4%{?dist}
Summary:        Commandline flags module for Python

Group:          Development/Languages
License:        BSD
URL:            http://code.google.com/p/python-gflags/
Source0:        http://python-gflags.googlecode.com/files/python-gflags-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools

%description
This project is the python equivalent of google-gflags, a Google commandline
flag implementation for C++. It is intended to be used in situations where a
project wants to mimic the command-line flag handling of a C++ app that uses
google-gflags, or for a Python app that, via swig or some other means, is
linked with a C++ app that uses google-gflags.

The gflags package contains a library that implements commandline flags
processing. As such it's a replacement for getopt(). It has increased
flexibility, including built-in support for Python types, and the ability to
define flags in the source file in which they're used. (This last is its major
difference from OptParse.)

%package -n python3-%{upstream_name}
Summary:        Commandline flags module for Python 3
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python-tools

%description -n python3-%{upstream_name}
This project is the python equivalent of google-gflags, a Google commandline
flag implementation for C++. It is intended to be used in situations where a
project wants to mimic the command-line flag handling of a C++ app that uses
google-gflags, or for a Python app that, via swig or some other means, is
linked with a C++ app that uses google-gflags.

The gflags package contains a library that implements commandline flags
processing. As such it's a replacement for getopt(). It has increased
flexibility, including built-in support for Python types, and the ability to
define flags in the source file in which they're used. (This last is its major
difference from OptParse.)


%prep
%setup -qc
mv %{name}-%{version} python2
sed -i '1s|^#!/usr/bin/env python$|#!%{__python2}|' python2/gflags2man.py
sed -i '/^#!\/usr\/bin\/env python$/,+1 d' python2/gflags*.py
cp -a python2 python3
sed -i '1s|^#!%{__python2}$|#!%{__python3}|' python3/gflags2man.py
2to3 --write --nobackup python3


%build
pushd python2
%{__python2} setup.py build
popd
pushd python3
%{__python3} setup.py build
popd


%install
pushd python3
%{__python3} setup.py install --skip-build --root %{buildroot}
mv %{buildroot}%{_bindir}/gflags2man.py  %{buildroot}%{_bindir}/gflags2man-3
chmod +x %{buildroot}%{_bindir}/gflags2man-3
popd

pushd python2
%{__python2} setup.py install --skip-build --root %{buildroot}
mv %{buildroot}%{_bindir}/gflags2man.py  %{buildroot}%{_bindir}/gflags2man
chmod +x %{buildroot}%{_bindir}/gflags2man
popd


%check
pushd python2
%{__python2} setup.py test
popd

pushd python3
%{__python3} setup.py test
popd


%files
%license python2/COPYING
%doc python2/AUTHORS python2/ChangeLog python2/COPYING python2/README
%{python2_sitelib}/%{upstream_name}.py*
%{python2_sitelib}/%{upstream_name}_validators.py*
%{python2_sitelib}/python_gflags-%{version}-*egg-info
%{_bindir}/gflags2man

%files -n python3-%{upstream_name}
%license python3/COPYING
%doc python3/AUTHORS python3/ChangeLog python3/COPYING python3/README
%{python3_sitelib}/%{upstream_name}.py*
%{python3_sitelib}/%{upstream_name}_validators.py*
%{python3_sitelib}/python_gflags-%{version}-*egg-info
%{python3_sitelib}/__pycache__/*
%{_bindir}/gflags2man-3


%changelog
* Thu Aug 06 2015 Liu Di <liudidi@gmail.com> - 2.0-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr 6 2015 Orion Poplawski <orion@cora.nwra.com> - 2.0-2
- Create python3 package (bug #1209201)

* Mon Apr 6 2015 Orion Poplawski <orion@cora.nwra.com> - 2.0-1
- Update to 2.0

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jul 24 2011 Silas Sewell <silas@sewell.org> - 1.5.1-1
- Update to 1.5.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct 26 2010 Silas Sewell <silas@sewell.ch> - 1.4-2
- Fix non-executable-script error

* Wed Oct 13 2010 Silas Sewell <silas@sewell.ch> - 1.4-1
- Initial package
