Name:		perl-Text-CSV
Version:	1.33
Release:	1%{?dist}
Summary:	Comma-separated values manipulator

Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/Text-CSV/
Source0:	http://search.cpan.org/CPAN/authors/id/M/MA/MAKAMAKA/Text-CSV-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:	perl(IO::Handle)

BuildArch:	noarch

BuildRequires:	perl(ExtUtils::MakeMaker)

# For test suite
BuildRequires:	perl(base)
BuildRequires:	perl(Carp)
BuildRequires:	perl(Test::Harness)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Test::Pod) >= 1.00
BuildRequires:	perl(IO::Handle)

%{?perl_default_filter}

%description
Text::CSV provides facilities for the composition and decomposition of
comma-separated values.  An instance of the Text::CSV class can combine
fields into a CSV string and parse a CSV string into fields.

The module accepts either strings or files as input and can utilize any
user-specified characters as delimiters, separators, and escapes so it is
perhaps better called ASV (anything separated values) rather than just CSV.

%prep
%setup -q -n Text-CSV-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%{__make} %{?_smp_mflags}

%check
%{__make} test TEST_VERBOSE=1

%install
%{__rm} -rf %{buildroot}
%{__make} pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'
%{__chmod} -R u+w %{buildroot}/*

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.33-1
- 更新到 1.33

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.21-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.21-7
- 为 Magic 3.0 重建

* Wed Aug 08 2012 Jitka Plesnikova <jplesnik@redhat.com> - 1.21-6
- Specify all dependencies.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.21-4
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.21-2
- Perl mass rebuild

* Tue Apr 05 2011 Johan Vromans <jvromans@squirrel.nl> 1.21-1
- Upgrade to upstream 1.21.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.18-2
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Jul  1 2010 Johan Vromans - 1.18-1
- Upgrade to upstream 1.18.

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.16-2
- Mass rebuild with perl-5.12.0

* Wed Mar 17 2010 Chris Weyl <cweyl@alumni.drew.edu> 1.16-1
- PERL_INSTALL_ROOT => DESTDIR, add perl_default_filter
- auto-update to 1.16 (by cpan-spec-update 0.01) (for DBIx::Class)
- added a new br on perl(Test::Harness) (version 0)

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.10-3
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jan 31 2009 Johan Vromans <jvromans@squirrel.nl> 1.10-1
- Initial Fedora RPM version
