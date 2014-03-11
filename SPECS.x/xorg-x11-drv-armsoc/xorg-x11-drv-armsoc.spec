# Tarfile created using git
# git clone git://git.linaro.org/arm/xorg/driver/xf86-video-armsoc.git
# git archive --format=tar --prefix=%{name}-%{version}/ %{gittag} | bzip2 > ~/%{name}-%{version}-%{gittag}.tar.bz2

%define gittag 3be1f62
%define tarfile %{name}-%{version}-%{gittag}.tar.bz2
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir %{moduledir}/drivers

Summary:   Xorg X11 armsocdrm driver
Name:      xorg-x11-drv-armsoc
Version:   0.6.0
Release:   0.7.%{gittag}%{?dist}
URL:       http://git.linaro.org/gitweb?p=arm/xorg/driver/xf86-video-armsoc.git
License:   MIT
Group:     User Interface/X Hardware Support

Source0:   %{tarfile}

ExclusiveArch: %{arm}

BuildRequires: kernel-headers
BuildRequires: libdrm-devel
BuildRequires: libudev-devel
BuildRequires: libXext-devel 
BuildRequires: libXrandr-devel 
BuildRequires: libXv-devel
BuildRequires: mesa-libGL-devel
BuildRequires: pixman-devel
BuildRequires: xorg-x11-server-devel
BuildRequires: xorg-x11-util-macros
BuildRequires: autoconf automake libtool
BuildRequires: perl-Carp

Requires:  xorg-x11-server-Xorg

%description 
X.Org X11 armsocdrm driver for ARM MALI GPUs such as the Samsung 
Exynos 4/5 series ARM devices.

%prep
%setup -q

%build
sh autogen.sh --with-drmmode=exynos
%configure --disable-static  --libdir=%{_libdir} --mandir=%{_mandir} --with-drmmode=exynos
make V=1

%install
make install DESTDIR=$RPM_BUILD_ROOT

# FIXME: Remove all libtool archives (*.la) from modules directory.  This
# should be fixed in upstream Makefile.am or whatever.
find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

%files
%doc README COPYING
%{driverdir}/armsoc_drv.so
%{_mandir}/man4/armsoc.4*

%changelog
* Mon Jan 13 2014 Adam Jackson <ajax@redhat.com> - 0.6.0-0.7.3be1f62
- 1.15 ABI rebuild

* Tue Dec 17 2013 Adam Jackson <ajax@redhat.com> - 0.6.0-0.6.3be1f62
- 1.15RC4 ABI rebuild

* Wed Nov 20 2013 Adam Jackson <ajax@redhat.com> - 0.6.0-0.5.3be1f62
- 1.15RC2 ABI rebuild

* Tue Nov 19 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.6.0-0.4.3be1f62
- update to latest git snapshot

* Wed Nov 06 2013 Adam Jackson <ajax@redhat.com> - 0.6.0-0.3.f245da3
- 1.15RC1 ABI rebuild

* Fri Oct 25 2013 Adam Jackson <ajax@redhat.com> - 0.6.0-0.2.f245da3
- ABI rebuild

* Wed Sep 11 2013 Dennis Gilmore <dennis@ausil.us> - 0.6.0-0.1.f245da3
- update to post 0.6.0 snapshot

* Mon Aug 12 2013 Dennis Gilmore <dennis@ausil.us> - 0.5.2-0.4.b4299f8
- update git snapshot

* Sun Jun 02 2013 Dennis Gilmore <dennis@ausil.us> 0.5.2-0.3.40c8ee2
- bump release

* Sun Jun 02 2013 Dennis Gilmore <dennis@ausil.us> 0.5.2-0.2.40c8ee2
- updated git snapshot, set the hwcursor for the one that works on exynos

* Sun Apr 21 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.5.2-0.1-02465b1
- Move to a git snapshot for the time being

* Thu Apr 04 2013 Dennis Gilmore <dennis@ausil.us> - 0.5.1-9
- patch to fix ftbfs bz#948089

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 0.5.1-8
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 0.5.1-7
- ABI rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 0.5.1-5
- ABI rebuild

* Thu Jan 10 2013 Adam Jackson <ajax@redhat.com> - 0.5.1-4
- ABI rebuild

* Sun Nov 25 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.5.1-3
- Review updates

* Sun Nov 25 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.5.1-2
- Update git url

* Sun Nov 25 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.5.1-1
- Initial package
