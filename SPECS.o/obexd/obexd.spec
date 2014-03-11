Name:		obexd
Version:	0.43
Release:	3%{?dist}
Summary:	D-Bus service for Obex Client access

Group:		System Environment/Daemons
License:	GPLv2+
Source0:	http://www.kernel.org/pub/linux/bluetooth/obexd-%{version}.tar.gz
Url:		http://www.bluez.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
ExcludeArch:	s390 s390x

BuildRequires:	glib2-devel
BuildRequires:	dbus-devel
BuildRequires:	bluez-libs-devel >= 4.0
BuildRequires:	openobex-devel
BuildRequires:	libical-devel

%description
obexd contains obex-client, a D-Bus service to allow sending files
using the Obex Push protocol, common on mobile phones and
other Bluetooth-equipped devices.

%prep
%setup -q

%build
%configure --disable-server

make %{?_smp_mflags}

chmod -x test/send-files

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README COPYING AUTHORS doc/client-api.txt test/send-files
%{_libexecdir}/obex-client
%{_datadir}/dbus-1/services/obex-client.service

%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.43-3
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.43-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 30 2011 Bastien Nocera <bnocera@redhat.com> 0.43-1
- Update to 0.43

* Tue Aug 02 2011 Bastien Nocera <bnocera@redhat.com> 0.42-1
- Update to 0.42

* Mon Jun 20 2011 Bastien Nocera <bnocera@redhat.com> 0.41-1
- Update to 0.41

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 20 2011 Bastien Nocera <bnocera@redhat.com> 0.40-1
- Update to 0.40

* Thu Jan 13 2011 Bastien Nocera <bnocera@redhat.com> 0.39-1
- Update to 0.39

* Sun Dec 26 2010 Bastien Nocera <bnocera@redhat.com> 0.38-1
- Update to 0.38

* Mon Nov 22 2010 Bastien Nocera <bnocera@redhat.com> 0.37-1
- Update to 0.37

* Fri Nov 05 2010 Bastien Nocera <bnocera@redhat.com> 0.36-1
- Update to 0.36

* Sat Oct 16 2010 Bastien Nocera <bnocera@redhat.com> 0.35-1
- Update to 0.35

* Wed Oct 06 2010 Bastien Nocera <bnocera@redhat.com> 0.34-1
- Update to 0.34

* Fri Sep 10 2010 Bastien Nocera <bnocera@redhat.com> 0.33-1
- Update to 0.33

* Thu Aug 26 2010 Bastien Nocera <bnocera@redhat.com> 0.32-1
- Update to 0.32

* Mon Aug 23 2010 Bastien Nocera <bnocera@redhat.com> 0.31-1
- Update to 0.31

* Thu Aug 05 2010 Bastien Nocera <bnocera@redhat.com> 0.30-1
- Update to 0.30

* Fri Jul 16 2010 Bastien Nocera <bnocera@redhat.com> 0.29-1
- Update to 0.29

* Tue Jun 15 2010 Bastien Nocera <bnocera@redhat.com> 0.28-1
- Update to 0.28

* Mon Jun 07 2010 Bastien Nocera <bnocera@redhat.com> 0.27-1
- Update to 0.27

* Mon May 24 2010 Bastien Nocera <bnocera@redhat.com> 0.26-1
- Update to 0.26

* Sat May 15 2010 Bastien Nocera <bnocera@redhat.com> 0.24-1
- Update to 0.24

* Mon Apr 26 2010 Bastien Nocera <bnocera@redhat.com> 0.23-1
- Update to 0.23

* Mon Apr 12 2010 Bastien Nocera <bnocera@redhat.com> 0.22-2
- Fix bluetooth-sendto not disappearing after transfer

* Mon Mar 15 2010 Bastien Nocera <bnocera@redhat.com> 0.22-1
- Update to 0.22

* Mon Mar 08 2010 Bastien Nocera <bnocera@redhat.com> 0.21-2
- Fix sending corruption (#550538)

* Tue Dec 22 2009 Bastien Nocera <bnocera@redhat.com> 0.21-1
- Update to 0.21

* Wed Dec 09 2009 Bastien Nocera <bnocera@redhat.com> 0.20-1
- Update to 0.20

* Thu Nov 19 2009 Bastien Nocera <bnocera@redhat.com> 0.19-1
- Update to 0.19

* Sat Sep 26 2009 Bastien Nocera <bnocera@redhat.com> 0.18-1
- Update to 0.18

* Thu Sep 10 2009 Karsten Hopp <karsten@redhat.com> 0.17-2
- ExcludeArch s390 s390x where we don't have openobex

* Tue Sep 01 2009 Bastien Nocera <bnocera@redhat.com> 0.17-1
- Update to 0.17

* Mon Aug 17 2009 Bastien Nocera <bnocera@redhat.com> 0.16-1
- Update to 0.16

* Tue Aug 11 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.15-3
- Use bzipped upstream tarball.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 16 2009 Bastien Nocera <bnocera@redhat.com> 0.15-1
- Update to 0.15

* Fri Jul 03 2009 Bastien Nocera <bnocera@redhat.com> 0.14-1
- Update to 0.14

* Mon Jun 08 2009 Bastien Nocera <bnocera@redhat.com> 0.13-1
- Update to 0.13

* Sun May 03 2009 Bastien Nocera <bnocera@redhat.com> 0.12-1
- Update to 0.12

* Sat Apr 25 2009 Bastien Nocera <bnocera@redhat.com> 0.11-1
- Update to 0.11

* Mon Apr 06 2009 - Bastien Nocera <bnocera@redhat.com> - 0.10-1
- Update to 0.10

* Sun Mar 15 2009 - Bastien Nocera <bnocera@redhat.com> - 0.9-1
- Udpate to 0.9

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Nov 20 2008 - Bastien Nocera <bnocera@redhat.com> - 0.8-1
- Update to 0.8

* Mon Nov 17 2008 - Bastien Nocera <bnocera@redhat.com> - 0.7-1
- Update to 0.7

* Fri Oct 17 2008 - Bastien Nocera <bnocera@redhat.com> - 0.6-1
- Update to 0.6

* Mon Oct 06 2008 - Bastien Nocera <bnocera@redhat.com> - 0.5-2
- Fix problems mentioned in the review

* Mon Oct 06 2008 - Bastien Nocera <bnocera@redhat.com> - 0.5-1
- First package

