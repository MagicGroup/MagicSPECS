Name: libdmapsharing
Version: 2.9.24
Release: 2%{?dist}
License: LGPLv2+
Source: http://www.flyn.org/projects/libdmapsharing/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
URL: http://www.flyn.org/projects/libdmapsharing/
Summary: A DMAP client and server library
Summary(zh_CN.UTF-8): DMAP 客户端和服务器库
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
BuildRequires: pkgconfig, glib2-devel, libsoup-devel >= 2.32
BuildRequires: avahi-glib-devel, gdk-pixbuf2-devel, gstreamer-plugins-base-devel >= 0.10.23.2

%description 
libdmapsharing implements the DMAP protocols. This includes support for
DAAP and DPAP.

%description -l zh_CN.UTF-8
DMAP 协议的实现，包括了 DAAP 和 DRAP 的支持。

%files 
%defattr(-, root, root, -)
%{_libdir}/libdmapsharing-3.0.so.*
%doc AUTHORS COPYING ChangeLog NEWS README


%package devel
Summary: Files needed to develop applications using libdmapsharing
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: libdmapsharing = %{version}-%{release}, pkgconfig, glib2-devel, libsoup-devel >= 2.32
Requires: avahi-glib-devel, gdk-pixbuf2-devel, gstreamer-plugins-base-devel >= 0.10.23.2

%description devel
libdmapsharing implements the DMAP protocols. This includes support for
DAAP and DPAP.  This package provides the libraries, include files, and
other resources needed for developing applications using libdmapsharing.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%files devel
%defattr(-, root, root, -)
%{_libdir}/pkgconfig/libdmapsharing-3.0.pc
%{_includedir}/libdmapsharing-3.0/
%{_libdir}/libdmapsharing-3.0.so
%{_datadir}/gtk-doc/html/libdmapsharing-3.0

%prep

%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libdmapsharing-3.0.la
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 2.9.24-2
- 为 Magic 3.0 重建

* Tue Jul 15 2014 Liu Di <liudidi@gmail.com> - 2.9.24-1
- 更新到 2.9.24

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 05 2011 W. Michael Petullo <mike[@]flyn.org> - 2.9.14-1
- new upstream version
- Remove patch from previous release (upstreamed)

* Tue Nov 08 2011 Adam Jackson <ajax@redhat.com> 2.9.12-2
- libdmapsharing-2.9.12-glib.patch: Fix FTBFS against new glib

* Mon Aug 22 2011 Adam Williamson <awilliam@redhat.com> - 2.9.12-1
- new upstream version

* Mon Mar 21 2011 W. Michael Petullo <mike[@]flyn.org> - 2.9.6-1
- New upstream version.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 07 2011 W. Michael Petullo <mike[@]flyn.org> - 2.9.5-1
- New upstream version, fixes problem compiling without libgee.

* Mon Feb 07 2011 W. Michael Petullo <mike[@]flyn.org> - 2.9.4-1
- New upstream version (API 3 series).

* Sun Dec 19 2010 W. Michael Petullo <mike[@]flyn.org> - 2.1.13-1
- New upstream version.

* Sun Nov 28 2010 W. Michael Petullo <mike[@]flyn.org> - 2.1.12-1
- New upstream version.

* Sun Oct 31 2010 W. Michael Petullo <mike[@]flyn.org> - 2.1.8-1
- New upstream version.
- Update Source and URL.
- BuildRequire gdk-pixbuf2-devel for DACP.
- BuildRequire libsoup-devel >= 2.32 for DACP.
- BuildRequire gstreamer-plugins-base-devel >= for transcoding.

* Fri Jun 04 2010 W. Michael Petullo <mike[@]flyn.org> - 1.9.0.21-1
- New upstream version.

* Fri May 28 2010 W. Michael Petullo <mike[@]flyn.org> - 1.9.0.18-1
- New upstream version.

* Fri Aug 28 2009 W. Michael Petullo <mike[@]flyn.org> - 1.9.0.13-1
- New upstream version.

* Thu Aug 27 2009 W. Michael Petullo <mike[@]flyn.org> - 1.9.0.12-1
- New upstream version.

* Sat Aug 15 2009 W. Michael Petullo <mike[@]flyn.org> - 1.9.0.11-1
- New upstream version.
- Add gtk-doc documentation to devel package.

* Wed Jul 29 2009 W. Michael Petullo <mike[@]flyn.org> - 1.9.0.10-1
- New upstream version.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 W. Michael Petullo <mike[@]flyn.org> - 1.9.0.9-1
- New upstream version.

* Tue Mar 10 2009 W. Michael Petullo <mike[@]flyn.org> - 1.9.0.4-1
- New upstream version.

* Fri Mar 06 2009 W. Michael Petullo <mike[@]flyn.org> - 1.9.0.3-1
- New upstream version.
- Use "-p /sbin/ldconfig."
- Remove requires that are already known by RPM.
- libdmapsharing-devel package now requires pkgconfig.
- Remove irrelevant INSTALL documentation.

* Sun Feb 22 2009 W. Michael Petullo <mike[@]flyn.org> - 1.9.0.1-3
- Require libsoup >= 2.25.92, as this version supports SOUP_ENCODING_EOF
message encoding, required for HTTP 1.0 clients.

* Sat Feb 07 2009 W. Michael Petullo <mike[@]flyn.org> - 1.9.0.1-2
- Fix BuildRequires.

* Sun Dec 28 2008 W. Michael Petullo <mike[@]flyn.org> - 1.9.0.1-1
- Initial package
