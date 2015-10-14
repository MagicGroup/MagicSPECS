#
# spec file for package kdirstat (version R14)
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
%define tde_pkg kdirstat
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


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	2.4.4
Release:	%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}
Summary:	Graphical disk usage display with cleanup facilities [Trinity]
Summary(zh_CN.UTF-8): 图形化的显示磁盘使用情况
Group:		Applications/Utilities
Group(zh_CN.UTF-8): 应用程序/工具
URL:		http://www.trinitydesktop.org

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz
Patch1:		%{name}-14.0.1-tqt.patch

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

BuildRequires:	gettext

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig
BuildRequires:	libtool

%description
KDirStat (TDE Directory Statistics) is a small utility program that sums
up disk usage for directory trees, very much like the Unix 'du' command.
It displays the disk space used up by a directory tree, both numerically
and graphically.  It is network transparent (i.e., you can use it to sum
up FTP servers), and comes with predefined and user configurable cleanup
actions.  You can directly open a directory branch in Konqueror or the
shell of your choice, compress it to a .tar.bz2 archive, or define your
own cleanup actions. 

%description -l zh_CN.UTF-8
图形化的显示目录的磁盘使用情况。

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
  --datadir=%{tde_datadir} \
  --includedir=%{tde_tdeincludedir} \
  --libdir=%{tde_libdir} \
  --mandir=%{tde_mandir} \
  \
  --disable-dependency-tracking \
  --disable-debug \
  --enable-new-ldflags \
  --enable-final \
  --enable-closure \
  --enable-rpath \
  --disable-gcc-hidden-visibility

# SMP safe !
%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}
magic_rpm_clean.sh
%find_lang %{tde_pkg} || :

# Fix desktop file location
%__mkdir_p "%{?buildroot}%{tde_tdeappdir}"
%__mv -f "%{?buildroot}%{tde_datadir}/applnk/Utilities/kdirstat.desktop" "%{?buildroot}%{tde_tdeappdir}"

%clean
%__rm -rf %{buildroot}


%post
for f in hicolor locolor; do
  touch --no-create %{tde_datadir}/icons/${f} || :
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f} || :
done

%postun
for f in hicolor locolor; do
  touch --no-create %{tde_datadir}/icons/${f} || :
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f} || :
done


%files
%defattr(-,root,root,-)
%{tde_bindir}/kdirstat
%{tde_tdeappdir}/kdirstat.desktop
%{tde_datadir}/apps/tdeconf_update/fix_move_to_trash_bin.pl
%{tde_datadir}/apps/tdeconf_update/kdirstat.upd
%{tde_datadir}/apps/kdirstat/
%{tde_tdedocdir}/HTML/en/kdirstat/
%{tde_datadir}/icons/hicolor/*/apps/kdirstat.png
%{tde_datadir}/icons/locolor/*/apps/kdirstat.png


%changelog
* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:2.4.4-1
- Initial release for TDE 14.0.0
