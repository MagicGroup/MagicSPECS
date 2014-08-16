Summary: Window Navigator Construction Kit
Summary(zh_CN.UTF-8): 窗口导航构建工具包
Name: libwnck3
Version:	3.4.7
Release: 1%{?dist}
URL: http://download.gnome.org/sources/libwnck/
#VCS: git:git://git.gnome.org/libwnck
Source0: http://download.gnome.org/sources/libwnck/3.4/libwnck-%{version}.tar.xz
License: LGPLv2+
Group: System Environment/Libraries

Requires: startup-notification

BuildRequires: glib2-devel
BuildRequires: gtk3-devel
BuildRequires:  pango-devel
BuildRequires:  startup-notification-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  libXres-devel
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  libtool, automake, autoconf
BuildRequires:  gnome-common
Conflicts: libwnck < 2.30.4-2.fc15

%description
libwnck (pronounced "libwink") is used to implement pagers, tasklists,
and other such things. It allows applications to monitor information
about open windows, workspaces, their names/icons, and so forth.

%description -l zh_CN.UTF-8
这个库用来实现页面，任务列表和其它的类似部件。允许程序监视有关打开的窗口，
工作区，他们的名字、图标和其它有用的信息。

%package devel
Summary: Libraries and headers for libwnck
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -n libwnck-%{version}

%build
rm -f libtool
autoreconf -f -i
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
magic_rpm_clean.sh
%find_lang libwnck-3.0

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f libwnck-3.0.lang
%doc AUTHORS COPYING README NEWS
%{_libdir}/lib*.so.*
%{_bindir}/wnck-urgency-monitor
%{_libdir}/girepository-1.0/Wnck-3.0.typelib

%files devel
%{_bindir}/wnckprop
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_datadir}/gir-1.0/Wnck-3.0.gir
%doc %{_datadir}/gtk-doc

%changelog
* Fri Aug 08 2014 Liu Di <liudidi@gmail.com> - 3.4.7-1
- 更新到 3.4.7

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 3.4.3-2
- 为 Magic 3.0 重建

* Sat Sep 22 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.3-1
- Update to 3.4.3

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 18 2012 Richard Hughes <hughsient@gmail.com> - 3.4.2-1
- Update to 3.4.2

* Tue Mar 27 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.0-1
- Update to 3.4.0

* Tue Feb  7 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.5-1
- Update to 3.3.5

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for glibc bug#747377

* Mon Oct 17 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.1-1
- Update to 3.2.1

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Mon Sep 19 2011 Matthias Clasen <mclasen@redhat.com> 3.1.92-1
- Update to 3.1.92

* Wed Aug 31 2011 Matthias Clasen <mclasen@redhat.com> 3.1.90-1
- Update to 3.1.90

* Wed Jul  6 2011 Matthias Clasen <mclasen@redhat.com> 3.0.2-1
- Update to 3.0.2

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> 2.91.6-3
- Rebuild against newer gtk3

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.91.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb 02 2011 Ray Strode <rstrode@redhat.com> 2.91.6-1
- Initial import.
