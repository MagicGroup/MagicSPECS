%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           ocaml-gettext
Version:        0.3.4
Release:        13%{?dist}
Summary:        OCaml library for i18n

License:        LGPLv2+ with exceptions
URL:            http://forge.ocamlcore.org/projects/ocaml-gettext
ExcludeArch:    sparc64 s390 s390x

Source0:        http://forge.ocamlcore.org/frs/download.php/676/ocaml-gettext-%{version}.tar.gz

Patch1:         ocaml-gettext-0.3.4-use-ocamlopt-g.patch

BuildRequires:  ocaml >= 4.00.1
BuildRequires:  ocaml-findlib-devel >= 1.3.3-3
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-camlp4-devel
BuildRequires:  ocaml-fileutils-devel >= 0.4.4-4
BuildRequires:  docbook-style-xsl
BuildRequires:  libxslt
BuildRequires:  libxml2
BuildRequires:  chrpath
BuildRequires:  autoconf
%if !0%{?rhel}
BuildRequires:  ocaml-ounit-devel
BuildRequires:  ocaml-camomile-devel >= 0.8.1
BuildRequires:  ocaml-camomile-data
%endif

%if !0%{?rhel}
# ocaml-gettext program needs camomile data files
Requires:       ocaml-camomile-data
%endif

%global __ocaml_requires_opts -i Asttypes -i Parsetree
%global __ocaml_provides_opts -i Pr_gettext


%description
Ocaml-gettext provides support for internationalization of Ocaml
programs.

Constraints :

* provides a pure Ocaml implementation,
* the API should be as close as possible to GNU gettext,
* provides a way to automatically extract translatable
  strings from Ocaml source code.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

# BZ 446919.
Requires:       ocaml-fileutils-devel >= 0.4.0


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%if !0%{?rhel}
%package        camomile
Summary:        Parts of %{name} which depend on Camomile
Requires:       %{name} = %{version}-%{release}


%description    camomile
The %{name}-camomile package contains the parts of %{name} which
depend on Camomile.


%package        camomile-devel
Summary:        Development files for %{name}-camomile
Requires:       %{name}-devel = %{version}-%{release}


%description    camomile-devel
The %{name}-camomile-devel package contains libraries and
signature files for developing applications that use
%{name}-camomile.
%endif


%prep
%setup -q

%patch1 -p1


%build
# Parallel builds don't work.
unset MAKEFLAGS
CFLAGS="$RPM_OPT_FLAGS" \
./configure \
  --libdir=%{_libdir} \
%if 0%{?rhel}
  --disable-camomile \
%else
  --enable-test \
%endif
  --with-docbook-stylesheet=/usr/share/sgml/docbook/xsl-stylesheets
make all


%check
%if !0%{?rhel}
pushd test
../_build/bin/test
popd
%endif


%install
# make install in the package is screwed up completely.  Install
# by hand instead.
export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
mkdir -p $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
mkdir -p $RPM_BUILD_ROOT%{_bindir}

# Remove *.o files - these shouldn't be distributed.
find _build -name '*.o' -exec rm {} \;

ocamlfind install gettext _build/lib/gettext/*
ocamlfind install gettext-stub _build/lib/gettext-stub/*
%if !0%{?rhel}
ocamlfind install gettext-camomile _build/lib/gettext-camomile/*
%endif
install -m 0755 _build/bin/ocaml-gettext $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 _build/bin/ocaml-xgettext $RPM_BUILD_ROOT%{_bindir}/

chrpath --delete $OCAMLFIND_DESTDIR/stublibs/dll*.so


%files
%doc COPYING
%{_libdir}/ocaml/gettext
%{_libdir}/ocaml/gettext-stub
%if %opt
%exclude %{_libdir}/ocaml/gettext/*.a
%exclude %{_libdir}/ocaml/gettext/*.cmxa
%exclude %{_libdir}/ocaml/gettext/*.cmx
%exclude %{_libdir}/ocaml/gettext-stub/*.a
%exclude %{_libdir}/ocaml/gettext-stub/*.cmxa
%exclude %{_libdir}/ocaml/gettext-stub/*.cmx
%endif
%exclude %{_libdir}/ocaml/gettext/*.ml
%exclude %{_libdir}/ocaml/gettext/*.mli
%exclude %{_libdir}/ocaml/gettext-stub/*.ml
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner


%files devel
%doc README CHANGELOG TODO
# %doc build/share/doc/html/*
%if %opt
%{_libdir}/ocaml/gettext/*.a
%{_libdir}/ocaml/gettext/*.cmxa
%{_libdir}/ocaml/gettext/*.cmx
%{_libdir}/ocaml/gettext-stub/*.a
%{_libdir}/ocaml/gettext-stub/*.cmxa
%{_libdir}/ocaml/gettext-stub/*.cmx
%endif
%{_libdir}/ocaml/gettext/*.ml
%{_libdir}/ocaml/gettext/*.mli
%{_libdir}/ocaml/gettext-stub/*.ml
%{_bindir}/ocaml-gettext
%{_bindir}/ocaml-xgettext


%if !0%{?rhel}
%files camomile
%doc COPYING
%{_libdir}/ocaml/gettext-camomile
%if %opt
%exclude %{_libdir}/ocaml/gettext-camomile/*.a
%exclude %{_libdir}/ocaml/gettext-camomile/*.cmxa
%exclude %{_libdir}/ocaml/gettext-camomile/*.cmx
%endif
%exclude %{_libdir}/ocaml/gettext-camomile/*.mli


%files camomile-devel
%doc README
%if %opt
%{_libdir}/ocaml/gettext-camomile/*.a
%{_libdir}/ocaml/gettext-camomile/*.cmxa
%{_libdir}/ocaml/gettext-camomile/*.cmx
%endif
%{_libdir}/ocaml/gettext-camomile/*.mli
%endif


%changelog
* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 0.3.4-13
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 0.3.4-11
- Rebuild for OCaml 4.01.0.
- Enable debuginfo.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 27 2012 Richard W.M. Jones <rjones@redhat.com> - 0.3.4-8
- BR >= OCaml 4.00.1 so we can't be built against the wrong OCaml.

* Fri Oct 19 2012 Richard W.M. Jones <rjones@redhat.com> - 0.3.4-7
- Rebuild for OCaml 4.00.1.
- Remove Group lines from the spec file.

* Tue Sep 25 2012 Richard W.M. Jones <rjones@redhat.com> - 0.3.4-6
- (RHEL only) Disable camomile, ocaml-ounit, tests.
- Modernize the spec file.

* Sat Jul 28 2012 Richard W.M. Jones <rjones@redhat.com> - 0.3.4-5
- Bump and rebuild against new OCaml 4.00.0 official release.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 09 2012 Richard W.M. Jones <rjones@redhat.com> - 0.3.4-3
- Rebuild for OCaml 4.00.0.

* Sat May 19 2012 Richard W.M. Jones <rjones@redhat.com> - 0.3.4-2
- Bump release and rebuild for new OCaml on ARM.
- Enable ppc64 support for camomile.

* Fri Jan  6 2012 Richard W.M. Jones <rjones@redhat.com> - 0.3.4-1
- New upstream version 0.3.4.
- Remove patch, now upstream.

* Wed Dec 21 2011 Karsten Hopp <karsten@redhat.com> 0.3.3-8
- fix configure line

* Wed Dec 21 2011 Karsten Hopp <karsten@redhat.com> 0.3.3-7
- build with 'make all', not 'make' as that defaults to 'make test' and fails on ppc64
  due to the missing gettext-camomile

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan  6 2011 Richard W.M. Jones <rjones@redhat.com> - 0.3.3-5
- Add patch for compiling against camomile 0.8.

* Wed Jan 05 2011 Richard W.M. Jones <rjones@redhat.com> - 0.3.3-4
- Rebuild for OCaml 3.12 (http://fedoraproject.org/wiki/Features/OCaml3.12).

* Mon Jan 11 2010 Richard W.M. Jones <rjones@redhat.com> - 0.3.3-3
- Remove BR ocaml-camlidl.  No longer required to build this.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 0.3.3-2
- Rebuild for OCaml 3.11.2.

* Mon Nov  2 2009 Richard W.M. Jones <rjones@redhat.com> - 0.3.3-1
- New upstream release 0.3.3 (mainly small bugfixes).
- This requires ocaml-fileutils 0.4.0 and is incompatible with
  any earlier version.
- Fixed a number of rpmlint warnings with *.ml files in the
  non-devel package.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 0.3.2-8
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec  5 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.2-6
- Patch to temporarily fix missing dynlink.cma.
- Rebuild for OCaml 3.11.0.

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.2-5
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.2-4
- Rebuild for OCaml 3.11.0

* Mon Jun  9 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.2-2
- Need to disable tests on ppc64 as well since the tests only work
  with gettext-camomile.

* Mon Jun  9 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.2-1
- New upstream release 0.3.2 (fixeds rhbz 446916).

* Tue May 27 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.1-3
- Enable tests, add check section.

* Tue May 27 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.1-2
- Patch to fix BZ 446916.

* Tue May 27 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.1-1
- New upstream version 0.3.1.
- Extra runtime requirements (BZ 446919).

* Wed Apr 30 2008 Richard W.M. Jones <rjones@redhat.com> - 0.3.0-1
- New upstream version 0.3.0.
- Big patch no longer required (integrated with upstream).
- findlib < 1.2.1-3 known not to work with this.
- build/ -> _build/
- Re-enable documentation.
- Prevent *.o files from being distributed.
- Distribute *.cmx and *.mli files.

* Sat Apr 26 2008 Richard W.M. Jones <rjones@redhat.com> - 0.2.0-3.20080321patch
- Change the naming scheme to conform with "Snapshot packages" guideline.
- Don't duplicate all the docs in camomile-devel.
- Disable documentation.  Wants 'fop', but 'fop' throws a giant Java
  exception when present.

* Thu Apr 17 2008 Richard W.M. Jones <rjones@redhat.com> - 0.2.0-2rwmj20080321
- Build camomile subpackages because the camomile dependency is
  rather large.  However we can't build camomile on ppc64 yet so
  don't build those subpackages there.

* Fri Mar 21 2008 Richard W.M. Jones <rjones@redhat.com> - 0.2.0-1rwmj20080321
- Initial RPM release.
