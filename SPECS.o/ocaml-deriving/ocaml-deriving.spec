%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)
%global debug_package %{nil}

Name:           ocaml-deriving
Version:        0.1.1a
Release:        21%{?dist}
Summary:        Extension to OCaml for deriving functions from types
License:        MIT

URL:            http://code.google.com/p/deriving/
Source0:        http://deriving.googlecode.com/files/deriving-%{version}.tar.gz

ExcludeArch:    sparc64 s390 s390x

Patch0:         ocaml-deriving-no-link-libs.patch
# This is included as part of the general fixes in patch 2.
#Patch1:         ocaml-deriving-0.1.1a-dynlink.patch
Patch2:         0001-fixes-for-3.12.0.patch
Patch3:         ocaml-deriving-0.1.1a-no-bimap-mli.patch

BuildRequires:  ocaml >= 3.11.0-1
BuildRequires:  ocaml-findlib-devel
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-camlp4-devel


%description
Extension to OCaml for deriving functions from type declarations.
Includes derivers for pretty-printing, type-safe marshalling with
structure-sharing, dynamic typing, equality, and more.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%setup -q -n deriving-0.1.1
%patch0
#%patch1 -p1
%patch2 -p1
%patch3 -p1


%build
# Parallel builds don't work.
unset MAKEFLAGS

make \
%if %opt
  OCAMLOPT="ocamlopt.opt -g"
%endif

cat >META <<'EOF'
name="deriving"
version="%{version}"
description = "Deriving"
requires = "num"
archive(byte) = "deriving.cma"
archive(native) = "deriving.cmxa"

package "syntax" (
    requires(syntax) = "camlp4,unix"
    archive(preprocessor,syntax) = "pa_deriving.cma"
    archive(syntax,toploop) = "pa_deriving.cma"

    package "base" (
       requires(syntax) = "camlp4"
       archive(preprocessor,syntax) = "pa_deriving_common.cmo pa_deriving.cmo"
       archive(syntax,toploop) = "pa_deriving_common.cmo pa_deriving.cmo"
    )
)

package "syntax_tc" (
    exists_if = "pa_deriving_tc.cma"
    requires(syntax) = "camlp4,unix,type-conv"
    archive(preprocessor,syntax) = "pa_deriving_tc.cma"
    archive(syntax,toploop) = "pa_deriving_tc.cma"

    package "base" (
       requires(syntax) = "camlp4"
       archive(preprocessor,syntax) = "pa_deriving_common.cmo pa_deriving_tc.cmo"
       archive(syntax,toploop) = "pa_deriving_common.cmo pa_deriving_tc.cmo"
    )
)
EOF


%check
# Parallel builds don't work.
unset MAKEFLAGS

cd tests
make
./tests


%install
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
mkdir -p $RPM_BUILD_ROOT%{_bindir}

ocamlfind install deriving \
  META lib/*.cma lib/*.cmxa lib/*.a lib/*.mli lib/*.cmi lib/*.cmx
install -m 0755 syntax/deriving $RPM_BUILD_ROOT%{_bindir}


%files
%doc COPYING
%{_libdir}/ocaml/deriving
%if %opt
%exclude %{_libdir}/ocaml/deriving/*.a
%exclude %{_libdir}/ocaml/deriving/*.cmxa
%exclude %{_libdir}/ocaml/deriving/*.cmx
%endif
%exclude %{_libdir}/ocaml/deriving/*.mli
%{_bindir}/*


%files devel
%doc COPYING README CHANGES
%if %opt
%{_libdir}/ocaml/deriving/*.a
%{_libdir}/ocaml/deriving/*.cmxa
%{_libdir}/ocaml/deriving/*.cmx
%endif
%{_libdir}/ocaml/deriving/*.mli


%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1a-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 0.1.1a-20
- Rebuild for OCaml 4.01.0.
- Modernize the spec file.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1a-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1a-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Dec 02 2012 Bruno Wolff III <bruno@wolff.to> - 0.1.1a-17
- Rebuild for ocaml 4.0.1.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1a-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Richard W.M. Jones <rjones@redhat.com> - 0.1.1a-15
- Rebuild for OCaml 4.00.0.

* Wed Feb  1 2012 Richard W.M. Jones <rjones@redhat.com> - 0.1.1a-14
- Update META file (RHBZ#785680).

* Thu Jan 12 2012 Richard W.M. Jones <rjones@redhat.com> - 0.1.1a-13
- Rebuild for OCaml 3.12.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1a-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan  6 2011 Richard W.M. Jones <rjones@redhat.com> - 0.1.1a-11
- Rebuild for OCaml 3.12.0.
- Include separate fixes for 3.12 by Jake Donham.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 0.1.1a-10
- Rebuild for OCaml 3.11.2.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1a-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 0.1.1a-8
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1a-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec  5 2008 Richard W.M. Jones <rjones@redhat.com> - 0.1.1a-6
- Patch to add dynlink.cma for camlp4lib.cma.
- Rebuild for OCaml 3.11.0.

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 0.1.1a-5
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 0.1.1a-4
- Rebuild for OCaml 3.11.0

* Mon May 10 2008 Richard W.M. Jones <rjones@redhat.com> - 0.1.1a-3
- Fix the License tag (MIT not BSD).

* Wed Mar  5 2008 Richard W.M. Jones <rjones@redhat.com> - 0.1.1a-2
- Remove ExcludeArch ppc64.

* Fri Feb 29 2008 Richard W.M. Jones <rjones@redhat.com> - 0.1.1a-1
- New upstream release which includes the license file.
- Patch OCamlMakefile so it doesn't statically link system libs with
  the library.

* Thu Feb 28 2008 Richard W.M. Jones <rjones@redhat.com> - 0.1.1-1
- Initial RPM release.
- Lacks a license file so we cannot release it for review yet.
