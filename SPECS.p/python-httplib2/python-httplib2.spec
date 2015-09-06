%global with_python3 1

%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           python-httplib2
Version:	0.9.1
Release:	2%{?dist}
Summary:        A comprehensive HTTP client library
Summary(zh_CN.UTF-8): 全面的 HTTP 客户端库
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        MIT
URL:            https://pypi.python.org/pypi/httplib2
Source0:        https://pypi.python.org/packages/source/h/httplib2/httplib2-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  python-setuptools-devel
BuildRequires:  python-devel
BuildArch:      noarch

%if 0%{?with_python3}
BuildRequires:  python3-devel
%endif # if with_python3

%description
A comprehensive HTTP client library that supports many features left out of
other HTTP libraries.

%description -l zh_CN.UTF-8
全面的 HTTP 客户端库。

%if 0%{?with_python3}
%package -n python3-httplib2
Summary:        A comprehensive HTTP client library
Summary(zh_CN.UTF-8): 全面的 HTTP 客户端库
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description -n python3-httplib2
A comprehensive HTTP client library that supports many features left out of
other HTTP libraries.
%description -n python3-httplib2 -l zh_CN.UTF-8
全面的 HTTP 客户端库。
%endif # with_python3

%prep
%setup -q -n httplib2-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!/usr/bin/python|#!%{__python3}|'
%endif # with_python3

%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd
%endif # with_python3
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{python_sitelib}/*

%if 0%{?with_python3}
%files -n python3-httplib2
%defattr(-,root,root,-)
%{python3_sitelib}/*
%endif # with_python3

%changelog
* Sun Sep 06 2015 Liu Di <liudidi@gmail.com> - 0.9.1-2
- 为 Magic 3.0 重建

* Sun Sep 06 2015 Liu Di <liudidi@gmail.com> - 0.9.1-1
- 更新到 0.9.1

* Tue Jun 17 2014 Liu Di <liudidi@gmail.com> - 0.6.0-8
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.6.0-7
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Aug 25 2010 Thomas Spura <tomspur@fedoraproject.org> - 0.6.0-4
- rebuild with python3.2
  http://lists.fedoraproject.org/pipermail/devel/2010-August/141368.html

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Apr 20 2010 Tom "spot" Callaway <tcallawa@redhat.com>
- minor spec cleanups
- enable python3 support

* Fri Apr 02 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.6.0-1
- version upgrade (#566721)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.4.0-2
- Rebuild for Python 2.6

* Thu Dec 27 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.4.0-1
- initial version
