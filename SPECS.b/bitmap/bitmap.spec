Name: bitmap
Version: 1.0.8
Release: 4%{?dist}
Summary: Bitmap editor and converter utilities for the X Window System
Summary(zh_CN.UTF-8): X 窗口系统下的位图编辑和转换工具
Group: User Interface/X
Group(zh_CN.UTF-8): 用户界面/X
Url: http://www.x.org
Source0: http://xorg.freedesktop.org/releases/individual/app/%{name}-%{version}.tar.bz2
Source1: bitmap.desktop
Source2: bitmap.png
License: MIT

# the bitmap-devel virtual provide is needed as it installs header files.
# this is currently used by lesstif package.
Provides: %{name}-devel = %{version}-%{release}

# libXaw-devel requires libXmu-devel 
# libXmu-devel requires libX11-devel, libXt-devel, xorg-x11-util-macros
BuildRequires: xorg-x11-xbitmaps libXaw-devel libXext-devel
BuildRequires: desktop-file-utils pkgconfig
# also needed at runtime
Requires: xorg-x11-xbitmaps

%description
Bitmap provides a bitmap editor and misc converter utilities for the X
Window System.

The package also includes files defining bitmaps associated with the 
Bitmap x11 editor.

%description -l zh_CN.UTF-8
X 窗口系统下的位图编辑和转换工具。

%prep
%setup -q


%build
%configure --disable-dependency-tracking
make %{?_smp_mflags} AM_LDFLAGS=-lXmu


%install
make install DESTDIR=%{buildroot} INSTALL='install -p'

desktop-file-install --vendor fedora                            \
        --dir %{buildroot}%{_datadir}/applications         \
        %{SOURCE1}

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/32x32/apps
install -p -m644 %{SOURCE2} %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%defattr(-,root,root,-)
# COPYING is a stub!
%doc ChangeLog
%{_bindir}/atobm
%{_bindir}/bmtoa
%{_bindir}/bitmap
%{_includedir}/X11/bitmaps/*
%{_datadir}/X11/app-defaults/Bitmap*
%{_datadir}/applications/*bitmap*
%{_datadir}/icons/hicolor/32x32/apps/bitmap.png
%{_mandir}/man1/*.1*

%changelog
* Sat Nov 07 2015 Liu Di <liudidi@gmail.com> - 1.0.8-4
- 为 Magic 3.0 重建

* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 1.0.8-3
- 更新到 1.0.8

* Tue Mar 04 2014 Liu Di <liudidi@gmail.com> - 1.0.7-2
- 更新到 1.0.7

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Jaromir Capik <jcapik@redhat.com> - 1.0.6-1
- Update to 1.0.6 (#808705)

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Mar 29 2011 Dan Horák <dan[at]danny.cz> - 1.0.3-10
- fix build

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Sep 27 2010 Parag Nemade <paragn AT fedoraproject.org> - 1.0.3-8
- Make sure this package follows current packaging guidelines.
- Removed old provides.

* Tue Dec 15 2009 Stepan Kasal <skasal@redhat.com> - 1.0.3-7
- silence scriptlets

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.3-4
- Autorebuild for GCC 4.3

* Mon Dec 17 2007 Patrice Dumas <pertusus@free.fr> 1.0.3-3
- keep timestamps

* Mon Jan 29 2007 Patrice Dumas <pertusus@free.fr> 1.0.3-2
- update to 1.0.3

* Tue Oct 10 2006 Patrice Dumas <pertusus@free.fr> 1.0.2-3
- use consistently %%{buildroot}
- provides xorg-x11-%%{name}-devel

* Mon Oct  9 2006 Patrice Dumas <pertusus@free.fr> 1.0.2-2
- buildrequires pkgconfig, libXext-devel

* Sun Sep  3 2006 Patrice Dumas <pertusus@free.fr> 1.0.2-1
- Packaged for fedora extras
