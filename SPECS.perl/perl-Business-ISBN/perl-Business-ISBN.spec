Name:           perl-Business-ISBN
Version:	2.09
%define module_version 2.05_03
Release:	1%{?dist}
Summary:        Perl module to work with International Standard Book Numbers
Summary(zh_CN.UTF-8): 国际标准书刊号的 Perl 模块

Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Business-ISBN/
Source0:        http://search.cpan.org/CPAN/authors/id/B/BD/BDFOY/Business-ISBN-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(base)
BuildRequires:  perl(Business::ISBN::Data)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(GD::Barcode::EAN13)
BuildRequires:  perl(IO::Socket)
BuildRequires:  perl(LWP::Simple)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))


%description
This modules handles International Standard Book Numbers, including
ISBN-10 and ISBN-13.

%description -l zh_CN.UTF-8
国际标准书刊号的 Perl 模块。

%prep
%setup -q -n Business-ISBN-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*
magic_rpm_clean.sh

%check



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes README LICENSE examples/
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%changelog
* Thu Apr 30 2015 Liu Di <liudidi@gmail.com> - 2.09-1
- 更新到 2.09

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.05.03-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.05.03-5
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.05.03-4
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 2.05.03-3
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.05.03-2
- 为 Magic 3.0 重建

* Tue Oct 09 2012 Jitka Plesnikova <jplesnik@redhat.com> - 2.05.03-1
- 2.05_03 bump. Fix failing tests (RT#78671, RT#75686)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.05-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Petr Pisar <ppisar@redhat.com> - 2.05-8
- Perl 5.16 rebuild
- Specify all dependencies

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.05-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 2.05-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.05-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.05-4
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.05-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.05-2
- rebuild against perl 5.10.1

* Mon Oct  5 2009 Stepan Kasal <skasal@redhat.com> - 2.05-1
- new upstream version

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.04_01-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.04_01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Nov 24 2008 Stepan Kasal <skasal@redhat.com> - 2.04_01-1
- new upstream version
- drop integrated patch

* Thu Feb  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.03-4
- rebuild for new perl

* Fri Oct 26 2007 Robin Norwood <rnorwood@redhat.com> - 2.03-3
- Apply patch to fix barcode test

* Thu Oct 25 2007 Robin Norwood <rnorwood@redhat.com> - 2.03-2
- Fix buildrequires and doc list

* Thu Oct 25 2007 Robin Norwood <rnorwood@redhat.com> - 2.03-1
- Initial build
