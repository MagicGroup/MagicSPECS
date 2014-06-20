%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           ocaml-cryptokit
Version:        1.9
Release:        2%{?dist}
Summary:        OCaml library of cryptographic and hash functions
License:        LGPLv2 with exceptions

URL:            http://forge.ocamlcore.org/projects/cryptokit/
Source0:        https://forge.ocamlcore.org/frs/download.php/1229/cryptokit-%{version}.tar.gz

ExcludeArch:    sparc64 s390 s390x

BuildRequires:  ocaml
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-findlib-devel
BuildRequires:  zlib-devel
BuildRequires:  chrpath


%description
The Cryptokit library for Objective Caml provides a variety of
cryptographic primitives that can be used to implement cryptographic
protocols in security-sensitive applications. The primitives provided
include:

* Symmetric-key cryptography: AES, DES, Triple-DES, ARCfour, in ECB,
  CBC, CFB and OFB modes.
* Public-key cryptography: RSA encryption and signature; Diffie-Hellman
  key agreement.
* Hash functions and MACs: SHA-1, SHA-256, RIPEMD-160, MD5, and MACs
  based on AES and DES.
* Random number generation.
* Encodings and compression: base 64, hexadecimal, Zlib compression. 

Additional ciphers and hashes can easily be used in conjunction with
the library. In particular, basic mechanisms such as chaining modes,
output buffering, and padding are provided by generic classes that can
easily be composed with user-provided ciphers. More generally, the
library promotes a "Lego"-like style of constructing and composing
transformations over character streams.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%setup -q -n cryptokit-%{version}
./configure --destdir $RPM_BUILD_ROOT


%build
# Some sort of circular dependency, so sometimes the first make fails.
# Just run make twice.
make ||:
make

chrpath --delete _build/src/dllcryptokit_stubs.so


%check
# This opens /dev/random but never reads from it.
make test


%install
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/ocaml
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/ocaml/stublibs
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT/%{_libdir}/ocaml
make install


%files
%doc LICENSE.txt
%{_libdir}/ocaml/cryptokit
%if %opt
%exclude %{_libdir}/ocaml/cryptokit/*.a
%exclude %{_libdir}/ocaml/cryptokit/*.cmxa
#%exclude %{_libdir}/ocaml/cryptokit/*.cmx
%endif
%exclude %{_libdir}/ocaml/cryptokit/*.mli
%{_libdir}/ocaml/stublibs/*.so*


%files devel
%doc README.txt LICENSE.txt Changes
%if %opt
%{_libdir}/ocaml/cryptokit/*.a
%{_libdir}/ocaml/cryptokit/*.cmxa
#%{_libdir}/ocaml/cryptokit/*.cmx
%endif
%{_libdir}/ocaml/cryptokit/*.mli


%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 1.9-1
- New upstream version 1.9.
- Rebuild for OCaml 4.01.0.
- Enable debuginfo.
- Modernize the spec file.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Dec 02 2012 Bruno Wolff III <bruno@wolff.to> - 1.6-3
- Rebuild for ocaml 4.0.1.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul  2 2012 Richard W.M. Jones <rjones@redhat.com> - 1.6-1
- New upstream version 1.6.

* Sun Jun 10 2012 Richard W.M. Jones <rjones@redhat.com> - 1.4-6
- Rebuild for OCaml 4.00.0.

* Thu Jan 12 2012 Richard W.M. Jones <rjones@redhat.com> - 1.4-5
- Rebuild for OCaml 3.12.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan  5 2011 Richard W.M. Jones <rjones@redhat.com> - 1.4-3
- New upstream version 1.4.
- Project has moved to a new location.
- META file is included in the project.
- Rebuild for OCaml 3.12.0.
- Build system changed.
- *.cmx files are no longer installed during build.
- Missing BR ocamldoc.
- Missing BR findlib.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 1.3-11
- Rebuild for OCaml 3.11.2.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 22 2009 Richard W.M. Jones <rjones@redhat.com> - 1.3-9
- Rebuild for OCaml 3.11.1.

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 1.3-7
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 1.3-6
- Rebuild for OCaml 3.11.0

* Tue Sep  2 2008 Richard W.M. Jones <rjones@redhat.com> - 1.3-5
- Install in cryptokit subdirectory.
- Include a META file (from Debian) (resolves rhbz#460844).

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 1.3-4
- Rebuild for OCaml 3.10.2

* Fri Feb 29 2008 David Woodhouse <dwmw2@infradead.org> 1.3-3
- Build on PPC64

* Fri Feb 15 2008 Richard W.M. Jones <rjones@redhat.com> - 1.3-2
- Don't duplicate the README file in both packages.
- Change the license to LGPLv2 with exceptions.

* Tue Feb 12 2008 Richard W.M. Jones <rjones@redhat.com> - 1.3-1
- Initial RPM release.
