Name:           perl-Test-POE-Client-TCP
Version:	1.12
Release:	2%{?dist}
Summary:        POE Component providing TCP client services for test cases
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Test-POE-Client-TCP/
Source0:        http://www.cpan.org/authors/id/B/BI/BINGOS/Test-POE-Client-TCP-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl >= 1:5.6.0
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.42
# Original perl(POE) >= 1.28 rounded to 3 digits
BuildRequires:  perl(POE) >= 1.280
BuildRequires:  perl(POE::Filter)
BuildRequires:  perl(POE::Filter::Line)
BuildRequires:  perl(POE::Wheel::ReadWrite)
BuildRequires:  perl(POE::Wheel::SocketFactory)
BuildRequires:  perl(Test::More) >= 0.47
BuildRequires:  perl(Test::Pod) >= 1.0
BuildRequires:  perl(Test::Pod::Coverage) >= 1.0
Requires:       perl(POE) >= 1.280
Requires:       perl(POE::Filter)
Requires:       perl(POE::Filter::Line)
Requires:       perl(POE::Wheel::ReadWrite)
Requires:       perl(POE::Wheel::SocketFactory)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Test::POE::Client::TCP is a POE component that provides a TCP client
framework for inclusion in client component test cases, instead of having
to roll your own.

%prep
%setup -q -n Test-POE-Client-TCP-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes examples LICENSE README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.12-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.12-1
- 更新到 1.12

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.10-7
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.10-6
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 1.10-4
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.10-2
- Perl mass rebuild

* Thu Jul 07 2011 Petr Pisar <ppisar@redhat.com> - 1.10-1
- 1.10 bump

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.08-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.08-2
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Jun 11 2010 Petr Pisar <ppisar@redhat.com> 1.08-1
- Specfile autogenerated by cpanspec 1.78 (bug #602659)
- Tune depencencies by hand
