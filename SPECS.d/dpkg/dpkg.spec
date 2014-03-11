%global pkgconfdir      %{_sysconfdir}/dpkg
%global pkgdatadir      %{_datadir}/dpkg

Name:           dpkg
Version:        1.16.12
Release:        1%{?dist}
Summary:        Package maintenance system for Debian Linux
Group:          System Environment/Base
# The entire source code is GPLv2+ with exception of the following
# lib/dpkg/md5.c, lib/dpkg/md5.h - Public domain
# lib/dpkg/showpkg.c, dselect/methods/multicd, lib/dpkg/utils.c, lib/dpkg/showpkg.c - GPLv2
# dselect/methods/ftp - GPL no version info
# scripts/Dpkg/Gettext.pm - BSD
# lib/compat/obstack.h, lib/compat/gettext.h,lib/compat/obstack.c - LGPLv2+
License:        GPLv2 and GPLv2+ and LGPLv2+ and Public Domain and BSD
URL:            http://packages.debian.org/unstable/admin/dpkg
Source0:        http://ftp.debian.org/debian/pool/main/d/dpkg/%{name}_%{version}.tar.xz
Patch0:         dpkg-perl-libexecdir.patch
Patch1:         dpkg-fix-logrotate.patch
BuildRequires:  zlib-devel bzip2-devel gettext ncurses-devel
BuildRequires:  autoconf automake gettext-devel
BuildRequires:  doxygen flex xz-devel po4a dotconf-devel
# for /usr/bin/pod2man
%if 0%{?fedora} > 18
BuildRequires: perl-podlators
%else 
BuildRequires: perl
%endif

%description 

This package contains the tools (including dpkg-source) required 
to unpack, build and upload Debian source packages.

This package also contains the programs dpkg which used to handle the 
installation and removal of packages on a Debian system.

This package also contains dselect, an interface for managing the 
installation and removal of packages on the system.

dpkg and dselect will certainly be non-functional on a rpm-based system
because packages dependencies will likely be unmet.

%package devel
Summary: Debian package management static library
Group:    Development/System
Provides: dpkg-static = %{version}-%{release}

%description devel
This package provides the header files and static library necessary to
develop software using dpkg, the same library used internally by dpkg.

Note though, that the API is to be considered volatile, and might change
at any time, use at your own risk.


%package dev
Summary:  Debian package development tools
Group:    Development/System
Requires: dpkg-perl = %{version}-%{release}
Requires: patch, make, binutils, bzip2, lzma, xz
Obsoletes: dpkg-devel < 1.16
BuildArch: noarch

%description dev
This package provides the development tools (including dpkg-source).
Required to unpack, build and upload Debian source packages

%package perl
Summary: Dpkg perl modules
Group:   System Environment/Base
Requires: dpkg = %{version}-%{release}
Requires: perl, perl-TimeDate
BuildArch: noarch

%description perl
This package provides the perl modules used by the scripts
in dpkg-dev. They cover a wide range of functionalities. Among them
there are the following modules:
  - Dpkg::Arch: manipulate Debian architecture information
  - Dpkg::BuildOptions: parse and manipulate DEB_BUILD_OPTIONS
  - Dpkg::Changelog: parse Debian changelogs
  - Dpkg::Checksums: generate and parse checksums
  - Dpkg::Compression::Process: wrapper around compression tools
  - Dpkg::Compression::FileHandle: transparently (de)compress files
  - Dpkg::Control: parse and manipulate Debian control information
    (.dsc, .changes, Packages/Sources entries, etc.)
  - Dpkg::Deps: parse and manipulate dependencies
  - Dpkg::ErrorHandling: common error functions
  - Dpkg::Index: collections of Dpkg::Control (Packages/Sources files for
    example)
  - Dpkg::IPC: spawn sub-processes and feed/retrieve data
  - Dpkg::Substvars: substitute variables in strings
  - Dpkg::Vendor: identify current distribution vendor
  - Dpkg::Version: parse and manipulate Debian package versions

%package -n dselect
Summary:  Debian package management front-end
Group:    System Environment/Base
Requires: %{name} = %{version}-%{release}

%description -n dselect
dselect is a high-level interface for the installation/removal of debs . 

%prep
%setup -q
%patch0 -p1
%patch1 -p1

# Filter unwanted Requires:
cat << \EOF > %{name}-req
#!/bin/sh
%{__perl_requires} $* |\
  sed -e '/perl(Dselect::Ftp)/d' -e '/perl(extra)/d' -e '/perl(file)/d' -e '/perl(dpkg-gettext.pl)/d' -e '/perl(controllib.pl)/d' -e '/perl(in)/d'
EOF

%define __perl_requires %{_builddir}/%{name}-%{version}/%{name}-req
chmod +x %{__perl_requires}

%build
autoreconf -fiv
%configure --disable-start-stop-daemon \
        --disable-linker-optimisations \
        --with-admindir=%{_localstatedir}/lib/dpkg \
        --without-selinux \
        --with-zlib \
        --with-bz2

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

mkdir -p %{buildroot}/%{pkgconfdir}/dpkg.cfg.d
mkdir -p %{buildroot}/%{pkgconfdir}/dselect.cfg.d
mkdir -p %{buildroot}/%{pkgconfdir}/origins

# Prepare "vendor" files for dpkg-vendor
cat <<EOF > %{buildroot}/%{pkgconfdir}/origins/fedora
Vendor: Fedora
Vendor-URL: http://www.fedoraproject.org/
Bugs: https://bugzilla.redhat.com
EOF
%if 0%{?fedora}
ln -sf fedora %{buildroot}/%{pkgconfdir}/origins/default
%endif

# from debian/dpkg.install
install -pm0644 debian/archtable %{buildroot}/%{pkgdatadir}/archtable
install -pm0644 debian/dpkg.cfg %{buildroot}/%{pkgconfdir}
install -pm0644 debian/shlibs.default %{buildroot}/%{pkgconfdir}
install -pm0644 debian/shlibs.override %{buildroot}/%{pkgconfdir}

# patched debian/dpkg.logrotate
mkdir -p %{buildroot}/%{_sysconfdir}/logrotate.d
install -pm0644 debian/dpkg.logrotate %{buildroot}/%{_sysconfdir}/logrotate.d/%{name}


%find_lang dpkg
%find_lang dpkg-dev
%find_lang dselect

# fedora has its own implementation
rm %{buildroot}%{_bindir}/update-alternatives
rm %{buildroot}%{_mandir}/man8/update-alternatives.8
rm -rf %{buildroot}%{_mandir}/*/man8/update-alternatives.8
rm -rf %{buildroot}%{_sysconfdir}/alternatives/

#fedora has own implemenation
#FIXME should we remove this ? 
rm -rf %{buildroot}%{_sbindir}/install-info

mkdir -p %{buildroot}/var/lib/dpkg/alternatives %{buildroot}/var/lib/dpkg/info \
 %{buildroot}/var/lib/dpkg/parts %{buildroot}/var/lib/dpkg/updates \
 %{buildroot}/var/lib/dpkg/methods


%post
# from dpkg.postinst
# Create the database files if they don't already exist
create_database() {
    admindir=${DPKG_ADMINDIR:-/var/lib/dpkg}

    for file in diversions statoverride status; do
    if [ ! -f "$admindir/$file" ]; then
        touch "$admindir/$file"
    fi
    done
}

# Create log file and set default permissions if possible
create_logfile() {
    logfile=/var/log/dpkg.log
    touch $logfile
    chmod 644 $logfile
    chown root:root $logfile 2>/dev/null || chown 0:0 $logfile
}
create_database
create_logfile


%files   -f dpkg.lang
%defattr(-,root,root,-)
%doc debian/changelog README AUTHORS THANKS TODO
%doc debian/copyright debian/usertags
%doc doc/README.feature-removal-schedule doc/triggers.txt
%dir %{pkgconfdir}
%dir %{pkgconfdir}/dpkg.cfg.d
%dir %{pkgconfdir}/origins
%config(noreplace) %{pkgconfdir}/dpkg.cfg
%config(noreplace) %{pkgconfdir}/origins/*
%config(noreplace) %{_sysconfdir}/logrotate.d/dpkg
%{_bindir}/dpkg
%{_bindir}/dpkg-deb
%{_bindir}/dpkg-maintscript-helper
%{_bindir}/dpkg-query
%{_bindir}/dpkg-split
%{_bindir}/dpkg-trigger
%{_bindir}/dpkg-divert
%{_bindir}/dpkg-statoverride
%dir %{pkgdatadir}
%{pkgdatadir}/abitable
%{pkgdatadir}/archtable
%{pkgdatadir}/cputable
%{pkgdatadir}/ostable
%{pkgdatadir}/triplettable
%dir /var/lib/dpkg/alternatives
%dir /var/lib/dpkg/info
%dir /var/lib/dpkg/parts
%dir /var/lib/dpkg/updates
%{_mandir}/man1/dpkg.1.gz
%{_mandir}/man1/dpkg-deb.1.gz
%{_mandir}/man1/dpkg-maintscript-helper.1.gz
%{_mandir}/man1/dpkg-query.1.gz
%{_mandir}/man1/dpkg-split.1.gz
%{_mandir}/man1/dpkg-trigger.1.gz
%{_mandir}/man5/dpkg.cfg.5.gz
%{_mandir}/man8/dpkg-divert.8.gz
%{_mandir}/man8/dpkg-statoverride.8.gz
%{_mandir}/*/man1/dpkg.1.gz
%{_mandir}/*/man1/dpkg-deb.1.gz
%{_mandir}/*/man1/dpkg-maintscript-helper.1.gz
%{_mandir}/*/man1/dpkg-query.1.gz
%{_mandir}/*/man1/dpkg-split.1.gz
%{_mandir}/*/man1/dpkg-trigger.1.gz
%{_mandir}/*/man5/dpkg.cfg.5.gz
%{_mandir}/*/man8/dpkg-divert.8.gz
%{_mandir}/*/man8/dpkg-statoverride.8.gz

%files devel
%defattr(-,root,root,-)
%{_libdir}/libdpkg.a
%{_libdir}/pkgconfig/libdpkg.pc
%{_includedir}/dpkg/*.h

%files dev
%defattr(-,root,root,-)
%doc doc/README.api doc/coding-style.txt doc/frontend.txt
%config(noreplace) %{pkgconfdir}/shlibs.default
%config(noreplace) %{pkgconfdir}/shlibs.override
%{_bindir}/dpkg-architecture
%{_bindir}/dpkg-buildpackage
%{_bindir}/dpkg-buildflags
%{_bindir}/dpkg-checkbuilddeps
%{_bindir}/dpkg-distaddfile
%{_bindir}/dpkg-genchanges
%{_bindir}/dpkg-gencontrol
%{_bindir}/dpkg-gensymbols
%{_bindir}/dpkg-mergechangelogs
%{_bindir}/dpkg-name
%{_bindir}/dpkg-parsechangelog
%{_bindir}/dpkg-scanpackages
%{_bindir}/dpkg-scansources
%{_bindir}/dpkg-shlibdeps
%{_bindir}/dpkg-source
%{_bindir}/dpkg-vendor
%{pkgdatadir}/*.mk
%{_mandir}/man1/dpkg-architecture.1.gz
%{_mandir}/man1/dpkg-buildflags.1.gz
%{_mandir}/man1/dpkg-buildpackage.1.gz
%{_mandir}/man1/dpkg-checkbuilddeps.1.gz
%{_mandir}/man1/dpkg-distaddfile.1.gz
%{_mandir}/man1/dpkg-genchanges.1.gz
%{_mandir}/man1/dpkg-gencontrol.1.gz
%{_mandir}/man1/dpkg-gensymbols.1.gz
%{_mandir}/man1/dpkg-mergechangelogs.1.gz
%{_mandir}/man1/dpkg-name.1.gz
%{_mandir}/man1/dpkg-parsechangelog.1.gz
%{_mandir}/man1/dpkg-scanpackages.1.gz
%{_mandir}/man1/dpkg-scansources.1.gz
%{_mandir}/man1/dpkg-shlibdeps.1.gz
%{_mandir}/man1/dpkg-source.1.gz
%{_mandir}/man1/dpkg-vendor.1.gz
%{_mandir}/man5/deb-control.5.gz
%{_mandir}/man5/deb-extra-override.5.gz
%{_mandir}/man5/deb-old.5.gz
%{_mandir}/man5/deb-origin.5.gz
%{_mandir}/man5/deb-override.5.gz
%{_mandir}/man5/deb-shlibs.5.gz
%{_mandir}/man5/deb-split.5.gz
%{_mandir}/man5/deb-src-control.5.gz
%{_mandir}/man5/deb-substvars.5.gz
%{_mandir}/man5/deb-symbols.5.gz
%{_mandir}/man5/deb-triggers.5.gz
%{_mandir}/man5/deb-version.5.gz
%{_mandir}/man5/deb.5.gz
%{_mandir}/*/man1/dpkg-architecture.1.gz
%{_mandir}/*/man1/dpkg-buildpackage.1.gz
%{_mandir}/*/man1/dpkg-buildflags.1.gz
%{_mandir}/*/man1/dpkg-checkbuilddeps.1.gz
%{_mandir}/*/man1/dpkg-distaddfile.1.gz
%{_mandir}/*/man1/dpkg-genchanges.1.gz
%{_mandir}/*/man1/dpkg-gencontrol.1.gz
%{_mandir}/*/man1/dpkg-gensymbols.1.gz
%{_mandir}/*/man1/dpkg-mergechangelogs.1.gz
%{_mandir}/*/man1/dpkg-name.1.gz
%{_mandir}/*/man1/dpkg-parsechangelog.1.gz
%{_mandir}/*/man1/dpkg-scanpackages.1.gz
%{_mandir}/*/man1/dpkg-scansources.1.gz
%{_mandir}/*/man1/dpkg-shlibdeps.1.gz
%{_mandir}/*/man1/dpkg-source.1.gz
%{_mandir}/*/man1/dpkg-vendor.1.gz
%{_mandir}/*/man5/deb-control.5.gz
%{_mandir}/*/man5/deb-extra-override.5.gz
%{_mandir}/*/man5/deb-old.5.gz
%{_mandir}/*/man5/deb-origin.5.gz
%{_mandir}/*/man5/deb-override.5.gz
%{_mandir}/*/man5/deb-shlibs.5.gz
%{_mandir}/*/man5/deb-split.5.gz
%{_mandir}/*/man5/deb-src-control.5.gz
%{_mandir}/*/man5/deb-substvars.5.gz
%{_mandir}/*/man5/deb-symbols.5.gz
%{_mandir}/*/man5/deb-triggers.5.gz
%{_mandir}/*/man5/deb-version.5.gz
%{_mandir}/*/man5/deb.5.gz

%files perl -f dpkg-dev.lang
%defattr(-,root,root,-)
%{_libexecdir}/dpkg/parsechangelog

%{perl_vendorlib}/Dpkg*
%{_mandir}/man3/Dpkg*.3*


%files -n dselect -f dselect.lang
%defattr(-,root,root,-)
%doc dselect/methods/multicd/README.multicd dselect/methods/ftp/README.mirrors.txt
%{_bindir}/dselect
%{perl_vendorlib}/Debian
%{_libdir}/dpkg/methods
%{_mandir}/man1/dselect.1.gz
%{_mandir}/*/man1/dselect.1.gz
%{_mandir}/man5/dselect.cfg.5.gz
%{_mandir}/*/man5/dselect.cfg.5.gz
%dir %{pkgconfdir}/dselect.cfg.d
/var/lib/dpkg/methods


%changelog
* Wed Oct 16 2013 Sérgio Basto <sergio@serjux.com> - 1.16.12-1
- Update to 1.16.12
- added /etc/dpkg/origins/... , by Oron Peled, rhbz #973832
- fix few files listed twice.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.16.10-7
- Perl 5.18 rebuild

* Mon Jul 01 2013 Sérgio Basto <sergio@serjux.com> - 1.16.10-6
- add support to logrotate, by Oron Peled, rhbz #979378
- added some new %doc and debian/copyright, by Oron Peled, rhbz #979378
- rpmlint cleanups, by Oron Peled, rhbz #979378 

* Sun Jun 30 2013 Sérgio Basto <sergio@serjux.com> - 1.16.10-5
- rhbz #979378 
  - Obsolete the old dpkg-devel.noarch (replaced by dpkg-dev)
  (Obsoletes: dpkg-devel < 1.16)
  - Readd to dpkg-perl: Requires: dpkg = <version>-<release>
  - Patchset Signed-off-by: Oron Peled
  - [PATCH 1/4] move dpkg.cfg from /etc to /etc/dpkg 
  - [PATCH 2/4] fix some pkgdatadir, pkgconfdir file locations
  - [PATCH 3/4] move "dpkg-dev.mo" files to dpkg-perl
  - [PATCH 4/4] minor fix to dpkg-perl ownerships
- move from dpkg to dpkg-dev, rhbz #979378 
  - dpkg-mergechangelogs and its man-pages
  - dpkg-buildflags and its man-pages
- remove man pages dups, also rhbz #979378
    dpkg-architecture.1.gz
    dpkg-buildflags.1.gz
    dpkg-buildpackage.1.gz
    dpkg-checkbuilddeps.1.gz
    dpkg-distaddfile.1.gz
    dpkg-genchanges.1.gz
    dpkg-gencontrol.1.gz
    dpkg-gensymbols.1.gz
    dpkg-mergechangelogs.1.gz
    dpkg-name.1.gz
    dpkg-parsechangelog.1.gz
    dpkg-scanpackages.1.gz
    dpkg-scansources.1.gz
    dpkg-shlibdeps.1.gz
    dpkg-source.1.gz
    dpkg-vendor.1.gz

* Sun Jun 02 2013 Sérgio Basto <sergio@serjux.com> - 1.16.10-4
- provided virtual -static package rhbz #967215

* Tue May 21 2013 Sérgio Basto <sergio@serjux.com> - 1.16.10-3
- Copied from dpkg-1.16.10/debian/dpkg.postinst, on post install, runs create_database, create_logfile. 
- Based on dpkg.install and dselect.install
  created some missing directories in /var/lib/dpkg and in /etc/dpkg .
- Drop Requirement dpkg of dpkg-perl.
- Fix a FIXME , all perls moved to dpkg-perl.
- TODO: set logrotates, see debian/dpkg.logrotate.

* Fri May 17 2013 Sérgio Basto <sergio@serjux.com> - 1.16.10-2
- apply fix by Oron Peled bug #648384, adds dpkg-perl as noarch

* Thu May 16 2013 Sérgio Basto <sergio@serjux.com> - 1.16.10-1
- Add BR perl-podlators for pod2man in F19 development or just BR perl
- Add some other importants BR: doxygen flex xz-devel po4a dotconf-devel
- Fix packages names which are debianized, so packages will be: dpkg-perl
and dpkg-dev (and dpkg-devel for headers of dpkg).
- Some clean ups.
- dpkg-perl must be arched.

* Sat May  4 2013 Oron Peled <oron@actcom.co.il>
- Bump version to Debian/wheezy
- Call autoreconf: make sure we don't reuse Debian packaged
  stuff (config.guess, etc.)
- CVE patches not needed -- is already fixed upstream
- Removed dpkg-change-libdir.patch:
  - Patching Makefile.in is wrong (can patch Makefile.am with autoreconf)
  - Less patch churn for non-critical paths
  - Accept /usr/lib/dpkg/parsechangelog
  - Accept /usr/lib/dpkg/methods

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15.5.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15.5.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15.5.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15.5.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 12 2011 Andrew Colin Kissa <andrew@topdog.za.net> - 1.15.5.6-6
- Fix CVE-2010-1679
- Fix CVE-2011-0402

* Sun Oct 17 2010 Jeroen van Meeuwen <kanarip@kanarip.com> - 1.15.5.6-5
- Apply minimal fix for rhbz #642160

* Thu Mar 11 2010 Andrew Colin Kissa <andrew@topdog.za.net> - 1.15.5.6-4
- Fix CVE-2010-0396

* Mon Feb 15 2010 Andrew Colin Kissa <andrew@topdog.za.net> - 1.15.5.6-3
- review changes

* Sun Feb 14 2010 Andrew Colin Kissa <andrew@topdog.za.net> - 1.15.5.6-2
- review changes

* Sat Feb 13 2010 Andrew Colin Kissa <andrew@topdog.za.net> - 1.15.5.6-1
- Upgrade to latest upstream
- review changes

* Tue Nov 10 2009 Andrew Colin Kissa <andrew@topdog.za.net> - 1.15.4.1-1
- Upgrade to latest upstream
- review changes

* Tue Dec 30 2008 Leigh Scott <leigh123linux@googlemail.com> - 1.14.23-3
- more review changes               

* Mon Dec 15 2008 Leigh Scott <leigh123linux@googlemail.com> - 1.14.23-1
- bump version and make some of the review changes

* Tue Aug 19 2008 Leigh Scott <leigh123linux@googlemail.com> - 1.14.20-5
- made changes for review 

* Thu Jul 31 2008 Leigh Scott <leigh123linux@googlemail.com> - 1.14.20-4
- Change release to -4 as server refused -3

* Thu Jul 31 2008 Leigh Scott <leigh123linux@googlemail.com> - 1.14.20-3
- split the package into dkpg, dpkg-dev & dselect

* Tue Jul 29 2008 Leigh Scott <leigh123linux@googlemail.com> - 1.14.20-2
- recode man files to UTF8

* Tue Jul 29 2008 Leigh Scott <leigh123linux@googlemail.com> - 1.14.20-1
- Rebuild ans add build requires ncurses-devel

* Thu Jul 19 2007 Patrice Dumas <pertusus@free.fr> - 1.14.5-1
- initial packaging
