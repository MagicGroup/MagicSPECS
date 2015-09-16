Name:       perl-CPANPLUS-Shell-Default-Plugins-RT 
Version:    0.01 
Release:    14%{?dist}
# see README 
License:    GPL+ or Artistic
Group:      Development/Libraries
Summary:    Check for rt.cpan.org tickets from within the CPANPLUS shell 
Source:     http://search.cpan.org/CPAN/authors/id/K/KA/KANE/CPANPLUS-Shell-Default-Plugins-RT-%{version}.tar.gz 
Url:        http://search.cpan.org/dist/CPANPLUS-Shell-Default-Plugins-RT
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:  noarch

BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(CPANPLUS) >= 0.059
BuildRequires: perl(Locale::Maketext::Simple)
BuildRequires: perl(LWP)
BuildRequires: perl(Params::Check) >= 0.23
# testing...
BuildRequires: perl(Test::More)

# not automagically picked up...
Requires:      perl(CPANPLUS::Shell::Default)

%description
This plugin allows you to query rt.cpan.org tickets for a given
distribution within the CPANPLUS shell.


%prep
%setup -q -n CPANPLUS-Shell-Default-Plugins-RT-%{version}

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


%clean
rm -rf %{buildroot} 

%files
%defattr(-,root,root,-)
%doc README 
%{perl_vendorlib}/*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.01-14
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.01-13
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.01-12
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.01-11
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.01-10
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.01-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.01-8
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.01-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.01-6
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.01-5
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.01-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.01-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 17 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.01-1
- update for submission
- add explicit requires on perl(CPANPLUS::Shell::Default)

* Mon Feb 16 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.01-0
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)

