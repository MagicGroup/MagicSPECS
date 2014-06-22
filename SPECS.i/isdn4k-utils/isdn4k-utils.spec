%global _default_patch_fuzz 2
%global app_defaults_dir %{_datadir}/X11/app-defaults
%global interver CVS-2010-05-01
%global PIE -fpie

Summary: Utilities for configuring an ISDN subsystem
Name: isdn4k-utils
Version: 3.2
Release: 97%{?dist}
License: GPLv2+ and GPL+ and MIT and BSD and zlib
Group: Applications/System
Url: http://www.isdn4linux.de/

# license issue, remove the isdn_lzscomp.c and firmwares
# Also remove ./eurofile/src/wuauth/sigfix.c (non-free)
# and isdnlog/isdnlog/ora* (non-free)
# and isdnlog/tools/telrate (non-free)
# and pcbit/convhexbin.c (non-free, but replaced with a free copy)
Source0: ftp://ftp.isdn4linux.de/pub/isdn4linux/utils/isdn4k-utils-%{interver}-patched.tar.bz2
Source2: isdn.init
Source7: capi20.conf
Source8: capi.service
Source9: capiinit.8

Source10: 40-isdn.rules
Source11: isdn.service

Patch0: isdn4k-utils-CVS-2009-10-20-redhat.patch
Patch1: isdn4k-utils-CVS-2009-10-20-lib64.patch
Patch3: isdn4k-utils-man.patch
Patch4: isdn4k-utils-CVS-2004-11-18-autoconf25x.patch
Patch5: isdn4k-utils-0202131200-true.patch

Patch11: isdn4k-utils-statfs.patch
Patch12: isdn4k-utils-CVS-2005-03-09-xmon.patch
Patch13: isdn4k-utils-capiinit.patch
Patch16: isdn4k-utils-CVS-2006-07-20-capi.patch
Patch17: isdn4k-utils-misc-overflow-in-capi-subsystem.patch
Patch18: isdn4k-utils-sh-linux.patch
Patch19: isdn4k-utils-autoconf-2.6.4-quoting.patch
Patch20: isdn4k-utils-CVS-2010-05-01-capi.patch
Patch21: isdn4k-utils-CVS-2010-05-01-capi-soname.patch
Patch22: isdn4k-utils-CVS-2010-05-01-patched-vboxgetty-config.patch
Patch23: isdn-manpages.patch
Patch24: isdn4k-fix-ipppd.patch
Patch25: isdn4k-utils-capi20-link.patch
Patch26: isdn4k-utils-CVS-2010-05-01-patched-legal-fixes.patch
Patch27: isdn4k-utils-CVS-2010-05-01-patched-strict-aliasing.patch
Patch28: isdn4k-fix-Werror-format-security-ftbfs.patch
patch29: vbox-tcl-8.6.patch

Requires: udev >= 039-10.14.EL4
Requires: hwdata >= 0.146.18.EL-1
Requires: initscripts >= 5.92
Requires(pre): coreutils, chkconfig, /sbin/service, bzip2
Conflicts: filesystem < 3
Conflicts: udev <= 179-1
Requires: systemd-units >= 39-2

BuildRequires: openjade
BuildRequires: linuxdoc-tools
BuildRequires: ncurses-devel
BuildRequires: tcl-devel
BuildRequires: libpcap-devel
BuildRequires: libICE-devel
BuildRequires: libSM-devel
BuildRequires: libX11-devel
BuildRequires: libXaw-devel
BuildRequires: libXmu-devel
BuildRequires: libXpm-devel
BuildRequires: libXt-devel
BuildRequires: libXext-devel
BuildRequires: imake
BuildRequires: automake
BuildRequires: libtool
BuildRequires: ppp-devel
BuildRequires: systemd-units >= 39-2
# for /usr/bin/pod2man
%if 0%{?fedora} > 18 || 0%{?rhel} > 6
BuildRequires: perl-podlators
%endif

ExcludeArch: s390 s390x

%description
The isdn4k-utils package contains a collection of utilities needed for
configuring an ISDN subsystem.

%package devel
Summary: Header files for capi development
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The isdn4k-utils-devel package contains the header files required to develop
capi applications.

%package static
Summary: Static library for capi development
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}

%description static
The isdn4k-utils-devel package contains the capi static library required to
develop capi applications.

%package vboxgetty
Summary: ISDN voice box (getty)
Group: Applications/Communications
Requires: %{name}, tcl

%description vboxgetty
The vboxgetty package contains vboxgetty and vboxputty, needed for an
ISDN voice box.

%package -n xisdnload
Summary: An ISDN connection load average display for the X Window System
Group: Applications/System
Requires: %{name}

%description -n xisdnload
The xisdnload utility displays a periodically updated histogram of the
load average over your ISDN connection.

%package doc
Summary: Documentation for isdn4k-utils
Group: Documentation
Requires: %{name}

%description doc
The isdn4k-utils-doc package contains the documentation for isdn4k-utils.

%prep
%setup -q -n %{name}-%{interver}-patched
%patch0 -p1 -b .redhat
%patch1 -p1 -b .lib64

%patch3 -p1 -b .man
%patch4 -p1 -b .ac25x
%patch5 -p1 -b .true

%patch11 -p1 -b .statfs
%patch12 -p1 -b .xmon
%patch13 -p1 -b .capi
%patch16 -p1 -b .capi
%patch17 -p1 -b .misc-overflow
%patch18 -p1 -b .sh-support
%patch19 -p1 -b .quote
%patch20 -p1 -b .capinew
%patch21 -p1 -b .capi-soname
%patch22 -p1 -b .vboxgetty-config
%patch23 -p0 -b .manpages
%patch24 -p1 -b .fix-ipppd
%patch25 -p1 -b .capi20-link
%patch26 -p1 -b .legal
%patch27 -p1 -b .no-strict-aliasing
%patch28 -p1 -b .format-security
%patch29 -p1 -b .tcl8.6

# remove useless files
find -type d -name "CVS" | xargs rm -rf

# enable capi20.new
rm -rf capi20 && mv capi20.new capi20

# autoreconf for new autofoo
for i in */configure; do
	cd `dirname $i`
	autoreconf --force --install
	cd ..
done

# fix utf8 issue
for f in vbox/doc/de/vbox.txt.in imontty/imontty.8.in FAQ/tutorial/EN-i4l.sgml \
		isdnlog/README isdnlog/tools/rate-files.man \
		Mini-FAQ/isdn-faq.txt vbox/doc/de/vbox.sgml.in ; do
	iconv -f iso-8859-1 -t utf-8 < $f > ${f}_
	mv ${f}_ $f
done

%build
export CFLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE"

mv .config.rpm .config
echo CONFIG_GENMAN=y >>.config
echo CONFIG_FAQ=y >>.config
echo "CONFIG_FAQDIR='/usr/share/doc/isdn4k-utils'" >>.config
echo "CONFIG_DATADIR='%{_datadir}/isdn'" >>.config
echo "LIBDIR='%{_libdir}'" >>.config
echo "CONFIG_FIRMWAREDIR='%{_datadir}/isdn'" >>.config
echo "CONFIG_CARD_SBINDIR='%{_sbindir}'" >>.config
sed -e "s,',,g" .config > .config.h

make subconfig
make

%install
mkdir -p %{buildroot}/dev \
         %{buildroot}/etc/{rc.d/init.d,ppp,isdn} \
         %{buildroot}/var/{log/vbox,spool/vbox,lock/isdn} \
         %{buildroot}%{_sbindir} \
         %{buildroot}%{_bindir} \
         %{buildroot}%{_mandir}/man1 \
         %{buildroot}%{_mandir}/man4 \
         %{buildroot}%{_mandir}/man8

chmod 1777 %{buildroot}/var/spool/vbox
make install DESTDIR=%{buildroot} \
             DATADIR=%{_datadir}/isdn \
             XAPPLOADDIR=%{app_defaults_dir} \
             MANPATH=%{_mandir} \
             MANSUFFIX=1

touch %{buildroot}/etc/ppp/ioptions

if [ -f %{buildroot}/etc/isdn/isdn.conf.new ] ; then
  mv -f %{buildroot}/etc/isdn/isdn.conf.new %{buildroot}/etc/isdn/isdn.conf
fi

# build some more documentation
%ifnarch sparc
	pushd FAQ/tutorial
	sgml2txt EN-i4l.sgml
	sgml2html EN-i4l.sgml
	popd
%endif

# copy config files for isdnlog
mkdir -p %{buildroot}%{_datadir}/isdn
cp -f isdnlog/*.dat %{buildroot}%{_datadir}/isdn/
chmod 644 %{buildroot}%{_datadir}/isdn/*.dat

# delete files to avoid conflicts and don't package *.la files
rm -rf %{buildroot}/etc/isdn/stop \
       %{buildroot}/etc/drdsl/adsl.conf \
       %{buildroot}%{_bindir}/cdb* \
       %{buildroot}%{_includedir}/freecdb.h \
       %{buildroot}%{_includedir}/freecdbmake.h \
       %{buildroot}%{_libdir}/*.la \
       %{buildroot}%{_libdir}/capi/*.la \
       %{buildroot}%{_libdir}/capi/*.so \
       %{buildroot}%{_mandir}/man1/cdb* \
       %{buildroot}%{_mandir}/man3 \
       %{buildroot}%{_mandir}/man5/vboxtcl.5* \
       %{buildroot}%{_docdir}/isdn4k-utils \
       %{buildroot}%{_docdir}/vbox \
       %{buildroot}/usr/X11R6 \
       %{buildroot}/usr/lib*/X11

# install isdn startup script
mkdir -p %{buildroot}%{_libexecdir}
install -m0755 %{SOURCE2} %{buildroot}%{_libexecdir}/isdn
install -m0755 -d %{buildroot}%{_unitdir}
install -m0644 %{SOURCE11} %{buildroot}%{_unitdir}/isdn.service
install -m0644 %{SOURCE8} %{buildroot}%{_unitdir}/capi.service

mv %{buildroot}%{_mandir}/man8/.isdnctrl_conf.8 \
   %{buildroot}%{_mandir}/man8/isdnctrl_conf.8

# move doc file to avoid conflict
mv isdnlog/README isdnlog/README.isdnlog

# install man page for capiinit
install -m644 %{SOURCE9} %{buildroot}%{_mandir}/man8/

# install config file for capi
mkdir -p $RPM_BUILD_ROOT/etc
install -m 644 capiinit/capi.conf $RPM_BUILD_ROOT/etc
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT/etc

# add comment
echo "# config files" >> %{buildroot}/etc/ppp/ioptions

# install 40-isdn.rules, it's dropped from udev in F14 and later
%if 0%{?fedora} > 13 || 0%{?rhel} > 6
	mkdir -p %{buildroot}%{_libdir}/udev/rules.d/
	install -m 644 %{SOURCE10} %{buildroot}%{_libdir}/udev/rules.d/
%endif

# touch zone-de-dtag.cdb, create it later in %post to avoid multilib issue
# on machine with BIGENDIAN
> %{buildroot}/%{_datadir}/isdn/zone-de-dtag.cdb

%post
/sbin/ldconfig
%systemd_post isdn.service

%preun
%systemd_preun isdn.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart isdn.service

%triggerun -- %{name} < 3.2-77
# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del isdn >/dev/null 2>&1 || :
/bin/systemctl try-restart isdn.service >/dev/null 2>&1 || :

%files
%defattr(-,root,root,755)
%dir /etc/isdn
%dir /var/spool/vbox
%dir /var/log/vbox
%dir %{_datadir}/isdn
%dir %{_libdir}/capi
%verify(not md5 size mtime) %config(noreplace) /etc/isdn/*
%verify(not md5 size mtime) %config(noreplace) /etc/ppp/ioptions
%config(noreplace) /etc/ppp/peers/*
%config(noreplace) /etc/capi.conf
%config(noreplace) /etc/capi20.conf
%if 0%{?fedora} > 13 || 0%{?rhel} > 6
%{_libdir}/udev/rules.d/40-isdn.rules
%endif
%{_libdir}/pppd
%{_datadir}/isdn/*.dat
%{_datadir}/isdn/dest.cdb
%{_libdir}/*.so.*
%{_libdir}/capi/*.so.*
%defattr(755,root,root,755)
%{_sbindir}/avmcapictrl
%{_sbindir}/hisaxctrl
%{_sbindir}/icnctrl
%{_sbindir}/isdnctrl
%{_sbindir}/pcbitctl
%{_libexecdir}/isdn
%{_unitdir}/isdn.service
%{_unitdir}/capi.service
%{_bindir}/*
%{_sbindir}/capiinit
%{_sbindir}/imon
%{_sbindir}/imontty
%{_sbindir}/ipppd
%{_sbindir}/ipppstats
%{_sbindir}/iprofd
%{_sbindir}/isdnlog
%{_sbindir}/loopctrl
%{_sbindir}/mkzonedb
%{_sbindir}/rcapid
%{_sbindir}/vboxd
%defattr(644,root,root,755)
%doc COPYING README isdnlog/README.*
%doc isdnlog/tools/zone/de/01033/zred.dtag.bz2
%ghost %{_datadir}/isdn/zone-de-dtag.cdb
%{_mandir}/man1/*
%{_mandir}/man4/*
%{_mandir}/man5/*
%{_mandir}/man7/*
%{_mandir}/man8/*
%exclude %{_mandir}/man1/xmonisdn.1*
%exclude %{_mandir}/man1/xisdnload.1*
%exclude %{_mandir}/man5/vboxgetty.conf.5*
%exclude %{_mandir}/man8/vboxgetty.8*
%exclude %{_mandir}/man8/vboxputty.8*
%exclude %{_bindir}/xisdnload
%exclude %{_bindir}/xmonisdn

%files vboxgetty
%defattr(644,root,root,755)
%doc vbox/examples/vboxgetty*.example
%{_mandir}/man5/vboxgetty.conf.5*
%{_mandir}/man8/vboxgetty.8*
%{_mandir}/man8/vboxputty.8*
%defattr(755,root,root,755)
%{_sbindir}/vboxgetty
%{_sbindir}/vboxputty

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files static
%{_libdir}/*.a

%files -n xisdnload
%defattr(644,root,root,755)
%doc xmonisdn/README
%{app_defaults_dir}/*
%{_mandir}/man1/xisdnload.1*
%{_mandir}/man1/xmonisdn.1*
%defattr(755,root,root,755)
%{_bindir}/xisdnload
%{_bindir}/xmonisdn

%files doc
%defattr(-,root,root)
%doc isdnlog/FAQ
%doc vbox/examples/vbox.conf.example
%doc vbox/examples/vboxd.conf.example
%doc vbox/examples/vboxrc.example
%doc vbox/examples/standard.tcl.example
%doc vbox/examples/timeout.msg.example
%doc vbox/examples/beep.msg*
%doc vbox/examples/timeout*
%doc FAQ/tutorial/* FAQ/i4lfaq* Mini-FAQ/isdn-faq.txt
%lang(de) %doc vbox/doc/de/vbox.sgml vbox/doc/de/vbox.txt


%changelog
* Wed Jun 18 2014 Than Ngo <than@redhat.com> - 3.2-97
- fix bz#1106807, FTBFS

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-96
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 3.2-95
- Rebuilt for https://fedoraproject.org/wiki/Changes/f21tcl86

* Tue Jan 28 2014 Kyle McMartin <kyle@fedoraproject.org> - 3.2-94
- isdn4k-fix-ipppd.patch: fix build on aarch64 (and future arches)
- isdn4k-fix-Werror-format-security-ftbfs.patch: fix FTBFS with
  -Werror=format-security by explicitly using string types. (rhbz#1037140)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-93
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Apr 25 2013 Than Ngo <than@redhat.com> - 3.2-92
- build with -fno-strict-aliasing

* Wed Apr 03 2013 Than Ngo <than@redhat.com> - 3.2-91
- add rhel condition

* Fri Mar 01 2013 Than Ngo <than@redhat.com> - 3.2-90
- add BR perl-podlators for pod2man

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-89
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan  4 2013 Tom Callaway <spot@fedoraproject.org> - 3.2-88
- apply fixes to remove additional non-free items

* Thu Nov 15 2012 Than Ngo <than@redhat.com> - 3.2-87
- bz#875538, fix symbol lookup error
- bz#850173, Scriptlets replaced with new systemd macros

* Mon Oct 08 2012 Than Ngo <than@redhat.com> - 3.2-86
- drop support for < f14

* Mon Aug 20 2012 Than Ngo <than@redhat.com> - 3.2-85
- add missing %% symbol for triggerun

* Fri Jul 20 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 3.2-84
- revert ARM arch exclusion
- add simple patch to fix building on ARM
- cleanup spec

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-82
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 3.2-81
- install everything in /usr
  https://fedoraproject.org/wiki/Features/UsrMove

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-80
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug 15 2011 Kalev Lember <kalevlember@gmail.com> - 3.2-79
- Rebuilt for rpm bug #728707

* Thu Jul 21 2011 Than Ngo <than@redhat.com> - 3.2-78
- install correct service scripts

* Thu Jul 21 2011 Than Ngo <than@redhat.com> - 3.2-77
- bz#717397, systemd unit file for isdn service
- drop triggerpostun

* Tue Jul 12 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 3.2-76
- Apply systemd unit file for capi service

* Wed Mar 16 2011 Than Ngo <than@redhat.com> - 3.2-75
- apply patch to fix man pages, thanks to John Bradshaw
  bz#673794, bz#665079, bz#663637, bz#675715, bz#669053, bz#675676, bz#669081,
  bz#675604, bz#675679, bz#664335, bz#674204, bz#669091

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-74
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 3.2-73
- Rebuilt for gcc bug 634757

* Mon Sep 20 2010 Than Ngo <than@redhat.com> - 3.2-72
- bz#545469, put vboxgetty config file in correct directory
- fix wrong exit status in startup scrripts

* Fri May 14 2010 Than Ngo <than@redhat.com> - 3.2-71
- fix bz#566909, thanks to Louis Lagendijk
    - own LIBDIR/capi
    - fix loading of plugins
    - remove chkconfig capi off

* Tue May 04 2010 Than Ngo <than@redhat.com> - 3.2-70
- enable capi.new
- add 40-isdn.rules, it's dropped from udev in F14 and later
- fix multilib issue
- add subpackage doc

* Mon May 03 2010 Than Ngo <than@redhat.com> - 3.2-69
- fix quotation issue with autoconf-2.64
- fix bz#556056, split off -static subpackage
- fix bz#539020, FTBFS

* Fri Jan 15 2010 Than Ngo <than@redhat.com> - 3.2-68
- fix license
- cleanup

* Wed Oct 28 2009 Than Ngo <than@redhat.com> - 3.2-67
- drop useless BR libXp-devel

* Mon Oct 19 2009 Than Ngo <than@redhat.com> - 3.2-66
- add missing man pages
- add upstream fixes

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-65
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Feb 27 2009 Than Ngo <than@redhat.com> 3.2-64
- fix build problem

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-63
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 19 2009 Than Ngo <than@redhat.com> - 3.2-62
- fix #398121, capiplugin.so uses non-existent libcapi20.so
- fix CAPI overflow
- fix #471712, add sh architecture support

* Mon Oct 27 2008 Than Ngo <than@redhat.com> 3.2-61
- bz450370, fix multilib issue

* Thu Oct 02 2008 Than Ngo <than@redhat.com> 3.2-60
- rebuild

* Tue Aug 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> 3.2-59
- fix license tag

* Mon Mar 03 2008 Than Ngo <than@redhat.com> 3.2-58
- fix build issue with new gcc 

* Fri Feb 15 2008 Than Ngo <than@redhat.com> 3.2-57
- rebuild against gcc 4.3

* Mon Jan 07 2008 Than Ngo <than@redhat.com> 3.2-56
- rebuilt

* Thu Sep 27 2007 Than Ngo <than@redhat.com> -  3.2-55
- fix build issue with glibc

* Thu Feb 08 2007 Than Ngo <than@redhat.com> 3.2-54.fc7
- rebuild

* Wed Nov 29 2006 Karsten Hopp <karsten@redhat.com> 3.2-53.fc7
- rebuild with new libpcap

* Mon Nov 13 2006 Than Ngo <than@redhat.com> - 3.2-52.fc7
- fix #213233, require main package with %%{version}-%%{release}

* Mon Oct 30 2006 Than Ngo <than@redhat.com> 3.2-51
- move .so in -devel #203627

* Wed Jul 19 2006 Than Ngo <than@redhat.com> 3.2-50
- add pppd 2.4.4
- use isdn-header files from upstream

* Wed Jul 14 2006 Jesse Keating <jkeating@redhat.com> - 3.2-49
- rebuild
- add missing br automake libtool

* Wed May 31 2006 Than Ngo <than@redhat.com> 3.2-47
- add requires on libpcap-devel

* Mon May 15 2006 Than Ngo <than@redhat.com> 3.2-46
- fix #191754, buildrequire on libXext-devel

* Tue Apr 25 2006 Adam Jackson <ajackson@redhat.com> 3.2-45
- Rebuild for updated imake build rules

* Tue Apr 25 2006 Than Ngo <than@redhat.com> 3.2-44
- add capi service

* Wed Apr 19 2006 Than Ngo <than@redhat.com> 3.2-43
- update to CVS-2006-02-13
- add support capi #169902

* Thu Mar 30 2006 Than Ngo <than@redhat.com> 3.2-42
- support pppd 2.4.3 #187218

* Fri Mar 10 2006 Than Ngo <than@redhat.com> 3.2-41
- add missing symlink for capi plugins #165198

* Wed Mar 01 2006 Karsten Hopp <karsten@redhat.de> 3.2-40
- Buildrequires: libXp-devel

* Fri Feb 17 2006 Than Ngo <than@redhat.com> 3.2-39 
- fix rpm file conflict #181854 

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.2-38.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.2-38.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Sun Dec 18 2005 Than Ngo <than@redhat.com> 3.2-38
- add correct app-defaults directory

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Wed Nov 16 2005 Than Ngo <than@redhat.com> 3.2-36
- fix for modular X

* Mon Nov 14 2005 Than Ngo <than@redhat.com> 3.2-35
- fix for modular X

* Sat Nov 12 2005 Florian La Roche <laroche@redhat.com>
- rebuild

* Tue Sep 13 2005 Than Ngo <than@redhat.com> 3.2-33
- cleanup %%post

* Wed Jul 27 2005 Than Ngo <than@redhat.com> 3.2-32 
- rebuilt

* Tue Jul 19 2005 Than Ngo <than@redhat.com> 3.2-31
- buildrequires on libpcap

* Mon Jul 18 2005 Than Ngo <than@redhat.com> 3.2-30 
- rebuild to fix broken dependencies

* Mon Jun 20 2005 Than Ngo <than@redhat.com> 3.2-29
- workaround for loading isdn module at system startup #160831

* Fri May 27 2005 Bill Nottingham <notting@redhat.com> 3.2-28
- remove setuid bit from vboxbeep

* Wed Apr 20 2005 Martin Stransky <stransky@redhat.com> 3.2-27
- fix for large filesystems (#155441)

>>>>>>> 1.34
* Wed Mar 09 2005 Than Ngo <than@redhat.com> 3.2-26
- update cvs snapshot
- fix gcc4 build problem

* Sat Mar 05 2005 Than Ngo <than@redhat.com> 3.2-25
- rebuilt

* Wed Feb 16 2005 Than Ngo <than@redhat.com> 3.2-24
- update cvs snapshot
- use RPM_OPT_FLAGS

* Wed Feb 02 2005 Than Ngo <than@redhat.com> 3.2-23
- fix typo in isdn startup script

* Tue Jan 25 2005 Than Ngo <than@redhat.com> 3.2-22
- fix the bug in isdn startup script, #146057

* Wed Dec 01 2004 Than Ngo <than@redhat.com> 3.2-21
- fix some minor build problems #140941

* Sat Nov 20 2004 Miloslav Trmac <mitr@redhat.com> 3.2-20
- Convert imontty.8 to UTF-8

* Thu Nov 18 2004 Than Ngo <than@redhat.com> 3.2-19
- update cvs snapshot
- workaround, add capi devices

* Tue Oct 05 2004 Than Ngo <than@redhat.com> 3.2-18.p1.1
- add workaround for #134525

* Wed Sep 01 2004 Than Ngo <than@redhat.com> 3.2-17.p1.1
- get rid of CVS files, #131430

* Thu May 13 2004 Than Ngo <than@redhat.com> 3.2-16.p1.1
- fix build problem with gcc-3.4
- fix typo bug in isdnlog, bug #120568
- fix capiplugin for working with pppd 2.4.2, bug #125723

* Thu May 13 2004 Than Ngo <than@redhat.com> 3.2-15.p1.1
- add patch to enable PIE build of userisdnctl

* Tue May 11 2004 Than Ngo <than@redhat.com> 3.2-14.p1.1
- fixed usage message in isdndial, bug #122987

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 25 2004 Than Ngo <than@redhat.com> 3.2-13.p1
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 11 2004 Than Ngo <than@redhat.com> 3.2-11.p1 
- add fix to get isdnlog working with Fritz!Card PCI V2.0, bug #115205

* Wed Jan 21 2004 Than Ngo <than@redhat.com> 3.2-10.p1
- fix build problem with new libpcap

-* Wed Jan 14 2004 Than Ngo <than@redhat.com> 3.2-9.p1
- fixed permission problem

* Thu Dec 18 2003 Than Ngo <than@redhat.com> 3.2-8.p1
- fixed conflict problem with redhat-config-network

* Mon Dec 15 2003 Than Ngo <than@redhat.com> 3.2-7.p1
- add patch to build against new glibc

* Fri Dec 12 2003 Jens Petersen <petersen@redhat.com> - 3.2-6.p1
- rebuild for tcl 8.4

* Thu Oct 23 2003 Than Ngo <than@redhat.com> 3.2-5.p1
- fix ISDN script to work with new redhat-config-network

* Wed Oct 22 2003 Than Ngo <than@redhat.com> 3.2-4.p1
- allow using nickname
- cleanup isdn script

* Fri Oct 10 2003 Than Ngo <than@redhat.com> 3.2-3.p1
- fixed wrong version of xisdnload (bug #106616)

* Tue Sep 30 2003 Than Ngo <than@redhat.com> 3.2-2.p1
- cleanup specfile

* Tue Sep 30 2003 Than Ngo <than@redhat.com> 3.2-1.p1
- 3.2p1
- support IPPP_FILTER (bug #104928)
 
* Mon Aug 11 2003 Than Ngo <than@redhat.com> 3.1-77
- rebuilt

* Mon Aug 11 2003 Than Ngo <than@redhat.com> 3.1-76
- add patch to build isdn4k-utils without kernel-source (bug #101751)
- cleanup (bug #79641)
  
* Mon Aug 11 2003 Than Ngo <than@redhat.com> 3.1-75
- rebuilt

* Mon Aug 11 2003 Than Ngo <than@redhat.com> 3.1-74
- add tcl-devel in buildrequires (bug #102034)

* Mon Jun 30 2003 Than Ngo <than@redhat.com> 3.1-73
- added missing example files (bug #81687)
- move vboxgetty man page in vboxgetty subpackage

* Thu Jun 19 2003 Than Ngo <than@redhat.com> 3.1-71
- get rid of ipppcomp

* Tue Jun 10 2003 Than Ngo <than@redhat.com> 3.1-69
- fix incorrect error messages (bug #96931)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 28 2003 Than Ngo <than@redhat.com> 3.1-66.1
- fix buildrequires problem

* Fri May 23 2003 Than Ngo <than@redhat.com> 3.1-65
- add usage fix

* Thu May 22 2003 Jeremy Katz <katzj@redhat.com> 3.1-63
- fix build with gcc 3.3

* Mon Feb  3 2003 Than Ngo <than@redhat.com> 3.1-62
- remove excludearch x86_64
- add fPIC patch for x86_64

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Dec 10 2002 Tim Powers <timp@redhat.com> 3.1-60
- rebuild to fix broken tcltk deps

* Fri Nov  8 2002 Than Ngo <than@redhat.com> 3.1-59
- fix build problem
- for the present exclude x86_64, it needs kernel-source rpm for building

* Mon Jul 01 2002 Than Ngo <than@redhat.com> 3.1-58
- add userisdnctl, isdnup

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jun 18 2002 Than Ngo <than@redhat.com> 3.1-56
- don't forcibly strip binaries

* Fri Jun 14 2002 Than Ngo <than@redhat.com> 3.1-55
- fix a bug in pppdcapi plugin for working with pppd-2.4.1 (bug #64279)

* Thu May 23 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.1-54
- Update
- Fix build with gcc 3.1
- Fix build with current auto* tools

* Mon Apr  8 2002 Than Ngo <than@redhat.com> 3.1-53
- fix bug in loading hisax modul for Card Elsa Quickstep 1000 (bug #62892)

* Fri Feb 22 2002 Than Ngo <than@redhat.com> 3.1-52
- fix bug in isdnlog (bug #60013)
- fix bug in imon

* Wed Feb 21 2002 Than Ngo <than@redhat.com> 3.1-51
- fix bad memory allocation (enrico.scholz@informatik.tu-chemnitz.de), bug #60179

* Tue Feb 19 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.1-50
- new upstream, needed to switch isdnlog to EUR currency for contries that
  have it
- fix installation of pppcapiplugin man page
- don't build against 2.4.5 kernel headers, they're not compatible with
  2.4.17.

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Dec 05 2001 Than Ngo <than@redhat.com> 3.1-48
- new upstream
- remove some unused patch files
- move pppcapiplugin to /usr/lib/pppd, The plugin option now looks in here
- devel sub package
- buildreqquires: linuxdoc-tools

* Mon Oct 29 2001 Than Ngo <than@redhat.com> 3.1-47
- fixed symlinks bugs (bug #55306)
- fix a bug in converting of old isdn configuration (bug #55083)
- some hacks for ASUS COM ISDNLink ISA PnP

* Tue Aug 28 2001 Than Ngo <than@redhat.com> 3.1-46
- some hacks for Teles 16.3 PnP
- fix order of isdn script

* Tue Aug 21 2001 Than Ngo <than@redhat.com> 3.1-45
- fix bug #52044

* Wed Aug  8 2001 Than Ngo <than@redhat.com>
- use hardlinks instead softlinks

* Mon Jul 02 2001 Than Ngo <than@redhat.com>
- make isdnctrl executable by normal users (Bug #30803)
- fix a minor bug in triggerpostun
- fix rebuild problem in beehive if kernel-source is missed

* Tue Jun 26 2001 Than Ngo <than@redhat.com>
- split package into isdn4k-utils, isdn4k-utils-vboxgetty, xisdnload
- convert old isdn configuration format into new format
- add startup script for loading module and starting isdnlog

* Tue Jun 19 2001 Than Ngo <than@redhat.com>
- buildprereq: XFree86-devel ncurses-devel tcl (Bug #45048)

* Tue Jun 19 2001 Than Ngo <than@redhat.com>
- fix to build against kernel-2.4.5
- fix to build against XFree86-4.1.x
- exclude s390, s390x 

* Mon Feb 12 2001 Than Ngo <than@redhat.com>
- clean up specfile

* Sat Feb 10 2001 Than Ngo <than@redhat.com>
- fixed for building against new glibc
- added missing files: divertctrl, eiconctrl, actctrl

* Thu Feb 08 2001 Than Ngo <than@redhat.com>
- fixed file conflicts

* Wed Feb 07 2001 Than Ngo <than@redhat.com>
- updated ipppd, isdnctrl for working with kernel-2.4
- added missing BuildRequires

* Tue Feb 06 2001 Than Ngo <than@redhat.com>
- rebuild against to fix version mismatch in isdnlog

* Mon Nov 20 2000 Than Ngo <than@redhat.com>
- rebuilt to fix bad dir perms

* Wed Nov 01 2000 Than Ngo <than@redhat.com>
- added ibod, a ISDN MPPP bandwidth on demand daemon

* Thu Aug 3  2000 Than Ngo <than@redhat.de>
- add more documents
- and missing config files to isdnlog
- some fixes in vbox, isdnlog, vboxgetty
- mark ioptions as %%config(noreplace)
- add pppdcapiplugin
- add missing /sbin/ldconfig in %%post and %%postun
- fix to build on ia64 

* Thu Jul 13 2000 Than Ngo <than@redhat.de>
- fix to build as nonroot

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Fri Jun 30 2000 Than Ngo <than@redhat.de>
- add documents in %%doc instead make install doc

* Thu Jun 29 2000 Than Ngo <than@redhat.de>
- add some header files for isdn4k-utils
  (don't need kernel-sources anymore)
- update to v3.1pre1

* Fri Jun 16 2000 Than Ngo <than@redhat.de>
- rebuilt for 7.0
- FHS fixes
- fix dependencies problem with new tcltk
- fix to built with kernel-2.4

* Fri Apr 28 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- add /usr/lib/isdn to filelist

* Fri Mar 24 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- fix compilation with kernel 2.4.x
- rebuild with new ncurses and Tcl
- enable building of eurofile and divertctl stuff

* Tue Mar  7 2000 Jeff Johnson <jbj@redhat.com>
- rebuild for sparc baud rates > 38400.

* Tue Feb 29 2000 Ngo Than <than@redhat.de>
- move isdn.init in isdn4k-utils package to isdn-config package

* Mon Feb 21 2000 Ngo Than <than@redhat.de>
- added small to fix problem for startup and shuttdown isdn

* Wed Feb 16 2000 Ngo Than <than@redhat.com>
- added small patch for ipppd, it can handle default route

* Fri Feb 11 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- remove execute bit from /etc/ppp/ioptions
- do not create /dev/isdnctrl if it already exists

* Fri Feb 11 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- remove suid-root from /usr/bin/vboxbeep

* Fri Feb 11 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- use relative instead of absolute link in postinstall script
- use only one patch-file for the config file
- change from 0700 to 0755 perms
- change Makefiles instead of moving things around in the spec file
- include the manpages of the X11 progs only in the xisdnload rpm

* Tue Feb 03 2000 Ngo Than <than@redhat.de>
- fix pap and chap problem in isdn.init

* Tue Feb 01 2000 Ngo Than <than@redhat.de>
- added new isdn.init for rhisdn.

* Mon Jan 17 2000 Karsten Hopp <karsten@redhat.de>
- uses now configured network and netmask

* Thu Jan 06 2000 Karsten Hopp <karsten@redhat.de>
- Configures DNS if no nameserver entry in resolv.conf
- needed for dial-on-demand

* Mon Jan 03 2000 Karsten Hopp <karsten@redhat.de>
- isdnconfig  moved into separate spec-file

* Tue Dec 21 1999 Karsten Hopp <karsten@redhat.de>
- updated isdn4k-utils
- several bugfixes isdnconfig

* Thu Sep 30 1999 Karsten Hopp <karsten@redhat.de>
- added isdnconfig script and related files

* Fri Sep 25 1999 Bill Nottingham <notting@redhat.com>
- bang on init script

* Mon Sep 20 1999 Cristian Gafton <gafton@redhat.com>
- fix dangling symlink

* Mon Sep 13 1999 Bill Nottingham <notting@redhat.com>
- strip binaries
- chkconfig --del in %%preun, not %%postun

* Tue Sep 07 1999 Cristian Gafton <gafton@redhat.com>
- fix some of the german exclusive language in the init script

* Sun Aug 29 1999 Cristian Gafton <gafton@redhat.com>
- imported into Red Hat Linux
