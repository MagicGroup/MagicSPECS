%define tarball xf86-video-savage
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/drivers

Summary:   Xorg X11 savage video driver
Name:      xorg-x11-drv-savage
Version:   2.3.7
Release:   3%{?dist}
URL:       http://www.x.org
License: MIT
Group:     User Interface/X Hardware Support

Source0:   http://ftp.nara.wide.ad.jp/pub/X11/x.org/individual/driver/%{tarball}-%{version}.tar.bz2
ExcludeArch: s390 s390x %{?rhel:ppc ppc64}

BuildRequires: xorg-x11-server-devel >= 1.10.99.902
BuildRequires: mesa-libGL-devel >= 6.4-4
BuildRequires: libdrm-devel >= 2.0-1
BuildRequires: autoconf automake libtool

Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires videodrv)

%description 
X.Org X11 savage video driver.

%prep
%setup -q -n %{tarball}-%{version}

%build
autoreconf -vif
%configure --disable-static --disable-dri
make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# FIXME: Remove all libtool archives (*.la) from modules directory.  This
# should be fixed in upstream Makefile.am or whatever.
find $RPM_BUILD_ROOT -regex ".*.la$" | xargs rm -f --

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{driverdir}/savage_drv.so
%{_mandir}/man4/savage.4*

%changelog
* Mon Jan 13 2014 Adam Jackson <ajax@redhat.com> - 2.3.7-3
- 1.15 ABI rebuild

* Tue Dec 17 2013 Adam Jackson <ajax@redhat.com> - 2.3.7-2
- 1.15RC4 ABI rebuild

* Thu Dec 05 2013 Adam Jackson <ajax@redhat.com> 2.3.7-1
- savage 2.3.7
- Trim changelog to f19

* Wed Nov 20 2013 Adam Jackson <ajax@redhat.com> - 2.3.6-12
- 1.15RC2 ABI rebuild

* Wed Nov 06 2013 Adam Jackson <ajax@redhat.com> - 2.3.6-11
- 1.15RC1 ABI rebuild

* Fri Oct 25 2013 Adam Jackson <ajax@redhat.com> - 2.3.6-10
- ABI rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Dave Airlie <airlied@redhat.com> 2.3.6-8
- autoreconf for aarch64
