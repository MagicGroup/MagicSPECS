Summary: A complete ODBC driver manager for Linux
Name: unixODBC
Version: 2.3.1
Release: 2%{?dist}
Group: System Environment/Libraries
URL: http://www.unixODBC.org/
# Programs are GPL, libraries are LGPL, except News Server library is GPL.
License: GPLv2+ and LGPLv2+

Source: http://www.unixODBC.org/%{name}-%{version}.tar.gz
Source1: odbcinst.ini
Source4: conffile.h
Source5: README.fedora

Patch1: depcomp.patch
Patch6: export-symbols.patch
Patch8: so-version-bump.patch
Patch9: keep-typedefs.patch

Conflicts: iodbc

BuildRequires: automake autoconf libtool libtool-ltdl-devel bison flex
BuildRequires: readline-devel

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Install unixODBC if you want to access databases through ODBC.
You will also need the mysql-connector-odbc package if you want to access
a MySQL database, and/or the postgresql-odbc package for PostgreSQL.

%package devel
Summary: Development files for programs which will use the unixODBC library
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The unixODBC package can be used to access databases through ODBC
drivers. If you want to develop programs that will access data through
ODBC, you need to install this package.

%prep
%setup -q
%patch1 -p1
%patch6 -p1
%patch8 -p1
%patch9 -p1

chmod 0644 Drivers/MiniSQL/*.c
chmod 0644 Drivers/nn/*.c
chmod 0644 Drivers/template/*.c
chmod 0644 doc/ProgrammerManual/Tutorial/*.html
chmod 0644 doc/lst/*
chmod 0644 include/odbcinst.h

# Blow away the embedded libtool and replace with build system's libtool.
# (We will use the installed libtool anyway, but this makes sure they match.)
rm -rf config.guess config.sub install-sh ltmain.sh libltdl
# this hack is so we can build with either libtool 2.2 or 1.5
libtoolize --install || libtoolize

%build

aclocal
automake --add-missing
autoconf

# unixODBC 2.2.14 is not aliasing-safe
CFLAGS="%{optflags} -fno-strict-aliasing"
CXXFLAGS="$CFLAGS"
export CFLAGS CXXFLAGS

%configure --with-gnu-ld=yes --enable-threads=yes \
	--enable-drivers=yes --enable-driverc=yes --enable-ltdllib
make all

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install
install -m644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}

# multilib header hacks
# we only apply this to known Red Hat multilib arches, per bug #181335
case `uname -i` in
  i386 | x86_64 | ia64 | ppc | ppc64 | s390 | s390x | sparc | sparc64 )
    mv $RPM_BUILD_ROOT%{_includedir}/unixodbc_conf.h $RPM_BUILD_ROOT%{_includedir}/unixodbc_conf_`uname -i`.h
    rm -f unixodbc_conf.h
    sed s/CONFFILE/unixodbc_conf/ %{SOURCE4} >unixodbc_conf.h
    install -m 644 unixodbc_conf.h $RPM_BUILD_ROOT%{_includedir}
    ;;
  *)
    ;;
esac

# add some explanatory documentation
cp %{SOURCE5} README.fedora

# remove obsolete Postgres drivers from the package (but not the setup code)
rm -f $RPM_BUILD_ROOT%{_libdir}/libodbcpsql.so*

# copy text driver documentation into main doc directory
# currently disabled because upstream no longer includes text driver
# mkdir -p doc/Drivers/txt
# cp -pr Drivers/txt/doc/* doc/Drivers/txt

# don't want to install doc Makefiles as docs
find doc -name 'Makefile*' | xargs rm

# we do not want to ship static libraries
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

# remove unpackaged files from the buildroot
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libltdl.*
rm -rf $RPM_BUILD_ROOT%{_datadir}/libtool

# initialize lists of .so files
find $RPM_BUILD_ROOT%{_libdir} -name "*.so.*" | sed "s|^$RPM_BUILD_ROOT||" > base-so-list
find $RPM_BUILD_ROOT%{_libdir} -name "*.so"   | sed "s|^$RPM_BUILD_ROOT||" > devel-so-list

# move these to main package, they're often dlopened...
for lib in libodbc.so libodbcinst.so libodbcpsqlS.so libodbcmyS.so
do
    echo "%{_libdir}/$lib" >> base-so-list
    grep -v "/$lib$" devel-so-list > devel-so-list.x
    mv -f devel-so-list.x devel-so-list
done

%clean
rm -rf $RPM_BUILD_ROOT

%files -f base-so-list
%defattr(-,root,root)
%doc README COPYING AUTHORS ChangeLog NEWS doc
%doc README.fedora
%config(noreplace) %{_sysconfdir}/odbc*
%{_bindir}/odbcinst
%{_bindir}/isql
%{_bindir}/dltest
%{_bindir}/iusql
%{_bindir}/odbc_config

%files devel -f devel-so-list
%defattr(-,root,root)
%{_includedir}/*

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 2.3.1-2
- 为 Magic 3.0 重建

* Tue Jan 10 2012 Tom Lane <tgl@redhat.com> 2.3.1-1
- Update to version 2.3.1.  The main externally-visible change is that the
  GUI programs are not part of the unixODBC tarball anymore, so they are no
  longer in this package, and the unixODBC-kde sub-RPM has disappeared.
  There is a separate package unixODBC-gui-qt that now provides those programs.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.14-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Aug 31 2010 Tom Lane <tgl@redhat.com> 2.2.14-12
- Fix isql crash at EOF with -b option
Resolves: #628909

* Mon May  3 2010 Tom Lane <tgl@redhat.com> 2.2.14-11
- Re-add accidentally-removed desktop icon for ODBCConfig
Related: #587933

* Sat Mar 13 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.2.14-10
- BR qt-assistant-adp-devel

* Sat Dec 19 2009 Tom Lane <tgl@redhat.com> 2.2.14-9
- Fix bug preventing drivers from being selected in ODBCConfig
Resolves: #544852

* Wed Nov 25 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.2.14-8
- Rebuild for Qt 4.6.0 RC1 in F13 (was built against Beta 1 with unstable ABI)

* Thu Oct 15 2009 Tom Lane <tgl@redhat.com> 2.2.14-7
- Clean up bogosity in multilib stub header support: ia64 should not be
  listed (it's not multilib), sparcv9 isn't a possible uname -i output

* Fri Aug 21 2009 Tom Lane <tgl@redhat.com> 2.2.14-6
- Switch to building against qt4, not qt3.  This means the DataManager,
  DataManagerII, and odbctest applications are gone.
Resolves: #514064
- Use Driver64/Setup64 to eliminate need for hand-adjustment of odbcinst.ini
Resolves: #514688
- Fix misdeclaration of SQLBIGINT and SQLUBIGINT in generated header files
Resolves: #518623

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun  9 2009 Peter Lemenkov <lemenkov@gmail.com> - 2.2.14-4
- Properly install *.desktop files
- No need to ship INSTALL in docs
- Use macros instead of hardcoded /usr/share and /usr/include
- fixed permissions on some doc- and src-files
- Almost all rpmlint messages are gone now

* Sat Jun 06 2009 Dennis Gilmore <dennis@ausil.us> - 2.2.14-3
- add sparc support to the multilib includes header

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Tom Lane <tgl@redhat.com> 2.2.14-1
- Update to unixODBC 2.2.14.  Note this involves an ABI break and a consequent
  soname version bump, because upstream fixed some mistakes in the widths of
  some API datatypes for 64-bit platforms.  Also, the formerly embedded
  mysql, postgresql, and text drivers have been removed.  (For mysql and
  postgresql, use the separate mysql-connector-odbc and postgresql-odbc
  packages, which are far more up to date.  The text driver is not currently
  shipped by upstream at all, but might get revived as a separate SRPM later.)
- Stop shipping .a library files, per distro policy.
- Fixes for libtool 2.2.

* Mon Jul 28 2008 Tom Lane <tgl@redhat.com> 2.2.12-9
- Fix build failure caused by new default patch fuzz = 0 policy in rawhide.

* Fri Jun 13 2008 Tom Lane <tgl@redhat.com> 2.2.12-8
- Install icons in /usr/share/pixmaps, not /usr/share/icons as this package
  has historically done; the former is considered correct.

* Fri Apr  4 2008 Tom Lane <tgl@redhat.com> 2.2.12-7
- Must BuildRequire qt3 now that Fedora has renamed qt4 to qt
Resolves: #440798

* Mon Feb 11 2008 Tom Lane <tgl@redhat.com> 2.2.12-6
- Move libodbcinst.so symlink into main package, since it's often dlopen'd
Related: #204882
- Clean up specfile's ugly coding for making base-vs-devel decisions

* Sun Dec 30 2007 Tom Lane <tgl@redhat.com> 2.2.12-5
- Add missing BuildRequires for flex.
Resolves: #427063

* Thu Aug  2 2007 Tom Lane <tgl@redhat.com> 2.2.12-4
- Update License tag to match code.

* Fri Apr 20 2007 Tom Lane <tgl@redhat.com> 2.2.12-3
- Make configure find correct Qt libraries when building on a multilib machine

* Mon Apr 16 2007 Tom Lane <tgl@redhat.com> 2.2.12-2
- Drop BuildRequires for kdelibs-devel
Resolves: #152717
- Clean up a few rpmlint complaints

* Wed Dec  6 2006 Tom Lane <tgl@redhat.com> 2.2.12-1
- Update to unixODBC 2.2.12.
- Add missing BuildPrereq for bison.
Resolves: #190427

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.2.11-7.1
- rebuild

* Mon Mar 27 2006 Tom Lane <tgl@redhat.com> 2.2.11-7
- Fix minor problems in desktop files (bug #185764)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.2.11-6.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.2.11-6.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov 21 2005 Tom Lane <tgl@redhat.com> 2.2.11-6
- Patch NO-vs-no discrepancy between aclocal/acinclude and recent autoconf
  versions (not sure if this has been broken for a long time, or was just
  exposed by modular X changeover).
- Apparently need to require libXt-devel too for modular X.

* Mon Nov  7 2005 Tom Lane <tgl@redhat.com> 2.2.11-5
- Adjust BuildPrereq for modular X.

* Sun Oct 16 2005 Florian La Roche <laroche@redhat.com> 2.2.11-4
- link against dependent libs
- fix some bugs to resolve unknown symbols ;-(

* Thu Sep 29 2005 Tom Lane <tgl@redhat.com> 2.2.11-3
- Force update of yac.h because the copy in the distributed tarball does not
  match bison 2.0's numbering of symbols (bz #162676)
- Include documentation of text-file driver
- Use private libltdl so we can omit RTLD_GLOBAL from dlopen flags (bz #161399)

* Sat Sep 24 2005 Tom Lane <tgl@redhat.com> 2.2.11-2
- Remove Makefiles accidentally included in docs installation (bz #168819)
- Updates to keep newer libtool code from installing itself as part of package

* Fri Apr  8 2005 Tom Lane <tgl@redhat.com> 2.2.11-1
- Update to unixODBC 2.2.11

* Mon Mar  7 2005 Tom Lane <tgl@redhat.com> 2.2.10-3
- Rebuild with gcc4.

* Wed Jan 12 2005 Tim Waugh <twaugh@redhat.com> 2.2.10-2
- Rebuilt for new readline.

* Thu Oct 28 2004 Tom Lane <tgl@redhat.com> 2.2.10-1
- Update to unixODBC 2.2.10

* Wed Sep 22 2004 Tom Lane <tgl@redhat.com> 2.2.9-1
- Update to unixODBC 2.2.9

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat May  8 2004 Tom Lane <tgl@redhat.com> 2.2.8-5
- Backpatch fix for double-free error from upstream devel sources.
- rebuilt

* Wed May  5 2004 Tom Lane <tgl@redhat.com> 2.2.8-4
- Add dependency to ensure kde subpackage stays in sync with main
  (needed because we moved odbctest from one pkg to the other,
  cf bug #122478)
- rebuilt

* Wed Mar 10 2004 Tom Lane <tgl@redhat.com> 2.2.8-3
- Use installed libltdl
- rebuilt for Fedora Core 2

* Tue Mar  9 2004 Tom Lane <tgl@redhat.com> 2.2.8-2
- Rename lo_xxx() to odbc_lo_xxx() (bug #117211) (temporary until 2.2.9)
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Mar  1 2004 Tom Lane <tgl@redhat.com>
- Update to 2.2.8
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Dec  4 2003 Joe Orton <jorton@redhat.com> 2.2.5-10
- rebuild to restore sqltypes.h after #111195

* Thu Oct 16 2003 Fernando Nasser <fnasser@redhat.com> 2.2.5-9
- Add XFree86-devel to the list of BuildPrereq.  Did not bump
  release as there is no need to rebuild.

* Thu Oct 16 2003 Fernando Nasser <fnasser@redhat.com> 2.2.5-9
- Add comments to the /etc/odbcinst.ini file regarding the proper
  setup for MySQL and the origin of each library needed.

* Tue Oct 14 2003 Fernando Nasser <fnasser@redhat.com> 2.2.5-8
- Move libodbcmyS.so to the main package as well.  It is used the
  same way as libodbcpsqlS.so.

* Tue Oct 14 2003 Fernando Nasser <fnasser@redhat.com> 2.2.5-7
- Bumped the version so it rebuilds.

* Tue Oct 14 2003 Fernando Nasser <fnasser@redhat.com> 2.2.5-4
- Revert previous change and special case libodbcpsql.so and
  libodbcpsqlS.so instead.  Here is the explanation (from Elliot
  Lee):
  ".so files are only used at link time for normal dynamic libraries.
   The libraries referred to here are being used as dynamically loaded
   modules, so I guess moving those particular .so files back to the
   main package would make sense, but the other .so files should stay
   in the devel subpackage."

* Fri Oct 10 2003 Fernando Nasser <fnasser@redhat.com> 2.2.5-3
- Moved all the shared library symlinks to the main package.
  They were deliberatedly being added to the devel package for
  unknown reasons but this was forcing users to install the 
  devel package always. 
- No need to special-case libodbc.so anymore

* Fri Sep 05 2003 Elliot Lee <sopwith@redhat.com> 2.2.5-2
- Run auto* so it rebuilds.

* Mon Jul 07 2003 Fernando Nasser <fnasser@redhat.com> 2.2.5-1
- Moved odbctest to the kde package to remove require on Qt stuff
  from the main package.
- Removed stray "\" from doc/Makefile.am
- Applied libtool fix (provided by Alex Oliva) so that it build
 with cross-compilers (which are used by 64 bit systems)
- Updated sources to the 2.2.5 community release
- Changed the included libtool to the 1.5-3 one so that
  it properly link the libraries with the newly generated ones
  and not with the ones installed on the build system (or give
  an error if an old version is not installed (# 91110)
- Added new files for executable DataManagerII and icons LinuxODBC.xpm
  and odbc.xpm

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Jan  9 2003 Bill Nottingham <notting@redhat.com> 2.2.3-5
- debloat

* Tue Dec 17 2002 Elliot Lee <sopwith@redhat.com> 2.2.3-4
- Run libtoolize etc.

* Thu Dec 12 2002 Elliot Lee <sopwith@redhat.com> 2.2.3-3
- Rebuild to fix filelist errors...?

* Fri Nov 29 2002 Tim Powers <timp@redhat.com> 2.2.3-2
- remove unpackaged files from the buildroot

* Tue Nov 19 2002 Elliot Lee <sopwith@redhat.com> 2.2.3-1
- Rebuild, update to 2.2.3

* Mon Aug 26 2002 Trond Eivind Glomsrd <teg@redhat.com> 2.2.2-3
- Move libodbc.so to the main package, so programs dlopening 
  it don't break (#72653)

* Sat Aug 10 2002 Elliot Lee <sopwith@redhat.com>
- rebuilt with gcc-3.2 (we hope)

* Mon Jul 22 2002 Trond Eivind Glomsrd <teg@redhat.com> 2.2.2-1
- 2.2.2
- desktop file changes (# 69371)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon May 20 2002 Trond Eivind Glomsrd <teg@redhat.com> 2.2.1-1
- 2.2.1
- Reenable other archs, as this should now build on 64 bit archs

* Sun May 19 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add at least mainframe; should this really be a i386-only rpm?

* Wed Apr 17 2002 Bernhard Rosenkraenzer <bero@redhat.com> 2.2.0-5
- rebuild

* Fri Apr  5 2002 Trond Eivind Glomsrd <teg@redhat.com> 2.2.0-4
- Avoid having files in more than one package (#62755)

* Tue Mar 26 2002 Trond Eivind Glomsrd <teg@redhat.com> 2.2.0-3
- Don't include kde plugin .so as a devel symlink (#61039)

* Fri Mar  8 2002 Bernhard Rosenkraenzer <bero@redhat.com> 2.2.0-2
- Rebuild with KDE 3.x

* Tue Feb 26 2002 Trond Eivind Glomsrd <teg@redhat.com> 2.2.0-1
- Just build on i386 now, there are 64 bit oddities 
- 2.2.0

* Fri Jan 11 2002 Trond Eivind Glomsrd <teg@redhat.com> 2.1.1-2
- move libodbcinstQ* to the kde subpackage

* Fri Jan 11 2002 Trond Eivind Glomsrd <teg@redhat.com> 2.1.1-1
- 2.1.1
- minor cleanups

* Fri Dec 14 2001 Trond Eivind Glomsrd <teg@redhat.com> 2.0.7-5
- Rebuild

* Wed Sep 12 2001 Tim Powers <timp@redhat.com>
- rebuild with new gcc and binutils

* Sun Jun 24 2001 Than Ngo <than@redhat.com>
- rebuild against qt-2.3.1, kde-2.1.x

* Fri Jun 15 2001 Trond Eivind Glomsrd <teg@redhat.com>
- Better default odbcinst.ini
- Minor cleanups

* Wed Jun  6 2001 Trond Eivind Glomsrd <teg@redhat.com>
- 2.0.7

* Wed Apr 25 2001 Trond Eivind Glomsrd <teg@redhat.com>
- Fix for isql segfault on EOF/ctrl-d exit

* Fri Apr 20 2001 Trond Eivind Glomsrd <teg@redhat.com>
- 2.0.6
- add patch for 64 bit archs (dword shouldn't be "long int")

* Wed Feb 28 2001 Trond Eivind Glomsrd <teg@redhat.com>
- rebuild

* Tue Nov 28 2000 Trond Eivind Glomsrd <teg@redhat.com>
- 1.8.13

* Tue Oct 10 2000 Trond Eivind Glomsrd <teg@redhat.com>
- enable GUI now that we have KDE compiled with the standard
  compiler
- move the applnk entries to the KDE package

* Thu Aug 24 2000 Nalin Dahyabhai <nalin@redhat.com>
- add the missing shared libs to the non-devel package

* Wed Aug 23 2000 Preston Brown <pbrown@redhat.com>
- 1.8.12 fixes problems with the postgresql driver

* Mon Jul 31 2000 Trond Eivind Glomsrd <teg@redhat.com>
- disable KDE subpackage to avoid the mess that is C++ binary
  compatibility 

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Fri Jun 30 2000 Florian La Roche <laroche@redhat.com>
- improved QTDIR detection

* Thu Jun 28 2000 Trond Eivind Glomsrd <teg@redhat.com>
- 1.8.10
- use %%{_tmppath}
- update URL
- including two missing libraries

* Tue Jun 13 2000 Preston Brown <pbrown@redhat.com>
- 1.8.9

* Fri Jun 09 2000 Preston Brown <pbrown@redhat.com>
- adopted for Winston, changed to Red Hat packaging standards

* Tue Apr 18 2000 Murray Todd Williams <murray@codingapes.com>
- added a unixODBC-devel RPM to the group, added KDE links and icons to system
- all of which came from recommendations from Fredrick Meunier
- <Fredrick.Meunier@computershare.com.au>

* Mon Apr 17 2000 Murray Todd Williams <murray@codingapes.com>
- unixODBC-1.8.7
- moved install to $RPM_BUILD_ROOT so it didn't overrun existing files.
