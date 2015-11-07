Name:       perl-POE-Component-Pluggable
Version:    1.26
Release:    7%{?dist}
# lib/POE/Component/Pluggable.pm -> GPL+ or Artistic
License:    GPL+ or Artistic
Group:      Development/Libraries
Summary:    A base class for creating plugin-enabled POE components
Source:     http://search.cpan.org/CPAN/authors/id/B/BI/BINGOS/POE-Component-Pluggable-%{version}.tar.gz
Url:        http://search.cpan.org/dist/POE-Component-Pluggable
BuildArch:  noarch
BuildRequires: perl(base)
BuildRequires: perl(constant) >= 1.17
BuildRequires: perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires: perl(Exporter)
BuildRequires: perl(POE) >= 1.004
BuildRequires: perl(Scalar::Util)
BuildRequires: perl(Task::Weaken)
BuildRequires: perl(Test::More) >= 0.47
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:      perl(constant) >= 1.17
Requires:      perl(POE) >= 1.004

%{?perl_default_filter}

%description
POE::Component::Pluggable is a base class for creating plugin enabled
POE Components. It is a generic port of POE::Component::IRC's plugin
system. If your component dispatches events to registered POE sessions,
then POE::Component::Pluggable may be a good fit for you.

%prep
%setup -q -n POE-Component-Pluggable-%{version}

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
%doc Changes examples/ README LICENSE
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 1.26-7
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.26-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.26-5
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.26-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 1.26-2
- Perl 5.16 rebuild

* Tue Jan 17 2012 Petr Šabata <contyk@redhat.com> - 1.26-1
- 1.26 bump
- Spec cleanup, remove excessive whitespace

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.24-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 1.24-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.24-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.24-4
- 661697 rebuild for fixing problems with vendorach/lib

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.24-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.24-2
- rebuild against perl 5.10.1

* Mon Aug 31 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.24-1
- submission

* Mon Aug 31 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.24-0
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)
