%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:           libxcb
Version: 1.11
Release: 1%{?dist}
Summary:        A C binding to the X11 protocol
Summary(zh_CN.UTF-8): X11 协议的 C 绑定

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        MIT
URL:            http://xcb.freedesktop.org/
Source0:        http://xcb.freedesktop.org/dist/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# This is stolen straight from the pthread-stubs source:
# http://cgit.freedesktop.org/xcb/pthread-stubs/blob/?id=6900598192bacf5fd9a34619b11328f746a5956d
# we don't need the library because glibc has working pthreads, but we need
# the pkgconfig file so libs that link against libxcb know this...
Source1:	pthread-stubs.pc.in

BuildRequires:  autoconf automake libtool pkgconfig
BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  libXau-devel
BuildRequires:  libxslt
BuildRequires:  xcb-proto >= 1.11
BuildRequires:  xorg-x11-proto-devel
BuildRequires:  xorg-x11-util-macros >= 1.18

%description
The X protocol C-language Binding (XCB) is a replacement for Xlib featuring a
small footprint, latency hiding, direct access to the protocol, improved
threading support, and extensibility.

%description -l zh_CN.UTF-8
X11 协议的 C 绑定。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package        doc
Summary:        Documentation for %{name}
Summary(zh_CN.UTF-8): %{name} 的文档
Group:          Documentation
Group(zh_CN.UTF-8): 文档
BuildArch:	noarch

%description    doc
The %{name}-doc package contains documentation for the %{name} library.

%description doc -l zh_CN.UTF-8
%{name} 的文档。

%prep
%setup -q 

%build
sed -i 's/pthread-stubs //' configure.ac
autoreconf -v --install
%configure --disable-static --docdir=%{_pkgdocdir} \
	   --enable-selinux --enable-xkb --disable-xprint
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
install -pm 644 COPYING NEWS README $RPM_BUILD_ROOT%{_pkgdocdir}
sed 's,@libdir@,%{_libdir},;s,@prefix@,%{_prefix},;s,@exec_prefix@,%{_exec_prefix},' %{SOURCE1} > $RPM_BUILD_ROOT%{_libdir}/pkgconfig/pthread-stubs.pc

find $RPM_BUILD_ROOT -name '*.la' -delete
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libxcb-composite.so.0*
%{_libdir}/libxcb-damage.so.0*
%{_libdir}/libxcb-dpms.so.0*
%{_libdir}/libxcb-dri2.so.0*
%{_libdir}/libxcb-dri3.so.0*
%{_libdir}/libxcb-glx.so.0*
%{_libdir}/libxcb-present.so.0*
%{_libdir}/libxcb-randr.so.0*
%{_libdir}/libxcb-record.so.0*
%{_libdir}/libxcb-render.so.0*
%{_libdir}/libxcb-res.so.0*
%{_libdir}/libxcb-screensaver.so.0*
%{_libdir}/libxcb-shape.so.0*
%{_libdir}/libxcb-shm.so.0*
%{_libdir}/libxcb-sync.so.1*
%{_libdir}/libxcb-xevie.so.0*
%{_libdir}/libxcb-xf86dri.so.0*
%{_libdir}/libxcb-xfixes.so.0*
%{_libdir}/libxcb-xinerama.so.0*
%{_libdir}/libxcb-xkb.so.1*
%{_libdir}/libxcb-xselinux.so.0*
%{_libdir}/libxcb-xtest.so.0*
%{_libdir}/libxcb-xv.so.0*
%{_libdir}/libxcb-xvmc.so.0*
%{_libdir}/libxcb.so.1*

%files devel
%defattr(-,root,root,-)
%{_includedir}/xcb
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*.3*

%files doc
%defattr(-,root,root,-)
%{_pkgdocdir}

%changelog
* Fri Aug 08 2014 Liu Di <liudidi@gmail.com> - 1.11-1
- 更新到 1.11

* Tue Jun 03 2014 Liu Di <liudidi@gmail.com> - 1.10-3
- 为 Magic 3.0 重建

* Tue Jun 03 2014 Liu Di <liudidi@gmail.com> - 1.10-2
- 为 Magic 3.0 重建

* Mon Jan 27 2014 Adam Jackson <ajax@redhat.com> 1.10-1
- libxcb 1.10 plus one. Updated ABIs: sync, xkb. New libs: dri3, present.

* Tue Aug  6 2013 Ville Skyttä <ville.skytta@iki.fi> - 1.9.1-3
- Install docs to %%{_pkgdocdir} where available.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 31 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.9.1-1
- libxcb 1.9.1

* Fri May 24 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.9-3
- Fix integer overflow in read_packet (CVE-2013-2064)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 16 2012 Adam Jackson <ajax@redhat.com> 1.9-1
- libxcb 1.9

* Tue Sep 04 2012 Adam Jackson <ajax@redhat.com> 1.8.1-4
- --enable-xkb for weston
- --disable-xprint instead of manual rm
- BuildRequire an updated xcb-proto for XKB and DRI2 fixes

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 09 2012 Adam Jackson <ajax@redhat.com> 1.8.1-1
- libxcb 1.8.1

* Fri Jan 13 2012 Adam Jackson <ajax@redhat.com> 1.8-2
- Don't %%doc in the base package, that pulls in copies of things we only
  want in -doc subpackage.

* Wed Jan 11 2012 Adam Jackson <ajax@redhat.com> 1.8-1
- libxcb 1.8
