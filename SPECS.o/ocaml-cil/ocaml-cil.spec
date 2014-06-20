%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

Name:           ocaml-cil
Version:        1.7.3
Release:        5%{?dist}
Summary:        CIL - Infrastructure for C Program Analysis and Transformation
License:        BSD

URL:            http://cil.sourceforge.net/
Source0:        http://downloads.sourceforge.net/cil/cil-%{version}.tar.gz

# RHBZ#994968
ExcludeArch:    armv7hl
ExcludeArch:    sparc64
ExcludeArch:    s390 s390x

BuildRequires:  ocaml, ocaml-findlib-devel, ocaml-ocamldoc

Patch0:         0001-Fix-testsuite-on-32-bit-machines.patch
Patch1:         0002-Do-not-fail-testsuite-on-new-gcc-behaviour.patch

# Enable ocamlopt -g.
Patch2:         cil-1.7.3-enable-ocamlopt-g.patch

%description
CIL (C Intermediate Language) is a high-level representation along
with a set of tools that permit easy analysis and source-to-source
transformation of C programs.

CIL is both lower-level than abstract-syntax trees, by clarifying
ambiguous constructs and removing redundant ones, and also
higher-level than typical intermediate languages designed for
compilation, by maintaining types and a close relationship with the
source program. The main advantage of CIL is that it compiles all
valid C programs into a few core constructs with a very clean
semantics. Also CIL has a syntax-directed type system that makes it
easy to analyze and manipulate C programs. Furthermore, the CIL
front-end is able to process not only ANSI-C programs but also those
using Microsoft C or GNU C extensions. If you do not use CIL and want
instead to use just a C parser and analyze programs expressed as
abstract-syntax trees then your analysis will have to handle a lot of
ugly corners of the language (let alone the fact that parsing C itself
is not a trivial task).

In essence, CIL is a highly-structured, "clean" subset of C. CIL
features a reduced number of syntactic and conceptual forms. For
example, all looping constructs are reduced to a single form, all
function bodies are given explicit return statements, syntactic sugar
like "->" is eliminated and function arguments with array types become
pointers.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%package        doc
Summary:        Documentation for %{name}
Requires:       %{name} = %{version}-%{release}
BuildRequires:  tex(latex), hevea


%description    doc
The %{name}-doc package contains documentation for users of %{name}.


%package        cilly
Summary:        Support programs for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
# test and doc use cilly: Requires must also be BuildRequires
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(lib)
BuildRequires:  perl(strict)
BuildRequires:  perl(Text::ParseWords)
# Some more dependencies used only for build and test
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(ExtUtils::MakeMaker)
# Filter out wrong Provides (automatically generated)
%global __provides_exclude perl\\(AR|GNUCC|MSLIB|MSLINK|MSVC\\)

%description    cilly
The %{name}-cilly package contains the 'cilly' wrapper/replacement
for gcc.


%prep
%setup -q -n cil-%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1

%build

export PERL_MM_OPT=INSTALLDIRS=vendor

%configure
# make -j is broken, do not use it
unset MAKEFLAGS
make all doc
# Force build of bytecode version even if ocamlopt is available
make OCAMLBEST= bin/cilly.byte

%check
make test

%install

export DESTDIR=$RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml

mkdir -p $OCAMLFIND_DESTDIR
make DESTDIR=$DESTDIR install

# clean up .packlist
find $DESTDIR -name .packlist -type f -exec rm -f {} \;

# make install does not install documentation
# Copy documentation in doc/ocaml-cil, avoiding spurious files not cleaned up by
# CIL
mkdir -p doc/ocaml-cil/html
cp -r doc/html/cil/api doc/ocaml-cil/html
cp -r doc/html/cil/examples doc/ocaml-cil/html
cp doc/html/cil/*.gif doc/ocaml-cil/html/
cp doc/html/cil/*.html doc/ocaml-cil/html/
cp doc/html/cil/*.css doc/ocaml-cil/html/
cp doc/html/cil/CIL.pdf doc/ocaml-cil/cil-manual.pdf

%clean
rm -rf $RPM_BUILD_ROOT


%files
%doc README.md LICENSE
%{_libdir}/ocaml/cil
%if %opt
%exclude %{_libdir}/ocaml/cil/*.a
%exclude %{_libdir}/ocaml/cil/*.cmxa
%exclude %{_libdir}/ocaml/cil/*.cmx
%endif
%exclude %{_libdir}/ocaml/cil/*.mli


%files devel
%doc README.md LICENSE
%if %opt
%{_libdir}/ocaml/cil/*.a
%{_libdir}/ocaml/cil/*.cmxa
%{_libdir}/ocaml/cil/*.cmx
%endif
%{_libdir}/ocaml/cil/*.mli


%files doc
%doc README.md LICENSE doc/ocaml-cil/*

%files cilly
%doc README.md LICENSE
%dir %{perl_vendorlib}/App
%{perl_vendorlib}/App/Cilly
%{perl_vendorlib}/App/Cilly.pm
%{_bindir}/cilly*


%changelog
* Thu Jun 12 2014 Richard W.M. Jones <rjones@redhat.com> - 1.7.3-5
- Bump and rebuild to attempt to fix broken dependencies.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 1.7.3-3
- Rebuild for OCaml 4.01.0.
- Enable debuginfo.

* Tue Sep  3 2013 Richard W.M. Jones <rjones@redhat.com> - 1.7.3-2
- ExcludeArch armv7hl (RHBZ#994968).

* Fri Aug 30 2013 Gabriel Kerneis <gabriel@kerneis.info> - 1.7.3-1
- New upstream version 1.7.3.
- Use upstream make install target.
- Build and install documentation.
- Run test suite.
- Fix perl-related Provides and Requires for -cilly.
- Enable on arm and ppc (fixed by upstream ./configure).
- Apply two upstream patches to test suite.

* Sun Aug  4 2013 Richard W.M. Jones <rjones@redhat.com> - 1.4.0-10
- Disable on arm (not supported by upstream ./configure).
- Modernize the spec file.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.4.0-8
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Dec 02 2012 Bruno Wolff III <bruno@wolff.to> - 1.4.0-6
- Rebuild for ocaml 4.0.1.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 1.4.0-4
- Perl 5.16 rebuild

* Sun Jun 10 2012 Richard W.M. Jones <rjones@redhat.com> - 1.4.0-3
- Rebuild for OCaml 4.00.0.

* Thu Jun 07 2012 Petr Pisar <ppisar@redhat.com> - 1.4.0-2
- Perl 5.16 rebuild
- Specify all Perl dependencies

* Fri Jan  6 2012 Richard W.M. Jones <rjones@redhat.com> - 1.4.0-1
- New upstream version 1.4.0.
- Rebuild for OCaml 3.12.1.

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.3.7-10
- Perl mass rebuild

* Thu Jun 09 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.3.7-9
- Perl 5.14 mass rebuild

* Fri Jan 07 2011 Richard W.M. Jones <rjones@redhat.com> - 1.3.7-8
- Rebuild for OCaml 3.12 (http://fedoraproject.org/wiki/Features/OCaml3.12).
- Patch: Remove '-lstr' option.
- Move configure into %%build section.

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.3.7-6
- Mass rebuild with perl-5.12.0

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 1.3.7-5
- Rebuild for OCaml 3.11.2.

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.3.7-4
- rebuild against perl 5.10.1

* Fri Oct 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.3.7-3
- Include natively compiled files and *.mli files (RHBZ#521324).

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue May 26 2009 Richard W.M. Jones <rjones@redhat.com> - 1.3.7-1
- New upstream version 1.3.7.
- Rebuild for OCaml 3.11.1.

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 21 2009 Richard W.M. Jones <rjones@redhat.com> - 1.3.6-10
- Fix prelink configuration file.

* Fri Dec  5 2008 Richard W.M. Jones <rjones@redhat.com> - 1.3.6-9
- Patch to fix stricter -output-obj checks in OCaml 3.11.0.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 1.3.6-8
- Rebuild for OCaml 3.11.0

* Tue Sep  2 2008 Richard W.M. Jones <rjones@redhat.com> - 1.3.6-7
- Prevent unwanted bytecode stripping by RPM and prelink.
- Place *.ml files into the -devel subpackage.

* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 1.3.6-6
- Fix Perl paths (rhbz#453759).

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 1.3.6-5
- Rebuild for OCaml 3.10.2

* Wed Nov  7 2007 Richard W.M. Jones <rjones@redhat.com> - 1.3.6-4
- ExcludeArch ppc - CIL doesn't build on PPC as it turns out.

* Wed Nov  7 2007 Richard W.M. Jones <rjones@redhat.com> - 1.3.6-3
- Change upstream URL.
- perl(CilConfig) set to package version
- Split out documentation into a separate -doc package.

* Mon Aug 20 2007 Richard W.M. Jones <rjones@redhat.com> - 1.3.6-2
- Initial RPM release.
