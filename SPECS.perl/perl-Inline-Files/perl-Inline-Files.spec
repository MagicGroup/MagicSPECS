Name:           perl-Inline-Files
Version:	0.69
Release:	1%{?dist}
Summary:        Allows for multiple inline files in a single perl file
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Inline-Files/
Source0:        http://search.cpan.org/CPAN/authors/id/A/AM/AMBS/Inline-Files-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
# Tests only:
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(Filter::Util::Call)
BuildRequires:  perl(Test)
BuildRequires:  perl(Test::More)
Requires:       perl(Data::Dumper)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Inline::Files generalizes the notion of the `__DATA__' marker and the
associated `<DATA>' file handle, to an arbitrary number of markers and
associated file handles.

%prep
%setup -q -n Inline-Files-%{version}
chmod -R a-x demo/* README Changes lib/Inline/Files.pm \
    lib/Inline/Files/Virtual.pm

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check


%files
%doc Changes README demo/
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.69-1
- 更新到 0.69

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.68-6
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.68-5
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.68-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.68-3
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.68-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 25 2011 Petr Sabata <contyk@redhat.com> - 0.68-1
- 0.68 bump

* Mon Jul 18 2011 Petr Sabata <contyk@redhat.com> - 0.67-2
- Perl mass rebuild

* Mon Jul 11 2011 Petr Sabata <contyk@redhat.com> - 0.67-1
- 0.67 bump

* Mon Jun 20 2011 Petr Pisar <ppisar@redhat.com> - 0.65-1
- 0.65 bump
- Remove defattr
- Correct spelling in description

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.64-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.64-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 01 2011 Petr Pisar <ppisar@redhat.com> - 0.64-1
- 0.64 bump
- Remove BuildRoot stuff and empty lines
- Consolidate dependencies

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.63-2
- 661697 rebuild for fixing problems with vendorach/lib

* Wed Jul 14 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 0.63-1
- update to 0.63

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.62-8
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.62-7
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.62-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.62-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.62-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.62-3
- rebuild for new perl

* Wed Nov 14 2007 Robin Norwood <rnorwood@redhat.com> - 0.62-2
- Fix permissions per package review.

* Wed Oct 24 2007 Robin Norwood <rnorwood@redhat.com> - 0.62-1
- Initial build
