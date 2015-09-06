%global with_python3 1

%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:           python-iniparse
Version:        0.4
Release:        17%{?dist}
Summary:        Python Module for Accessing and Modifying Configuration Data in INI files
Summary(zh_CN.UTF-8): 访问和修改 INI 文件中的配置数据的 Python 模块
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        MIT and Python
URL:            http://code.google.com/p/iniparse/
Source0:        http://iniparse.googlecode.com/files/iniparse-%{version}.tar.gz
Patch0:         fix-issue-28.patch
# The patch upstream (http://code.google.com/p/iniparse/issues/detail?id=22)
# is Python3-only. The patch below uses python-six to create a version that works
# with both Python major versions and is more error-prone.
Patch1:         %{name}-python3-compat.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-setuptools
BuildRequires:  python-six
BuildRequires:  python2-devel
BuildRequires:  python-test

Requires:       python-six

%if 0%{?with_python3}
BuildRequires:  python3-setuptools
BuildRequires:  python3-six
BuildRequires:  python3-devel
BuildRequires:  python3-test
%endif

BuildArch: noarch

%description
iniparse is an INI parser for Python which is API compatible
with the standard library's ConfigParser, preserves structure of INI
files (order of sections & options, indentation, comments, and blank
lines are preserved when data is updated), and is more convenient to
use.
%description -l zh_CN.UTF-8
访问和修改 INI 文件中的配置数据的 Python 模块。

%if 0%{?with_python3}
%package -n python3-iniparse
Summary:        Python 3 Module for Accessing and Modifying Configuration Data in INI files
Summary(zh_CN.UTF-8): 访问和修改 INI 文件中的配置数据的 Python3 模块
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       python3-six

%description -n python3-iniparse
iniparse is an INI parser for Python 3 which is API compatible
with the standard library's configparser, preserves structure of INI
files (order of sections & options, indentation, comments, and blank
lines are preserved when data is updated), and is more convenient to
use.
%description -n python3-iniparse -l zh_CN.UTF-8
访问和修改 INI 文件中的配置数据的 Python3 模块。
%endif

%prep
%setup -q -n iniparse-%{version}
%patch0 -p1
%patch1 -p0
chmod -c -x html/index.html


%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
mv $RPM_BUILD_ROOT/usr/share/doc/iniparse-%{version} $RPM_BUILD_ROOT/%{_docdir}/python3-iniparse
popd
%endif


%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
mv $RPM_BUILD_ROOT/usr/share/doc/iniparse-%{version} $RPM_BUILD_ROOT%{_pkgdocdir}

# Don't dupe the license
rm -rf $RPM_BUILD_ROOT%{_pkgdocdir}/LICENSE*
rm -rf $RPM_BUILD_ROOT%{_docdir}/python3-iniparse/LICENSE*
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%check
%{__python2} runtests.py

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} runtests.py
popd
%endif

%files
%defattr(-,root,root,-)
%doc %{_pkgdocdir}
%{!?_licensedir:%global license %%doc}
%license LICENSE LICENSE-PSF
%{python_sitelib}/*

%if 0%{?with_python3}
%files -n python3-iniparse
%defattr(-,root,root,-)
%doc %{_docdir}/python3-iniparse
%{!?_licensedir:%global license %%doc}
%license LICENSE LICENSE-PSF
%{python3_sitelib}/*
%endif


%changelog
* Sun Sep 06 2015 Liu Di <liudidi@gmail.com> - 0.4-17
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jul 31 2014 Tom Callaway <spot@fedoraproject.org> - 0.4-15
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.4-13
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Fri Mar 07 2014 Tim Lauridsen <timlau@fedoraproject.org> - 0.4-12
- added python3-test to buildreq for python3 
- run unittest with python3 also

* Fri Mar 07 2014 Tim Lauridsen <timlau@fedoraproject.org> - 0.4-11
- added python-test to buildreq, for unittests

* Fri Mar 07 2014 Tim Lauridsen <timlau@fedoraproject.org> - 0.4-10
- added %%check to run unittests when build
- updated fix-issue-28.patch, so test cases dont fail

* Fri Sep 20 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.4-9
- Introduce python3 subpackage.
- Use %%__python2 instead of %%__python.

* Mon Jul 29 2013 Ville Skyttä <ville.skytta@iki.fi> - 0.4-8
- Install docs to %%{_pkgdocdir} where available.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-6
- fix for upstream issue 28

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild


* Sat Nov 7 2009 Tim Lauridsen <timlau@fedoraproject.org> - 0.4-1
- Release 0.4

* Sat Nov 7 2009 Tim Lauridsen <timlau@fedoraproject.org> - 0.3.1-2
- removed patch

* Sat Nov 7 2009 Tim Lauridsen <timlau@fedoraproject.org> - 0.3.1-1
- Release 0.3.1
-   Fix empty-line handling bugs introduced in 0.3.0 

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 2 2009 Tim Lauridsen <timlau@fedoraproject.org> - 0.3.0-2
- added patch from upstream to fix regrestion :

* Sat Feb 28 2009 Tim Lauridsen <timlau@fedoraproject.org> - 0.3.0-1
- Release 0.3.0
-  Fix handling of continuation lines
-  Fix DEFAULT handling
-  Fix picking/unpickling 

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Dec 7 2008 Tim Lauridsen <timlau@fedoraproject.org> - 0.2.4-1
- Release 0.2.4:
-   Updated to work with Python-2.6 (Python-2.4 and 2.5 are still supported)
-   Support for files opened in unicode mode
-   Fixed Python-3.0 compatibility warnings
-   Minor API cleanup 
* Fri Nov 28 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.2.3-5
- Rebuild for Python 2.6
* Tue Jan 8 2008 Tim Lauridsen <timlau@fedoraproject.org> - 0.2.3-4
- own the %%{_docdir}/python-iniparse-%{version} directory
* Tue Dec 11 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.2.3-3
- handle egg-info too
* Tue Dec 11 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.2.3-2
- removed patch source line
* Tue Dec 11 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.2.3-1
- Updates to release 0.2.3
- removed empty ini file patch, it is included in 0.2.3
* Mon Nov 19 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.2.2-2
- Added upstream patch to fix problems with empty ini files.
* Tue Sep 25 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.2.2-1
- Updated to release 0.2.2
- removed patch to to fix problems with out commented lines, included in upstream source
* Wed Sep 12 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.2.1-4
- Added some logic to get the right python-setuptools buildrequeres
- based on the fedora version, to make the same spec file useful in
- all fedora releases.
* Mon Sep 10 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.2.1-3
- Added patch from upstream svn to fix problems with out commented lines.
* Tue Aug 28 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.2.1-2
- Changed BuildRequires python-setuptools to python-setuptools-devel
* Tue Aug 7 2007 Paramjit Oberoi <param@cs.wisc.edu> - 0.2.1-1
- Release 0.2.1
* Fri Jul 27 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.2-3
- relocated doc to %{_docdir}/python-iniparse-%{version}
* Thu Jul 26 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.2-2
- changed name from iniparse to python-iniparse
* Tue Jul 17 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.2-1
- Release 0.2
- Added html/* to %%doc
* Fri Jul 13 2007 Tim Lauridsen <timlau@fedoraproject.org> - 0.1-1
- Initial build.
