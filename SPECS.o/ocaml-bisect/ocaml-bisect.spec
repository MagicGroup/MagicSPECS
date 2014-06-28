%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           ocaml-bisect
Version:        1.3
Release:        3%{?dist}
Summary:        OCaml code coverage tool
License:        GPLv3+

ExcludeArch:    sparc64 s390 s390x

URL:            http://bisect.x9c.fr/
Source0:        https://forge.ocamlcore.org/frs/download.php/1051/bisect-%{version}.tar.gz

Patch1:         bisect-1.3-enable-debug.patch

BuildRequires:  ocaml >= 3.10.0
BuildRequires:  ocaml-findlib-devel
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-camlp4-devel

%global __ocaml_requires_opts -i Asttypes -i Parsetree


%description
Bisect is a code coverage tool for the Objective Caml language. It is
a camlp4-based tool that allows to instrument your application before
running tests. After application execution, it is possible to generate
a report in HTML format that is the replica of the application source
code annotated with code coverage information.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%setup -q -n bisect-%{version}
%patch1 -p1

%build
sh configure
make PATH_OCAML_BIN=%{_bindir} all


%check
make PATH_OCAML_BIN=%{_bindir} tests


%install
rm -rf $RPM_BUILD_ROOT

export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR

# FFS ... please use DESTDIR ...

mkdir -p $RPM_BUILD_ROOT%{_bindir}
pushd $RPM_BUILD_ROOT%{_bindir}
ln -s %{_bindir}/ocamlbuild
popd
make install PATH_OCAML_PREFIX=$RPM_BUILD_ROOT%{_prefix}

pushd $RPM_BUILD_ROOT%{_bindir}
rm ocamlbuild
popd


%files
%doc COPYING
%{_bindir}/bisect-report
%{_libdir}/ocaml/bisect
%if %opt
%exclude %{_libdir}/ocaml/bisect/*.a
%exclude %{_libdir}/ocaml/bisect/*.cmxa
%endif


%files devel
%doc CHANGES COPYING README VERSION doc/bisect.pdf ocamldoc
%if %opt
%{_libdir}/ocaml/bisect/*.a
%{_libdir}/ocaml/bisect/*.cmxa
%endif


%changelog
* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 1.3-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 1.3-1
- New upstream version 1.3.
- Rebuild for OCaml 4.01.0.
- Enable debuginfo.
- Enable tests.
- Modernize the specfile.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Dec 02 2012 Bruno Wolff III <bruno@wolff.to> 1.1-4
- Rebuild for ocaml 4.0.1.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Richard W.M. Jones <rjones@redhat.com> - 1.1-2
- Rebuild for OCaml 4.00.0.

* Fri Jan 13 2012 Richard W.M. Jones <rjones@redhat.com> - 1.1-1
- New upstream version 1.1.
- Rebuild for OCaml 3.12.1.
- Remove two patches, upstream.
- Add a bunch of hacks because of lack of proper DESTDIR.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 06 2011 Richard W.M. Jones <rjones@redhat.com> - 1.0-3
- Rebuild for OCaml 3.12 (http://fedoraproject.org/wiki/Features/OCaml3.12).
- Patch for "Error: The constructor Ast.CrMth expects 6 argument(s), [etc]"

* Tue Jan  5 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0-1
- Update to non-alpha 1.0 (requested by upstream author).
- Use upstream RPM 4.8 OCaml dependency generator.
- Use %%global instead of %%define.
- Define PATH_OCAML_BIN to work around strangeness in Makefile.
- Remove nojava patch.
- Add patch to fix build of thread code.
- Rechecked in rpmlint.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0-0.7.alpha
- Rebuild for OCaml 3.11.2.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.6.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0-0.5.alpha
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.4.alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0-0.3.alpha
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0-0.2.alpha
- Rebuild for OCaml 3.11.0

* Sun Aug 24 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0-0.1.alpha
- Initial RPM release.
