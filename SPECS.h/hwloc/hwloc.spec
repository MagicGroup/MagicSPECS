Summary:   Portable Hardware Locality - portable abstraction of hierarchical architectures
Name:      hwloc
Version:   1.8.1
Release:   2%{?dist}
License:   BSD
Group:     Applications/System
URL:       http://www.open-mpi.org/projects/hwloc/
Source0:   http://www.open-mpi.org/software/hwloc/v%{version}/downloads/%{name}-%{version}.tar.bz2

BuildRequires: cairo-devel
BuildRequires: libpciaccess-devel
BuildRequires: libtool-ltdl-devel
BuildRequires: libX11-devel
BuildRequires: libxml2-devel
BuildRequires: libXNVCtrl-devel
BuildRequires: ncurses-devel
BuildRequires: transfig doxygen w3m
BuildRequires: texlive-latex texlive-makeindex
BuildRequires: autoconf automake libtool
%ifnarch s390 s390x
BuildRequires: libibverbs-devel
%endif
%ifnarch s390 s390x %{arm} aarch64
BuildRequires: numactl-devel
%endif
Requires:  %{name}-libs%{?_isa} = %{version}-%{release}

%description
The Portable Hardware Locality (hwloc) software package provides 
a portable abstraction (across OS, versions, architectures, ...) 
of the hierarchical topology of modern architectures, including 
NUMA memory nodes,  shared caches, processor sockets, processor cores
and processing units (logical processors or "threads"). It also gathers
various system attributes such as cache and memory information. It primarily
aims at helping applications with gathering information about modern
computing hardware so as to exploit it accordingly and efficiently.

hwloc may display the topology in multiple convenient formats. 
It also offers a powerful programming interface (C API) to gather information 
about the hardware, bind processes, and much more.

%package devel
Summary:   Headers and shared development libraries for hwloc
Group:     Development/Libraries
Requires:  %{name}-libs = %{version}-%{release}

%description devel
Headers and shared object symbolic links for the hwloc.

%package libs
Summary:   Run time libraries for the hwloc
Group:     Development/Libraries

%description libs
Run time libraries for the hwloc

%prep
%setup -q

%build
autoreconf --force --install
%configure
make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot} INSTALL="%{__install} -p"

#Fix wrong permition on file hwloc-assembler-remote => I have reported this to upstream already
chmod 0755 %{buildroot}%{_bindir}/hwloc-assembler-remote

# We don't ship .la files.
find %{buildroot} -name '*.la' -exec rm -f {} ';'

cp -p AUTHORS COPYING NEWS README VERSION %{buildroot}%{_defaultdocdir}/%{name}
cp -p doc/hwloc-hello.c %{buildroot}%{_defaultdocdir}/%{name}

%check
make check

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%{_bindir}/%{name}*
%{_bindir}/lstopo
%{_bindir}/lstopo-no-graphics
%{_mandir}/man1/%{name}*
%{_mandir}/man1/lstopo*

%files devel
%{_libdir}/pkgconfig/*
%{_mandir}/man3/*
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*
%{_includedir}/%{name}.h
%{_defaultdocdir}/%{name}/*c
%{_libdir}/*.so

%files libs
%{_mandir}/man7/%{name}*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/%{name}.dtd
%{_datadir}/%{name}/%{name}-valgrind.supp
%dir %{_defaultdocdir}/%{name}
%{_defaultdocdir}/%{name}/*[^c]
%{_libdir}/libhwloc*so.*


%changelog
* Fri Feb 14 2014 Jirka Hladky <hladky.jiri@gmail.com> - 1.8.1-2
- Fixed BuildRequires

* Thu Feb 13 2014 Jirka Hladky <hladky.jiri@gmail.com> - 1.8.1-1
- Update to 1.8.1

* Sat Jan 04 2014 Jirka Hladky <hladky.jiri@gmail.com> - 1.8-2
- Unversioned docdir change, more info on 
  https://fedoraproject.org/wiki/Changes/UnversionedDocdirs

* Thu Dec 19 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.8-1
- Update to 1.8
- No numa on aarch64
- Cleanup and modernise spec

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May  9 2013 Jirka Hladky <hladky.jiri@gmail.com> - 1.7-1
- Minor issue with the man page fixed

* Tue Apr 23 2013 Jirka Hladky <hladky.jiri@gmail.com> - 1.7-0
- Update to version 1.7

* Thu Jan 31 2013 Jirka Hladky <hladky.jiri@gmail.com> - 1.6.1-1
- Created libs package with reduced dependencies

* Sat Jan 19 2013 Jirka Hladky <hladky.jiri@gmail.com> - 1.6.1-0
- Update to version 1.6.1

* Mon Nov  5 2012  Jirka Hladky  <hladky.jiri@gmail.com> - 1.5.1-1
- Update to version 1.5.1

* Wed Aug 15 2012 Jirka Hladky  <hladky.jiri@gmail.com> - 1.5-1
- Update to version 1.5

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 15 2012 Orion Poplawski <orion@cora.nwra.com> - 1.4.2-1
- Update to version 1.4.2

* Wed Apr 18 2012 Jirka Hladky  <hladky.jiri@gmail.com> - 1.4.1-2
- Fixed build dependency for s390x

* Mon Apr 16 2012 Jirka Hladky  <hladky.jiri@gmail.com> - 1.4.1-1
- Update to version 1.4.1
- BZ812622 - libnuma was splitted out of numactl package

* Thu Apr 12 2012 Dan Horák <dan[at]danny.cz> - 1.4-2
- no InfiniBand on s390(x)

* Wed Feb 14 2012 Jirka Hladky  <hladky.jiri@gmail.com> - 1.4-1
- Update to 1.4 release

* Mon Nov 14 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.3-1
- Update build for ARM support

* Sat Oct 15 2011 Jirka Hladky <hladky.jiri@gmail.com> - 1.3-0
 - 1.3 release
 - added dependency on libibverbs-devel pciutils-devel
 - cannot provide support for cuda (cuda_runtime_api.h). 
 - Nvidia CUDA is free but not open-source therefore not in Fedora.

* Fri Oct 07 2011 Jirka Hladky <hladky.jiri@gmail.com> - 1.2.2-1
 - moved *.so to the devel package
 - libhwloc*so* in the main package

* Wed Oct 05 2011 Jirka Hladky <hladky.jiri@gmail.com> - 1.2.2-0
- 1.2.2 release
- Fix for BZ https://bugzilla.redhat.com/show_bug.cgi?id=724937 for 32-bit PPC

* Sat Sep 17 2011 Jirka Hladky <hladky.jiri@gmail.com> - 1.2.1-0
- 1.2.1 release
- Moved libhwloc*.so* to the main package

* Mon Jun 27 2011 Jirka Hladky <hladky.jiri@gmail.com> - 1.2-0
- 1.2 release

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-0.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan  3 2011 Dan Horák <dan[at]danny.cz> - 1.1-0.1
- fix build on s390(x) where numactl is missing

* Sat Jan  1 2011 Jirka Hladky <hladky.jiri@gmail.com> - 1.1-0
- 1.1 rel# Patch to the 1.1 fix 2967 http://www.open-mpi.org/software/hwloc/nightly/v1.1/hwloc-1.1rc6r2967.tar.bz2
- Fix hwloc_bitmap_to_ulong right after allocating the bitmap.
- Fix the minimum width of NUMA nodes, caches and the legend in the graphical lstopo output.
- Cleanup error management in hwloc-gather-topology.sh.
- Add a manpage and usage for hwloc-gather-topology.sh on Linux.
- Rename hwloc-gather-topology.sh to hwloc-gather-topology to be consistent with the upcoming version 1.2ease

* Mon Jul 19 2010 Jirka Hladky <jhladky@redhat.com> - 1.0.2-1
- 1.0.2 release
- added "check" section to the RPM SPEC file

* Mon Jul 19 2010 Jirka Hladky <jhladky@redhat.com> - 1.0.2-0.1.rc1r2330
- 1.0.2 release candidate

* Mon Jul 12 2010 Jirka Hladky <jhladky@redhat.com> - 1.0.1-19
- Fixed issues as described at https://bugzilla.redhat.com/show_bug.cgi?id=606498#c6

* Fri Jul 09 2010 Jirka Hladky <jhladky@redhat.com> - 1.0.1-18
- Fixed issues as described at https://bugzilla.redhat.com/show_bug.cgi?id=606498

* Fri Jun 18 2010 Jirka Hladky <jhladky@redhat.com> - 1.0.1-17
- Initial build
