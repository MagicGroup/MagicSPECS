#
# spec file for package kbibtex (version R14)
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
%define tde_pkg kbibtex
%define tde_prefix /opt/trinity
%define tde_appdir %{tde_datadir}/applications
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


Name:			trinity-%{tde_pkg}
Epoch:			%{tde_epoch}
Version:        0.2.3
Release:		%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}.1
Summary:        A BibTeX editor for TDE
Summary(zh_CN.UTF-8): TDE 下的 BibTeX 编辑器
Group:          Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
URL:            http://www.unix-ag.uni-kl.de/~fischer/kbibtex/download.html

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:			%{_prefix}
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz
Patch1:			%{name}-14.0.1-tqt.patch

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

BuildRequires:	gettext

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig

# XSLT support
BuildRequires:	libxslt-devel


%description
KBibTeX is a BibTeX editor for TDE to edit bibliographies used with LaTeX.
KBibTeX is released under the GNU Public License (GPL) version 2 or any later version.

%description -l zh_CN.UTF-8
TDE 下的 BibTeX 编辑器。

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

# Warning: --enable-final causes FTBFS
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
  --disable-final \
  --enable-closure \
  --enable-rpath \
  --disable-gcc-hidden-visibility
  
%__make %{?_smp_mflags}


%install
%__rm -rf $RPM_BUILD_ROOT
%__make install DESTDIR=$RPM_BUILD_ROOT

# Useless files ..
%__rm -f %{?buildroot}%{tde_tdelibdir}/*.a
magic_rpm_clean.sh
%find_lang %{tde_pkg} || :

%clean
%__rm -rf $RPM_BUILD_ROOT


%post
for i in hicolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
update-desktop-database %{tde_tdeappdir} > /dev/null

%postun
for i in hicolor ; do
 touch --no-create %{tde_datadir}/icons/$i 2>/dev/null || :
 gtk-update-icon-cache --quiet %{tde_datadir}/icons/$i 2>/dev/null || :
done
update-desktop-database %{tde_tdeappdir} > /dev/null


%files 
%defattr(-,root,root,-)
%doc AUTHORS BUGS COPYING NEWS README TODO ChangeLog
%{tde_bindir}/kbibtex
%{tde_tdelibdir}/libkbibtexpart.la
%{tde_tdelibdir}/libkbibtexpart.so
%{tde_tdeappdir}/kbibtex.desktop
%{tde_datadir}/apps/kbibtex/
%dir %{tde_datadir}/apps/kbibtexpart
%{tde_datadir}/apps/kbibtexpart/kbibtex_part.rc
%dir %{tde_datadir}/apps/kbibtexpart/xslt
%{tde_datadir}/apps/kbibtexpart/xslt/MARC21slim2MODS3.xsl
%{tde_datadir}/apps/kbibtexpart/xslt/MARC21slimUtils.xsl
%{tde_datadir}/apps/kbibtexpart/xslt/UNIMARC2MODS3.xsl
%{tde_datadir}/apps/kbibtexpart/xslt/html.xsl
%{tde_datadir}/icons/hicolor/*/apps/kbibtex.png
%{tde_datadir}/services/kbibtex_part.desktop
%{tde_mandir}/man1/kbibtex.1*
%{tde_tdedocdir}/HTML/en/kbibtex/


%changelog
* Sat Oct 10 2015 Liu Di <liudidi@gmail.com> - 2:0.2.3-1.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:0.2.3-1
- Initial release for TDE 14.0.0
