%global _hardened_build 1
%{?!with_python:      %global with_python      1}
%{?!with_perl:        %global with_perl        1}
%{?!with_ecc:        %global with_ecc          1}

%if %{with python}
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%{?filter_setup:
%global _ldns_internal_filter /^_ldns[.]so.*/d;
%filter_from_requires %{_ldns_internal_filter}
%filter_from_provides %{_ldns_internal_filter}
%filter_setup
}
%global _ldns_internal _ldns[.]so[.].*
%global __requires_exclude ^(%{_ldns_internal})$
%global __provides_exclude ^(%{_ldns_internal})$
%endif

%if %{with_perl}
%{?perl_default_filter}
%endif

Summary: Low-level DNS(SEC) library with API
Name: ldns
Version: 1.6.17
Release: 9%{?dist}

License: BSD
Url: http://www.nlnetlabs.nl/%{name}/
Source0: http://www.nlnetlabs.nl/downloads/%{name}/%{name}-%{version}.tar.gz
Patch1: ldns-1.6.17-multilib.patch
Patch2: ldns-1.6.16-dsa-key-failures.patch
Patch3: ldns-1.6.17-keygen.patch

# https://www.nlnetlabs.nl/bugs-script/show_bug.cgi?id=685
# https://bugzilla.redhat.com/show_bug.cgi?id=1230140
Patch4: ldns-1.6.17-doxyparse-perl-5-22-fix.patch

Group: System Environment/Libraries
# Only needed for builds from svn snapshot
# BuildRequires: libtool
# BuildRequires: autoconf
# BuildRequires: automake

BuildRequires: libpcap-devel
BuildRequires: openssl-devel
BuildRequires: gcc-c++
BuildRequires: doxygen

# for snapshots only
# BuildRequires: libtool, autoconf, automake
%if %{with python}
BuildRequires: python-devel, swig
%endif
%if %{with perl}
BuildRequires: perl-ExtUtils-MakeMaker
%endif
Requires: ca-certificates

# Transition: To ensure people who installed 'ldns' for binaries don't lose them. Remove in f21
Obsoletes: ldns < 1.6.17-4
Conflicts: ldns < 1.6.17-4
Provides: ldns = %{version}-%{release}
Provides: ldns%{?_isa} = %{version}-%{release}
Requires: ldns-utils

%description
ldns is a library with the aim to simplify DNS programming in C. All
low-level DNS/DNSSEC operations are supported. We also define a higher
level API which allows a programmer to (for instance) create or sign
packets.

%package devel
Summary: Development package that includes the ldns header files
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The devel package contains the ldns library and the include files

%package utils
Summary: DNS(SEC) utilities for querying dns
Group: Applications/System
Requires: %{name}%{?_isa} = %{version}-%{release}

%description utils
Collection of tools to get, check or alter DNS(SEC) data.

%if %{with python}
%package -n python-ldns
Summary: Python extensions for ldns
Group: Applications/System
Requires: %{name}%{?_isa} = %{version}-%{release}
Obsoletes: ldns-python < 1.6.17-4
Conflicts: ldns-python < 1.6.17-4


%description -n python-ldns
Python extensions for ldns
%endif

%if %{with perl}
%package -n perl-ldns
Summary: Perl extensions for ldns
Group: Applications/System
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Obsoletes: ldns-perl < 1.6.17-4
Conflicts: ldns-perl < 1.6.17-4

%description -n perl-ldns
Perl extensions for ldns
%endif

%package doc
Summary: Documentation for the ldns library
Group: Development/Libraries
BuildArch: noarch

%description doc
This package contains documentation for the ldns library

%prep
%setup -q
%patch1 -p1
%patch2 -p1 -b .dsa
%patch3 -p1 -b .keygen
%patch4 -p1
# To built svn snapshots
# rm config.guess config.sub ltmain.sh
# aclocal
# libtoolize -c --install
# autoreconf --install

%build
CFLAGS="%{optflags} -fPIC"
CXXFLAGS="%{optflags} -fPIC"
LDFLAGS="-Wl,-z,relro,-z,now -pie"
export CFLAGS CXXFLAGS LDFLAGS
%configure \
  --disable-rpath \
  --disable-static \
%if %{with ecc}
  --enable-gost \
  --enable-ecdsa \
%else
  --disable-gost \
  --disable-ecdsa \
%endif
%if %{with python}
  --with-pyldns \
%endif
  --with-ca-file=/etc/pki/tls/certs/ca-bundle.trust.crt \
  --with-ca-path=/etc/pki/tls/certs/ \
  --with-trust-anchor=%{_sharedstatedir}/unbound/root.key

pushd drill
%configure \
  --disable-rpath \
%if %{with ecc}
  --enable-gost \
  --enable-ecdsa \
%else
  --disable-gost \
  --disable-ecdsa \
%endif
  --with-ca-file=/etc/pki/tls/certs/ca-bundle.trust.crt \
  --with-ca-path=/etc/pki/tls/certs/ \
  --with-trust-anchor=%{_sharedstatedir}/unbound/root.key
popd

pushd examples
%configure \
  --disable-rpath \
%if %{with ecc}
  --enable-gost \
  --enable-ecdsa \
%else
  --disable-gost \
  --disable-ecdsa \
%endif
  --with-ca-file=/etc/pki/tls/certs/ca-bundle.trust.crt \
  --with-ca-path=/etc/pki/tls/certs/ \
  --with-trust-anchor=%{_sharedstatedir}/unbound/root.key
popd

# We cannot use the built-in --with-p5-dns-ldns
%if %{with perl}
  pushd contrib/DNS-LDNS
  perl Makefile.PL INSTALLDIRS=vendor  INC="-I. -I../.."
  make
  popd
%endif

make %{?_smp_mflags}
make -C drill %{?_smp_mflags}
make -C examples %{?_smp_mflags}
make %{?_smp_mflags} doc

%install
rm -rf %{buildroot}

make DESTDIR=%{buildroot} INSTALL="%{__install} -p" install
make DESTDIR=%{buildroot} INSTALL="%{__install} -p" install-doc

# don't package xml files
rm doc/*.xml
# don't package building script for install-doc in doc section
rm doc/doxyparse.pl
# remove double set of man pages
rm -rf doc/man
# remove .la files
rm -rf %{buildroot}%{_libdir}/*.la %{buildroot}%{python_sitearch}/*.la
make -C drill DESTDIR=%{buildroot} install
make -C examples DESTDIR=%{buildroot} install
%if %{with perl}
  make -C contrib/DNS-LDNS DESTDIR=%{buildroot} pure_install
  chmod 755 %{buildroot}%{perl_vendorarch}/auto/DNS/LDNS/LDNS.so
  rm -f %{buildroot}%{perl_vendorarch}/auto/DNS/LDNS/{.packlist,LDNS.bs}
%endif

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc README LICENSE
%{_libdir}/libldns*so.*

%files utils
%{_bindir}/drill
%{_bindir}/ldnsd
%{_bindir}/ldns-chaos
%{_bindir}/ldns-compare-zones
%{_bindir}/ldns-[d-z]*
%{_mandir}/man1/*

%files devel
%doc Changelog README
%{_libdir}/libldns*so
%{_bindir}/ldns-config
%dir %{_includedir}/ldns
%{_includedir}/ldns/*.h
%{_mandir}/man3/*

%if %{with python}
%files -n python-ldns
%{python_sitearch}/*
%endif

%if %{with perl}
%files -n perl-ldns
%{perl_vendorarch}/*
%exclude %dir %{perl_vendorarch}/auto/
%endif

%files doc
%doc doc

%changelog
* Tue Nov 10 2015 Liu Di <liudidi@gmail.com> - 1.6.17-9
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 1.6.17-8
- 为 Magic 3.0 重建

* Thu Sep 17 2015 Liu Di <liudidi@gmail.com> - 1.6.17-7
- 为 Magic 3.0 重建

* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 1.6.17-6
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Liu Di <liudidi@gmail.com> - 1.6.17-5
- 为 Magic 3.0 重建

* Tue May 06 2014 Paul Wouters <pwouters@redhat.com> - 1.6.17-4
- Rename ldns-python to python-ldns
- Rename ldns-perl to perl-ldns
- Ensure ldns-utils is dragged it so an upgrade does not remove utils

* Tue May 06 2014 Paul Wouters <pwouters@redhat.com> - 1.6.17-3
- CVE-2014-3209 ldns: ldns-keygen generates keys with world readable permissions
- Fix 1017958 - 32 and 64 bit ldns conflicts on some manual pages
- Fix rhbz#1062874 - cannot install ldns.x86_64 in parallel to ldns.i686
- Incorporate fixes from Tuomo Soini <tis@foobar.fi>
- hardened build
- fix ldns internal provides and requires filter
- fix perl-ldns requirement to include %%_isa
- setup filters for perl and python bindings for internal stuff
- split utils to separate package

* Mon Mar 24 2014 Tomas Hozza <thozza@redhat.com> - 1.6.17-2
- Fix error causing ldns to sometimes produce faulty DSA sign (#1077776)
- Fix FTBFS due to perl modules

* Fri Jan 10 2014 Paul Wouters <pwouters@redhat.com> - 1.6.17-1
- Updated to 1.6.17
- Enable perl bindings via new ldns-perl sub-package
- Enable ECDSA/GOST which is now allowed in Fedora
- Removed patches merged upstream, ported multilib patch to 1.6.17

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Tomas Hozza <thozza@redhat.com> - 1.6.16-5
- Fix compiler warnings and one uninitialized value
- make ldns-config multilib clean
- Fix man pages and usages errors

* Mon Jun 03 2013 Paul Wouters <pwouters@redhat.com> - 1.6.16-4
- Use /var/lib/unbound/root.key for --with-trust-anchor

* Fri Apr 19 2013 Adam Tkac <atkac redhat com> - 1.6.16-3
- make package multilib clean

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 30 2012 Paul Wouters <pwouters@redhat.com> - 1.6.16-1
- Updated to 1.6.16
- Addresses bug in 1.6.14 and 1.6.15 that affects opendnssec
  (if you have empty non-terminals and use NSEC3)

* Fri Oct 26 2012 Paul Wouters <pwouters@redhat.com> - 1.6.15-1
- Updated to 1.6.15, as 1.6.14 accidentally broke ABI
  (We never released 1.6.14)

* Tue Oct 23 2012 Paul Wouters <pwouters@redhat.com> - 1.6.14-1
- [pulled before release]
- Updated to 1.6.14
- Removed merged in patch
- Added new dependancy on ca-certificates for ldns-dane PKIX validation

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 01 2012 Paul Wouters <pwouters@redhat.com> - 1.6.13-2
- Added reworked ldns-read-zone patch from trunk
  (adds -p for SOA padding, and -o for zeroizing timestamps/sigs)

* Mon May 21 2012 Paul Wouters <pwouters@redhat.com> - 1.6.13-1
- Upgraded to 1.6.13, bugfix release
- Added --disable-ecdsa as ECC is still banned
- Removed --with-sha2 - it is always enabled and option was removed

* Wed Jan 11 2012 Paul Wouters <paul@nohats.ca> - 1.6.12-1
- Upgraded to 1.6.12, fixes important end of year handling date bug

* Wed Oct  5 2011 Paul Wouters <paul@xelerance.com> - 1.6.11-2
- Updated to 1.6.11, fixes rhbz#741026 which is CVE-2011-3581
- Python goes into sitearch, not sitelib
- Fix source link and spelling errors in description

* Mon Sep 19 2011 Paul Wouters <paul@xelerance.com> - 1.6.10-2
- Fix for losing nameserver when it drops UDP fragments in
  ldns_resolver_send_pkt [Willem Toorop <willem@NLnetLabs.nl>]
- Added ldnsx module (to be merged into ldns soon)
  http://git.xelerance.com/cgi-bin/gitweb.cgi?p=ldnsx.git;a=summary

* Wed Jun 08 2011 Paul Wouters <paul@xelerance.com> - 1.6.10-1
- Upodated to 1.6.10
- Commented out dependancies that are only needed for snapshots

* Sun Mar 27 2011 Paul Wouters <paul@xelerance.com> - 1.6.9-1
- Updated to 1.6.9

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 24 2011 Paul Wouters <paul@xelerance.com> - 1.6.8-1
- Updated to 1.6.8

* Thu Aug 26 2010 Paul Wouters <paul@xelerance.com> - 1.6.6-2
- Bump for EVR

* Mon Aug 09 2010 Paul Wouters <paul@xelerance.com> - 1.6.6-1
- Upgraded to 1.6.6

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jun 15 2010 Paul Wouters <paul@xelerance.com> - 1.6.5-1
- Updated to 1.6.5

* Fri Jan 22 2010 Paul Wouters <paul@xelerance.com> - 1.6.4-2
- Fix missing _ldns.so causing ldns-python to not work
- Patch for installing ldns-python files
- Patch for rpath in ldns-python
- Don't install .a file for ldns-python

* Wed Jan 20 2010 Paul Wouters <paul@xelerance.com> - 1.6.4-1
- Upgraded to 1.6.4. 
- Added ldns-python sub package

* Fri Dec 04 2009 Paul Wouters <paul@xelerance.com> - 1.6.3-1
- Upgraded to 1.6.3, which has minor bugfixes

* Fri Nov 13 2009 Paul Wouters <paul@xelerance.com> - 1.6.2-1
- Upgraded to 1.6.2. This fixes various bugs.
  (upstream released mostly to default with sha2 for the imminent
   signed root, but we already enabled that in our builds)

* Tue Aug 25 2009 Tomas Mraz <tmraz@redhat.com> - 1.6.1-3
- rebuilt with new openssl

* Sun Aug 16 2009 Paul Wouters <paul@xelerance.com> - 1.6.1-2
- Added openssl dependancy back in, since we get more functionality
 when using openssl. Especially in 'drill'.

* Sun Aug 16 2009 Paul Wouters <paul@xelerance.com> - 1.6.1-1
- Updated to 1.6.1

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Paul Wouters <paul@xelerance.com> - 1.6.0-4
- Fixed the ssl patch so it can now compile --without-ssl

* Sat Jul 11 2009 Paul Wouters <paul@xelerance.com> - 1.6.0-3
- Added patch to compile with --without-ssl
- Removed openssl dependancies
- Recompiled with --without-ssl

* Sat Jul 11 2009 Paul Wouters <paul@xelerance.com> - 1.6.0-2
- Updated to 1.6.0
- (did not yet compile with --without-ssl due to compile failures)

* Fri Jul 10 2009 Paul Wouters <paul@xelerance.com> - 1.6.0-1
- Updated to 1.6.0
- Compile without openssl

* Thu Apr 16 2009 Paul Wouters <paul@xelerance.com> - 1.5.1-4
- Memory management bug when generating a sha256 key, see:
  https://bugzilla.redhat.com/show_bug.cgi?id=493953

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 10 2009 Paul Wouters <paul@xelerance.com> - 1.5.1-1
- Updated to new version, 1.5.0 had a bug preventing
  zone signing.

* Mon Feb  9 2009 Paul Wouters <paul@xelerance.com> - 1.5.0-1
- Updated to new version

* Thu Feb 05 2009 Adam Tkac <atkac redhat com> - 1.4.0-3
- fixed configure flags

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 1.4.0-2
- rebuild with new openssl

* Fri Nov  7 2008 Paul Wouters <paul@xelerance.com> - 1.4.0-1
- Updated to 1.4.0

* Wed May 28 2008 Paul Wouters <paul@xelerance.com> - 1.3.0-3
- enable SHA2 functionality

* Wed May 28 2008 Paul Wouters <paul@xelerance.com> - 1.3.0-2
- re-tag (don't do builds while renaming local repo dirs)

* Wed May 28 2008 Paul Wouters <paul@xelerance.com> - 1.3.0-1
- Updated to latest release

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.2-3
- Autorebuild for GCC 4.3

* Wed Dec  5 2007 Paul Wouters <paul@xelerance.com> - 1.2.2-2
- Rebuild for new libcrypto

* Thu Nov 29 2007 Paul Wouters <paul@xelerance.com> - 1.2.2-1
- Upgraded to 1.2.2. Removed no longer needed race workaround

* Tue Nov 13 2007 Paul Wouters <paul@xelerance.com> - 1.2.1-4
- Try to fix racing ln -s statements in parallel builds

* Fri Nov  9 2007 Paul Wouters <paul@xelerance.com> - 1.2.1-3
- Added patch for ldns-read-zone that does not put @. in RRDATA

* Fri Oct 19 2007 Paul Wouters <paul@xelerance.com> - 1.2.1-2
- Use install -p to work around multilib conflicts for .h files

* Wed Oct 10 2007 Paul Wouters <paul@xelerance.com> - 1.2.1-1
- Updated to 1.2.1
- Removed patches that got moved into upstream

* Wed Aug  8 2007 Paul Wouters <paul@xelerance.com> 1.2.0-11
- Patch for ldns-key2ds to write to stdout
- Again remove extra set of man pages from doc
- own /usr/include/ldns (bug 233858)

* Wed Aug  8 2007 Paul Wouters <paul@xelerance.com> 1.2.0-10
- Added sha256 DS record patch to ldns-key2ds
- Minor tweaks for proper doc/man page installation.
- Workaround for parallel builds

* Mon Aug  6 2007 Paul Wouters <paul@xelerance.com> 1.2.0-2
- Own the /usr/include/ldns directory (bug #233858)
- Removed obsoleted patch
- Remove files form previous libtool run accidentally packages by upstream

* Mon Sep 11 2006 Paul Wouters <paul@xelerance.com> 1.0.1-4
- Commented out 1.1.0 make targets, put make 1.0.1 targets.

* Mon Sep 11 2006 Paul Wouters <paul@xelerance.com> 1.0.1-3
- Fixed changelog typo in date
- Rebuild requested for PT_GNU_HASH support from gcc
- Did not upgrade to 1.1.0 due to compile issues on x86_64

* Fri Jan  6 2006 Paul Wouters <paul@xelerance.com> 1.0.1-1
- Upgraded to 1.0.1. Removed temporary clean hack from spec file.

* Sun Dec 18 2005 Paul Wouters <paul@xelerance.com> 1.0.0-8
- Cannot use make clean because there are no Makefiles. Use hardcoded rm.

* Sun Dec 18 2005 Paul Wouters <paul@xelerance.com> 1.0.0-7
- Patched 'make clean' target to get rid of object files shipped with 1.0.0

* Tue Dec 13 2005 Paul Wouters <paul@xelerance.com> 1.0.0-6
- added a make clean for 2.3.3 since .o files were left behind upstream,
  causing failure on ppc platform

* Sun Dec 11 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.0.0-5
- minor cleanups

* Wed Oct  5 2005 Paul Wouters <paul@xelerance.com> 0.70_1205
- reworked for svn version

* Sun Sep 25 2005 Paul Wouters <paul@xelerance.com> - 0.70
- Initial version
