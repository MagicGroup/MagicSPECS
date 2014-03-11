%if !(0%{?rhel} >= 6 || 0%{?fedora} >= 13)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%endif

Name:           python-configobj
Version:        4.7.2
Release:        4%{?dist}
Summary:        Config file reading, writing, and validation

Group:          System Environment/Libraries
License:        BSD
URL:            http://www.voidspace.org.uk/python/configobj.html
Source0:        http://www.voidspace.org.uk/downloads/configobj-%{version}.zip
Patch0:         configobj-import-all-fix.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires: python-devel

%description
ConfigObj is a simple but powerful config file reader and writer: an ini file
round tripper. Its main feature is that it is very easy to use, with a
straightforward programmer's interface and a simple syntax for config files. 
It has lots of other features though:
    * Nested sections (subsections), to any level
    * List values
    * Multiple line values
    * String interpolation (substitution)
    * Integrated with a powerful validation system
          o including automatic type checking/conversion
          o repeated sections
          o and allowing default values
    * All comments in the file are preserved
    * The order of keys/sections is preserved
    * No external dependencies
    * Full Unicode support
    * A powerful unrepr mode for storing basic datatypes


%prep
%setup -q -n configobj-%{version}
%patch0 -p1 -b .all

%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --skip-build --root=$RPM_BUILD_ROOT

%check
export PYTHONPATH="%{buildroot}/%{python_sitelib}"
%{__python} tests/test_configobj.py

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc docs/*
%{python_sitelib}/*

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 4.7.2-4
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 4.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jun 17 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 4.7.2-1
- Fix traceback when doing from validate import *
- Upstream bugfix release

* Wed Jan 20 2010 Luke Macken <lmacken@redhat.com> - 4.7.0-2
- Merge a bunch of changes from Gareth Armstrong <gareth.armstrong@hp.com>
    - The src zip file should come either from http://www.voidspace.org.uk/
      downloads/ or http://code.google.com/p/configobj/ as the PyPI tarball is
      not complete.  No docs and no test code.
    - Added docs
    - Remove BR on python-setuptools-devel

* Sun Jan 10 2010 Luke Macken <lmacken@redhat.com> - 4.7.0-1
- Update to 4.7.0

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May  7 2009 Yaakov M. Nemoy <ynemoy@fedoraproject.org> - 4.6.0-1
- updated to latest upstream

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 09 2009 Luke Macken <lmacken@redhat.com> - 4.5.3-4
- Conditionally include the egg-info, when available (#478417)

* Mon Dec 1 2008 Toshio Kuratomi <toshio@fedoraproject.org> - 4.5.3-3
- Upload Source file so this actually builds.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 4.5.3-2
- Rebuild for Python 2.6

* Sat Jun 28 2008 Luke Macken <lmacken@redhat.com> - 4.5.3-1
- Update to 4.5.3

* Thu Feb 28 2008 Luke Macken <lmacken@redhat.com> - 4.5.2-1
- Update to 4.5.2

* Sun Sep  2 2007 Luke Macken <lmacken@redhat.com> - 4.4.0-2
- Update for python-setuptools changes in rawhide

* Sat Mar  3 2007 Luke Macken <lmacken@redhat.com> - 4.4.0-1
- 4.4.0

* Sat Dec  9 2006 Luke Macken <lmacken@redhat.com> - 4.3.2-6
- Rebuild for python 2.5

* Sun Sep  3 2006 Luke Macken <lmacken@redhat.com> - 4.3.2-5
- Fix dist tag

* Sun Sep  3 2006 Luke Macken <lmacken@redhat.com> - 4.3.2-4
- Rebuild for FC6

* Mon Aug 14 2006 Luke Macken <lmacken@redhat.com> - 4.3.2-3
- Include pyo files

* Tue Jul 18 2006 Luke Macken <lmacken@redhat.com> - 4.3.2-2
- Fix typo in the url

* Mon Jul 10 2006 Luke Macken <lmacken@redhat.com> - 4.3.2-1
- Initial package
