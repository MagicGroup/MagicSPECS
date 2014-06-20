%global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")

%global with_adns 0
%global with_lua 1
%global with_gtk2 1

%if 0%{?rhel} != 0
#RHEL:
    %global with_portaudio 0
    %global with_GeoIP 0
    %if 0%{?rhel} <= 6
        # RHEL6: use GTK2
       %global with_gtk2 1
    %endif
%else
    %global with_portaudio 1
    %global with_GeoIP 1
%endif


Summary:	Network traffic analyzer
Name:		wireshark
Version:	1.10.8
Release:	1%{?dist}
License:	GPL+
Group:		Applications/Internet
Source0:	http://wireshark.org/download/src/%{name}-%{version}.tar.bz2
Source1:	90-wireshark-usbmon.rules
# Fedora-specific
Patch1:		wireshark-0001-enable-Lua-support.patch
# Fedora-specific
Patch2:		wireshark-0002-Customize-permission-denied-error.patch
# No longer necessary - will be removed in the next release (1.12.x)
Patch3:		wireshark-0003-Load-correct-shared-object-name-in-python.patch
# No longer necessary - will be removed in the next release (1.12.x)
Patch4:		wireshark-0004-fix-documentation-build-error.patch
# Will be proposed upstream
Patch5:		wireshark-0005-fix-string-overrun-in-plugins-profinet.patch
# Backported from upstream. See https://bugs.wireshark.org/bugzilla/show_bug.cgi?id=8326
Patch6:		wireshark-0006-From-Peter-Lemenkov-via-https-bugs.wireshark.org-bug.patch
# Backported from upstream. See also https://bugzilla.redhat.com/1007139
Patch7:		wireshark-0007-The-beginning-of-an-openflow-dissector.patch
# Will be proposed upstream
Patch8:		wireshark-0008-adds-autoconf-macro-file.patch
# Fedora-specific
Patch9:		wireshark-0009-Restore-Fedora-specific-groups.patch
# Will be proposed upstream
Patch10:	wireshark-0010-Add-pkgconfig-entry.patch
# Will be proposed upstream
Patch11:	wireshark-0011-Install-autoconf-related-file.patch
# Fedora-specific
Patch12:	wireshark-0012-move-default-temporary-directory-to-var-tmp.patch
# No longer necessary - will be removed in the next release (1.12.x)
Patch13:	wireshark-0013-Copy-over-r49999-from-trunk.patch
# No longer necessary - will be removed in the next release (1.12.x)
Patch14:	wireshark-0014-Fix-https-bugs.wireshark.org-bugzilla-show_bug.cgi-i.patch
# No longer necessary - will be removed in the next release (1.12.x)
Patch15:	wireshark-0015-From-Dirk-Jagdmann-Make-sure-err_str-is-initialized.patch
# No longer necessary - will be removed in the next release (1.12.x)
Patch16:	wireshark-0016-Crash-when-selecting-Decode-As-based-on-SCTP-PPID.-B.patch
# No longer necessary - will be removed in the next release (1.12.x)
Patch17:	wireshark-0017-Fix-https-bugs.wireshark.org-bugzilla-show_bug.cgi-i.patch
# No longer necessary - will be removed in the next release (1.12.x)
Patch18:	wireshark-0018-Copy-over-from-Trunk.patch
# No longer necessary - will be removed in the next release (1.12.x)
Patch19:	wireshark-0019-Bugfix-port-number-endianness.-Bug-9530-https-bugs.w.patch
# No longer necessary - will be removed in the next release (1.12.x)
Patch20:	wireshark-0020-Something-went-wrong-with-the-backport-of-r53608-r53.patch
# Applied upstream:
# https://bugs.wireshark.org/bugzilla/show_bug.cgi?id=9576
Patch21:	wireshark-0021-Remove-g_memmove.patch
# W.i.p. patch. See also:
# https://bugs.wireshark.org/bugzilla/show_bug.cgi?id=9561
Patch22:	wireshark-0022-Fix-IP-types.patch
# No longer necessary - will be removed in the next release (1.12.x)
Patch23:	wireshark-0023-Copy-over-r54544-from-trunk.patch
# Fedora-specific
Patch24:	wireshark-0024-Fix-paths-in-a-wireshark.desktop-file.patch
# Fedora-specific
Patch25:        wireshark-0025-Fix-Capture-Dialog-layout.patch
# Applied upstream (unstable branch)
Patch26:        wireshark-0026-amqp-1.0.patch

Url:		http://www.wireshark.org/
BuildRequires:	libpcap-devel >= 0.9
BuildRequires:	libsmi-devel
BuildRequires:	zlib-devel, bzip2-devel
BuildRequires:	openssl-devel
BuildRequires:	glib2-devel
BuildRequires:	elfutils-devel, krb5-devel
BuildRequires:	pcre-devel, libselinux
BuildRequires:	gnutls-devel
BuildRequires:	desktop-file-utils
BuildRequires:	xdg-utils
BuildRequires:	flex, bison
BuildRequires:	libcap-devel
%if 0%{?fedora} > 18
BuildRequires:	perl-podlators
%endif
BuildRequires:	libgcrypt-devel
%if %{with_GeoIP}
BuildRequires:	GeoIP-devel
%endif
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
%if %{with_gtk2}
BuildRequires:	gtk2-devel
%else
BuildRequires:	gtk3-devel
%endif

# Temporary hack - wireshark-1.8.0 is not compilable with upstream
# Makefile.in / configure, they need to be regenerated
BuildRequires: libtool, automake, autoconf

Requires(pre):	shadow-utils
%if %{with_adns}
Requires:	adns
%endif

%package	gnome
Summary:	Gnome desktop integration for wireshark
Group:		Applications/Internet
Requires:	%{name} = %{version}-%{release}
Requires:	xdg-utils
Requires:	hicolor-icon-theme
%if %{with_gtk2}
Requires:	gtk2
%else
Requires:	gtk3
%endif
%if %{with_portaudio}
Requires:	portaudio
%endif
%if %{with_GeoIP}
Requires:	GeoIP
%endif

%package devel
Summary:	Development headers and libraries for wireshark
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release} glibc-devel glib2-devel


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
%setup -q

%if %{with_lua}
%patch1 -p1 -b .enable_lua
%endif

%patch2 -p1 -b .perm_denied_customization
#%patch3 -p1 -b .soname
#%patch4 -p1 -b .pod2man
%patch5 -p1 -b .profinet_crash
%patch6 -p1 -b .rtpproxy
%patch7 -p1 -b .openflow
%patch8 -p1 -b .add_autoconf
%patch9 -p1 -b .restore_group
%patch10 -p1 -b .add_pkgconfig
%patch11 -p1 -b .install_autoconf
%patch12 -p1 -b .tmp_dir
#%patch13 -p1 -b .allow_64kpackets_for_usb
#%patch14 -p1 -b .dont_die_during_sip_dissection
#%patch15 -p1 -b .fix_main_window
#%patch16 -p1 -b .fix_sctp
#%patch17 -p1 -b .fix_global_pinfo
#%patch18 -p1 -b .fix_overflow
#%patch19 -p1 -b .fix_endianness
#%patch20 -p1 -b .fix_previous_backport
%patch21 -p1 -b .remove_g_memmove
%patch22 -p1 -b .rtpproxy_ip_types
#%patch23 -p1 -b .rare_bug_with_sniffer_traces
%patch24 -p1 -b .fix_paths
%patch25 -p1 -b .fix_capture_dlg_layout
%patch26 -p1 -b .amqp-1.0

%build
%ifarch s390 s390x sparcv9 sparc64
export PIECFLAGS="-fPIE"
%else
export PIECFLAGS="-fpie"
%endif
# FC5+ automatic -fstack-protector-all switch
export RPM_OPT_FLAGS=${RPM_OPT_FLAGS//-fstack-protector-strong/-fstack-protector-all}
export CFLAGS="$RPM_OPT_FLAGS $CPPFLAGS $PIECFLAGS -D_LARGEFILE64_SOURCE"
export CXXFLAGS="$RPM_OPT_FLAGS $CPPFLAGS $PIECFLAGS -D_LARGEFILE64_SOURCE"
export LDFLAGS="$LDFLAGS -pie"

autoreconf -ivf

%configure \
   --bindir=%{_sbindir} \
   --enable-ipv6 \
   --with-libsmi \
   --with-gnu-ld \
   --with-pic \
%if %{with_gtk2}
   --with-gtk3=no \
%else
   --with-gtk3=yes \
%endif
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
%if %{with_portaudio}
   --with-portaudio \
%else
  --with-portaudio=no \
%endif
%if %{with_GeoIP}
   --with-geoip \
%else
   --with-geoip=no \
%endif
   --with-ssl \
   --disable-warnings-as-errors \
   --with-plugins=%{_libdir}/%{name}/plugins/%{version} \
   --with-dumpcap-group="wireshark" \
   --enable-setcap-install \
   --enable-airpcap

#remove rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
# The evil plugins hack
perl -pi -e 's|-L../../epan|-L../../epan/.libs|' plugins/*/*.la

make DESTDIR=%{buildroot} install
make DESTDIR=%{buildroot} install_desktop_files

# Install python stuff.
mkdir -p %{buildroot}%{python_sitearch}
install -m 644 tools/wireshark_be.py tools/wireshark_gen.py  %{buildroot}%{python_sitearch}

desktop-file-validate %{buildroot}%{_datadir}/applications/wireshark.desktop

#install devel files (inspired by debian/wireshark-dev.header-files)
install -d -m 0755  %{buildroot}%{_includedir}/wireshark
IDIR="%{buildroot}%{_includedir}/wireshark"
mkdir -p "${IDIR}/epan"
mkdir -p "${IDIR}/epan/crypt"
mkdir -p "${IDIR}/epan/ftypes"
mkdir -p "${IDIR}/epan/dfilter"
mkdir -p "${IDIR}/epan/dissectors"
mkdir -p "${IDIR}/wiretap"
mkdir -p "${IDIR}/wsutil"
mkdir -p %{buildroot}/%{_sysconfdir}/udev/rules.d
install -m 644 color.h config.h register.h	"${IDIR}/"
install -m 644 cfile.h file.h			"${IDIR}/"
install -m 644 frame_data_sequence.h		"${IDIR}/"
install -m 644 packet-range.h print.h		"${IDIR}/"
install -m 644 epan/*.h				"${IDIR}/epan/"
install -m 644 epan/crypt/*.h			"${IDIR}/epan/crypt"
install -m 644 epan/ftypes/*.h			"${IDIR}/epan/ftypes"
install -m 644 epan/dfilter/*.h			"${IDIR}/epan/dfilter"
install -m 644 epan/dissectors/*.h		"${IDIR}/epan/dissectors"
install -m 644 wiretap/*.h			"${IDIR}/wiretap"
install -m 644 wsutil/*.h			"${IDIR}/wsutil"
install -m 644 ws_symbol_export.h               "${IDIR}/"
install -m 644 %{SOURCE1}                       %{buildroot}/%{_sysconfdir}/udev/rules.d/

# Remove .la files
rm -f %{buildroot}%{_libdir}/%{name}/plugins/%{version}/*.la

# Remove .la files in libdir
rm -f %{buildroot}%{_libdir}/*.la

%pre
getent group wireshark >/dev/null || groupadd -r wireshark
getent group usbmon >/dev/null || groupadd -r usbmon

%post
/sbin/ldconfig
/usr/bin/udevadm trigger --subsystem-match=usbmon

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
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README*
%{_sbindir}/editcap
%{_sbindir}/tshark
%{_sbindir}/mergecap
%{_sbindir}/text2pcap
%{_sbindir}/dftest
%{_sbindir}/capinfos
%{_sbindir}/randpkt
%{_sbindir}/reordercap
%attr(0750, root, wireshark) %caps(cap_net_raw,cap_net_admin=ep) %{_sbindir}/dumpcap
%{_sbindir}/rawshark
%{_sysconfdir}/udev/rules.d/90-wireshark-usbmon.rules
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
%{_mandir}/man1/reordercap.*
%{_datadir}/wireshark
%if %{with_lua}
%exclude %{_datadir}/wireshark/init.lua
%endif


%files gnome
%{_datadir}/applications/wireshark.desktop
%{_datadir}/icons/hicolor/16x16/apps/wireshark.png
%{_datadir}/icons/hicolor/24x24/apps/wireshark.png
%{_datadir}/icons/hicolor/32x32/apps/wireshark.png
%{_datadir}/icons/hicolor/48x48/apps/wireshark.png
%{_datadir}/icons/hicolor/64x64/apps/wireshark.png
%{_datadir}/icons/hicolor/128x128/apps/wireshark.png
%{_datadir}/icons/hicolor/256x256/apps/wireshark.png
%{_datadir}/icons/hicolor/16x16/mimetypes/application-wireshark-doc.png
%{_datadir}/icons/hicolor/24x24/mimetypes/application-wireshark-doc.png
%{_datadir}/icons/hicolor/32x32/mimetypes/application-wireshark-doc.png
%{_datadir}/icons/hicolor/48x48/mimetypes/application-wireshark-doc.png
%{_datadir}/icons/hicolor/64x64/mimetypes/application-wireshark-doc.png
%{_datadir}/icons/hicolor/128x128/mimetypes/application-wireshark-doc.png
%{_datadir}/icons/hicolor/256x256/mimetypes/application-wireshark-doc.png
%{_datadir}/mime/packages/wireshark.xml
%{_sbindir}/wireshark
%{_mandir}/man1/wireshark.*

%files devel
%doc doc/README.*
%if %{with_lua}
%config(noreplace) %{_datadir}/wireshark/init.lua
%endif
%{_includedir}/wireshark
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_datadir}/aclocal/*

%changelog
* Fri Jun 13 2014 Peter Hatina <phatina@redhat.com> - 1.10.8-1
- Ver. 1.10.8

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 30 2014 Peter Hatina <phatina@redhat.com> - 1.0.7-2
- add AMQP 1.0 support

* Wed Apr 23 2014 Peter Hatina <phatina@redhat.com> - 1.10.7-1
- Ver. 1.10.7

* Fri Mar 21 2014 Peter Hatina <phatina@redhat.com> - 1.10.6-2
- Reload udev rule for usbmon subsystem only

* Sat Mar 08 2014 Peter Lemenkov <lemenkov@gmail.com> - 1.10.6-1
- Ver. 1.10.6

* Fri Mar  7 2014 Peter Hatina <phatina@redhat.com> - 1.10.5-4
- Fix Capture Dialog layout on low resolution displays
- Resolves: #1071313

* Sun Feb  9 2014 Ville Skyttä <ville.skytta@iki.fi>
- Fix --with-gtk* build option usage.

* Wed Jan 29 2014 Peter Lemenkov <lemenkov@gmail.com> - 1.10.5-3
- Fixed paths in the desktop-file (see rhbz #1059188)

* Mon Jan 13 2014 Peter Lemenkov <lemenkov@gmail.com> - 1.10.5-2
- Updated RTPproxy dissector (again)
- Fix rare issue with the Sniffer traces (patch no. 23)

* Mon Dec 23 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.10.5-1
- Ver. 1.10.5
- Don't apply upstreamed patches no. 18, 19, 20.

* Thu Dec 19 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.10.4-2
- Fix endianness in the Bitcoin protocol dissector (patch no. 19)
- Last-minute fix for wrongly backported change (patch no. 20)
- Fix FTBFS in Rawhide (see patch no. 21 - recent Glib doesn't provide g_memmove macro anymore)

* Wed Dec 18 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.10.4-1
- Ver. 1.10.4
- Don't apply upsteamed patches no. 13, 14, 15, 16, 17
- Fix variable overflow (patch no. 18)
- Updated RTPproxy dissector (backported three more patches from trunk)

* Tue Dec 10 2013 Peter Hatina <phatina@redhat.com> - 1.10-3-9
- remove python support

* Tue Dec 10 2013 Peter Hatina <phatina@redhat.com> - 1.10-3-8
- fix read permissions of /dev/usbmon* for non-root users

* Mon Dec 09 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.10.3-7
- Fix error in the backported RTPproxy patches

* Fri Dec 06 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.10.3-6
- Updated RTPproxy dissector (again), squashed patch no. 15 (applied upstream).
- Use proper soname in the python scripts
- Don't apply no longer needed fix for pod2man.
- Fix for main window. See patch no. 15
- Fix for SCTP dissection. See patch no. 16
- Fix for rare issue in Base Station Subsystem GPRS Protocol dissection. See
  patch no. 17
- Fix building w/o Lua

* Wed Nov 27 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.10.3-5
- Updated RTPproxy dissector (again)
- Allow packets more than 64k (for USB capture). See patch no. 13
- Don't die during loading of some SIP capture files. See patch no. 14
- Backport support for RTPproxy dissector timeouts detection. See patch no. 15

* Wed Nov 13 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.10.3-4
- Updated RTPproxy dissector

* Thu Nov 07 2013 Peter Hatina <phatina@redhat.com> - 1.10.3-3
- fix subpackage requires

* Wed Nov 06 2013 Peter Hatina <phatina@redhat.com> - 1.10.3-2
- harden dumpcap capabilities

* Sat Nov 02 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.10.3-1
- Ver. 1.10.3
- Dropped upsteamed patch no. 13

* Tue Oct 01 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.10.2-8
- Added support for rtpproxy conversations (req/resp matching)

* Tue Sep 24 2013 Peter Hatina <phatina@redhat.com> - 1.10.2-7
- fix build error caused by symbols clash

* Tue Sep 17 2013 Peter Hatina <phatina@redhat.com> - 1.10.2-6
- move default temporary directory to /var/tmp

* Fri Sep 13 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.10.2-5
- Convert automake/pkgconfig files into patches (better upstream integration)
- Restored category in the *.desktop file
- Install another one necessary header file - frame_data_sequence.h

* Thu Sep 12 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.10.2-4
- Enhance desktop integration (*.desktop and MIME-related files)

* Thu Sep 12 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.10.2-3
- Fix building on Fedora 18 (no perl-podlators)

* Thu Sep 12 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.10.2-2
- Add an OpenFlow dissector

* Wed Sep 11 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.10-2-1
- Ver. 1.10.2
- Actually remove the console helper

* Mon Sep 09 2013 Peter Lemenkov <lemenkov@gmail.com> - 1.10.1-1
- Ver. 1.10.1
- Backported rtpproxy dissector module

* Wed Sep 04 2013 Peter Hatina <phatina@redhat.com> - 1.10.0-11
- fix missing ws_symbol_export.h

* Wed Sep 04 2013 Peter Hatina <phatina@redhat.com> - 1.10.0-10
- fix tap iostat overflow

* Wed Sep 04 2013 Peter Hatina <phatina@redhat.com> - 1.10.0-9
- fix sctp bytes graph crash

* Wed Sep 04 2013 Peter Hatina <phatina@redhat.com> - 1.10.0-8
- fix string overrun in plugins/profinet

* Tue Sep 03 2013 Peter Hatina <phatina@redhat.com> - 1.10.0-7
- fix BuildRequires - libgcrypt-devel

* Tue Sep 03 2013 Peter Hatina <phatina@redhat.com> - 1.10.0-6
- fix build parameter -fstack-protector-all

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 24 2013 Peter Hatina <phatina@redhat.com> 1.10.0-4
- fix pod2man build error

* Mon Jun 24 2013 Peter Hatina <phatina@redhat.com> 1.10.0-3
- fix bogus date

* Mon Jun 17 2013 Peter Hatina <phatina@redhat.com> 1.10.0-2
- fix flow graph crash

* Mon Jun 17 2013 Peter Hatina <phatina@redhat.com> 1.10.0-1
- upgrade to 1.10.0
- see http://www.wireshark.org/docs/relnotes/wireshark-1.10.0.html

* Mon Apr 08 2013 Peter Hatina <phatina@redhat.com> 1.8.6-5
- fix documentation build error

* Wed Mar 27 2013 Peter Hatina <phatina@redhat.com> 1.8.6-4
- fix capture crash (#894753)

* Tue Mar 19 2013 Peter Hatina <phatina@redhat.com> 1.8.6-3
- fix dns resolving crash (#908211)

* Mon Mar 18 2013 Peter Hatina <phatina@redhat.com> 1.8.6-2
- return to gtk2, stable branch 1.8 is not gtk3 ready

* Tue Mar 12 2013 Peter Hatina <phatina@redhat.com> 1.8.6-1
- upgrade to 1.8.6
- see http://www.wireshark.org/docs/relnotes/wireshark-1.8.6.html

* Sun Feb 10 2013 Parag Nemade <paragn AT fedoraproject DOT org> - 1.8.5-3
- Remove vendor tag from desktop file as per https://fedorahosted.org/fesco/ticket/1077

* Tue Feb 05 2013 Peter Hatina <phatina@redhat.com> - 1.8.5-2
- fix gtk3 layout issues
- NOTE: there may be some windows with broken layouts left

* Thu Jan 31 2013 Peter Hatina <phatina@redhat.com> - 1.8.5-1
- upgrade to 1.8.5
- see http://www.wireshark.org/docs/relnotes/wireshark-1.8.5.html

* Mon Dec 03 2012 Peter Hatina <phatina@redhat.com> - 1.8.4-1
- upgrade to 1.8.4
- see http://www.wireshark.org/docs/relnotes/wireshark-1.8.4.html

* Tue Oct 16 2012 Peter Hatina <phatina@redhat.com> - 1.8.3-2
- backport dissector table fix
- TODO: remove this after new release

* Thu Oct 11 2012 Peter Hatina <phatina@redhat.com> - 1.8.3-1
- upgrade to 1.8.3
- see http://www.wireshark.org/docs/relnotes/wireshark-1.8.3.html

* Tue Sep  4 2012 Jan Safranek <jsafrane@redhat.com> - 1.8.2-3
- added back compatibility with RHEL6
- GeoIP build dependency made also conditional on with_GeoIP variable

* Wed Aug 29 2012 Jan Safranek <jsafrane@redhat.com> - 1.8.2-2
- fixed "libwireshark.so.1: cannot open shared object file" error
  message on startup

* Thu Aug 16 2012 Jan Safranek <jsafrane@redhat.com> - 1.8.2-1
- upgrade to 1.8.2
- see http://www.wireshark.org/docs/relnotes/wireshark-1.8.2.html

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 24 2012 Jan Safranek <jsafrane@redhat.com> - 1.8.1-1
- upgrade to 1.8.1
- see http://www.wireshark.org/docs/relnotes/wireshark-1.8.1.html

* Mon Jun 25 2012 Jan Safranek <jsafrane@redhat.com> - 1.8.0
- upgrade to 1.8.0
- see http://www.wireshark.org/docs/relnotes/wireshark-1.8.0.html

* Wed May 23 2012 Jan Safranek <jsafrane@redhat.com> - 1.6.8-1
- upgrade to 1.6.8
- see http://www.wireshark.org/docs/relnotes/wireshark-1.6.8.html

* Mon May 21 2012 Jan Safranek <jsafrane@redhat.com> - 1.6.7-2
- Removed dependency on GeoIP on RHEL.

* Tue Apr 10 2012 Jan Safranek <jsafrane@redhat.com> - 1.6.7-1
- upgrade to 1.6.7
- see http://www.wireshark.org/docs/relnotes/wireshark-1.6.7.html

* Wed Mar 28 2012 Jan Safranek <jsafrane@redhat.com> - 1.6.6-1
- upgrade to 1.6.6
- see http://www.wireshark.org/docs/relnotes/wireshark-1.6.6.html

* Fri Mar  9 2012 Jan Safranek <jsafrane@redhat.com> - 1.6.5-2
- fixed wireshark crashing when using combo box in import dialog (#773290)
- added AES support into netlogon dissector

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
