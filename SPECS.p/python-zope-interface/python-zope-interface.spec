# Filter private shared library provides
%filter_provides_in %{python_sitearch}/zope/interface/.*\.so$
%filter_setup

Name:		python-zope-interface
Version:	3.7.0
Release:	2%{?dist}
Summary:	Zope 3 Interface Infrastructure
Group:		Development/Libraries
License:	ZPLv2.1
URL:		http://pypi.python.org/pypi/zope.interface
Source0:	http://pypi.python.org/packages/source/z/zope.interface/zope.interface-%{version}.tar.gz
BuildRequires:	python2-devel
BuildRequires:	python-setuptools
# since F14
Obsoletes:	python-zope-filesystem <= 1-8

%description
Interfaces are a mechanism for labeling objects as conforming to a given API
or contract.

This is a separate distribution of the zope.interface package used in Zope 3.

%prep
%setup -n zope.interface-%{version} -q

%build
CFLAGS="%{optflags}" %{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root  %{buildroot}

# Will put docs in %%{_docdir} instead
%{__rm} -f %{buildroot}%{python_sitearch}/zope/interface/{,tests/}*.txt

# C files don't need to be packaged
%{__rm} -f %{buildroot}%{python_sitearch}/zope/interface/_zope_interface_coptimizations.c

# deal with documentation
%{__mkdir_p} %{buildroot}%{_docdir}/%{name}-%{version}/
%{__cp} -p src/zope/interface/*.txt src/zope/interface/tests/*.txt \
		%{buildroot}%{_docdir}/%{name}-%{version}
%{__mv} %{buildroot}%{_docdir}/%{name}-%{version}/README{,-development}.txt
%{__cp} -p CHANGES.txt COPYRIGHT.txt LICENSE.txt README.txt \
		%{buildroot}%{_docdir}/%{name}-%{version}/


%check

%files
%defattr(-,root,root,-)
%{_docdir}/%{name}-%{version}/
%{python_sitearch}/zope/interface/
# Co-own %%{python_sitearch}/zope/
%dir %{python_sitearch}/zope/
%exclude %{python_sitearch}/zope/interface/tests/
%exclude %{python_sitearch}/zope/interface/common/tests/
%{python_sitearch}/zope.interface-*.egg-info
%{python_sitearch}/zope.interface-*-nspkg.pth

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 3.7.0-2
- 为 Magic 3.0 重建

* Sat Jan  7 2012 Robin Lee <cheeselee@fedoraproject.org> - 3.7.0-1
- Update to 3.7.0 (ZTK 1.1.3)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct  4 2010 Robin Lee <cheeselee@fedoraproject.org> - 3.6.1-7
- Obsoletes python-zope-filesystem

* Wed Sep 29 2010 jkeating - 3.6.1-6
- Rebuilt for gcc bug 634757

* Sun Sep 19 2010 Robin Lee <robinlee.sysu@gmail.com> - 3.6.1-5
- Move the texts files to %%doc
- Exclude the tests from installation
- Filter private shared library provides

* Wed Sep 15 2010 Robin Lee <robinlee.sysu@gmail.com> - 3.6.1-4
- Run the test suite
- Don't move the text files

* Tue Aug 31 2010 Robin Lee <robinlee.sysu@gmail.com> - 3.6.1-3
- Remove python-zope-filesystem from requirements
- Own %%{python_sitearch}/zope/
- BR: python-setuptools-devel renamed to python-setuptools
- Spec cleaned up

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 3.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jun 22 2010 Robin Lee <robinlee.sysu@gmail.com> - 3.6.1-1
- update to 3.6.1
- License provided in the source package
- include the tests

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 05 2009 Felix Schwarz <felix.schwarz@oss.schwarz.eu> 3.5.2-1
- update to 3.5.2

* Mon Jun 01 2009 Luke Macken <lmacken@redhat.com> 3.5.1-3
- Add python-setuptools-devel to the BuildRequires, so we generate egg-info

* Sun Apr 05 2009 Felix Schwarz <felix.schwarz@oss.schwarz.eu> 3.5.1-2
- use correct source filename (upstream switched from zip to tar.gz)

* Sun Apr 05 2009 Felix Schwarz <felix.schwarz@oss.schwarz.eu> 3.5.1-1
- update to 3.5.1

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 17 2008 Conrad Meyer <konrad@tylerc.org> - 3.5.0-3
- Make compatible with the new python-zope-filesystem.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 3.5.0-2
- Rebuild for Python 2.6

* Sat Nov 15 2008 Felix Schwarz <felix.schwarz@oss.schwarz.eu> 3.5.0-1
- update to 3.5.0

* Mon Mar 31 2008 Paul Howarth <paul@city-fan.org> 3.4.1-1
- update to 3.4.1
- incorporate suggestions from Felix Schwarz:
  - new summary and description
  - new upstream URL (old one out of date)
  - don't package test files
  - include more documentation

* Mon Mar 31 2008 Paul Howarth <paul@city-fan.org> 3.3.0-1
- update to 3.3.0
- update source URL to include versioned directory and new tarball name
- drop the gcc 4.x compatibility patch, no longer needed
- don't run the test suite as it now depends on zope.testing
- exclude _zope_interface_coptimizations.c source from the binary package

* Thu Feb 14 2008 Paul Howarth <paul@city-fan.org> 3.0.1-10
- rebuild with gcc 4.3.0 for Fedora 9

* Fri Jan  4 2008 Paul Howarth <paul@city-fan.org> 3.0.1-9
- tweak %%files list to pull in egg info file when necessary
- fix permissions on shared objects (silence rpmlint)

* Wed Aug 29 2007 Paul Howarth <paul@city-fan.org> 3.0.1-8
- update license tag to ZPLv2.1 in anticipation of this tag being approved

* Sat Dec  9 2006 Paul Howarth <paul@city-fan.org> 3.0.1-7
- rebuild against python 2.5 for Rawhide

* Tue Oct 31 2006 Paul Howarth <paul@city-fan.org> 3.0.1-6
- add %%check section

* Wed Sep 20 2006 Paul Howarth <paul@city-fan.org> 3.0.1-5
- dispense with %%{pybasever} macro and python-abi dependency, not needed from
  FC4 onwards
- include ZPL 2.1 license text
- add reference in %%description to origin of patch
- change License: tag from "ZPL 2.1" to "Zope Public License" to shut rpmlint up

* Thu Aug 31 2006 Paul Howarth <paul@city-fan.org> 3.0.1-4
- files list simplified as .pyo files are no longer %%ghost-ed

* Tue May  9 2006 Paul Howarth <paul@city-fan.org> 3.0.1-3
- import from PyVault Repository
- rewrite in Fedora Extras style

* Tue Aug 23 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 3.0.1-2
- add bug fix for gcc 4

* Mon Feb 07 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 3.0.1-1
- new rpm

