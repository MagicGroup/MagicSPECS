# we build CUPS also with relro
%global _hardened_build 1

Summary: OpenPrinting CUPS filters and backends
Name:    cups-filters
Version: 1.0.46
Release: 2%{?dist}

# For a breakdown of the licensing, see COPYING file
# GPLv2:   filters: commandto*, imagetoraster, pdftops, rasterto*,
#                   imagetopdf, pstopdf, texttopdf
#         backends: parallel, serial
# GPLv2+:  filters: gstopxl, textonly, texttops, imagetops, foomatic-rip
# GPLv3:   filters: bannertopdf
# GPLv3+:  filters: urftopdf
# LGPLv2+:   utils: cups-browsed
# MIT:     filters: gstoraster, pdftoijs, pdftoopvp, pdftopdf, pdftoraster
License: GPLv2 and GPLv2+ and GPLv3 and GPLv3+ and LGPLv2+ and MIT

Url:     http://www.linuxfoundation.org/collaborate/workgroups/openprinting/cups-filters
Source0: http://www.openprinting.org/download/cups-filters/cups-filters-%{version}.tar.xz

Requires: cups-filters-libs%{?_isa} = %{version}-%{release}

# Obsolete cups-php (bug #971741)
Obsoletes: cups-php < 1:1.6.0-1
# Don't Provide it because we don't build the php module
#Provides: cups-php = 1:1.6.0-1

BuildRequires: cups-devel
# pdftopdf
BuildRequires: qpdf-devel
# pdftops
BuildRequires: poppler-utils
# pdftoijs, pdftoopvp, pdftoraster, gstoraster
BuildRequires: poppler-devel poppler-cpp-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: libtiff-devel
BuildRequires: zlib-devel
BuildRequires: pkgconfig dbus-devel
# libijs
BuildRequires: ghostscript-devel
BuildRequires: freetype-devel
BuildRequires: fontconfig-devel
BuildRequires: lcms2-devel
# cups-browsed
BuildRequires: avahi-devel avahi-glib-devel
BuildRequires: systemd

# Make sure we get postscriptdriver tags.
BuildRequires: python-cups

# Testing font for test scripts.
BuildRequires: dejavu-sans-fonts

# autogen.sh
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool

Requires: cups-filesystem
Requires: poppler-utils
# pstopdf
Requires: bc grep sed

# cups-browsed
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

# Ghostscript CUPS filters live here since Ghostscript 9.08.
Provides: ghostscript-cups = 9.08
Obsoletes: ghostscript-cups < 9.08

# foomatic-rip's upstream moved from foomatic-filters to cups-filters-1.0.42
Provides: foomatic-filters = 4.0.9-8
Obsoletes: foomatic-filters < 4.0.9-8

%package libs
Summary: OpenPrinting CUPS filters and backends - cupsfilters and fontembed libraries
Group:   System Environment/Libraries
# LGPLv2: libcupsfilters
# MIT:    libfontembed
License: LGPLv2 and MIT

%package devel
Summary: OpenPrinting CUPS filters and backends - development environment
Group:   Development/Libraries
License: LGPLv2 and MIT
Requires: cups-filters-libs%{?_isa} = %{version}-%{release}

%description
Contains backends, filters, and other software that was
once part of the core CUPS distribution but is no longer maintained by
Apple Inc. In addition it contains additional filters developed
independently of Apple, especially filters for the PDF-centric printing
workflow introduced by OpenPrinting.

%description libs
This package provides cupsfilters and fontembed libraries.

%description devel
This is the development package for OpenPrinting CUPS filters and backends.

%prep
%setup -q

%build
# work-around Rpath
./autogen.sh

# --with-pdftops=hybrid - use Poppler's pdftops instead of Ghostscript for
#                         Brother, Minolta, and Konica Minolta to work around
#                         bugs in the printer's PS interpreters
# --with-rcdir=no - don't install SysV init script
%configure --disable-static \
           --disable-silent-rules \
           --with-pdftops=hybrid \
           --enable-dbus \
           --with-rcdir=no

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

# https://fedoraproject.org/wiki/Packaging_tricks#With_.25doc
mkdir __doc
mv  %{buildroot}%{_datadir}/doc/cups-filters/* __doc
rm -rf %{buildroot}%{_datadir}/doc/cups-filters

# Don't ship libtool la files.
rm -f %{buildroot}%{_libdir}/lib*.la

# Not sure what is this good for.
rm -f %{buildroot}%{_bindir}/ttfread

# systemd unit file
mkdir -p %{buildroot}%{_unitdir}
install -p -m 644 utils/cups-browsed.service %{buildroot}%{_unitdir}

# LSB3.2 requires /usr/bin/foomatic-rip,
# create it temporarily as a relative symlink
ln -sf ../lib/cups/filter/foomatic-rip %{buildroot}%{_bindir}/foomatic-rip

%check
make check

%post
%systemd_post cups-browsed.service

# Initial installation
if [ $1 -eq 1 ] ; then
    IN=%{_sysconfdir}/cups/cupsd.conf
    OUT=%{_sysconfdir}/cups/cups-browsed.conf
    keyword=BrowsePoll

    # We can remove this after few releases, it's just for the introduction of cups-browsed.
    if [ -f "$OUT" ]; then
        echo -e "\n# NOTE: This file is not part of CUPS. You need to start & enable cups-browsed service." >> "$OUT"
    fi

    # move BrowsePoll from cupsd.conf to cups-browsed.conf
    if [ -f "$IN" ] && grep -iq ^$keyword "$IN"; then
        if ! grep -iq ^$keyword "$OUT"; then
            (cat >> "$OUT" <<EOF

# Settings automatically moved from cupsd.conf by RPM package:
EOF
            ) || :
            (grep -i ^$keyword "$IN" >> "$OUT") || :
            #systemctl enable cups-browsed.service >/dev/null 2>&1 || :
        fi
        sed -i -e "s,^$keyword,#$keyword directive moved to cups-browsed.conf\n#$keyword,i" "$IN" || :
    fi
fi

%preun
%systemd_preun cups-browsed.service

%postun
%systemd_postun_with_restart cups-browsed.service 

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%doc __doc/README __doc/AUTHORS __doc/NEWS
%config(noreplace) %{_sysconfdir}/cups/cups-browsed.conf
%config(noreplace) %{_sysconfdir}/fonts/conf.d/99pdftoopvp.conf
%attr(0755,root,root) %{_cups_serverbin}/filter/*
%attr(0755,root,root) %{_cups_serverbin}/backend/parallel
# Serial backend needs to run as root (bug #212577#c4).
%attr(0700,root,root) %{_cups_serverbin}/backend/serial
%{_datadir}/cups/banners
%{_datadir}/cups/charsets
%{_datadir}/cups/data/*
# this needs to be in the main package because of cupsfilters.drv
%{_datadir}/cups/ppdc/pcl.h
%{_datadir}/cups/drv/cupsfilters.drv
%{_datadir}/cups/mime/cupsfilters.types
%{_datadir}/cups/mime/cupsfilters.convs
%{_datadir}/ppd/cupsfilters
%{_sbindir}/cups-browsed
%{_unitdir}/cups-browsed.service
%{_mandir}/man8/cups-browsed.8.gz
%{_mandir}/man5/cups-browsed.conf.5.gz
%{_mandir}/man1/foomatic-rip.1.gz
%{_bindir}/foomatic-rip

%files libs
%doc __doc/COPYING fontembed/README
%{_libdir}/libcupsfilters.so.*
%{_libdir}/libfontembed.so.*

%files devel
%{_includedir}/cupsfilters
%{_includedir}/fontembed
%{_datadir}/cups/ppdc/escp.h
%{_libdir}/pkgconfig/libcupsfilters.pc
%{_libdir}/pkgconfig/libfontembed.pc
%{_libdir}/libcupsfilters.so
%{_libdir}/libfontembed.so

%changelog
* Thu Feb 20 2014 Jiri Popelka <jpopelka@redhat.com> - 1.0.46-1
- 1.0.46

* Fri Feb 14 2014 Jiri Popelka <jpopelka@redhat.com> - 1.0.45-1
- 1.0.45

* Mon Jan 20 2014 Jiri Popelka <jpopelka@redhat.com> - 1.0.44-1
- 1.0.44

* Tue Jan 14 2014 Jiri Popelka <jpopelka@redhat.com> - 1.0.43-2
- add /usr/bin/foomatic-rip symlink, due to LSB3.2 (#1052452)

* Fri Dec 20 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.43-1
- 1.0.43: upstream fix for bug #768811 (pdf-landscape)

* Sat Nov 30 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.42-1
- 1.0.42: includes foomatic-rip (obsoletes foomatic-filters package)

* Tue Nov 19 2013 Tim Waugh <twaugh@redhat.com> - 1.0.41-4
- Adjust filter costs so application/vnd.adobe-read-postscript input
  doesn't go via pstotiff (bug #1008166).

* Thu Nov 14 2013 Jaromír Končický <jkoncick@redhat.com> - 1.0.41-3
- Fix memory leaks in cups-browsed (bug #1027317).

* Wed Nov  6 2013 Tim Waugh <twaugh@redhat.com> - 1.0.41-2
- Include dbus so that colord support works (bug #1026928).

* Wed Oct 30 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.41-1
- 1.0.41 - PPD-less printing support

* Mon Oct 21 2013 Tim Waugh <twaugh@redhat.com> - 1.0.40-4
- Fix socket leaks in the BrowsePoll code (bug #1021512).

* Wed Oct 16 2013 Tim Waugh <twaugh@redhat.com> - 1.0.40-3
- Ship the gstoraster MIME conversion rule now we provide that filter
  (bug #1019261).

* Fri Oct 11 2013 Tim Waugh <twaugh@redhat.com> - 1.0.40-2
- Fix PDF landscape printing (bug #768811).

* Fri Oct 11 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.40-1
- 1.0.40
- Use new "hybrid" pdftops renderer.

* Thu Oct 03 2013 Jaromír Končický <jkoncick@redhat.com> - 1.0.39-1
- 1.0.39
- Removed obsolete patches "pdf-landscape" and "browsepoll-notifications"

* Tue Oct  1 2013 Tim Waugh <twaugh@redhat.com> - 1.0.38-4
- Use IPP notifications for BrowsePoll when possible (bug #975241).

* Tue Oct  1 2013 Tim Waugh <twaugh@redhat.com> - 1.0.38-3
- Fixes for some printf-type format mismatches (bug #1014093).

* Tue Sep 17 2013 Tim Waugh <twaugh@redhat.com> - 1.0.38-2
- Fix landscape printing for PDFs (bug #768811).

* Wed Sep 04 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.38-1
- 1.0.38

* Thu Aug 29 2013 Jaromír Končický <jkoncick@redhat.com> - 1.0.37-1
- 1.0.37.

* Tue Aug 27 2013 Jaromír Končický <jkoncick@redhat.com> - 1.0.36-5
- Added build dependency - font required for running tests

* Tue Aug 27 2013 Jaromír Končický <jkoncick@redhat.com> - 1.0.36-4
- Added checking phase (make check)

* Wed Aug 21 2013 Tim Waugh <twaugh@redhat.com> - 1.0.36-3
- Upstream patch to re-work filter costs (bug #998977). No longer need
  text filter costs patch as paps gets used by default now if
  installed.

* Mon Aug 19 2013 Marek Kasik <mkasik@redhat.com> - 1.0.36-2
- Rebuild (poppler-0.24.0)

* Tue Aug 13 2013 Tim Waugh <twaugh@redhat.com> - 1.0.36-1
- 1.0.36.

* Tue Aug 13 2013 Tim Waugh <twaugh@redhat.com> - 1.0.35-7
- Upstream patch to move in filters from ghostscript.

* Tue Jul 30 2013 Tim Waugh <twaugh@redhat.com> - 1.0.35-6
- Set cost for text filters to 200 so that the paps filter gets
  preference for the time being (bug #988909).

* Wed Jul 24 2013 Tim Waugh <twaugh@redhat.com> - 1.0.35-5
- Handle page-label when printing n-up as well.

* Tue Jul 23 2013 Tim Waugh <twaugh@redhat.com> - 1.0.35-4
- Added support for page-label (bug #987515).

* Thu Jul 11 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.35-3
- Rebuild (qpdf-5.0.0)

* Mon Jul 01 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.35-2
- add cups-browsed(8) and cups-browsed.conf(5)
- don't reverse lookup IP address in URI (#975822)

* Wed Jun 26 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.35-1
- 1.0.35

* Mon Jun 24 2013 Marek Kasik <mkasik@redhat.com> - 1.0.34-9
- Rebuild (poppler-0.22.5)

* Wed Jun 19 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.34-8
- fix the note we add in cups-browsed.conf

* Wed Jun 12 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.34-7
- Obsolete cups-php (#971741)

* Wed Jun 05 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.34-6
- one more cups-browsed leak fixed (#959682)

* Wed Jun 05 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.34-5
- perl is actually not required by pstopdf, because the calling is in dead code

* Mon Jun 03 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.34-4
- fix resource leaks and other problems found by Coverity & Valgrind (#959682)

* Wed May 15 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.34-3
- ship ppdc/pcl.h because of cupsfilters.drv

* Tue May 07 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.34-2
- pstopdf requires bc (#960315)

* Thu Apr 11 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.34-1
- 1.0.34

* Fri Apr 05 2013 Fridolin Pokorny <fpokorny@redhat.com> - 1.0.33-1
- 1.0.33
- removed cups-filters-1.0.32-null-info.patch, accepted by upstream

* Thu Apr 04 2013 Fridolin Pokorny <fpokorny@redhat.com> - 1.0.32-2
- fixed segfault when info is NULL

* Thu Apr 04 2013 Fridolin Pokorny <fpokorny@redhat.com> - 1.0.32-1
- 1.0.32

* Fri Mar 29 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.31-3
- add note to cups-browsed.conf

* Thu Mar 28 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.31-2
- check cupsd.conf existence prior to grepping it (#928816)

* Fri Mar 22 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.31-1
- 1.0.31

* Tue Mar 19 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.30-4
- revert previous change

* Wed Mar 13 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.30-3
- don't ship banners for now (#919489)

* Tue Mar 12 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.30-2
- move BrowsePoll from cupsd.conf to cups-browsed.conf in %%post

* Fri Mar 08 2013 Jiri Popelka <jpopelka@redhat.com> - 1.0.30-1
- 1.0.30: CUPS browsing and broadcasting in cups-browsed

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.29-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jan 19 2013 Rex Dieter <rdieter@fedoraproject.org> 1.0.29-3
- backport upstream buildfix for poppler-0.22.x

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 1.0.29-2
- rebuild due to "jpeg8-ABI" feature drop

* Thu Jan 03 2013 Jiri Popelka <jpopelka@redhat.com> 1.0.29-1
- 1.0.29

* Wed Jan 02 2013 Jiri Popelka <jpopelka@redhat.com> 1.0.28-1
- 1.0.28: cups-browsed daemon and service

* Thu Nov 29 2012 Jiri Popelka <jpopelka@redhat.com> 1.0.25-1
- 1.0.25

* Fri Sep 07 2012 Jiri Popelka <jpopelka@redhat.com> 1.0.24-1
- 1.0.24

* Wed Aug 22 2012 Jiri Popelka <jpopelka@redhat.com> 1.0.23-1
- 1.0.23: old pdftopdf removed

* Tue Aug 21 2012 Jiri Popelka <jpopelka@redhat.com> 1.0.22-1
- 1.0.22: new pdftopdf (uses qpdf instead of poppler)

* Wed Aug 08 2012 Jiri Popelka <jpopelka@redhat.com> 1.0.20-4
- rebuild

* Thu Aug 02 2012 Jiri Popelka <jpopelka@redhat.com> 1.0.20-3
- commented multiple licensing breakdown (#832130)
- verbose build output

* Thu Aug 02 2012 Jiri Popelka <jpopelka@redhat.com> 1.0.20-2
- BuildRequires: poppler-cpp-devel (to build against poppler-0.20)

* Mon Jul 23 2012 Jiri Popelka <jpopelka@redhat.com> 1.0.20-1
- 1.0.20

* Tue Jul 17 2012 Jiri Popelka <jpopelka@redhat.com> 1.0.19-1
- 1.0.19

* Wed May 30 2012 Jiri Popelka <jpopelka@redhat.com> 1.0.18-1
- initial spec file
