%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)
%global debug_package %{nil}

Name:           ocaml-curl
Version:        0.5.3
Release:        12%{?dist}
Summary:        OCaml Curl library (ocurl)
License:        MIT

URL:            http://sourceforge.net/projects/ocurl
Source0:        http://downloads.sourceforge.net/ocurl/ocurl-%{version}.tgz

Patch1:         ocurl-0.5.3-include-o-cmx.patch

ExcludeArch:    sparc64 s390 s390x

BuildRequires:  ocaml >= 3.10.0-7
BuildRequires:  ocaml-findlib-devel, curl-devel >= 7.12.0
BuildRequires:  gawk

# Explicitly require Curl (fixes #711261). Since ocaml-curl uses
# -custom rather than ocamlmklib, automatic detection is infeasible.
Requires: curl-devel >= 7.12.0


%description
The Ocaml Curl Library (Ocurl) is an interface library for the
programming language Ocaml to the networking library libcurl.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%setup -q -n ocurl
%patch1 -p1

# Files in the archive have spurious +x mode.
find -type f | xargs chmod 0644
chmod 0755 configure install-sh


%build
# Parallel builds don't work.
unset MAKEFLAGS

%configure --libdir=%{_libdir} --with-findlib
make all \
%if %opt
  OCBYTE="ocamlc.opt -g" \
  OCOPT="ocamlopt.opt -g"
%else

%endif


%install
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
make install

# Install curl.mli
cp curl.mli $OCAMLFIND_DESTDIR/curl

# Make clean in the examples dir so our docs don't contain binaries.
make -C examples clean


%files
%doc COPYING
%{_libdir}/ocaml/curl
%if %opt
%exclude %{_libdir}/ocaml/curl/*.a
%exclude %{_libdir}/ocaml/curl/*.o
%exclude %{_libdir}/ocaml/curl/*.cmx
%exclude %{_libdir}/ocaml/curl/*.cmxa
%endif
%exclude %{_libdir}/ocaml/curl/*.mli


%files devel
%doc examples/*
%if %opt
%{_libdir}/ocaml/curl/*.a
%{_libdir}/ocaml/curl/*.o
%{_libdir}/ocaml/curl/*.cmx
%{_libdir}/ocaml/curl/*.cmxa
%endif
%{_libdir}/ocaml/curl/*.mli


%changelog
* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 0.5.3-12
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 0.5.3-10
- Rebuild for OCaml 4.01.0.
- Debuginfo does not work for this package.
- Include *.cmx & *.o files in -devel package (for inlining).
- Modernize the spec file.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Nov  4 2012 Michael Ekstrand <michael@elehack.net> - 0.5.3-7
- Rebuild for OCaml 4 update

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Richard W.M. Jones <rjones@redhat.com> - 0.5.3-5
- Rebuild for OCaml 4.00.0.

* Fri Jan 06 2012 Richard W.M. Jones <rjones@redhat.com> - 0.5.3-4
- Rebuild for OCaml 3.12.1.

* Tue Jun  7 2011 Michael Ekstrand <michael@elehack.net> - 0.5.3-3
- Add curl-devel to Requires (#711261)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan  5 2011 Richard W.M. Jones <rjones@redhat.com> - 0.5.3-1
- New upstream version 0.5.3.
- Rebuild for OCaml 3.12.0.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 0.5.1-3
- Rebuild for OCaml 3.11.2.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 0.5.1-1
- New upstream version 0.5.1.
- Rebuild for OCaml 3.11.1.

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 0.5.0-3
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 0.5.0-2
- Rebuild for OCaml 3.11.0

* Sun Aug 31 2008 Richard W.M. Jones <rjones@redhat.com> - 0.5.0-1
- New upstream release 0.5.0.

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.2.1-9
- fix license tag

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 0.2.1-8
- Rebuild for OCaml 3.10.2

* Sat Mar  1 2008 Richard W.M. Jones <rjones@redhat.com> - 0.2.1-7
- Rebuild for ppc64.

* Tue Feb 12 2008 Richard W.M. Jones <rjones@redhat.com> - 0.2.1-6
- Force rebuild for OCaml 3.10.1.

* Thu Sep  6 2007 Richard W.M. Jones <rjones@redhat.com> - 0.2.1-5
- Force rebuild because of changed build-requires/provides scripts in OCaml.

* Thu Aug 30 2007 Richard W.M. Jones <rjones@redhat.com> - 0.2.1-4
- Force rebuild because of changed BRs in base OCaml.

* Thu Aug  2 2007 Richard W.M. Jones <rjones@redhat.com> - 0.2.1-3
- ExcludeArch ppc64
- Remove Requires curl, which is not necessary.
- Use %-doc to handle docs in the devel package.

* Mon Jun 11 2007 Richard W.M. Jones <rjones@redhat.com> - 0.2.1-2
- Updated to latest packaging guidelines.

* Sat May 26 2007 Richard W.M. Jones <rjones@redhat.com> - 0.2.1-1
- Initial RPM release.
