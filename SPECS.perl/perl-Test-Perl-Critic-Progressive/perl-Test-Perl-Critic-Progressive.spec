Name:           perl-Test-Perl-Critic-Progressive
Version:        0.03
Release:        15%{?dist}
Summary:        Gradually enforce coding standards
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Test-Perl-Critic-Progressive/
Source0:        http://www.cpan.org/authors/id/T/TH/THALJEF/Test-Perl-Critic-Progressive-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Perl::Critic) >= 1.082
BuildRequires:  perl(Perl::Critic::Utils) >= 1.082
BuildRequires:  perl(Test::Builder)
# Tests only:
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage) >= 1.00
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(Perl::Critic) >= 1.082
Requires:       perl(Perl::Critic::Utils) >= 1.082

# Filter underspecified dependencies
%{?perl_default_filter:
%filter_from_requires /^perl(Perl::Critic)$/d
%filter_from_requires /^perl(Perl::Critic::Utils)$/d
%perl_default_filter
}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(Perl::Critic(::Utils)?\\)$

%description
Applying coding standards to large amounts of legacy code is a daunting
task. Often times, legacy code is so non-compliant that it seems downright
impossible. But, if you consistently chip away at the problem, you will
eventually succeed! Test::Perl::Critic::Progressive uses the Perl::Critic
engine to prevent further deterioration of your code and gradually steer it
towards conforming with your chosen coding standards.

%prep
%setup -q -n Test-Perl-Critic-Progressive-%{version}

%build
%{__perl} Build.PL installdirs=vendor
./Build

%install
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
./Build test

%files
%defattr(-,root,root,-)
%doc Changes LICENSE README TODO
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.03-15
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.03-14
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.03-13
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.03-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.03-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.03-10
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.03-9
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 0.03-7
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 25 2011 Iain Arnell <iarnell@gmail.com> 0.03-5
- update filtering for rpm 4.9

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.03-4
- Perl mass rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.03-3
- Perl mass rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.03-2
- Perl mass rebuild

* Thu Jan 27 2011 Petr Pisar <ppisar@redhat.com> 0.03-1
- Specfile autogenerated by cpanspec 1.78.
- Remove BuildRoot stuff