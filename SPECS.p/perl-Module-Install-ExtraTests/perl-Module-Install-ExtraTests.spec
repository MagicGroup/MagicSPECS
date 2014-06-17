Name:       perl-Module-Install-ExtraTests 
Version:    0.007
Release:    5%{?dist}
License:    GPL+ or Artistic
Group:      Development/Libraries
Summary:    Ignorable, contextual test support for Module::Install
Url:        http://search.cpan.org/dist/Module-Install-ExtraTests
Source:     http://search.cpan.org/CPAN/authors/id/R/RJ/RJBS/Module-Install-ExtraTests-%{version}.tar.gz 
BuildArch:  noarch
BuildRequires:  perl(Module::Install)
# Run-time
BuildRequires:  perl(ExtUtils::Command)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Module::Install::Base)
# Tests
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(ExtUtils::Command)
Requires:       perl(File::Find)
Requires:       perl(File::Spec)

%description
This allows extra_tests; to be declared in Makefile.PL, indicating that the 
test files found in the directory ./xt should be run only in certain 
instances:

  ./xt/author  - run when the tests are being run in an author's working copy
  ./xt/smoke   - run when the dist is being smoked (AUTOMATED_TESTING=1)
  ./xt/release - run during "make disttest"

%prep
%setup -q -n Module-Install-ExtraTests-%{version}
# Update bundled Module::Install from system
touch inc/.author

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'
%{_fixperms} %{buildroot}/*

%check


%files
%doc Changes LICENSE README 
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.007-5
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.007-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.007-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.007-2
- Perl 5.16 rebuild

* Mon Jan 30 2012 Petr Pisar <ppisar@redhat.com> - 0.007-1
- 0.007 bump

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.006-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.006-8
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.006-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.006-6
- 661697 rebuild for fixing problems with vendorach/lib

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.006-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.006-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.006-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.006-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 16 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.006-1
- update to 0.006

* Thu Oct 23 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.004-2
- bump

* Thu Oct 23 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.004-1
- update to 0.004

* Sat Sep 06 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.003-1
- initial Fedora packaging
- generated with cpan2dist (CPANPLUS::Dist::Fedora version 0.0.1)
