
Name:           accountsservice
Version:	0.6.40
Release:        2%{?dist}
Summary:        D-Bus interfaces for querying and manipulating user account information
Summary(zh_CN.UTF-8): 查询和处理用户账户信息的 D-Bus 接口

Group:          System Environment/Daemons
Group(zh_CN.UTF-8): 系统环境/服务
License:        GPLv3+
URL:            http://www.fedoraproject.org/wiki/Features/UserAccountDialog
#VCS: git:git://git.freedesktop.org/accountsservice
Source0:        http://www.freedesktop.org/software/accountsservice/accountsservice-%{version}.tar.xz

BuildRequires:  glib2-devel
BuildRequires:  dbus-glib-devel
BuildRequires:  polkit-devel
BuildRequires:  intltool
BuildRequires:  systemd-units
BuildRequires:  systemd-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  vala-devel
BuildRequires:  vala-tools

Requires:       polkit
Requires:       shadow-utils

Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%package libs
Summary: Client-side library to talk to accountsservice
Summary(zh_CN.UTF-8): 与 accountsservice 通信的客户端库
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: %{name} = %{version}-%{release}

%description libs
The accountsservice-libs package contains a library that can
be used by applications that want to interact with the accountsservice
daemon.


%package devel
Summary: Development files for accountsservice-libs
Group: Development/Libraries
Requires: %{name}-libs = %{version}-%{release}

%description devel
The accountsservice-devel package contains headers and other
files needed to build applications that use accountsservice-libs.


%description
The accountsservice project provides a set of D-Bus interfaces for
querying and manipulating user account information and an implementation
of these interfaces, based on the useradd, usermod and userdel commands.


%prep
%setup -q

%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/*.a
magic_rpm_clean.sh
%find_lang accounts-service


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%post
%systemd_post accounts-daemon.service

%preun
%systemd_preun accounts-daemon.service

%postun
%systemd_postun accounts-daemon.service

%files -f accounts-service.lang
%defattr(-,root,root,-)
%doc COPYING README AUTHORS
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.Accounts.conf
%{_libexecdir}/accounts-daemon
%{_datadir}/dbus-1/interfaces/org.freedesktop.Accounts.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.Accounts.User.xml
%{_datadir}/dbus-1/system-services/org.freedesktop.Accounts.service
%{_datadir}/polkit-1/actions/org.freedesktop.accounts.policy
%dir %{_localstatedir}/lib/AccountsService/
%dir %{_localstatedir}/lib/AccountsService/users
%dir %{_localstatedir}/lib/AccountsService/icons
%{_unitdir}/accounts-daemon.service

%files libs
%{_libdir}/libaccountsservice.so.*
%{_libdir}/girepository-1.0/AccountsService-1.0.typelib

%files devel
%{_includedir}/accountsservice-1.0
%{_libdir}/libaccountsservice.so
%{_libdir}/pkgconfig/accountsservice.pc
%{_datadir}/gir-1.0/AccountsService-1.0.gir
#%{_datadir}/vala/vapi/*
%dir %{_datadir}/gtk-doc/html/libaccountsservice
%{_datadir}/gtk-doc/html/libaccountsservice/*

%changelog
* Wed Oct 28 2015 Liu Di <liudidi@gmail.com> - 0.6.40-2
- 更新到 0.6.40

* Tue Apr 16 2013 Matthias Clasen <mclasen@redhat.com> - 0.6.31-1
- Update to 0.6.31

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 16 2013 Richard Hughes <rhughes@redhat.com> - 0.6.30-1
- Update to 0.6.30

* Fri Nov 16 2012 Matthias Clasen <mclasen@redhat.com> - 0.6.26-1
- Update to 0.6.26

* Tue Oct  2 2012 Matthias Clasen <mclasen@redhat.com> - 0.6.25-2
- Update to 0.6.25
- Use systemd scriptlets (#856649)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jul 14 2012 Ville Skyttä <ville.skytta@iki.fi> - 0.6.22-2
- Add ldconfig scriptlets to -libs.

* Thu Jun 28 2012 Ray Strode <rstrode@redhat.com> 0.6.22-1
- Update to 0.6.22.
- Fixes CVE-2012-2737 - local file disclosure
  Related:  #832532

* Thu May 30 2012 Matthias Clasen <mclasen@redhatcom> 0.6.21-1
- Update to 0.6.21

* Fri May 04 2012 Ray Strode <rstrode@redhat.com> 0.6.20-1
- Update to 0.6.20. Should fix user list.
  Related: #814690

* Thu May 03 2012 Ray Strode <rstrode@redhat.com> 0.6.19-1
- Update to 0.6.19
  Allows user deletion of logged in users
  Related: #814690

* Wed Apr 11 2012 Matthias Clasen <mclsaen@redhat.com> - 0.6.18-1
- Update to 0.6.18

* Tue Mar 27 2012 Ray Strode <rstrode@redhat.com> 0.6.17-1
- Update to latest release

* Sun Mar  4 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.6.15-4
- Fix unitdir with usrmove

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 29 2011 Matthias Clasen <mclasen@redhat.com> 0.6.15-2
- Make resetting user icons work
- Update to 0.6.15
- Fixes session chooser at login screen when logged into vt

* Wed Sep 21 2011 Ray Strode <rstrode@redhat.com> 0.6.14-2
- Fix wtmp loading so users coming from the network are
  remembered in the user list in subsequent boots

* Wed Sep 21 2011 Ray Strode <rstrode@redhat.com> 0.6.14-1
- Update to 0.6.14

* Sun Sep  4 2011 Matthias Clasen <mclasen@redhat.com> - 0.6.13-3
- Fix fast user switching

* Mon Aug 15 2011 Kalev Lember <kalevlember@gmail.com> - 0.6.13-2
- Rebuilt for rpm bug #728707

* Tue Jul 19 2011 Matthias Clasen <mclasen@redhat.com> - 0.6.13-1
- Update to 0.6.13
- Drop ConsoleKit dependency

* Mon Jun 06 2011 Ray Strode <rstrode@redhat.com> 0.6.12-1
- Update to latest release

* Wed May 18 2011 Matthias Clasen <mclasen@redhat.com> 0.6.11-1
- Update to 0.6.11

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb 02 2011 Ray Strode <rstrode@redhat.com> 0.6.3-1
- Update to 0.6.3

* Thu Jan 27 2011 Matthias Clasen <mclasen@redhat.com> 0.6.2-1
- Update to 0.6.2

* Wed Jul 21 2010 Matthias Clasen <mclasen@redhat.com> 0.6.1-1
- Update to 0.6.1
- Install systemd unit file

* Mon Apr  5 2010 Matthias Clasen <mclasen@redhat.com> 0.6-2
- Always emit changed signal on icon change

* Tue Mar 30 2010 Matthias Clasen <mclasen@redhat.com> 0.6-1
- Update to 0.6

* Mon Mar 22 2010 Matthias Clasen <mclasen@redhat.com> 0.5-1
- Update to 0.5

* Mon Feb 22 2010 Bastien Nocera <bnocera@redhat.com> 0.4-3
- Fix directory ownership

* Mon Feb 22 2010 Bastien Nocera <bnocera@redhat.com> 0.4-2
- Add missing directories to the filelist

* Fri Jan 29 2010 Matthias Clasen <mclasen@redhat.com> 0.4-1
- Initial packaging, based on work by Richard Hughes
