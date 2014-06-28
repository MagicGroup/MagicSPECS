%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)
%global debug_package %{nil}

Name:           ocaml-perl4caml
Version:        0.9.5
Release:        30%{?dist}
Summary:        OCaml library for calling Perl libraries and code
License:        LGPLv2+ with exceptions

URL:            http://git.annexia.org/?p=perl4caml.git;a=summary
# There is currently no website hosting the tarballs.
Source0:        perl4caml-%{version}.tar.gz

ExcludeArch:    sparc64 s390 s390x

# Include upstream patch for Perl 5.12:
# http://git.annexia.org/?p=perl4caml.git;a=commitdiff_plain;h=4cb12aa05bd5aa69ccfa1c6d41ab10bc79a3c3a3
Patch0:         perl4caml-0.9.5-svtrv.patch

BuildRequires:  ocaml >= 3.10.0
BuildRequires:  ocaml-ocamldoc
BuildRequires:  perl-devel >= 5.8
BuildRequires:  perl(ExtUtils::Embed)

# Perl4caml provides type-safe wrappers for these Perl modules:
#Requires:  perl-Date-Calc
##Requires:  perl-Date-Format
##Requires:  perl-Date-Parse
##Requires:  perl-Net-Google
##Requires:  perl-HTML-Element
#Requires:  perl-HTML-Parser
#Requires:  perl-HTML-Tree
#Requires:  perl-libwww-perl
#Requires:  perl-Template-Toolkit
#Requires:  perl-URI
#Requires:  perl-WWW-Mechanize

# RHBZ#533948
Requires: perl-libs%{?_isa}

# We're also going to pick up a versioned dependency, to help track things:
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))


%description
Perl4caml allows you to use Perl code within Objective CAML (OCaml),
thus neatly side-stepping the (old) problem with OCaml which was that
it lacked a comprehensive set of libraries. Well now you can use any
part of CPAN in your OCaml code.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%setup -q -n perl4caml-%{version}
%patch0 -p1
find -name .cvsignore -exec rm {} \;


%build
# Parallel builds don't work:
unset MAKEFLAGS

make EXTRA_EXTRA_CFLAGS="$RPM_OPT_FLAGS" \
     OCAMLC="ocamlc.opt" OCAMLOPT="ocamlopt.opt -g"
rm -f examples/*.{cmi,cmo,cmx,o,bc,opt}


%check
# Parallel builds don't work:
unset MAKEFLAGS

# Set the library path used by ocamlrun so it uses the library
# we just built in the current directory.
CAML_LD_LIBRARY_PATH=`pwd` make test


%install
export DESTDIR=$RPM_BUILD_ROOT
mkdir -p $DESTDIR/%{_libdir}/ocaml/stublibs

make install

# Don't delete rpath!  See:
# https://www.redhat.com/archives/fedora-packaging/2008-March/thread.html#00070


%files
%doc COPYING.LIB
%{_libdir}/ocaml/perl
%if %opt
%exclude %{_libdir}/ocaml/perl/*.a
%exclude %{_libdir}/ocaml/perl/*.cmxa
%endif
%exclude %{_libdir}/ocaml/perl/*.mli
%exclude %{_libdir}/ocaml/perl/*.ml
%{_libdir}/ocaml/stublibs/*.so


%files devel
%doc COPYING.LIB AUTHORS doc/* examples html README
%if %opt
%{_libdir}/ocaml/perl/*.a
%{_libdir}/ocaml/perl/*.cmxa
%endif
%{_libdir}/ocaml/perl/*.mli
%{_libdir}/ocaml/perl/*.ml


%changelog
* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 0.9.5-30
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Sep 19 2013 Richard W.M. Jones <rjones@redhat.com> - 0.9.5-27
- OCaml 4.01.0 rebuild.
- Modernize the spec file.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.9.5-25
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 29 2012 Richard W.M. Jones <rjones@redhat.com> - 0.9.5-23
- Rebuild for OCaml 4.00.1.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Petr Pisar <ppisar@redhat.com> - 0.9.5-21
- Perl 5.16 rebuild

* Sat Jun 09 2012 Richard W.M. Jones <rjones@redhat.com> - 0.9.5-20
- Rebuild for OCaml 4.00.0.

* Fri Jan 06 2012 Richard W.M. Jones <rjones@redhat.com> - 0.9.5-19
- Rebuild for OCaml 3.12.1.

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.9.5-18
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 05 2011 Richard W.M. Jones <rjones@redhat.com> - 0.9.5-16
- Rebuild for OCaml 3.12 (http://fedoraproject.org/wiki/Features/OCaml3.12).

* Sun Jun 27 2010 Ralf Corsepius <corsepiu@fedoraproject.org> - 0.9.5-15
- Once more rebuild with perl-5.12.x.

* Tue Jun  8 2010 Richard W.M. Jones <rjones@redhat.com> - 0.9.5-14
- Fix for perl-libs dependency (RHBZ#533948).
- Include upstream patch for Perl 5.12 (Iain Arnell).

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.9.5-13
- Mass rebuild with perl-5.12.0

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 0.9.5-12
- Rebuild for OCaml 3.11.2.

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.9.5-11
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 0.9.5-9
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 0.9.5-7
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 0.9.5-6
- Rebuild for OCaml 3.11.0

* Wed Apr 23 2008 Richard W.M. Jones <rjones@redhat.com> - 0.9.5-5
- Rebuild for OCaml 3.10.2.

* Tue Mar 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.9.5-4
- add Requires for versioned perl (libperl.so)

* Wed Mar 12 2008 Richard W.M. Jones <rjones@redhat.com> - 0.9.5-3
- Fix %check rule (#436785).
- Use rpath for dllperl4caml.so as per this thread:
  https://www.redhat.com/archives/fedora-packaging/2008-March/thread.html#00070
  (#436807).
- Require rpath.

* Tue Mar  4 2008 Richard W.M. Jones <rjones@redhat.com> - 0.9.5-2
- Rebuild for ppc64.

* Sat Mar  1 2008 Richard W.M. Jones <rjones@redhat.com> - 0.9.5-1
- New upstream release 0.9.5.
- Clarify license is LGPLv2+ with exceptions
- Remove excessive BuildRequires - Perl modules not needed for building.
- Pass RPM C flags to the make.
- 'make test' fails where perl4caml is already installed.

* Sat Feb 23 2008 Richard W.M. Jones <rjones@redhat.com> - 0.9.4-1
- Initial RPM release.
