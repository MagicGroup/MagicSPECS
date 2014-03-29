%global prerel pre6

Name:      elinks
Summary:   A text-mode Web browser
Version:   0.12
Release:   0.37.%{prerel}%{?dist}
License:   GPLv2
URL:       http://elinks.or.cz
Group:     Applications/Internet
Source:    http://elinks.or.cz/download/elinks-%{version}%{prerel}.tar.bz2
Source2:   elinks.conf

BuildRequires: automake
BuildRequires: bzip2-devel
BuildRequires: expat-devel
BuildRequires: gpm-devel
BuildRequires: js-devel
BuildRequires: krb5-devel
BuildRequires: libidn-devel
BuildRequires: nss_compat_ossl-devel
BuildRequires: pkgconfig
BuildRequires: zlib-devel
Requires(preun): %{_sbindir}/alternatives
Requires(post): coreutils
Requires(post): %{_sbindir}/alternatives
Requires(postun): coreutils
Requires(postun): %{_sbindir}/alternatives
Provides:  webclient
Provides:  links = 1:0.97-1
Provides: text-www-browser

Patch0: elinks-0.11.0-ssl-noegd.patch
Patch1: elinks-0.10.1-utf_8_io-default.patch
Patch3: elinks-0.11.0-getaddrinfo.patch
Patch4: elinks-0.11.0-sysname.patch
Patch5: elinks-0.10.1-xterm.patch
Patch7: elinks-0.11.3-macropen.patch
Patch8: elinks-scroll.patch
Patch9: elinks-nss.patch
Patch10: elinks-nss-inc.patch
Patch11: elinks-0.12pre5-js185.patch
Patch12: elinks-0.12pre5-ddg-search.patch
Patch13: elinks-0.12pre6-autoconf.patch
Patch14: elinks-0.12pre5-ssl-hostname.patch

%description
Elinks is a text-based Web browser. Elinks does not display any images,
but it does support frames, tables and most other HTML tags. Elinks'
advantage over graphical browsers is its speed--Elinks starts and exits
quickly and swiftly displays Web pages.

%prep
%setup -q -n %{name}-%{version}%{prerel}

# Prevent crash when HOME is unset (bug #90663).
%patch0 -p1

# UTF-8 by default
%patch1 -p1

# Make getaddrinfo call use AI_ADDRCONFIG.
%patch3 -p1

# Don't put so much information in the user-agent header string (bug #97273).
%patch4 -p1

# Fix xterm terminal: "Linux" driver seems better than "VT100" (#128105)
%patch5 -p1

# fix for open macro in new glibc
%patch7 -p1

#upstream fix for out of screen dialogs
%patch8 -p1

# Port elinks to use NSS library for cryptography (#346861) - accepted upstream
%patch9 -p1

# Port elinks to use NSS library for cryptography (#346861) - incremental patch
%patch10 -p1

# backported upstream commits f31cf6f, 2844f8b, 218a225, and 12803e4
%patch11 -p1

# add default "ddg" dumb/smart rewrite prefixes for DuckDuckGo (#856348)
%patch12 -p1

# add missing AC_LANG_PROGRAM around the first argument of AC_COMPILE_IFELSE
%patch13 -p1

# verify server certificate hostname with nss_compat_ossl (#881411)
%patch14 -p1

# remove bogus serial numbers
sed -i 's/^# *serial [AM0-9]*$//' acinclude.m4 config/m4/*.m4

# we need to recreate autotools files because of the NSS patch
aclocal -I config/m4
autoconf
autoheader

%build
export CFLAGS="$RPM_OPT_FLAGS $(getconf LFS_CFLAGS) -D_GNU_SOURCE"
%configure %{?rescue:--without-gpm} --without-x --with-gssapi \
  --enable-bittorrent --with-nss_compat_ossl --enable-256-colors \
  --without-openssl --without-gnutls

# uncomment to turn off optimizations
#sed -i 's/-O2/-O0/' Makefile.config

MOPTS="V=1"
if tty >/dev/null 2>&1; then
    # turn on fancy colorized output only when we have a TTY device
    MOPTS=
fi
make %{?_smp_mflags} $MOPTS

%install
make install DESTDIR=$RPM_BUILD_ROOT V=1
rm -f $RPM_BUILD_ROOT%{_datadir}/locale/locale.alias
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/elinks.conf
touch $RPM_BUILD_ROOT%{_bindir}/links
true | gzip -c > $RPM_BUILD_ROOT%{_mandir}/man1/links.1.gz
%find_lang elinks

%postun
if [ "$1" -ge "1" ]; then
	links=`readlink %{_sysconfdir}/alternatives/links`
	if [ "$links" == "%{_bindir}/elinks" ]; then
		%{_sbindir}/alternatives --set links %{_bindir}/elinks
	fi
fi
exit 0

%post
#Set up alternatives files for links
%{_sbindir}/alternatives --install %{_bindir}/links links %{_bindir}/elinks 90 \
  --slave %{_mandir}/man1/links.1.gz links-man %{_mandir}/man1/elinks.1.gz
links=`readlink %{_sysconfdir}/alternatives/links`
if [ "$links" == "%{_bindir}/elinks" ]; then
	%{_sbindir}/alternatives --set links %{_bindir}/elinks
fi


%preun
if [ $1 = 0 ]; then
	%{_sbindir}/alternatives --remove links %{_bindir}/elinks
fi
exit 0

%files -f elinks.lang
%doc README SITES TODO COPYING
%ghost %verify(not md5 size mtime) %{_bindir}/links
%{_bindir}/elinks
%ghost %verify(not md5 size mtime) %{_mandir}/man1/links.1.gz
%config(noreplace) %{_sysconfdir}/elinks.conf
%{_mandir}/man1/elinks.1*
%{_mandir}/man5/*

%changelog
* Wed Sep 18 2013 Kamil Dudka <kdudka@redhat.com> - 0.12-0.37.pre6
- verify server certificate hostname with nss_compat_ossl (#881411)

* Tue Sep 03 2013 Kamil Dudka <kdudka@redhat.com> - 0.12-0.36.pre6
- remove ancient Obsoletes tag against links (#1002132)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-0.35.pre6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Feb 25 2013 Kamil Dudka <kdudka@redhat.com> - 0.12-0.34.pre6
- update to latest upstream pre-release
- drop unneeded patches
- fix autoconf warnings
- explicitly disable using OpenSSL and GnuTLS

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-0.33.pre5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 04 2013 Kamil Dudka <kdudka@redhat.com> - 0.12-0.32.pre5
- do not delegate GSSAPI credentials (CVE-2012-4545)

* Mon Oct 08 2012 Kamil Dudka <kdudka@redhat.com> - 0.12-0.31.pre5
- add default "ddg" dumb/smart rewrite prefixes for DuckDuckGo (#856348)

* Tue Aug 28 2012 Kamil Dudka <kdudka@redhat.com> - 0.12-0.30.pre5
- fix specfile issues reported by the fedora-review script

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-0.29.pre5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Mar 09 2012 Kamil Dudka <kdudka@redhat.com> - 0.12-0.28.pre5
- do not crash if add_heartbeat() returned NULL (#798103)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-0.27.pre5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri May 06 2011 Kamil Dudka <kdudka@redhat.com> - 0.12-0.26.pre5
- improve the js-1.8.5 patch (upstream commit 218a225)

* Thu Apr 21 2011 Kamil Dudka <kdudka@redhat.com> - 0.12-0.25.pre5
- port to js-1.8.5 API (upstream commits f31cf6f and 2844f8b)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-0.24.pre5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Apr 07 2010 Kamil Dudka <kdudka@redhat.com> - 0.12-0.23.pre5
- do not print control characters to build logs
- avoid aclocal warnings

* Thu Jan 07 2010 Kamil Dudka <kdudka@redhat.com> - 0.12-0.22.pre5
- remove patch for configure script to find OpenSSL (we use NSS now)
- remove buildrequires for nss-devel (#550770)

* Sun Dec 27 2009 Kamil Dudka <kdudka@redhat.com> 0.12-0.21.pre5
- add buildrequires for js-devel (#550717) and zlib-devel
- build support for 256 color terminal

* Mon Dec 14 2009 Ondrej Vasik <ovasik@redhat.com> 0.12-0.20.pre5
- Add buildrequires for gpm-devel to enable gpm support(#547064)

* Fri Aug 14 2009 Orion Poplawski <orion@cora.nwra.com> 0.12-0.19.pre5
- Add Requires(post/postun): coreutils for readlink

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-0.18.pre5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 08 2009 Ondrej Vasik <ovasik@redhat.com> 0.12-0.17.pre5
- new upstream bugfix prerelease

* Mon Jun 01 2009 Ondrej Vasik <ovasik@redhat.com> 0.12-0.16.pre4
- new upstream bugfix prerelease
- defuzz patches

* Wed Apr 29 2009 Kamil Dudka <kdudka@redhat.com> 0.12-0.15.pre3
- try to load default NSS root certificates if the configuration option
  connection.ssl.trusted_ca_file is set to an empty string (#497788)

* Tue Apr 28 2009 Ondrej Vasik <ovasik@redhat.com> 0.12-0.14.pre3
- enable certificate verification by default via configuration
  file(#495532)

* Tue Apr 28 2009 Kamil Dudka <kdudka@redhat.com> 0.12-0.13.pre3
- use appropriate BuildRequires for nss_compat_ossl (#495532)
- support for trusted CA certificates loading from file in PEM format

* Fri Apr 03 2009 Ondrej Vasik <ovasik@redhat.com> 0.12-0.12.pre3
- use word Elinks instead of Links in package description

* Mon Mar 30 2009 Ondrej Vasik <ovasik@redhat.com> 0.12-0.11.pre3
- new upstream bugfix prerelease
- defuzz patches

* Wed Mar 25 2009 Ondrej Vasik <ovasik@redhat.com> 0.12-0.10.pre2
- use better obsoletes/provides for links, use alternatives for
  links manpage and binary(#470703)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-0.9.pre2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 16 2009 Tomas Mraz <tmraz@redhat.com> 0.12-0.8.pre2
- rebuild with new openssl

* Wed Jan 14 2009 Ondrej Vasik <ovasik@redhat.com> 0.12-0.7.pre2
- versioned obsoletes and provides for links

* Wed Oct  1 2008 Kamil Dudka <kdudka@redhat.com> 0.12-0.6.pre2
- port elinks to use NSS library for cryptography (#346861)

* Mon Sep 29 2008 Ondrej Vasik <ovasik@redhat.com> 0.12-0.5.pre2
- new upstream bugfix prerelease
- Removed already applied patches for tabreload and bittorrent

* Mon Sep  1 2008 Ondrej Vasik <ovasik@redhat.com> 0.12-0.4.pre1
- upstream fix for bittorrent protocol
- upstream fix for out of screen bittorrent dialog texts

* Tue Jul 15 2008 Ondrej Vasik <ovasik@redhat.com> 0.12-0.3.pre1
- get rid off fuzz in patches

* Tue Jul 15 2008 Ondrej Vasik <ovasik@redhat.com> 0.12-0.2.pre1
- fix a crash when opening tab during page reload

* Tue Jul  1 2008 Ondrej Vasik <ovasik@redhat.com> 0.12-0.1.pre1
- unstable elinks-0.12 pre1, solves several long-term issues 
  unsolvable (or very hard to solve) in 0.11.4 (like #173411),
  in general is elinks-0.12pre1 considered better than 0.11.4
- dropped patches negotiate-auth, chunkedgzip - included in 0.12pre1,
  modified few others due source code changes

* Sat Jun 21 2008 Ondrej Vasik <ovasik@redhat.com> 0.11.4-1
- new stable upstream release

* Thu Mar  6 2008 Ondrej Vasik <ovasik@redhat.com> 0.11.4-0.4.rc1
- new upstream release candidate marked stable

* Thu Feb 21 2008 Ondrej Vasik <ovasik@redhat.com> 0.11.4-0.3.rc0
- fixed broken output for gzipped chunked pages(#410801)

* Thu Feb 07 2008 Ondrej Vasik <ovasik@redhat.com> 0.11.4-0.2.rc0
- used -D_GNU_SOURCE instead of ugly hack/patch to 
  have NI_MAXPATH defined

* Wed Feb 06 2008 Ondrej Vasik <ovasik@redhat.com> 0.11.4-0.1.rc0
- new version marked stable by upstream 0.11.4rc0
- enabled experimental bittorent support(#426702)

* Wed Dec 05 2007 Ondrej Vasik <ovasik@redhat.com> 0.11.3-7
- rebuilt because of new OpenSSL

* Thu Oct 11 2007 Ondrej Vasik <ovasik@redhat.com> 0.11.3-6
- generalized text-www-browser requirements(#174566)

* Tue Aug 28 2007 Ondrej Vasik <ovasik@redhat.com> 0.11.3-5
- rebuilt because of expat 2.0

* Wed Aug 22 2007 Ondrej Vasik <ovasik@redhat.com> 0.11.3-4
- rebuilt for F8
- changed license tag to GPLv2

* Thu Aug  9 2007 Ondrej Vasik <ovasik@redhat.com> 0.11.3-3
- fix of open macro(new glibc) by Joe Orton

* Fri Jul 27 2007 Ondrej Vasik <ovasik@redhat.com> 0.11.3-2
- cleanup of duplicates in buildreq, added license file to doc 
- (package review by Tyler Owen(#225725))

* Tue Jun  5 2007 Ondrej Vasik <ovasik@redhat.com> 0.11.3-1
- update to new upstream version
- removed patch for #210103 , included in upstream release
- updated patch elinks-0.11.1-negotiate.patch to pass build

* Mon Mar 26 2007 Karel Zak <kzak@redhat.com> 0.11.2-1
- update to new upstream version
- cleanup spec file

* Wed Oct 11 2006 Karel Zak <kzak@redhat.com> 0.11.1-5
- fix #210103 - elinks crashes when given bad HTTP_PROXY

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.11.1-4.1
- rebuild

* Mon Jun 12 2006 Karel Zak <kzak@redhat.com> 0.11.1-4
- improved negotiate-auth patch (faster now)

* Fri Jun  9 2006 Karel Zak <kzak@redhat.com> 0.11.1-3
- added negotiate-auth (GSSAPI) support -- EXPERIMENTAL!

* Mon May 29 2006 Karel Zak <kzak@redhat.com> 0.11.1-2
- update to new upstream version

* Wed May 17 2006 Karsten Hopp <karsten@redhat.de> 0.11.0-3
- add buildrequires bzip2-devel, expat-devel,libidn-devel

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.11.0-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.11.0-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 10 2006 Karel Zak <kzak@redhat.com> 0.11.0-2
- use upstream version of srcdir.patch

* Tue Jan 10 2006 Karel Zak <kzak@redhat.com> 0.11.0-1
- update to new upstream version
- fix 0.11.0 build system (srcdir.patch)
- regenerate patches:
     elinks-0.11.0-getaddrinfo.patch, 
     elinks-0.11.0-ssl-noegd.patch,
     elinks-0.11.0-sysname.patch,
     elinks-0.11.0-union.patch

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com> 0.10.6-2.1
- rebuilt

* Wed Nov  9 2005 Karel Zak <kzak@redhat.com> 0.10.6-2
- rebuild (against new openssl)

* Thu Sep 29 2005 Karel Zak <kzak@redhat.com> 0.10.6-1
- update to new upstream version

* Tue May 17 2005 Karel Zak <kzak@redhat.com> 0.10.3-3
- fix #157300 - Strange behavior on ppc64 (patch by Miloslav Trmac)

* Tue May 10 2005 Miloslav Trmac <mitr@redhat.com> - 0.10.3-2
- Fix checking for numeric command prefix (#152953, patch by Jonas Fonseca)
- Fix invalid C causing assertion errors on ppc and ia64 (#156647)

* Mon Mar 21 2005 Karel Zak <kzak@redhat.com> 0.10.3-1
- sync with upstream; stable 0.10.3

* Sat Mar  5 2005 Karel Zak <kzak@redhat.com> 0.10.2-2
- rebuilt

* Tue Feb  8 2005 Karel Zak <kzak@redhat.com> 0.10.2-1
- sync with upstream; stable 0.10.2

* Fri Jan 28 2005 Karel Zak <kzak@redhat.com> 0.10.1-1
- sync with upstream; stable 0.10.1

* Thu Oct 14 2004 Karel Zak <kzak@redhat.com> 0.9.2-2
- the "Linux" driver seems better than "VT100" for xterm (#128105)

* Wed Oct  6 2004 Karel Zak <kzak@redhat.com> 0.9.2-1
- upload new upstream tarball with stable 0.9.2 release

* Mon Sep 20 2004 Jindrich Novy <jnovy@redhat.com> 0.9.2-0.rc7.4
- 0.9.2rc7.
- changed summary in spec to get rid of #41732, #61499

* Mon Sep 13 2004 Tim Waugh <twaugh@redhat.com> 0.9.2-0.rc4.3
- Avoid symbol clash (bug #131170).

* Fri Aug  6 2004 Tim Waugh <twaugh@redhat.com> 0.9.2-0.rc4.2
- 0.9.2rc4.

* Mon Jul 12 2004 Tim Waugh <twaugh@redhat.com> 0.9.2-0.rc2.2
- Fix elinks -dump -stdin (bug #127624).

* Thu Jul  1 2004 Tim Waugh <twaugh@redhat.com> 0.9.2-0.rc2.1
- 0.9.2rc2.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun  2 2004 Tim Waugh <twaugh@redhat.com> 0.9.1-3
- Build with LFS support (bug #125064).

* Fri May 28 2004 Tim Waugh <twaugh@redhat.com> 0.9.1-2
- Use UTF-8 by default (bug #76445).

* Thu Mar 11 2004 Tim Waugh <twaugh@redhat.com> 0.9.1-1
- 0.9.1.
- Use %%find_lang.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Dec  8 2003 Tim Waugh <twaugh@redhat.com> 0.4.3-1
- 0.4.3.
- Updated pkgconfig patch.

* Mon Aug 11 2003 Tim Waugh <twaugh@redhat.com> 0.4.2-7.1
- Rebuilt.

* Mon Aug 11 2003 Tim Waugh <twaugh@redhat.com> 0.4.2-7
- Don't require XFree86-libs (bug #102072).

* Tue Jul 22 2003 Nalin Dahyabhai <nalin@redhat.com> 0.4.2-6.2
- rebuild

* Thu Jun 12 2003 Tim Waugh <twaugh@redhat.com> 0.4.2-6.1
- Rebuilt.

* Thu Jun 12 2003 Tim Waugh <twaugh@redhat.com> 0.4.2-6
- Make getaddrinfo call use AI_ADDRCONFIG.
- Don't put so much information in the user-agent header string (bug #97273).

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jun  2 2003 Tim Waugh <twaugh@redhat.com> 0.4.2-4.1
- Rebuild again.

* Mon Jun  2 2003 Tim Waugh <twaugh@redhat.com> 0.4.2-4
- Rebuild.

* Mon May 12 2003 Tim Waugh <twaugh@redhat.com> 0.4.2-3
- Prevent crash when HOME is unset (bug #90663).

* Sun May 04 2003 Florian La Roche <Florian.LaRoche@redhat.de> 0.4.2-2
- use relative symlinks to elinks

* Wed Feb  5 2003 Tim Waugh <twaugh@redhat.com> 0.4.2-1
- 0.4.2 (bug #83273).

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 0.3.2-5
- rebuilt

* Thu Jan 16 2003 Tim Waugh <twaugh@redhat.com>
- Fix URL (bug #81987).

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 0.3.2-4
- rebuild

* Mon Dec 23 2002 Tim Waugh <twaugh@redhat.com> 0.3.2-3
- Fix bug #62368.

* Thu Dec 12 2002 Nalin Dahyabhai <nalin@redhat.com>
- use openssl's pkg-config data, if available

* Wed Nov 20 2002 Tim Powers <timp@redhat.com> 0.3.2-2
- rebuild on all arches

* Tue Aug 20 2002 Jakub Jelinek <jakub@redhat.com> 0.3.2-1
- update to 0.3.2 to fix the DNS Ctrl-C segfaults
- update URLs, the project moved
- include man page

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jan 24 2002 Tim Powers <timp@redhat.com>
- rebuilt against new openssl

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan  2 2002 Preston Brown <pbrown@redhat.com> 0.96-4
- cookie fix

* Thu Sep 13 2001 Bernhard Rosenkraenzer <bero@redhat.com> 0.96-3
- Save some more space in rescue mode

* Wed Jul 18 2001 Bernhard Rosenkraenzer <bero@redhat.com> 0.96-2
- Add the links manual from links.sourceforge.net (RFE #49228)

* Tue Jul  3 2001 Bernhard Rosenkraenzer <bero@redhat.com> 0.96-1
- update to 0.96

* Fri Jun 22 2001 Nalin Dahyabhai <nalin@redhat.com>
- actually run make in build phase

* Tue Jun 12 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Fri Mar  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Tue Jan  9 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.95

* Mon Jan  1 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.94 final

* Sun Dec 24 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- pre9

* Mon Dec 10 2000 Preston Brown <pbrown@redhat.com>
- Upgraded to pre8.

* Tue Dec  5 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.94pre7
- Minor fixes to the specfile (s/Copyright:/License:/)
- merge rescue stuff

* Fri Nov 24 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.94pre5

* Wed Nov 15 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.94pre4

* Tue Oct 24 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.94pre1

* Wed Aug  2 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.92 (needed - prior versions won't display XHTML properly)

* Thu Jul 20 2000 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment to work around bugs

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jun 15 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.84

* Sun Jun 11 2000 Preston Brown <pbrown@redhat.com>
- provides virtual package webclient.

* Thu Jan  6 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- initial RPM
