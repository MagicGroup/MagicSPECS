Name:       perl-Eval-Context 
Version:    0.07 
Release:    24%{?dist}
# see lib/Eval/Context.pm
License:    GPL+ or Artistic
Group:      Development/Libraries
Summary:    Evalute perl code in context wraper 
Source:     http://search.cpan.org/CPAN/authors/id/N/NK/NKH/Eval-Context-%{version}.tar.gz 
Url:        http://search.cpan.org/dist/Eval-Context
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:  noarch

BuildRequires: perl(ExtUtils::MakeMaker) 
BuildRequires: perl(Module::Build::Compat)
BuildRequires: perl(Data::Compare)
BuildRequires: perl(Data::Dumper)
BuildRequires: perl(Data::TreeDumper)
BuildRequires: perl(Directory::Scratch::Structured)
BuildRequires: perl(File::Slurp)
BuildRequires: perl(Package::Generator)
BuildRequires: perl(Readonly)
BuildRequires: perl(Safe)
BuildRequires: perl(Sub::Exporter)
BuildRequires: perl(Sub::Install)
BuildRequires: perl(Symbol)
BuildRequires: perl(Test::More)
BuildRequires: perl(Test::Block)
BuildRequires: perl(Test::Dependencies)
BuildRequires: perl(Test::Distribution)
BuildRequires: perl(Test::Exception)
BuildRequires: perl(Test::NoWarnings)
BuildRequires: perl(Test::Output)
#BuildRequires: perl(Test::Perl::Critic)
BuildRequires: perl(Test::Pod)
BuildRequires: perl(Test::Pod::Coverage)
BuildRequires: perl(Test::Spelling)
BuildRequires: perl(Test::Strict)
BuildRequires: perl(Test::Warn)
BuildRequires: perl(version) >= 0.5


%description
This module defines a subroutine that let you evaluate Perl code in a
specific context. The code can be passed directly as a string or as a file
name to read from.  It also provides some subroutines to let you define and
optionally share variables and subroutines between your code and the code
you wish to evaluate. Finally there is some support for running your code
in a safe compartment.

%prep
%setup -q -n Eval-Context-%{version}

perl -pi -e 's/^#~ //' t/003*

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

%check
# note: Test::Fixme and Test::Kwalitee are both author tests, not tests that
# exercise functionality


%clean
rm -rf %{buildroot} 

%files
%defattr(-,root,root,-)
%doc README Changes Todo.txt 
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.07-24
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.07-23
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.07-22
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.07-21
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.07-20
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.07-19
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.07-18
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.07-17
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.07-16
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.07-15
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.07-14
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.07-13
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.07-12
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.07-10
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.07-8
- 661697 rebuild for fixing problems with vendorach/lib

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.07-7
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.07-6
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.07-5
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 10 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.07-2
- drop Test::Perl::Critic -- it's failing, and an author test to boot

* Sat Nov 29 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.07-1
- update for submission

* Sat Nov 29 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.07-0.1
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.5)

