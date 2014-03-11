Summary: Ncurses support utilities
Name: ncurses
Version: 5.9
Release: 5.20120204%{?dist}
License: MIT
Group: System Environment/Base
URL: http://invisible-island.net/ncurses/ncurses.html
Source0: ftp://invisible-island.net/ncurses/ncurses-%{version}.tar.gz

Patch1: ncurses-5.9-20111224-patch.sh.bz2
Patch2: ncurses-5.9-20111231-20120204.patch.bz2
Patch8: ncurses-config.patch
Patch9: ncurses-libs.patch
Patch11: ncurses-urxvt.patch
Patch12: ncurses-kbs.patch
BuildRequires: gpm-devel pkgconfig
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: %{name}-libs = %{version}-%{release}

%description
The curses library routines are a terminal-independent method of
updating character screens with reasonable optimization.  The ncurses
(new curses) library is a freely distributable replacement for the
discontinued 4.4 BSD classic curses library.

This package contains support utilities, including a terminfo compiler
tic, a decompiler infocmp, clear, tput, tset, and a termcap conversion
tool captoinfo.

%package libs
Summary: Ncurses libraries
Group: System Environment/Libraries
Requires: %{name}-base = %{version}-%{release}
# libs introduced in 5.6-13 
Obsoletes: ncurses < 5.6-13
Conflicts: ncurses < 5.6-13
Obsoletes: libtermcap < 2.0.8-48

%description libs
The curses library routines are a terminal-independent method of
updating character screens with reasonable optimization.  The ncurses
(new curses) library is a freely distributable replacement for the
discontinued 4.4 BSD classic curses library.

This package contains the ncurses libraries.

%package base
Summary: Descriptions of common terminals
Group: System Environment/Base
Obsoletes: termcap < 1:5.5-2
# base introduced in 5.6-13 
Conflicts: ncurses < 5.6-13
# /lib -> /usr/lib move
Conflicts: filesystem < 3

%description base
This package contains descriptions of common terminals. Other terminal
descriptions are included in the ncurses-term package.

%package term
Summary: Terminal descriptions
Group: System Environment/Base
Requires: %{name}-base = %{version}-%{release}

%description term
This package contains additional terminal descriptions not found in
the ncurses-base package.

%package devel
Summary: Development files for the ncurses library
Group: Development/Libraries
Requires: %{name}-libs = %{version}-%{release}
Requires: pkgconfig
Obsoletes: libtermcap-devel < 2.0.8-48
Provides: libtermcap-devel = 2.0.8-48

%description devel
The header files and libraries for developing applications that use
the ncurses terminal handling library.

Install the ncurses-devel package if you want to develop applications
which will use ncurses.

%package static
Summary: Static libraries for the ncurses library
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description static
The ncurses-static package includes static libraries of the ncurses library.

%prep
%setup -q

%patch1 -p1
%patch2 -p1

%patch8 -p1 -b .config
%patch9 -p1 -b .libs
%patch11 -p1 -b .urxvt
%patch12 -p1 -b .kbs

# this will be in documentation, drop executable bits
cp -p install-sh test
find test -type f | xargs chmod 644

for f in ANNOUNCE; do
	iconv -f iso8859-1 -t utf8 -o ${f}{_,} &&
		touch -r ${f}{,_} && mv -f ${f}{_,}
done

%build
%define ncurses_options \\\
    --with-shared --without-ada --with-ospeed=unsigned \\\
    --enable-hard-tabs --enable-xmc-glitch --enable-colorfgbg \\\
    --with-terminfo-dirs=%{_sysconfdir}/terminfo:%{_datadir}/terminfo \\\
    --enable-overwrite \\\
    --enable-pc-files \\\
    --with-pkg-config-libdir=%{_libdir}/pkgconfig \\\
    --with-termlib=tinfo \\\
    --with-chtype=long

mkdir narrowc widec
cd narrowc
ln -s ../configure .
%configure %{ncurses_options} --with-ticlib
make %{?_smp_mflags} libs
make %{?_smp_mflags} -C progs

cd ../widec
ln -s ../configure .
%configure %{ncurses_options} --enable-widec --without-progs
make %{?_smp_mflags} libs
cd ..

%install
rm -rf ${RPM_BUILD_ROOT}

make -C narrowc DESTDIR=$RPM_BUILD_ROOT install.{libs,progs,data}
rm -f $RPM_BUILD_ROOT%{_libdir}/libtinfo.*
make -C widec DESTDIR=$RPM_BUILD_ROOT install.{libs,includes,man}

chmod 755 ${RPM_BUILD_ROOT}%{_libdir}/lib*.so.*.*
chmod 644 ${RPM_BUILD_ROOT}%{_libdir}/lib*.a

magic_rpm_clean.sh

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/terminfo

baseterms=

# prepare -base and -term file lists
for termname in \
    ansi dumb linux vt100 vt100-nav vt102 vt220 vt52 \
    Eterm\* aterm bterm cons25 cygwin eterm\* gnome gnome-256color hurd jfbterm \
    konsole konsole-256color mach\* mlterm mrxvt nsterm putty\* pcansi \
    rxvt rxvt-\* screen screen-\*color screen.\* sun teraterm teraterm2.3 \
    vte vte-256color vwmterm wsvt25\* xfce xterm xterm-\*
do
    for i in $RPM_BUILD_ROOT%{_datadir}/terminfo/?/$termname; do
        for t in $(find $RPM_BUILD_ROOT%{_datadir}/terminfo -samefile $i); do
            baseterms="$baseterms $(basename $t)"
        done
    done
done 2> /dev/null
for t in $baseterms; do
    echo "%dir %{_datadir}/terminfo/${t::1}"
    echo %{_datadir}/terminfo/${t::1}/$t
done 2> /dev/null | sort -u > terms.base
find $RPM_BUILD_ROOT%{_datadir}/terminfo \! -type d | \
    sed "s|^$RPM_BUILD_ROOT||" | while read t
do
    echo "%dir $(dirname $t)"
    echo $t
done 2> /dev/null | sort -u | comm -2 -3 - terms.base > terms.term

# can't replace directory with symlink (rpm bug), symlink all headers
mkdir $RPM_BUILD_ROOT%{_includedir}/ncurses{,w}
for l in $RPM_BUILD_ROOT%{_includedir}/*.h; do
    ln -s ../$(basename $l) $RPM_BUILD_ROOT%{_includedir}/ncurses
    ln -s ../$(basename $l) $RPM_BUILD_ROOT%{_includedir}/ncursesw
done

# don't require -ltinfo when linking with --no-add-needed
for l in $RPM_BUILD_ROOT%{_libdir}/libncurses{,w}.so; do
    soname=$(basename $(readlink $l))
    rm -f $l
    echo "INPUT($soname -ltinfo)" > $l
done

rm -f $RPM_BUILD_ROOT%{_libdir}/libcurses{,w}.so
echo "INPUT(-lncurses)" > $RPM_BUILD_ROOT%{_libdir}/libcurses.so
echo "INPUT(-lncursesw)" > $RPM_BUILD_ROOT%{_libdir}/libcursesw.so

echo "INPUT(-ltinfo)" > $RPM_BUILD_ROOT%{_libdir}/libtermcap.so

rm -f $RPM_BUILD_ROOT%{_libdir}/terminfo
rm -f $RPM_BUILD_ROOT%{_libdir}/pkgconfig/{*_g,ncurses++*}.pc

bzip2 NEWS

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc ANNOUNCE AUTHORS NEWS.bz2 README TO-DO
%{_bindir}/[cirt]*
%{_mandir}/man1/[cirt]*
%{_mandir}/man5/*
%{_mandir}/man7/*

%files libs
%defattr(-,root,root)
%{_libdir}/lib*.so.*

%files base -f terms.base
%defattr(-,root,root)
%doc README
%dir %{_sysconfdir}/terminfo
%{_datadir}/tabset
%dir %{_datadir}/terminfo

%files term -f terms.term
%defattr(-,root,root)

%files devel
%defattr(-,root,root)
%doc test
%doc doc/html/hackguide.html
%doc doc/html/ncurses-intro.html
%doc c++/README*
%doc misc/ncurses.supp
%{_bindir}/ncurses*-config
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%dir %{_includedir}/ncurses
%dir %{_includedir}/ncursesw
%{_includedir}/ncurses/*.h
%{_includedir}/ncursesw/*.h
%{_includedir}/*.h
%{_mandir}/man1/ncurses*-config*
%{_mandir}/man3/*

%files static
%defattr(-,root,root)
%{_libdir}/lib*.a

%clean
rm -rf ${RPM_BUILD_ROOT}

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 5.9-5.20120204
- 为 Magic 3.0 重建

* Wed Feb 08 2012 Miroslav Lichvar <mlichvar@redhat.com> 5.9-4.20120204
- move libs and terms to /usr
- update to patch 20120204

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9-3.20110716
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 18 2011 Miroslav Lichvar <mlichvar@redhat.com> 5.9-2.20110716
- update to patch 20110716
- update rxvt-unicode entry

* Tue Apr 05 2011 Miroslav Lichvar <mlichvar@redhat.com> 5.9-1
- update to 5.9

* Tue Mar 22 2011 Miroslav Lichvar <mlichvar@redhat.com> 5.8-2.20110319
- update to patch 20110319

* Wed Mar 02 2011 Miroslav Lichvar <mlichvar@redhat.com> 5.8-1
- update to 5.8

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.7-11.20101211
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 13 2010 Miroslav Lichvar <mlichvar@redhat.com> 5.7-10.20101211
- update to patch 20101211

* Mon Nov 29 2010 Miroslav Lichvar <mlichvar@redhat.com> 5.7-9.20101128
- update to patch 20101128
- update rxvt-unicode entry (#653081)

* Wed Jul 14 2010 Miroslav Lichvar <mlichvar@redhat.com> 5.7-8.20100703
- update to patch 20100703
- add README to base subpackage

* Wed Feb 03 2010 Miroslav Lichvar <mlichvar@redhat.com> 5.7-7.20100130
- update to patch 20100130
- fix ncursesw5-config and pc files to use correct tinfo

* Mon Jan 25 2010 Miroslav Lichvar <mlichvar@redhat.com> 5.7-6.20100123
- update to patch 20100123
- remove AS_NEEDED from linker scripts

* Wed Jan 20 2010 Miroslav Lichvar <mlichvar@redhat.com> 5.7-5.20100116
- fix narrow/wide libtinfo compatibility
- fix wattrset macro to not produce warning with current gcc (#556645)

* Mon Jan 18 2010 Miroslav Lichvar <mlichvar@redhat.com> 5.7-4.20100116
- update to patch 20100116
- don't require -ltinfo when linking with --no-add-needed

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.7-3.20090207
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.7-2.20090207
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 10 2009 Miroslav Lichvar <mlichvar@redhat.com> 5.7-1.20090207
- update to 5.7, patch 20090207
- use default pcf in xterm description
- include NEWS

* Thu Oct 02 2008 Miroslav Lichvar <mlichvar@redhat.com> 5.6-20.20080927
- update to patch 20080927

* Wed Jul 23 2008 Miroslav Lichvar <mlichvar@redhat.com> 5.6-19.20080628
- rebuild with new gpm

* Mon Jul 07 2008 Miroslav Lichvar <mlichvar@redhat.com> 5.6-18.20080628
- update to patch 20080628
- move mlterm and screen.* entries to -base
- change kbs to ^? in rxvt and screen entries

* Mon May 26 2008 Miroslav Lichvar <mlichvar@redhat.com> 5.6-17.20080524
- update to patch 20080524
- force installing wide libtinfo

* Fri Mar 07 2008 Miroslav Lichvar <mlichvar@redhat.com> 5.6-16.20080301
- update to patch 20080301
- provide libtermcap.so (#428898)
- move all headers to /usr/include
- move libncursesw out of /usr
- make examples in documentation compilable (#436355)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 5.6-15.20080112
- Autorebuild for GCC 4.3

* Tue Jan 15 2008 Miroslav Lichvar <mlichvar@redhat.com> 5.6-14.20080112
- obsolete libtermcap-devel (#428898)

* Mon Jan 14 2008 Miroslav Lichvar <mlichvar@redhat.com> 5.6-13.20080112
- update to patch 20080112
- make -libs, -base, -term subpackages
- obsolete termcap and libtermcap
- update urxvt entry

* Tue Oct 16 2007 Miroslav Lichvar <mlichvar@redhat.com> 5.6-12.20070812
- allocate additional working buffers in new_field (#310071)

* Wed Oct 10 2007 Miroslav Lichvar <mlichvar@redhat.com> 5.6-11.20070812
- don't write beyond field buffer in form driver (#310071)

* Thu Oct 04 2007 Miroslav Lichvar <mlichvar@redhat.com> 5.6-10.20070812
- fix comp_hash string output
- avoid comparing padding in cchar_t structure
- remove gawk from buildrequires

* Thu Aug 23 2007 Miroslav Lichvar <mlichvar@redhat.com> 5.6-9.20070812
- rebuild
- buildrequire gawk

* Mon Aug 13 2007 Miroslav Lichvar <mlichvar@redhat.com> 5.6-8.20070812
- update to patch 20070812

* Wed Jun 13 2007 Miroslav Lichvar <mlichvar@redhat.com> 5.6-7.20070612
- update to patch 20070612

* Thu Mar 08 2007 Miroslav Lichvar <mlichvar@redhat.com> 5.6-6.20070303
- update to patch 20070303
- use one libtinfo for both libncurses and libncursesw
- shorten -devel description

* Mon Feb 19 2007 Miroslav Lichvar <mlichvar@redhat.com> 5.6-5.20070217
- update to patch 20070217
- replace libcurses.so symlink with linker script (#228891)

* Mon Feb 12 2007 Miroslav Lichvar <mlichvar@redhat.com> 5.6-4.20070210
- update to patch 20070210
- generate separate terminfo library
- move static libraries to -static subpackage
- avoid unnecessary linking with libdl 

* Tue Feb 06 2007 Miroslav Lichvar <mlichvar@redhat.com> 5.6-3.20070203
- update to patch 20070203
- spec cleanup (#226188)

* Sun Jan 21 2007 Miroslav Lichvar <mlichvar@redhat.com> 5.6-2.20070120
- update to patch 20070120
- don't depend on bash, drop resetall script
- include rxvt-unicode description

* Wed Jan 10 2007 Miroslav Lichvar <mlichvar@redhat.com> 5.6-1.20070106
- update to 5.6, patch 20070106

* Mon Dec 11 2006 Miroslav Lichvar <mlichvar@redhat.com> 5.5-27.20061209
- update to patch 20061209
- strip large tables from shared libraries, reduce number of relocations
- package utils linked with libncurses instead of libncursesw
- package only wide-character headers

* Thu Nov 30 2006 Miroslav Lichvar <mlichvar@redhat.com> 5.5-26.20060715
- move also hardlinked entries (#217750)
- search /etc/terminfo for local terminfo entries

* Mon Nov 27 2006 Miroslav Lichvar <mlichvar@redhat.com> 5.5-25.20060715
- move libncurses and some terminfo entries out of /usr
- drop console symlink and sparc terminfo entries

* Thu Aug 31 2006 Miroslav Lichvar <mlichvar@redhat.com> 5.5-24.20060715
- modify tgetstr to make screen happy (#202480)
- use CFLAGS when linking (#199369)
- change BuildRoot tag to comply with Fedora packaging guidelines

* Wed Aug 16 2006 Miroslav Lichvar <mlichvar@redhat.com> 5.5-23.20060715
- fix another crash in tgetent (#202480)

* Mon Jul 17 2006 Miroslav Lichvar <mlichvar@redhat.com> 5.5-22.20060715
- update to patch 20060715
- fix package summary (#197655)

* Sat Jul 08 2006 Miroslav Lichvar <mlichvar@redhat.com> 5.5-21
- fix crash in tgetent (#198032)

* Fri Jul 07 2006 Miroslav Lichvar <mlichvar@redhat.com> 5.5-20
- update to patch 20060701
- don't strip libraries, chmod +x them
- move .so links to devel package
- add gpm-devel to buildrequires
- spec cleanup

* Mon Feb 27 2006 Miroslav Lichvar <mlichvar@redhat.com> - 5.5-19
- avoid comparing padding in cchar_t structure (#182024)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 5.5-18.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 5.5-18.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Jan 31 2006 Jindrich Novy <jnovy@redhat.com> 5.5-18
- add --with-chtype=long to avoid type clashes on x86_64 (#178824)
- spec cleanup

* Fri Jan 27 2006 Petr Raszyk <praszyk@redhat.com> 5.5-17
- Rebuild.

* Fri Jan 27 2006 Petr Raszyk <praszyk@redhat.com> 5.5-11
- According Henrik Nordstrom (hno@squid-cache.org)
  Diff between the two versions of curses.h on x86_64
  Patch ncurses-5.5-chtypeaslong2.patch
  See #178824

* Fri Dec 23 2005 Petr Raszyk <praszyk@redhat.com> 5.5-10
- Rebuild.

* Thu Dec 22 2005 Jindrich Novy <jnovy@redhat.com> 5.5-9
- helped Petr to strip libs. 

* Thu Dec 22 2005 Petr Raszyk <praszyk@redhat.com> 5.5-8
- Strip *.so libs.

* Wed Dec 21 2005 Petr Raszyk <praszyk@redhat.com> 5.5-1
- Upgrade to ncurses 5.5

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Thu Dec 1 2005 Petr Raszyk <praszyk@redhat.com> 5.4-23
- Rebuild.

* Thu Dec 1 2005 Petr Raszyk <praszyk@redhat.com> 5.4-22
- Rebuild.

* Thu Dec 1 2005 Petr Raszyk <praszyk@redhat.com> 5.4-21
- Clear window after: filter()+'terminal-resizing'+endwin()
  doupdate()+endwin()
  See bug #174498, patch ncurses-5.4-endwinfilter.patch

* Fri Nov 18 2005 Bill Nottingham <notting@redhat.com> 5.4-20
- fix location for resize in ncurses-resetall.sh

* Fri Sep 30 2005 5.4-19 <praszyk@redhat.com> 5.4-19
- Clear window after: filter()+initscr()+endwin()+refresh()
  See bug #2966, patch ncurses-5.4-filter.patch

* Wed Aug 03 2005 Karsten Hopp <karsten@redhat.de> 5.4-18
- rebuild with new rpm

* Wed Apr 27 2005 Petr Rockai <prockai@redhat.com> - 5.4-17
- apply patch from Hans de Goede, fixing BR142659 [The
  terminfo data for kbs changed from \177 to ^H]

* Sun Mar 06 2005 Petr Rockai <prockai@redhat.com>
- rebuild

* Thu Jan 27 2005 Adrian Havill <havill@redhat.com> 5.4-15
- update to newest jumbo monthly patch + weeklies, fixing
  new line cursor move problem (#140326)

* Wed Oct 21 2004 Adrian Havill <havill@redhat.com> 5.4-14
- escape rpm macros in the changelog (#135408)

* Tue Aug 31 2004 Adrian Havill <havill@redhat.com> 5.4-13
- term.sh can't detect CJK environment; revert
- gt 2.7 behaves better with xterm-new

* Tue Aug  3 2004 Adrian Havill <havill@redhat.com> 5.4-12
- make xterm same as xterm-r6
- detect for "dumb" in term.sh

* Thu Jul 29 2004 Adrian Havill <havill@redhat.com> 5.4-11
- add latest rollup patches and weekly patches
- remove home/end patch, which is now included in latest
  terminfo.src and termcap.src
- add term.sh to /etc/profile.d, reference in /etc/bashrc
- modify term.sh to support rxvt (#122815 comment 93)

* Fri Jul 08 2004 Adrian Havill <havill@redhat.com> 5.4-10
- add home/end mappings to gnome definition (#122815)

* Tue Jul 06 2004 Adrian Havill <havill@redhat.com> 5.4-9.fc3
- n-v-r

* Tue Jul 06 2004 Adrian Havill <havill@redhat.com> 5.4-9.fc2
- n-v-r

* Tue Jul 06 2004 Adrian Havill <havill@redhat.com> 5.4-9
- remove terminfo try-to-please-all xterm hackery; it's now ptty
  and profile's job to point to the correct terminal. (#122815)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun May 30 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- remove ncurses-c++-devel rpm, all files are also part of ncurses-devel

* Sat May 29 2004 Joe Orton <jorton@redhat.com> 5.4-6
- fix xterm terminfo entry (Hans de Geode, #122815)

* Thu May 06 2004 Adrian Havill <havill@redhat.com> 5.4-5
- remove --with-gpm from configure, as it adds a pkg
  dependency (#122336) and causes too many problems vs its benefits

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 26 2004 Adrian Havill <havill@redhat.com> 5.4-3
- xterm-color is wrong for rh; inverted bs/del (#115499)

* Wed Feb 25 2004 Adrian Havill <havill@redhat.com> 5.4-3
- link "xterm" to "xterm-color" as temp fix for escape problem (#115448)
- remove old zcat for PATCH1

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 10 2004 Adrian Havill <havill@redhat.com> 5.4-1
- version update to 5.4

* Thu Jan 29 2004 Adrian Havill <havill@redhat.com> 5.3-10
- add /usr/include/ncursesw (#112979)
- allow for non-gzipped man pages during the build process

* Sun Sep 21 2003 Matt Wilson <msw@redhat.com> 5.3-9.3
- remove the elf32/elf64 provides/obsoletes

* Wed Sep 17 2003 Matt Wilson <msw@redhat.com> 5.3-9.2
- rebuild to fix gzipped file md5sums (#91211)

* Thu Sep 11 2003 Adrian Havill <havill@redhat.com> 5.3-9.1
- RHEL bump

* Thu Sep 11 2003 Adrian Havill <havill@redhat.com> 5.3-9
- remove not-so safe-sprintf configure option because the code does
  not appear to be stable enough for some apps. (#103790)

* Wed Aug 20 2003 Adrian Havill <havill@redhat.com> 5.3-8.1
- RHEL bump

* Wed Aug 20 2003 Adrian Havill <havill@redhat.com> 5.3-8
- multilib patch (#91211)

* Mon Aug 11 2003 Adrian Havill <havill@redhat.com> 5.3-7
- fixed the safe sprintf code that was enabled in the previous release
  by the configure parameter. (#101486)

* Mon Jun 16 2003 Elliot Lee <sopwith@redhat.com> 5.3-6.1
- Fix ac25 patch, make it easy to turn off GPM support

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 22 2003 Adrian Havill <havill@redhat.com> 5.3-5
- added latest rollup patch with widec/UTF8 centric weekly (20030517)
- added --enable-widec to configure (#86311)
  original work done by Mr. Sam <sam@email-scan.com>
- require sharutils (#86605)
- add gpm, xmc support
- add debug syms back into package
- updated autoconf/configure patch

* Thu Feb  6 2003 Bill Nottingham <notting@redhat.com> 5.3-4
- fix debuginfo package

* Fri Jan 31 2003 Adrian Havill <havill@redhat.com> 5.3-3
- remunged xterm changes from 5.2 patch for 5.3
- updated screen entry (#82951)
- fixed ka3, kb2 and kf0 entries (#77506)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 22 2003 Adrian Havill <havill@redhat.com> 5.3-1
- upgrade to 5.3 for sake of utf-8, wide chars (#77585 ...)
- spec file summary/desc grammar (#73583)
- add Requires: for c++ devel subpkg (#74002)
- terminfo.src patches no longer needed
- adjust autoconf patch

* Thu Dec 05 2002 Elliot Lee <sopwith@redhat.com> 5.2-29
- Merge in multilib fixes

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Apr  8 2002 Bernhard Rosenkraenzer <bero@redhat.com> 5.2-26
- Remove duplicated files (#62752)
- Don't strip libraries (#60398)
- Remove cbt capability from xterm description (#61077)

* Mon Feb 25 2002 Bernhard Rosenkraenzer <bero@redhat.com> 5.2-25
- Remove bogus man pages
- Remove bool hack, it breaks make menuconfig

* Fri Feb 22 2002 Bernhard Rosenkraenzer <bero@redhat.com> 5.2-24
- Rebuild for glibc 2.3/gcc 3.1

* Fri Feb 22 2002 Bernhard Rosenkraenzer <bero@redhat.com> 5.2-23
- Put the bool type back in for !c++, but leave TRUE/FALSE out

* Thu Feb 21 2002 Bernhard Rosenkraenzer <bero@redhat.com> 5.2-21
- Don't define TRUE/FALSE etc., we don't care about SVR4 compliance and
  it breaks building gdb

* Thu Feb 21 2002 Bernhard Rosenkraenzer <bero@redhat.com> 5.2-20
- Rebuild for glibc 2.3/gcc 3.1

* Thu Feb 21 2002 Bernhard Rosenkraenzer <bero@redhat.com> 5.2-19
- Patchlevel 20020218
- Re-add %%{_includedir}/ncurses.h (#60169)

* Tue Feb 12 2002 Bernhard Rosenkraenzer <bero@redhat.com> 5.2-18
- Add C++ bindings (#59751)

* Tue Feb 12 2002 Bernhard Rosenkraenzer <bero@redhat.com> 5.2-17
- Patchlevel 20020209
- Fix zero-substitution of cf_cv_type_of_bool (#59450)
- Fix rebuilding of configure script with autoconf 2.5x

* Thu Jan 31 2002 Bernhard Rosenkraenzer <bero@redhat.com> 5.2-16
- Patchlevel 20020127

* Tue Nov 27 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.2-14
- Patchlevel 20011124

* Thu Sep 13 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.2-13
- Sync with patchlevel 20010908

* Fri Jul 20 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.2-12
- Sync terminfo with termcap 11.0.1-10

* Sun Jun 24 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.2-11
- Update to patchlevel 20010623, fixes some lynx issues

* Mon Jun 18 2001 Helge Deller <hdeller@redhat.de>
- fixed tput -S segfaulting bug (#44669)
- use _tmppath for BuildRoot:
- Copyright -> License

* Sun Apr 15 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Update to patchlevel 20010407

* Tue Mar  6 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix up some terminfo entries containing includes to
  "/var/tmp/ncurses-root/something" (#30771)

* Wed Feb 22 2001 Harald Hoyer <harald@redhat.de>
- fixed rxvt backspace setting

* Fri Feb  9 2001 Yukihiro Nakai <ynakai@redhat.com>
- Update Japanese kterm patch

* Mon Jan 15 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Update
- Add japanese patch from termcap
- Fix ospeed handling

* Mon Jan  1 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Add libcurses.a -> libncurses.a symlink (RFE #23023)

* Tue Dec 12 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Use --with-ospeed='unsigned int'

* Fri Nov 17 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix alpha and ia64
- Rebuild with gcc 2.96-64

* Thu Nov  2 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 5.2
- Fix typo in man page (Bug #20205)
- update the "screen" terminfo entries to the version supplied with
  screen 3.9.8

* Mon Oct  9 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Update (fixes the "make menuconfig" bug introduced by the security fix)

* Tue Oct  3 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix security problem (possible buffer overrun)

* Fri Aug  4 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Add the bugfix patches from the ncurses maintainer

* Thu Jul 13 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 5.1

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun  5 2000 Matt Wilson <msw@redhat.com>
- *don't ship symlinks from lib*.so.5 to lib*.so.4!
- use FHS macros

* Fri Jun  2 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- rebuild for 7.0
- /usr/share/man
- update URL for patches
- misc. fixes to spec file

* Mon Mar 20 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- use the real library version number
- update to 20000319

* Tue Mar  7 2000 Jeff Johnson <jbj@redhat.com>
- rebuild for sparc baud rates > 38400.

* Fri Feb 18 2000 Preston Brown <pbrown@redhat.com>
- xterm terminfo entries from XFree86 3.3.6
- final round of xterm fixes, follow debian policy.

* Sat Feb  5 2000 Bernhard Rosenkränzer <bero@redhat.com>
- strip libraries

* Thu Feb  3 2000 Bernhard Rosenkränzer <bero@redhat.com>
- More xterm fixes (Bug #9087)

* Thu Jan 27 2000 Bernhard Rosenkränzer <bero@redhat.com>
- More xterm fixes from Hans de Goede (Bug #8633)

* Sat Jan 15 2000 Bernhard Rosenkränzer <bero@redhat.com>
- remove some broken symlinks (leftovers from libncurses.so.5)
- Use %%configure (Bug #8484)

* Tue Jan 11 2000 Bernhard Rosenkränzer <bero@redhat.com>
- Add xterm patch from Hans de Goede <hans@highrise.nl>
- Patch 20000108, this fixes a problem with a header file.

* Wed Jan  5 2000 Bernhard Rosenkränzer <bero@redhat.com>
- Add 20000101 patch, hopefully finally fixing the xterm description

* Wed Dec 22 1999 Cristian Gafton <gafton@redhat.com>
- revert to the old major number - because the ABI is not changed (and we
  should be handling the changes via symbol versioning anyway)

* Fri Nov 12 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix a typo in spec
- Add the 19991006 patch, fixing some C++ STL compatibility problems.
- get rid of profiling and debugging versions - we need to save space...

* Thu Nov  4 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- 5.0
- some spec cleanups to make updating easier
- add links *.so.5 to *.so.4 - they are fully binary compatible.
  (Why did they change the invocation number???)

* Wed Sep 22 1999 Cristian Gafton <gafton@redhat.com>
- make clean in the test dir - don't ship any binaries at all.

* Mon Sep 13 1999 Preston Brown <pbrown@redhat.com>
- fixed stripping of test programs.

* Sun Aug 29 1999 Preston Brown <pbrown@redhat.com>
- removed 'flash' capability for xterm; see bug #2820 for details.

* Fri Aug 27 1999 Cristian Gafton <gafton@redhat.com>
- add the resetall script from Marc Merlin <marc@merlins.org>

* Fri Aug 27 1999 Preston Brown <pbrown@redhat.com>
- added iris-ansi-net as alias for iris-ansi (bug #2561)

* Fri Jul 30 1999 Michael K. Johnson <johnsonm@redhat.com>
- added ncurses-intro.hmtl and hackguide.html to -devel package [bug #3929]

* Tue Apr 06 1999 Preston Brown <pbrown@redhat.com>
- make sure ALL binaries are stripped (incl. test binaries)

* Thu Mar 25 1999 Preston Brown <pbrown@redhat.com>
- made xterm terminfo stuff MUCH better.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 16)

* Sat Mar 13 1999 Cristian Gafton <gafton@redhat.com>
- fixed header for C++ compiles

* Fri Mar 12 1999 Jeff Johnson <jbj@redhat.com>
- add terminfo entries for linux/linux-m on sparc (obsolete termfile_sparc).

* Thu Feb 18 1999 Cristian Gafton <gafton@redhat.com>
- updated patchset from original site

* Thu Dec 03 1998 Cristian Gafton <gafton@redhat.com>
- don't build the C++ demo code
- update patch set to the current as of today (redid all the individual
  patches in a single one)

* Wed Oct 14 1998 Cristian Gafton <gafton@redhat.com>
- make sure to strip the binaries

* Wed Sep 23 1998 Cristian Gafton <gafton@redhat.com>
- added another zillion of patches. The spec file *is* ugly
- defattr

* Mon Jul 20 1998 Cristian Gafton <gafton@redhat.com>
- added lots of patches. This spec file is starting to look ugly

* Wed Jul 01 1998 Alan Cox <alan@redhat.com>
- Fix setuid trusting. Open termcap/info files as the real user.

* Wed May 06 1998 Cristian Gafton <gafton@redhat.com>
- added terminfo entry for the poor guys using lat1 and/or lat-2 on their
  consoles... Enjoy linux-lat ! Thanks, Erik !

* Tue Apr 21 1998 Cristian Gafton <gafton@redhat.com>
- new patch to get xterm-color and nxterm terminfo entries
- aliased them to rxvt, as that seems to satisfy everybody

* Sun Apr 12 1998 Cristian Gafton <gafton@redhat.com>
- added %%clean section

* Tue Apr 07 1998 Cristian Gafton <gafton@redhat.com>
- removed /usr/lib/terminfo symlink - we shouldn't need that

* Mon Apr 06 1998 Cristian Gafton <gafton@redhat.com>
- updated to 4.2 + patches
- added BuildRoot

* Sat Apr 04 1998 Cristian Gafton <gafton@redhat.com>
- rebuilt with egcs on alpha

* Wed Dec 31 1997 Erik Troan <ewt@redhat.com>
- version 7 didn't rebuild properly on the Alpha somehow -- no real changes
  are in this version

* Tue Dec 09 1997 Erik Troan <ewt@redhat.com>
- TIOCGWINSZ wasn't used properly

* Tue Jul 08 1997 Erik Troan <ewt@redhat.com>
- built against glibc, linked shared libs against -lc

