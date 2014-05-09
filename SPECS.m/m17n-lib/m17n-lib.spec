# note this duplicates native anthy IMEs
%bcond_without anthy

Name:    m17n-lib
Version:  1.6.4
Release:  5%{?dist}
Summary:  Multilingual text library

Group:    System Environment/Libraries
License:  LGPLv2+
URL:    http://www.nongnu.org/m17n/
Source0:  http://download.savannah.gnu.org/releases/m17n/%{name}-%{version}.tar.gz
Patch0:  %{name}-1.6.1-multilib.patch

BuildRequires:  m17n-db-devel libthai
%if %{with anthy}
BuildRequires:  anthy-devel
%endif
BuildRequires:  libxml2-devel, libXft-devel, fontconfig-devel
BuildRequires:  freetype-devel , fribidi-devel, gd-devel, libXaw-devel
BuildRequires:  libotf-devel
Requires:  m17n-db


%description
m17n-lib is a multilingual text library used primarily to allow
the input of many languages with the input table maps from m17n-db.

The package provides the core and input method backend libraries.

%package  anthy
Summary:  Anthy module for m17n
Group:    System Environment/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description anthy
Anthy module for %{name} allows ja-anthy.mim to support input conversion.


%package  devel
Summary:  Development files for %{name}
Group:    Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-tools = %{version}-%{release}

%description devel
Development files for %{name}.


%package  tools
Summary:  m17n GUI Library tools
Group:    System Environment/Libraries
Requires: m17n-db-extras
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tools
Tools to test M17n GUI widget library.


%prep
%setup -q 
%patch0 -p0

%build
%configure --disable-rpath --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

# parallel make usage with make command fails build on koji
make

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
# fix bug rh#680363
rm $RPM_BUILD_ROOT%{_libdir}/m17n/1.0/libmimx-ispell.so

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post tools -p /sbin/ldconfig
%postun tools -p /sbin/ldconfig

%files
%doc AUTHORS COPYING NEWS ChangeLog README
#Own module directory path
%dir %{_libdir}/m17n
%dir %{_libdir}/m17n/1.0
%{_bindir}/m17n-conv
%{_libdir}/libm17n.so.*
%{_libdir}/libm17n-core.so.*
%{_libdir}/libm17n-flt.so.*

#Anthy module
%files anthy
%{_libdir}/m17n/1.0/libmimx-anthy.so

%files devel
%{_bindir}/m17n-config
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*

%files tools
%{_bindir}/m17n-date
%{_bindir}/m17n-dump
%{_bindir}/m17n-edit
%{_bindir}/m17n-view
%{_libdir}/m17n/1.0/libm17n-X.so
%{_libdir}/m17n/1.0/libm17n-gd.so
%{_libdir}/libm17n-gui.so.*

%changelog
* Sat May 03 2014 Liu Di <liudidi@gmail.com> - 1.6.4-5
- 为 Magic 3.0 重建

* Fri Nov 30 2012 Parag Nemade <pnemade AT redhat DOT com> - 1.6.4-4
- Resolves:rh#880957 - m17n-lib doesn't uninstall properly

* Tue Nov 20 2012 Parag Nemade <pnemade AT redhat DOT com> - 1.6.4-3
- m17n-lib to own %%{_libdir}/m17n

* Tue Nov 20 2012 Parag Nemade <pnemade AT redhat DOT com> - 1.6.4-2
- Resolves:rh#877925 - drop m17n-lib-flt provides
- Fix bogus date in %%changelog
- Make sure not to attempt to use parallel make as it fails the build

* Tue Sep 18 2012 Parag Nemade <pnemade AT redhat DOT com> - 1.6.4-1
- update to 1.6.4

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 11 2011 Parag Nemade <pnemade AT redhat DOT com> - 1.6.3-1
- update to 1.6.3

* Tue Mar 22 2011 Parag Nemade <pnemade AT redhat DOT com> - 1.6.2-3
- Resolves: rh#680363 - Remove m17n-lib-ispell subpackage
- Resolves: rh#677866 - m17n*.pc reports wrong moduledir on x86_64 system

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 06 2010 Parag Nemade <pnemade AT redhat.com> - 1.6.2-1
- update to new upstream release 1.6.2

* Mon Sep 13 2010 Parag Nemade <pnemade AT redhat.com> - 1.6.1-5
- Fix some packaging issue
- Change Requires: m17n-db-datafiles to m17n-db-extras

* Fri Sep 10 2010 Daiki Ueno <dueno@redhat.com> - 1.6.1-4
- supply libotf cflags/libs manually, since the current libotf package
  does not ship with "libotf-config" and m17n-lib cannot detect those
  values
- fix paths for modules used by GUI support

* Wed Aug 11 2010 Adam Jackson <ajax@redhat.com> 1.6.1-3
- Fix Obsoletes: so upgrades actually work (1.5.5-3 < 1.5.5-3.fc13)

* Wed Jul 07 2010 Parag Nemade <pnemade@redhat.com> - 1.6.1-2
- Resolves: rh#602029:-m17n-lib-devel multilib conflict 
- Fix rpmlint rpath error.

* Tue Apr 27 2010 Parag Nemade <pnemade AT redhat.com> - 1.6.1-1
- update to new upstream release 1.6.1

* Wed Apr 07 2010 Parag Nemade <pnemade AT redhat.com> - 1.6.0-1
- update to new upstream release 1.6.0

* Wed Dec 23 2009 Jens Petersen <petersen@redhat.com> - 1.5.5-2
- add bcond for otf, anthy, and gui
- subpackage flt for emacs, etc
- add subpackages for anthy and ispell modules
- disable new gui subpackage (and hence ispell)

* Mon Aug 17 2009 Parag Nemade <pnemade@redhat.com> - 1.5.5-1
- update to new upstream release 1.5.5

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 03 2009 Parag Nemade <pnemade@redhat.com> -1.5.4-1
- Update to new upstream release 1.5.4

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Oct 21 2008 Parag Nemade <pnemade@redhat.com> -1.5.3-1.fc10
- Update to new upstream release 1.5.3

* Thu Jul 03 2008 Parag Nemade <pnemade@redhat.com> -1.5.2-1
- Update to new upstream release 1.5.2

* Thu Feb 07 2008 Parag Nemade <pnemade@redhat.com> -1.5.1-1.fc9
- Update to new upstream release 1.5.1

* Fri Dec 28 2007 Parag Nemade <pnemade@redhat.com> -1.5.0-1.fc9
- Update to new upstream release 1.5.0
- Added missing internal-flt.h file as Source1

* Wed Aug 22 2007 Parag Nemade <pnemade@redhat.com> - 1.4.0-2
- rebuild against new rpm package
- update license tag

* Thu Jul 19 2007 Jens Petersen <petersen@redhat.com>
- buildrequire and require m17n-db >= 1.4.0

* Thu Jul 19 2007 Parag Nemade <pnemade@redhat.com> - 1.4.0-1
- Updated to new upstream release 1.4.0

* Wed Jan 10 2007 Mayank Jain <majain@redhat.com> - 1.3.4-1.1.fc7
- rebuild for m17n-lib-1.3.4 version
- Updated m17n-lib-nobuild-examples.patch

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.3.3-1.1.fc6
- rebuild

* Wed Jul 12 2006 Mayank Jain <majain@redhat.com> - 1.3.3-1.fc6
- Updated spec file for changes mentioned in RH bug 193524, comment 4
- Thanks to Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>

* Thu Mar  2 2006 Jens Petersen <petersen@redhat.com> - 1.3.3-1
- update to 1.3.3 minor bugfix release

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.3.2-1.1
- bump again for double-long bug on ppc(64)

* Fri Feb 10 2006 Jens Petersen <petersen@redhat.com> - 1.3.2-1
- update to 1.3.2 bugfix release
  - m17n-lib-no-gui-headers.patch is now upstream

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.3.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Feb  2 2006 Jens Petersen <petersen@redhat.com> - 1.3.1-1
- update to 1.3.1 release
  - rename use_otf and use_anthy macros to with_gui and with_examples
  - build --with-gui=no and replace m17n-lib-1.2.0-core-libs-only.patch
    with m17n-lib-no-gui-headers.patch and m17n-lib-nobuild-examples.patch

* Fri Dec 16 2005 Jens Petersen <petersen@redhat.com> - 1.2.0-2
- import to Fedora Core
- buildrequire autoconf

* Thu Nov 10 2005 Jens Petersen <petersen@redhat.com> - 1.2.0-1
- do not build static lib and .la files (Warren Togami)

* Wed Oct  5 2005 Jens Petersen <petersen@redhat.com>
- initial packaging for Fedora Extras

* Sat Jan 15 2005 UTUMI Hirosi <utuhiro78@yahoo.co.jp>
- modify spec for fedora
