%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)
%global debug_package %{nil}

%global svnrev 234

Name:           ocaml-xml-light
Version:        2.3
Release:        0.7.svn%{svnrev}%{?dist}
Summary:        Minimal XML parser and printer for OCaml

Group:          Development/Libraries
License:        LGPLv2+
URL:            http://tech.motion-twin.com/xmllight.html

# Upstream does not have releases (or rather, it did up to version 2.2
# and then they stopped).  Use the SVN repository here:
# https://code.google.com/p/ocamllibs/source/checkout
#
# To prepare a source release:
# (1) Adjust 'svnrev' above to the latest release.
# (2) Check out the sources:
#       svn checkout http://ocamllibs.googlecode.com/svn/trunk/ ocamllibs
# (3) Create a tarball:
#       cd ocamllibs/xml-light/
#       tar -zcf /tmp/xml-light-NNN.tar.gz --xform='s,^\.,xml-light-NNN,' .
#         (where NNN is the svnrev above)
Source0:        xml-light-%{svnrev}.tar.gz

ExcludeArch:    sparc64 s390 s390x

BuildRequires:  ocaml >= 4.00.1
BuildRequires:  ocaml-findlib-devel >= 1.3.3-3
BuildRequires:  ocaml-ocamldoc
BuildRequires:  gawk


%description
Xml-Light is a minimal XML parser & printer for OCaml. It provides
functions to parse an XML document into an OCaml data structure, work
with it, and print it back to an XML document. It support also DTD
parsing and checking, and is entirely written in OCaml, hence it does
not require additional C library.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%setup -n xml-light-%{svnrev}


%build
# Build breaks if parallelized.
unset MAKEFLAGS
make all
make doc
%if %opt
make opt
%endif
sed -e 's/@VERSION@/%{VERSION}/' < META.in > META


%check
./test.exe <<EOF
<abc><123/></abc>

EOF

%if %opt
./test_opt.exe <<EOF
<abc><123/></abc>

EOF
%endif


%install
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
rm -f test.cmi
ocamlfind install xml-light META *.mli *.cmi *.cma *.a *.cmxa *.cmx


%files
%doc README
%{_libdir}/ocaml/xml-light
%if %opt
%exclude %{_libdir}/ocaml/xml-light/*.a
%exclude %{_libdir}/ocaml/xml-light/*.cmxa
%exclude %{_libdir}/ocaml/xml-light/*.cmx
%endif
%exclude %{_libdir}/ocaml/xml-light/*.mli


%files devel
%doc README doc/*
%if %opt
%{_libdir}/ocaml/xml-light/*.a
%{_libdir}/ocaml/xml-light/*.cmxa
%{_libdir}/ocaml/xml-light/*.cmx
%endif
%{_libdir}/ocaml/xml-light/*.mli


%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-0.7.svn234
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Sep 19 2013 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.6.svn234
- OCaml 4.01.0 rebuild.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-0.5.svn234
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-0.4.svn234
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 27 2012 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.3.svn234
- BR >= OCaml 4.00.1 so we can't be built against the wrong OCaml.

* Tue Oct 30 2012 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.2.svn234
- Rebuild for OCaml 4.00.1.

* Tue Aug 21 2012 Richard W.M. Jones <rjones@redhat.com> - 2.3-0.1.svn234
- Update to latest version (subversion release 234).
- Includes fix for CVE-2012-3514 - moderate impact hash table collisions
  (resolves: rhbz#787890).
- Clean up the spec file and bring up to modern standards.
- Add tests.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.cvs20070817-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Richard W.M. Jones <rjones@redhat.com> - 2.2.cvs20070817-18
- Rebuild for OCaml 4.00.0.

* Fri Jan 06 2012 Richard W.M. Jones <rjones@redhat.com> - 2.2.cvs20070817-17
- Rebuild for OCaml 3.12.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.cvs20070817-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 06 2011 Richard W.M. Jones <rjones@redhat.com> - 2.2.cvs20070817-15
- Rebuild for OCaml 3.12 (http://fedoraproject.org/wiki/Features/OCaml3.12).

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 2.2.cvs20070817-14
- Rebuild for OCaml 3.11.2.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.cvs20070817-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 2.2.cvs20070817-12
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.cvs20070817-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 2.2.cvs20070817-10
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 2.2.cvs20070817-9
- Rebuild for OCaml 3.11.0

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 2.2.cvs20070817-8
- Rebuild for OCaml 3.10.2

* Sat Mar  1 2008 Richard W.M. Jones <rjones@redhat.com> - 2.2.cvs20070817-7
- Rebuild for ppc64.

* Tue Feb 12 2008 Richard W.M. Jones <rjones@redhat.com> - 2.2.cvs20070817-6
- Rebuild for OCaml 3.10.1

* Thu Sep  6 2007 Richard W.M. Jones <rjones@redhat.com> - 2.2.cvs20070817-5
- Don't package test.cmi file (it's a test program).

* Thu Sep  6 2007 Richard W.M. Jones <rjones@redhat.com> - 2.2.cvs20070817-4
- Force rebuild because of updated requires/provides scripts in OCaml.

* Thu Aug 30 2007 Richard W.M. Jones <rjones@redhat.com> - 2.2.cvs20070817-3
- Force rebuild because of changed BRs in base OCaml.

* Fri Aug 24 2007 Richard W.M. Jones <rjones@redhat.com> - 2.2.cvs20070817-2
- Clarified that the license is LGPLv2+.

* Fri Aug 17 2007 Richard W.M. Jones <rjones@redhat.com> - 2.2.cvs20070817-1
- Initial RPM release.
