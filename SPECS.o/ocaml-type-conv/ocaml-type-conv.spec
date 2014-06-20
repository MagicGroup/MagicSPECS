%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

%global dlnode 821

Name:           ocaml-type-conv
Version:        3.0.5
Release:        8%{?dist}
Summary:        OCaml base library for type conversion
License:        LGPLv2+ with exceptions and BSD

URL:            http://forge.ocamlcore.org/projects/type-conv/
Source0:        http://forge.ocamlcore.org/frs/download.php/%{dlnode}/type_conv-%{version}.tar.gz

ExcludeArch:    sparc64 s390 s390x

BuildRequires:  ocaml >= 3.12.0
BuildRequires:  ocaml-findlib
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-camlp4-devel

%global __ocaml_requires_opts -i Asttypes -i Parsetree


%description
The type-conv mini library factors out functionality needed by
different preprocessors that generate code from type specifications,
because this functionality cannot be duplicated without losing the
ability to use these preprocessors simultaneously.


%prep
%setup -q -n type_conv-%{version}
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


%build
ocaml setup.ml -build


%install
rm -rf $RPM_BUILD_ROOT
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
ocaml setup.ml -install


%files
%doc LICENSE LICENSE.Tywith Changelog COPYRIGHT README.txt
%{_libdir}/ocaml/type_conv


%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 3.0.5-7
- Rebuild for OCaml 4.01.0.
- Enable debuginfo (unsuccessfully - the build system is insane).
- Modernize the spec file.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 15 2013 Michael Ekstrand <michael@elehack.net> - 3.0.5-4
- Drop 3.12 compatbility patch (#741482)

* Mon Oct 29 2012 Richard W.M. Jones <rjones@redhat.com> - 3.0.5-3
- Rebuild for OCaml 4.00.1.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Richard W.M. Jones <rjones@redhat.com> - 3.0.5-1
- Update to new upstream version 3.0.5.
- Rebuild for OCaml 4.00.0.
- Tarball and install directory are now called "type_conv" instead of
  "type-conv".

* Fri Jan 06 2012 Richard W.M. Jones <rjones@redhat.com> - 3.0.4-2
- Rebuild for OCaml 3.12.1.

* Mon Sep 26 2011 Michael Ekstrand <michael@elehack.net> - 3.0.4-1
- New upstream release from forge.ocamlcore.org (#725167)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan  5 2011 Richard W.M. Jones <rjones@redhat.com> - 2.0.2-1
- New upstream version 2.0.2.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 1.6.10-3
- Rebuild for OCaml 3.11.2.

* Sun Oct  4 2009 Richard W.M. Jones <rjones@redhat.com> - 1.6.10-2
- New upstream version 1.6.10.
- "CHANGES" -> "Changelog"

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.6.7-2
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Tue Mar 10 2009 Richard W.M. Jones <rjones@redhat.com> - 1.6.7-1
- New upstream version 1.6.7.
- Fixed source URL.
- VERSION file no longer exists in upstream tarball.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 1.6.4-3
- Rebuild for OCaml 3.11.0+rc1.

* Mon Nov 24 2008 Richard W.M. Jones <rjones@redhat.com> - 1.6.4-2
- Rebuild.

* Thu Nov 20 2008 Richard W.M. Jones <rjones@redhat.com> - 1.6.4-1
- New upstream version 1.6.4.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 1.6.1-2
- Rebuild for OCaml 3.11.0

* Sun Aug 31 2008 Richard W.M. Jones <rjones@redhat.com> - 1.6.1-1
- New upstream version 1.6.1.

* Mon May  5 2008 Richard W.M. Jones <rjones@redhat.com> - 1.5.0-2
- Ignore Asttypes/Parsetree.

* Sat May  3 2008 Richard W.M. Jones <rjones@redhat.com> - 1.5.0-1
- New upstream version 1.5.0.

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 1.4.0-2
- Rebuild for OCaml 3.10.2

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 1.4.0-1
- New version 1.4.0.
- Fixed upstream URL.

* Wed Mar  5 2008 Richard W.M. Jones <rjones@redhat.com> - 1.3.0-3
- Remove ExcludeArch ppc64.

* Sat Mar  1 2008 Richard W.M. Jones <rjones@redhat.com> - 1.3.0-2
- Add missing BR for ocaml-camlp4-devel and test build in mock.

* Sun Feb 24 2008 Richard W.M. Jones <rjones@redhat.com> - 1.3.0-1
- Initial RPM release.
