Name:           libnice
Version: 0.1.13
Release:        1%{?dist}
Summary:        GLib ICE implementation
Summary(zh_CN.UTF-8): GLib ICE 实现 

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2 and MPLv1.1
URL:            http://nice.freedesktop.org/wiki/
Source0:        http://nice.freedesktop.org/releases/%{name}-%{version}.tar.gz

BuildRequires:	glib2-devel
BuildRequires:  gstreamer-devel
BuildRequires:	gstreamer-plugins-base-devel
BuildRequires:  gstreamer1-devel >= 0.11.91
BuildRequires:	gstreamer1-plugins-base-devel >= 0.11.91
BuildRequires:	gupnp-igd-devel >= 0.1.2


%description
%{name} is an implementation of the IETF's draft Interactive Connectivity
Establishment standard (ICE). ICE is useful for applications that want to
establish peer-to-peer UDP data streams. It automates the process of traversing
NATs and provides security against some attacks. Existing standards that use
ICE include the Session Initiation Protocol (SIP) and Jingle, XMPP extension
for audio/video calls.

%description -l zh_CN.UTF-8
GLib ICE 实现。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}
Requires:	glib2-devel
Requires:	pkgconfig


%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q


%check
#make check


%build
%configure --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
magic_rpm_clean.sh

%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc NEWS README COPYING COPYING.LGPL COPYING.MPL
%{_bindir}/stunbdc
%{_bindir}/stund
%{_bindir}/*-example
%{_libdir}/gstreamer-0.10/libgstnice010.so
%{_libdir}/gstreamer-1.0/libgstnice.so
%{_libdir}/*.so.*


%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/nice.pc
%{_datadir}/gtk-doc/html/%{name}/
%{_libdir}/girepository-1.0/Nice-0.1.typelib
%{_datadir}/gir-1.0/Nice-0.1.gir

%changelog
* Mon Jul 13 2015 Liu Di <liudidi@gmail.com> - 0.1.13-1
- 更新到 0.1.13

* Tue Jul 22 2014 Liu Di <liudidi@gmail.com> - 0.1.7-1
- 更新到 0.1.7

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.1.3-2
- 为 Magic 3.0 重建

* Fri Sep 14 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.1.3-1
- Update to 0.1.3.
- Add BR on gstreamer1 packages.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 23 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.1.2-1
- Update to 0.1.2.

* Mon Jan 16 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.1.1-3
- Rebuild for new gupnp-idg.

* Sun Jan 08 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.1.1-2
- Rebuild for new gcc.

* Wed Dec  7 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.1.1-1
- Update to 0.1.1.
- Drop ppc64 patch. Fixed upstream.

* Tue Aug 16 2011 David Woodhouse <dwmw2@infradead.org> - 0.1.0-5
- Apply portability patch to nice/Makefile.in too. I hate autocrap.

* Tue Aug 16 2011 David Woodhouse <dwmw2@infradead.org> - 0.1.0-4
- Fix non-portable symbol checks in nice/Makefile.am

* Fri Jun 17 2011 Peter Robinson <pbrobinson@gmail.com> - 0.1.0-3
- rebuild for new gupnp/gssdp

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 26 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.1.0-1
- Update to 0.1.0.
- Enable make check.
- Drop buildroot and clean section. No longer needed.

* Wed Aug  4 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.0.13-1
- Update to 0.0.13.

* Wed May 19 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.0.12-1
- Update to 0.0.12.

* Fri Mar 19 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.0.11-1
- Update to 0.0.11.

* Wed Dec 16 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.0.10-2
- Rebuild for new gupnp-igd.

* Mon Nov  9 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.0.10-1
- Update to 0.0.10.

* Thu Sep 17 2009 Bastien Nocera <bnocera@redhat.com> 0.0.9-2
- Rebuild for new gupnp

* Sun Aug  2 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.0.9-1
- Update to 0.0.9.
- Drop sha1 patch. Fixed upstream.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 21 2009 Warren Togami <wtogami@redhat.com> - 0.0.8-2
- stun sha1 patch from upstream to make it work at all

* Sun Jun 21 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.0.8-1
- Update to 0.0.8.

* Sun Jun 14 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.0.7-1
- Update to 0.0.7.
- Add BR on gupnp-igd-devel.

* Mon Apr 13 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.0.6-1
- Update to 0.0.6.

* Wed Mar 18 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.0.5-1
- Update to 0.0.5.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Dec 27 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.0.4-1
- Initial Fedora spec.

