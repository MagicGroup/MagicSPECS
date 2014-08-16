%global cache /var/cache/man
%global gnulib_ver 20120404-stable

Summary: Tools for searching and reading man pages
Summary(zh_CN.UTF-8): 搜索和读取手册页的工具
Name: man-db
Version: 2.6.7.1
Release: 1%{?dist}
# GPLv2+ .. man-db
# GPLv3+ .. gnulib
License: GPLv2+ and GPLv3+
Group: System Environment/Base
Group(zh_CN.UTF-8): 系统环境/基本
URL: http://www.nongnu.org/man-db/

Source0: http://download.savannah.gnu.org/releases/%{name}/%{name}-%{version}.tar.xz
Source1: man-db.crondaily
Source2: man-db.sysconfig

Patch0: 1110274-Add-systemd-tmpfiles-snippet-to-clean-up-old-cat-fil.patch

Obsoletes: man < 2.0
Provides: man = %{version}
Provides: man-pages-reader = %{version}
# FPC exception for gnulib - copylib - https://fedorahosted.org/fpc/ticket/174
Provides: bundled(gnulib) = %{gnulib_ver}

Requires: coreutils, grep, groff-base, gzip, less
BuildRequires: gdbm-devel, gettext, groff, less, libpipeline-devel, zlib-devel

%description
The man-db package includes five tools for browsing man-pages:
man, whatis, apropos, manpath and lexgrog. man formats and displays
manual pages. whatis searches the manual page names. apropos searches the
manual page names and descriptions. manpath determines search path
for manual pages. lexgrog directly reads header information in
manual pages.

%description -l zh_CN.UTF-8
搜索和读取手册页的工具，共有 5 个：man, whatis, apropos, manpath 和 lexgrog。

%prep
%setup -q
%patch0 -p1 

%build
%configure \
    --with-sections="1 1p 8 2 3 3p 4 5 6 7 9 0p n l p o 1x 2x 3x 4x 5x 6x 7x 8x" \
    --disable-setuid --with-browser=elinks --with-lzip=lzip \
    --with-override-dir=overrides
make CC="%{__cc} %{optflags}" %{?_smp_mflags} V=1

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT prefix=%{_prefix} INSTALL='install -p'

# move the documentation to the relevant place
mv $RPM_BUILD_ROOT%{_datadir}/doc/man-db/* ./

# remove zsoelim - part of groff package
rm $RPM_BUILD_ROOT%{_bindir}/zsoelim
rm $RPM_BUILD_ROOT%{_datadir}/man/man1/zsoelim.1

# remove libtool archives
rm $RPM_BUILD_ROOT%{_libdir}/man-db/*.la

# install cache directory
install -d -m 0755  $RPM_BUILD_ROOT%{cache}

# install cron script for man-db creation/update
install -D -p -m 0755 %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.daily/man-db.cron

# config for cron script
install -D -p -m 0644 %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/man-db

# config for tmpfiles.d
install -D -p -m 0644 init/systemd/man-db.conf $RPM_BUILD_ROOT/usr/lib/tmpfiles.d/.
magic_rpm_clean.sh
%find_lang %{name}
%find_lang %{name}-gnulib

# clear the old cache
%post
%{__rm} -rf %{cache}/*

%files -f %{name}.lang -f %{name}-gnulib.lang
%{!?_licensedir:%global license %%doc}
%license docs/COPYING
%doc README man-db-manual.txt man-db-manual.ps ChangeLog NEWS
%config(noreplace) %{_sysconfdir}/man_db.conf
%config(noreplace) %{_sysconfdir}/sysconfig/man-db
%config(noreplace) %{_sysconfdir}/cron.daily/man-db.cron
%config(noreplace) /usr/lib/tmpfiles.d/man-db.conf
%{_sbindir}/accessdb
%{_bindir}/man
%{_bindir}/whatis
%{_bindir}/apropos
%{_bindir}/manpath
%{_bindir}/lexgrog
%{_bindir}/catman
%{_bindir}/mandb
%dir %{_libdir}/man-db
%{_libdir}/man-db/*.so
%dir %{_libexecdir}/man-db
%{_libexecdir}/man-db/globbing
%{_libexecdir}/man-db/manconv
%attr(0755,root,root)   %dir %{cache}
# documentation and translation
%{_mandir}/man1/apropos.1*
%{_mandir}/man1/lexgrog.1*
%{_mandir}/man1/man.1*
%{_mandir}/man1/manconv.1*
%{_mandir}/man1/manpath.1*
%{_mandir}/man1/whatis.1*
%{_mandir}/man5/manpath.5*
%{_mandir}/man8/accessdb.8*
%{_mandir}/man8/catman.8*
%{_mandir}/man8/mandb.8*
%lang(zh_CN)   %{_datadir}/man/zh_CN/man*/*

%changelog
* Sat Aug 09 2014 Liu Di <liudidi@gmail.com> - 2.6.7.1-1
- 更新到 2.6.7.1

* Tue Oct 30 2012 Peter Schiffer <pschiffe@redhat.com> - 2.6.3-2
- resolves: #870680
  use less as the default pager

* Wed Oct 24 2012 Peter Schiffer <pschiffe@redhat.com> - 2.6.3-1
- resolves: #858577
  updated to 2.6.3
- cleaned .spec file
- resolves: #855632
  fixed SIGABRT crash
- adds support for man-pages-overrides

* Tue Jul 31 2012 Peter Schiffer <pschiffe@redhat.com> - 2.6.2-5
- resolves: #841431
  ignore cached man pages if they don't exist anymore

* Fri Jul 20 2012 Dan Horák <dan[at]danny.cz> - 2.6.2-4
- fully patch the autotools files, fixes FTBFS due updated automake

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 12 2012 Peter Schiffer <pschiffe@redhat.com> - 2.6.2-2
- resolves: #829553
  clear the old man cache on install or update

* Tue Jul 10 2012 Peter Schiffer <pschiffe@redhat.com> - 2.6.2-1
- resolves: #833312
  update to 2.6.2
- resolves: #657409
  fixed warning when invoking col by the mandb program in cron
- resolves: #829935
  enabled support for man pages compressed with lzip
- resolves: #821778
  added virtual provides for bundled gnulib library
- resolves: #824825
  apropos returns correct exit code for invalid man page

* Tue Apr 24 2012 Peter Schiffer <pschiffe@redhat.com> - 2.6.1-4
- related: #693458
  updated patch for .so links because previous one wasn't working very well

* Tue Apr 24 2012 Peter Schiffer <pschiffe@redhat.com> - 2.6.1-3
- added autoconf, automake, libtool and gettext-devel to the build requires

* Tue Apr 24 2012 Peter Schiffer <pschiffe@redhat.com> - 2.6.1-2
- resolves: #677669
  added support for wildcards in path
- resolves: #693458
  fixed error with .so links

* Thu Apr 05 2012 Peter Schiffer <pschiffe@redhat.com> - 2.6.1-1
- resolves: #790771
  update to 2.6.1
- resolves: #806086
  removed hard-dependency on cron, update man db after install or update

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 05 2011 Peter Schiffer <pschiffe@redhat.com> - 2.6.0.2-3
- resolves: #702904
  fixed double free or corruption issue
- resolves: #739207
  require groff-base instead of groff
- rebuilt for gdbm-1.9.1-1

* Sun May 29 2011 Ville Skyttä <ville.skytta@iki.fi> - 2.6.0.2-2
- Own the %%{_libdir}/man-db dir.

* Thu Apr 21 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 2.6.0.2-1
- update to 2.6.0.2
- remove obsolete patches
- add libpipe dependency

* Wed Mar 23 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 2.5.9-6
- Build with zlib support.
- Use elinks as default HTML browser.
   thanks Ville Skyttä

* Wed Mar 23 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 2.5.9-5
* Resolves: #684977
  backport upstream patch

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 27 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 2.5.9-3
- Resolves: #659292
  use ionice in man cron job

* Wed Nov 24 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 2.5.9-2
- Resolves: #655385 - use old format of nroff output

* Mon Nov 22 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 2.5.9-1
- update to 2.5.9

* Fri Oct  1 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 2.5.7-8
- add less buildrequire

* Wed Sep 29 2010 jkeating - 2.5.7-7
- Rebuilt for gcc bug 634757

* Fri Sep 24 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 2.5.7-6
- Resolves: #630506 (change the description)
- minor spec file changes

* Mon Aug 30 2010 Dennis Gilmore <dennis@ausil.us> - 2.5.7-5
- Provide Versioned man

* Mon Aug 16 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 2.5.7-4
- remove obsolete conflict flag

* Mon Aug 16 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 2.5.7-3
- provides man tag
- resolves: #621688
  remove problematic man-pages (now in man-pages-de package)

* Fri Apr 16 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 2.5.7-2
- add conflicts tag

* Wed Feb 17 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 2.5.7-1
- initial build
