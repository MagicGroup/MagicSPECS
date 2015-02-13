### Abstract ###

Name: python-ldap
Version: 2.4.17
Release: 1%{?dist}
Epoch: 0
License: Python
Group: System Environment/Libraries
Summary: An object-oriented API to access LDAP directory servers
URL: http://python-ldap.sourceforge.net/
Source0: http://pypi.python.org/packages/source/p/python-ldap/python-ldap-%{version}.tar.gz

### Patches ###
# Fedora specific patch
Patch0: python-ldap-2.4.16-dirs.patch

### Dependencies ###
Requires: openldap 
# LDAP controls, extop, syncrepl require pyasn1
Requires: python-pyasn1, python-pyasn1-modules

### Build Dependencies ###
BuildRequires: openldap-devel
BuildRequires: openssl-devel
BuildRequires: python2-devel 
BuildRequires: cyrus-sasl-devel

# we don't want to provide private python extension libs
%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$
%filter_setup
}

%description
python-ldap provides an object-oriented API for working with LDAP within
Python programs.  It allows access to LDAP directory servers by wrapping the 
OpenLDAP 2.x libraries, and contains modules for other LDAP-related tasks 
(including processing LDIF, LDAPURLs, LDAPv3 schema, etc.).

%prep
%setup -q -n python-ldap-%{version}
%patch0 -p1 -b .dirs

# clean up cvs hidden files
rm -rf Demo/Lib/ldap/.cvsignore Demo/.cvsignore Demo/Lib/ldif/.cvsignore Demo/Lib/ldap/async/.cvsignore \
       Demo/Lib/.cvsignore Demo/Lib/ldapurl/.cvsignore

# Fix interpreter
sed -i 's|#! python|#!/usr/bin/python|g' Demo/simplebrowse.py

%build
%{__python} setup.py build

%install
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENCE CHANGES README TODO Demo
%{python_sitearch}/_ldap.so
%{python_sitearch}/dsml.py*
%{python_sitearch}/ldapurl.py*
%{python_sitearch}/ldif.py*
%{python_sitearch}/ldap/
%{python_sitearch}/python_ldap-%{version}-*.egg-info

%changelog
* Mon Sep 29 2014 Petr Spacek <pspacek@redhat.com> - 0:2.4.17-1
- New upstream release adds features required in bug 1122486
- Dependency on pyasn1-modules was added to fix bug 995545

* Thu Sep 25 2014 Petr Spacek <pspacek@redhat.com> - 0:2.4.16-1
- New upstream release fixes bug 1007820
- Dependency on pyasn1 was added to fix bug 995545

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.4.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.4.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.4.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.4.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.4.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jan 02 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.4.6-1
- New upstream release

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.3.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Sep 24 2010 Parag Nemade <paragn AT fedoraproject.org> - 0:2.3.12-1
- Merge-review cleanup (#226343)

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0:2.3.10-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jan 14 2010 Matthew Barnes <mbarnes@redhat.com> - 0:2.3.10-1
- Update to 2.3.10
- Change source URI to pypi.python.org.

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0:2.3.6-3
- rebuilt with new openssl

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 01 2009 Matthew Barnes <mbarnes@redhat.com> - 0:2.3.6-1
- Update to 2.3.6

* Fri Feb 27 2009 Matthew Barnes <mbarnes@redhat.com> - 0:2.3.5-5
- Fix a build error.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.3.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 16 2009 Tomas Mraz <tmraz@redhat.com> - 0:2.3.5-3
- rebuild with new openssl

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0:2.3.5-2
- Rebuild for Python 2.6

* Wed Sep  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:2.3.5-1
- fix license tag
- update to 2.3.5

* Sun Feb 17 2008 Matthew Barnes <mbarnes@redhat.com> - 0:2.3.1-3.fc9
- Rebuild with GCC 4.3

* Wed Dec 05 2007 Matthew Barnes <mbarnes@redhat.com> - 0:2.3.1-2.fc9
- Rebuild against new openssl.

* Wed Oct 10 2007 Matthew Barnes <mbarnes@redhat.com> - 0:2.3.1-1.fc8
- Update to 2.3.1

* Fri Jun 08 2007 Matthew Barnes <mbarnes@redhat.com> - 0:2.3.0-1.fc8
- Update to 2.3
- Spec file cleanups.

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 0:2.2.0-3
- rebuild against python 2.5

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com>
- rebuild

* Wed May 17 2006 Matthew Barnes <mbarnes@redhat.com> - 2.2.0-2
- Put back the epoch line... happy beehive?

* Tue May 15 2006 Matthew Barnes <mbarnes@redhat.com> - 2.2.0-1
- Update to 2.2.0
- Update python-ldap-2.0.6-rpath.patch and rename it to
  python-ldap-2.2.0-dirs.patch.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0:2.0.6-5.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0:2.0.6-5.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Nov  8 2005 Tomas Mraz <tmraz@redhat.com> - 2.0.6-5
- rebuilt with new openssl

* Tue Mar 22 2005 Warren Togami <wtogami@redhat.com> - 2.0.6-4
- add LICENCE (#150842)
- simplify python reqs
- remove invalid rpath

* Wed Mar 16 2005 Dan Williams <dcbw@redhat.com> - 0:2.0.6-2
- rebuilt to pick up new libssl.so.5

* Tue Feb  8 2005 David Malcolm <dmalcolm@redhat.com> - 0:2.0.6-1
- 2.0.6

* Tue Nov 16 2004 Nalin Dahyabhai <nalin@redhat.com> - 0:2.0.1-3
- rebuild (#139161)

* Mon Aug 30 2004 David Malcolm <dmalcolm@redhat.com> - 0:2.0.1-2
- Rewrote description; added requirement for openldap

* Tue Aug 17 2004 David Malcolm <dmalcolm@redhat.com> - 0:2.0.1-1
- imported into Red Hat's packaging system from Fedora.us; set release to 1

* Wed Jun 30 2004 Panu Matilainen <pmatilai@welho.com> 0:2.0.1-0.fdr.1
- update to 2.0.1

* Sun Dec 07 2003 Panu Matilainen <pmatilai@welho.com> 0:2.0.0-0.fdr.0.4.pre16
- fix spec permissions + release tag order (bug 1099)

* Sat Dec  6 2003 Ville Skyttä <ville.skytta at iki.fi> 0:2.0.0-0.fdr.0.pre16.3
- Stricter python version requirements.
- BuildRequire openssl-devel.
- Explicitly build *.pyo, install them as %%ghost.
- Own more installed dirs.
- Remove $RPM_BUILD_ROOT at start of %%install.

* Wed Dec 03 2003 Panu Matilainen <pmatilai@welho.com> 0:2.0.0-0.fdr.0.pre16.2
- duh, build requires python-devel, not just python...

* Wed Dec 03 2003 Panu Matilainen <pmatilai@welho.com> 0:2.0.0-0.fdr.0.pre16.1
- Initial Fedora packaging.
