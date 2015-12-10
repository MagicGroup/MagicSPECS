Name:          gypsy
Version:       0.9
Release:       5%{?dist}
Summary:       A GPS multiplexing daemon

Group:         System Environment/Libraries
# See LICENSE file for details
License:       LGPLv2 and GPLv2
URL:           http://gypsy.freedesktop.org/
Source0:       http://gypsy.freedesktop.org/releases/%{name}-%{version}.tar.gz
Patch0:        gypsy-0.8-unusedvar.patch
Patch1:        gypsy-0.9-gtypeinit.patch

BuildRequires: bluez-libs-devel
BuildRequires: dbus-devel
BuildRequires: dbus-glib-devel
BuildRequires: glib2-devel
BuildRequires: gtk-doc
BuildRequires: libgudev1-devel
BuildRequires: libxslt

Requires: dbus

%description
Gypsy is a GPS multiplexing daemon which allows multiple clients to 
access GPS data from multiple GPS sources concurrently. 

%package devel
Summary: Development package for gypsy
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: dbus-glib-devel
Requires: pkgconfig

%description devel
Header files for development with gypsy.

%package docs
Summary: Documentation files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description docs
This package contains developer documentation for %{name}.

%prep
%setup -q
%patch0 -p1 -b .unusedvar
%patch1 -p1 -b .gtypeinit

%build
%configure --disable-static
find . -name Makefile|xargs sed -i 's!-Werror!!g'
find . -name Makefile|xargs sed -i 's!=format-security!!g'
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/libgypsy.la

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING COPYING.lib LICENSE
%config(noreplace) %{_sysconfdir}/gypsy.conf
%{_sysconfdir}/dbus-1/system.d/Gypsy.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.Gypsy.service
%{_libexecdir}/gypsy-daemon
%{_libdir}/libgypsy.so.0
%{_libdir}/libgypsy.so.0.0.0

%files devel
%{_libdir}/pkgconfig/gypsy.pc
%{_includedir}/gypsy
%{_libdir}/libgypsy.so

%files docs
%doc %{_datadir}/gtk-doc/html/gypsy

%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun May 19 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.9-1
- New upstream 0.9 release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 16 2011 Peter Robinson <pbrobinson@fedoraproject.org> 0.8-5
- Bump build

* Sat Jun 11 2011 Peter Robinson <pbrobinson@fedoraproject.org> 0.8-4
- Cleanup spec, drop unncessary gtk-doc dep - fixes RHBZ 707562

* Sun Mar 13 2011 Karsten Hopp <karsten@redhat.com> 0.8-3
- fix build problem with latest gcc (unused variable)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep 7 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.8-2
- Update to new source URL

* Wed Jun 9 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.8-1
- New upstream 0.8 release

* Thu Aug 06 2009 Bastien Nocera <bnocera@redhat.com> 0.7-1
- Update to 0.7

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 19 2009 Bastien Nocera <bnocera@redhat.com> 0.6-9
- Gypsy is supposed to run as a system service, as root

* Wed Mar  4 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.6-8
- Move docs to noarch, some spec file updates

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 18 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.6-6
- Add gtk-doc build req

* Sat Nov 22 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.6-5
- Rebuild

* Thu Sep 11 2008 - Bastien Nocera <bnocera@redhat.com> 0.6-4
- Rebuild

* Thu May 15 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.6-3
- Further spec file cleanups

* Mon Apr 28 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.6-2
- Some spec file cleanups

* Sat Apr 26 2008 Peter Robinson <pbrobinson@fedoraproject.org> 0.6-1
- Initial package
