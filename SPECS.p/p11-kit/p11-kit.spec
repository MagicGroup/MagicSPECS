Name:           p11-kit
Version:        0.20.2
Release:        2%{?dist}
Summary:        Library for loading and sharing PKCS#11 modules

License:        BSD
URL:            http://p11-glue.freedesktop.org/p11-kit.html
Source0:        http://p11-glue.freedesktop.org/releases/p11-kit-%{version}.tar.gz
Source1:        trust-extract-compat
BuildRequires:  libtasn1-devel >= 2.3
BuildRequires:  nss-softokn-freebl
BuildRequires:  libffi-devel
BuildRequires:  gtk-doc

%description
p11-kit provides a way to load and enumerate PKCS#11 modules, as well
as a standard configuration setup for installing PKCS#11 modules in
such a way that they're discoverable.


%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package trust
Summary:        System trust module from %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires(post):   %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
Conflicts:        nss < 3.14.3-9

%description trust
The %{name}-trust package contains a system trust PKCS#11 module which
contains certificate anchors and black lists.


# solution taken from icedtea-web.spec
%define multilib_arches ppc64 sparc64 x86_64 ppc64le
%ifarch %{multilib_arches}
%define alt_ckbi  libnssckbi.so.%{_arch}
%else
%define alt_ckbi  libnssckbi.so
%endif


%prep
%setup -q

%build
# These paths are the source paths that  come from the plan here:
# https://fedoraproject.org/wiki/Features/SharedSystemCertificates:SubTasks
%configure --disable-static --enable-doc --with-trust-paths=%{_sysconfdir}/pki/ca-trust/source:%{_datadir}/pki/ca-trust-source --with-hash-impl=freebl --disable-silent-rules
make %{?_smp_mflags} V=1

%install
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pkcs11/modules
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/pkcs11/*.la
install -p -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_libdir}/p11-kit/
# Install the example conf with %%doc instead
rm $RPM_BUILD_ROOT%{_sysconfdir}/pkcs11/pkcs11.conf.example

%check
make check


%post -p /sbin/ldconfig

%post trust
%{_sbindir}/update-alternatives --install %{_libdir}/libnssckbi.so \
        %{alt_ckbi} %{_libdir}/pkcs11/p11-kit-trust.so 30

%postun -p /sbin/ldconfig

%postun trust
if [ $1 -eq 0 ] ; then
        # package removal
        %{_sbindir}/update-alternatives --remove %{alt_ckbi} %{_libdir}/pkcs11/p11-kit-trust.so
fi


%files
%doc AUTHORS COPYING NEWS README
%doc p11-kit/pkcs11.conf.example
%dir %{_sysconfdir}/pkcs11
%dir %{_sysconfdir}/pkcs11/modules
%dir %{_datadir}/p11-kit
%dir %{_datadir}/p11-kit/modules
%dir %{_libdir}/p11-kit
%{_bindir}/p11-kit
%{_libdir}/libp11-kit.so.*
%{_libdir}/p11-kit-proxy.so
%{_mandir}/man1/trust.1.gz
%{_mandir}/man8/p11-kit.8.gz
%{_mandir}/man5/pkcs11.conf.5.gz

%files devel
%{_includedir}/p11-kit-1/
%{_libdir}/libp11-kit.so
%{_libdir}/pkgconfig/p11-kit-1.pc
%doc %{_datadir}/gtk-doc/

%files trust
%{_bindir}/trust
%dir %{_libdir}/pkcs11
%{_libdir}/pkcs11/p11-kit-trust.so
%{_datadir}/p11-kit/modules/p11-kit-trust.module
%{_libdir}/p11-kit/trust-extract-compat


%changelog
* Sat Jan 25 2014 Ville Skyttä <ville.skytta@iki.fi> - 0.20.2-2
- Own the %%{_libdir}/pkcs11 dir in -trust.

* Tue Jan 14 2014 Stef Walter <stefw@redhat.com> - 0.20.2-1
- Update to upstream stable 0.20.2 release
- Fix regression involving blacklisted anchors [#1041328]
- Support ppc64le in build [#1052707]

* Mon Sep 09 2013 Stef Walter <stefw@redhat.com> - 0.20.1-1
- Update to upstream stable 0.20.1 release
- Extract compat trust data after we've changes
- Skip compat extraction if running as non-root
- Better failure messages when removing anchors

* Thu Aug 29 2013 Stef Walter <stefw@redhat.com> - 0.19.4-1
- Update to new upstream 0.19.4 release

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Stef Walter <stefw@redhat.com> - 0.19.3-1
- Update to new upstream 0.19.3 release (#967822)

* Wed Jun 05 2013 Stef Walter <stefw@redhat.com> - 0.18.3-1
- Update to new upstream stable release
- Fix intermittent firefox cert validation issues (#960230)
- Include the manual pages in the package

* Tue May 14 2013 Stef Walter <stefw@redhat.com> - 0.18.2-1
- Update to new upstream stable release
- Reduce the libtasn1 dependency minimum version

* Thu May 02 2013 Stef Walter <stefw@redhat.com> - 0.18.1-1
- Update to new upstream stable release
- 'p11-kit extract-trust' lives in libdir

* Thu Apr 04 2013 Stef Walter <stefw@redhat.com> - 0.18.0-1
- Update to new upstream stable release
- Various logging tweaks (#928914, #928750)
- Make the 'p11-kit extract-trust' explicitly reject
  additional arguments

* Thu Mar 28 2013 Stef Walter <stefw@redhat.com> - 0.17.5-1
- Make 'p11-kit extract-trust' call update-ca-trust
- Work around 32-bit oveflow of certificate dates
- Build fixes

* Tue Mar 26 2013 Stef Walter <stefw@redhat.com> - 0.17.4-2
- Pull in patch from upstream to fix build on ppc (#927394)

* Wed Mar 20 2013 Stef Walter <stefw@redhat.com> - 0.17.4-1
- Update to upstream version 0.17.4

* Mon Mar 18 2013 Stef Walter <stefw@redhat.com> - 0.17.3-1
- Update to upstream version 0.17.3
- Put the trust input paths in the right order

* Tue Mar 12 2013 Stef Walter <stefw@redhat.com> - 0.16.4-1
- Update to upstream version 0.16.4

* Fri Mar 08 2013 Stef Walter <stefw@redhat.com> - 0.16.3-1
- Update to upstream version 0.16.3
- Split out system trust module into its own package.
- p11-kit-trust provides an alternative to an nss module

* Tue Mar 05 2013 Stef Walter <stefw@redhat.com> - 0.16.1-1
- Update to upstream version 0.16.1
- Setup source directories as appropriate for Shared System Certificates feature

* Tue Mar 05 2013 Stef Walter <stefw@redhat.com> - 0.16.0-1
- Update to upstream version 0.16.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Sep 17 2012 Kalev Lember <kalevlember@gmail.com> - 0.14-1
- Update to 0.14

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Kalev Lember <kalevlember@gmail.com> - 0.13-1
- Update to 0.13

* Tue Mar 27 2012 Kalev Lember <kalevlember@gmail.com> - 0.12-1
- Update to 0.12
- Run self tests in %%check

* Sat Feb 11 2012 Kalev Lember <kalevlember@gmail.com> - 0.11-1
- Update to 0.11

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Matthias Clasen <mclasen@redhat.com> - 0.9-1
- Update to 0.9

* Wed Oct 26 2011 Kalev Lember <kalevlember@gmail.com> - 0.8-1
- Update to 0.8

* Mon Sep 19 2011 Matthias Clasen <mclasen@redhat.com> - 0.6-1
- Update to 0.6

* Sun Sep 04 2011 Kalev Lember <kalevlember@gmail.com> - 0.5-1
- Update to 0.5

* Sun Aug 21 2011 Kalev Lember <kalevlember@gmail.com> - 0.4-1
- Update to 0.4
- Install the example config file to documentation directory

* Wed Aug 17 2011 Kalev Lember <kalevlember@gmail.com> - 0.3-2
- Tighten -devel subpackage deps (#725905)

* Fri Jul 29 2011 Kalev Lember <kalevlember@gmail.com> - 0.3-1
- Update to 0.3
- Upstream rewrote the ASL 2.0 bits, which makes the whole package
  BSD-licensed

* Tue Jul 12 2011 Kalev Lember <kalevlember@gmail.com> - 0.2-1
- Initial RPM release
