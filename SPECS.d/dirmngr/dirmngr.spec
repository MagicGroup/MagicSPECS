
# Fedora Review: http://bugzilla.redhat.com/171289

Name:	 dirmngr
Summary: Client for Managing/Downloading CRLs
Version: 1.1.1
Release: 2%{?dist}

License: GPLv3+
Group:	 System Environment/Libraries
URL:	 http://www.gnupg.org/
Source0: ftp://ftp.gnupg.org/gcrypt/dirmngr/dirmngr-%{version}.tar.bz2
Source1: ftp://ftp.gnupg.org/gcrypt/dirmngr/dirmngr-%{version}.tar.bz2.sig

Source10: dirmngr.conf
Source11: ldapservers.conf
Source12: dirmngr.logrotate
Source13: dirmngrtmp.conf

Patch1:  dirmngr-1.1.0-ocsp-crash.patch

BuildRequires: gawk
BuildRequires: gettext
BuildRequires: libassuan-devel >= 2.0.0
BuildRequires: libgcrypt-devel
BuildRequires: libksba-devel
BuildRequires: openldap-devel
BuildRequires: pth-devel

Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Requires: logrotate

%description
Dirmngr is a server for managing and downloading certificate
revocation lists (CRLs) for X.509 certificates and for downloading
the certificates themselves. Dirmngr also handles OCSP requests as
an alternative to CRLs. Dirmngr is either invoked internally by
gpgsm (from gnupg2) or when running as a system daemon through
the dirmngr-client tool.


%prep
%setup -q
%patch1 -p1 -b .crash

pushd doc
iconv -f iso-8859-1 -t utf-8 dirmngr.texi -o dirmngr.texi.NEW && mv dirmngr.texi.NEW dirmngr.texi
iconv -f iso-8859-1 -t utf-8 dirmngr.info -o dirmngr.info.NEW && mv dirmngr.info.NEW dirmngr.info
popd


%build

# FIX for https://bugzilla.redhat.com/565131
# not sure how best to turn this into something more upstreamable
# patch configure to try this combo first? -- Rex
export LDAPLIBS="-lldap -llber"

%configure \
  --disable-dependancy-tracking

make %{?_smp_mflags}


%install

# dirs
mkdir -p %{buildroot}%{_sysconfdir}/dirmngr/trusted-certs
mkdir -p %{buildroot}%{_var}/cache/dirmngr/crls.d
mkdir -p %{buildroot}%{_var}/lib/dirmngr/extra-certs
mkdir -p %{buildroot}%{_var}/log/dirmngr
mkdir -p %{buildroot}%{_var}/run/dirmngr

make install DESTDIR=%{buildroot}

# dirmngr.log, logrotate
install -p -m644 -D %{SOURCE12} %{buildroot}%{_sysconfdir}/logrotate.d/dirmngr

# conf files
install -p -m644 %{SOURCE10} %{SOURCE11} %{buildroot}%{_sysconfdir}/dirmngr/

# autocreate /var/run/dirmngr on boot
install -p -m644 -D %{SOURCE13} %{buildroot}%{_prefix}/lib/tmpfiles.d/dirmngr.conf

%find_lang %{name}

## unpackaged files
rm -f %{buildroot}%{_infodir}/dir
rm -rf %{buildroot}%{_docdir}/dirmngr/examples


%check
make check


%post
/sbin/install-info %{_infodir}/dirmngr.info.gz %{_infodir}/dir ||:

%preun
if [ $1 -eq 0 ]; then
  /sbin/install-info --delete %{_infodir}/dirmngr.info.gz %{_infodir}/dir ||:
fi


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING README ChangeLog NEWS
%doc doc/examples
%{_bindir}/dirmngr*
%{_libexecdir}/dirmngr_ldap
%{_infodir}/dirmngr.info*
%{_mandir}/man1/*
# TODO/FIXME
#{_initrddir}/*
## files/dirs for --daemon mode
%dir %{_sysconfdir}/dirmngr
%config(noreplace) %{_sysconfdir}/dirmngr/*.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/*
%{_prefix}/lib/tmpfiles.d/*.conf
%{_var}/cache/dirmngr/
%{_var}/lib/dirmngr/
%{_var}/log/dirmngr/
%dir %{_var}/run/dirmngr


%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 29 2013 Tomáš Mráz <tmraz@redhat.com> - 1.1.1-1
- new upstream release

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Tomas Mraz <tmraz@redhat.com> - 1.1.0-6
- upstream fix for CVE-2011-2207 (blocking other request processing
  when one CRL request is being processed) (#710529)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec  1 2010 Tomas Mraz <tmraz@redhat.com> - 1.1.0-4
- fix crash on some OCSP responses (patch by Tomas Trnka) (#658230)

* Thu Nov 25 2010 Tomas Mraz <tmraz@redhat.com> - 1.1.0-3
- revert ghosting the /var/run/dirmngr so we do not need to create
  it in the post script

* Wed Nov 24 2010 Tomas Mraz <tmraz@redhat.com> - 1.1.0-2
- make /var/run/dirmngr ghost and create it with tmpfiles (#656573)

* Tue Aug 10 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.1.0-1
- dirmngr-1.1.0

* Mon Feb 15 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.0.3-6
- FTBFS dirmngr-1.0.3-5.fc13 (#565131)

* Mon Jan 11 2010 Tomas Mraz <tmraz@redhat.com> - 1.0.3-5
- better ldapservers.conf file
- correct the license field

* Tue Dec  8 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0.3-4
- Explicitly BR libassuan-static in accordance with the Packaging
  Guidelines (libassuan-devel is still static-only).

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 22 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.3-2
- fix info scriptlet (uninstall)

* Wed Jun 17 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.3-1
- dirmngr-1.0.3

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Aug 01 2008 Rex Dieter <rdieter@fedoraproject.org> 1.0.2-1
- dirmngr-1.0.2

* Mon Feb 11 2008 Rex Dieter <rdieter@fedoraproject.org> 1.0.1-2
- respin (gcc43)

* Thu Jan 03 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.1-1
- dirmngr-1.0.1

* Tue Dec 04 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.0-7
- respin for openldap 

* Wed Oct 03 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.0-6
- /var/log/dirmngr.log -> /var/log/dirmngr/dirmngr.log
- remove use of %%ghost (e.g. dirmngr.log shouldn't be owned)
- BR: gettext

* Sun Aug 26 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.0-5
- BR: gawk

* Sat Aug 25 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.0-4
- respin (BuildID)

* Thu Aug 09 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.0-3
- License: GPLv2+

* Wed Nov 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0.0-2
- dirmngr-1.0.0

* Mon Nov 13 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.6-2
- BR: libassuan-static

* Tue Sep 05 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.6-1
- dirmngr-0.9.6

* Tue Aug 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.4-5
- fc6 respin

* Mon Jun 26 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.4-4
- %%config(noreplace) %%_sysconfdir/logrotate.d/dirmngr

* Mon Jun 26 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.4-3
- use 'iconv -f iso-8859-1 -t utf-8' to avoid dropping characters

* Mon Jun 26 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.4-2
- remove non-ASCII chars from dirmngr.info
- %%config %%_sysconfdir/logrotate.d/dirmngr

* Mon Jun 26 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.4-1
- 0.9.4
- %%doc COPYING
- drop upstreamed info patch
- use logrotate on dirmngr.log
- add comment to (previously) empty ldapservers.conf

* Tue May 16 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.3-1
- 0.9.3

* Sat Oct 22 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.2-3
- create/own more files/dirs for --daemon mode
- TODO: proper init script

* Thu Oct 20 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.2-2
- drop BR: libgpg-error-devel, texinfo
- drop goofy conditional 'make install-strip '
- BR: libksba-devel >= 0.9.11
- BR: libassuan-devel >= 0.6.8
- fix spelling error(s) in %%description
- --disable-dependancy-tracking

* Thu Oct 20 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.2-1
- 0.9.2

* Mon Mar 21 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.1-0.fdr.1
- 0.9.1

* Fri Jan 07 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.0-0.fdr.2
- fix info entry (so deletion/uninstallation works)

* Fri Jan 07 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.0-0.fdr.1
- 0.9.0

* Thu Dec 16 2004 Rex Dieter <rexdieter[AT]users.sf.net> 0.5.5-0.fdr.2
- 64bit fix (look for openldap in %%_libdir, not just /usr/lib)

* Wed Oct 20 2004 Rex Dieter <rexdieter[AT]users.sf.net> 0.5.5-0.fdr.1
- first try

