%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           ocaml-expat
Version:        0.9.1
Release:        28%{?dist}
Summary:        OCaml wrapper for the Expat XML parsing library
License:        MIT

URL:            http://www.xs4all.nl/~mmzeeman/ocaml/
Source0:        http://www.xs4all.nl/~mmzeeman/ocaml/ocaml-expat-%{version}.tar.gz

ExcludeArch:    sparc64 s390 s390x

BuildRequires:  ocaml >= 3.10.1
BuildRequires:  ocaml-findlib-devel, expat-devel >= 2.0.1, chrpath
BuildRequires:  util-linux-ng, gawk


%description
An ocaml wrapper for the Expat XML parsing library. It allows you to
write XML-Parsers using the SAX method. An XML document is parsed on
the fly without needing to load the entire XML-Tree into memory.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%setup -q


%build
make depend
make -j1 all \
%if %opt
  allopt \
  OCAMLC="ocamlc.opt -g" \
  OCAMLOPT="ocamlopt.opt -g"
%endif


%install
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
make install

# Remove rpath from stublibs .so file.
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs/*.so


%files
%doc LICENCE README changelog
%{_libdir}/ocaml/expat
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner
%if %opt
%exclude %{_libdir}/ocaml/expat/*.a
%exclude %{_libdir}/ocaml/expat/*.cmxa
%endif
%exclude %{_libdir}/ocaml/expat/*.mli


%files devel
%doc LICENCE README changelog
%if %opt
%{_libdir}/ocaml/expat/*.a
%{_libdir}/ocaml/expat/*.cmxa
%endif
%{_libdir}/ocaml/expat/*.mli


%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 0.9.1-27
- Rebuild for OCaml 4.01.0.
- Enable debuginfo.
- Modernize the spec file.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Dec 02 2012 Bruno Wolff III <bruno@wolff.to> - 0.9.1-24
- Rebuild for ocaml 4.0.1.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Richard W.M. Jones <rjones@redhat.com> - 0.9.1-22
- Rebuild for OCaml 4.00.0.

* Fri Jan 06 2012 Richard W.M. Jones <rjones@redhat.com> - 0.9.1-21
- Rebuild for OCaml 3.12.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 05 2011 Richard W.M. Jones <rjones@redhat.com> - 0.9.1-19
- Rebuild for OCaml 3.12 (http://fedoraproject.org/wiki/Features/OCaml3.12).

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 0.9.1-18
- Rebuild for OCaml 3.11.2.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 0.9.1-16
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 0.9.1-14
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 0.9.1-13
- Rebuild for OCaml 3.11.0

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.9.1-12
- fix license tag

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 0.9.1-11
- Rebuild for OCaml 3.10.2

* Sat Mar  1 2008 Richard W.M. Jones <rjones@redhat.com> - 0.9.1-10
- Rebuild for ppc64.

* Tue Feb 12 2008 Richard W.M. Jones <rjones@redhat.com> - 0.9.1-9
- Rebuild for OCaml 3.10.1.

* Thu Sep  6 2007 Richard W.M. Jones <rjones@redhat.com> - 0.9.1-8
- Force rebuild because of updated requires/provides scripts in OCaml.

* Thu Aug 30 2007 Richard W.M. Jones <rjones@redhat.com> - 0.9.1-7
- Force rebuild because of changed BRs in base OCaml.

* Tue Aug 28 2007 Richard W.M. Jones <rjones@redhat.com> - 0.9.1-6
- Temporarily add BuildRequires: util-linux-ng to see if that cures
  problems building on Koji (note: builds work elsewhere, just not
  on Koji).

* Tue Aug 28 2007 Richard W.M. Jones <rjones@redhat.com> - 0.9.1-5
- Link against expat 2.x.

* Thu Aug  2 2007 Richard W.M. Jones <rjones@redhat.com> - 0.9.1-4
- ExcludeArch ppc64
- Remove rpath from the stublibs .so file.
- Strip the stublibs .so file.

* Tue Jun 19 2007 Richard W.M. Jones <rjones@redhat.com> - 0.9.1-3
- BuildRequires expat-devel.

* Mon Jun 11 2007 Richard W.M. Jones <rjones@redhat.com> - 0.9.1-2
- Updated to latest packaging guidelines.

* Sat May 26 2007 Richard W.M. Jones <rjones@redhat.com> - 0.9.1-1
- Initial RPM release.
