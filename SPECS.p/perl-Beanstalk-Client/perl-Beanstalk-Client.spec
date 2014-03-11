Name:           perl-Beanstalk-Client
Version:        1.06
Release:        10%{?dist}
Summary:        Client class to talk to a beanstalkd server
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Beanstalk-Client/
Source0:        http://search.cpan.org/CPAN/authors/id/G/GB/GBARR/Beanstalk-Client-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(Class::Accessor::Fast)
BuildRequires:  perl(Error)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(YAML::Syck)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Beanstalk::Client provides a Perl API of protocol version 1.0 to the
beanstalkd server, a fast, general-purpose, in-memory workqueue service by
Keith Rarick.

%prep
%setup -q -n Beanstalk-Client-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*

%check


%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/Beanstalk
%{_mandir}/man3/Beanstalk::*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.06-10
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.06-9
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.06-8
- 为 Magic 3.0 重建

* Sat Jan 28 2012 Liu Di <liudidi@gmail.com> - 1.06-7
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.06-5
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.06-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.06-2
- 661697 rebuild for fixing problems with vendorach/lib

* Tue Jun 22 2010 Ruben Kerkhof <ruben@rubenkerkhof.com> 1.06-1
- Upstream released new version

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.05-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.05-3
- rebuild against perl 5.10.1

* Wed Jul 29 2009 Ruben Kerkhof <ruben@rubenkerkhof.com> 1.05-2
- Review fixes (#513869)

* Sun Jul 26 2009 Ruben Kerkhof <ruben@rubenkerkhof.com> - 1.05-1
- Initial import
