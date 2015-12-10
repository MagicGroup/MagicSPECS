%define php_extdir %(php-config --extension-dir 2>/dev/null || echo %{_libdir}/php4)
%global php_apiver %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)

# Private libraries are not be exposed globally by RPM
# RPM 4.8
%{?filter_provides_in: %filter_provides_in %{php_extdir}/.*\.so$}
%{?filter_setup}
# RPM 4.9
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{php_extdir}/.*\\.so$

Name:           uuid
Version:        1.6.2
Release:        23%{?dist}
Summary:        Universally Unique Identifier library
Summary(zh_CN.UTF-8): 通用唯一标识符库
License:        MIT
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL:            http://www.ossp.org/pkg/lib/uuid/
Source0:        ftp://ftp.ossp.org/pkg/lib/uuid/uuid-%{version}.tar.gz
Patch0:         uuid-1.6.1-ossp.patch
Patch1:         uuid-1.6.1-mkdir.patch
Patch2:         uuid-1.6.2-php54.patch

# rhbz#829532
Patch3:         uuid-1.6.2-hwaddr.patch

# do not strip binaries
Patch4:         uuid-1.6.2-nostrip.patch
Patch5: uuid-1.6.2-manfix.patch
Patch6: uuid-aarch64.patch


BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  libtool

%description
OSSP uuid is a ISO-C:1999 application programming interface (API)
and corresponding command line interface (CLI) for the generation
of DCE 1.1, ISO/IEC 11578:1996 and RFC 4122 compliant Universally
Unique Identifier (UUID). It supports DCE 1.1 variant UUIDs of version
1 (time and node based), version 3 (name based, MD5), version 4
(random number based) and version 5 (name based, SHA-1). Additional
API bindings are provided for the languages ISO-C++:1998, Perl:5 and
PHP:4/5. Optional backward compatibility exists for the ISO-C DCE-1.1
and Perl Data::UUID APIs.

%description -l zh_CN.UTF-8
通用唯一标识符库。

%package devel
Summary:        Development support for Universally Unique Identifier library
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       pkgconfig
Requires:       %{name} = %{version}-%{release}

%description devel
Development headers and libraries for OSSP uuid.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package c++
Summary:        C++ support for Universally Unique Identifier library
Summary(zh_CN.UTF-8): %{name} 的 C++ 支持
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires:       %{name} = %{version}-%{release}

%description c++
C++ libraries for OSSP uuid.

%description c++ -l zh_CN.UTF-8
%{name} 的 C++ 支持.

%package c++-devel
Summary:        C++ development support for Universally Unique Identifier library
Summary(zh_CN.UTF-8): %{name} 的 C++ 开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}-c++ = %{version}-%{release}
Requires:       %{name}-devel = %{version}-%{release}

%description c++-devel
C++ development headers and libraries for OSSP uuid.

%description c++-devel -l zh_CN.UTF-8
%{name} 的 C++ 开发包。

%package perl
Summary:        Perl support for Universally Unique Identifier library
Summary(zh_CN.UTF-8): %{name} 的 Perl 绑定
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       %{name} = %{version}-%{release}

%description perl
Perl OSSP uuid modules, which includes a Data::UUID replacement.

%description perl -l zh_CN.UTF-8
%{name} 的 Perl 绑定。

%package php
Summary:        PHP support for Universally Unique Identifier library
Summary(zh_CN.UTF-8): %{name} 的 php 绑定
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
BuildRequires:  php-devel
Requires:       %{name} = %{version}-%{release}
%if 0%{?php_zend_api:1}
Requires: php(zend-abi) = %{php_zend_api}
Requires: php(api) = %{php_core_api}
%else
Requires: php-api = %{php_apiver}
%endif

%description php
PHP OSSP uuid module.

%description php -l zh_CN.UTF-8
%{name} 的 php 绑定。

%package pgsql
Summary:        PostgreSQL support for Universally Unique Identifier library
Summary(zh_CN.UTF-8): %{name} 的 PostreSQL 支持
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
BuildRequires:  postgresql-devel
Requires:       postgresql%{_isa}
Requires:       %{_datadir}/pgsql
Requires:       %{name} = %{version}-%{release}

%description pgsql
PostgreSQL OSSP uuid module.

%description pgsql -l zh_CN.UTF-8
%{name} 的 PostgreSQL 支持。

%package dce
Summary:        DCE support for Universally Unique Identifier library
Summary(zh_CN.UTF-8): %{name} 的 DCE 支持
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}

%description dce
DCE OSSP uuid library.

%description dce -l zh_CN.UTF-8
%{name} 的 DCE 支持。

%package dce-devel
Summary:        DCE development support for Universally Unique Identifier library
Summary(zh_CN.UTF-8): %{name}-dce 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name}-dce = %{version}-%{release}
Requires:       %{name}-devel = %{version}-%{release}

%description dce-devel
DCE development headers and libraries for OSSP uuid.

%description dce-devel -l zh_CN.UTF-8
%{name}-dce 的开发包。

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1 -b .php54
%patch3 -p1 -b .hwaddr
%patch4 -p1 -b .nostrip
%patch5 -p1 -b .manfix
%patch6 -p1 -b .aarch64

%build
# Build the library.
export LIB_NAME=libossp-uuid.la
export DCE_NAME=libossp-uuid_dce.la
export CXX_NAME=libossp-uuid++.la
export PHP_NAME=$(pwd)/php/modules/ossp-uuid.so
export PGSQL_NAME=$(pwd)/pgsql/libossp-uuid.so
export CFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$RPM_OPT_FLAGS"
%configure \
    --disable-static \
    --without-perl \
    --without-php \
    --with-dce \
    --with-cxx \
    --with-pgsql

make LIBTOOL=/usr/bin/libtool CFLAGS="$CFLAGS" CXXFLAGS="$CXXFLAGS" %{?_smp_mflags}

# Build the Perl module.
pushd perl
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS" COMPAT=1
%{__perl} -pi -e 's/^\tLD_RUN_PATH=[^\s]+\s*/\t/' Makefile
make %{?_smp_mflags}
popd

# Build the PHP module.
pushd php
export PHP_RPATH=no
phpize
CFLAGS="$RPM_OPT_FLAGS -I.. -L.. -L../.libs"
%configure --enable-uuid
make CFLAGS="$CFLAGS" CXXFLAGS="$CXXFLAGS" %{?_smp_mflags}
popd

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la $RPM_BUILD_ROOT%{_libdir}/*.a
chmod 755 $RPM_BUILD_ROOT%{_libdir}/*.so.*.*.*

# Install the Perl modules.
pushd perl
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*
popd

# Install the PHP module.
pushd php
make install INSTALL_ROOT=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{php_extdir}/*.a
popd

# Put the php config bit into place
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cat} << __EOF__ > %{buildroot}%{_sysconfdir}/php.d/%{name}.ini
; Enable %{name} extension module
extension=%{name}.so
__EOF__

magic_rpm_clean.sh

%check
make check

pushd perl
LD_LIBRARY_PATH=../.libs make test
popd

pushd php
LD_LIBRARY_PATH=../.libs make test
popd
# Simple extension load test (no test run in make test)
LD_LIBRARY_PATH=.libs php -n -d extension_dir=php/modules -d extension=uuid.so -m | grep uuid

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%post c++ -p /sbin/ldconfig

%post dce -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%postun c++ -p /sbin/ldconfig

%postun dce -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog HISTORY NEWS PORTING README SEEALSO THANKS TODO USERS
%{_bindir}/uuid
%{_libdir}/libossp-uuid.so.*
%{_mandir}/man1/*
%exclude %{_mandir}/man1/uuid-config.*

%files devel
%defattr(-,root,root,-)
%{_bindir}/uuid-config
%{_includedir}/uuid.h
%{_libdir}/libossp-uuid.so
%{_libdir}/pkgconfig/ossp-uuid.pc
%{_mandir}/man3/ossp-uuid.3*
%{_mandir}/man1/uuid-config.*

%files c++
%defattr(-,root,root,-)
%{_libdir}/libossp-uuid++.so.*

%files c++-devel
%defattr(-,root,root,-)
%{_includedir}/uuid++.hh
%{_libdir}/libossp-uuid++.so
%{_mandir}/man3/uuid++.3*

%files perl
%defattr(-,root,root,-)
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Data*
%{perl_vendorarch}/OSSP*
%{_mandir}/man3/Data::UUID.3*
%{_mandir}/man3/OSSP::uuid.3*

%files php
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/php.d/%{name}.ini
%{php_extdir}/%{name}.so

%files pgsql
%defattr(-,root,root,-)
%{_libdir}/pgsql/*
%{_datadir}/pgsql/*

%files dce
%defattr(-,root,root,-)
%{_libdir}/libossp-uuid_dce.so.*

%files dce-devel
%defattr(-,root,root,-)
%{_includedir}/uuid_dce.h
%{_libdir}/libossp-uuid_dce.so

%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 1.6.2-23
- 为 Magic 3.0 重建

* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 1.6.2-22
- 为 Magic 3.0 重建

* Sat Oct 17 2015 Liu Di <liudidi@gmail.com> - 1.6.2-21
- 为 Magic 3.0 重建

* Sat Oct 17 2015 Liu Di <liudidi@gmail.com> - 1.6.2-20
- 为 Magic 3.0 重建

* Thu Sep 17 2015 Liu Di <liudidi@gmail.com> - 1.6.2-19
- 为 Magic 3.0 重建

* Tue Jun 17 2014 Liu Di <liudidi@gmail.com> - 1.6.2-18
- 为 Magic 3.0 重建

* Wed Jan 16 2013 Liu Di <liudidi@gmail.com> - 1.6.2-17
- 为 Magic 3.0 重建

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.6.2-16
- 为 Magic 3.0 重建

* Thu Sep 27 2012 Liu Di <liudidi@gmail.com> - 1.6.2-15
- 为 Magic 3.0 重建

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 1.6.2-13
- Perl 5.16 rebuild

* Tue Jun 19 2012 Michal Hlavinka <mhlavink@redhat.com> - 1.6.2-12
- enforce usage of our c(xx)flags

* Tue Jun 19 2012 Michal Hlavinka <mhlavink@redhat.com> - 1.6.2-11
- fix debuginfo

* Tue Jun 19 2012 Michal Hlavinka <mhlavink@redhat.com> - 1.6.2-10
- fix generation of MAC address based uuids (#829532), 
  patch by Philip Prindeville

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 1.6.2-9
- Perl 5.16 rebuild

* Thu Jan 19 2012 Remi Collet <remi@fedoraproject.org> - 1.6.2-8
- build against php 5.4, with patch
- add filter_provides to avoid private-shared-object-provides shout.so
- add minimal %%check for php extension

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.6.2-6
- Perl mass rebuild

* Sat May 14 2011 Iain Arnell <iarnell@gmail.com> 1.6.2-5
- fix php_zend_api check

* Thu Mar 03 2011 Karsten Hopp <karsten@redhat.com> 1.6.2-4
- fix build

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jun 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.6.2-2
- Mass rebuild with perl-5.12.0

* Wed Apr 21 2010 Michal Hlavinka <mhlavink@redhat.com> - 1.6.2-1
- updated to 1.6.2
- uuid-config man page moved to sub-package containing uuid-config (#562838)

* Mon Feb  1 2010 Stepan Kasal <skasal@redhat.com> - 1.6.1-10
- silence rpmlint by using $(pwd) instead of shell variable RPM_SOURCE_DIR

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.6.1-9
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Remi Collet <Fedora@FamilleCollet.com> - 1.6.1-7
- rebuild for new PHP 5.3.0 ABI (20090626)
- add PHP ABI check
- use php_extdir
- add php configuration file (/etc/php.d/uuid.ini)

* Thu May  7 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.6.1-6
- Using plain old "Requires: pkgconfig" instead -- see my post to
  fedora-devel-list made today.

* Mon May  4 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.6.1-5
- Replace expensive %%{_libdir}/pkgconfig dependency in uuid-devel
  with pkgconfig%%{_isa} for Fedora >= 11 (#484849).

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.6.1-3
- Rebuild for new perl

* Thu Mar  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.6.1-2
- forgot to cvs add patch

* Thu Mar  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.6.1-1
- 1.6.1

* Thu Mar  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.6.0-4
- rebuild for new perl

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.6.0-3
- Autorebuild for GCC 4.3

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.6.0-2
- Rebuild for selinux ppc32 issue.

* Tue Jul 24 2007 Steven Pritchard <steve@kspei.com> 1.6.0-1
- Update to 1.6.0.
- BR Test::More.

* Tue Apr 17 2007 Steven Pritchard <steve@kspei.com> 1.5.1-3
- Fix find option order.
- Use fixperms macro instead of our own chmod incantation.
- BR ExtUtils::MakeMaker.

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 1.5.1-2
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Aug 28 2006 Steven Pritchard <steve@kspei.com> 1.5.1-1
- Update to 1.5.1.

* Sat Jul 29 2006 Steven Pritchard <steve@kspei.com> 1.5.0-1
- Update to 1.5.0.
- Rename libuuid* to libossp-uuid*, uuid.3 to ossp-uuid.3, and uuid.pc
  to ossp-uuid.pc to avoid conflicts with e2fsprogs-devel (#198520).
- Clean out the pgsql directory.  (Some cruft shipped with this release.)

* Wed May 24 2006 Steven Pritchard <steve@kspei.com> 1.4.2-4
- Remove static php module.

* Tue May 23 2006 Steven Pritchard <steve@kspei.com> 1.4.2-3
- Force use of system libtool.
- Make libs executable.

* Tue May 23 2006 Steven Pritchard <steve@kspei.com> 1.4.2-2
- License is MIT(-ish).

* Fri May 19 2006 Steven Pritchard <steve@kspei.com> 1.4.2-1
- Initial packaging attempt.
