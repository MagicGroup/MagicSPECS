%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)
%global debug_package %{nil}

%global dlnode  832

Name:           ocaml-sexplib
Version:        7.0.5
Release:        10%{?dist}
Summary:        OCaml library for converting OCaml values to S-expressions
License:        LGPLv2+ with exceptions and BSD

URL:            http://forge.ocamlcore.org/projects/sexplib
Source0:        http://forge.ocamlcore.org/frs/download.php/%{dlnode}/sexplib-%{version}.tar.gz

ExcludeArch:    sparc64 s390 s390x

# Fix ocamlbuild for ocaml 4.00.0.
Patch1:         sexplib-7.0.5-patch-ocamlbuild-ocaml4.patch

BuildRequires:  ocaml >= 3.12.0
BuildRequires:  ocaml-findlib-devel
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-type-conv >= 3.0.5
BuildRequires:  ocaml-camlp4-devel


%description
This library contains functionality for parsing and pretty-printing
S-expressions. In addition to that it contains an extremely useful
preprocessing module for Camlp4, which can be used to automatically
generate code from type definitions for efficiently converting
OCaml-values to S-expressions and vice versa. In combination with the
parsing and pretty-printing functionality this frees users from having
to write their own I/O-routines for datastructures they
define. Possible errors during automatic conversions from
S-expressions to OCaml-values are reported in a very human-readable
way. Another module in the library allows you to extract and replace
sub-expressions in S-expressions.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%setup -q -n sexplib-%{version}
ocaml setup.ml -configure --prefix %{_prefix} \
      --libdir %{_libdir} \
      --libexecdir %{_libexecdir} \
      --exec-prefix %{_exec_prefix} \
      --bindir %{_bindir} \
      --sbindir %{_sbindir} \
      --mandir %{_mandir} \
      --datadir %{_datadir} \
      --localstatedir %{_localstatedir} \
      --sharedstatedir %{_sharedstatedir} \
      --destdir $RPM_BUILD_ROOT

%patch1 -p1


%build
ocaml setup.ml -build


%check
ocaml setup.ml -test


%install
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
ocaml setup.ml -install


%files
%doc LICENSE LICENSE.Tywith
%{_libdir}/ocaml/sexplib
%if %opt
%exclude %{_libdir}/ocaml/sexplib/*.a
%exclude %{_libdir}/ocaml/sexplib/*.cmxa
%endif
%exclude %{_libdir}/ocaml/sexplib/*.mli
%exclude %{_libdir}/ocaml/sexplib/*.ml


%files devel
%doc LICENSE LICENSE.Tywith Changelog COPYRIGHT README.txt
%if %opt
%{_libdir}/ocaml/sexplib/*.a
%{_libdir}/ocaml/sexplib/*.cmxa
%endif
%{_libdir}/ocaml/sexplib/*.mli
%{_libdir}/ocaml/sexplib/*.ml


%changelog
* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 7.0.5-10
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 19 2014 Richard W.M. Jones <rjones@redhat.com> - 7.0.5-8
- Rebuild against latest Arg module.

* Thu Sep 19 2013 Richard W.M. Jones <rjones@redhat.com> - 7.0.5-7
- OCaml 4.01.0 rebuild.
- Modernize the spec file.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 30 2012 Richard W.M. Jones <rjones@redhat.com> - 7.0.5-4
- Rebuild for OCaml 4.00.1.

* Mon Jul 30 2012 Richard W.M. Jones <rjones@redhat.com> - 7.0.5-3
- Patch for OCaml 4.00.0 official.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Richard W.M. Jones <rjones@redhat.com> - 7.0.5-1
- Update to latest upstream version 7.0.5.
- Rebuild for OCaml 4.00.0.

* Fri Jan 06 2012 Richard W.M. Jones <rjones@redhat.com> - 7.0.4-2
- Rebuild for OCaml 3.12.1.

* Tue Sep 27 2011 Michael Ekstrand <michael@elehack.net> - 7.0.4-1
- New upstream release 7.0.4 from forge.ocamlcore.org (#741483)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan  6 2011 Richard W.M. Jones <rjones@redhat.com> - 6.0.4-1
- New upstream version 6.0.4.
- Rebuild for OCaml 3.12.0.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 4.2.15-2
- Rebuild for OCaml 3.11.2.

* Sun Oct  4 2009 Richard W.M. Jones <rjones@redhat.com> - 4.2.15-1
- New upstream version 4.2.15.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 12 2009 Richard W.M. Jones <rjones@redhat.com> - 4.2.10-2
- Rebuild to try to fix rpmdepsize FTBFS problem.

* Sat May 22 2009 Richard W.M. Jones <rjones@redhat.com> - 4.2.10-1
- Rebuild for OCaml 3.11.1.
- New upstream version 4.2.10.

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Mon Mar 30 2009 Richard W.M. Jones <rjones@redhat.com> - 4.2.7-2
- Force rebuild against latest ocaml-type-conv.

* Tue Mar 10 2009 Richard W.M. Jones <rjones@redhat.com> - 4.2.7-1
- New upstream version 4.2.7.
- Fixed source URL.
- Removed the patch as it is now upstream.
- Fixed the doc line.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 4.2.1-2
- Rebuild for OCaml 3.11.0+rc1.

* Thu Nov 20 2008 Richard W.M. Jones <rjones@redhat.com> - 4.2.1-1
- New upstream version 4.2.1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 4.0.1-2
- Rebuild for OCaml 3.11.0

* Sun Aug 31 2008 Richard W.M. Jones <rjones@redhat.com> - 4.0.1-1
- New upstream release 4.0.1.
- Patch a build problem in the test suite.
- ml file should be packaged in the -devel subpackage, not in main.

* Mon May 10 2008 Richard W.M. Jones <rjones@redhat.com> - 3.7.4-2
- Added BR ocaml-camlp4-devel.
- Added a check section to run the included tests.

* Sat May  3 2008 Richard W.M. Jones <rjones@redhat.com> - 3.7.4-1
- New upstream version 3.7.4.

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 3.7.1-1
- New upstream version 3.7.1.
- Fixed upstream URL.
- Depend on latest type-conv.

* Wed Mar  5 2008 Richard W.M. Jones <rjones@redhat.com> - 3.5.0-2
- Remove ExcludeArch ppc64.

* Sun Feb 24 2008 Richard W.M. Jones <rjones@redhat.com> - 3.5.0-1
- Initial RPM release.
