%define gmyth_upnp_version 0.7.1

Summary: MythTV remote access libraries
Summary(zh_CN.UTF-8): MythTV 远程访问库
Name: gmyth
Version: 0.7.1
Release: 21%{?dist}
License: LGPLv2+
Group: System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL: http://gmyth.sf.net

Source0: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Upstream is bad at pushing stuff to the sourceforge download
# Source1: http://downloads.sourceforge.net/%{name}/gmyth-upnp_%{gmyth_upnp_version}.tar.gz
Source1: http://ftp.debian.org/debian/pool/main/g/gmyth-upnp/gmyth-upnp_%{gmyth_upnp_version}.orig.tar.gz
Patch1: gmyth-remove-debug.patch
Patch2: gmyth-upnp-remove-warning.patch
Patch3: gmyth-upnp-0.7.1-fix-dso-linkage.patch
Patch4: gmyth-0.7.1-curlheader.patch

BuildRequires: mysql-devel curl-devel libxml2-devel glib2-devel libupnp-devel

%description
GMyth is a library used by applications to access content provided by the
MythTV set-top box framework, such as Live TV broadcasts, TV recordings, or
TV listings.

The package also includes GMyth-UPNP, used to discover MythTV servers using UPNP.

%description -l zh_CN.UTF-8 
MythTV 远程访问库。

%package devel
Summary: Development libraries for MythTV remote access
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires: gmyth = %{version}-%{release}
Requires: pkgconfig glib2-devel mysql-devel curl-devel libupnp-devel

%description devel
gmyth-devel contains development libraries and headers for the GMyth and
GMyth-UPNP libraries.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q
%patch1 -p0 -b .debug
tar xvzf %{SOURCE1}
pushd gmyth-upnp-%{gmyth_upnp_version}
%patch2 -p0 -b .warning
%patch3 -p1 -b .dso
popd
%patch4 -p1 -b .curlheader

chmod a-x gmyth/*.[ch]

%build
%configure
make %{?_smp_mflags}

pushd gmyth-upnp-%{gmyth_upnp_version}
CFLAGS=-I`pwd`/../ PKG_CONFIG_PATH=`pwd`/.. %configure
make %{?_smp_mflags} LDFLAGS=-L`pwd`/../gmyth/.libs/
popd

%install
make install DESTDIR=$RPM_BUILD_ROOT
pushd gmyth-upnp-%{gmyth_upnp_version}
make install DESTDIR=$RPM_BUILD_ROOT
popd
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.a
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%doc AUTHORS COPYING
%{_bindir}/*
%{_libdir}/libgmyth.so.*
%{_libdir}/libgmythupnp.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/gmyth
%dir %{_includedir}/gmyth-upnp
%{_includedir}/gmyth-upnp/gmyth_upnp.h
%{_libdir}/libgmyth.so
%{_libdir}/libgmythupnp.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 0.7.1-20
- 为 Magic 3.0 重建

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Feb 26 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.7.1-18
- Fix FTBFS for F-17 mass rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 11 2011 Karsten Hopp <karsten@redhat.com> 0.7.1-16
- bump and rebuild to link with latest libupnp on ppc, too
- don't include curl/types.h, it was empty anyway and got removed from the latest curl

* Tue May 31 2011 Adam Jackson <ajax@redhat.com> 0.7.1-15
- Rebuild for new libupnp

* Fri Mar 25 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.7.1-14
- Fix dso linkage issue (FTBFS bug 564741)

* Wed Mar 23 2011 Dan Horák <dan@danny.cz> - 0.7.1-13.1
- rebuilt for mysql 5.5.10 (soname bump in libmysqlclient)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-12.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.7.1-11.1
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-10.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 21 2009 Karsten Hopp <karsten@redhat.com> 0.7.1-9.1
- rebuild with latest mysql on s390x

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 23 2009 - Bastien Nocera <bnocera@redhat.com> - 0.7.1-8
- Rebuild for new MySQL libraries

* Mon Sep 01 2008 - Bastien Nocera <bnocera@redhat.com> - 0.7.1-7
- Remove extraneous debug and warnings

* Fri Aug 29 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 0.7.1-6
- Include /usr/include/gmyth-upnp directory

* Fri May 23 2008 - Bastien Nocera <bnocera@redhat.com> - 0.7.1-5
- Update gmyth-upnp to 0.7.1

* Sun May 18 2008 - Bastien Nocera <bnocera@redhat.com> - 0.7.1-4
- Fix the gmyth-upnp pkgconfig file

* Sun May 18 2008 - Bastien Nocera <bnocera@redhat.com> - 0.7.1-3
- Add gmyth-upnp to the package

* Mon Mar 03 2008 - Bastien Nocera <bnocera@redhat.com> - 0.7.1-2
- Remove our own COPYING file, the upstream reports the right
  license now

* Mon Mar 03 2008 - Bastien Nocera <bnocera@redhat.com> - 0.7.1-1
- Update to 0.7.1

* Mon Feb 04 2008 - Bastien Nocera <bnocera@redhat.com> - 0.7.0-1
- Update to 0.7.0

* Wed Dec 05 2007 - Bastien Nocera <bnocera@redhat.com> - 0.4-6
- Rebuild

* Tue Oct 09 2007 - Bastien Nocera <bnocera@redhat.com> - 0.4-5
- Add patch from upstream to avoid crashing when the port isn't
  defined (and the default doesn't work) (GNOME #483748)

* Fri Sep 21 2007 - Bastien Nocera <bnocera@redhat.com> - 0.4-4
- Add a dist flag to the release

* Sat Sep 08 2007 - Bastien Nocera <bnocera@redhat.com> - 0.4-3
- Fix permissions in installed files
- Fix Source usage for sourceforge
- Use correct license, as per upstream

* Thu Sep 06 2007 - Bastien Nocera <bnocera@redhat.com> - 0.4-2
- Updated with comments from Matthias Clasen

* Fri Aug 31 2007 - Bastien Nocera <bnocera@redhat.com> 0.4-1
- First version

