# Default version for this component
%define kdecomp smartcardauth
%define tdeversion 3.5.13.2

# If TDE is built in a specific prefix (e.g. /opt/trinity), the release will be suffixed with ".opt".
%if "%{?tde_prefix}" != "/usr"
%define _variant .opt
%endif

# TDE 3.5.13 specific building variables
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_appdir %{tde_datadir}/applications

%define tde_tdeappdir %{tde_appdir}/kde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%define _docdir %{tde_tdedocdir}


Name:		trinity-%{kdecomp}
Summary:	SmartCard Login and LUKS Decrypt, Setup Utility
Version:	1.0
Release:	3%{?dist}%{?_variant}

License:	GPLv2+
Group:		Applications/System

Vendor:		Trinity Project
Packager:	Francois Andriot <francois.andriot@free.fr>
URL:		http://www.trinitydesktop.org/

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	%{kdecomp}-trinity-%{tdeversion}.tar.xz
Patch0:		smartcardauth-3.5.13-ftbfs.patch

BuildRequires:	trinity-tqtinterface-devel >= 3.5.13.1
BuildRequires:	trinity-tdelibs-devel >= 3.5.13.1
BuildRequires:	trinity-tdebase-devel >= 3.5.13.1
BuildRequires: desktop-file-utils

#BuildRequires:	perl-PAR-Packer
%if 0%{?mgaversion} || 0%{?mdkversion}
Requires:		perl-pcsc-perl
%endif
%if 0%{?rhel} || 0%{?fedora}
Requires:		pcsc-perl
%endif
%if 0%{?suse_version}
Requires:		perl-pcsc
%endif

%description
This utility will allow you to set up your computer to accept a SmartCard as an authentication source for:
- Your encrypted LUKS partition
- TDE3.x, including automatic login, lock, and unlock features

It is designed to work with any ISO 7816-1,2,3,4 compliant smartcard
Examples of such cards are:
- The Schlumberger MultiFlex
- The ACS ACOS5 / ACOS6 series of cryptographic ISO 7816 cards

If a card is chosen that has PKSC support, such as the ACOS cards, this utility can run
simultaneously with the certificate reading program(s) to provide single sign on
in addition to the PKCS certificate functionality


%if 0%{?suse_version}
%debug_package
%endif


%prep
unset QTDIR; . /etc/profile.d/qt3.sh
%setup -q -n %{kdecomp}-trinity-%{tdeversion}

# Ugly hack to modify TQT include directory inside autoconf files.
# If TQT detection fails, it fallbacks to TQT4 instead of TQT3 !
%__sed -i "src/Makefile" \
	-e "s|/usr/include/tqt|%{tde_includedir}/tqt|g" \
	-e "s|/usr/include/qt3|${QTINC}|g"

%__sed -i "Makefile" \
	-e "s|/usr/lib/perl5/Chipcard|/usr/lib64/perl5/vendor_perl/Chipcard|g"

%build
export PATH="%{tde_bindir}:${PATH}"
export LDFLAGS="-L%{tde_libdir} -I%{tde_includedir}"

./build_ckpasswd


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


%clean
%__rm -rf %{buildroot}


%post
update-desktop-database %{tde_appdir} > /dev/null
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :

%postun
update-desktop-database %{tde_appdir} > /dev/null
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :


%files
%defattr(-,root,root,-)
%doc gpl.txt
%{_sysconfdir}/init/smartauthlogin.conf
%{_sysconfdir}/smartauth/smartauth.sh.in
%{_sysconfdir}/smartauth/smartauthmon.sh.in
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
* Tue Aug 06 2013 Liu Di <liudidi@gmail.com> - 1.0-3.opt
- 为 Magic 3.0 重建

* Wed Oct 03 2012 Francois Andriot <francois.andriot@free.fr> - 1.0-2
- Initial build for TDE 3.5.13.1

* Sat Dec 03 2011 Francois Andriot <francois.andriot@free.fr> - 1.0-1
- Initial build for RHEL 5, RHEL 6, Fedora 15, Fedora 16

