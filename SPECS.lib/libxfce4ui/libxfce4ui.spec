# Review at https://bugzilla.redhat.com/show_bug.cgi?id=554599


Name:           libxfce4ui
Version:	4.12.1
Release: 5%{?dist}
Summary:        Commonly used Xfce widgets
Summary(zh_CN.UTF-8): xfce 通用的部件

Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
License:        LGPLv2+
URL:            http://xfce.org/
#VCS git:git://git.xfce.org/xfce/libxfce4ui
%global xfceversion %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:        http://archive.xfce.org/src/xfce/%{name}/%{xfceversion}/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  pkgconfig(gobject-2.0) >= 2.24.0
BuildRequires:  pkgconfig(gtk+-2.0) >= 2.20.0
BuildRequires:  libSM-devel
BuildRequires:  pkgconfig(libxfce4util-1.0) >= %{xfceversion}
BuildRequires:  pkgconfig(libxfconf-0) >= 4.10
BuildRequires:  pkgconfig(libstartup-notification-1.0) >= 0.4
BuildRequires:  gtk-doc
BuildRequires:  desktop-file-utils
# FIXME: Enable libglade again one day
#BuildRequires:  glade3-libgladeui-devel >= 3.5.0
BuildRequires:  gettext
BuildRequires:  intltool
# FIXME: obsolete libxfcegui4 one day 
#Provides:       libxfcegui4 = %{version}
#Obsoletes:      libxfcegui4 < %{version}

%description
Libxfce4ui is used to share commonly used Xfce widgets among the Xfce
applications.

%description -l zh_CN.UTF-8
Xfce 程序通用的部件。

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       %{name} = %{version}-%{release}
Requires:       gtk2-devel
Requires:       libxfce4util-devel
# FIXME: Enable libglade again one day
#Requires:       glade3-libgladeui-devel
Requires:       pkgconfig
# FIXME: obsolete libxfcegui4 one day 
#Provides:       libxfcegui4-devel = %{version}
#Obsoletes:      libxfcegui4-devel < %{version}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q


%build
# FIXME: Enable libglade again one day
%configure --enable-gtk-doc --disable-static --disable-gladeui
# Remove rpaths
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

# The LD_LIBRARY_PATH hack is needed for --enable-gtk-doc
# because lt-libxfce4ui-scan is linked against libxfce4ui
export LD_LIBRARY_PATH=$( pwd )/libxfce4ui/.libs

make %{?_smp_mflags} V=1


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
magic_rpm_clean.sh
%find_lang %{name}
desktop-file-install                                       \
  --delete-original                                        \
  --dir=${RPM_BUILD_ROOT}%{_datadir}/applications          \
  ${RPM_BUILD_ROOT}%{_datadir}/applications/xfce4-about.desktop

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README THANKS
%config(noreplace) %{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-keyboard-shortcuts.xml
%{_libdir}/*.so.*


%files devel
%defattr(-,root,root,-)
%doc TODO
%{_bindir}/xfce4-about
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%doc %{_datadir}/gtk-doc/
%{_datadir}/applications/xfce4-about.desktop
%{_datadir}/icons/hicolor/48x48/apps/xfce4-logo.png

%changelog
* Tue Nov 10 2015 Liu Di <liudidi@gmail.com> - 4.12.1-5
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 4.12.1-4
- 为 Magic 3.0 重建

* Sat Oct 24 2015 Liu Di <liudidi@gmail.com> - 4.12.1-3
- 为 Magic 3.0 重建

* Fri Oct 23 2015 Liu Di <liudidi@gmail.com> - 4.12.1-2
- 更新到 4.12.1

* Tue Jun 10 2014 Liu Di <liudidi@gmail.com> - 4.11.1-3
- 更新到 4.11.1

* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 4.10.0-3
- 为 Magic 3.0 重建

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Apr 28 2012 Christoph Wickert <cwickert@fedoraproject.org> - 4.10.0-1
- Update to 4.10.0 final

* Sat Apr 14 2012 Kevin Fenzi <kevin@scrye.com> - 4.9.2-1
- Update to 4.9.2 (Xfce 4.10pre2)

* Sun Apr 01 2012 Kevin Fenzi <kevin@scrye.com> - 4.9.1-1
- Update to 4.9.1

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 23 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.8.1-1
- Update to 4.8.1

* Sun Dec 18 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.8.0-6
- Fix Control shortcuts (#768704)
- Add review # and VCS key

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 4.8.0-5
- Rebuild for new libpng

* Wed Mar 16 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.8.0-5
- Remove requirements for libxfcegui4-devel now that glade support was omitted

* Tue Feb 22 2011 Rakesh Pandit <rakesh@fedoraproject.org> - 4.8.0-4
- Disable glade as it still uses old API

* Tue Feb 22 2011 Rakesh Pandit <rakesh@fedoraproject.org> - 4.8.0-3
- Rebuild for new glade

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 16 2011 Kevin Fenzi <kevin@tummy.com> - 4.8.0-1
- Update to 4.8.0 final. 

* Sun Jan 02 2011 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.6-1
- Update to 4.7.6

* Mon Nov 29 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.5-1
- Update to 4.7.5

* Mon Nov 08 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.4-1
- Update to 4.7.4

* Sun Sep 05 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.3-1
- Update to 4.7.3
- Drop dependency on gtk-doc (#604399)

* Tue Jul 27 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.2-2
- Fix file conflict with libxfce4gui (#618719)

* Fri May 21 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.2-1
- Update to 4.7.2

* Wed May 19 2010 Kevin Fenzi <kevin@tummy.com> - 4.7.1-3
- Rebuild for new glade version. 

* Tue Jan 12 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.1-2
- Fix license tag
- Build gtk-doc

* Tue Jan 05 2010 Christoph Wickert <cwickert@fedoraproject.org> - 4.7.1-1
- Initial spec file, based on libxfcegui4.spec

