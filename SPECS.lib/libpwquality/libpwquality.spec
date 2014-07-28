Summary: A library for password generation and password quality checking
Summary(zh_CN.UTF-8): 密码生成和密码质量校验库
Name: libpwquality
Version: 1.2.3
Release: 3%{?dist}
# The package is BSD licensed with option to relicense as GPLv2+
# - this option is redundant as the BSD license allows that anyway.
License: BSD or GPLv2+
Group: System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
Source0: http://fedorahosted.org/releases/l/i/libpwquality/libpwquality-%{version}.tar.bz2
Patch1: libpwquality-1.2.3-translation-updates.patch

%global _pwqlibdir %{_libdir}
%global _moduledir %{_libdir}/security
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

%description -l zh_CN.UTF-8
密码生成和密码质量校验库，这个库使用 cracklib 和 cracklib 字典
来进一些检查。

%package devel
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Summary: Support for development of applications using the libpwquality library
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires: libpwquality%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
Files needed for development of applications using the libpwquality
library.
See the pwquality.h header file for the API.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package -n python-pwquality
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Summary: Python bindings for the libpwquality library
Summary(zh_CN.UTF-8): %{name} 的 Python 绑定
Requires: libpwquality%{?_isa} = %{version}-%{release}

%description -n python-pwquality
This is pwquality Python module that provides Python bindings
for the libpwquality library. These bindings can be used
for easy password quality checking and generation of random
pronounceable passwords from Python applications.

%description -n python-pwquality -l zh_CN.UTF-8
%{name} 的 Python 绑定。

%prep
%setup -q
%patch1 -p2 -b .translations

%build
%configure \
	--with-securedir=%{_moduledir} \
	--with-pythonsitedir=%{python_sitearch} \
	--disable-static

make -C po update-po
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'

%if "%{_pwqlibdir}" != "%{_libdir}"
pushd $RPM_BUILD_ROOT%{_libdir}
mv libpwquality.so.* $RPM_BUILD_ROOT%{_pwqlibdir}
ln -sf %{_pwqlibdir}/libpwquality.so.*.* libpwquality.so
popd
%endif
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_moduledir}/*.la
magic_rpm_clean.sh
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
%{_pwqlibdir}/libpwquality.so.*
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
* Mon Jul 28 2014 Liu Di <liudidi@gmail.com> - 1.2.3-3
- 为 Magic 3.0 重建

* Fri Nov 29 2013 Tomáš Mráz <tmraz@redhat.com> 1.2.3-2
- translation updates

* Thu Sep 12 2013 Tomáš Mráz <tmraz@redhat.com> 1.2.3-1
- fix problem with parsing the pam_pwquality options
  patch by Vladimir Sorokin.
- updated translations from Transifex
- treat empty user or password as NULL
- move the library to /usr

* Wed Jun 19 2013 Tomas Mraz <tmraz@redhat.com> 1.2.2-1
- manual page fixes
- make it possible to set the maxsequence configuration value
- updated translations from Transifex

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
