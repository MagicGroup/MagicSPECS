Summary: A high quality TV viewer
Name: tvtime
Version: 1.0.2
Release: 18%{?dist}
License: GPLv2+ and LGPLv2+
Group: Applications/Multimedia
URL: http://tvtime.sourceforge.net
Source0: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Upstream is dead since 2005...
Patch0: tvtime-1.0.1-gcc4.1.patch
Patch1: tvtime-1.0.1-header.patch
Patch2: tvtime-1.0.1-fsbadval.patch
Patch3: tvtime-1.0.2-alsamixer.patch
Patch4: tvtime-1.0.2-localedef.patch
Patch5: tvtime-1.0.2-alsamixer2.patch
Patch6: tvtime-1.0.2-xss.patch
Patch7: tvtime-1.0.2-videoinput.patch
Patch8:	tvtime-1.0.2-libpng15.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: gtk2 >= 2.6
Requires: hicolor-icon-theme
Requires(postun): desktop-file-utils

BuildRequires: freetype-devel >= 2.0
BuildRequires: zlib-devel
BuildRequires: libpng-devel
BuildRequires: SDL-devel
BuildRequires: libxml2-devel
BuildRequires: libICE-devel
BuildRequires: libSM-devel
BuildRequires: libX11-devel
BuildRequires: libXext-devel
BuildRequires: libXinerama-devel
BuildRequires: libXtst-devel
BuildRequires: libXv-devel
BuildRequires: libXxf86vm-devel
BuildRequires: libXt-devel
BuildRequires: libXi-devel
BuildRequires: libXScrnSaver-devel
BuildRequires: libtool
BuildRequires: desktop-file-utils

ExcludeArch: s390 s390x

%description
tvtime is a high quality television application for use with video
capture cards.  tvtime processes the input from a capture card and
displays it on a computer monitor or projector.  Unlike other television
applications, tvtime focuses on high visual quality making it ideal for
videophiles.

%prep
%setup -q
%patch0 -p1 -b .gcc
%patch1 -p1 -b .header
%patch2 -p1 -b .fsbadval
%patch3 -p1 -b .alsamixer
%patch4 -p1 -b .localedef
%patch5 -p1 -b .alsamixer2
%patch6 -p1 -b .xss
%patch7 -p1 -b .vidioc
%patch8 -p1 -b .libpng15

for i in AUTHORS docs/man/{de,es}/*.?; do
	iconv -f iso-8859-1 -t utf-8 "$i" > "${i}_" && \
	touch -r "$i" "${i}_" && \
	mv "${i}_" "$i"
done
# Remove .png extension from desktop file as it causes a warning
# in desktop-file-install
sed -i "s|tvtime.png|tvtime|g" docs/net-tvtime.desktop



%build
libtoolize --force
autoreconf
%configure --disable-dependency-tracking --disable-rpath

make CXXFLAGS="%{optflags}" %{?_smp_mflags} \
	CFLAGS="%{optflags}" %{?_smp_mflags}

%install
rm -rf %{buildroot}

make DESTDIR=%{buildroot} INSTALL="/usr/bin/install -p" install
desktop-file-install --remove-category="Application" --add-category="Video" \
	--delete-original --dir=%{buildroot}%{_datadir}/applications \
	docs/net-tvtime.desktop

%find_lang %{name}

%post
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor 2> /dev/null || :
fi
%{_bindir}/update-desktop-database > /dev/null 2>&1 || :

%postun
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor 2> /dev/null || :
fi
%{_bindir}/update-desktop-database > /dev/null 2>&1 || :

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-, root, root, -)
%doc AUTHORS ChangeLog COPYING COPYING.LGPL NEWS README* data/COPYING* docs/html
%{_mandir}/man?/*
%dir %{_sysconfdir}/tvtime/
%config(noreplace) %{_sysconfdir}/tvtime/tvtime.xml
%{_bindir}/tvtime-command
%{_bindir}/tvtime-configure
%{_bindir}/tvtime-scanner
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/tvtime.png
%{_datadir}/pixmaps/*
%{_datadir}/tvtime/
%lang(de) %{_mandir}/de/man?/*
%lang(es) %{_mandir}/es/man?/*
%{_bindir}/tvtime

%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.0.2-18
- 为 Magic 3.0 重建

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 24 2010 Tomas Smetana <tsmetana@redhat.com> 1.0.2-16
- fix #655038 - tvtime does not work with UVC webcams

* Mon Nov 08 2010 Tomas Smetana <tsmetana@redhat.com> 1.0.2-15
- fix #571339 use a saner way to disable screensaver, thanks to Debian folks
  for the patch, namely Resul Cetin

* Fri Nov 05 2010 Tomas Smetana <tsmetana@redhat.com> 1.0.2-14
- rebuild with new libxml

* Mon Jan 04 2010 Tomas Smetana <tsmetana@redhat.com> 1.0.2-13
- finish merge review (#226508)
- revert the font-related patch; continue shipping tvtime's specific fonts

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 09 2009 Tomas Smetana <tsmetana@redhat.com> 1.0.2-11
- fix a typo in the default config file

* Sun Jun 28 2009 Tomas Smetana <tsmetana@redhat.com> 1.0.2-10
- fix BuildRequires (XInput.h has moved...)

* Sun Jun 28 2009 Tomas Smetana <tsmetana@redhat.com> 1.0.2-9
- try to document the new ALSA mixer settings, make ALSA mixer
  the default one

* Mon Jun 01 2009 Tomas Smetana <tsmetana@redhat.com> 1.0.2-8
- merge review round two; thanks to Jussi Lehtola

* Sun May 31 2009 Tomas Smetana <tsmetana@redhat.com> 1.0.2-7
- fix conflicting types for locale_t
- fix build requires for rawhide

* Sun May 31 2009 Tomas Smetana <tsmetana@redhat.com> 1.0.2-6
- fix #498167 - patch by Philipp Hahn adding ALSA mixer support
- merge review changes

* Tue Mar 03 2009 Tomas Smetana <tsmetana@redhat.com> 1.0.2-5
- fix font requirements

* Mon Mar 02 2009 Tomas Smetana <tsmetana@redhat.com> 1.0.2-4
- fix #477473 - drop fonts, depend on liberation-fonts

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Apr 03 2008 Tomas Smetana <tsmetana@redhat.com> 1.0.2-2
- compile with $RPM_OPT_FLAGS

* Mon Mar 10 2008 Tomas Smetana <tsmetana@redhat.com> 1.0.2-1
- update to 1.0.2

* Thu Mar 06 2008 Tomas Smetana <tsmetana@redhat.com> 1.0.1-8
- fix #235622 - X error when toggling fullscreen

* Tue Feb 12 2008 Tomas Smetana <tsmetana@redhat.com> 1.0.1-7
- fix license tag and summary
- rebuild (gcc-4.3)

* Thu Jul 13 2006 Than Ngo <than@redhat.com> 1.0.1-6
- fix build problem

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.0.1-5.1
- rebuild

* Tue May 16 2006 Than Ngo <than@redhat.com> 1.0.1-5 
- add BR on libXt-devel

* Mon Feb 27 2006 Than Ngo <than@redhat.com> 1.0.1-4
- fix post install script error #182895

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.0.1-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0.1-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 23 2005 Than Ngo <than@redhat.com> 1.0.1-3
- fix build problem with gcc4.1

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Nov 15 2005 Than Ngo <than@redhat.com> 1.0.1-2 
- fix for modular X

* Mon Sep 12 2005 Than Ngo <than@redhat.com> 1.0.1-1
- update to 1.0.1

* Wed Aug 17 2005 Than Ngo <than@redhat.com> 0.99-2
- rebuilt

* Tue Jul 19 2005 Than Ngo <than@redhat.com> 0.99-1
- update to 0.99
- fix gcc4 build problem

* Wed Apr 27 2005 Jeremy Katz <katzj@redhat.com> - 0.9.15-7
- silence %%post

* Mon Mar 28 2005 Christopher Aillon <caillon@redhat.com>
- rebuilt

* Fri Mar 25 2005 Christopher Aillon <caillon@redhat.com> 0.9.15-5
- Update the GTK+ theme icon cache on (un)install

* Sat Mar 05 2005 Than Ngo <than@redhat.com> 0.9.15-4
- rebuilt

* Mon Nov 22 2004 Miloslav Trmac <mitr@redhat.com> - 0.9.15-3
- Convert German man pages to UTF-8

* Tue Nov 16 2004 Than Ngo <than@redhat.com> 0.9.15-2
- remove suid root

* Sun Oct 31 2004 Than Ngo <than@redhat.com> 0.9.15-1
- update to 0.9.15

* Fri Oct 29 2004 Than Ngo <than@redhat.com> 0.9.14-2
- fix build problem on x86_64

* Fri Oct 29 2004 Than Ngo <than@redhat.com> 0.9.14-1
- update to 0.9.14

* Wed Sep 29 2004 Than Ngo <than@redhat.com> 0.9.13-1
- update to 0.9.13

* Mon Jun 21 2004 Than Ngo <than@redhat.com> 0.9.12-10
- fix gcc-3.4 build problem, thank to Jakub

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon May 24 2004 Than Ngo <than@redhat.com> 0.9.12-8
- add another patch to enable PIE build of tvtime binary

* Mon May 17 2004 Than Ngo <than@redhat.com> 0.9.12-7
- add patch to enable PIE build

* Mon Apr 19 2004 Than Ngo <than@redhat.com> 0.9.12-6
- add BuildRequires: libxml2-devel, bug #121237

* Tue Mar 16 2004 Mike A. Harris <mharris@redhat.com 0.9.12-5
- BuildRequires: s/XFree86-libs/XFree86-devel/

* Thu Mar 11 2004 Than Ngo <than@redhat.com> 0.9.12-4
- fixed gcc-3.4 build problem

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Dec 04 2003 Than Ngo <than@redhat.com> 0.9.12-2
- get rid of unused vsync.c code, which is broken on ppc/ppc64.

* Wed Dec 03 2003 Than Ngo <than@redhat.com> 0.9.12-1
- 0.9.12 release

* Mon Nov 10 2003 Than Ngo <than@redhat.com> 0.9.10-2
- built into new Fedora tree

* Mon Oct 13 2003 Than Ngo <than@redhat.com> 0.9.10-1
- 0.9.10
