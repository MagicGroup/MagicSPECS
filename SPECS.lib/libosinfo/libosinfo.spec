# -*- rpm-spec -*-

# Plugin isn't ready for real world use yet - it needs
# a security audit at very least
%define with_plugin 0

%define with_gir 0

%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7
%define with_gir 1
%endif

Summary: A library for managing OS information for virtualization
Summary(zh_CN.UTF-8): 为虚拟化管理系统信息的库
Name: libosinfo
Version: 0.2.10
Release: 1%{?dist}%{?extra_release}
License: LGPLv2+
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Source: https://fedorahosted.org/releases/l/i/%{name}/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
URL: http://libosinfo.org
BuildRequires: glib2-devel
BuildRequires: check-devel
BuildRequires: libxml2-devel >= 2.6.0
BuildRequires: libxslt-devel >= 1.0.0
BuildRequires: vala
BuildRequires: vala-tools
BuildRequires: libsoup-devel
%if %{with_gir}
BuildRequires: gobject-introspection-devel
%endif
Requires: udev

%description
libosinfo is a library that allows virtualization provisioning tools to
determine the optimal device settings for a hypervisor/operating system
combination.

%description -l zh_CN.UTF-8
为虚拟化管理系统信息的库。

%package devel
Summary: Libraries, includes, etc. to compile with the libosinfo library
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
Requires: glib2-devel

%description devel
libosinfo is a library that allows virtualization provisioning tools to
determine the optimal device settings for a hypervisor/operating system
combination.

Libraries, includes, etc. to compile with the libosinfo library

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package vala
Summary: Vala bindings
Summary(zh_CN.UTF-8): Vala 绑定
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description vala
libosinfo is a library that allows virtualization provisioning tools to
determine the optimal device settings for a hypervisor/operating system
combination.

This package provides the Vala bindings for libosinfo library.

%description vala -l zh_CN.UTF-8
Vala 绑定。

%prep
%setup -q

%build
%if %{with_gir}
%define gir_arg --enable-introspection=yes
%else
%define gir_arg --enable-introspection=no
%endif

%configure %{gir_arg} --enable-vala=yes --enable-udev=yes
%__make %{?_smp_mflags} V=1

chmod a-x examples/*.js examples/*.py

%install
rm -fr %{buildroot}
%__make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_libdir}/*.la
magic_rpm_clean.sh

%check
make check

%clean
rm -fr %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%doc AUTHORS ChangeLog COPYING.LIB NEWS README
%{_bindir}/osinfo-detect
%{_bindir}/osinfo-db-validate
%{_bindir}/osinfo-query
%{_bindir}/osinfo-install-script
%dir %{_datadir}/libosinfo/
%dir %{_datadir}/libosinfo/db/
%dir %{_datadir}/libosinfo/schemas/
%{_datadir}/libosinfo/db/usb.ids
%{_datadir}/libosinfo/db/pci.ids
%{_datadir}/libosinfo/db/devices
%{_datadir}/libosinfo/db/oses
%{_datadir}/libosinfo/db/hypervisors
%{_datadir}/libosinfo/db/install-scripts
%{_datadir}/libosinfo/db/datamaps/windows-lang.xml
%{_datadir}/libosinfo/db/datamaps/x11-keyboard.xml
%{_datadir}/libosinfo/schemas/libosinfo.rng
%{_mandir}/man1/osinfo-db-validate.1*
%{_mandir}/man1/osinfo-detect.1*
%{_mandir}/man1/osinfo-query.1*
%{_mandir}/man1/osinfo-install-script.1*
%{_libdir}/%{name}-1.0.so.*
/lib/udev/rules.d/95-osinfo.rules
%if %{with_gir}
%{_libdir}/girepository-1.0/Libosinfo-1.0.typelib
%endif

%files devel
%defattr(-, root, root)
%doc examples/demo.js
%doc examples/demo.py
%{_libdir}/%{name}-1.0.so
%dir %{_includedir}/%{name}-1.0/
%dir %{_includedir}/%{name}-1.0/osinfo/
%{_includedir}/%{name}-1.0/osinfo/*.h
%{_libdir}/pkgconfig/%{name}-1.0.pc
%if %{with_gir}
%{_datadir}/gir-1.0/Libosinfo-1.0.gir
%endif
%{_datadir}/gtk-doc/html/Libosinfo

%files vala
%defattr(-, root, root)
%{_datadir}/vala/vapi/libosinfo-1.0.vapi

%changelog
* Wed Jul 23 2014 Liu Di <liudidi@gmail.com> - 0.2.10-1
- 更新到 0.2.10

* Fri Oct 12 2012 Zeeshan Ali <zeenix@redhat.com> - 0.2.1-1
- Fix and simplify udev rule.
- Fedora:
  - Fix minimum RAM requirements for F16 and F17.
- Add data on:
  - Fedora 18
  - GNOME 3.6
  - Ubuntu 12.10
- Fixes to doc build.
- Install script:
  - Add get_config_param method.
  - Differenciate between expected/output script names.
  - Add more utility functions.
- Add 'installer-reboots' parameter to medias.
- osinfo-detect does not die of DB loading errors anymore.
- More type-specific entity value getters/setters.
- Fixe and update RNG file.
- Add 'subsystem' property/attribute to devices.

* Mon Sep 03 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.2.0-1
- Update to 0.2.0 release.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Zeeshan Ali <zeenix@redhat.com> - 0.1.2-1
- Update to 0.1.2 release.

* Thu Apr 12 2012 Zeeshan Ali <zeenix@redhat.com> - 0.1.1-1
- Update to 0.1.1 release.

* Wed Mar 14 2012 Daniel P. Berrange <berrange@redhat.com> - 0.1.0-2
- Remove obsolete perl based scripts (rhbz #803086)

* Wed Feb 08 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.1.0-1
- Update to 0.1.0 release

* Tue Jan  17 2012 Zeeshan Ali <zeenix@redhat.com> - 0.0.5-1
- Update to 0.0.5 release

* Tue Jan  3 2012 Daniel P. Berrange <berrange@redhat.com> - 0.0.4-2
- Remove pointless gir conditionals

* Wed Dec 21 2011 Daniel P. Berrange <berrange@redhat.com> - 0.0.4-1
- Update to 0.0.4 release

* Thu Nov 24 2011 Daniel P. Berrange <berrange@redhat.com> - 0.0.2-1
- Initial package

