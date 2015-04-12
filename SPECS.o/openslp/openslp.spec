
Summary: Open implementation of Service Location Protocol V2
Summary(zh_CN.UTF-8): 服务位置协议 V2 的开源实现
Name:    openslp
Version: 2.0.0
Release: 7%{?dist}

Group:   System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License: BSD
URL:     http://sourceforge.net/projects/openslp/
Source0: http://downloads.sf.net/openslp/openslp-%{version}.tar.gz

Source1: slpd.init
# Source1,2: simple man pages (slightly modified help2man output)
Source2: slpd.8.gz
Source3: slptool.1.gz
# Source3: service file
Source4: slpd.service

# Patch1: creates script from upstream init script that sets multicast
#     prior to the start of the service
Patch1:  openslp-2.0.0-multicast-set.patch
# Patch2: notify systemd of start-up completion
Patch2:  openslp-2.0.0-notify-systemd-of-start-up.patch

BuildRequires: automake libtool
BuildRequires: bison
BuildRequires: flex 
BuildRequires: openssl-devel
BuildRequires: systemd-units systemd-devel

%description
Service Location Protocol is an IETF standards track protocol that
provides a framework to allow networking applications to discover the
existence, location, and configuration of networked services in
enterprise networks.

OpenSLP is an open source implementation of the SLPv2 protocol as defined
by RFC 2608 and RFC 2614.

%description -l zh_CN.UTF-8
服务位置协议 V2 的开源实现。

%package devel
Summary: OpenSLP headers and libraries
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:   Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
OpenSLP header files and libraries.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package server
Summary: OpenSLP server daemon
Summary(zh_CN.UTF-8): %{name} 的服务端
Group:   System Environment/Daemons
Group(zh_CN.UTF-8): 系统环境/服务
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires(preun): chkconfig, /sbin/service
Requires(post): chkconfig
Requires(postun): /sbin/service
Requires: net-tools
%description server
OpenSLP server daemon to dynamically register services.

%description server -l zh_CN.UTF-8
%{name} 的服务端。

%prep
%setup -q

%patch1 -p1 -b .multicast-set
%patch2 -p2 -b .systemd

# tarball goof (?), it wants to re-automake anyway, so let's do it right.
#libtoolize --force
#aclocal
#autoconf
#automake --add-missing
autoreconf -f -i

# remove CVS leftovers...
find . -name "CVS" | xargs rm -rf


%build

# for x86_64
export CFLAGS="-fPIC -fno-strict-aliasing -fPIE -DPIE $RPM_OPT_FLAGS"
# for slpd
export LDFLAGS="-pie -Wl,-z,now"

%configure \
  --prefix=%{_prefix} \
  --libdir=%{_libdir} \
  --sysconfdir=%{_sysconfdir} \
  --localstatedir=/var \
  --disable-dependency-tracking \
  --disable-static \
  --enable-slpv2-security \
  --disable-rpath \
  --enable-async-api

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%if 0%{?fedora} < 23
install -p -D -m755  %{SOURCE1} $RPM_BUILD_ROOT%{_initrddir}/slpd
%endif

mkdir -p ${RPM_BUILD_ROOT}/%{_sysconfdir}/slp.reg.d

# install script that sets multicast
mkdir -p ${RPM_BUILD_ROOT}/usr/lib/%{name}-server
install -m 0755 etc/slpd.all_init ${RPM_BUILD_ROOT}/usr/lib/%{name}-server/slp-multicast-set.sh

# install service file
mkdir -p ${RPM_BUILD_ROOT}/%{_unitdir}
install -p -m 644 %{SOURCE4} ${RPM_BUILD_ROOT}/%{_unitdir}/slpd.service

# install man page
mkdir -p ${RPM_BUILD_ROOT}/%{_mandir}/man8/
mkdir -p ${RPM_BUILD_ROOT}/%{_mandir}/man1/
cp %SOURCE2 ${RPM_BUILD_ROOT}/%{_mandir}/man8/
cp %SOURCE3 ${RPM_BUILD_ROOT}/%{_mandir}/man1/

# nuke unpackaged/unwanted files
rm -rf $RPM_BUILD_ROOT/usr/doc
rm -f  $RPM_BUILD_ROOT%{_libdir}/lib*.la
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post server
%systemd_post slpd.service

%preun server
%systemd_preun slpd.service

%postun server
%systemd_postun_with_restart slpd.service


%files
%defattr(-,root,root)
%doc AUTHORS COPYING FAQ NEWS README THANKS
%config(noreplace) %{_sysconfdir}/slp.conf
%{_bindir}/slptool
%{_libdir}/libslp.so.1*
%{_mandir}/man1/*

%files server
%defattr(-,root,root)
%doc doc/doc/html/IntroductionToSLP
%doc doc/doc/html/UsersGuide
%doc doc/doc/html/faq*
%{_sbindir}/slpd
%config(noreplace) %{_sysconfdir}/slp.reg
%config(noreplace) %{_sysconfdir}/slp.spi
%if 0%{?fedora} < 23
%config(noreplace) %{_initrddir}/slpd
%endif
%{_unitdir}/slpd.service
%{_mandir}/man8/*
/usr/lib/%{name}-server/slp-multicast-set.sh

%files devel
%defattr(-,root,root)
%doc doc/doc/html/ProgrammersGuide
%doc doc/doc/rfc
%{_includedir}/slp.h
%{_libdir}/libslp.so


%changelog
* Thu Apr 02 2015 Liu Di <liudidi@gmail.com> - 2.0.0-7
- 为 Magic 3.0 重建

* Wed Mar 11 2015 Adam Jackson <ajax@redhat.com> 2.0.0-6
- Drop sysvinit script from F23+

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Aug 04 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.0-4
- Link to libsystemd.so instead of old libsystemd-daemon.so
  Resolves: #1125103

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 17 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.0-2
- Launch slpd as a 'notify' daemon with systemd, rather than forking
  (patch by Stephen Gallagher)

* Tue Oct 01 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.0.0-1
- Update to openslp-2.0.0
- Fix bogus dates in %%changelog
- Add systemd support
- Add man pages for slptool and slpd
- Add CFLAGS and LDFLAGS for full relro
- Build with -fno-strict-aliasing

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 19 2013 Rex Dieter <rdieter@fedoraproject.org> 1.2.1-19
- -server: Requires: +net-tools (for netstat, #975868)

* Wed Jan 30 2013 Rex Dieter <rdieter@fedoraproject.org> 1.2.1-18
- update URL: tag (#905975)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 16 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.2.1-14
- slpd crashes if slptool findsrvtypes is run, when message logging is on (#523609)

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.2.1-13
- rebuilt with new openssl

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 1.2.1-10
- rebuild with new openssl

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.1-9
- Autorebuild for GCC 4.3

* Tue Dec 04 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.2.1-8
- respin for openssl

* Tue Aug 21 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.2.1-7
- respin (buildID)

* Tue Aug 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.2.1-6
- fc6 respin

* Wed Aug 09 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.2.1-5
- fc6 respin

* Wed Mar 1 2006 Rex Dieter <rexdieter[AT]users.sf.net> 
- fc5: gcc/glibc respin

* Mon Dec 19 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.2.1-4
- make %%postun safer

* Wed Nov 16 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.2.1-3
- rebuild (for new openssl)
- make %%postun safer

* Fri Oct 21 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.2.1-2
- -fPIC (for x86_64)

* Fri Oct 21 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.2.1-1
- 1.2.1
- move most docs to -server
- --enable-slpv2-security
- --disable-dependency-tracking

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 1.2.0
- rebuild on all arches

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Mon Jul 19 2004 Rex Dieter <rexdieter at sf.net> 0:1.2.0-0.fdr.4
- BR: flex

* Fri Jul 16 2004 Rex Dieter <rexdieter at sf.net> 0:1.2.0-0.fdr.3
- BR: bison

* Thu Jul 15 2004 Rex Dieter <rexdieter at sf.net> 0:1.2.0-0.fdr.2
- fix/add condrestart to init script

* Thu Jul 15 2004 Rex Dieter <rexdieter at sf.net> 0:1.2.0-0.fdr.1
- 1.2.0
- use -pie
- don't use Requires(post,postun)

* Fri Oct 24 2003 Rex Dieter <rexdieter af sf.net> 0:1.0.11-0.fdr.7
- fix for Fedora Core
- fix description (main package does *not* include daemon and header files).

* Fri May 30 2003 Rex Dieter <rexdieter at sf.net> 0:1.0.11-0.fdr.6
- -server: Requires(preun,postun): /sbin/service
- add a few more %%doc files to base pkg.
- initscript: add (real) 'reload' action.
- initscript: use $prog instead of hardcoded slpd.

* Fri May 16 2003 Rex Dieter <rexdieter at sf.net> 0:1.0.11-0.fdr.5
- -server: fix %postun on uninstall

* Fri May 2 2003 Rex Dieter <rexdieter at sf.net> 0:1.0.11-0.fdr.4
- *really* do %%config(noreplace) slp.conf

* Thu May 1 2003 Rex Dieter <rexdieter at sf.net> 0:1.0.11-0.fdr.3
- capitalize Summary's.
- %%config(noreplace) slp.conf

* Thu May 1 2003 Rex Dieter <rexdieter at sf.net> 0:1.0.11-0.fdr.2
- docs: remove CVS files, include rfc, move ProgrammersGuide to -devel.
- improve sub-pkg descriptions.
- improve server %%preun,%%postun scripts: condrestart on upgrade,
  suppress output of server shutdown,restarts.

* Thu May 1 2003 Rex Dieter <rexdieter at sf.net> 0:1.0.11-0.fdr.1
- specfile cleanups for fedora packaging.

* Tue Apr 29 2003 Rex Dieter <rexdieter at sf.net> 0:1.0.11-0.fdr.0
- 1.0.11 release.
- fedorize things

* Mon Feb 03 2003 Rex Dieter <rexdieter at sf.net> 0:1.0.10-1.0
- sanitize specfile
- -devel,-server subpkgs.
