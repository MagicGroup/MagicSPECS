%global build_with_ijs_support 1

Name:           gutenprint
Summary:        Printer Drivers Package
Version:        5.2.9
Release:        16%{?dist}
Group:          System Environment/Base
URL:            http://gimp-print.sourceforge.net/
Source0:        http://downloads.sourceforge.net/gimp-print/%{name}-%{version}.tar.bz2
# Post-install script to update foomatic PPDs.
Source1:        gutenprint-foomaticppdupdate
# Post-install script to update CUPS native PPDs.
Source2:        cups-genppdupdate.py.in
Patch0:         gutenprint-menu.patch
Patch1:         gutenprint-O6.patch
Patch2:         gutenprint-selinux.patch
Patch3:         gutenprint-postscriptdriver.patch
Patch4:         gutenprint-device-ids.patch
Patch5:         gutenprint-ui2-libdeps.patch
Patch6:         gutenprint-yyin.patch
Patch7:         gutenprint-manpage.patch
Patch8:         gutenprint-test-suite.patch
License:        GPLv2+

BuildRequires:  cups-libs, cups-devel, cups
BuildRequires:  gettext-devel,pkgconfig,gimp-devel
BuildRequires:  libtiff-devel,libjpeg-devel,libpng-devel
BuildRequires:  foomatic,gtk2-devel
%if %{build_with_ijs_support}
BuildRequires:  ghostscript-devel
%endif
BuildRequires:  gimp
BuildRequires:  chrpath
Obsoletes:      gimp-print-utils < 4.2.7-25
Provides:       gimp-print-utils = 4.2.7-25

# Make sure we get postscriptdriver tags.
BuildRequires:  python-cups

# autoreconf
BuildRequires: autoconf automake libtool

## NOTE ##
# The README file in this package contains suggestions from upstream
# on how to package this software. I'd be inclined to follow those
# suggestions unless there's a good reason not to do so.

%description
Gutenprint is a package of high quality printer drivers for Linux, BSD,
Solaris, IRIX, and other UNIX-alike operating systems.
Gutenprint was formerly called Gimp-Print.

%package doc
Summary:        Documentation for gutenprint
Group:          Documentation

%description doc
Documentation for gutenprint.

%package devel
Summary:        Library development files for gutenprint
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gtk2-devel
Obsoletes:      gimp-print-devel < 4.2.7-25
Provides:       gimp-print-devel = 4.2.7-25

%description devel
This package contains headers and libraries required to build applications that
uses gutenprint package.

%package plugin
Summary:        GIMP plug-in for gutenprint
Group:          System Environment/Base
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gimp
Obsoletes:      gimp-print-plugin < 4.2.7-25
Provides:       gimp-print-plugin = 4.2.7-25

%description plugin
This package contains the gutenprint GIMP plug-in.

%package foomatic
Summary:        Foomatic printer database information for gutenprint
Group:          System Environment/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires(post): foomatic
# python-cups is required for the update script (bug #246865)
Requires(post): python-cups
Requires:       foomatic-db
Obsoletes:      gimp-print < 4.2.7-25
Provides:       gimp-print = 4.2.7-25

%description  foomatic
This package contains a database of printers,printer drivers,
and driver descriptions.

%package extras
Summary:        Sample test pattern generator for gutenprint-devel
Group:          Applications/Publishing
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description extras
This package contains test pattern generator and the sample test pattern
that is used by gutenprint-devel package.

%package cups
Summary:        CUPS drivers for Canon, Epson, HP and compatible printers
Group:          Applications/Publishing
Requires:       cups >= 1.2.1-1.7
Requires:       %{name}%{?_isa} = %{version}-%{release}
Obsoletes: gimp-print-cups < 4.2.7-26
Provides: gimp-print-cups = %{version}-%{release}
Obsoletes: gutenprint-ppds-cs < 5.0.0-8
Provides: gutenprint-ppds-cs = %{version}-%{release}
Obsoletes: gutenprint-ppds-da < 5.0.0-8
Provides: gutenprint-ppds-da = %{version}-%{release}
Obsoletes: gutenprint-ppds-de < 5.0.0-8
Provides: gutenprint-ppds-de = %{version}-%{release}
Obsoletes: gutenprint-ppds-el < 5.0.0-8
Provides: gutenprint-ppds-el = %{version}-%{release}
Obsoletes: gutenprint-ppds-en_GB < 5.0.0-8
Provides: gutenprint-ppds-en_GB = %{version}-%{release}
Obsoletes: gutenprint-ppds-es < 5.0.0-8
Provides: gutenprint-ppds-es = %{version}-%{release}
Obsoletes: gutenprint-ppds-fr < 5.0.0-8
Provides: gutenprint-ppds-fr = %{version}-%{release}
Obsoletes: gutenprint-ppds-hu < 5.0.0-8
Provides: gutenprint-ppds-hu = %{version}-%{release}
Obsoletes: gutenprint-ppds-ja < 5.0.0-8
Provides: gutenprint-ppds-ja = %{version}-%{release}
Obsoletes: gutenprint-ppds-nb < 5.0.0-8
Provides: gutenprint-ppds-nb = %{version}-%{release}
Obsoletes: gutenprint-ppds-nl < 5.0.0-8
Provides: gutenprint-ppds-nl = %{version}-%{release}
Obsoletes: gutenprint-ppds-pl < 5.0.0-8
Provides: gutenprint-ppds-pl = %{version}-%{release}
Obsoletes: gutenprint-ppds-pt < 5.0.0-8
Provides: gutenprint-ppds-pt = %{version}-%{release}
Obsoletes: gutenprint-ppds-sk < 5.0.0-8
Provides: gutenprint-ppds-sk = %{version}-%{release}
Obsoletes: gutenprint-ppds-sv < 5.0.0-8
Provides: gutenprint-ppds-sv = %{version}-%{release}
Obsoletes: gutenprint-ppds-zh_TW < 5.0.0-8
Provides: gutenprint-ppds-zh_TW = %{version}-%{release}

%description cups
This package contains native CUPS support for a wide range of Canon,
Epson, HP and compatible printers.

%prep
%setup -q -n %{name}-%{version}
# Fix menu placement of GIMP plugin.
%patch0 -p1 -b .menu
# Don't use -O6 compiler option.
%patch1 -p1 -b .O6
# Restore file contexts when updating PPDs.
%patch2 -p1 -b .selinux
# Allow the CUPS dynamic driver to run inside a build root.
%patch3 -p1 -b .postscriptdriver
# Added IEEE 1284 Device ID for
#  Epson Stylus D78 (bug #245948).
#  Epson Stylus Photo R230 (from Ubuntu #520466).
#  Epson Stylus D92 (bug #570888).
#  Epson Stylus Photo 1400 (bug #577299).
#  Epson Stylus Photo 830U (bug #577307).
#  HP DeskJet 959C (bug #577291).
#  Canon PIXMA iP1900 (bug #741329).
#  Canon PIXMA iP3000 (bug #652179).
#  Canon PIXMA iP4000 (bug #741006).
#  Canon PIXMA iP4200 (bug #626365).
#  Epson Stylus C92 (bug #735400).
#  Epson Stylus Color 680 (bug #652228).
#  Epson Stylus Photo 1270 (bug #638537).
#  Epson Stylus Photo R2400 (bug #720270).
#  HP LaserJet 4050/4100/4350/5100/8000/M3027 MFP/M3035 MFP/P3005 (bug #659043).
#  HP Color LaserJet 2500/4550 (bug #659044).
#  Brother hl-2035 (bug #651603#c3)
#  Canon PIXMA MP250 (bug #744087).
#  Canon PIXMA MP500 (bug #911727).
#  Canon PIXMA Pro9000mk2.
#  Kyocera FS-1118MFP (bug #782379).
%patch4 -p1 -b .device-ids
# Fix build against new versions of gcc.

# 5.2.9 has had wrong libgutenprintui2 dependencies
%patch5 -p1 -b .ui2_libdeps

# Don't export yy* symbols (bug #882194).
%patch6 -p1 -b .yyin

# Added some escputil options to the manpage (bug #979064).
%patch7 -p1 -b .manpage

# Fix the test suite.
%patch8 -p1 -b .test-suite

cp %{SOURCE2} src/cups/cups-genppdupdate.in

%build
# autoreconf has been added due to bug #925535,
# should be safe to remove once configure is Autoconf > 2.68 generated,
# i.e. with gutenprint > 5.2.9
mkdir m4local
autoreconf --verbose --force --install

# Don't run the weave test as it takes a very long time.
sed -i -e 's,^\(TESTS *=.*\) run-weavetest,\1,' test/Makefile.in

%configure --disable-static --disable-dependency-tracking  \
            --with-foomatic --with-ghostscript \
            --enable-samples --enable-escputil \
            --enable-test --disable-rpath \
            --enable-cups-1_2-enhancements \
            --disable-cups-ppds \
            --enable-simplified-cups-ppds

make %{?_smp_mflags}

%check
make check
 
%install
make DESTDIR=%{buildroot} install

mkdir -p %{buildroot}%{_sbindir}
install -m755 %{SOURCE1} %{buildroot}%{_sbindir}

rm -rf %{buildroot}%{_datadir}/gutenprint/doc
rm -f %{buildroot}%{_datadir}/foomatic/kitload.log
rm -rf %{buildroot}%{_libdir}/gutenprint/5.2/modules/*.la
rm -f %{buildroot}%{_sysconfdir}/cups/command.types

%find_lang %{name} --all-name

%if %{build_with_ijs_support}
%else
rm -f %{buildroot}%{_mandir}/man1/ijsgutenprint.1*
%endif

# Fix up rpath.  If you can find a way to do this without resorting
# to chrpath, please let me know!
for file in \
  %{buildroot}%{_sbindir}/cups-genppd.5.2 \
  %{buildroot}%{_libdir}/gimp/*/plug-ins/* \
  %{buildroot}%{_libdir}/*.so.* \
  %{buildroot}%{_cups_serverbin}/driver/* \
  %{buildroot}%{_cups_serverbin}/filter/* \
  %{buildroot}%{_bindir}/*
do
  chrpath --delete ${file}
done


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post cups
/usr/sbin/cups-genppdupdate >/dev/null 2>&1 || :
/sbin/service cups reload >/dev/null 2>&1 || :
exit 0


%files -f %{name}.lang
%doc COPYING
%{_bindir}/escputil
%{_mandir}/man1/escputil.1*
%{_bindir}/ijsgutenprint.5.2
%if %{build_with_ijs_support}
%{_mandir}/man1/ijsgutenprint.1*
%endif
%{_datadir}/gutenprint
%{_libdir}/*.so.*
%{_libdir}/gutenprint/

# For some reason the po files are needed as well.
%{_datadir}/locale/*/gutenprint_*.po

%files doc
%doc COPYING AUTHORS NEWS README doc/FAQ.html doc/gutenprint-users-manual.odt doc/gutenprint-users-manual.pdf

%files devel
%doc ChangeLog doc/developer/reference-html doc/developer/gutenprint.pdf
%doc doc/gutenprint doc/gutenprintui2
%{_includedir}/gutenprint/
%{_includedir}/gutenprintui2/
%{_libdir}/*.so
%{_libdir}/pkgconfig/gutenprint.pc
%{_libdir}/pkgconfig/gutenprintui2.pc
%exclude %{_libdir}/*.la

%files plugin
%{_libdir}/gimp/*/plug-ins/gutenprint

%files foomatic
%doc 
%{_sbindir}/gutenprint-foomaticppdupdate
%{_datadir}/foomatic/db/source/driver/*
%{_datadir}/foomatic/db/source/opt/*

%files extras
%doc
%{_bindir}/testpattern
%{_datadir}/gutenprint/samples/*

%files cups
%doc
%{_datadir}/cups/calibrate.ppm
%{_cups_serverbin}/filter/*
%{_cups_serverbin}/driver/*
%{_bindir}/cups-calibrate
%{_sbindir}/cups-genppd*
%{_mandir}/man8/cups-calibrate.8*
%{_mandir}/man8/cups-genppd*.8*

%post foomatic
/bin/rm -f /var/cache/foomatic/*
if [ $1 -eq 2 ]; then
  %{_sbindir}/gutenprint-foomaticppdupdate %{version} >/dev/null 2>&1 || :
fi

%postun foomatic
/bin/rm -f /var/cache/foomatic/*

%changelog
* Thu Apr 17 2014 Liu Di <liudidi@gmail.com> - 5.2.9-16
- 为 Magic 3.0 重建

* Tue Apr 15 2014 Liu Di <liudidi@gmail.com> - 5.2.9-15
- 为 Magic 3.0 重建

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.9-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 16 2013 Tim Waugh <twaugh@redhat.com> - 5.2.9-13
- Run test suite.

* Thu Jun 27 2013 Tim Waugh <twaugh@redhat.com> - 5.2.9-12
- Fixed changelog dates.
- Added some escputil options to the manpage (bug #979064).

* Mon Mar 25 2013 Jiri Popelka <jpopelka@redhat.com> - 5.2.9-11
- Run autoreconf prior to running configure (#925535)

* Tue Feb 19 2013 Jiri Popelka <jpopelka@redhat.com> - 5.2.9-10
- Added IEEE 1284 Device ID for Canon PIXMA MP500 (bug #911727).

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 17 2013 Jiri Popelka <jpopelka@redhat.com> 5.2.9-8
- Added IEEE 1284 Device ID for Kyocera FS-1118MFP (bug #782379).
- Use arch-specific dependency when requiring base package.

* Tue Dec 18 2012 Tim Waugh <twaugh@redhat.com> 5.2.9-7
- Don't export yy* symbols (bug #882194).

* Fri Dec 07 2012 Jiri Popelka <jpopelka@redhat.com> 5.2.9-6
- 5.2.9 has had wrong libgutenprintui2 dependencies

* Fri Oct 19 2012 Tim Waugh <twaugh@redhat.com> 5.2.9-5
- Added IEEE 1284 Device IDs for Samsung ML-1450 (bug #844687) and
  Canon ML280 series (bug #848093).

* Fri Sep 21 2012 Tim Waugh <twaugh@redhat.com> 5.2.9-4
- Updated source URL.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 09 2012 Jiri Popelka <jpopelka@redhat.com> 5.2.9-1
- 5.2.9

* Tue Jun 12 2012 Jiri Popelka <jpopelka@redhat.com> 5.2.8-2
- bumped release

* Tue Jun 12 2012 Jiri Popelka <jpopelka@redhat.com> 5.2.8-1
- 5.2.8

* Tue Apr 03 2012 Nils Philippsen <nils@redhat.com> - 5.2.7-11
- rebuild against gimp 2.8.0 release candidate

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 16 2011 Nils Philippsen <nils@redhat.com> - 5.2.7-9
- rebuild for GIMP 2.7

* Mon Nov  7 2011 Tim Waugh <twaugh@redhat.com> 5.2.7-8
- Rebuild for new libpng.

* Tue Oct 11 2011 Tim Waugh <twaugh@redhat.com> 5.2.7-7
- Added IEEE 1284 Device ID for Canon PIXMA MP250 (bug #744087).

* Tue Sep 27 2011 Jiri Popelka <jpopelka@redhat.com> 5.2.7-6
- Use _cups_serverbin macro from cups-devel for where to put driver executables.
- Added IEEE 1284 Device ID for:
    Epson Stylus Photo R2400 (bug #720270)
    Epson Stylus C92 (bug #735400)
    Canon PIXMA iP1900 (bug #741329)
    Canon PIXMA iP4000 (bug #741006)

* Tue Aug 09 2011 Jiri Popelka <jpopelka@redhat.com> 5.2.7-5
- Improve the null-pointer.patch (bug #725447).
- Added IEEE 1284 Device ID for:
    Epson Stylus D78 (bug #245948).

* Tue Jun 28 2011 Tim Waugh <twaugh@redhat.com> 5.2.7-4
- Fixed use of find_lang macro (bug #716426).

* Wed Jun 15 2011 Tim Waugh <twaugh@redhat.com> 5.2.7-3
- Rebuilt against new python-cups package to fix postscriptdriver tags
  (bug #712074).

* Tue Jun  7 2011 Tim Waugh <twaugh@redhat.com> 5.2.7-2
- Fix build against newer versions of gcc.
- cups-genppdupdate: fixed multicat support (bug #711021).  It was
  writing an extra newline character after the URI, which caused the
  gutenprint.5.2 multicat process to exit.  This prevented some
  PPDs from being updated.

* Thu May 05 2011 Jiri Popelka <jpopelka@redhat.com> 5.2.7-1
- 5.2.7.

* Thu Dec 02 2010 Jiri Popelka <jpopelka@redhat.com> 5.2.6-3
- Added IEEE 1284 Device ID for:
    Canon PIXMA iP4200 (bug #626365).
    Canon PIXMA iP3000 (bug #652179).
    Epson Stylus Color 680 (bug #652228).
    Epson Stylus Photo 1270 (bug #638537).
    HP LaserJet 4050/4100/4350/5100/8000/M3027 MFP/M3035 MFP/P3005 (bug #659043).
    HP Color LaserJet 2500/4550 (bug #659044).
    Brother hl-2035 (bug #651603#c3).
- Avoid null pointer access in escputil (bug #659120).

* Fri Nov 26 2010 Tim Waugh <twaugh@redhat.com> 5.2.6-2
- The pycups requirement is now python-cups.

* Wed Aug 11 2010 Jiri Popelka <jpopelka@redhat.com> 5.2.6-1
- 5.2.6.

* Mon Jul 12 2010 Jiri Popelka <jpopelka@redhat.com> 5.2.5-10
- Added COPYING file to main package.

* Thu Jul  8 2010 Jiri Popelka <jpopelka@redhat.com> 5.2.5-9
- Don't ship kitload.log in foomatic sub-package (bug #594709).

* Fri Jun 11 2010 Tim Waugh <twaugh@redhat.com> 5.2.5-8
- Fixed Source0 URL.

* Wed May 12 2010 Jiri Popelka <jpopelka@redhat.com> 5.2.5-7
- Added IEEE 1284 Device ID for:
    Epson Stylus Photo 1400 (bug #577299).
    Epson Stylus Photo 830U (bug #577307).
    HP DeskJet 959C (bug #577291).

* Thu Mar 25 2010 Tim Waugh <twaugh@redhat.com> 5.2.5-6
- Added IEEE 1284 Device ID for Epson Stylus Photo R230 (from Ubuntu #520466).

* Mon Mar  8 2010 Tim Waugh <twaugh@redhat.com> 5.2.5-5
- Added IEEE 1284 Device ID for Epson Stylus D92 (bug #570888).

* Tue Mar  2 2010 Tim Waugh <twaugh@redhat.com> 5.2.5-4
- Better defattr use in file manifests.
- Fixed mixed spaces and tabs.
- Fixed main package summary.
- Added comments for all sources and patches.

* Mon Feb 15 2010 Tim Waugh <twaugh@redhat.com> 5.2.5-3
- The cups sub-package requires the exactly-matching main gutenprint
  package.

* Fri Feb 12 2010 Tim Waugh <twaugh@redhat.com> 5.2.5-2
- 5.2.5.

* Fri Feb  5 2010 Tim Waugh <twaugh@redhat.com> 5.2.4-11
- CUPS driver: if DESTDIR is set, use it when looking for XML files.
  Fixes postscriptdriver tags.

* Thu Feb  4 2010 Tim Waugh <twaugh@redhat.com> 5.2.4-10
- Rebuild for postscriptdriver tags.

* Wed Nov 25 2009 Tim Waugh <twaugh@redhat.com> 5.2.4-9
- The foomatic sub-package requires foomatic-db (for directories).

* Fri Nov 20 2009 Tim Waugh <twaugh@redhat.com> 5.2.4-8
- Don't ship command.types as CUPS defines its own.

* Thu Oct 29 2009 Tim Waugh <twaugh@redhat.com> 5.2.4-7
- Removed incorrect Device ID for Brother HL-2060 (bug #531370).

* Mon Sep 28 2009 Tim Waugh <twaugh@redhat.com> 5.2.4-6
- Reimplemented PPD upgrade script in Python to avoid perl
  dependency (bug #524978).

* Tue Sep  1 2009 Tim Waugh <twaugh@redhat.com> 5.2.4-5
- Provide IEEE 1284 Device IDs in CUPS model list.

* Tue Aug 18 2009 Tim Waugh <twaugh@redhat.com> 5.2.4-4
- Enabled simplified CUPS drivers (bug #518030).

* Mon Aug  3 2009 Tim Waugh <twaugh@redhat.com> 5.2.4-3
- Silence gutenprint-foomaticppdupdate on gutenprint-foomatic upgrade.

* Fri Jul 31 2009 Tim Waugh <twaugh@redhat.com> 5.2.4-2
- 5.2.4.  Re-enabled compiler optimization for ppc64.

* Thu Jul 30 2009 Tim Waugh <twaugh@redhat.com> 5.2.3-8
- Don't show output when upgrading cups sub-package (bug #507324).
- Split documentation into doc sub-package (bug #492452).

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Tim Waugh <twaugh@redhat.com> 5.2.3-6
- Don't build CUPS PPDs (instead build a CUPS driver that can
  generate them).  Fixes build (bug #511538).

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 29 2009 Tim Waugh <twaugh@redhat.com> 5.2.3-4
- When updating foomatic PPDs, don't give a traceback if some PPD is
  not strictly conformant (bug #481397).

* Sat Jan 10 2009 Tim Waugh <twaugh@redhat.com> 5.2.3-3
- Don't use popen2 in the foomatic PPD update script.

* Thu Jan  8 2009 Tim Waugh <twaugh@redhat.com> 5.2.3-2
- Only run the foomatic PPD update script on update, and make sure the
  script can deal with major version upgrades (bug #478328).

* Tue Dec 23 2008 Tim Waugh <twaugh@redhat.com> 5.2.3-1
- 5.2.3.

* Fri Dec  5 2008 Tim Waugh <twaugh@redhat.com> 5.2.2-2
- Fixed generation of globalized PPDs.

* Thu Nov 20 2008 Tim Waugh <twaugh@redhat.com> 5.2.2-1
- 5.2.2.
- Restore SELinux file contexts of modified PPDs.

* Mon Aug  4 2008 Tim Waugh <twaugh@redhat.com>
- Fixed summary for foomatic sub-package.

* Thu Jul 31 2008 Tom "spot" Callaway <tcallawa@redhat.com> 5.0.2-3
- fix license tag

* Wed Feb 13 2008 Tim Waugh <twaugh@redhat.com> 5.0.2-2
- Rebuild for GCC 4.3.

* Fri Jan 18 2008 Tim Waugh <twaugh@redhat.com> 5.0.2-1
- 5.0.2.  No longer need lpstat patch.

* Mon Jan  7 2008 Tim Waugh <twaugh@redhat.com>
- Own %%{_datadir}/gutenprint (bug #427801).

* Fri Oct  5 2007 Tim Waugh <twaugh@redhat.com> 5.0.1-5
- Don't ship samples in the main package.

* Fri Aug 31 2007 Tim Waugh <twaugh@redhat.com> 5.0.1-4
- Plug-in name is gutenprint, not print.

* Mon Jul  2 2007 Tim Waugh <twaugh@redhat.com> 5.0.1-3
- The foomatic package requires system-config-printer-libs for the
  update script (bug #246865).

* Mon Jul  2 2007 Tim Waugh <twaugh@redhat.com> 5.0.1-2
- Fix up foomatic PPD files after upgrade (bug #246448).

* Tue Jun 26 2007 Tim Waugh <twaugh@redhat.com> 5.0.1-1
- 5.0.1.

* Thu May 10 2007 Tim Waugh <twaugh@redhat.com> 5.0.0.99.1-3
- Try to work around GCC bug #239003.
- Don't add extra compiler flags.
- Moved gimp-print obsoletes/provides to the foomatic sub-package
  (bug #238890).

* Mon Mar  5 2007 Tim Waugh <twaugh@redhat.com> 5.0.0.99.1-2
- Slightly better obsoletes/provides to follow the naming guidelines.

* Mon Mar  5 2007 Tim Waugh <twaugh@redhat.com> 5.0.0.99.1-1
- 5.0.0.99.1.
- No longer need PPDs sub-packages: CUPS driver is included in the cups
  sub-package.
- Package the CUPS driver in sbindir and put a symlink in the CUPS ServerBin
  directory to work around bug #231015.
- Set POSIX locale when parsing lpstat output.

* Fri Mar  2 2007 Tim Waugh <twaugh@redhat.com> 5.0.0-7
- Fixed menu patch.
- Don't list rastertogutenprint twice.

* Wed Feb 28 2007 Tim Waugh <twaugh@redhat.com>
- Fixed typo in patch line.

* Wed Feb 28 2007 Tim Waugh <twaugh@redhat.com> 5.0.0-6
- Ported menu patch from gimp-print package.
- Fixed summary for plugin sub-package.

* Fri Feb  9 2007 Tim Waugh <twaugh@redhat.com> 5.0.0-5
- More obsoletes/provides for gimp-print sub-packages.

* Fri Jan 19 2007 Tim Waugh <twaugh@redhat.com> 5.0.0-4
- Disable libgutenprintui (GTK+ 1.2 library).  Build requires gtk2-devel,
  not gtk+-devel.

* Tue Jan 16 2007 Tim Waugh <twaugh@redhat.com> 5.0.0-3
- More obsoletes/provides fixing (bug #222546).

* Fri Jan 12 2007 Tim Waugh <twaugh@redhat.com> 5.0.0-2
- Make cups sub-package obsolete/provide gimp-print-cups.
- PPDs sub-packages require cups sub-package.
- Remove foomatic cache after foomatic sub-package is installed/removed.
- Obsoletes/Provides gimp-print-utils.

* Thu Jan 11 2007 Tim Waugh <twaugh@redhat.com> 5.0.0-1
- The cups subpackage no longer requires gimp-print-cups.
- Ship escputil, native CUPS backend/filters, and cups-calibrate.

* Thu Jan 11 2007 Parag Nemade <panemade@gmail.com>- 5.0.0-0.17
- Enabling -plugin subpackage as gimp-print dropped its -plugin subpackage.

* Tue Nov 14 2006 Parag Nemade <panemade@gmail.com>- 5.0.0-0.16
- Added missing dependency of gimp-print-cups in gutenprint-cups

* Tue Oct 03 2006 Parag Nemade <panemade@gmail.com>- 5.0.0-0.15
- Did some fix for tag issue

* Fri Sep 29 2006 Parag Nemade <panemade@gmail.com>- 5.0.0-0.14
- Removed unwanted .la files and made following files owned by 
  main package.
  /usr/share/gutenprint/5.0.0
  /usr/share/gutenprint

* Fri Sep 29 2006 Parag Nemade <panemade@gmail.com>- 5.0.0-0.13
- Fixed some missing file remove locations path

* Thu Sep 28 2006 Parag Nemade <panemade@gmail.com>- 5.0.0-0.12
- Fixed rpm build for x86_64 arch

* Fri Sep 08 2006 Parag Nemade <panemade@gmail.com>- 5.0.0-0.11
- Separated GIMP plugin under gutenprint-plugin package

* Thu Sep 07 2006 Parag Nemade <panemade@gmail.com>- 5.0.0-0.10
- Added gimp as BR

* Thu Sep 07 2006 Parag Nemade <panemade@gmail.com>- 5.0.0-0.9
- Removed Requires(post) and Requires(postun) lines in SPEC
- Removed mixed usage of macros

* Wed Aug 09 2006 Parag Nemade <panemade@gmail.com>- 5.0.0-0.8
- Moved cups related files from main rpm to gutenprint-cups

* Wed Aug 09 2006 Parag Nemade <panemade@gmail.com>- 5.0.0-0.7
- Moved /usr/share/gutenprint/doc to %%doc of main rpm and devel rpm 
- Additionally added API documents for gutenprint and gutenprintui2

* Tue Aug 08 2006 Parag Nemade <panemade@gmail.com>- 5.0.0-0.6
- Added cups-genppdupdate.5.0 at post section
- Splitted gutenprint main rpm for separate languages

* Wed Aug 02 2006 Parag Nemade <panemade@gmail.com>- 5.0.0-0.5
- New upstream release

* Wed Jul 19 2006 Parag Nemade <panemade@gmail.com>- 5.0.0-0.4.rc3
- Removed Requires on perl-Curses and perl-perlmenu 
  as both are automatically added on binary RPM
- Commented Obsoletes and provides tag as Fedora Extras package can not
  Obsoletes Fedora Core Package.

* Tue Jul 18 2006 Parag Nemade <panemade@gmail.com>- 5.0.0-0.3.rc3
- Added 3 more sub-packages-extras,cups,foomatic
- Added BuildRequires gtk+-devel
- Added correct options for %%configure
- Added Requires for perl-Curses, perl-perlmenu
- Added cups restart command at post section of SPEC

* Tue Jul 18 2006 Parag Nemade <panemade@gmail.com>- 5.0.0-0.2.rc3
- Added Obsoletes and Provides tag

* Fri Jul 14 2006 Parag Nemade <panemade@gmail.com>- 5.0.0-0.1.rc3
- Initial Release

