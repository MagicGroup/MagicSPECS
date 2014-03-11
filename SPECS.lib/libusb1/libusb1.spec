Summary: A library which allows userspace access to USB devices
Name: libusb1
Version: 1.0.9
Release: 0.7.rc1%{?dist}
# This is a git snapshot of what will hopefully soon become 1.0.9, but
# we need this now, to get things in place for:
# http://fedoraproject.org/wiki/Features/UsbNetworkRedirection
# To regenerate do:
# git clone git://git.libusb.org/libusb.git
# cd libusb
# git checkout 1.0.9-rc1
# ./autogen.sh
# make dist
# mv libusb-1.0.8.tar.bz2 libusb-1.0.9-rc1.tar.bz2
Source0: libusb-1.0.9-rc1.tar.bz2
#Source0: http://downloads.sourceforge.net/libusb/libusb-%{version}.tar.bz2
License: LGPLv2+
Group: System Environment/Libraries
URL: http://libusb.wiki.sourceforge.net/Libusb1.0
BuildRequires: doxygen

%description
This package provides a way for applications to access USB devices. Note that
this library is not compatible with the original libusb-0.1 series.

%package devel
Summary: Development files for libusb
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-devel-doc = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains the header files and libraries needed to develop
applications that use libusb1.

%package devel-doc
Summary: Development files for libusb
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}
BuildArch: noarch

%description devel-doc
This package contains documentation needed to develop applications that
use libusb1.

%package static
Summary: Static development files for libusb
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description static
This package contains static libraries to develop applications that use libusb1.

%prep
%setup -q -n libusb-1.0.8

%build
%configure --libdir=%{_libdir}
make CFLAGS="$RPM_OPT_FLAGS"
pushd doc
make docs
popd

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

# Our snapshot reports itself as 1.0.8, change the pkg-config file version to
# 1.0.9 so that configure checks by apps who need the new 1.0.9 succeed
sed -i 's/1\.0\.8/1.0.9/' %{buildroot}%{_libdir}/pkgconfig/libusb-1.0.pc

#mkdir -p %{buildroot}%{_libdir}/pkgconfig
#mv %{buildroot}/%{_lib}/pkgconfig/* %{buildroot}%{_libdir}/pkgconfig/

magic_rpm_clean.sh

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-,root,root)
%doc AUTHORS COPYING README NEWS ChangeLog
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libusb-1.0.pc

%files devel-doc
%defattr(-,root,root)
%doc doc/html examples/*.c

%files static
%defattr(-,root,root)
%{_libdir}/*.a

%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.0.9-0.7.rc1
- 为 Magic 3.0 重建

* Wed Apr 18 2012 Liu Di <liudidi@gmail.com> - 1.0.9-0.6.rc1
- 为 Magic 3.0 重建

* Wed Apr 18 2012 Liu Di <liudidi@gmail.com> - 1.0.9-0.5.rc1
- 为 Magic 3.0 重建

* Thu Jan 12 2012 Liu Di <liudidi@gmail.com> - 1.0.9-0.4.rc1
- 为 Magic 3.0 重建

* Fri Sep 16 2011 Hans de Goede <hdegoede@redhat.com> - 1.0.9-0.3.rc1
- Update to upstream 1.0.9-rc1 release

* Thu Aug 11 2011 Hans de Goede <hdegoede@redhat.com> - 1.0.9-0.2.git212ca37c
- Report version in pkg-config file as 1.0.9

* Thu Jul 14 2011 Hans de Goede <hdegoede@redhat.com> - 1.0.9-0.1.git212ca37c
- Update to a git snapshot which should be pretty close to the final 1.0.9
- Many bugfixes
- Needed for: http://fedoraproject.org/wiki/Features/UsbNetworkRedirection

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 26 2011 Jan Vcelak <jvcelak@redhat.com> 1.0.8-6
- package config file has to be in /usr/lib/pkgconfig

* Tue Jan 25 2011 Jan Vcelak <jvcelak@redhat.com> 1.0.8-5
- move libraries from /usr/lib to /lib (#519716)

* Sun Nov 07 2010 Dan Horák <dan[at]danny.cz> - 1.0.8-4
- drop the ExcludeArch as it's causing too many troubles

* Wed Sep 29 2010 jkeating - 1.0.8-3
- Rebuilt for gcc bug 634757

* Tue Sep 14 2010 Jan Vcelak <jvcelak@redhat.com> 1.0.8-2
- USB access error messages are now handled by standard logging mechanism
  instead of printing to stderr (#628356)

* Mon May 17 2010 Jindrich Novy <jnovy@redhat.com> 1.0.8-1
- update to 1.0.8 (#592901)

* Fri Jan 22 2010 Jindrich Novy <jnovy@redhat.com> 1.0.6-2
- put all doxygen and other docs to separate noarch subpackage to avoid
  multiarch conflicts (#507980)

* Wed Dec 02 2009 Jindrich Novy <jnovy@redhat.com> 1.0.6-1
- update to 1.0.6

* Mon Sep 28 2009 Jindrich Novy <jnovy@redhat.com> 1.0.3-1
- update to 1.0.3

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 15 2009 Jindrich Novy <jnovy@redhat.com> 1.0.2-1
- update to 1.0.2

* Wed May 13 2009 Jindrich Novy <jnovy@redhat.com> 1.0.1-1
- update to 1.0.1

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 15 2008 - Bastien Nocera <bnocera@redhat.com> - 1.0.0-1
- Update to 1.0.0

* Fri Nov 21 2008 - Bastien Nocera <bnocera@redhat.com> - 0.9.4-1
- Update to 0.9.4

* Tue Sep 23 2008 Jindrich Novy <jnovy@redhat.com> 0.9.3-0.1
- update to 0.9.3

* Sun Jul 06 2008 - Bastien Nocera <bnocera@redhat.com> - 0.9.1
- Update to 0.9.1

* Mon May 26 2008 Jindrich Novy <jnovy@redhat.com> 0.9.0-0.4
- update to official beta

* Thu May 23 2008 Jindrich Novy <jnovy@redhat.com> 0.9.0-0.3.gitbef33bb
- update comment on how the tarball was created
- use abbreviated git hash within package name to avoid conflicts
- add to %%description that libusb1 is incompatible with libsub-0.1

* Thu May 22 2008 Jindrich Novy <jnovy@redhat.com> 0.9.0-0.2.gitbef33bb
- add info on how the snapshot tarball was created

* Wed May 21 2008 Jindrich Novy <jnovy@redhat.com> 0.9.0-0.1.gitbef33bb
- use proper version to denote it is a git snapshot

* Thu May 15 2008 Jindrich Novy <jnovy@redhat.com> 0.9.0-0.1
- initial packaging
