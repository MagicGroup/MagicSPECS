%define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")

%define with_adns 0
%define with_lua 1
%if 0%{?rhel} != 0
%define with_portaudio 0
%else
%define with_portaudio 1
%endif

Summary:	Network traffic analyzer
Name:		wireshark
Version:	1.6.5
Release:	2%{?dist}
License:	GPL+
Group:		Applications/Internet
Source0:	http://wireshark.org/download/src/%{name}-%{version}.tar.bz2
Source2:	wireshark.console
Source3:	wireshark.desktop
Source4:	wireshark-autoconf.m4
Source5:	wireshark-mime-package.xml
Source6:	wiresharkdoc-16x16.png
Source7:	wiresharkdoc-32x32.png
Source8:	wiresharkdoc-48x48.png
Source9:	wiresharkdoc-256x256.png

Patch1:		wireshark-nfsv41-cleanup.patch
Patch2:		wireshark-1.2.4-enable_lua.patch
Patch3:		wireshark-libtool-pie.patch
Patch4:		wireshark-1.6.1-group-msg.patch
Patch5:		wireshark-1.6.0-soname.patch
Patch6:		wireshark-1.6.2-nfsv41-addstatus.patch
Patch7:		wireshark-gnome3-msgbox.patch

Url:		http://www.wireshark.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	libpcap-devel >= 0.9
BuildRequires:	libsmi-devel
BuildRequires:	zlib-devel, bzip2-devel
BuildRequires:	openssl-devel
BuildRequires:	glib2-devel, gtk2-devel
BuildRequires:	elfutils-devel, krb5-devel
BuildRequires:	python, pcre-devel
BuildRequires:	gnutls-devel
BuildRequires:	desktop-file-utils
BuildRequires:	xdg-utils
BuildRequires:	flex, bison, python, python-devel
BuildRequires:	GeoIP-devel
BuildRequires:	libcap-devel
%if %{with_adns}
BuildRequires:	adns-devel
%else
BuildRequires:	c-ares-devel
%endif
%if %{with_portaudio}
BuildRequires:	portaudio-devel
%endif
%if %{with_lua}
BuildRequires:	lua-devel
%endif

Requires(pre):	shadow-utils
%if %{with_adns}
Requires:	adns
%endif

%package	gnome
Summary:	Gnome desktop integration for wireshark
Group:		Applications/Internet
Requires:	gtk2
Requires:	wireshark = %{version}-%{release}
Requires:	xdg-utils
Requires:	GeoIP
Requires:	hicolor-icon-theme

%if %{with_portaudio}
Requires:	portaudio
%endif

%package devel
Summary:	Development headers and libraries for wireshark
Group:		Development/Libraries
Requires:	%{name} = %{version} glibc-devel glib2-devel


%description
Wireshark is a network traffic analyzer for Unix-ish operating systems.

This package lays base for libpcap, a packet capture and filtering 
library, contains command-line utilities, contains plugins and 
documentation for wireshark. A graphical user interface is packaged 
separately to GTK+ package.

%description gnome
Contains wireshark for Gnome 2 and desktop integration file

%description devel
The wireshark-devel package contains the header files, developer
documentation, and libraries required for development of wireshark scripts
and plugins.


%prep
%setup -q -n %{name}-%{version}
# disable NFS patch for now, remove if steved@redhat.com does not complain
#%patch1 -p1 

%if %{with_lua}
%patch2 -p1 -b .enable_lua
%endif

%patch3 -p1 -b .v4cleanup
%patch4 -p1 -b .group-msg
%patch5 -p1 -b .soname
%patch6 -p1 -b .v4staus
%patch7 -p1 -b .gnome3

%build
%ifarch s390 s390x sparcv9 sparc64
export PIECFLAGS="-fPIE"
%else
export PIECFLAGS="-fpie"
%endif
# FC5+ automatic -fstack-protector-all switch
export RPM_OPT_FLAGS=${RPM_OPT_FLAGS//-fstack-protector/-fstack-protector-all}
export CFLAGS="$RPM_OPT_FLAGS $CPPFLAGS $PIECFLAGS -D_LARGEFILE64_SOURCE"
export CXXFLAGS="$RPM_OPT_FLAGS $CPPFLAGS $PIECFLAGS -D_LARGEFILE64_SOURCE"
export LDFLAGS="$LDFLAGS -pie"

%configure \
   --bindir=%{_sbindir} \
   --enable-ipv6 \
   --with-libsmi \
   --with-gnu-ld \
   --with-pic \
%if %{with_adns}
   --with-adns \
%else
   --with-adns=no \
%endif
%if %{with_lua}
   --with-lua \
%else
   --with-lua=no \
%endif
   --with-ssl \
   --disable-warnings-as-errors \
   --with-python \
   --with-plugins=%{_libdir}/%{name}/plugins/%{version} \
   --with-dumpcap-group="wireshark" \
   --enable-setcap-install \
   --enable-airpcap

#remove rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

# The evil plugins hack
perl -pi -e 's|-L../../epan|-L../../epan/.libs|' plugins/*/*.la

make DESTDIR=$RPM_BUILD_ROOT install

# Install python stuff.
mkdir -p $RPM_BUILD_ROOT%{python_sitearch}
install -m 644 tools/wireshark_be.py tools/wireshark_gen.py  $RPM_BUILD_ROOT%{python_sitearch}

desktop-file-install --vendor fedora				\
	--dir ${RPM_BUILD_ROOT}%{_datadir}/applications		\
	--add-category X-Fedora					\
	%{SOURCE3}

mkdir -p $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/{16x16,32x32,48x48,64x64,256x256}/apps

install -m 644 image/wsicon16.png $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/16x16/apps/wireshark.png
install -m 644 image/wsicon32.png $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/32x32/apps/wireshark.png
install -m 644 image/wsicon48.png $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/48x48/apps/wireshark.png
install -m 644 image/wsicon64.png $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/64x64/apps/wireshark.png
install -m 644 image/wsicon256.png $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/256x256/apps/wireshark.png

#install devel files (inspired by debian/wireshark-dev.header-files)
install -d -m 0755  $RPM_BUILD_ROOT/%{_includedir}/wireshark
IDIR="${RPM_BUILD_ROOT}%{_includedir}/wireshark"
mkdir -p "${IDIR}/epan"
mkdir -p "${IDIR}/epan/crypt"
mkdir -p "${IDIR}/epan/ftypes"
mkdir -p "${IDIR}/epan/dfilter"
mkdir -p "${IDIR}/epan/dissectors"
mkdir -p "${IDIR}/wiretap"
mkdir -p "${IDIR}/wsutil"
install -m 644 color.h config.h register.h	"${IDIR}/"
install -m 644 cfile.h file.h			"${IDIR}/"
install -m 644 packet-range.h print.h   	"${IDIR}/"
install -m 644 epan/*.h				"${IDIR}/epan/"
install -m 644 epan/crypt/*.h			"${IDIR}/epan/crypt"
install -m 644 epan/ftypes/*.h			"${IDIR}/epan/ftypes"
install -m 644 epan/dfilter/*.h			"${IDIR}/epan/dfilter"
install -m 644 epan/dissectors/*.h		"${IDIR}/epan/dissectors"
install -m 644 wiretap/*.h			"${IDIR}/wiretap"
install -m 644 wsutil/*.h			"${IDIR}/wsutil"

#	Create pkg-config control file.
mkdir -p "${RPM_BUILD_ROOT}%{_libdir}/pkgconfig"
cat > "${RPM_BUILD_ROOT}%{_libdir}/pkgconfig/wireshark.pc" <<- "EOF"
	prefix=%{_prefix}
	exec_prefix=%{_prefix}
	libdir=%{_libdir}
	includedir=%{_includedir}

	Name:		%{name}
	Description:	Network Traffic Analyzer
	Version:	%{version}
	Requires:	glib-2.0 gmodule-2.0
	Libs:		-L${libdir} -lwireshark -lwiretap
	Cflags:		-DWS_VAR_IMPORT=extern -DHAVE_STDARG_H -DWS_MSVC_NORETURN= -I${includedir}/wireshark -I${includedir}/wireshark/epan
EOF

#	Install the autoconf macro.
mkdir -p "${RPM_BUILD_ROOT}%{_datadir}/aclocal"
cp "%{SOURCE4}" "${RPM_BUILD_ROOT}%{_datadir}/aclocal/wireshark.m4"

# Install desktop stuff
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/{icons/gnome/{16x16,32x32,48x48,256x256}/mimetypes,mime/packages}
install -m 644 -T %{SOURCE5} $RPM_BUILD_ROOT/%{_datadir}/mime/packages/wireshark.xml
install -m 644 -T %{SOURCE6} $RPM_BUILD_ROOT/%{_datadir}/icons/gnome/16x16/mimetypes/application-x-pcap.png
install -m 644 -T %{SOURCE7} $RPM_BUILD_ROOT/%{_datadir}/icons/gnome/32x32/mimetypes/application-x-pcap.png
install -m 644 -T %{SOURCE8} $RPM_BUILD_ROOT/%{_datadir}/icons/gnome/48x48/mimetypes/application-x-pcap.png
install -m 644 -T %{SOURCE9} $RPM_BUILD_ROOT/%{_datadir}/icons/gnome/256x256/mimetypes/application-x-pcap.png

# Remove .la files
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{name}/plugins/%{version}/*.la

# Remove .la files in libdir
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la

# add wspy_dissectors directory for plugins
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/%{name}/python/%{version}/wspy_dissectors

%clean
rm -rf $RPM_BUILD_ROOT

%pre
getent group wireshark >/dev/null || groupadd -r wireshark

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post gnome
update-desktop-database &> /dev/null ||:
update-mime-database %{_datadir}/mime &> /dev/null || :
touch --no-create %{_datadir}/icons/gnome &>/dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun gnome
update-desktop-database &> /dev/null ||:
update-mime-database %{_datadir}/mime &> /dev/null || :
if [ $1 -eq 0 ] ; then
	touch --no-create %{_datadir}/icons/gnome &>/dev/null
	gtk-update-icon-cache %{_datadir}/icons/gnome &>/dev/null || :

	touch --no-create %{_datadir}/icons/hicolor &>/dev/null
	gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/gnome &>/dev/null || :
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README* 
%{_sbindir}/editcap
#%{_sbindir}/idl2wrs
%{_sbindir}/tshark
%{_sbindir}/mergecap
%{_sbindir}/text2pcap
%{_sbindir}/dftest
%{_sbindir}/capinfos
%{_sbindir}/randpkt
%attr(0750, root, wireshark) %caps(cap_net_raw,cap_net_admin=eip) %{_sbindir}/dumpcap
%{_sbindir}/rawshark
%{python_sitearch}/*.py*
%{_libdir}/lib*.so.*
%{_libdir}/wireshark
%{_mandir}/man1/editcap.*
%{_mandir}/man1/tshark.*
%{_mandir}/man1/mergecap.*
%{_mandir}/man1/text2pcap.*
%{_mandir}/man1/capinfos.*
%{_mandir}/man1/dumpcap.*
%{_mandir}/man4/wireshark-filter.*
%{_mandir}/man1/rawshark.*
%{_mandir}/man1/dftest.*
%{_mandir}/man1/randpkt.*
%{_datadir}/wireshark
%if %{with_lua}
%exclude %{_datadir}/wireshark/init.lua
%endif


%files gnome
%defattr(-,root,root)
%{_datadir}/applications/fedora-wireshark.desktop
%{_datadir}/icons/hicolor/16x16/apps/wireshark.png
%{_datadir}/icons/hicolor/32x32/apps/wireshark.png
%{_datadir}/icons/hicolor/48x48/apps/wireshark.png
%{_datadir}/icons/hicolor/64x64/apps/wireshark.png
%{_datadir}/icons/hicolor/256x256/apps/wireshark.png
%{_datadir}/icons/gnome/16x16/mimetypes/application-x-pcap.png
%{_datadir}/icons/gnome/32x32/mimetypes/application-x-pcap.png
%{_datadir}/icons/gnome/48x48/mimetypes/application-x-pcap.png
%{_datadir}/icons/gnome/256x256/mimetypes/application-x-pcap.png
%{_datadir}/mime/packages/wireshark.xml
%{_sbindir}/wireshark
%{_mandir}/man1/wireshark.*

%files devel
%defattr(-,root,root)
%doc doc/README.*
%config(noreplace) %{_datadir}/wireshark/init.lua
%{_includedir}/wireshark
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_datadir}/aclocal/*
%{_mandir}/man1/idl2wrs.*
%{_sbindir}/idl2wrs

%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 1.6.5-2
- 为 Magic 3.0 重建

* Wed Jan 11 2012 Jan Safranek <jsafrane@redhat.com> - 1.6.5-1
- upgrade to 1.6.5
- see http://www.wireshark.org/docs/relnotes/wireshark-1.6.5.html

* Fri Dec  2 2011 Jan Safranek <jsafrane@redhat.com> - 1.6.4-1
- upgrade to 1.6.4
- see http://www.wireshark.org/docs/relnotes/wireshark-1.6.4.html
- build with c-ares and libpcap (#759305)
- fixed display of error message boxes on startup in gnome3 (#752559)

* Mon Nov 14 2011 Jan Safranek <jsafrane@redhat.com> - 1.6.3-2
- added dependency on shadow-utils (#753293)
- removed usermode support

* Wed Nov  2 2011 Jan Safranek <jsafrane@redhat.com> - 1.6.3-1
- upgrade to 1.6.3
- see http://www.wireshark.org/docs/relnotes/wireshark-1.6.3.html

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-5
- Rebuilt for glibc bug#747377

* Fri Oct 21 2011 Jan Safranek <jsafrane@redhat.com> - 1.6.2-4
- updated autoconf macros and pkgconfig file in wireshark-devel to reflect
  current config.h (#746655)

* Mon Oct 17 2011 Steve Dickson <steved@redhat.com> - 1.6.2-3
- Fixed a regression introduce by upstream patch r38306
    which caused v4.1 traffic not to be displayed.
- Added v4 error status to packet detail window.

* Tue Sep 13 2011 Jan Safranek <jsafrane@redhat.com> - 1.6.2-2
- fixed spelling of the security message (#737270)

* Fri Sep  9 2011 Jan Safranek <jsafrane@redhat.com> - 1.6.2-1
- upgrade to 1.6.2
- see http://www.wireshark.org/docs/relnotes/wireshark-1.6.2.html

* Thu Jul 21 2011 Jan Safranek <jsafrane@redhat.com> - 1.6.1-1
- upgrade to 1.6.1
- see http://www.wireshark.org/docs/relnotes/wireshark-1.6.1.html

* Thu Jun 16 2011 Jan Safranek <jsafrane@redhat.com> - 1.6.0-4
- fixed previous incomplete fix

* Thu Jun 16 2011 Jan Safranek <jsafrane@redhat.com> - 1.6.0-3
- fixed Fedora-specific message when user is not part of 'wireshark' group
  - now it does not contain '<' and '>' characters (#713545)

* Thu Jun  9 2011 Jan Safranek <jsafrane@redhat.com> - 1.6.0-2
- added wspy_dissectors directory to the package
  - other packages can add Python plugins there
  - as side effect, removed following message:
    [Errno 2] No such file or directory: '/usr/lib64/wireshark/python/1.6.0/wspy_dissectors'
- enabled zlib support

* Wed Jun  8 2011 Jan Safranek <jsafrane@redhat.com> - 1.6.0-1
- upgrade to 1.6.0
- see http://www.wireshark.org/docs/relnotes/wireshark-1.6.0.html

* Thu Jun  2 2011 Jan Safranek <jsafrane@redhat.com> - 1.4.7-1
- upgrade to 1.4.7
- see http://www.wireshark.org/docs/relnotes/wireshark-1.4.7.html

* Thu May 19 2011 Steve Dickson <steved@redhat.com> - 1.4.6-3
- Improved the NFS4.1 patcket dissectors 

* Sat May 07 2011 Christopher Aillon <caillon@redhat.com> - 1.4.6-2
- Update icon cache scriptlet

* Tue Apr 19 2011 Jan Safranek <jsafrane@redhat.com> - 1.4.6-1
- upgrade to 1.4.6
- see http://www.wireshark.org/docs/relnotes/wireshark-1.4.6.html

* Mon Apr 18 2011 Jan Safranek <jsafrane@redhat.com> - 1.4.5-1
- upgrade to 1.4.5
- see http://www.wireshark.org/docs/relnotes/wireshark-1.4.5.html

* Sun Apr 03 2011 Cosimo Cecchi <cosimoc@redhat.com> - 1.4.4-2
- Use hi-res icons

* Thu Mar  3 2011 Jan Safranek <jsafrane@redhat.com> - 1.4.4-1
- upgrade to 1.4.4
- see http://www.wireshark.org/docs/relnotes/wireshark-1.4.4.html

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Jan Safranek <jsafrane@redhat.com> - 1.4.3-2
- create the 'wireshark' group as system, not user
- add few additional header files to -devel subpackage (#671997)

* Thu Jan 13 2011 Jan Safranek <jsafrane@redhat.com> - 1.4.3-1
- upgrade to 1.4.3
- see http://www.wireshark.org/docs/relnotes/wireshark-1.4.3.html

* Wed Jan  5 2011 Jan Safranek <jsafrane@redhat.com> - 1.4.2-5
- fixed buffer overflow in ENTTEC dissector (#666897)

* Wed Dec 15 2010 Jan Safranek <jsafrane@redhat.com> - 1.4.2-4
- added epan/dissectors/*.h to -devel subpackage (#662969)

* Mon Dec  6 2010 Jan Safranek <jsafrane@redhat.com> - 1.4.2-3
- fixed generation of man pages again (#635878)

* Fri Nov 26 2010 Jan Safranek <jsafrane@redhat.com> - 1.4.2-2
- rework the Wireshark security (#657490). Remove the console helper and
  allow only members of new 'wireshark' group to capture the packets.

* Mon Nov 22 2010 Jan Safranek <jsafrane@redhat.com> - 1.4.2-1
- upgrade to 1.4.2
- see http://www.wireshark.org/docs/relnotes/wireshark-1.4.2.html

* Mon Nov  1 2010 Jan Safranek <jsafrane@redhat.com> - 1.4.1-2
- temporarily disable zlib until
  https://bugs.wireshark.org/bugzilla/show_bug.cgi?id=4955 is resolved (#643461)
  
* Fri Oct 22 2010 Jan Safranek <jsafrane@redhat.com> - 1.4.1-1
- upgrade to 1.4.1
- see http://www.wireshark.org/docs/relnotes/wireshark-1.4.1.html
- Own the %%{_libdir}/wireshark dir (#644508)
- associate *.pcap files with wireshark (#641163)

* Wed Sep 29 2010 jkeating - 1.4.0-2
- Rebuilt for gcc bug 634757

* Fri Sep 24 2010 Jan Safranek <jsafrane@redhat.com> - 1.4.0-2
- fixed generation of man pages (#635878)

* Tue Aug 31 2010 Jan Safranek <jsafrane@redhat.com> - 1.4.0-1
- upgrade to 1.4.0
- see http://www.wireshark.org/docs/relnotes/wireshark-1.4.0.html

* Fri Jul 30 2010 Jan Safranek <jsafrane@redhat.com> - 1.2.10-1
- upgrade to 1.2.10
- see http://www.wireshark.org/docs/relnotes/wireshark-1.2.10.html

* Fri Jul 30 2010 Jan Safranek <jsafrane@redhat.com> - 1.2.9-4
- Rebuilt again for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jul 22 2010 Jan Safranek <jsafrane@redhat.com> - 1.2.9-3
- removing useless LDFLAGS (#603224)

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jun 11 2010 Radek Vokal <rvokal@redhat.com> - 1.2.9-1
- upgrade to 1.2.9
- see http://www.wireshark.org/docs/relnotes/wireshark-1.2.9.html

* Mon May 17 2010 Radek Vokal <rvokal@redhat.com> - 1.2.8-4
- removing traling bracket from python_sitearch (#592391)

* Fri May  7 2010 Radek Vokal <rvokal@redhat.com> - 1.2.8-3
- fix patched applied without fuzz=0

* Thu May  6 2010 Radek Vokal <rvokal@redhat.com> - 1.2.8-2
- use sitearch instead of sitelib to avoid pyo and pyc conflicts

* Thu May  6 2010 Radek Vokal <rvokal@redhat.com> - 1.2.8-1
- upgrade to 1.2.8
- see http://www.wireshark.org/docs/relnotes/wireshark-1.2.8.html

* Tue Apr  6 2010 Radek Vokal <rvokal@redhat.com> - 1.2.7-2
- rebuild with GeoIP support (needs to be turned on in IP protocol preferences)

* Fri Apr  2 2010 Radek Vokal <rvokal@redhat.com> - 1.2.7-1
- upgrade to 1.2.7
- see http://www.wireshark.org/docs/relnotes/wireshark-1.2.7.html 

* Wed Mar 24 2010 Radek Vokal <rvokal@redhat.com> - 1.2.6-3
- bring back -pie

* Tue Mar 16 2010 Jeff Layton <jlayton@redhat.com> - 1.2.6-2
- add patch to allow decode of NFSv4.0 callback channel
- add patch to allow decode of more SMB FIND_FILE infolevels

* Fri Jan 29 2010 Radek Vokal <rvokal@redhat.com> - 1.2.6-1
- upgrade to 1.2.6
- see http://www.wireshark.org/docs/relnotes/wireshark-1.2.6.html 

* Wed Jan 20 2010 Radek Vokal <rvokal@redhat.com> - 1.2.5-5
- minor spec file tweaks for better svn checkout support (#553500)

* Tue Jan 05 2010 Radek Vokál <rvokal@redhat.com> - 1.2.5-4
- init.lua is present always and not only when lua support is enabled

* Tue Jan 05 2010 Radek Vokál <rvokal@redhat.com> - 1.2.5-3
- fix file list, init.lua is only in -devel subpackage (#552406)

* Fri Dec 18 2009 Patrick Monnerat <pm@datasphere.ch> 1.2.5-2
- Autoconf macro for plugin development.

* Fri Dec 18 2009 Radek Vokal <rvokal@redhat.com> - 1.2.5-1
- upgrade to 1.2.5
- fixes security vulnaribilities, see http://www.wireshark.org/security/wnpa-sec-2009-09.html 

* Thu Dec 17 2009 Radek Vokal <rvokal@redhat.com> - 1.2.4-3
- split -devel package (#547899, #203642, #218451)
- removing root warning dialog (#543709)

* Mon Dec 14 2009 Radek Vokal <rvokal@redhat.com> - 1.2.4-2
- enable lua support - http://wiki.wireshark.org/Lua
- attempt to fix filter crash on 64bits

* Wed Nov 18 2009 Radek Vokal <rvokal@redhat.com> - 1.2.4-1
- upgrade to 1.2.4
- http://www.wireshark.org/docs/relnotes/wireshark-1.2.4.html

* Fri Oct 30 2009 Radek Vokal <rvokal@redhat.com> - 1.2.3-1
- upgrade to 1.2.3
- http://www.wireshark.org/docs/relnotes/wireshark-1.2.3.html

* Mon Sep 21 2009 Radek Vokal <rvokal@redhat.com> - 1.2.2-1
- upgrade to 1.2.2
- http://www.wireshark.org/docs/relnotes/wireshark-1.2.2.html

* Mon Sep 14 2009 Bill Nottingham <notting@redhat.com> - 1.2.1-5
- do not use portaudio in RHEL

* Fri Aug 28 2009 Radek Vokal <rvokal@redhat.com> - 1.2.1-4
- yet anohter rebuilt

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.2.1-3
- rebuilt with new openssl

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Radek Vokal <rvokal@redhat.com> - 1.2.1
- upgrade to 1.2.1
- http://www.wireshark.org/docs/relnotes/wireshark-1.2.1.html

* Tue Jun 16 2009 Radek Vokal <rvokal@redhat.com> - 1.2.0
- upgrade to 1.2.0
- http://www.wireshark.org/docs/relnotes/wireshark-1.2.0.html

* Fri May 22 2009 Radek Vokal <rvokal@redhat.com> - 1.1.4-0.pre1
- update to latest development build

* Thu Mar 26 2009 Radek Vokal <rvokal@redhat.com> - 1.1.3-1
- upgrade to 1.1.3

* Thu Mar 26 2009 Radek Vokal <rvokal@redhat.com> - 1.1.2-4.pre1
- fix libsmi support

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-3.pre1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Radek Vokal <rvokal@redhat.com> - 1.1.2-2.pre1
- add netdump support

* Sun Feb 15 2009 Steve Dickson <steved@redhat.com> - 1.1.2-1.pre1
- NFSv4.1: Add support for backchannel decoding

* Mon Jan 19 2009 Radek Vokal <rvokal@redhat.com> - 1.1.2-0.pre1
- upgrade to latest development release
- added support for portaudio (#480195)

* Sun Jan 18 2009 Tomas Mraz <tmraz@redhat.com> - 1.1.1-0.pre1.2
- rebuild with new openssl

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.1.1-0.pre1.1
- Rebuild for Python 2.6

* Thu Nov 13 2008 Radek Vokál <rvokal@redhat.com> 1.1.1-0.pre1
- upgrade to 1.1.1 development branch

* Wed Sep 10 2008 Radek Vokál <rvokal@redhat.com> 1.0.3-1
- upgrade to 1.0.3
- Security-related bugs in the NCP dissector, zlib compression code, and Tektronix .rf5 file parser have been fixed. 
- WPA group key decryption is now supported. 
- A bug that could cause packets to be wrongly dissected as "Redback Lawful Intercept" has been fixed. 

* Mon Aug 25 2008 Radek Vokál <rvokal@redhat.com> 1.0.2-3
- fix requires for wireshark-gnome

* Thu Jul 17 2008 Steve Dickson <steved@redhat.com> 1.0.2-2
- Added patches to support NFSv4.1

* Fri Jul 11 2008 Radek Vokál <rvokal@redhat.com> 1.0.2-1
- upgrade to 1.0.2

* Tue Jul  8 2008 Radek Vokál <rvokal@redhat.com> 1.0.1-1
- upgrade to 1.0.1

* Sun Jun 29 2008 Dennis Gilmore <dennis@ausil.us> 1.0.0-3
- add sparc arches to -fPIE 
- rebuild for new gnutls

* Tue Apr  1 2008 Radek Vokál <rvokal@redhat.com> 1.0.0-2
- fix BuildRequires - python, yacc, bison

* Tue Apr  1 2008 Radek Vokál <rvokal@redhat.com> 1.0.0-1
- April Fools' day upgrade to 1.0.0

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.99.7-3
- Autorebuild for GCC 4.3

* Wed Dec 19 2007 Radek Vokál <rvokal@redhat.com> 0.99.7-2
- fix crash in unprivileged mode (#317681)

* Tue Dec 18 2007 Radek Vokál <rvokal@redhat.com> 0.99.7-1
- upgrade to 0.99.7

* Fri Dec  7 2007 Radek Vokál <rvokal@redhat.com> 0.99.7-0.pre2.1
- rebuilt for openssl

* Mon Nov 26 2007 Radek Vokal <rvokal@redhat.com> 0.99.7-0.pre2
- switch to libsmi from net-snmp
- disable ADNS due to its lack of Ipv6 support
- 0.99.7 prerelease 2

* Tue Nov 20 2007 Radek Vokal <rvokal@redhat.com> 0.99.7-0.pre1
- upgrade to 0.99.7 pre-release

* Wed Sep 19 2007 Radek Vokál <rvokal@redhat.com> 0.99.6-3
- fixed URL

* Thu Aug 23 2007 Radek Vokál <rvokal@redhat.com> 0.99.6-2
- rebuilt

* Mon Jul  9 2007 Radek Vokal <rvokal@redhat.com> 0.99.6-1
- upgrade to 0.99.6 final

* Fri Jun 15 2007 Radek Vokál <rvokal@redhat.com> 0.99.6-0.pre2
- another pre-release
- turn on ADNS support

* Wed May 23 2007 Radek Vokál <rvokal@redhat.com> 0.99.6-0.pre1
- update to pre1 of 0.99.6 release

* Mon Feb  5 2007 Radek Vokál <rvokal@redhat.com> 0.99.5-1
- multiple security issues fixed (#227140)
- CVE-2007-0459 - The TCP dissector could hang or crash while reassembling HTTP packets
- CVE-2007-0459 - The HTTP dissector could crash.
- CVE-2007-0457 - On some systems, the IEEE 802.11 dissector could crash.
- CVE-2007-0456 - On some systems, the LLT dissector could crash.

* Mon Jan 15 2007 Radek Vokal <rvokal@redhat.com> 0.99.5-0.pre2
- another 0.99.5 prerelease, fix build bug and pie flags

* Tue Dec 12 2006 Radek Vokal <rvokal@redhat.com> 0.99.5-0.pre1
- update to 0.99.5 prerelease

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 0.99.4-5
- rebuild for python 2.5 

* Tue Nov 28 2006 Radek Vokal <rvokal@redhat.com> 0.99.4-4
- rebuilt for new libpcap and net-snmp

* Thu Nov 23 2006 Radek Vokal <rvokal@redhat.com> 0.99.4-3
- add htmlview to Buildrequires to be picked up by configure scripts (#216918)

* Tue Nov  7 2006 Radek Vokal <rvokal@redhat.com> 0.99.4-2.fc7
- Requires: net-snmp for the list of MIB modules 

* Wed Nov  1 2006 Radek Vokál <rvokal@redhat.com> 0.99.4-1
- upgrade to 0.99.4 final

* Tue Oct 31 2006 Radek Vokál <rvokal@redhat.com> 0.99.4-0.pre2
- upgrade to 0.99.4pre2

* Tue Oct 10 2006 Radek Vokal <rvokal@redhat.com> 0.99.4-0.pre1
- upgrade to 0.99.4-0.pre1

* Fri Aug 25 2006 Radek Vokál <rvokal@redhat.com> 0.99.3-1
- upgrade to 0.99.3
- Wireshark 0.99.3 fixes the following vulnerabilities:
- the SCSI dissector could crash. Versions affected: CVE-2006-4330
- the IPsec ESP preference parser was susceptible to off-by-one errors. CVE-2006-4331
- a malformed packet could make the Q.2931 dissector use up available memory. CVE-2006-4333 

* Tue Jul 18 2006 Radek Vokál <rvokal@redhat.com> 0.99.2-1
- upgrade to 0.99.2

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.99.2-0.pre1.1
- rebuild

* Tue Jul 11 2006 Radek Vokál <rvokal@redhat.com> 0.99.2-0.pre1
- upgrade to 0.99.2pre1, fixes (#198242)

* Tue Jun 13 2006 Radek Vokal <rvokal@redhat.com> 0.99.1-0.pre1
- spec file changes

* Fri Jun  9 2006 Radek Vokal <rvokal@redhat.com> 0.99.1pre1-1
- initial build for Fedora Core
