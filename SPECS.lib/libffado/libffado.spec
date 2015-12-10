Summary:        Free firewire audio driver library
Summary(zh_CN.UTF-8): 自由的火线音频驱动库
Name:           libffado
Version: 2.2.1
Release:        3%{?dist}
# src/libutil/float_cast.h is LGPLv2+.
# The rest is (GPLv2 or GPLv3)
License:        LGPLv2+ and (GPLv2 or GPLv3)
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL:            http://www.ffado.org/
Source0:        http://www.ffado.org/files/%{name}-%{version}.tgz
# The trunk is tarballed as follows:
# bash libffado-snapshot.sh 2088
# The fetch script
Source9:        libffado-snapshot.sh
# We want the documentation for the library API only, not for the entire source:
# http://subversion.ffado.org/ticket/293
Patch0:         libffado-api-doc-only.patch
BuildRequires:  alsa-lib-devel
BuildRequires:  dbus-c++-devel
BuildRequires:  dbus-devel
BuildRequires:  dbus-python
BuildRequires:  desktop-file-utils
BuildRequires:  doxygen
BuildRequires:  glibmm24-devel
BuildRequires:  graphviz
BuildRequires:  libconfig-devel
BuildRequires:  libiec61883-devel
BuildRequires:  libraw1394-devel
BuildRequires:  libxml++-devel
BuildRequires:  pkgconfig
BuildRequires:  PyQt4-devel
BuildRequires:  python2-devel
BuildRequires:  scons
BuildRequires:  subversion
ExcludeArch:    s390 s390x
Requires:       udev

%description
The FFADO project aims to provide a generic, open-source solution for the
support of FireWire based audio devices for the Linux platform. It is the
successor of the FreeBoB project.

%description -l zh_CN.UTF-8
自由的火线音频驱动库。

%package devel
Summary:        Free firewire audio driver library development headers
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        GPLv2 or GPLv3
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files needed to build applications against libffado.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package -n ffado
Summary:        Free firewire audio driver library applications and utilities
Summary(zh_CN.UTF-8): %{name} 库的应用程序和工具
Group:          Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
# support/tools/* is GPLv3
# Some files in support/mixer-qt4/ffado are GPLv3+
# The rest is GPLv2 or GPLv3
License:        GPLv3 and GPLv3+ and (GPLv2 or GPLv3)
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       dbus
Requires:       dbus-python
Requires:       PyQt4

%description -n ffado
Applications and utilities for use with libffado.

%description -n ffado -l zh_CN.UTF-8
%{name} 库的应用程序和工具。

%prep
%setup -q
%patch0 -p1 -b .api.doc.only

# We don't want to install all tests
sed -i '/Install/d' tests/{,*/}SConscript

%build
scons %{?_smp_mflags} \
      COMPILE_FLAGS="%{optflags} -ffast-math" \
      PREFIX=%{_prefix} \
      LIBDIR=%{_libdir} \
      MANDIR=%{_mandir} \
      UDEVDIR=%{_prefix}/lib/udev/rules.d/ \
      BUILD_TESTS=1

%install
scons DESTDIR=%{buildroot} install

# We need to install the xdg stuff manually
mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install --dir %{buildroot}%{_datadir}/applications \
   --add-category="Settings" \
   support/xdg/ffado.org-ffadomixer.desktop
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/64x64/apps
ln -s ../../../../libffado/icons/hi64-apps-ffado.png \
    %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/ffado.png

# Install ffado-test RHBZ#805940
install -m 755 tests/ffado-test %{buildroot}%{_bindir}
magic_rpm_clean.sh

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post -n ffado
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun -n ffado
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans -n ffado
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%doc AUTHORS ChangeLog LICENSE.* README
%{_libdir}/libffado.so.*
%dir %{_datadir}/libffado/
%{_datadir}/libffado/configuration
%{_prefix}/lib/udev/rules.d/*

%files devel
%doc doc/reference/html/
%{_includedir}/libffado/
%{_libdir}/pkgconfig/libffado.pc
%{_libdir}/libffado.so

%files -n ffado
%{_mandir}/man1/ffado-*.1*
%{_bindir}/*
%{_datadir}/libffado/*.xml
%{_datadir}/libffado/python/
%{_datadir}/libffado/icons/
%{_datadir}/dbus-1/services/org.ffado.Control.service
%{_datadir}/applications/ffado.org-ffadomixer.desktop
%{_datadir}/icons/hicolor/64x64/apps/ffado.png
%{python_sitelib}/ffado/


%changelog
* Mon Nov 09 2015 Liu Di <liudidi@gmail.com> - 2.2.1-3
- 为 Magic 3.0 重建

* Sat Oct 31 2015 Liu Di <liudidi@gmail.com> - 2.2.1-2
- 为 Magic 3.0 重建

* Wed Jul 16 2014 Liu Di <liudidi@gmail.com> - 2.2.1-1
- 更新到 2.2.1

* Thu Sep 20 2012 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 2.1.0-1
- Update to 2.1.0.
- Drop upstreamed & old patches, README.Fedora file.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-0.10.20120325.svn2088
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 2.1.0-0.9.20120325.svn2088
- Fix multilib confict RHBZ#831405
- Fix DSO linking #ticket 355

* Sun Mar 25 2012 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 2.1.0-0.8.20120325.svn2088
- Update to svn2088.
- Drop upstreamed gcc-4.7 patch.

* Thu Mar 22 2012 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 2.1.0-0.7.20111030.svn2000
- Include the ffado-test executable RHBZ#805940
- Fix .desktop file warning

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-0.6.20111030.svn2000
- Rebuilt for c++ ABI breakage

* Tue Jan 10 2012 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 2.1.0-0.5.20111030.svn2000
- gcc-4.7 compile fix

* Sun Oct 30 2011 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 2.1.0-0.4.20111030.svn2000
- Update to svn2000.
- Drop the gold linker patch. The issue is properly solved upstream. See upstream tracker #293

* Mon Apr 26 2011 Brendan Jones <brendan.jones.it@gmail.com> - 2.1.0-0.3.20110426.svn1983
- Update to svn1983
- Clean up redundant patches
- Patch to rebuild using gold linker. Fixes RHBZ#684392

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-0.2.20101015.svn1913
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Oct 15 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 2.1.0-0.1.20101015.svn1913
- Update to svn1913. Fixes RHBZ#635315
- Drop upstreamed patches

* Thu Aug 26 2010 Dan Horák <dan[at]danny.cz> - 2.0.1-5.20100706.svn1864
- no Firewire on s390(x)

* Thu Jul 29 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 2.0.1-4.20100706.svn1864
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jul 14 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 2.0.1-3.20100706.svn1864
- Remove ENABLE_ALL
- Improve the libffado-dont-use-bundled-libs.patch
- Drop BR: expat-devel libavc1394-devel
- Move configuration file to the library package
- Minor enhancement in the .desktop file
- Add links to upstream tickets for patches
- Add -ffast-math to the compiler flags
- Add patch to compile against libconfig-1.4.5

* Tue Jul 13 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 2.0.1-2.20100706.svn1864
- Add ENABLE_ALL flag to support more devices
- Don't bundle tests
- Include some preliminary documentation for the tools until the manpages arrive
- Patch out bundled libraries. Also fixes some rpmlints
- Improve the instructions how to create the tarball

* Wed Jul 07 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 2.0.1-1.20100706.svn1864
- Update to trunk, post 2.0.1.

* Sat Jun 05 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 2.0.0-1.20100605.svn1845
- Update to trunk, post 2.0.0.

* Mon May 18 2009 Jarod Wilson <jarod@redhat.com> - 2.0-0.4.rc2
- Update to 2.0.0-rc2

* Thu Nov 06 2008 Jarod Wilson <jarod@redhat.com> - 2.0-0.3.beta7
- Update to beta7
- Put arch-dependent helper/test binaries in libexecdir instead of datadir

* Sun Aug 10 2008 Jarod Wilson <jwilson@redhat.com> - 2.0-0.2.beta6
- Review clean-ups (#456353)

* Tue Jul 22 2008 Jarod Wilson <jwilson@redhat.com> - 2.0-0.1.beta6
- Initial Fedora build of libffado
