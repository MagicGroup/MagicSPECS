Summary: Graphical effect and filter library
Summary(zh_CN.UTF-8): 图像效果和过滤器库
Name:    qimageblitz
Version: 0.0.6
Release: 5%{?dist}

Group:   System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License: BSD and ImageMagick
URL:     http://qimageblitz.sourceforge.net/
Source0: http://download.kde.org/stable/qimageblitz/qimageblitz-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# upstreamed to kdesupport
# r1204248 | rdieter | 2010-12-06 08:05:09 -0600 (Mon, 06 Dec 2010) | 2 lines
Patch100: qimageblitz-0.0.4-noexecstack.patch

BuildRequires: cmake
BuildRequires: qt4-devel

%description
Blitz is a graphical effect and filter library for KDE4 that contains
improvements over KDE 3.x's kdefx library including bugfixes, memory and
speed improvements, and MMX/SSE support.

%description -l zh_CN.UTF-8
图像效果和过滤器库。

%package devel
Summary: Developer files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:   Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
%{summary}.
%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package examples
Summary: Example programs for %{name}
Summary(zh_CN.UTF-8): %{name} 的样例程序
Group:   System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires: %{name}%{?_isa} = %{version}-%{release}
%description examples
This package contains the blitztest example program for %{name}.
%description examples -l zh_CN.UTF-8
%{name} 的样例程序。

%prep
%setup -q
%patch100 -p1


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} %{?_cmake_skip_rpath}  .. 
popd 

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf $RPM_BUILD_ROOT
make install/fast  DESTDIR=$RPM_BUILD_ROOT -C %{_target_platform}
magic_rpm_clean.sh

%check
export PKG_CONFIG_PATH=%{buildroot}%{_datadir}/pkgconfig:%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion qimageblitz)" = "4.0.0"


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc Changelog README* COPYING
%{_libdir}/libqimageblitz.so.4*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libqimageblitz.so
%{_libdir}/pkgconfig/qimageblitz.pc
%{_includedir}/qimageblitz/

%files examples
%defattr(-,root,root,-)
%{_bindir}/blitztest


%changelog
* Wed Sep 09 2015 Liu Di <liudidi@gmail.com> - 0.0.6-5
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.0.6-4
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.0.6-3
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug 16 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.0.6-1
- qimageblitz-0.0.6

* Fri Jan 22 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.0.4-3
- require the main package with exact version-release in -examples
- remove explicit Requires: qt4-devel pkgconfig from -devel, now autodetected

* Tue Jan 05 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.0.4-2
- update summary/description/Source_url
- %%files: track soname
- cleaner cmake-fu
- upstream noexecstack patch

* Tue Jan 05 2010 Than Ngo <than@redhat.com> - 0.0.4-1
- use the official 0.0.4

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.4-0.6.svn706674
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.4-0.5.svn706674
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 7 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.0.4-0.4.svn706674
- Fix noexecstack patch to disable execstack also on x86_64 (#428036).

* Tue Jan 8 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.0.4-0.3.svn706674
- Apply Debian patch by Sune Vuorela to fix executable stack (#428036).

* Wed Sep 19 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.0.4-0.2.svn706674
- Move blitztest example to its own subpackage.

* Fri Aug 3 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.0.4-0.1.svn706674
- First Fedora package
