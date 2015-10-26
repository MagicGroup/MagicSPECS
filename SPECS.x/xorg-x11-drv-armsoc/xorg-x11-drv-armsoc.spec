%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir       %{moduledir}/drivers
%define gitdate 20150531
%define gitrev .%{gitdate}

%undefine _hardened_build

Summary:   Xorg X11 armsocdrm driver
Summary(zh_CN.UTF-8): Xorg X11 armsocdrm 驱动
Name:      xorg-x11-drv-armsoc
Version:   1.3.0
Release:   4%{?gitrev}%{?dist}
URL:       http://cgit.freedesktop.org/xorg/driver/xf86-video-armsoc
License:   MIT
Group:     User Interface/X Hardware Support
Group(zh_CN.UTF-8): 用户界面/X 硬件支持

Source0:    xf86-video-armsoc-%{gitdate}.tar.bz2
Source2:    make-git-snapshot.sh
Patch1:     stat-inc.patch

ExclusiveArch: %{arm} aarch64

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

Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires videodrv)

%description 
X.Org X11 armsocdrm driver for ARM MALI GPUs such as the Samsung 
Exynos 4/5 series ARM devices.

%description -l zh_CN.UTF-8
ARM MALI GPU 的驱动。

%if 0%{?gitdate}
%define dirsuffix %{gitdate}
%else
%define dirsuffix %{version}
%endif

%prep
%setup -q -n xf86-video-armsoc-%{?gitdate:%{gitdate}}%{!?gitdate:%{dirsuffix}} 
touch AUTHORS
%patch1 -p1

%build
%{?gitdate:autoreconf -v --install}

%configure --disable-static  --libdir=%{_libdir} --mandir=%{_mandir} --with-drmmode=exynos
make %{?_smp_mflags} V=1

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
* Wed Jul 29 2015 Dave Airlie <airlied@redhat.com> - 1.3.0-4.20150531
- 1.15 ABI rebuild

* Tue Jun 23 2015 Adam Jackson <ajax@redhat.com> - 1.3.0-3.20150531
- Undefine _hardened_build

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-2.20150531
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 31 2015 Dennis Gilmore <dennis@ausil.us> - 1.3.0-1.20150531
- update to latest git
- add patch to fix ftbfs for missing includes
- pull source from  https://github.com/endlessm/xf86-video-armsoc

* Mon May 11 2015 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 1.1.0-2.20150212
- Handle pointer as a pointer to make gcc happy.

* Thu Feb 12 2015 Hans de Goede <hdegoede@redhat.com> - 1.1.0-1.20150212
- Update to git snapshot of the day to fix FTBFS
- This also bumps the version we're based on from 0.7.0 + git patches to
  1.1.0 + git patches.

* Wed Feb 11 2015 Hans de Goede <hdegoede@redhat.com> - 0.7.0-7.20140504
- xserver 1.17 ABI rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-6.20140504
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 16 2014 Hans de Goede <hdegoede@redhat.com> - 0.7.0-5.20140504
- xserver 1.15.99.903 ABI rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-4.20140504
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May  6 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.7.0-3.20140504
- Build on aarch64 too

* Sun May 04 2014 Dennis Gilmore <dennis@ausil.us> - 0.7.0-2.20140504
- update git snapshot for ftbfs

* Thu May 01 2014 Dennis Gilmore <dennis@ausil.us> - 0.7.0-1.20140501
- update git snapshot
- add script to make tarball from git
- xserver 1.15.99-20140428 git snapshot ABI rebuild
- sync package to match other x drivers

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
