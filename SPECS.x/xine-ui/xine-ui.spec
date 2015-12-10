# TODO, sometime: nvtvsimple

# hg version
# %global hgdate 20091217

Summary:        A skinned xlib-based gui for xine-lib
Summary(zh_CN.UTF-8): xine-lib 可换肤的基于 xlib 的图形界面
Name:           xine-ui
Version:	0.99.9
Release:        3%{?dist}
License:        GPLv2+
Group:          Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
URL:            http://www.xine-project.org/

Source0:        http://sourceforge.net/projects/xine/files/xine-ui/%{version}/xine-ui-%{version}.tar.xz

#Use source from hg for now to fix a few bugs
#This tarball has been created with
# hg clone http://hg.debian.org/hg/xine-lib/xine-ui/ xine-ui-0.99.6
# find xine-ui-0.99.6 -name .hg* -exec rm -rf {} \;
# find xine-ui-0.99.6 -name .cvs* -exec rm -rf {} \;
# tar jcf xine-ui-0.99.6-20091217.tar.bz2 xine-ui-0.99.6/
# Source0:	xine-ui-%{version}-%{hgdate}.tar.bz2
BuildRequires:	autoconf
BuildRequires:	automake

# Patch to enable linking to shared library version of lirc
Patch0:         xine-ui-0.99.5-shared-lirc.patch
# Patch to use UTF-8 documentation, BZ #512598
Patch1:         xine-ui-0.99.5-utf8doc.patch


#o Sources for -skins. Ugh.
Source1:	http://xine-project.org/skins/Antares.tar.gz
Source2:        http://xine-project.org/skins/Bambino-Black.tar.gz
Source3:        http://xine-project.org/skins/Bambino-Blue.tar.gz
Source4:        http://xine-project.org/skins/Bambino-Green.tar.gz
Source5:        http://xine-project.org/skins/Bambino-Orange.tar.gz
Source6:        http://xine-project.org/skins/Bambino-Pink.tar.gz
Source7:        http://xine-project.org/skins/Bambino-Purple.tar.gz
Source8:        http://xine-project.org/skins/Bambino-White.tar.gz
Source9:        http://xine-project.org/skins/blackslim2.tar.gz
Source10:       http://xine-project.org/skins/Bluton.tar.gz
Source11:       http://xine-project.org/skins/caramel.tar.gz
Source12:       http://xine-project.org/skins/CelomaChrome.tar.gz
Source13:       http://xine-project.org/skins/CelomaGold.tar.gz
Source14:       http://xine-project.org/skins/CelomaMdk.tar.gz
Source15:       http://xine-project.org/skins/Centori.tar.gz
Source16:       http://xine-project.org/skins/cloudy.tar.gz
Source17:       http://xine-project.org/skins/concept.tar.gz
Source18:       http://xine-project.org/skins/Crystal.tar.gz
Source19:       http://xine-project.org/skins/Galaxy.tar.gz
Source20:       http://xine-project.org/skins/gudgreen.tar.gz
Source21:       http://xine-project.org/skins/KeramicRH8.tar.gz
Source22:       http://xine-project.org/skins/Keramic.tar.gz
Source23:       http://xine-project.org/skins/lcd.tar.gz
Source24:       http://xine-project.org/skins/mp2k.tar.gz
Source25:       http://xine-project.org/skins/mplayer.tar.gz
Source26:       http://xine-project.org/skins/OMS_legacy.tar.gz
Source27:       http://xine-project.org/skins/pitt.tar.gz
Source28:       http://xine-project.org/skins/Polaris.tar.gz
Source29:       http://xine-project.org/skins/Sunset.tar.gz
Source30:       http://xine-project.org/skins/xinium.tar.gz

Source31:	default.ogv

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Package was named xine in rpmfusion
Provides:       xine = %{version}-%{release}
Obsoletes:      xine < %{version}-%{release}

BuildRequires:  aalib-devel >= 1.2.0
BuildRequires:  curl-devel >= 7.10.2
BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  libcaca-devel
BuildRequires:  libpng-devel >= 1.5
BuildRequires:  libtermcap-devel
BuildRequires:  libXft-devel
BuildRequires:  libXi-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXt-devel
BuildRequires:  libXtst-devel
BuildRequires:  libXv-devel
BuildRequires:  libXxf86vm-devel
BuildRequires:  readline-devel
BuildRequires:  xine-lib-devel >= 1.1.0
BuildRequires:  xorg-x11-proto-devel

# Lirc-devel is not available on EPEL-5
%if 0%{?rhel} == 0
BuildRequires:  lirc-devel
%endif

# For dir ownership
Requires:       hicolor-icon-theme
Requires:       xine-lib

%description
xine-ui is the traditional, skinned GUI for xine-lib. 

%description -l zh_CN.UTF-8
这是 xine-lib 的一个图形界面。

# Skins

%package skins
Summary:        Extra skins for xine-ui
Summary(zh_CN.UTF-8): xine-ui 的额外皮肤
Group:          Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Requires:       %{name} = %{version}-%{release}
# Package in RPMFusion was named skine-skins
Obsoletes:      xine-skins
%if 0%{?fedora}>10 || 0%{?rhel}>5
BuildArch:      noarch
%endif

%description skins
This package contains extra skins for xine-ui.

%description skins -l zh_CN.UTF-8
xine-ui 的额外皮肤。

%package aaxine
Summary:	ASCII art player for terminals
Summary(zh_CN.UTF-8): 终端下的 ASCII 字符播放器
Group:		Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Requires:	%{name} = %{version}-%{release}
Requires:	xine-lib-extras

%description aaxine
This package contains the ASCII art player for terminals like the vt100

%description aaxine -l zh_CN.UTF-8
终端下的 ASCII 艺术字符播放器。

%prep
# Setup xine
%setup0 -q
# Setup skins
%setup1 -T -q -c -n %{name}-%{version}/fedoraskins -a1 -a2 -a3 -a4 -a5 -a6 -a7 -a8 -a9 -a10 -a11 -a12 -a13 -a14 -a15 -a16 -a17 -a18 -a19 -a20 -a21 -a22 -a23 -a24 -a25 -a26 -a27 -a28 -a29 -a30
# Restore directory
%setup -T -D

# Backup time stamp
touch -r m4/_xine.m4 m4/_xine.m4.stamp
#%patch0 -p1
%patch1 -p1
# and restore it
touch -r m4/_xine.m4.stamp m4/_xine.m4


# By default aaxine dlopen()'s a nonversioned libX11.so, however in Fedora
# it's provided by libX11-devel => version the dlopen()
libx11so=$(ls -1 %{_libdir}/libX11.so.? | tail -n 1)
if [ -n "$libx11so" -a -f "$libx11so" ] ; then
    sed -i -e "s/\"libX11\\.so\"/\"$(basename $libx11so)\"/" src/aaui/main.c
fi

#touch -r configure.ac configure.ac.stamp
#sed -i -e 's/LINUX_KD_HB/LINUX_KD_H/g;s|linux/kd\.hb|linux/kd.h|g' \
#    config.h.in configure.ac configure
#touch -r configure.ac.stamp configure.ac

for f in doc/man/{de,es,fr}/*.1* doc/README?{cs,de,es,fi,fr,it} ; do
    iconv -f iso-8859-1 -t utf-8 $f > $f.utf8 && \
    touch -r $f $f.utf8 && \
    mv $f.utf8 $f
done
for f in doc/README_uk ; do
    iconv -f koi8-r -t utf-8 $f > $f.utf8 && \
    touch -r $f $f.utf8 && \
    mv $f.utf8 $f
done
for f in doc/man/pl/*.1* doc/README?{cs,pl}* ; do
    iconv -f iso-8859-2 -t utf-8 $f > $f.utf8 && \
    touch -r $f $f.utf8 && \
     mv $f.utf8 $f
done

cp -a src/xitk/xine-toolkit/README doc/README.xitk

# Clean out skins
find fedoraskins/ -type d -name "CVS" -exec rm -rf {} \; || :
find fedoraskins/ -type d -name ".xvpics" -exec rm -rf {} \; || :

sed -i 's,default.avi,default.ogv,' src/xitk/actions.c
sed -i 's,default.avi,default.ogv,' misc/visuals/Makefile.in

%build
./autogen.sh noconfig
export LIRC_CFLAGS="-llirc_client"
export LIRC_LIBS="-llirc_client"
#%configure --disable-dependency-tracking --enable-vdr-keys --with-aalib XINE_DOCPATH=%{_docdir}/%{name}-%{version}
# Set documentation directory
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="install -p"
%find_lang 'xi\(ne-ui\|tk\)'

desktop-file-install --remove-category="Application" --vendor="" \
    --add-category="Audio" --add-category="Video" \
    --dir %{buildroot}%{_datadir}/applications misc/desktops/xine.desktop

# Remove the desktop file installed in the wrong place 
rm -rf %{buildroot}%{_datadir}/xine/desktop

# Remove the default avi. Gets replaced with default.ogv
rm -rf %{buildroot}%{_datadir}/xine/visuals/default.avi

# Remove automatically installed documentation (listed in %doc)
rm -rf %{buildroot}%{_docdir}/

# Install extra skins
cp -a fedoraskins/* %{buildroot}%{_datadir}/xine/skins/


%clean
rm -rf %{buildroot}


%post
# Mime type
update-desktop-database &> /dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :
# Icon cache
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
# Mime type
update-desktop-database &> /dev/null || :
update-mime-database %{_datadir}/mime &> /dev/null || :
# Icon cache
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f 'xi\(ne-ui\|tk\)'.lang
%defattr(-,root,root,-)
%doc doc/README*
%{_bindir}/cacaxine
%{_bindir}/fbxine
%{_bindir}/xine
%{_bindir}/xine-bugreport
%{_bindir}/xine-check
%{_bindir}/xine-remote

%dir %{_datadir}/xine/skins/
%{_datadir}/xine/skins/xinetic/
#%{_datadir}/xine/skins/xine-ui_logo.mpv
%{_datadir}/xine/skins/xine_splash.png
%{_datadir}/xine/oxine/
%{_datadir}/xine/visuals/

%{_datadir}/mime/packages/xine-ui.xml
%{_datadir}/applications/*xine.desktop
%{_datadir}/icons/hicolor/*x*/apps/xine.png
%{_datadir}/pixmaps/xine.xpm
%{_mandir}/man1/*.1.gz
%lang(de) %{_mandir}/de/man1/*.1.gz
%lang(es) %{_mandir}/es/man1/*.1.gz
%lang(fr) %{_mandir}/fr/man1/*.1.gz
%lang(pl) %{_mandir}/pl/man1/*.1.gz

%files skins
%defattr(-,root,root,-)
%{_datadir}/xine/skins/*
%exclude %{_datadir}/xine/skins/xinetic/
#%exclude %{_datadir}/xine/skins/xine-ui_logo.mpv
%exclude %{_datadir}/xine/skins/xine_splash.png

%files aaxine
%defattr(-,root,root,-)
%{_bindir}/aaxine

%changelog
* Sat Nov 14 2015 Liu Di <liudidi@gmail.com> - 0.99.9-3
- 为 Magic 3.0 重建

* Fri Nov 06 2015 Liu Di <liudidi@gmail.com> - 0.99.9-2
- 为 Magic 3.0 重建

* Sat Sep 19 2015 Liu Di <liudidi@gmail.com> - 0.99.9-1
- 更新到 0.99.9

* Tue Jun 10 2014 Liu Di <liudidi@gmail.com> - 0.99.8-1
- 更新到 0.99.8

* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 0.99.6-31
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.6-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Michael J Gruber <mjg@fedoraproject.org> 0.99.6-29
- fix build with libpng-1.5

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.99.6-28.1
- Rebuild for new libpng

* Sun Aug 14 2011 Rex Dieter <rdieter@fedoraproject.org> - 0.99.6-27.1
- Rebuilt for rpm (#728707)

* Thu Jul 21 2011 Michael J Gruber <mjg@fedoraproject.org> 0.99.6-27
- fix build with newer curl (curl/types.h gone MIA)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.6-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun May 02 2010 Thomas Janssen <thomasj@fedoraproject.org> 0.99.6-25
- fix help crash #579021

* Sun Apr 18 2010 Thomas Janssen <thomasj@fedoraproject.org> 0.99.6-24
- replaced default.avi with default.ogv #572378

* Fri Apr 16 2010 Thomas Janssen <thomasj@fedoraproject.org> 0.99.6-23
- subpkg aaxine to prevent xine-lib-extras for xine-ui

* Sun Apr 11 2010 Thomas Janssen <thomasj@fedoraproject.org> 0.99.6-2
- readded skins

* Sun Apr 11 2010 Thomas Janssen <thomasj@fedoraproject.org> 0.99.6-1
- xine-ui-0.99.6

* Thu Dec 17 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.99.6-0.1.20091217hg
- Switch to development branch by suggestion of upstream to fix some bugs.

* Thu Sep 03 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.99.5-16
- Move xine-ui_logo.mpv to main package from -skins.

* Sat Jul 25 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.99.5-15
- Move xine_splash.png to main package from -skins.
- Fix EPEL build.

* Thu Jul 23 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.99.5-14
- Fix build in rawhide.

* Mon Jul 20 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.99.5-13
- Added -skins subpackage.

* Wed Jul 15 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.99.5-12
- Added BR: xorg-x11-proto-devel.

* Sun May 17 2009 Jussi Lehtola <jussi.lehtola@iki.fi> - 0.99.5-11
- Added missing icon cache update to %%post section.

* Sun May 17 2009 Jussi Lehtola <jussi.lehtola@iki.fi> - 0.99.5-10
- Use desktop-install --remove-category instead of sed.

* Sat May 16 2009 Jussi Lehtola <jussi.lehtola@iki.fi> - 0.99.5-9
- More desktop file fixes.
- Fix aaxine by adding Requires: xine-lib-extras.

* Fri May 15 2009 Jussi Lehtola <jussi.lehtola@iki.fi> - 0.99.5-8
- Conserve time stamps.
- Drop unnecessary desktop file patch.
- Drop unnecessary versioning of dlopen'd libX11.so.
- Add mime type update and fix icon cache update.

* Fri May 15 2009 Jussi Lehtola <jussi.lehtola@iki.fi> - 0.99.5-7
- Fixes for inclusion into Fedora.

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.99.5-6
- rebuild for new F11 features

* Wed Oct 29 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.99.5-5
- rebuilt

* Sun Oct 26 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.99.5-4
- rebuilt

* Mon Aug 04 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.99.5-2
- rebuild

* Sat Jul 14 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.99.5-1
- 0.99.5, lots of patches made obsolete.
- Update icon cache and desktop database.
- Patch {aa,caca}xine to dlopen libX11.so.* instead of libX11.so at runtime.
- Patch to look for linux/kd.h instead of linux/kd.hb during build.
- Don't run autotools during build.

* Thu Mar 01 2007 Thorsten Leemhuis <fedora at leemhuis.info> - 0.99.4-11
- rebuild for new curl

* Tue Nov  7 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.99.4-10
- Re-enable VDR keys and patch, patched xine-lib not required (#1241).

* Thu Nov  2 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.99.4-9
- Drop X-Livna and Application desktop entry categories.

* Thu Nov  2 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.99.4-8
- Make VDR support optional, disabled by default, fixes #1238.

* Thu Apr 20 2006 Dams <anvil[AT]livna.org> - 0.99.4-7
- Added patch8 to fix up buffer overflow describe in #926

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Fri Jan 20 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.99.4-0.lvn.6
- %%langify non-English manpages, really convert all (and more docs) to UTF-8.
- Improve summary and description.

* Tue Jan  3 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.99.4-0.lvn.5
- Adapt to modular X.
- Drop pre-FC5 workarounds and rpmbuild conditionals.

* Thu Sep 29 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.99.4-0.lvn.4
- Clean up obsolete pre-FC3 stuff (LIRC and CACA now unconditionally enabled).
- Drop zero Epochs.

* Thu Sep 15 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.4-0.lvn.3
- Apply sprintf, uifixups and xftfontsize patches from Alex Stewart/freshrpms.
- Fix fbxine crash when the tty mode can't be set (upstreamed).
- Fix fbxine usage message and options (upstreamed).
- Make vdr support conditional (default enabled), require vdr-patched xine-lib
  if enabled, and build with it for FC4+.
- Build with gcc4 again on FC4+.

* Sun Aug 14 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.4-0.lvn.2
- Sync VDR patch with vdr-xine-0.7.5 (just for tracking purposes, no changes).

* Tue Aug  2 2005 Dams <anvil[AT]livna.org> - 0:0.99.4-0.lvn.1
- Updated to 0.99.4
- Fixed files section
- Dropped patch5 
- Dropped patch3

* Sun Jul 10 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.3-0.lvn.8
- Build with compat-gcc-32 for FC4 ("--with gcc32") as a temporary workaround
  for spurious directory creation attempts (#419) and possibly other issues.
- Use shared LIRC client libs, possibly enable LIRC support also on x86_64.
- Apply gcc4 menu crash fix, kudos for the patch to freshrpms.net and
  Alex Stewart, this'll be handy when we try with gcc4 again (#467).
- Clean up obsolete pre-FC2 stuff.

* Sat Jun  4 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.3-0.lvn.7
- Apply VDR support update patch from vdr-xine-0.7.4.

* Sat May 28 2005 Thorsten Leemhuis <fedora at leemhuis.info> - 0:0.99.3-0.lvn.6
- Fix typo

* Mon May  9 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.3-0.lvn.5
- Add support for CACA, rebuild with "--without caca" to disable (#380).

* Sat Apr 30 2005 Dams <anvil[AT]livna.org> - 0:0.99.3-0.lvn.4
- Fixed gcc4 build

* Wed Apr 13 2005 Dams <anvil[AT]livna.org> - 0:0.99.3-0.lvn.3
- Conditional lirc buildreq (default enabled)

* Sat Jan  1 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:0.99.3-0.lvn.2
- Enable support for VDR interaction keys.
- Enable curl unconditionally.
- Build with dependency tracking disabled.

* Wed Dec 29 2004 Dams <anvil[AT]livna.org> - 0:0.99.3-0.lvn.1
- Updated to 0.99.3

* Tue Jul  6 2004 Dams <anvil[AT]livna.org> 0:0.99.2-0.lvn.2
- Updated no-march/mcpu patch
- Updated mkinstalldirs patch

* Mon Jul  5 2004 Dams <anvil[AT]livna.org> 0:0.99.2-0.lvn.1
- Updated to 0.99.2

* Sun Jun 13 2004 Dams <anvil[AT]livna.org> 0:0.99.1-0.lvn.3
- Updated desktop entry for HID compliance

* Fri May 21 2004 Dams <anvil[AT]livna.org> 0:0.99.1-0.lvn.2
- Updated URL in Source0

* Sat Apr 17 2004 Dams <anvil[AT]livna.org> 0:0.99.1-0.lvn.1
- Updated to 0.99.1

* Thu Feb 26 2004 Dams <anvil[AT]livna.org> 0:0.9.23-0.lvn.2
- Updated xine-lib version requirement in build dependancy
- Hopefully fixed build for RH9

* Thu Dec 25 2003 Dams <anvil[AT]livna.org> 0:0.9.23-0.lvn.1
- s/fedora/livna/

* Thu Dec 25 2003 Dams <anvil[AT]livna.org> 0:0.9.23-0.fdr.1
- Updated patch for no march/mcpu from configure

* Wed Dec 24 2003 Dams <anvil[AT]livna.org> 0:0.9.23-0.fdr.1
- Updated to 0.9.23

* Sun Sep 28 2003 Dams <anvil[AT]livna.org> 0:0.9.22-0.fdr.4
- Added patch to fix po/Makefile for servern2 build

* Sun Aug 31 2003 Dams <anvil[AT]livna.org> 0:0.9.22-0.fdr.3
- Translated manpages iconv'ed into utf-8 encoding

* Sat Aug 23 2003 Dams <anvil[AT]livna.org> 0:0.9.22-0.fdr.2
- Conflict with old xine-skins packages
- Removed lirc conditionnal build requirement
- Added conditionnal Build dependencies for curl
- Added missing libtool BuildRequires

* Wed Aug 20 2003 Dams <anvil[AT]livna.org> 0:0.9.22-0.fdr.2
- No more -skins package
- No more url in Source0

* Fri Aug  8 2003 Dams <anvil[AT]livna.org> 0:0.9.22-0.fdr.1
- Updated to 0.9.22

* Tue Jul 15 2003 Dams <anvil[AT]livna.org> 0:0.9.21-0.fdr.3
- exporting SED=__sed seems to fix build to rh80

* Sun Jul  6 2003 Dams <anvil[AT]livna.org> 0:0.9.21-0.fdr.2
- Trying to avoid unowned directories
- Patch for configure not to set march/mcpu.
- Removed BuildArch.

* Sat May 17 2003 Dams <anvil[AT]livna.org> 0:0.9.21-0.fdr.1
- Updated to 0.9.21
- buildroot -> RPM_BUILD_ROOT
- Updated URL in Source0
- Updated BuildRequires

* Sat Apr 12 2003 Dams <anvil[AT]livna.org> 0:0.9.20-0.fdr.5
- Arch stuff

* Wed Apr  9 2003 Dams <anvil[AT]livna.org> 0:0.9.20-0.fdr.4
- Fixed typo
- Rebuild, linked against xine-lib 1 beta10

* Mon Apr  7 2003 Dams <anvil[AT]livna.org> 0:0.9.20-0.fdr.3
- Only one find_lang

* Mon Apr  7 2003 Dams <anvil[AT]livna.org> 0:0.9.20-0.fdr.2
- Added BuildRequires.
- Added --with directives.
- Added use of desktop-file-install
- Added more Requires tag.

* Thu Apr  3 2003 Dams <anvil[AT]livna.org> 
- Initial build.
