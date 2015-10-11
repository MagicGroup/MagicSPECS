#
# spec file for package kiosktool (version R14)
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
%define tde_pkg kiosktool
%define tde_prefix /opt/trinity
%define tde_appdir %{tde_datadir}/applications
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


Name:			trinity-%{tde_pkg}
Epoch:			%{tde_epoch}
Version:		1.0
Release:		%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}
Summary:		Tool to configure the TDE kiosk framework
Group:			Applications/Multimedia
URL:			http://www.trinitydesktop.org/

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

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

BuildRequires:	gettext

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


%description
A Point&Click tool for system administrators to enable 
TDE's KIOSK features or otherwise preconfigure TDE for 
groups of users.


##########

%if 0%{?pclinuxos} || 0%{?suse_version} && 0%{?opensuse_bs} == 0
%debug_package
%endif

##########


%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}

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
  
%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf $RPM_BUILD_ROOT
%__make install DESTDIR=$RPM_BUILD_ROOT

%find_lang %{tde_pkg}

%__mkdir_p "%{?buildroot}%{tde_confdir}"
cat <<EOF >"%{?buildroot}%{tde_confdir}/kiosktoolrc"
[General]
GroupBlacklist=bin,daemon,sys,tty,disk,lp,www,kmem,wheel,mail,news,uucp,shadow,utmp,at,xok,named,ftp,postfix,maildrop,man,sshd,distcc,nobody,nogroup
EOF

# Updates applications categories for openSUSE
echo "OnlyShowIn=TDE;" >>"%{?buildroot}%{tde_tdeappdir}/%{tde_pkg}.desktop"
%if 0%{?suse_version}
%suse_update_desktop_file %{tde_pkg} System SystemSetup
%endif


%clean
%__rm -rf $RPM_BUILD_ROOT


%post
touch --no-create %{tde_datadir}/icons/crystalsvg ||:
gtk-update-icon-cache -q %{tde_datadir}/icons/crystalsvg 2> /dev/null ||:
update-desktop-database >& /dev/null ||:

%postun
touch --no-create %{tde_datadir}/icons/crystalsvg ||:
gtk-update-icon-cache -q %{tde_datadir}/icons/crystalsvg 2> /dev/null ||:
update-desktop-database >& /dev/null ||:



%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%doc ChangeLog COPYING README TODO
%{tde_bindir}/kiosktool
%{tde_bindir}/kiosktool-tdedirs
%{tde_tdeappdir}/kiosktool.desktop
%{tde_datadir}/apps/kiosktool/
%{tde_tdedocdir}/HTML/en/kiosktool/
%{tde_datadir}/icons/crystalsvg/*/apps/kiosktool.png
%{tde_confdir}/kiosktoolrc

%changelog
* Mon Jul 29 2013 Francois Andriot <francois.andriot@free.fr> - 2:1.0-1
- Initial release for TDE 14.0.0
