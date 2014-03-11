Summary: A library for password generation and password quality checking
Name: libpwquality
Version: 1.2.1
Release: 2%{?dist}
# The package is BSD licensed with option to relicense as GPLv2+
# - this option is redundant as the BSD license allows that anyway.
License: BSD or GPLv2+
Group: System Environment/Base
Source0: http://fedorahosted.org/releases/l/i/libpwquality/libpwquality-%{version}.tar.bz2

%global _moduledir /%{_lib}/security
%global _secconfdir %{_sysconfdir}/security

Requires: cracklib-dicts >= 2.8
Requires: pam%{?_isa}
BuildRequires: cracklib-devel
BuildRequires: gettext
BuildRequires: pam-devel
BuildRequires: python2-devel

URL: http://libpwquality.fedorahosted.org/

# we don't want to provide private python extension libs
%define __provides_exclude_from ^%{python_sitearch}/.*\.so$.

%description
This is a library for password quality checks and generation
of random passwords that pass the checks.
This library uses the cracklib and cracklib dictionaries
to perform some of the checks.

%package devel
Group: Development/Libraries
Summary: Files needed for developing PAM-aware applications and modules for PAM
Requires: libpwquality%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
Files needed for development of applications using the libpwquality
library.
See the pwquality.h header file for the API.

%package -n python-pwquality
Group: Development/Libraries
Summary: Python bindings for the libpwquality library
Requires: libpwquality%{?_isa} = %{version}-%{release}

%description -n python-pwquality
This is pwquality Python module that provides Python bindings
for the libpwquality library. These bindings can be used
for easy password quality checking and generation of random
pronounceable passwords from Python applications.

%prep
%setup -q

%build
%configure \
	--with-securedir=/%{_lib}/security \
	--with-pythonsitedir=%{python_sitearch} \
	--disable-static

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'

pushd $RPM_BUILD_ROOT%{_libdir}
mv libpwquality.so.* $RPM_BUILD_ROOT/%{_lib}/
ln -sf ../../%{_lib}/libpwquality.so.*.* libpwquality.so
popd
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_moduledir}/*.la

%find_lang libpwquality

%check
# Nothing yet

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f libpwquality.lang
%defattr(-,root,root,-)
%doc COPYING README NEWS AUTHORS
%{_bindir}/pwmake
%{_bindir}/pwscore
%{_moduledir}/pam_pwquality.so
/%{_lib}/libpwquality.so.*
%config(noreplace) %{_secconfdir}/pwquality.conf
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*

%files devel
%defattr(-,root,root,-)
%{_includedir}/pwquality.h
%{_libdir}/libpwquality.so
%{_libdir}/pkgconfig/*.pc

%files -n python-pwquality
%defattr(-,root,root,-)
%{python_sitearch}/pwquality.so

%changelog
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 20 2012 Tomas Mraz <tmraz@redhat.com> 1.2.1-1
- properly free pwquality settings
- add extern "C" to public header
- updated translations from Transifex

* Thu Aug 16 2012 Tomas Mraz <tmraz@redhat.com> 1.2.0-1
- add maxsequence check for too long monotonic character sequence.
- clarified alternative licensing to GPLv2+.
- add local_users_only option to skip the pwquality checks for
  non-locals. (thanks to Stef Walter)

* Wed Jun 13 2012 Tomas Mraz <tmraz@redhat.com> 1.1.1-1
- use rpm built-in filtering of provides (rhbz#830153)
- remove strain debug fprintf() (rhbz#831567)

* Thu May 24 2012 Tomas Mraz <tmraz@redhat.com> 1.1.0-1
- fix leak when throwing PWQError exception
- added pkgconfig file
- call the simplicity checks before the cracklib check
- add enforce_for_root option to the PAM module
- updated translations from Transifex

* Thu Dec  8 2011 Tomas Mraz <tmraz@redhat.com> 1.0.0-1
- added a few additional password quality checks
- bugfix in configuration file parsing

* Fri Nov 11 2011 Tomas Mraz <tmraz@redhat.com> 0.9.9-1
- added python bindings and documentation

* Mon Oct 10 2011 Tomas Mraz <tmraz@redhat.com> 0.9-2
- fixes for problems found in review (missing BR on pam-devel,
  License field, Source URL, Require pam, other cleanups)

* Mon Oct  3 2011 Tomas Mraz <tmraz@redhat.com> 0.9-1
- first spec file for libpwquality
