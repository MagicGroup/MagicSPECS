# TODO:
# - --enable-tunnel (BR: pkgconfig(tunnel) >= 0.3.3)
# - fill in dependencies for !system_ortp, !system_mediastreamer
# - check if all this configure option I've set are really needed
# - separate libraries that do not require gnome into subpackages for Jingle support in kopete
# - if system_mediastreamerpackages copies for "libmediastreamer.so.1", "libortp.so.8" libraries
#   those should be installed to private path and LD_LIBARY_PATH setup with wrappers.
#   without doing so do not stbr it to Th!
#
# Conditional build:
%bcond_without	ldap			# LDAP support
%bcond_without	openssl			# SSL support
%bcond_without	system_ortp		# use custom ortp
%bcond_without	system_mediastreamer	# use custom mediastreamer


Name:           linphone
Version:	3.7.0
Release:        6%{?dist}
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

BuildRequires:	belle-sip-devel

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

%if %{without system_ortp}
%define		_noautoreq_1	libortp\.so.*
%endif
%if %{without system_mediastreamer}
%define		_noautoreq_2	libmediastreamer\.so.*
%endif

%filter_requires_in %{?_noautoreq_1} %{?_noautoreq_2}
%filter_provides_in %{?_noautoreq_1} %{?_noautoreq_2}

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
Requires:       mediastreamer-devel%{?_isa} >= 2.10.0
Requires:       glib2-devel%{?_isa}

%description    devel
Libraries and headers required to develop software with linphone.

%package -n linphonec
Summary:	Linphone Internet Phone console interface
Group:		Applications/Communications
Requires:	%{name}-libs = %{version}-%{release}

%description -n linphonec
Linphonec is the console version of originally GNOME Internet phone
Linphone.

%package libs
Summary:	Linphone libraries
Group:		Libraries
Requires(post,postun):	/sbin/ldconfig
Requires:	belle-sip >= 1.3.0
Requires:	libsoup-devel >= 2.26
%{?with_system_mediastreamer:Requires:	mediastreamer%{?_isa} >= 2.10.0}
%{?with_system_ortp:Requires:	ortp%{?_isa} >= 0.23.0}
Requires:	sqlite >= 3.7.0

%description libs
Linphone libraries.


%package static
Summary:	Linphone static libraries
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static version of Linphone libraries.

%prep
%setup0 -q
%patch0 -p1 -b .rootca
%ifarch %{arm}
%patch1 -p1 -b .arm
%endif

autoreconf -i -f

find '(' -name '*.c' -o -name '*.h' ')' -print0 | xargs -0 %{__sed} -i -e 's,\r$,,'

%if %{without system_ortp}
cd oRTP
autoreconf -fisv
cd ..
%else
# remove bundled oRTP
rm -rf oRTP
%endif

%if %{without system_ortp}
cd mediastreamer2
autoreconf -fisv
cd ..
%else
rm -rf mediastreamer2
%endif

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
%configure \
	--with-html-dir=%{_gtkdocdir} \
	--enable-alsa \
	%{?with_system_mediastreamer:--enable-external-mediastreamer} \
	%{?with_system_ortp:--enable-external-ortp} \
	--enable-ipv6 \
	%{?with_ldap:--enable-ldap} \
	--disable-silent-rules \
	%{?with_openssl:--enable-ssl} \
	--enable-static \
	--disable-strict

# although main configure already calls {oRTP,mediastreamer2}/configure,
# reconfigure them with different dirs
%if %{without system_ortp}
cd oRTP
%configure \
	--enable-static \
	--enable-ipv6 \
	--libdir=%{_libdir}/%{name} \
	--includedir=%{_libdir}/%{name}/include
cd ..
%endif
%if %{without system_ortp}
cd mediastreamer2
%configure \
	--enable-static \
	--disable-libv4l \
	--libdir=%{_libdir}/%{name} \
	--includedir=%{_libdir}/%{name}/include
cd ..
%endif

make %{?_smp_mflags} \
	GITDESCRIBE=/bin/true \
	GIT_TAG=%{version}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	GITDESCRIBE=/bin/true \
	GIT_TAG=%{version} \
	DESTDIR=$RPM_BUILD_ROOT

install pixmaps/%{name}.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
%{!?with_system_mediastreamer:%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/mediastreamer}
%{!?with_system_ortp:%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/ortp}

# the executable is missing, so the manual is useless
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/sipomatic.1*
%{__rm} $RPM_BUILD_ROOT%{_mandir}/cs/man1/sipomatic.1*

# some tests
%{__rm} $RPM_BUILD_ROOT%{_bindir}/*_test

install -d $RPM_BUILD_ROOT%{_examplesdir}
mv $RPM_BUILD_ROOT%{_datadir}/tutorials/%{name} $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
magic_rpm_clean.sh
%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_bindir}/scrollkeeper-update

%if %{without system_mediastreamer} || %{without system_ortp}
%post libs
/sbin/ldconfig %{_libdir}/%{name}
%else
%post libs -p /sbin/ldconfig
%endif

%postun
%{_bindir}/scrollkeeper-update

%postun libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/linphone
%{_datadir}/applications/linphone.desktop
%{_datadir}/pixmaps/linphone.png
%{_datadir}/pixmaps/linphone/*
%{_datadir}/linphone
%{_mandir}/man1/linphone.1*

%files -n linphonec
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/linphonec
%attr(755,root,root) %{_bindir}/linphonecsh
%{_mandir}/man1/linphonec.1*
%{_mandir}/man1/linphonecsh.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblinphone.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblinphone.so.6
%if %{without system_mediastreamer} || %{without system_ortp}
%dir %{_libdir}/%{name}
%endif
%if %{without system_mediastreamer}
%attr(755,root,root) %{_libdir}/%{name}/libmediastreamer.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/%{name}/libmediastreamer.so.?
%{_libdir}/%{name}/mediastream
%endif
%if %{without system_ortp}
%attr(755,root,root) %{_libdir}/%{name}/libortp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/%{name}/libortp.so.?
%endif
%{_datadir}/sounds/linphone

%files devel
%defattr(644,root,root,755)
%doc coreapi/help/doc/html
%attr(755,root,root) %{_libdir}/liblinphone.so
%attr(755,root,root) %{_bindir}/lp-gen-wrappers
%{_includedir}/linphone
%{_libdir}/pkgconfig/linphone.pc
%{_libdir}/liblinphone.la
%if %{without system_mediastreamer} || %{without system_ortp}
%dir %{_libdir}/%{name}/include
%dir %{_libdir}/%{name}/pkgconfig
%endif
%if %{without system_mediastreamer}
%attr(755,root,root) %{_libdir}/%{name}/libmediastreamer.so
%{_libdir}/%{name}/libmediastreamer.la
%{_libdir}/%{name}/include/mediastreamer2
%{_libdir}/%{name}/pkgconfig/mediastreamer.pc
%endif
%if %{without system_ortp}
%attr(755,root,root) %{_libdir}/%{name}/libortp.so
%{_libdir}/%{name}/libortp.la
%{_libdir}/%{name}/include/ortp
%{_libdir}/%{name}/pkgconfig/ortp.pc
%endif
#%{_datadir}/exmaples/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/liblinphone.a
%if %{without system_mediastreamer}
%{_libdir}/%{name}/libmediastreamer.a
%endif
%if %{without system_ortp}
%{_libdir}/%{name}/libortp.a
%endif

%changelog
* Tue Jun 24 2014 Liu Di <liudidi@gmail.com> - 3.7.0-6
- 为 Magic 3.0 重建

* Tue Jun 24 2014 Liu Di <liudidi@gmail.com> - 3.7.0-5
- 为 Magic 3.0 重建

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
