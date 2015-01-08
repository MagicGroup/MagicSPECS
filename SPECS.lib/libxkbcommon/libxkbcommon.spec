#global gitdate  20120917

Name:           libxkbcommon
Version:	0.5.0
Release: 1%{?gitdate:.%{gitdate}}%{?dist}
Summary:        X.Org X11 XKB parsing library
Summary(zh_CN.UTF-8): X.Org X11 XKB 解析库
License:        MIT
URL:            http://www.x.org

%if 0%{?gitdate}
Source0:       %{name}-%{gitdate}.tar.bz2
%else
Source0:        http://xkbcommon.org/download/%{name}-%{version}.tar.xz
%endif
Source1:        make-git-snapshot.sh

BuildRequires:  autoconf automake libtool
BuildRequires:  xorg-x11-util-macros byacc flex bison
BuildRequires:  xorg-x11-proto-devel libX11-devel
BuildRequires:  xkeyboard-config-devel
%if 0%{?fedora} > 20
%global x11 1
BuildRequires:  pkgconfig(xcb-xkb) >= 1.10
%endif

%description
%{name} is the X.Org library for compiling XKB maps into formats usable by
the X Server or other display servers.

%description -l zh_CN.UTF-8
X.Org X11 XKB 解析库。

%package devel
Summary:        X.Org X11 XKB parsing development package
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
X.Org X11 XKB parsing development package

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package x11
Summary:        X.Org X11 XKB keymap creation library
Summary(zh_CN.UTF-8): X.Org X11 XKB 键盘映射创建库
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description x11
%{name}-x11 is the X.Org library for creating keymaps by querying the X
server.

%description x11 -l zh_CN.UTF-8
X.Org X11 XKB 键盘映射创建库。

%package x11-devel
Summary:        X.Org X11 XKB keymap creation library
Summary(zh_CN.UTF-8): X.Org X11 XKB 键盘映射创建库的开发文件
Requires:       %{name}-x11%{?_isa} = %{version}-%{release}

%description x11-devel
X.Org X11 XKB keymap creation library development package

%description x11-devel -l zh_CN.UTF-8
X.Org X11 XKB 键盘映射创建库的开发文件。

%prep
%setup -q -n %{name}-%{?gitdate:%{gitdate}}%{!?gitdate:%{version}}

autoreconf -v --install || exit 1

%build
%configure \
  --disable-silent-rules \
  --disable-static \
  %{?x11:--enable-x11}%{!?x11:--disable-x11}

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

find $RPM_BUILD_ROOT -name '*.la' -exec rm -fv {} ';'
magic_rpm_clean.sh

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING
%{_libdir}/libxkbcommon.so.0.0.0
%{_libdir}/libxkbcommon.so.0

%files devel
%{_libdir}/libxkbcommon.so
%dir %{_includedir}/xkbcommon/
%{_includedir}/xkbcommon/xkbcommon.h
%{_includedir}/xkbcommon/xkbcommon-compat.h
%{_includedir}/xkbcommon/xkbcommon-keysyms.h
%{_includedir}/xkbcommon/xkbcommon-names.h
%{_includedir}/xkbcommon/xkbcommon-compose.h
%{_libdir}/pkgconfig/xkbcommon.pc
%{_docdir}/libxkbcommon/*

%if 0%{?x11}
%post x11 -p /sbin/ldconfig
%postun x11 -p /sbin/ldconfig

%files x11
%{_libdir}/libxkbcommon-x11.so.0.0.0
%{_libdir}/libxkbcommon-x11.so.0

%files x11-devel
%{_libdir}/libxkbcommon-x11.so
%{_includedir}/xkbcommon/xkbcommon-x11.h
%{_libdir}/pkgconfig/xkbcommon-x11.pc
%endif

%changelog
* Wed Dec 24 2014 Liu Di <liudidi@gmail.com> - 0.5.0-1
- 更新到 0.5.0

* Fri Aug 08 2014 Liu Di <liudidi@gmail.com> - 0.4.2-5
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Rex Dieter <rdieter@fedoraproject.org> - 0.4.2-3
- make -x11 support conditional (f21+, #1000497)
- --disable-silent-rules

* Fri May 23 2014 Hans de Goede <hdegoede@redhat.com> - 0.4.2-2
- Bump release to 2 to avoid confusion with non official non scratch 0.4.2-1

* Thu May 22 2014 Rex Dieter <rdieter@fedoraproject.org> - 0.4.2-1
- xkbcommon 0.4.2 (#1000497)
- own %%{_includedir}/xkbcommon/
- -x11: +ldconfig scriptlets
- -devel: don't include xkbcommon-x11.h
- run reautoconf in %%prep (instead of %%build)
- tighten subpkg deps via %%_isa
- .spec cleanup, remove deprecated stuff
- BR: pkgconfig(xcb-xkb) >= 1.10

* Wed Feb 05 2014 Peter Hutterer <peter.hutterer@redhat.com> 0.4.0-1
- xkbcommon 0.4.0
- Add new xkbcommon-x11 and xkbcommon-x11-devel subpackages

* Tue Aug 27 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.3.1-1
- xkbcommon 0.3.1

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Apr 18 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.3.0-1
- xkbcommon 0.3.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 23 2012 Adam Jackson <ajax@redhat.com> 0.2.0-1
- xkbcommon 0.2.0

* Mon Sep 17 2012 Thorsten Leemhuis <fedora@leemhuis.info> 0.1.0-8.20120917
- Today's git snapshot

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-7.20120306
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 06 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.1.0-6.20120306
- BuildRequire xkeyboard-config-devel to get the right XKB target path (#799717)

* Tue Mar 06 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.1.0-5.20120306
- Today's git snapshot

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-4.20111109
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 09 2011 Adam Jackson <ajax@redhat.com> 0.1.0-3
- Today's git snap

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-2.20101110
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Nov 06 2010 Dave Airlie <airlied@redhat.com> 0.1.0-1.20101110
- inital import

