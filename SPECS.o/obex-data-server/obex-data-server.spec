Name:		obex-data-server
Version:	0.4.6
Release:	3%{?dist}
Epoch:		1
Summary:	D-Bus service for Obex access

Group:		System Environment/Daemons
License:	GPLv2+
Source0:	http://tadas.dailyda.com/software/%{name}-%{version}.tar.gz
Url:		http://tadas.dailyda.com/blog
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
ExcludeArch: s390 s390x

BuildRequires:	dbus-glib-devel
BuildRequires:	bluez-libs-devel
BuildRequires:	openobex-devel
BuildRequires:	gtk2-devel
BuildRequires:	libusb-devel
BuildRequires:	libtool

%description
obex-data-server is a D-Bus service to allow sending and receiving files
using the ObexFTP and Obex Push protocols, common on mobile phones and
other Bluetooth-equipped devices.

%prep
%setup -q

%build
%configure --enable-bip=gdk-pixbuf

make %{?_smp_mflags}

cat << EOF > README
Bug tracking system is at:
http://bugs.muiline.com/view_all_bug_page.php

Web page is at:
http://tadas.dailyda.com/blog/

SVN tree:
svn://svn.muiline.com/obex-data-server/trunk/

SVN browsing:
http://svn.muiline.com/cgi-bin/viewvc.cgi/obex-data-server/trunk/

EOF

%install
rm -rf $RPM_BUILD_ROOT
chmod a-x test/*.py
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README COPYING dbus-api.txt test/ods-dbus-test.c test/ods-server-test.py test/ods-session-test.py
%{_bindir}/obex-data-server
%{_sysconfdir}/obex-data-server/
%{_datadir}/dbus-1/services/obex-data-server.service
%{_mandir}/man1/obex-data-server.1.gz

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1:0.4.6-3
- 为 Magic 3.0 重建

* Thu Jan 19 2012 Liu Di <liudidi@gmail.com> - 1:0.4.6-2
- 为 Magic 3.0 重建

* Thu Jun 09 2011 Bastien Nocera <bnocera@redhat.com> 0.4.6-1
- Update to 0.4.6

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 21 2009 Bastien Nocera <bnocera@redhat.com> 0.4.5-1
- Update to 0.4.5

* Thu Sep 10 2009 Karsten Hopp <karsten@redhat.com> 0.4.3-4
- ExcludeArch s390 s390x where we don't have openobex

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 08 2009 - Bastien Nocera <bnocera@redhat.com> - 0.4.3-1
- Update to 0.4.3

* Sat Nov 01 2008 - Bastien Nocera <bnocera@redhat.com> - 0.4.2-1
- Update to 0.4.2

* Sun Oct 26 2008 - Bastien Nocera <bnocera@redhat.com> - 0.4.1-1
- Update to 0.4.1

* Fri Oct 17 2008 - Bastien Nocera <bnocera@redhat.com> - 0.4-1
- Update to 0.4

* Mon Oct 06 2008 - Bastien Nocera <bnocera@redhat.com> - 0.3.99-2
- Update to rev 1998
- Use gdk-pixbuf instead of ImageMagick for BIP support

* Mon Sep 29 2008 - Bastien Nocera <bnocera@redhat.com> - 0.3.99-1
- Update to rev 1977

* Mon Sep 15 2008 - Bastien Nocera <bnocera@redhat.com> - 0.3.4-8
- Add ImageMagic BR

* Mon Sep 15 2008 - Bastien Nocera <bnocera@redhat.com> - 0.3.4-7
- Add missing patch

* Mon Sep 15 2008 - Bastien Nocera <bnocera@redhat.com> - 0.3.4-6
- Update to latest SVN trunk, with BlueZ 4 patch

* Fri Sep 12 2008 - Bastien Nocera <bnocera@redhat.com> - 0.3.4-5
- Another BlueZ 4.x patch update

* Fri Sep 12 2008 - Bastien Nocera <bnocera@redhat.com> - 0.3.4-4
- Update bluez 4.x patch for the latest D-Bus API

* Thu Sep 11 2008 - Bastien Nocera <bnocera@redhat.com> - 0.3.4-3
- Rebuild with BlueZ 4.x patch

* Thu Sep 11 2008 Matthias Clasen <mclasen@redhat.com> - 0.3.4-2
- Rebuild

* Sat Aug 23 2008 - Bastien Nocera <bnocera@redhat.com> - 0.3.4-1
- Update to 0.3.4
- Fixes a problem accessing Nokia phones (#456541)

* Tue Apr 01 2008 - Bastien Nocera <bnocera@redhat.com> - 0.3.1-1
- Update to 0.3.1
- Fixes a number of crashers

* Thu Feb 21 2008 - Bastien Nocera <bnocera@redhat.com> - 0.3-1
- Update to 0.3

* Wed Feb 13 2008 - Bastien Nocera <bnocera@redhat.com> - 0.2-1
- Update to 0.2
- Remove system-wide service file

* Thu Feb 07 2008 - Bastien Nocera <bnocera@redhat.com> - 0.1-1
- Update to release 0.1
- Up Epoch as version numbering sucks

* Mon Feb 04 2008 - Bastien Nocera <bnocera@redhat.com> - 0.01-6.04022008
- Update from SVN

* Sun Jan 20 2008 - Bastien Nocera <bnocera@redhat.com> - 0.01-5.16012007
- Fix rpmlint issues

* Fri Jan 18 2008 - Bastien Nocera <bnocera@redhat.com> - 0.01-4.16012007
- Add BR on libtool

* Thu Jan 17 2008 - Bastien Nocera <bnocera@redhat.com> - 0.01-3.16012007
- Remove exec bits on example apps

* Wed Jan 16 2008 - Bastien Nocera <bnocera@redhat.com> - 0.01-2.16012007
- Add COPYING, and add some data to the README

* Wed Jan 16 2008 - Bastien Nocera <bnocera@redhat.com> - 0.01-1.16012007
- First package

