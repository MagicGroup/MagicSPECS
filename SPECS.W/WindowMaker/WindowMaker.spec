Summary:        A fast, feature rich Window Manager
Summary(zh_CN.UTF-8): 一个快速，功能丰富的窗口管理器
Name:           WindowMaker
Version:	0.95.7
Release:	3%{?dist}

License:        GPLv2+
Group:          User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
URL:            http://www.windowmaker.org
Source0:        http://windowmaker.org/pub/source/release/WindowMaker-%{version}.tar.gz
Source1:        WindowMaker-xsession.desktop
Source2:        WindowMaker-application.desktop

Source3:        WindowMaker-uk.po
Source4:        WPrefs-uk.po

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
# X BR
BuildRequires:  libICE-devel
BuildRequires:  libSM-devel
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  libXft-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXpm-devel
BuildRequires:  libXrender-devel
BuildRequires:  xorg-x11-proto-devel
BuildRequires:  libXmu-devel
BuildRequires:  libXrandr-devel
# graphic BR
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libungif-devel
BuildRequires:  libtiff-devel

# other
BuildRequires:  zlib-devel
BuildRequires:  gettext-devel
BuildRequires:  fontconfig-devel
BuildRequires:  automake autoconf libtool
BuildRequires:  chrpath

Requires:       WINGs-libs = %{version}-%{release}

%description
Window Maker is an X11 window manager designed to give additional
integration support to the GNUstep Desktop Environment. In every way
possible, it reproduces the elegant look and feel of the nextstep GUI.
It is fast, feature rich, easy to configure, and easy to use. In
addition, Window Maker works with GNOME and KDE, making it one of the
most useful and universal window managers available.

%description -l zh_CN.UTF-8
一个快速的，功能丰富的 X11 窗口管理器。

%package devel
Summary:        Development files for WindowMaker
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       WindowMaker = %{version}-%{release}
Requires:       WINGs-devel = %{version}-%{release}

%description devel
Development files for WindowMaker.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package -n WINGs-libs
Summary:        Widgets and image libraries needed for WindowMaker
Summary(zh_CN.UTF-8): %{name} 的部件和图像库
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库

%description -n WINGs-libs
Widgets and image libraries needed for WindowMaker.

%description -n WINGs-libs -l zh_CN.UTF-8
%{name} 的部件和图像库。

%package -n WINGs-devel
Summary:        Development files for the WINGs library
Summary(zh_CN.UTF-8): WINGs 的开发包
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:       WINGs-libs = %{version}-%{release}
Requires:       libX11-devel
Requires:       xorg-x11-proto-devel
Requires:       libXinerama-devel
Requires:       libXrandr-devel
Requires:       libXext-devel
Requires:       libtiff-devel
Requires:       zlib-devel
Requires:       libXpm-devel
Requires:       libjpeg-devel
Requires:       libpng-devel
Requires:       libungif-devel
Requires:       libXft-devel
Requires:       fontconfig-devel

%description -n WINGs-devel
Development files for the WINGs library.

%description -n WINGs-devel -l zh_CN.UTF-8
WINGs 的开发包。

%prep
%setup -q

# add uk translation
cp %{SOURCE3} po/uk.po
cp %{SOURCE4} WPrefs.app/po/uk.po

# cleanup menu entries
for i in WindowMaker/*menu* ; do
echo $i
sed -i.old -e 's:/usr/local/:%{_prefix}/:g' \
  -e 's:/home/mawa:$(HOME):g' \
  -e 's:GNUstep/Applications/WPrefs.app:bin:g' $i
done

%build
CFLAGS="$RPM_OPT_FLAGS -DNEWAPPICON"
LINGUAS=`(cd po ; echo *.po | sed 's/.po//g')`
NLSDIR="%{_datadir}/locale"

export CFLAGS LINGUAS NLSDIR

%configure \
 --disable-static \
 --enable-modelock \
 --enable-xrandr \
 --enable-xinerama \
 --enable-usermenu \
 --x-includes=%{_includedir} \
 --x-libraries=%{_libdir}

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT NLSDIR=%{_datadir}/locale install
magic_rpm_clean.sh
%find_lang '\(WPrefs\|WindowMaker\|WINGs\|wmgenmenu\)'

install -D -m0644 -p %{SOURCE1} \
%{buildroot}%{_datadir}/xsessions/WindowMaker.desktop
install -D -m0644 -p %{SOURCE2} \
%{buildroot}%{_datadir}/applications/WindowMaker.desktop

find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'

chmod 755 %{buildroot}%{_datadir}/WindowMaker/{autostart.sh,exitscript.sh}

# remove rpath
for f in wmaker wdwrite wdread getstyle setstyle convertfonts seticons \
geticonset wmsetbg wmagnify wmgenmenu wmmenugen WPrefs ; do
chrpath --delete %{buildroot}%{_bindir}/$f
done

chrpath --delete %{buildroot}%{_libdir}/libWINGs.so.3.1.0

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post -n WINGs-libs -p /sbin/ldconfig

%postun -n WINGs-libs -p /sbin/ldconfig

%files -f '\(WPrefs\|WindowMaker\|WINGs\|wmgenmenu\)'.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog NEWS FAQ* README* COPYING*
%config %{_sysconfdir}/WindowMaker/
%{_bindir}/wmaker
%{_bindir}/wdwrite
%{_bindir}/wdread
%{_bindir}/getstyle
%{_bindir}/setstyle
%{_bindir}/convertfonts
%{_bindir}/seticons
%{_bindir}/geticonset
%{_bindir}/wmsetbg
%{_bindir}/wmagnify
%{_bindir}/wmgenmenu
%{_bindir}/wmmenugen
%{_bindir}/WPrefs
%{_bindir}/wkdemenu.pl
%{_bindir}/wm-oldmenu2new
%{_bindir}/wmaker.inst
%{_bindir}/wmiv
%{_bindir}/wxcopy
%{_bindir}/wxpaste
%{_libdir}/libWMaker.so.*
%{_datadir}/xsessions/WindowMaker.desktop
%{_datadir}/applications/WindowMaker.desktop
%{_datadir}/WindowMaker/
%{_datadir}/WPrefs/
%{_mandir}/man1/*.1*
%{_mandir}/man8/upgrade-windowmaker-defaults*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libWMaker.so
%{_includedir}/WMaker.h
%{_libdir}/pkgconfig/WUtil.pc

%files -n WINGs-libs
%defattr(-,root,root,-)
%doc WINGs/BUGS WINGs/ChangeLog WINGs/NEWS WINGs/README WINGs/TODO
%{_libdir}/libWINGs.so.*
%{_libdir}/libwraster.so.*
%{_libdir}/libWUtil.so.*
%{_datadir}/WINGs/

%files -n WINGs-devel
%defattr(-,root,root,-)
%{_bindir}/get-wings-flags
%{_bindir}/get-wraster-flags
%{_bindir}/get-wutil-flags
%{_libdir}/libWINGs.so
%{_libdir}/libWUtil.so
%{_libdir}/libwraster.so
%{_libdir}/pkgconfig/WINGs.pc
%{_libdir}/pkgconfig/wrlib.pc
%{_includedir}/WINGs/
%{_includedir}/wraster.h
%{_mandir}/man1/get-wings-flags*
%{_mandir}/man1/get-wraster-flags*
%{_mandir}/man1/get-wutil-flags*

%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 0.95.7-3
- 为 Magic 3.0 重建

* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 0.95.7-2
- 为 Magic 3.0 重建

* Mon Oct 19 2015 Liu Di <liudidi@gmail.com> - 0.95.7-1
- 更新到 0.95.7

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 0.95.3-4
- 为 Magic 3.0 重建

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.95.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 31 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.95.3-2
- fix description

* Mon May 28 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.95.3-1
- version upgrade (rhbz#824670)

* Wed Feb 15 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.95.2-1
- version upgrade

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.95.0-0.3.crm.a9e136ec41118f8842f7aa1457b2db83dbde6b7f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Dec 17 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.95.0-0.2.crm.a9e136ec41118f8842f7aa1457b2db83dbde6b7f
- fix requires

* Sat Dec 10 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.95.0-0.1.crm.a9e136ec41118f8842f7aa1457b2db83dbde6b7f
- build git snapshot
- cleanup spec file
- obsolete WindowMaker-devel package

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.92.0-23
- Rebuild for new libpng

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.92.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 08 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.92.0-21
- add -lfontconfig to WPrefs (fixes #660950)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.92.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.92.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Sep 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.92.0-18
- fix patches to apply without fuzz
- adjust URL/Source to new website

* Mon Feb 11 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de> - 0.92.0-17
- Rebuilt for gcc43

* Thu Jan 03 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.92.0-16
- fix #427430

* Sun Dec 09 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.92.0-15
- add patches from #267041 for less wakeup calls
- fix multilib stuff #343431

* Thu Aug 23 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 0.92.0-14
- new license tag
- rebuild for buildid

* Sun Jun 03 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.92.0-13
- fix a menu bug for WPrefs
- clean up menu path

* Thu Apr 26 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.92.0-12
- apply some changes from Patrice Dumas
- fix requires

* Sun Mar 04 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.92.0-11
- fix install location of WPrefs (#228346)
- fix menu modification sniplet
- split into sub packages to fix multilib issues (#228346)
- mark sh files executable

* Sat Nov 04 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.92.0-10
- fix #185579: bouncing animation will respect animations off setting
- fix #211263: missing dependencies in devel package

* Fri Sep 15 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.92.0-9
- FE6 rebuild

* Thu Mar 02 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.92.0-8
- fix gdm detection

* Sun Feb 26 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.92.0-7
- fix #181981
- go to new cvs snapshot (which includes qt fix)
- add patches from altlinuxs rpm (suggested by Andrew Zabolotny)
- get rid of static libs (finally)
- tune configure
- add uk translation
- finally add extras source
- fix stack-smash while reading workspace names

* Thu Feb 16 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.92.0-6
- Rebuild for Fedora Extras 5

* Fri Nov 25 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.92.0-5
- modular xorg integration

* Thu Nov 17 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.92.0-4
- add menu fix from Rudol Kastel (#173329)

* Mon Aug 22 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.92.0-3
- add gcc4/x86_64 patch from cvs

* Tue Aug 09 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.92.0-2
- try to fix x86_64 build

* Tue Aug 09 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.92.0-1
- upgrade to new version 
- use dist tag
- use smp_mflags
- fix #163459

* Tue May 31 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add disttag fc3<fc4

* Tue May 31 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.91.0-1
- upgrade to 0.91.0

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Fri Nov 28 2003 Dams <anvil[AT]livna.org> - 0:0.80.2-0.fdr.6
- exclude -> rm
- Added patch to fix gtk2 apps handling and other focus things

* Wed Sep 17 2003 Dams <anvil[AT]livna.org> 0:0.80.2-0.fdr.5
- Shortened files section
- Fixed tarball permissions (now a+r)

* Wed Sep 17 2003 Dams <anvil[AT]livna.org> 0:0.80.2-0.fdr.4
- Header files were installed in the wrong directory. Fixed. Slovak
  man pages installation fixed same way.
- WindowWaker-libs is now obsolete.

* Tue Aug 12 2003 Dams <anvil[AT]livna.org> 0:0.80.2-0.fdr.3
- buildroot -> RPM_BUILD_ROOT
- New devel package
- No more libs package

* Thu Apr 10 2003 Dams <anvil[AT]livna.org> 0:0.80.2-0.fdr.2
- Added missing Require: for gettext

* Tue Apr  8 2003 Dams <anvil[AT]livna.org>
- Initial build.
