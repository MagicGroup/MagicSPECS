Summary: Statically linked binary providing simplified versions of system commands
Summary(zh_CN.UTF-8): 系统命令的静态链接简单版本
Name: busybox
Version: 1.24.1
Release: 7%{?dist}
Epoch: 1
License: GPLv2
Group: System Environment/Shells
Group(zh_CN.UTF-8): 系统环境/外壳
Source: http://www.busybox.net/downloads/%{name}-%{version}.tar.bz2
Source1: busybox-static.config
Source2: busybox-petitboot.config
Patch1: http://www.busybox.net/downloads/fixes-1.22.1/busybox-1.22.1-ash.patch
Patch2: http://www.busybox.net/downloads/fixes-1.22.1/busybox-1.22.1-date.patch
Patch3: http://www.busybox.net/downloads/fixes-1.22.1/busybox-1.22.1-iplink.patch
Patch4: http://www.busybox.net/downloads/fixes-1.22.1/busybox-1.22.1-nc.patch

Obsoletes: busybox-anaconda
URL: http://www.busybox.net
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: glibc-static
# This package used to include a bundled copy of uClibc, but we now
# use the system copy.
%ifnarch ppc64
BuildRequires: uClibc-static
%endif

%package petitboot
Group: System Environment/Shells
Group(zh_CN.UTF-8): 系统环境/外壳
Summary: Version of busybox configured for use with petitboot
Summary(zh_CN.UTF-8): 使用 petitboot 的 busybox 版本

%description
Busybox is a single binary which includes versions of a large number
of system commands, including a shell.  This package can be very
useful for recovering from certain types of system failures,
particularly those involving broken shared libraries.

%description -l zh_CN.UTF-8
BusyBox可以被自定义化以提供一个超过两百种功能的子集。它可以提供多数详
列在单一UNIX规范里的功能，以及许多用户会想在 Linux 系统上看到的功能。
BusyBox 使用ash。在 BusyBox的网站上可以找到所有功能的列表。

%description petitboot
Busybox is a single binary which includes versions of a large number
of system commands, including a shell.  The version contained in this
package is a minimal configuration intended for use with the Petitboot
bootloader used on PlayStation 3. The busybox package provides a binary
better suited to normal use.

%description petitboot -l zh_CN.UTF-8
BusyBox可以被自定义化以提供一个超过两百种功能的子集。它可以提供多数详
列在单一UNIX规范里的功能，以及许多用户会想在 Linux 系统上看到的功能。
BusyBox 使用ash。在 BusyBox的网站上可以找到所有功能的列表。

这个包是给 PlayStation 3 启动用的，一般情况使用 busybox 包即可。

%prep
%setup -q
%patch1 -b .uname -p1
%patch2 -b .ext2_fs_h -p1
%patch3 -p1
%patch4 -p1

%build
# create static busybox - the executable is kept as busybox-static
# We use uclibc instead of system glibc, uclibc is several times
# smaller, this is important for static build.
# uclibc can't be built on ppc64,s390,ia64, we set $arch to "" in this case
arch=`uname -m | sed -e 's/i.86/i386/' -e 's/ppc/powerpc/' -e 's/armv7l/arm/' -e 's/armv5tel/arm/' -e 's/ppc64//' -e 's/powerpc64//' -e 's/ia64//' -e 's/s390.*//'`
cp %{SOURCE1} .config
# set all new options to defaults
yes "" | make oldconfig
# gcc needs to be convinced to use neither system headers, nor libs,
# nor startfiles (i.e. crtXXX.o files)
if test "$arch"; then \
    mv .config .config1 && \
    grep -v ^CONFIG_SELINUX .config1 >.config && \
    yes "" | make oldconfig && \
    cat .config && \
    make V=1 \
        EXTRA_CFLAGS="-g -isystem %{_includedir}/uClibc" \
        CFLAGS_busybox="-static -nostartfiles -L%{_libdir}/uClibc %{_libdir}/uClibc/crt1.o %{_libdir}/uClibc/crti.o %{_libdir}/uClibc/crtn.o"; \
else \
    mv .config .config1 && \
    grep -v \
        -e ^CONFIG_FEATURE_HAVE_RPC \
        -e ^CONFIG_FEATURE_MOUNT_NFS \
        -e ^CONFIG_FEATURE_INETD_RPC \
        .config1 >.config && \
    echo "# CONFIG_FEATURE_HAVE_RPC is not set" >>.config && \
    echo "# CONFIG_FEATURE_MOUNT_NFS is not set" >>.config && \
    echo "# CONFIG_FEATURE_INETD_RPC is not set" >>.config && \
    yes "" | make oldconfig && \
    cat .config && \
    make V=1 CC="gcc $RPM_OPT_FLAGS"; \
fi
cp busybox_unstripped busybox.static
cp docs/busybox.1 docs/busybox.static.1

# create busybox optimized for petitboot
make clean
# copy new configuration file
cp %{SOURCE2} .config
# set all new options to defaults
yes "" | make oldconfig
# -g is needed for generation of debuginfo.
# (Don't want to use full-blown $RPM_OPT_FLAGS for this,
# it makes binary much bigger: -O2 instead of -Os, many other options)
if test "$arch"; then \
    make V=1 \
        EXTRA_CFLAGS="-g -isystem %{_includedir}/uClibc" \
        CFLAGS_busybox="-static -nostartfiles -L%{_libdir}/uClibc %{_libdir}/uClibc/crt1.o %{_libdir}/uClibc/crti.o %{_libdir}/uClibc/crtn.o"; \
else \
    make V=1 CC="%__cc $RPM_OPT_FLAGS"; \
fi
cp busybox_unstripped busybox.petitboot
cp docs/busybox.1 docs/busybox.petitboot.1

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
install -m 755 busybox.static $RPM_BUILD_ROOT%{_sbindir}/busybox
install -m 755 busybox.petitboot $RPM_BUILD_ROOT%{_sbindir}/busybox.petitboot
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1
install -m 644 docs/busybox.static.1 $RPM_BUILD_ROOT/%{_mandir}/man1/busybox.1
install -m 644 docs/busybox.petitboot.1 $RPM_BUILD_ROOT/%{_mandir}/man1/busybox.petitboot.1

magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc LICENSE README
%{_sbindir}/busybox
%{_mandir}/man1/busybox.1.gz

%files petitboot
%defattr(-,root,root,-)
%doc LICENSE README
%{_sbindir}/busybox.petitboot
%{_mandir}/man1/busybox.petitboot.1.gz

%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 1:1.24.1-7
- 更新到 1.24.1

* Fri Mar 07 2014 Liu Di <liudidi@gmail.com> - 1:1.22.1-6
- 更新到 1.22.1

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 1:1.19.4-5
- 为 Magic 3.0 重建

* Fri Apr 13 2012 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.19.4-4
- Fixed breakage with newer kernel headers
- Excluded Sun-RPC dependednt features not available in newer static glibc

* Mon Mar 12 2012 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.19.4-3
- Tweaked spec file again to generate even more proper debuginfo package

* Wed Mar  7 2012 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.19.4-2
- Tweaked spec file to generate proper debuginfo package

* Tue Feb 28 2012 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.19.4-1
- update to 1.19.4

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.19.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 31 2011 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.19.3-1
- update to 1.19.3

* Sat Aug 27 2011 Daniel Drake <dsd@laptop.org> - 1:1.18.2-6
- Fix compilation against uClibc and Linux-3.0 headers

* Fri Aug 26 2011 Daniel Drake <dsd@laptop.org> - 1:1.18.2-5
- Remove Linux 2.4 support from insmod/modprobe/etc.
- Fixes build failures on ARM, where such ancient syscalls are not present

* Sat Jun 11 2011 Peter Robinson <pbrobinson@gmail.com> - 1:1.18.2-4
- Add support for ARM

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.18.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb  7 2011 Tom Callaway <spot@fedoraproject.org> - 1:1.18.2-2
- apply fixes from upstream

* Mon Feb  7 2011 Tom Callaway <spot@fedoraproject.org> - 1:1.18.2-1
- update to 1.18.2
- use system uClibc

* Mon Oct  4 2010 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.15.1-10
- add compatibility with man-db config file (#639461)

* Wed Sep 29 2010 jkeating - 1:1.15.1-9
- Rebuilt for gcc bug 634757

* Fri Sep 17 2010 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.15.1-8
- fix build system so that it works with make 3.82 too

* Wed May  5 2010 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.15.1-7
- teach uclibc to use /etc/localtime

* Wed Feb 24 2010 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.15.1-6
- tweak installed docs

* Wed Jan 27 2010 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.15.1-5
- enable Fedora-specific uname -p behavior (#534081)

* Fri Nov 26 2009 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.15.1-4
- make uclibc use 32-bit compat struct utmp (#541587)

* Fri Nov 10 2009 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.15.1-3
- re-enable rpm applet (#534092)

* Fri Oct  2 2009 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.15.1-2
- add manpage generation (#525658)

* Sun Sep 13 2009 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.15.1-1
- Rebase to 1.15.1

* Fri Sep 11 2009 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.14.1-6
- REALLY fix build on s390, ia64

* Fri Sep 11 2009 Denys Vlasenko <dvlasenk@redhat.com> - 1:1.14.1-5
- fix build on s390, ia64

* Wed Sep 02 2009 Chris Lumens <clumens@redhat.com> 1.14.1-4
- Remove busybox-anaconda (#514319).

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.14.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 12 2009 Ivana Varekova <varekova@redhat.com> - 1:1.14.1-2
- add new options to readlink - patch created by Denys Valsenko

* Thu May 28 2009 Ivana Varekova <varekova@redhat.com> - 1:1.14.1-1
- fix ppc problem
- update to 1.14.1

* Sun May 24 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 1:1.13.2-4
- Fixing FTBFS on i586/x86_64/ppc, ppc64 still an issue:
- Updated uClibc to 0.9.30.1, subsequently:
- Removed uClibc-0.9.30 patch (merged upstream).
- Added uClibc-0.9.30.1-getline.patch -- prevents conflicts with getline()
  from stdio.h
- Temporarily disable C99 math to bypass ppc bug, see https://bugs.uclibc.org/show_bug.cgi?id=55

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.13.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb  9 2009 Ivana Varekova <varekova@redhat.com> - 1:1.13.2-2
- use uClibc instead of glibc for static build - thanks Denys Vlasenko

* Mon Jan 19 2009 Ivana Varekova <varekova@redhat.com> - 1:1.13.2-1
- update to 1.13.2

* Tue Dec  2 2008 Ivana Varekova <varekova@redhat.com> - 1:1.12.1-2
- enable selinux in static version of busybox (#462724)

* Mon Nov 10 2008 Ivana Varekova <varekova@redhat.com> - 1:1.12.1-1
- update to 1.12.1

* Tue Aug 26 2008 Ivana Varekova <varekova@redhat.com> - 1:1.10.3-3
- fix findfs problem - #455998

* Wed Jul 23 2008 Ivana Varekova <varekova@redhat.com> - 1:1.10.3-2
- add findfs to static version of busybox 
  (kexec-tools need it #455998)

* Tue Jun 10 2008 Ivana Varekova <varekova@redhat.com> - 1:1.10.3-1
- update to 1.10.3

* Fri May 16 2008 Ivana Varekova <varekova@redhat.com> - 1:1.10.2-1
- update to 1.10.2

* Thu May  9 2008 Ivana Varekova <varekova@redhat.com> - 1:1.10.1-1
- update to 1.10.1

* Thu Feb 14 2008 Ivana Varekova <varekova@redhat.com> - 1:1.9.1-1
- update to 1.9.1
- fix a problem with netfilter.h - thanks dwmw2

* Fri Feb  8 2008 Ivana Varekova <varekova@redhat.com> - 1:1.9.0-2
- fix hwclock on ia64 machines

* Mon Jan  7 2008 Ivana Varekova <varekova@redhat.com> - 1:1.9.0-1
- update to 1.9.0

* Mon Dec  3 2007 Ivana Varekova <varekova@redhat.com> - 1:1.8.2-1
- update to 1.8.2

* Wed Nov 21 2007 Ivana Varekova <varekova@redhat.com> - 1:1.8.1-1
- update to 1.8.1

* Tue Nov  6 2007 Ivana Varekova <varekova@redhat.com> - 1:1.7.3-1
- update to 1.7.3 
- remove --gc-sections from static build Makefile

* Thu Nov  1 2007 Ivana Varekova <varekova@redhat.com> - 1:1.7.2-4
- fix 359371 - problem with grep output

* Wed Oct 31 2007 Ivana Varekova <varekova@redhat.com> - 1:1.7.2-3
- fix another sed problem (forgotten fflush - #356111)

* Mon Oct 29 2007 Ivana Varekova <varekova@redhat.com> - 1:1.7.2-2
- fix sed problem with output (#356111)

* Mon Oct 22 2007 Ivana Varekova <varekova@redhat.com> - 1:1.7.2-1
- update to 1.7.2
 
* Tue Sep  4 2007 Ivana Varekova <varekova@redhat.com> - 1:1.6.1-2
- spec file cleanup

* Mon Jul 23 2007 Ivana Varekova <varekova@redhat.com> - 1:1.6.1-1
- update to 1.6.1

* Fri Jun  1 2007 Ivana Varekova <varekova@redhat.com> - 1:1.5.1-2
- add msh shell

* Thu May 24 2007 Ivana Varekova <varekova@redhat.com> - 1:1.5.1-1
- update to 1.5.1

* Sat Apr  7 2007 David Woodhouse <dwmw2@redhat.com> - 1:1.2.2-8
- Add busybox-petitboot subpackage

* Mon Apr  2 2007 Ivana Varekova <varekova@redhat.com> - 1:1.2.2-7
- Resolves: 234769 
  busybox ls does not work without a tty

* Mon Feb 19 2007 Ivana Varekova <varekova@redhat.com> - 1:1.2.2-6
- incorporate package review feedback

* Fri Feb  2 2007 Ivana Varekova <varekova@redhat.com> - 1:1.2.2-5
- fix id_ps patch (thanks Chris MacGregor)

* Tue Jan 30 2007 Ivana Varekova <varekova@redhat.com> - 1:1.2.2-4
- remove debuginfo

* Mon Jan 22 2007 Ivana Varekova <varekova@redhat.com> - 1:1.2.2-3
- Resolves: 223620
  id output shows context twice
- fix iptunnel x kernel-headers problem

* Mon Dec 10 2006 Ivana Varekova <varekova@redhat.com> - 1:1.2.2-2
- enable ash 

* Thu Nov 16 2006 Ivana Varekova <varekova@redhat.com> - 1:1.2.2-1
- update to 1.2.2

* Mon Aug 28 2006 Ivana Varekova <varekova@redhat.com> - 1:1.2.0-3
- fix #200470 - dmesg aborts
  backport dmesg upstream changes

* Mon Aug 28 2006 Ivana Varekova <varekova@redhat.com> - 1:1.2.0-2
- fix #202891 - tar problem

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:1.2.0-1.1
- rebuild

* Tue Jul  4 2006 Ivana Varekova <varekova@redhat.com> - 1:1.2.0-1
- update to 1.2.0

* Thu Jun  8 2006 Jeremy Katz <katzj@redhat.com> - 1:1.1.3-2
- fix so that busybox.anaconda has sh

* Wed May 31 2006 Ivana Varekova <varekova@redhat.com> - 1:1.1.3-1
- update to 1.1.3

* Mon May 29 2006 Ivana Varekova <varekova@redhat.com> - 1:1.1.2-3
- fix Makefile typo (#193354)

* Fri May  5 2006 Ivana Varekova <varekova@redhat.com> - 1:1.1.2-1
- update to 1.1.2

* Thu May  4 2006 Ivana Varekova <varekova@redhat.com> - 1:1.1.1-2
- add -Z option to id command, rename ps command -Z option (#190534)

* Wed May 03 2006 Ivana Varekova <varekova@redhat.com> - 1:1.1.1-1
- update to 1.1.1
- fix CVE-2006-1058 - BusyBox passwd command 
  fails to generate password with salt (#187386)
- add -minimal-toc option
- add RPM_OPT_FLAGS
- remove asm/page.h used sysconf command to get PAGE_SIZE
- add overfl patch to aviod Buffer warning

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:1.01-2.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:1.01-2.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Oct 13 2005 Daniel Walsh <dwalsh@redhat.com> -  1.01-2
- Add sepol for linking load_policy

* Thu Sep  1 2005 Ivana Varekova <varekova@redhat.com> - 1.01-1
- update to 1.01
 
* Tue May 11 2005 Ivana Varekova <varekova@redhat.com> - 1.00-5
- add debug files to debug_package

* Mon Mar  7 2005 Ivana Varekova <varekova@redhat.com> - 1.00-4
- rebuilt

* Wed Jan 26 2005 Ivana Varekova <varekova@redhat.com> - 1.00-3
- update to 1.00 - fix bug #145681
- rebuild

* Thu Jan 13 2005 Jeremy Katz <katzj@redhat.com> - 1.00.rc1-6
- enable ash as the shell in busybox-anaconda

* Sat Oct  2 2004 Bill Nottingham <notting@redhat.com> - 1.00.rc1-5
- fix segfault in SELinux patch (#134404, #134406)

* Fri Sep 17 2004 Phil Knirsch <pknirsch@redhat.com> - 1.00.rc1-4
- Fixed double free in freecon() call (#132809)

* Fri Sep 10 2004 Daniel Walsh <dwalsh@redhat.com> - 1.00.rc1-3
- Add CONFIG_STATIC=y for static builds

* Wed Aug 25 2004 Jeremy Katz <katzj@redhat.com> - 1.00.rc1-2
- rebuild

* Fri Jun 25 2004 Dan Walsh <dwalsh@redhat.com> 1.00-pre10.1
- Add BuildRequires libselinux-devel
- Update to latest from upstream

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 11 2004 Karsten Hopp <karsten@redhat.de> 1.00.pre8-4 
- add mknod to busybox-anaconda

* Wed Apr 21 2004 Karsten Hopp <karsten@redhat.de> 1.00.pre8-3 
- fix LS_COLOR in anaconda patch

* Tue Mar 23 2004 Jeremy Katz <katzj@redhat.com> 1.00.pre8-2
- add awk to busybox-anaconda

* Sat Mar 20 2004 Dan Walsh <dwalsh@redhat.com> 1.00-pre8.1
- Update with latest patch. 
- Turn off LS_COLOR in static patch

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jan 27 2004 Dan Walsh <dwalsh@redhat.com> 1.00-pre5.2
- Fix is_selinux_enabled calls

* Mon Dec 29 2003 Dan Walsh <dwalsh@redhat.com> 1.00-pre5.1
-Latest update

* Wed Nov 26 2003 Dan Walsh <dwalsh@redhat.com> 1.00-pre3.2
- Add insmod

* Mon Sep 15 2003 Dan Walsh <dwalsh@redhat.com> 1.00-pre3.1
- Upgrade to pre3

* Thu Sep 11 2003 Dan Walsh <dwalsh@redhat.com> 1.00.2
- Upgrade selinux support

* Wed Jul 23 2003 Dan Walsh <dwalsh@redhat.com> 1.00.1
- Upgrade to 1.00 package

* Wed Jul 16 2003 Elliot Lee <sopwith@redhat.com> 0.60.5-10
- Rebuild

* Mon Jul 14 2003 Jeremy Katz <katzj@redhat.com> 0.60.5-9
- rebuild

* Mon Jul 14 2003 Jeremy Katz <katzj@redhat.com> 0.60.5-8
- add dmesg to busybox-anaconda

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Jan 13 2003 Jeremy Katz <katzj@redhat.com> 0.60.5-5
- lost nolock for anaconda mount when rediffing, it returns (#81764)

* Mon Jan 6 2003 Dan Walsh <dwalsh@redhat.com> 0.60.5-4
- Upstream developers wanted to eliminate the use of floats

* Thu Jan 3 2003 Dan Walsh <dwalsh@redhat.com> 0.60.5-3
- Fix free to work on large memory machines.

* Sat Dec 28 2002 Jeremy Katz <katzj@redhat.com> 0.60.5-2
- update Config.h for anaconda build to include more useful utils

* Thu Dec 19 2002 Dan Walsh <dwalsh@redhat.com> 0.60.5-1
- update latest release

* Thu Dec 19 2002 Dan Walsh <dwalsh@redhat.com> 0.60.2-8
- incorporate hammer changes

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon May 06 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- fix compilation on mainframe

* Tue Apr  2 2002 Jeremy Katz <katzj@redhat.com>
- fix static busybox (#60701)

* Thu Feb 28 2002 Jeremy Katz <katzj@redhat.com>
- don't include mknod in busybox.anaconda so we get collage mknod

* Fri Feb 22 2002 Jeremy Katz <katzj@redhat.com>
- rebuild in new environment

* Wed Jan 30 2002 Jeremy Katz <katzj@redhat.com>
- update to 0.60.2
- include more pieces for the anaconda version so that collage can go away
- make the mount in busybox.anaconda default to -onolock

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
`- automated rebuild

* Mon Jul  9 2001 Tim Powers <timp@redhat.com>
- don't obsolete sash
- fix URL and spelling in desc. to satisfy rpmlint

* Thu Jul 05 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add missing defattr for anaconda subpackage

* Thu Jun 28 2001 Erik Troan <ewt@redhat.com>
- initial build for Red Hat
