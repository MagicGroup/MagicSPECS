Name:		kmod
Version:	17
Release:	2%{?dist}
Summary:	Linux kernel module management utilities

Group:		System Environment/Kernel
License:	GPLv2+
URL:		http://git.kernel.org/?p=utils/kernel/kmod/kmod.git;a=summary
Source0:	ftp://ftp.kernel.org/pub/linux/utils/kernel/kmod/%{name}-%{version}.tar.xz
Source1:	weak-modules
Exclusiveos:	Linux

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:	chrpath
BuildRequires:	zlib-devel
BuildRequires:	xz-devel
BuildRequires:  libxslt

Requires: %{name}-libs%{?_isa} = %{version}-%{release}

Provides:	module-init-tools = 4.0-1
Obsoletes:	module-init-tools < 4.0-1
Provides:	/sbin/modprobe

%description
The kmod package provides various programs needed for automatic
loading and unloading of modules under 2.6, 3.x, and later kernels, as well
as other module management programs. Device drivers and filesystems are two
examples of loaded and unloaded modules.

%package libs
Summary:	Libraries to handle kernel module loading and unloading
License:	LGPLv2+
Group:		System Environment/Libraries

%description libs
The kmod-libs package provides runtime libraries for any application that
wishes to load or unload Linux kernel modules from the running system.

%package devel
Summary:	Header files for kmod development
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The kmod-devel package provides header files used for development of
applications that wish to load or unload Linux kernel modules.

%prep
%setup -q

%build
export V=1
%configure \
  --with-zlib \
  --with-xz
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
pushd $RPM_BUILD_ROOT/%{_mandir}/man5
ln -s modprobe.d.5.gz modprobe.conf.5.gz
popd

rm -rf $RPM_BUILD_ROOT%{_libdir}/*.la
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
ln -sf ../bin/kmod $RPM_BUILD_ROOT%{_sbindir}/modprobe
ln -sf ../bin/kmod $RPM_BUILD_ROOT%{_sbindir}/modinfo
ln -sf ../bin/kmod $RPM_BUILD_ROOT%{_sbindir}/insmod
ln -sf ../bin/kmod $RPM_BUILD_ROOT%{_sbindir}/rmmod
ln -sf ../bin/kmod $RPM_BUILD_ROOT%{_sbindir}/depmod
ln -sf ../bin/kmod $RPM_BUILD_ROOT%{_sbindir}/lsmod

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/depmod.d
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/modprobe.d

mkdir -p $RPM_BUILD_ROOT/sbin
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_sbindir}/weak-modules

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/depmod.d
%dir %{_sysconfdir}/modprobe.d
%dir %{_prefix}/lib/modprobe.d
%{_bindir}/kmod
%{_sbindir}/modprobe
%{_sbindir}/modinfo
%{_sbindir}/insmod
%{_sbindir}/rmmod
%{_sbindir}/lsmod
%{_sbindir}/depmod
%{_sbindir}/weak-modules
%{_datadir}/bash-completion/completions/kmod
%attr(0644,root,root) %{_mandir}/man5/*.5*
%attr(0644,root,root) %{_mandir}/man8/*.8*
%doc NEWS README TODO COPYING

%files libs
%{_libdir}/libkmod.so.*

%files devel
%{_includedir}/libkmod.h
%{_libdir}/pkgconfig/libkmod.pc
%{_libdir}/libkmod.so

%changelog
* Fri Jun 06 2014 Liu Di <liudidi@gmail.com> - 17-2
- 为 Magic 3.0 重建

* Wed Apr 09 2014 Josh Boyer <jwboyer@fedoraproject.org> - 17-1
- Update to version 17

* Thu Jan 02 2014 Václav Pavlín <vpavlin@redhat.com> - 16-1
- Update to version 16

* Thu Aug 22 2013 Josh Boyer <jwboyer@fedoraproject.org> - 15-1
- Update to version 15

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 05 2013 Josh Boyer <jwboyer@redhat.com> - 14-1
- Update to version 14

* Fri Apr 19 2013 Václav Pavlín <vpavlin@redhat.com> - 13-2
- Main package should require -libs

* Wed Apr 10 2013 Josh Boyer <jwboyer@redhat.com> - 13-1
- Update to version 13

* Wed Mar 20 2013 Weiping Pan <wpan@redhat.com> - 12-3
- Pull in weak-modules for kABI from Jon Masters <jcm@redhat.com> 

* Mon Mar 18 2013 Josh Boyer <jwboyer@redhat.com>
- Add patch to make rmmod understand built-in modules (rhbz 922187)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 06 2012 Josh Boyer <jwboyer@redhat.com>
- Update to version 12

* Thu Nov 08 2012 Josh Boyer <jwboyer@redhat.com>
- Update to version 11

* Fri Sep 07 2012 Josh Boyer <jwboyer@redaht.com>
- Update to version 10

* Mon Aug 27 2012 Josh Boyer <jwboyer@redhat.com>
- Update to version 9

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 23 2012 Josh Boyer <jwboyer@redhat.com> - 8-2
- Provide modprobe.conf(5) (rhbz 824552)

* Tue May 08 2012 Josh Boyer <jwboyer@redhat.com> - 8-1
- Update to version 8

* Mon Mar 19 2012 Kay Sievers <kay@redhat.com> - 7-1
- update to version 7
  - fix issue with --show-depends, where built-in
    modules of the running kernel fail to include
    loadable modules of the kernel specified

* Sun Mar 04 2012 Kay Sievers <kay@redhat.com> - 6-1
- update to version 6
- remove all patches, they are included in the release

* Fri Feb 24 2012 Kay Sievers <kay@redhat.com> - 5-8
- try to address brc#771285

* Sun Feb 12 2012 Kay Sievers <kay@redhat.com> - 5-7
- fix infinite loop with softdeps

* Thu Feb 09 2012 Harald Hoyer <harald@redhat.com> 5-6
- add upstream patch to fix "modprobe --ignore-install --show-depends"
  otherwise dracut misses a lot of modules, which are already loaded

* Wed Feb 08 2012 Harald Hoyer <harald@redhat.com> 5-5
- add "lsmod"

* Tue Feb  7 2012 Kay Sievers <kay@redhat.com> - 5-4
- remove temporarily added fake-provides

* Tue Feb  7 2012 Kay Sievers <kay@redhat.com> - 5-3
- temporarily add fake-provides to be able to bootstrap
  the new udev which pulls the old udev into the buildroot

* Tue Feb  7 2012 Kay Sievers <kay@redhat.com> - 5-1
- Update to version 5
- replace the module-init-tools package and provide all tools
  as compatibility symlinks

* Mon Jan 16 2012 Kay Sievers <kay@redhat.com> - 4-1
- Update to version 4
- set --with-rootprefix=
- enable zlib and xz support

* Thu Jan 05 2012 Jon Masters <jcm@jonmasters.org> - 3-1
- Update to latest upstream (adds new depmod replacement utility)
- For the moment, use the "kmod" utility to test the various functions

* Fri Dec 23 2011 Jon Masters <jcm@jonmasters.org> - 2-6
- Update kmod-2-with-rootlibdir patch with rebuild automake files

* Fri Dec 23 2011 Jon Masters <jcm@jonmasters.org> - 2-5
- Initial build for Fedora following package import

* Thu Dec 22 2011 Jon Masters <jcm@jonmasters.org> - 2-4
- There is no generic macro for non-multilib "/lib", hardcode like others

* Thu Dec 22 2011 Jon Masters <jcm@jonmasters.org> - 2-3
- Update package incorporating fixes from initial review feedback
- Cleaups to SPEC, rpath, documentation, library and binary locations

* Thu Dec 22 2011 Jon Masters <jcm@jonmasters.org> - 2-2
- Update package for posting to wider test audience (initial review submitted)

* Thu Dec 22 2011 Jon Masters <jcm@jonmasters.org> - 2-1
- Initial Fedora package for module-init-tools replacement (kmod) library
