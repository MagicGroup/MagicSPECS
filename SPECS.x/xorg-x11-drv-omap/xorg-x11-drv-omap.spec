# Tarfile created using git
# git clone git://github.com/robclark/xf86-video-omap.git xf86-video-omap
# git archive --format=tar --prefix=%{name}-%{version}/ %{gittag}-%{version} | bzip2 > ~/%{name}-%{version}.tar.bz2

%define tarfile %{name}-%{version}.tar.bz2
%define gittag xf86-video-omap
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir %{moduledir}/drivers

Summary:   Xorg X11 omapdrm driver
Name:      xorg-x11-drv-omap
Version:   0.4.3
Release:   13%{?dist}
URL:       http://www.x.org
License:   MIT
Group:     User Interface/X Hardware Support

Source0:   %{tarfile}
Patch0:    xorg-omap-fix-pageflip.patch

ExclusiveArch: %{arm}

BuildRequires: kernel-headers >= 2.6.32.3
BuildRequires: pkgconfig(libdrm_omap)
BuildRequires: libudev-devel
BuildRequires: libXext-devel 
BuildRequires: libXrandr-devel 
BuildRequires: libXv-devel
BuildRequires: mesa-libGL-devel >= 6.5-9
BuildRequires: xorg-x11-server-devel >= 1.4.99.1-0.15
BuildRequires: autoconf automake libtool

Requires:  xorg-x11-server-Xorg >= 1.4.99.1

# last version of the xorg-x11-drv-omapfb in arm koji
Obsoletes: xorg-x11-drv-omapfb <= 0.1.1-3.git20110428.fc17
Provides: xorg-x11-drv-omapfb = 0.1.1-3.git20110428.fc17.1

%description 
X.Org X11 omapdrm driver for TI OMAP 3/4/5xxx series ARM devices.

%prep
%setup -q
%patch0 -p1 -b .pageflip

%build
sh autogen.sh
#autoreconf -v --install || exit 1
%configure --disable-static  --libdir=%{_libdir} --mandir=%{_mandir}
make V=1

%install
make install DESTDIR=$RPM_BUILD_ROOT

# FIXME: Remove all libtool archives (*.la) from modules directory.  This
# should be fixed in upstream Makefile.am or whatever.
find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

%files
%doc README COPYING
%{driverdir}/omap_drv.so
%{_mandir}/man4/omap.4*

%changelog
* Mon Jan 13 2014 Adam Jackson <ajax@redhat.com> - 0.4.3-13
- 1.15 ABI rebuild

* Tue Dec 17 2013 Adam Jackson <ajax@redhat.com> - 0.4.3-12
- 1.15RC4 ABI rebuild

* Wed Nov 20 2013 Adam Jackson <ajax@redhat.com> - 0.4.3-11
- 1.15RC2 ABI rebuild

* Wed Nov 06 2013 Adam Jackson <ajax@redhat.com> - 0.4.3-10
- 1.15RC1 ABI rebuild

* Fri Oct 25 2013 Adam Jackson <ajax@redhat.com> - 0.4.3-9
- ABI rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jun  1 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.4.3-7
- Add upstream patch to fix page flip bugs

* Sun Mar 31 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.4.3-6
- Rebuild

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 0.4.3-5
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 0.4.3-4
- ABI rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 0.4.3-2
- ABI rebuild

* Tue Jan 15 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.4.3-1
- Update to the 0.4.3 tagged release

* Thu Jan 10 2013 Adam Jackson <ajax@redhat.com> - 0.4.2-3
- ABI rebuild

* Wed Oct 24 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.4.2-2
- Add patch to fix rotation detection

* Tue Oct 23 2012 Peter Robinson <pbrobinson@fedoraproject.org> 0.4.2-1
- Update to the 0.4.2 tagged release

* Wed Aug 01 2012 Dennis Gilmore <dennis@ausil.us> - 0.4.0-0.1.git201207801
- update to latest git snapshot

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.1-0.2.git20120511
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 11 2012 Dennis Gilmore <dennis@ausil.us> 0.0.1-0.1.git20120511
- initial fedora packaging
