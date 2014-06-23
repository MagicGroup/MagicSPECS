Name:           linphone
Version:	3.7.0
Release:        4%{?dist}
Summary:        Phone anywhere in the whole world by using the Internet

License:        GPLv2+
URL:            http://www.linphone.org/

%define majorver %(echo %{version} | awk -F. '{print $1"."$2}')
Source0:        http://download.savannah.gnu.org/releases/linphone/%{majorver}.x/sources/%{name}-%{version}.tar.gz
Patch0:         linphone-3.6.1-rootca.patch
Patch1:         linphone-3.6.1-arm.patch

# for video support
BuildRequires:  glew-devel
BuildRequires:  libtheora-devel
BuildRequires:  libv4l-devel
BuildRequires:  libvpx-devel
# xxd used in mediastreamer2/src/Makefile.in
BuildRequires:  vim-common

BuildRequires:  libosip2-devel >= 3.6.0
BuildRequires:  libeXosip2-devel >= 3.6.0
BuildRequires:  libpcap-devel
BuildRequires:  libsoup-devel
BuildRequires:  libudev-devel
BuildRequires:  libupnp-devel
BuildRequires:  openssl-devel
BuildRequires:  pulseaudio-libs-devel

BuildRequires:  sqlite-devel
BuildRequires:  readline-devel
BuildRequires:  ncurses-devel

BuildRequires:  libnotify-devel
BuildRequires:  gtk2-devel >= 2.16
BuildRequires:  alsa-lib-devel

BuildRequires:  opus-devel
BuildRequires:  speex-devel >= 1.2
BuildRequires:  spandsp-devel
BuildRequires:  gsm-devel

BuildRequires:  desktop-file-utils

BuildRequires:  perl(XML::Parser)

BuildRequires:  libglade2-devel

BuildRequires:  intltool
BuildRequires:  doxygen

BuildRequires:  libtool

BuildRequires:  ortp-devel >= 1:0.22.0
Requires:       ortp%{?_isa} >= 1:0.22.0

%description
Linphone is mostly sip compliant. It works successfully with these
implementations:
    * eStara softphone (commercial software for windows)
    * Pingtel phones (with DNS enabled and VLAN QOS support disabled).
    * Hotsip, a free of charge phone for Windows.
    * Vocal, an open source SIP stack from Vovida that includes a SIP proxy
        that works with linphone since version 0.7.1.
    * Siproxd is a free sip proxy being developed by Thomas Ries because he
        would like to have linphone working behind his firewall. Siproxd is
        simple to setup and works perfectly with linphone.
    * Partysip aims at being a generic and fully functionnal SIP proxy. Visit
        the web page for more details on its functionalities.

Linphone may work also with other sip phones, but this has not been tested yet.

%package devel
Summary:        Development libraries for linphone
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       linphone-mediastreamer-devel%{?_isa} = %{version}-%{release}
Requires:       glib2-devel%{?_isa}

%description    devel
Libraries and headers required to develop software with linphone.

%package mediastreamer
Summary:        A media streaming library for telephony applications

%description mediastreamer
Mediastreamer2 is a GPL licensed library to make audio and video
real-time streaming and processing. Written in pure C, it is based
upon the oRTP library.

%package mediastreamer-devel
Summary:        Development libraries for mediastreamer2
Requires:       linphone-mediastreamer%{?_isa} = %{version}-%{release}
Requires:       ortp-devel%{?_isa}

%description mediastreamer-devel
Libraries and headers required to develop software with mediastreamer2.

%prep
%setup0 -q
%patch0 -p1 -b .rootca
%ifarch %{arm}
%patch1 -p1 -b .arm
%endif

autoreconf -i -f

# remove bundled oRTP
rm -rf oRTP

# Fix encoding
for f in share/cs/*.1; do
  /usr/bin/iconv -f iso-8859-2 -t utf-8 -o $f.new $f
  sed -i -e 's/Encoding: ISO-8859-2/Encoding: UTF-8/' $f.new
  mv $f.new $f
done
for f in ChangeLog AUTHORS; do
  /usr/bin/iconv -f iso-8859-1 -t utf-8 -o $f.new $f
  mv $f.new $f
done


%build
%configure --disable-static \
           --enable-glx \
           --disable-ffmpeg \
           --disable-rpath \
           --enable-console_ui=yes \
           --enable-gtk_ui=yes \
           --enable-ipv6 \
           --enable-truespeech \
           --enable-alsa \
           --enable-strict \
           --enable-nonstandard-gsm \
           --enable-rsvp \
           --enable-ssl \
           --enable-zrtp \
           --enable-external-ortp

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}
%find_lang mediastreamer

desktop-file-install \
  --delete-original \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --remove-category Application \
  --add-category Telephony \
  --add-category GTK \
  $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

# move docs to %%doc
mkdir -p doc/linphone doc/mediastreamer
mv $RPM_BUILD_ROOT%{_datadir}/doc/linphone*/html doc/linphone
mv $RPM_BUILD_ROOT%{_datadir}/doc/mediastreamer*/html doc/mediastreamer

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post mediastreamer -p /sbin/ldconfig

%postun mediastreamer -p /sbin/ldconfig

%files -f %{name}.lang
%doc AUTHORS ChangeLog COPYING NEWS README TODO
%{_bindir}/linphone
%{_bindir}/linphonec
%{_bindir}/linphonecsh
%{_bindir}/lpc2xml_test
%{_bindir}/xml2lpc_test
%{_libdir}/liblinphone.so.5*
%{_libdir}/liblpc2xml.so.0*
%{_libdir}/libxml2lpc.so.0*
%{_mandir}/man1/*
%lang(cs) %{_mandir}/cs/man1/*
%{_datadir}/applications/*%{name}.desktop
%{_datadir}/gnome/help/linphone
%{_datadir}/pixmaps/linphone
%{_datadir}/sounds/linphone
%{_datadir}/linphone

%files devel
%doc doc/linphone/html
%{_includedir}/linphone
%{_libdir}/liblinphone.so
%{_libdir}/liblpc2xml.so
%{_libdir}/libxml2lpc.so
%{_libdir}/pkgconfig/linphone.pc

%files mediastreamer -f mediastreamer.lang
%doc mediastreamer2/AUTHORS mediastreamer2/ChangeLog mediastreamer2/COPYING
%doc mediastreamer2/NEWS mediastreamer2/README
%{_bindir}/mediastream
%{_libdir}/libmediastreamer_base.so.3*
%{_libdir}/libmediastreamer_voip.so.3*
%{_datadir}/images

%files mediastreamer-devel
%doc doc/mediastreamer/html
%{_includedir}/mediastreamer2
%{_libdir}/libmediastreamer_base.so
%{_libdir}/libmediastreamer_voip.so
%{_libdir}/pkgconfig/mediastreamer.pc

%changelog
* Mon Jun 09 2014 Liu Di <liudidi@gmail.com> - 3.7.0-4
- 为 Magic 3.0 重建

* Mon Jun 09 2014 Liu Di <liudidi@gmail.com> - 3.7.0-3
- 更新到 3.7.0

* Mon Nov 18 2013 Dave Airlie <airlied@redhat.com> - 3.6.1-3
- rebuilt for GLEW 1.10

* Sat Jul 27 2013 Alexey Kurov <nucleo@fedoraproject.org> - 3.6.1-2
- use /etc/ssl/certs/ca-bundle.crt root_ca
- fix armv7hl compilation

* Sun Jul  7 2013 Alexey Kurov <nucleo@fedoraproject.org> - 3.6.1-1
- linphone-3.6.1

* Fri Apr 26 2013 Jon Ciesla <limburgher@gmail.com> - 3.5.2-8
- Drop desktop vendor tag.

* Sat Mar 23 2013 Alexey Kurov <nucleo@fedoraproject.org> - 3.5.2-7
- autoreconf in %%prep (#926078)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 31 2012 Alexey Kurov <nucleo@fedoraproject.org> - 3.5.2-5
- add -mediastreamer and -mediastreamer-devel subpackages

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Mar  5 2012 Alexey Kurov <nucleo@fedoraproject.org> - 3.5.2-3
- drop regression patch

* Mon Feb 27 2012 Alexey Kurov <nucleo@fedoraproject.org> - 3.5.2-2
- install docs in -devel
- update glib-2.31 patch
- revert commit causing regression in 3.5.2

* Wed Feb 22 2012 Alexey Kurov <nucleo@fedoraproject.org> - 3.5.2-1
- linphone-3.5.2

* Sun Feb 19 2012 Alexey Kurov <nucleo@fedoraproject.org> - 3.5.1-1
- linphone-3.5.1
- BR: libsoup-devel
- Requires: ortp >= 1:0.18.0

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 27 2011 Alexey Kurov <nucleo@fedoraproject.org> - 3.5.0-2
- enable spandsp

* Mon Dec 26 2011 Alexey Kurov <nucleo@fedoraproject.org> - 3.5.0-1
- linphone-3.5.0
- add BR: libnotify-devel
- disable spandsp (#691039)

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 3.4.3-2
- Rebuild for new libpng

* Fri Sep  2 2011 Alexey Kurov <nucleo@fedoraproject.org> - 3.4.3-1
- linphone-3.4.3
- BR: openssl-devel libsamplerate-devel gettext
- BR: pulseaudio-libs-devel jack-audio-connection-kit-devel
- drop 3.2.1 patches

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Mar 17 2010 Jesse Keating <jkeating@redhat.com> - 3.2.1-2
- Apply patches from bug 555510 to update linphone
- Drop the doc/mediastreamer dir from devel package

* Mon Mar 01 2010 Adam Jackson <ajax@redhat.com> 2.1.1-5
- Rebuild for libortp.so.7

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 13 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 2.1.1-3
- Re-base patches to fix rebuild breakdowns.
- Fix various autotool source file bugs.
- Use pre-built autotool-generated files.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 14 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.1.1-1
- Update to 2.1.1

* Fri Feb  1 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.1.0-1
- Update to 2.1.0

* Wed Aug 29 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.7.1-4
- Update license tag.

* Wed Aug 29 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.7.1-3
- Update license tag.

* Mon May 14 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.7.1-2
- Add patch for compiling against external GSM library.

* Tue Apr 17 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.7.1-1
- Update to 1.7.1
- Drop linphone-1.0.1-desktop.patch, linphone-1.4.1-libs.patch and
  linphone-1.5.1-osipcompat.patch

* Fri Mar 16 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.6.0-4
- Fix up encodings in Czech manpages

* Fri Mar 16 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.6.0-3
- Move autoheader after aclocal, fixes 232592

* Mon Jan 29 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.6.0-2
- Fix buildrequires

* Mon Jan 29 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.6.0-1
- Update to 1.6.0

* Wed Nov 22 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.5.1-2
- Mark translated man pages with lang macro

* Tue Nov 21 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.5.1-1
- Update to 1.5.1

* Thu Oct 26 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.5.0-2
- Don't forget to add new files and remove old ones!

* Thu Oct 26 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.5.0-1
- Update to 1.5.0
- Fix spelling error in description.
- Remove invalid categories on desktop file.

* Wed Aug 30 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.2.0-7
- Bump release so that I can "make tag"

* Wed Aug 30 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.2.0-6
- Add BR for perl(XML::Parser) so that intltool will work.

* Wed Aug 30 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.2.0-5
- Bump release and rebuild.

* Mon Feb 13 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.0-2
- Rebuild for Fedora Extras 5

* Wed Feb  8 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.0-1
- Added version for speex-devel BR (#179879)

* Tue Jan 24 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.0-2
- Fixed selecting entry from address book (#177189)

* Tue Jan  3 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.2.0-1
- Upstream update

* Mon Dec  5 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.1.0-2
- Added version on ortp-devel

* Mon Dec  5 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.1.0-1
- Upstream update

* Wed Nov 30 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.0.1-5
- Remove ortp documentation for -devel

* Wed Nov 30 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.0.1-4
- Split out ortp

* Fri May 27 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.0.1-3
- Fix multiple menu entry and missing icon (#158975)
- Clean up spec file

* Fri May  6 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.0.1-2
- Add disttag to Release

* Fri Apr  8 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.0.1-2
- Remove -Werror from configure for now
- Fix .desktop file to have Terminal=false instead of 0

* Thu Mar 24 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 1.0.1-1
- Upstream update
- Separated ortp
- Added %%doc

* Wed Mar 23 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.12.2-7
- pkgconfig and -devel fixes

* Wed Mar 23 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.12.2-6
- Fix build on x86_64

* Sat Mar 19 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.12.2-5
- %%

* Sat Mar 19 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.12.2-4
- Used %%find_lang
- Tightened up %%files
- Streamlined spec file

* Thu Mar 17 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.12.2-3
- Broke %%description at 80 columns

* Wed Mar 16 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.12.2-2
- Removed explicit Requires

* Tue Mar 15 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0.12.2-1
- Bump release to 1
- Cleaned up the -docs and -speex patches

* Fri Jan 21 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0:0.12.2-0.iva.1
- Fixed a silly spec error

* Fri Jan 21 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0:0.12.2-0.iva.0
- Initial RPM release.
