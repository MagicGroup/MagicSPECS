%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           python-iniparse
Version:        0.4
Release:        5%{?dist}
Summary:        Python Module for Accessing and Modifying Configuration Data in INI files
Group:          Development/Libraries
License:        MIT
URL:            http://code.google.com/p/iniparse/
Source0:        http://iniparse.googlecode.com/files/iniparse-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if 0%{?fedora} >= 8
BuildRequires: python-setuptools-devel
%else
BuildRequires: python-setuptools
%endif

BuildArch: noarch

%description
iniparse is an INI parser for Python which is API compatible
with the standard library's ConfigParser, preserves structure of INI
files (order of sections & options, indentation, comments, and blank
lines are preserved when data is updated), and is more convenient to
use.

%prep
%setup -q -n iniparse-%{version}
 
%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
# fixes
chmod 644 $RPM_BUILD_ROOT//usr/share/doc/iniparse-%{version}/index.html
mv $RPM_BUILD_ROOT/usr/share/doc/iniparse-%{version} $RPM_BUILD_ROOT/usr/share/doc/python-iniparse-%{version}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%dir %{_docdir}/python-iniparse-%{version} 
%doc %{_docdir}/python-iniparse-%{version}/*
%{python_sitelib}/*



%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.4-5
- 为 Magic 3.0 重建

* Mon Jan 23 2012 Liu Di <liudidi@gmail.com> - 0.4-4
- 为 Magic 3.0 重建

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
