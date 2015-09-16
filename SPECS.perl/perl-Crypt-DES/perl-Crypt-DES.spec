Name:           perl-Crypt-DES
Version:        2.07
Release:        5%{?dist}
Summary:        Perl DES encryption module
License:        BSD
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Crypt-DES/
Source0:        http://www.cpan.org/authors/id/D/DP/DPARIS/Crypt-DES-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
# Tests:
BuildRequires:  perl(Benchmark)
BuildRequires:  perl(Data::Dumper)
# Optional tests:
BuildRequires:  perl(Crypt::CBC) > 1.22
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%{?perl_default_filter}

%description
DES encryption module.

%prep
%setup -q -n Crypt-DES-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc COPYRIGHT README
%{perl_vendorarch}/auto/Crypt/
%{perl_vendorarch}/Crypt/
%{_mandir}/man3/Crypt::DES.3pm*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 2.07-5
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 2.07-4
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 2.07-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Oct  3 2013 Paul Howarth <paul@city-fan.org> - 2.07-1
- Update to 2.07
  - SvUPGRADE was changed to a statement
- This release by DPARIS -> update source URL
- Changes file dropped upstream
- Drop %%defattr, redundant since rpm 4.4
- Make %%files list more explicit
- Don't need to remove empty directories from the buildroot
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Don't use macros for commands

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.05.002-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 19 2013 Petr Pisar <ppisar@redhat.com> - 2.05.002-1
- 2.05_002 bump

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 2.05-20
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.05-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.05-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 2.05-17
- Perl 5.16 rebuild

* Fri May 25 2012 Petr Pisar <ppisar@redhat.com> - 2.05-16
- Update build-time dependencies
- Do not export private libraries

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.05-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.05-14
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.05-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.05-12
- Rebuild to fix problems with vendorarch/lib (#661697)

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.05-11
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 2.05-10
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.05-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.05-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Mar  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.05-7
- rebuild for new perl (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.05-6
- Autorebuild for GCC 4.3

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.05-5
- rebuild for new perl

* Tue Apr 17 2007 Steven Pritchard <steve@kspei.com> 2.05-4
- Use fixperms macro instead of our own chmod incantation.
- BR ExtUtils::MakeMaker.

* Mon Aug 28 2006 Steven Pritchard <steve@kspei.com> 2.05-3
- Fix find option order.
- Minor spec cleanup to more closely match cpanspec output.

* Sat Feb 18 2006 Steven Pritchard <steve@kspei.com> 2.05-2
- Rebuild.

* Thu Feb 02 2006 Steven Pritchard <steve@kspei.com> 2.05-1
- Update to 2.05.
- Drop explicit Requires: perl(Crypt::CBC).
- LD_RUN_PATH hack shouldn't be needed now.
- Trim file list a bit.
- License is BSD, more or less.

* Sat Sep 17 2005 Steven Pritchard <steve@kspei.com> 2.03-2
- Minor spec cleanup.

* Fri Aug 26 2005 Steven Pritchard <steve@kspei.com> 2.03-1
- Specfile autogenerated.
