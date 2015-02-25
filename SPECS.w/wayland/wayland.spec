#global gitdate 20130515

Name:           wayland
Version:        1.7.0
Release:        2%{?gitdate:.%{gitdate}}%{?dist}
Summary:        Wayland Compositor Infrastructure

Group:          User Interface/X
License:        MIT
URL:            http://%{name}.freedesktop.org/
%if 0%{?gitdate}
Source0:        wayland-%{gitdate}.tar.xz
%else
Source0:        http://wayland.freedesktop.org/releases/%{name}-%{version}.tar.xz
%endif
Source1:        make-git-snapshot.sh

BuildRequires:  autoconf automake libtool
BuildRequires:  chrpath
BuildRequires:  doxygen
BuildRequires:  pkgconfig(libffi)
BuildRequires:  expat-devel
BuildRequires:  libxslt
BuildRequires:  docbook-style-xsl
BuildRequires:  xmlto
BuildRequires:  graphviz

Provides:       %{name}-common = %{version}-%{release}
Obsoletes:      %{name}-common < 0.85.0

%description
Wayland is a protocol for a compositor to talk to its clients as well as a C
library implementation of that protocol. The compositor can be a standalone
display server running on Linux kernel modesetting and evdev input devices,
an X application, or a wayland client itself. The clients can be traditional
applications, X servers (rootless or fullscreen) or other display servers.

%package devel
Summary: Common headers for wayland
License: MIT
%description devel
Common headers for wayland

%package -n libwayland-client
Summary: Wayland client library
License: MIT
%description -n libwayland-client
Wayland client library

%package -n libwayland-cursor
Summary: Wayland cursor library
License: MIT
%description -n libwayland-cursor
Wayland cursor library

%package -n libwayland-server
Summary: Wayland server library
License: MIT
%description -n libwayland-server
Wayland server library

%package -n libwayland-client-devel
Summary: Headers and symlinks for developing wayland client applications
License: MIT
Requires: libwayland-client%{?_isa} = %{version}-%{release}
Requires: wayland-devel%{?_isa} = %{version}-%{release}
%description -n libwayland-client-devel
Headers and symlinks for developing wayland client applications.

%package -n libwayland-cursor-devel
Summary: Headers and symlinks for developing wayland cursor applications
License: MIT
Requires: libwayland-cursor%{?_isa} = %{version}-%{release}
Requires: wayland-devel%{?_isa} = %{version}-%{release}
%description -n libwayland-cursor-devel
Headers and symlinks for developing wayland cursor applications.

%package -n libwayland-server-devel
Summary: Headers and symlinks for developing wayland server applications
License: MIT
Requires: libwayland-server%{?_isa} = %{version}-%{release}
Requires: wayland-devel%{?_isa} = %{version}-%{release}
%description -n libwayland-server-devel
Headers and symlinks for developing wayland server applications.

%prep
%setup -q -n %{name}-%{?gitdate:%{gitdate}}%{!?gitdate:%{version}}

%build
autoreconf -v --install
%configure --disable-static --enable-documentation
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -name \*.la | xargs rm -f

# Remove lib64 rpaths
chrpath -d $RPM_BUILD_ROOT%{_libdir}/libwayland-cursor.so

%check
mkdir -m 700 tests/run
# known failure in i686 koji (not always, but sometimes?):
#     resources-test, test "destroy_res_tst":	signal 11, fail
XDG_RUNTIME_DIR=$PWD/tests/run make check || \
{ rc=$?; cat tests/test-suite.log; } # exit $rc; }

%clean
rm -rf $RPM_BUILD_ROOT

%post -n libwayland-client -p /sbin/ldconfig
%postun -n libwayland-client -p /sbin/ldconfig

%post -n libwayland-cursor -p /sbin/ldconfig
%postun -n libwayland-cursor -p /sbin/ldconfig

%post -n libwayland-server -p /sbin/ldconfig
%postun -n libwayland-server -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc README TODO
#doc %{_datadir}/doc/wayland/*

%files devel
%defattr(-,root,root,-)
%{_bindir}/wayland-scanner
%{_includedir}/wayland-util.h
%{_includedir}/wayland-egl.h
%{_includedir}/wayland-version.h
%{_datadir}/aclocal/wayland-scanner.m4
%{_libdir}/pkgconfig/wayland-scanner.pc
%dir %{_datadir}/wayland
%{_datadir}/wayland/wayland-scanner.mk
%{_datadir}/wayland/wayland.xml
%{_datadir}/wayland/wayland.dtd
%{_mandir}/man3/*.3*

%files -n libwayland-client
%defattr(-,root,root,-)
%{_libdir}/libwayland-client.so.0*

%files -n libwayland-cursor
%defattr(-,root,root,-)
%{_libdir}/libwayland-cursor.so.0*

%files -n libwayland-server
%defattr(-,root,root,-)
%{_libdir}/libwayland-server.so.0*

%files -n libwayland-client-devel
%defattr(-,root,root,-)
%{_includedir}/wayland-client*.h
%{_libdir}/libwayland-client.so
%{_libdir}/pkgconfig/wayland-client.pc

%files -n libwayland-cursor-devel
%defattr(-,root,root,-)
%{_includedir}/wayland-cursor*.h
%{_libdir}/libwayland-cursor.so
%{_libdir}/pkgconfig/wayland-cursor.pc

%files -n libwayland-server-devel
%defattr(-,root,root,-)
%{_includedir}/wayland-server*.h
%{_libdir}/libwayland-server.so
%{_libdir}/pkgconfig/wayland-server.pc

%changelog
* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1.7.0-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Tue Feb 17 2015 Richard Hughes <rhughes@redhat.com> - 1.7.0-1
- Wayland 1.7.0

* Fri Sep 19 2014 Kalev Lember <kalevlember@gmail.com> - 1.6.0-1
- Update to 1.6.0
- Remove lib64 rpaths

* Fri Aug 22 2014 Kevin Fenzi <kevin@scrye.com> 1.5.91-1
- Update to 1.5.90

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 02 2014 Adam Jackson <ajax@redhat.com> 1.5.0-4
- Update protocol: new surface error enums

* Mon Jun 30 2014 Adam Jackson <ajax@redhat.com> 1.5.0-3
- Remove blocking flush patch as it actually introduces deadlocks now

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Richard Hughes <rhughes@redhat.com> - 1.5.0-1
- Wayland 1.5.0

* Tue May 13 2014 Richard Hughes <rhughes@redhat.com> - 1.4.93-1
- Wayland 1.4.93

* Fri Jan 24 2014 Richard Hughes <rhughes@redhat.com> - 1.4.0-1
- Wayland 1.4.0

* Mon Jan 20 2014 Richard Hughes <rhughes@redhat.com> - 1.3.93-1
- Wayland 1.3.93

* Sat Dec 21 2013 Ville Skyttä <ville.skytta@iki.fi> - 1.3.91-2
- Call ldconfig in libwayland-cursor %%post* scripts.
- Run test suite during build.
- Compress snapshot tarballs with xz.

* Tue Dec 17 2013 Richard Hughes <rhughes@redhat.com> - 1.3.91-1
- Wayland 1.3.91

* Mon Nov 25 2013 Lubomir Rintel <lkundrak@v3.sk> - 1.3.0-1
- Wayland 1.3.0

* Mon Oct 07 2013 Adam Jackson <ajax@redhat.com> 1.2.0-3
- Don't use MSG_DONTWAIT in wl_connection_flush.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Richard Hughes <rhughes@redhat.com> - 1.2.0-1
- wayland 1.2.0

* Wed May 15 2013 Richard Hughes <rhughes@redhat.com> - 1.1.90-0.1.20130515
- Update to a git snapshot based on what will become 1.1.90

* Tue Apr 16 2013 Richard Hughes <rhughes@redhat.com> - 1.1.0-1
- wayland 1.1.0

* Wed Mar 27 2013 Richard Hughes <rhughes@redhat.com> - 1.0.6-1
- wayland 1.0.6

* Thu Feb 21 2013 Adam Jackson <ajax@redhat.com> 1.0.5-1
- wayland 1.0.5

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 02 2013 Adam Jackson <ajax@redhat.com> 1.0.3-1
- wayland 1.0.3

* Tue Oct 23 2012 Adam Jackson <ajax@redhat.com> 1.0.0-1
- wayland 1.0

* Thu Oct 18 2012 Adam Jackson <ajax@redhat.com> 0.99.0-1
- wayland 0.99.0

* Tue Sep 04 2012 Adam Jackson <ajax@redhat.com> 0.95.0-1
- wayland 0.95.0 (#843738)

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.89.0-2.20120424
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 24 2012 Richard Hughes <rhughes@redhat.com> - 0.89.0-1
- Update to a git snapshot based on 0.89.0

* Sat Feb 18 2012 Thorsten Leemhuis <fedora@leemhuis.info> - 0.85.0-1
- update to 0.85.0
- adjust license, as upstream changed it to MIT
- update make-git-snapshot.sh to current locations and scheme
- drop common package, not needed anymore
- compositor is now in a separate package, hence reduce BuildRequires to what
  is actually needed (a lot less) and adjust summary
- make usage of a git checkout in spec file optional
- a %%{?_isa} to requires where it makes sense

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-0.6.20101221
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.1-0.5.20101221
- Rebuild for new libpng

* Wed Jun 15 2011 Lubomir Rintel <lkundrak@v3.sk> - 0.1-0.4.20101221
- Install real compositor binary instead of a libtool wrapper

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-0.3.20101221
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Adam Jackson <ajax@redhat.com> 0.1-0.2.20101221
- Today's git snap

* Tue Nov 23 2010 Adam Jackson <ajax@redhat.com> 0.1-0.2.20101123
- Today's git snap
- Fix udev rule install (#653353)

* Mon Nov 15 2010 Adam Jackson <ajax@redhat.com> 0.1-0.1.20101111
- Initial packaging
