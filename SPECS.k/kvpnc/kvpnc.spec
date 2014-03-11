Summary: 	A KDE frontend for various vpn clients
Name:   	kvpnc
Version: 	0.9.6
Release: 	1%{?dist}
License: 	GPLv2+
Group: 		Applications/Networking
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source: 	http://download.gna.org/kvpnc/kvpnc-%{version}%{?betaver:-%{betaver}}.tar.bz2
Patch0:		 kvpnc-0.9.6-admin.patch
URL: 		http://home.gna.org/kvpnc/en/index.html
BuildRequires:	kdelibs-devel libjpeg-devel libpng-devel


%description
KVpnc is a KDE Desktop Environment frontend for various vpn clients.
It supports Cisco VPN (vpnc), IPSec (FreeS/WAN (OpenS/WAN), racoon), PPTP (pptpclient) and OpenVPN.

%prep
%setup -q -n kvpnc-%{version}%{?betaver:-%{betaver}}
%patch0 -p1

%build
make -f admin/Makefile.common
%configure --disable-rpath --disable-debug --with-xinerama --with-fpic --with-gnu-ld
#临时措施
sed -i 's/\/include\/tqt/\/include\/tqt \-lqt\-mt \-ltdecore \-ltdeui \-lkwalletclient \-lDCOP \-lkio/g' src/Makefile
%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

install -d %{buildroot}/%{_datadir}/config/
make install-strip DESTDIR=%buildroot

magic_rpm_clean.sh

%find_lang %{name}

# Stolen from guarddog spec
### consolehelper entry
#mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps
#ln -sf consolehelper $RPM_BUILD_ROOT%{_bindir}/%{name}
#cat > $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps/%{name} <<EOF
#USER=root
#PROGRAM=%{_sbindir}/%{name}
#SESSION=true
#FALLBACK=true
#EOF

### pam entry
#mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pam.d
#cat > $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/%{name} <<EOF
#auth       sufficient   pam_rootok.so
#auth       include	system-auth
#session    optional     pam_xauth.so
#account    required     pam_permit.so
#EOF

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig 
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/*
%{_datadir}/doc/HTML/kvpnc
%{_datadir}/doc/HTML/en/kvpnc
%{_datadir}/applnk
%{_datadir}/apps/kvpnc
%{_datadir}/config
%{_datadir}/icons
#%config(noreplace) %{_sysconfdir}/pam.d/%{name}


%changelog
* Fri Jul 04 2008 Funda Wang <fundawang@mandriva.org> 0.9.1-0.rc1.2mdv2009.0
+ Revision: 231508
- rebuild

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Tue Jun 03 2008 Funda Wang <fundawang@mandriva.org> 0.9.1-0.rc1.1mdv2009.0
+ Revision: 214652
- New version 0.9.1-rc1 ( kde4 version !! )

  + Thierry Vignaud <tvignaud@mandriva.com>
    - fix no-buildroot-tag

* Wed Dec 26 2007 Funda Wang <fundawang@mandriva.org> 0.9.0-1mdv2008.1
+ Revision: 137856
- New version 0.9.0

  + Thierry Vignaud <tvignaud@mandriva.com>
    - kill re-definition of %%buildroot on Pixel's request

* Thu May 03 2007 Laurent Montel <lmontel@mandriva.org> 0.8.9-1mdv2008.0
+ Revision: 20866
- 0.8.9


* Wed Feb 14 2007 Laurent Montel <lmontel@mandriva.com> 0.8.8-1mdv2007.0
+ Revision: 120750
- 0.8.8

* Wed Dec 13 2006 Laurent Montel <lmontel@mandriva.com> 0.8.7-1mdv2007.1
+ Revision: 96178
- 0.8.7

  + Lenny Cartier <lenny@mandriva.com>
    - Import kvpnc

* Tue Sep 26 2006 Laurent MONTEL <lmontel@mandriva.com> 0.8.6-1
- New version

* Mon Jul 24 2006 Nicolas L閏ureuil <neoclust@mandriva.org> 0.8.5.1-3mdv2007.0
- Fix for new PAM

* Mon Jun 19 2006 Nicolas L閏ureuil <neoclust@mandriva.org> 0.8.5.1-2mdv2007.0
- Rebuild to regenerate menu

* Sun May 21 2006 Laurent MONTEL <lmontel@mandriva.com> 0.8.5.1-1
- 0.8.5.1

* Fri May 19 2006 Lenny Cartier <lenny@mandriva.com> 0.8.5-1mdk
- 0.8.5

* Thu May 11 2006 Nicolas L閏ureuil <neoclust@mandriva.org> 0.8.4-4mdk
- Remove redundant BuildRequires

* Wed May 10 2006 Nicolas L閏ureuil <neoclust@mandriva.org> 0.8.4-3mdk
- Fix BuildRequires

* Tue May 09 2006 Laurent MONTEL <lmontel@mandriva.com> 0.8.4-2
- Rebuild to generate category

* Wed Apr 12 2006 Laurent MONTEL <lmontel@mandriva.com> 0.8.4-1
- 0.8.4

* Sun Mar 05 2006 Nicolas L閏ureuil <neoclust@mandriva.org> 0.8.3-1mdk
- New release 0.8.3

* Sat Jan 07 2006 Anssi Hannula <anssi@mandriva.org> 0.8.2.1-2mdk
- fix x86_64 build

* Tue Dec 27 2005 Laurent MONTEL <lmontel@mandriva.com> 0.8.2.1-1
- 0.8.2.1

* Sun Dec 25 2005 Nicolas L閏ureuil <neoclust@mandriva.org> 0.8.2-2mdk
- Fix BuildRequires

* Sun Dec 25 2005 Nicolas L閏ureuil <neoclust@mandriva.org> 0.8.2-1mdk
- New release 0.8.2
- Drop patch 2 : Merged Upstream

* Tue Oct 11 2005 Daouda LO <daouda@mandriva.com> 0.8-2mdk
- fix crash on startup

* Wed Oct 05 2005 Nicolas L閏ureuil <neoclust@mandriva.org> 0.8-1mdk
- New release 0.8
- fix file section

* Sat Jul 09 2005 Laurent MONTEL <lmontel@mandriva.com> 0.7.2-2
- REbuild

* Thu Jul 07 2005 Laurent MONTEL <lmontel@mandriva.com> 0.7.2-1
- 0.7.2

* Fri Jun 17 2005 Laurent MONTEL <lmontel@mandriva.com> 0.7-1
- 0.7

* Tue Jun 07 2005 Laurent MONTEL <lmontel@mandriva.com> 0.7-0.rc1.1
- 0.7rc1

* Tue Apr 26 2005 Nicolas L閏ureuil <neoclust@mandriva.org> 0.6.1-2mdk
- Fix build for amd64

* Sat Apr 02 2005 Laurent MONTEL <lmontel@mandrakesoft.com> 0.6.1-1mdk
- 0.6.1

* Fri Mar 11 2005 Laurent MONTEL <lmontel@mandrakesoft.com> 0.6-2mdk
- Reupload

* Mon Feb 28 2005 Laurent MONTEL <lmontel@mandrakesoft.com> 0.6-1mdk
- 0.6

* Wed Dec 29 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 0.5.1-1mdk
- 0.5.1

* Wed Dec 29 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 0.5-4mdk
- Add patch2: fix crash in configure settings

* Wed Dec 29 2004 Laurent MONTEL <lmontel@mandrakesoft.com> 0.5-3mdk
- Fix spec file
- Add debug flag
- Add enable-final flag
- Fix pam entry
- Now necessary consolehelper stuff which broke all kvpnc

* Sun Dec 26 2004 Couriousous <couriousous@mandrake.org> 0.5-2mdk
- Add consolehelper stuff as kvpnc requires to run as root
- Add Requires kvpnc-backend
  Thank misc for all the explications

* Sun Dec 26 2004 Couriousous <couriousous@mandrake.org> 0.5-1mdk
- 0.5
- Remove vpnc require
- Update description
- Fix menu entry

* Wed Jun 30 2004 Nick Brown <nickbroon@blueyonder.co.uk> 0.3-1mdk
- First Mandrake release

