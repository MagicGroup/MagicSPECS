%global         releasedate 20150615
Name:           hdhomerun
Version:        0.0.%{releasedate}
Release:        0.%{?dist}
Summary:        Silicon Dust HDHomeRun configuration utility
Summary(zh_CN.UTF-8): HDHomeRun 配置程序 

Group:          Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
License:        LGPLv3 and GPLv3
URL:            http://www.silicondust.com/
Source0:        http://download.silicondust.com/hdhomerun/libhdhomerun_%{releasedate}.tgz
Source1:        http://download.silicondust.com/hdhomerun/hdhomerun_config_gui_%{releasedate}.tgz
Source2:	hdhomerun_config_gui.desktop
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  gtk2-devel
BuildRequires:  libicns-utils
BuildRequires:  desktop-file-utils
Requires:       gtk2

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%description
The configuration and firmware upgrade utility for Silicon Dust's
networked HDTV dual-tuner HDHomeRun device.

%description -l zh_CN.UTF-8
HDHomeRun 配置程序。

%package devel
Summary: Developer tools for the hdhomerun library
Summary(zh_CN.UTF-8): %{name} 的开发包
Group: Development
Group(zh_CN.UTF-8): 开发/库
Requires: hdhomerun = %{version}-%{release}

%description devel
The hdhumerun-devel package provides developer tools for the hdhomerun library.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%prep
%setup -q -c -a 1
# Fix up linefeeds, drop execute bit and don't strip binaries
%{__sed} -i 's/\r//' libhdhomerun/*
%{__chmod} -x libhdhomerun/*
%{__sed} -i -e '/$(STRIP).*/d' -e 's/C\(PP\)\?FLAGS .=/C\1FLAGS ?=/' libhdhomerun/Makefile

# Convert files to utf8
for f in libhdhomerun/*; do
  /usr/bin/iconv -f iso-8859-1 -t utf-8 --output $f.new $f && mv $f.new $f
done

%build
cd hdhomerun_config_gui
%configure
make 
cd ..
cat << __EOF__ > README.firmware
The HDHomeRun Firmwares are not redistributable, but the latest versions of
both the US ATSC and European DVB-T firmwares can always be obtained from
the Silicon Dust web site:

http://www.silicondust.com/downloads/linux

__EOF__

pushd hdhomerun_config_gui/OSX
icns2png -x hdhr.icns
popd

%install
rm -rf $RPM_BUILD_ROOT
make -C hdhomerun_config_gui install DESTDIR=$RPM_BUILD_ROOT
install -m0755 libhdhomerun/hdhomerun_config $RPM_BUILD_ROOT%{_bindir}/
mkdir include
cp -a libhdhomerun/*.h include
sed -r 's|(^#include +["])(.*)(["] *$)|#include <hdhomerun/\2>|' \
    libhdhomerun/hdhomerun.h > include/hdhomerun.h
mkdir -p $RPM_BUILD_ROOT%{_includedir}/hdhomerun
install -m0755 include/*.h $RPM_BUILD_ROOT%{_includedir}/hdhomerun/
desktop-file-install --dir=${RPM_BUILD_ROOT}%{_datadir}/applications %{SOURCE2}

for size in 16x16 32x32 128x128 256x256 512x512
do
    mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${size}
    install -m0755 hdhomerun_config_gui/OSX/hdhr_${size}x32.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${size}/hdhr.png
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc libhdhomerun/lgpl.txt libhdhomerun/README hdhomerun_config_gui/COPYING README.firmware
# lib and cli are LGPLv3
%{_libdir}/libhdhomerun.so
%{_bindir}/hdhomerun_config
# gui is GPLv3
%{_bindir}/hdhomerun_config_gui
%{_datadir}/applications/hdhomerun_config_gui.desktop
%{_datadir}/icons/hicolor/*/hdhr.png

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/hdhomerun
%{_includedir}/hdhomerun/*.h

%changelog
* Sat Jun 28 2015 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0-0.28.20150615
- Update to 20150615

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0-0.27.20140604
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.0-0.26.20140604
- Rebuilt for GCC 5 C++11 ABI change

* Tue Sep 23 2014 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0-0.26.20140604
- Remove duplicate description section

* Tue Sep 23 2014 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0-0.25.20140604
- Extract icons from OSX icon set
- Add desktop file for GUI

* Tue Sep 23 2014 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.0-0.24.20140604
- Update to 20140604

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0-0.23.20130328
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0-0.22.20130328
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0-0.21.20130328
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 07 2013 Paul Wouters <pwouters@redhat.com> - 0.0-0.20.20130328
- Update to 20130328 (rhbz#964210)
- Removed DESTDIR patch, got merged in at upstream

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0-0.19.20120405
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Sep 27 2012 Jeffrey Ollie <jeff@ocjtech.us> - 0.0-0.18.20120405
- Update to 20120405

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0-0.17.20100213
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0-0.16.20100213
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.0-0.15.20100213
- Rebuild for new libpng

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0-0.14.20100213
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Mar 09 2010 Jarod Wilson <jarod@redhat.com> - 0.0-0.13.20100213
- Update to 20100213 release
- Add a devel sub-package so other software can be built against
  the system libhdhomerun (Rolf Fokkens, fixes rhbz#571139)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0-0.12.20090415
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 30 2009 Jarod Wilson <jarod@redhat.com> 0.0-0.11.20090415
- Add README.firmware, pointing folks to firmware downloads

* Tue Jun 23 2009 Jarod Wilson <jarod@redhat.com> 0.0-0.10.20090415
- Update to 20090415 release
- Add new GTK2 config GUI

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0-0.9.20081002
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Nov 20 2008 Jarod Wilson <jarod@redhat.com> 0.0-0.8.20081002
- Update to 20081002 release

* Tue Aug 19 2008 Jarod Wilson <jarod@redhat.com> 0.0-0.7.20080727
- Update to 20080727 release

* Thu Feb 14 2008 Jarod Wilson <jwilson@redhat.com> 0.0-0.6.20080212
- Update to 20080212 release

* Fri Oct 19 2007 Jarod Wilson <jwilson@redhat.com> - 0.0-0.5.20071015
- Update to 20071015 release
- Update license field

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.0-0.4.20070716
- Rebuild for selinux ppc32 issue.

* Tue Jul 17 2007 Jarod Wilson <jwilson@redhat.com> 0.0-0.3.20070716
- Update to 20070716 release

* Thu Jul 12 2007 Jarod Wilson <jwilson@redhat.com> 0.0-0.2.20070616
- Use sed instead of perl, drop perl BR: (jeff@ocjtech.us)
- Convert source files to utf8 (jeff@ocjtech.us)

* Mon Jun 18 2007 Jarod Wilson <jwilson@redhat.com> 0.0-0.1.20070616
- Update to 20070616 release
- Don't install any of the header files and drop lib from the package
  name, since this really isn't a library

* Fri May 18 2007 Jarod Wilson <jwilson@redhat.com> 0.0-0.1.20070512
- Initial packaging for Fedora
