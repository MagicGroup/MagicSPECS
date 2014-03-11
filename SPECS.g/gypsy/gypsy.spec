Name:          gypsy
Version:       0.8
Release:       4%{?dist}
Summary:       A GPS multiplexing daemon

Group:         System Environment/Libraries
# See LICENSE file for details
License:       LGPLv2 and GPLv2
URL:           http://gypsy.freedesktop.org/
Source0:       http://gypsy.freedesktop.org/releases/%{name}-%{version}.tar.gz

BuildRequires: bluez-libs-devel
BuildRequires: dbus-devel
BuildRequires: dbus-glib-devel
BuildRequires: glib2-devel
BuildRequires: gtk-doc
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
Requires: gtk-doc
BuildArch: noarch

%description docs
This package contains developer documentation for %{name}.

%prep
%setup -q

%build
%configure --disable-static
#gcc 4.6
find . -name Makefile|xargs sed -i 's/\-Werror//g'
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/libgypsy.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING COPYING.lib LICENSE
%{_sysconfdir}/dbus-1/system.d/Gypsy.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.Gypsy.service
%{_libexecdir}/gypsy-daemon
%{_libdir}/libgypsy.so.0
%{_libdir}/libgypsy.so.0.0.0

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/gypsy.pc
%{_includedir}/gypsy
%{_libdir}/libgypsy.so

%files docs
%defattr(-,root,root,-)
%doc %{_datadir}/gtk-doc/html/gypsy

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 0.8-4
- 为 Magic 3.0 重建

* Mon Dec 12 2011 Liu Di <liudidi@gmail.com> - 0.8-3
- 为 Magic 3.0 重建

* Tue Sep 7 2010 Peter Robinson <pbrobinson@gmail.com> 0.8-2
- Update to new source URL

* Wed Jun 9 2010 Peter Robinson <pbrobinson@gmail.com> 0.8-1
- New upstream 0.8 release

* Thu Aug 06 2009 Bastien Nocera <bnocera@redhat.com> 0.7-1
- Update to 0.7

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 19 2009 Bastien Nocera <bnocera@redhat.com> 0.6-9
- Gypsy is supposed to run as a system service, as root

* Wed Mar  4 2009 Peter Robinson <pbrobinson@gmail.com> 0.6-8
- Move docs to noarch, some spec file updates

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 18 2008 Peter Robinson <pbrobinson@gmail.com> 0.6-6
- Add gtk-doc build req

* Sat Nov 22 2008 Peter Robinson <pbrobinson@gmail.com> 0.6-5
- Rebuild

* Thu Sep 11 2008 - Bastien Nocera <bnocera@redhat.com> 0.6-4
- Rebuild

* Mon May 15 2008 Peter Robinson <pbrobinson@gmail.com> 0.6-3
- Further spec file cleanups

* Mon Apr 28 2008 Peter Robinson <pbrobinson@gmail.com> 0.6-2
- Some spec file cleanups

* Sat Apr 26 2008 Peter Robinson <pbrobinson@gmail.com> 0.6-1
- Initial package
