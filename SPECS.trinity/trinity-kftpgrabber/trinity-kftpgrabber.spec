#
# spec file for package kftprgrabber (version R14)
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
%define tde_version 14.0.0
%endif
%define tde_pkg kftpgrabber
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


Name:			trinity-%{tde_pkg}
Epoch:			%{tde_epoch}
Version:        0.8.1
Release:		%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}
Summary:        A FTP client for TDE.
Group:          Applications/Internet
URL:            http://www.kftp.org/

%if 0%{?suse_version}
License:	GPL-2.0+
%else
License:	GPLv2+
%endif

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:			%{_prefix}
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz
Patch0:			%{tde_pkg}-14.0.0.patch


BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig

# SUSE desktop files utility
%if 0%{?suse_version}
BuildRequires:	update-desktop-files
%endif

%if 0%{?opensuse_bs} && 0%{?suse_version}
# for xdg-menu script
BuildRequires:	brp-check-trinity
%endif

# OPENSSL support
BuildRequires:	openssl-devel


%description
KFTPgrabber is a graphical FTP client for the Trinity Desktop Environment. It
implements many features required for usable FTP interaction.

Feature list:
- Multiple simultaneous FTP sessions in separate tabs
- A tree-oriented transfer queue
- TLS/SSL support for the control connection and the data channel
- X509 certificate support for authentication
- FXP site-to-site transfer support
- One-time password (OTP) support using S/KEY, MD5, RMD160 or SHA1
- Site bookmarks with many options configurable per-site
- Distributed FTP daemon support (implementing the PRET command)
- Can use Zeroconf for local site discovery
- Bookmark import plugins from other FTP clients
- Support for the SFTP protocol
- A nice traffic graph
- Ability to limit upload and download speed
- Priority and skip lists
- Integrated SFV checksum verifier
- Direct viewing/editing of remote files
- Advanced default "on file exists" action configuration
- Filter displayed files/directories as you type


%package devel
Summary:  	Development files for %{name}
Group: 		Development/Libraries
Requires: 	%{name} = %{version}-%{release}

%description devel
%{summary}


##########

%if 0%{?pclinuxos} || 0%{?suse_version} && 0%{?opensuse_bs} == 0
%debug_package
%endif

##########

%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}
%patch0 -p1 -b .orig

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR QTINC QTDIR
export PATH="%{tde_bindir}:${PATH}"

# Warning: --enable-final causes FTBFS
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
  --disable-final \
  --enable-closure \
  --enable-rpath \
  --disable-gcc-hidden-visibility
  
%__make %{?_smp_mflags}


%install
%__rm -rf $RPM_BUILD_ROOT
%__make install DESTDIR=$RPM_BUILD_ROOT

%find_lang %{tde_pkg}


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


%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING README ChangeLog
%{tde_bindir}/kftpgrabber
%{tde_libdir}/libkftpinterfaces.so.0
%{tde_libdir}/libkftpinterfaces.so.0.0.0
%{tde_tdelibdir}/kftpimportplugin_filezilla3.la
%{tde_tdelibdir}/kftpimportplugin_filezilla3.so
%{tde_tdelibdir}/kftpimportplugin_gftp.la
%{tde_tdelibdir}/kftpimportplugin_gftp.so
%{tde_tdelibdir}/kftpimportplugin_kftp.la
%{tde_tdelibdir}/kftpimportplugin_kftp.so
%{tde_tdelibdir}/kftpimportplugin_ncftp.la
%{tde_tdelibdir}/kftpimportplugin_ncftp.so
%{tde_tdeappdir}/kftpgrabber.desktop
%{tde_datadir}/apps/kftpgrabber/
%{tde_datadir}/config.kcfg/kftpgrabber.kcfg
%{tde_datadir}/icons/hicolor/*/apps/kftpgrabber.png
%{tde_datadir}/services/kftpimportplugin_filezilla3.desktop
%{tde_datadir}/services/kftpimportplugin_gftp.desktop
%{tde_datadir}/services/kftpimportplugin_kftp.desktop
%{tde_datadir}/services/kftpimportplugin_ncftp.desktop
%{tde_datadir}/servicetypes/kftpbookmarkimportplugin.desktop
%{tde_tdedocdir}/HTML/en/kftpgrabber/


%files devel
%defattr(-,root,root,-)
%{tde_tdeincludedir}/kftpgrabber/
%{tde_libdir}/libkftpinterfaces.la
%{tde_libdir}/libkftpinterfaces.so


%changelog
* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:0.8.1-1
- Initial release for TDE 14.0.0
