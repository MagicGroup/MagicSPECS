Name:           perl-YAML-Syck
Version:        1.20 
Release:        4%{?dist}
Summary:        Fast, lightweight YAML loader and dumper
License:        BSD and MIT
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/YAML-Syck/
Source0:        http://www.cpan.org/authors/id/T/TO/TODDR/YAML-Syck-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Keep bundled inc::Module::Install to break cycle perl-Modules-Install
# → perl-YAML-Tiny → perl-YAML-Syck.
BuildRequires:  perl(Cwd)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(lib)
BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time
BuildRequires:  perl(constant)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(XSLoader)
# Tests
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(Storable)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Tie::Hash)
# Optional tests
BuildRequires:  perl(Devel::Leak)
BuildRequires:  perl(JSON)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
This module provides a Perl interface to the libsyck data serialization
library. It exports the Dump and Load functions for converting Perl data
structures to YAML strings, and the other way around.

%prep
%setup -q -n YAML-Syck-%{version}
rm -rf inc/parent inc/PerlIO.pm inc/Test

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes COMPATIBILITY COPYING README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/YAML*
%{perl_vendorarch}/JSON*
%{_mandir}/man3/*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.20-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 1.20-2
- Perl 5.16 rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 1.20-1
- 1.20 bump

* Sat Jun 16 2012 Petr Pisar <ppisar@redhat.com> - 1.17-5
- Perl 5.16 rebuild
- Specify all dependencies

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Iain Arnell <iarnell@gmail.com> - 1.17 -3
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 07 2010 Steven Pritchard <steve@kspei.com> 1.17-1
- Update to 1.17.
- Update Source0 URL.
- BR JSON (for tests).

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.07-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.07-3
- rebuild against perl 5.10.1

* Tue Oct  6 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1.07-2
- fix license

* Sun Sep 27 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.07-1
- auto-update to 1.07 (by cpan-spec-update 0.01)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jun 09 2008 Steven Pritchard <steve@kspei.com> 1.05-1
- Update to 1.05.

* Mon Mar  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.04-2
- rebuild for new perl (again)

* Wed Feb 20 2008 Steven Pritchard <steve@kspei.com> 1.04-1
- Update to 1.04.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.01-3
- Autorebuild for GCC 4.3

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.01-2
- rebuild for new perl

* Mon Jan 28 2008 Steven Pritchard <steve@kspei.com> 1.01-1
- Update to 1.01.

* Tue Oct 16 2007 Steven Pritchard <steve@kspei.com> 0.98-1
- Update to 0.98.

* Tue Sep 18 2007 Steven Pritchard <steve@kspei.com> 0.97-1
- Update to 0.97.

* Sun Aug 12 2007 Steven Pritchard <steve@kspei.com> 0.96-1
- Update to 0.96.

* Fri Aug 03 2007 Steven Pritchard <steve@kspei.com> 0.95-1
- Update to 0.95.

* Fri Jul 13 2007 Steven Pritchard <steve@kspei.com> 0.94-1
- Update to 0.94.

* Wed Jun 27 2007 Steven Pritchard <steve@kspei.com> 0.91-1
- Update to 0.91.

* Sat May 19 2007 Steven Pritchard <steve@kspei.com> 0.85-1
- Update to 0.85.

* Fri May 04 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.82-3
- add perl split BR's

* Fri May 04 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.82-2
- bump

* Thu Feb 01 2007 Steven Pritchard <steve@kspei.com> 0.82-1
- Specfile autogenerated by cpanspec 1.69.1.
- Remove explicit build dependency on perl.
- Include JSON module.
- BR Devel::Leak (for tests).
