#
# spec file for package kopete-otr (version R14)
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
%define tde_pkg kopete-otr
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

# Required for Mageia 2: removes the ldflag '--no-undefined'
%define _disable_ld_no_undefined 1


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	0.7
Release:	%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}.1
Summary:	Off-The-Record encryption for Kopete [Trinity]
Summary(zh_CN.UTF-8): Kopete 的 OTR 加密
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
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils
BuildRequires:	trinity-tdenetwork-devel >= %{tde_version}

# Kopete is provided by tdenetwork
Requires:		trinity-kopete >= %{tde_version}

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig

# OTR support
BuildRequires:	libotr-devel


%description
This plugin enables Off-The-Record encryption for the TDE instant
messenger Kopete. Using this plugin you can encrypt chatsessions to other
users with IM-Cients supporting the OTR encryption method.

%description -l zh_CN.UTF-8
Kopete 的 OTR 加密。

##########

%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}
%patch1 -p1

%__cp "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"

%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --datadir=%{tde_datadir} \
  --libdir=%{tde_libdir} \
  --mandir=%{tde_mandir} \
  --includedir=%{tde_tdeincludedir} \
  \
  --disable-dependency-tracking \
  --disable-debug \
  --enable-new-ldflags \
  --enable-final \
  --enable-closure \
  --enable-rpath \
  --disable-gcc-hidden-visibility

%__make %{_smp_mflags} || %__make


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

# Unwanted files
%__rm -f %{?buildroot}%{tde_libdir}/libkotr.so
magic_rpm_clean.sh
%find_lang kopete_otr || :


%clean
%__rm -rf %{buildroot}


%post
touch --no-create %{tde_datadir}/icons/crystalsvg || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/crystalsvg || :
/sbin/ldconfig || :

%postun
touch --no-create %{tde_datadir}/icons/crystalsvg || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/crystalsvg || :
/sbin/ldconfig || :


%files 
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README TODO
%{tde_libdir}/libkotr.la
%{tde_libdir}/libkotr.so.0
%{tde_libdir}/libkotr.so.0.0.0
%{tde_tdelibdir}/kcm_kopete_otr.la
%{tde_tdelibdir}/kcm_kopete_otr.so
%{tde_tdelibdir}/kopete_otr.la
%{tde_tdelibdir}/kopete_otr.so
%{tde_datadir}/apps/kopete_otr
%{tde_datadir}/config.kcfg/kopete_otr.kcfg
%{tde_tdedocdir}/HTML/en/kopete_otr/
%{tde_datadir}/icons/crystalsvg/16x16/apps/kopete_otr.png
%{tde_datadir}/services/tdeconfiguredialog/kopete_otr_config.desktop
%{tde_datadir}/services/kopete_otr.desktop


%changelog
* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 2:0.7-1.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:0.7-1
- Initial release for TDE 14.0.0
