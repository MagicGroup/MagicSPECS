Name:           perl-POE-Component-Client-DNS
Version:        1.051
Release:        8%{?dist}
Summary:        Non-blocking/concurrent DNS queries using Net::DNS and POE

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/POE-Component-Client-DNS
Source0:        http://search.cpan.org/CPAN/authors/id/R/RC/RCAPUTO/POE-Component-Client-DNS-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

BuildArch:      noarch
BuildRequires:  perl(Net::DNS) >= 0.59
BuildRequires:  perl(ExtUtils::MakeMaker)
# Original perl(POE) >= 1.28 rounded to 3 digit precision
BuildRequires:  perl(POE) >= 1.280
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::NoWarnings) >= 0.084

Requires:       perl(Net::DNS) >= 0.59
# Original perl(POE) >= 1.28 rounded to 3 digit precision
Requires:       perl(POE) >= 1.280

%{?perl_default_filter}

%description
POE::Component::Client::DNS provides a facility for non-blocking, concurrent
DNS requests. Using POE, it allows other tasks to run while waiting for name
servers to respond.


%prep
%setup -q -n POE-Component-Client-DNS-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

# the perldoc/pod documentation is nice, but I really found this much more
# useful.
cp t/01_resolve.t example_resolve


%check
# tests are not conducted as they require network access.
%{?_with_network_tests: make test }


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc CHANGES README example_resolve
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.051-8
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.051-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 1.051-6
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.051-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.051-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.051-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.051-2
- 661697 rebuild for fixing problems with vendorach/lib

* Tue Jun  8 2010 Petr Pisar <ppisar@redhat.com> - 1.051-1
- 1.051 bump

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.050-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.050-2
- rebuild against perl 5.10.1

* Sun Sep 27 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.050-1
- auto-update to 1.050 (by cpan-spec-update 0.01)
- added a new br on perl(Test::NoWarnings) (version 0.084)

* Tue Aug 25 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.04-1
- auto-update to 1.04 (by cpan-spec-update 0.01)
- added a new br on perl(ExtUtils::MakeMaker) (version 0)
- altered br on perl(POE) (0.31 => 1.007)
- added a new req on perl(Net::DNS) (version 0.59)
- added a new req on perl(POE) (version 1.007)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May 21 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.03-1
- auto-update to 1.03 (by cpan-spec-update 0.01)
- added a new br on perl(Test::More) (version 0)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.00-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.00-2
- rebuild for new perl

* Thu Jan 11 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.00-1
- update to 1.00
- bump br on Net::DNS to >= 0.59

* Thu Aug 31 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.99-2
- bump for mass rebuild

* Sat Jul 15 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.99-1
- bump for f-e release

* Thu Jul 13 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.99-0
- Initial spec file for F-E
