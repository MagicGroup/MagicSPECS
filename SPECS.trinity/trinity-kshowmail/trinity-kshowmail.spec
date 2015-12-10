#
# spec file for package kshowmail (version R14)
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
%define tde_pkg kshowmail
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
Version:	3.3.1
Release:	%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}.3
Summary:	Look messages into your mail server
Summary(zh_CN.UTF-8): 查看邮件服务器的信息
Group:		Applications/Internet
Group(zh_CN.UTF-8): 应用程序/互联网
URL:		http://sourceforge.net/projects/kshowmail/

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
BuildRequires:	trinity-tdepim-devel >= %{tde_version}

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig
BuildRequires:	fdupes

%description
Very simply kshowmail is a program that allows you to look in on your mail server,
see what is waiting, decide if it is legitimate, and delete it right off of the server if it is not.
All without dragging any messages into your computer.

%description -l zh_CN.UTF-8
查看你的邮件服务器上的信息。

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
  --enable-final \
  --enable-new-ldflags \
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

# Install missing icons
install -D -m 644 "pics/cr16-app-kshowmail.png" "$RPM_BUILD_ROOT%{tde_datadir}/icons/hicolor/16x16/apps/kshowmail.png"
install -D -m 644 "pics/kshowmail.png"          "$RPM_BUILD_ROOT%{tde_datadir}/icons/hicolor/48x48/apps/kshowmail.png"

%__rm -rf %{?buildroot}%{tde_tdedocdir}/HTML/{de,es,fr,hu,it,ru,sv}

%clean
%__rm -rf $RPM_BUILD_ROOT


%files 
%defattr(-,root,root,-)
%doc AUTHORS COPYING README ChangeLog
%{tde_bindir}/kshowmail
%{tde_tdelibdir}/kcm_kshowmailconfigaccounts.la
%{tde_tdelibdir}/kcm_kshowmailconfigaccounts.so
%{tde_tdelibdir}/kcm_kshowmailconfigactions.la
%{tde_tdelibdir}/kcm_kshowmailconfigactions.so
%{tde_tdelibdir}/kcm_kshowmailconfigdisplay.la
%{tde_tdelibdir}/kcm_kshowmailconfigdisplay.so
%{tde_tdelibdir}/kcm_kshowmailconfigfilter.la
%{tde_tdelibdir}/kcm_kshowmailconfigfilter.so
%{tde_tdelibdir}/kcm_kshowmailconfiggeneral.la
%{tde_tdelibdir}/kcm_kshowmailconfiggeneral.so
%{tde_tdelibdir}/kcm_kshowmailconfiglog.la
%{tde_tdelibdir}/kcm_kshowmailconfiglog.so
%{tde_tdelibdir}/kcm_kshowmailconfigspamcheck.la
%{tde_tdelibdir}/kcm_kshowmailconfigspamcheck.so
%{tde_tdeappdir}/kshowmail.desktop
%{tde_datadir}/apps/kshowmail/
%{tde_datadir}/icons/crystalsvg/16x16/apps/kshowmail.png
%{tde_datadir}/icons/hicolor/*/apps/kshowmail.png
%{tde_datadir}/services/kshowmailconfigaccounts.desktop
%{tde_datadir}/services/kshowmailconfigactions.desktop
%{tde_datadir}/services/kshowmailconfigdisplay.desktop
%{tde_datadir}/services/kshowmailconfigfilter.desktop
%{tde_datadir}/services/kshowmailconfiggeneral.desktop
%{tde_datadir}/services/kshowmailconfiglog.desktop
%{tde_datadir}/services/kshowmailconfigspamcheck.desktop
%lang(en) %{tde_tdedocdir}/HTML/en/kshowmail/

%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 2:3.3.1-1.3
- 为 Magic 3.0 重建

* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 2:3.3.1-1.2
- 为 Magic 3.0 重建

* Tue Oct 13 2015 Liu Di <liudidi@gmail.com> - 2:3.3.1-1.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:3.3.1-1
- Initial release for TDE 14.0.0
