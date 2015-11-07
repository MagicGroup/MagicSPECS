#
# spec file for package kscope (version R14)
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
%define tde_pkg kscope
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
Version:	1.6.2
Release:	%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}.2
Summary:	Source editing environment for TDE
Summary(zh_CN.UTF-8): TDE 下的源码编辑环境
Group:		Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
URL:		http://kscope.sourceforge.net
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
Requires:		cscope

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig
BuildRequires:	fdupes

BuildRequires:	flex
BuildRequires:	bison


%description
KScope is a TDE front-end to Cscope. It provides a source-editing environment
for large C projects. KScope is focused on source editing and analysis.

KScope is built around an efficient mechanism for code-navigation, which
allows the user to run queries on the code.

The types of queries KScope can run include:
* Get all references to a symbol
* Find the definition of a symbol
* Find all functions called by or calling to a function
* Find an EGrep pattern
* Find all files #including some file

These queries are handled by an underlying Cscope process. KScope simply
serves as a front-end to this process, feeding it with queries, and parsing
its output into result lists. The items in those lists can later be selected
to open an editor at the matching line.

Main Features:
* Multiple editor windows (using your favourite TDE editor)
* Project management
* Front-end to most Cscope queries
* Tag list for every open editor
* Call-tree window
* Session management, including saving and restoring queries
* Works with externally-built cscope.out files

%description -l zh_CN.UTF-8
TDE 下的源码编辑环境。

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
  --mandir=%{tde_mandir} \
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
magic_rpm_clean.sh
%find_lang %{tde_pkg} || :

# Move desktop icon to correct location
%__mkdir_p "%{?buildroot}%{tde_tdeappdir}"
%__mv -f "%{?buildroot}%{tde_datadir}/applnk/"*"/%{tde_pkg}.desktop" "%{?buildroot}%{tde_tdeappdir}"

%clean
%__rm -rf $RPM_BUILD_ROOT


%post
for i in hicolor locolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done


%postun
for i in hicolor locolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done


%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING README ChangeLog
%{tde_bindir}/kscope
%{tde_tdeappdir}/kscope.desktop
%{tde_datadir}/apps/kscope/
%{tde_tdedocdir}/HTML/en/kscope/
%{tde_datadir}/icons/hicolor/*/apps/kscope.png
%{tde_datadir}/icons/locolor/*/apps/kscope.png


%changelog
* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 2:1.6.2-1.2
- 为 Magic 3.0 重建

* Tue Oct 13 2015 Liu Di <liudidi@gmail.com> - 2:1.6.2-1.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:1.6.2-1
- Initial release for TDE 14.0.0
