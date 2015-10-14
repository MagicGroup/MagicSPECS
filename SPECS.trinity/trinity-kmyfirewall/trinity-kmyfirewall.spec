#
# spec file for package kmyfirewall (version R14)
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
%define tde_pkg kmyfirewall
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_confdir %{_sysconfdir}/trinity
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
Version:	1.1.1
Release:	%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}
Summary:	Iptables based firewall configuration tool for TDE
Summary(zh_CN.UTF-8): TDE 下 Iptables 防火墙的配置工具
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

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig
BuildRequires:	libtool


%description
KMyFirewall attempts to make it easier to setup iptables based firewalls on
Linux systems. It will be the right tool if you like to have a so called
"Personal Firewall" running on your Linux box, but don't have the time and/or
the interest to spend hours in front of the iptables manual just to setup a 
Firewall that keeps the "bad" people out.

There is also the possibility to save entire rule sets, so you only have to
configure your rule set one time and then you can use it on several computers
giving each of them a similar configuration (p.e. school networks, office,
university etc.)

%description -l zh_CN.UTF-8
TDE 下的 Iptables 防火墙配置工具。

%post
update-desktop-database %{tde_tdeappdir} > /dev/null
for f in hicolor locolor; do
  touch --no-create %{tde_datadir}/icons/${f} || :
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f} || :
done
/sbin/ldconfig || :

%postun
update-desktop-database %{tde_tdeappdir} > /dev/null
for f in hicolor locolor; do
  touch --no-create %{tde_datadir}/icons/${f} || :
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f} || :
done
/sbin/ldconfig || :

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING COPYING-DOCS README TODO
%{tde_bindir}/kmyfirewall
%{tde_libdir}/libkmfcore.so.*
%{tde_libdir}/libkmfwidgets.so.*
%{tde_tdelibdir}/libkmfcompiler_ipt.la
%{tde_tdelibdir}/libkmfcompiler_ipt.so
%{tde_tdelibdir}/libkmfgenericinterfacepart.la
%{tde_tdelibdir}/libkmfgenericinterfacepart.so
%{tde_tdelibdir}/libkmfinstaller_linux.la
%{tde_tdelibdir}/libkmfinstaller_linux.so
%{tde_tdelibdir}/libkmfinstallerplugin.la
%{tde_tdelibdir}/libkmfinstallerplugin.so
%{tde_tdelibdir}/libkmfipteditorpart.la
%{tde_tdelibdir}/libkmfipteditorpart.so
%{tde_tdelibdir}/libkmfruleoptionedit_custom.la
%{tde_tdelibdir}/libkmfruleoptionedit_custom.so
%{tde_tdelibdir}/libkmfruleoptionedit_interface.la
%{tde_tdelibdir}/libkmfruleoptionedit_interface.so
%{tde_tdelibdir}/libkmfruleoptionedit_ip.la
%{tde_tdelibdir}/libkmfruleoptionedit_ip.so
%{tde_tdelibdir}/libkmfruleoptionedit_limit.la
%{tde_tdelibdir}/libkmfruleoptionedit_limit.so
%{tde_tdelibdir}/libkmfruleoptionedit_mac.la
%{tde_tdelibdir}/libkmfruleoptionedit_mac.so
%{tde_tdelibdir}/libkmfruleoptionedit_protocol.la
%{tde_tdelibdir}/libkmfruleoptionedit_protocol.so
%{tde_tdelibdir}/libkmfruleoptionedit_state.la
%{tde_tdelibdir}/libkmfruleoptionedit_state.so
%{tde_tdelibdir}/libkmfruleoptionedit_tos.la
%{tde_tdelibdir}/libkmfruleoptionedit_tos.so
%{tde_tdelibdir}/libkmfruletargetoptionedit_log.la
%{tde_tdelibdir}/libkmfruletargetoptionedit_log.so
%{tde_tdelibdir}/libkmfruletargetoptionedit_mark.la
%{tde_tdelibdir}/libkmfruletargetoptionedit_mark.so
%{tde_tdelibdir}/libkmfruletargetoptionedit_nat.la
%{tde_tdelibdir}/libkmfruletargetoptionedit_nat.so
%{tde_tdelibdir}/libkmfruletargetoptionedit_tos.la
%{tde_tdelibdir}/libkmfruletargetoptionedit_tos.so
%{tde_tdeappdir}/kmyfirewall.desktop
%{tde_datadir}/apps/kmfgenericinterfacepart/
%{tde_datadir}/apps/kmfipteditorpart/
%{tde_datadir}/apps/kmfsystray/
%{tde_datadir}/apps/kmyfirewall/
%{tde_datadir}/config.kcfg/kmfconfig.kcfg
%{tde_confdir}/kmyfirewallrc
%{tde_tdedocdir}/HTML/en/kmyfirewall/
%{tde_datadir}/icons/hicolor/*/apps/kmyfirewall.png
%{tde_datadir}/icons/locolor/*/apps/kmyfirewall.png
%{tde_datadir}/mimelnk/application/kmfgrs.desktop
%{tde_datadir}/mimelnk/application/kmfnet.desktop
%{tde_datadir}/mimelnk/application/kmfpkg.desktop
%{tde_datadir}/mimelnk/application/kmfrs.desktop
%{tde_datadir}/services/kmf*.desktop
%{tde_datadir}/servicetypes/kmf*.desktop

##########

%package devel
Summary:		Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:			Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:		%{name} = %{epoch}:%{version}-%{release}

%description devel
%{summary}

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%files devel
%{tde_tdeincludedir}/kmyfirewall
%{tde_libdir}/libkmfcore.la
%{tde_libdir}/libkmfcore.so
%{tde_libdir}/libkmfwidgets.la
%{tde_libdir}/libkmfwidgets.so

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
export kde_confdir="%{tde_confdir}"

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

%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}
magic_rpm_clean.sh

%clean
%__rm -rf %{buildroot}


%changelog
* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:1.1.1-1
- Initial release for TDE 14.0.0
