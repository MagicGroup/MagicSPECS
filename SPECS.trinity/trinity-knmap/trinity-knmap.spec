#
# spec file for package knmap (version R14)
#
# Copyright (c) 2014 Trinity Desktop Environment
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.
#
# Please submit bugfixes or comments via http://www.trinitydesktop.org/
#

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.0.1
%endif
%define tde_pkg knmap
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	2.1
Release:	%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}.2
Summary:	An NMAP frontend for TDE
Summary(zh_CN.UTF-8): TDE 下的 NMAP 前端
Group:		Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
URL:		http://sourceforge.net/projects/knmap/

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz

Patch1:		trinity-knmap--14.0.1-tqt.patch

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils
BuildRequires:	gettext

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig
BuildRequires:	libtool

# NMAP support
Requires:		nmap


%description
Knmap is a TDE-based interface to the 'nmap' facility.

The main Knmap window provides for the entry of nmap options and the
display of nmap-generated output.

This program is a complete re-write of one by the same name written by
Alexandre Sagala. The last version of that program was 0.9 which was
released on 2003-03-09 and targeted the KDE 2.2 and QT 2.3 environments.

Not to mention that it did not cater for the full set of 'nmap' options.
Or, perhaps, 'nmap' progressed whilst that version of Knmap languished.

http://www.kde-apps.org/content/show.php?content=31108

%description -l zh_CN.UTF-8
TDE 下的 NMAP 前端。

##########

%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}
%patch1 -p1

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"

%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --libdir=%{tde_libdir} \
  --datadir=%{tde_datadir} \
  --includedir=%{tde_tdeincludedir} \
  \
  --disable-dependency-tracking \
  --disable-debug \
  --enable-new-ldflags \
  --enable-final \
  --enable-closure \
  --enable-rpath \
  --disable-gcc-hidden-visibility
  
%__make %{?_smp_mflags}


%install
%__rm -rf $RPM_BUILD_ROOT
%__make install DESTDIR=$RPM_BUILD_ROOT

# Move desktop icon to XDG directory
%__mkdir_p %{buildroot}%{tde_tdeappdir}
%__mv "%{buildroot}%{tde_datadir}/applnk/"*"/%{tde_pkg}.desktop" "%{buildroot}%{tde_tdeappdir}/%{tde_pkg}.desktop"
%__rm -r "%{buildroot}%{tde_datadir}/applnk"

magic_rpm_clean.sh

%clean
%__rm -rf $RPM_BUILD_ROOT


%post
for i in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done


%postun
for i in hicolor ; do
  touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README ChangeLog
%{tde_bindir}/knmap
%{tde_tdeappdir}/knmap.desktop
%{tde_datadir}/apps/knmap/
%{tde_tdedocdir}/HTML/en/knmap/
%{tde_datadir}/icons/hicolor/*/apps/knmap.png
%{tde_datadir}/icons/hicolor/*/apps/knmapman.png
%{tde_datadir}/icons/hicolor/*/apps/localman.png
%{tde_datadir}/icons/hicolor/*/apps/manpage.png
%{tde_datadir}/icons/hicolor/*/apps/manstylesheet.png
%{tde_datadir}/icons/hicolor/*/apps/profilecopy.png
%{tde_datadir}/icons/hicolor/*/apps/profiledelete.png
%{tde_datadir}/icons/hicolor/*/apps/profileload.png
%{tde_datadir}/icons/hicolor/*/apps/profilerename.png
%{tde_datadir}/icons/hicolor/*/apps/profilesave.png
%{tde_datadir}/icons/hicolor/*/apps/profilesaveas.png
%{tde_datadir}/icons/hicolor/*/apps/scanclose.png
%{tde_datadir}/icons/hicolor/*/apps/scanduplicate.png
%{tde_datadir}/icons/hicolor/*/apps/scannew.png
%{tde_datadir}/icons/hicolor/*/apps/scanrename.png
%{tde_datadir}/icons/hicolor/*/apps/zoomcustom.png
%{tde_datadir}/icons/hicolor/*/apps/zoomin.png
%{tde_datadir}/icons/hicolor/*/apps/zoomout.png


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2:2.1-1.2
- 为 Magic 3.0 重建

* Mon Oct 12 2015 Liu Di <liudidi@gmail.com> - 2:2.1-1.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:2.1-1
- Initial release for TDE 14.0.0
