#
# spec file for package smartcardauth (version R14)
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
%define tde_pkg smartcardauth
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
Version:	1.0
Release:	%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}
Summary:	SmartCard Login and LUKS Decrypt, Setup Utility
Summary(zh_CN.UTF-8): 智能卡登录和加密设置工具
Group:		Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
URL:		http://www.trinitydesktop.org/

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz
Source1:		trinity-%{tde_pkg}-rpmlintrc

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig
BuildRequires:	fdupes

#BuildRequires:	perl-PAR-Packer
Requires:		pcsc-perl

# DB4/DB5 support
%define with_db 1
BuildRequires:  libdb-devel
BuildRequires:  libdb-cxx-devel

# PAM support
BuildRequires:	pam-devel


%description
This utility will allow you to set up your computer to accept a SmartCard as an authentication source for:
- Your encrypted LUKS partition
- TDE, including automatic login, lock, and unlock features

It is designed to work with any ISO 7816-1,2,3,4 compliant smartcard
Examples of such cards are:
- The Schlumberger MultiFlex
- The ACS ACOS5 / ACOS6 series of cryptographic ISO 7816 cards

If a card is chosen that has PKSC support, such as the ACOS cards, this utility can run
simultaneously with the certificate reading program(s) to provide single sign on
in addition to the PKCS certificate functionality

%description -l zh_CN.UTF-8
智能卡登录和加密设置工具。

##########

%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}

%__sed -i "Makefile" \
	-e "s|/usr/lib/perl5/Chipcard|%{_libdir}/perl5/vendor_perl/Chipcard|g"


%build
export PATH="%{tde_bindir}:${PATH}"

cd src
make CFLAGS="${RPM_OPT_FLAGS}"  CXXFLAGS="${RPM_OPT_FLAGS}"


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}

%__install -D -m 755 scriptor_standalone.pl %{buildroot}%{tde_bindir}/scriptor.pl
%__install -D -m 755 src/ckpasswd %{buildroot}%{tde_bindir}/smartauthckpasswd
#%__install -D -m 755 src/ckpasswd %{buildroot}%{tde_bindir}/smartauthmon
%__ln_s smartauthckpasswd %{buildroot}%{tde_bindir}/smartauthmon
%__cp -Rp usr/*  %{buildroot}%{tde_prefix}

%__mkdir_p %{buildroot}%{_sysconfdir}
%__cp -Rp etc/* %{buildroot}%{_sysconfdir}

echo "OnlyShowIn=TDE;" >>"%{?buildroot}%{tde_datadir}/applications/smartcardauth.desktop"
echo "OnlyShowIn=TDE;" >>"%{?buildroot}%{tde_datadir}/applications/smartcardrestrict.desktop"
magic_rpm_clean.sh

%clean
%__rm -rf %{buildroot}


%post
update-desktop-database %{tde_tdeappdir} > /dev/null
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :

%postun
update-desktop-database %{tde_tdeappdir} > /dev/null
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :


%files
%defattr(-,root,root,-)
%doc gpl.txt
%{_sysconfdir}/init/smartauthlogin.conf
%{_sysconfdir}/smartauth/
%{tde_bindir}/cryptosmartcard.sh
%{tde_bindir}/scriptor.pl
%{tde_bindir}/setupcard.sh
%{tde_bindir}/setupslavecard.sh
%{tde_bindir}/smartauth.sh
%{tde_bindir}/smartauthckpasswd
%{tde_bindir}/smartauthmon
%{tde_datadir}/applications/smartcardauth.desktop
%{tde_datadir}/applications/smartcardrestrict.desktop
%{tde_datadir}/icons/hicolor/16x16/apps/smartcardauth.png
%{tde_datadir}/icons/hicolor/32x32/apps/smartcardauth.png
%{tde_datadir}/initramfs-tools/hooks/cryptlukssc


%changelog
* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:1.0-1
- Initial release for TDE 14.0.0
