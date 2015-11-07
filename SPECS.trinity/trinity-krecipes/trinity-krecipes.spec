#
# spec file for package krecipes (version R14)
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
%define tde_pkg krecipes
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
Version:	1.0beta2
Release:	%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}.2
Summary:	Recipes manager for TDE
Summary(zh_CN.UTF-8): TDE 下的食谱管理程序
Group:		Applications/Utilities
Group(zh_CN.UTF-8): 应用程序/工具
URL:		http://www.trinitydesktop.org/
License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz

Patch1:		%{name}-14.0.1-tqt.patch

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	desktop-file-utils
BuildRequires:	gettext

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig
BuildRequires:	fdupes

# MYSQL support
BuildRequires:	mysql-devel

# POSTGRESQL support
BuildRequires:	postgresql-devel

# SQLITE support
BuildRequires:	sqlite-devel


%description
Krecipes is a TDE application designed to manage recipes. It can help you to
do your shopping list, search through your recipes to find what you can do
with available ingredients and a diet helper. It can also import or export
recipes from files in various format (eg RecipeML or Meal-Master) or from
databases.

%description -l zh_CN.UTF-8
TDE 下的食谱管理程序。

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
  --docdir=%{tde_tdedocdir} \
  --libdir=%{tde_libdir} \
  \
  --disable-dependency-tracking \
  --disable-debug \
  --enable-new-ldflags \
  --enable-final \
  --enable-closure \
  --enable-rpath \
  --disable-gcc-hidden-visibility \
  \
  --with-sqlite \
  --with-mysql \
  --with-postgresql

%__make %{?_smp_mflags} || %__make


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}
magic_rpm_clean.sh
%find_lang %{tde_pkg} || :

# Fix desktop file location
%__mkdir_p "%{?buildroot}%{tde_tdeappdir}"
%__mv -f "%{?buildroot}%{tde_datadir}/applnk/"*"/krecipes.desktop" "%{?buildroot}%{tde_tdeappdir}"

# Removes duplicate files
%fdupes "%{buildroot}%{tde_datadir}"

rm -rf %{buildroot}%{tde_tdedocdir}/HTML/{da,es,et,pt,sv}

%clean
%__rm -rf %{buildroot}


%post
for f in crystalsvg hicolor ; do
  touch --no-create %{tde_datadir}/icons/${f} || :
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f} || :
done


%postun
for f in crystalsvg hicolor ; do
  touch --no-create %{tde_datadir}/icons/${f} || :
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f} || :
done


%files 
%defattr(-,root,root,-)
%{tde_bindir}/krecipes
%{tde_tdeappdir}/krecipes.desktop
%{tde_datadir}/apps/krecipes/
%{tde_datadir}/icons/crystalsvg/*/mimetypes/krecipes_file.png
%{tde_datadir}/icons/hicolor/*/apps/krecipes.png
%{tde_datadir}/mimelnk/application/x-krecipes-backup.desktop
%{tde_datadir}/mimelnk/application/x-krecipes-recipes.desktop
%lang(en) %{tde_tdedocdir}/HTML/en/

%changelog
* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 2:1.0beta2-1.2
- 为 Magic 3.0 重建

* Tue Oct 13 2015 Liu Di <liudidi@gmail.com> - 2:1.0beta2-1.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:1.0beta2-1
- Initial release for TDE 14.0.0
