#
# spec file for package tde-systemsettings (version R14)
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
%define tde_pkg tde-systemsettings
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_confdir %{_sysconfdir}/trinity
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_sysconfdir %{_sysconfdir}/trinity
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	0.0svn20070312
Release:	%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}.2
Summary:	Easy to use control centre for TDE
Summary(zh_CN.UTF-8): TDE 的系统配置程序
Group:		Applications/Utilities
Group(zh_CN.UTF-8): 应用程序/工具
URL:		http://www.trinitydesktop.org

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz
Source1:		kde-settings-laptops.directory

Patch1:		%{name}-14.0.1-tqt.patch

Provides:	trinity-kde-systemsettings = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:	trinity-kde-systemsettings < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:	trinity-systemsettings = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:	trinity-systemsettings < %{?epoch:%{epoch}:}%{version}-%{release}

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig
BuildRequires:	fdupes

Requires:		trinity-guidance


%description
System preferences is a replacement for the TDE
Control Centre with an improved user interface.

%description -l zh_CN.UTF-8
TDE 的系统配置程序。

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
export kde_confdir="%{tde_confdir}"


%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --datadir=%{tde_datadir} \
  --includedir=%{tde_tdeincludedir} \
  --sysconfdir=%{tde_sysconfdir} \
  \
  --disable-dependency-tracking \
  --disable-debug \
  --enable-final \
  --enable-new-ldflags \
  --enable-closure \
  --enable-rpath \
  --disable-gcc-hidden-visibility

%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

%__install -D -m 644 %{SOURCE1} %{buildroot}%{tde_datadir}/desktop-directories/tde-settings-laptops.directory

# Unwanted files
%__rm -f %{buildroot}%{tde_datadir}/applications/tde/kcmfontinst.desktop
%__rm -f %{buildroot}%{tde_datadir}/desktop-directories/tde-settings-power.directory
%__rm -f %{buildroot}%{tde_datadir}/desktop-directories/tde-settings-system.directory

%__rm -f %{buildroot}%{tde_datadir}/applications/tde/laptop.desktop

echo "OnlyShowIn=TDE;" >>"%{?buildroot}%{tde_tdeappdir}/audioencoding.desktop"
echo "OnlyShowIn=TDE;" >>"%{?buildroot}%{tde_tdeappdir}/defaultapplication.desktop"
echo "OnlyShowIn=TDE;" >>"%{?buildroot}%{tde_tdeappdir}/kcm_knetworkconfmodule_ss.desktop"
echo "OnlyShowIn=TDE;" >>"%{?buildroot}%{tde_tdeappdir}/medianotifications.desktop"
echo "OnlyShowIn=TDE;" >>"%{?buildroot}%{tde_tdeappdir}/systemsettings.desktop"
magic_rpm_clean.sh

%clean
%__rm -rf %{buildroot}


%post
touch --no-create %{tde_datadir}/icons/crystalsvg || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/crystalsvg || :
update-desktop-database %{tde_tdeappdir} -q &> /dev/null

%postun
touch --no-create %{tde_datadir}/icons/crystalsvg || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/crystalsvg || :
update-desktop-database %{tde_tdeappdir} -q &> /dev/null

%files
%defattr(-,root,root,-)
%doc README TODO
%dir %{tde_sysconfdir}/xdg
%dir %{tde_sysconfdir}/xdg/menus
%dir %{tde_sysconfdir}/xdg/menus/applications-merged
%{tde_sysconfdir}/xdg/menus/applications-merged/tde-system-settings-merge.menu
%{tde_sysconfdir}/xdg/menus/tde-system-settings.menu
%{tde_bindir}/systemsettings
%{tde_datadir}/applications/tde/audioencoding.desktop
%{tde_datadir}/applications/tde/defaultapplication.desktop
%{tde_datadir}/applications/tde/kcm_knetworkconfmodule_ss.desktop
#%{tde_datadir}/applications/tde/laptop.desktop
%{tde_datadir}/applications/tde/medianotifications.desktop
%{tde_datadir}/applications/tde/systemsettings.desktop
%{tde_datadir}/apps/systemsettings/
%{tde_confdir}/systemsettingsrc
%{tde_datadir}/desktop-directories/*.directory
%{tde_datadir}/icons/crystalsvg/*/apps/systemsettings.png
%{tde_tdedocdir}/HTML/en/systemsettings/


%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 2:0.0svn20070312-1.2
- 为 Magic 3.0 重建

* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 2:0.0svn20070312-1.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:0.0svn20070312-1
- Initial release for TDE 14.0.0
