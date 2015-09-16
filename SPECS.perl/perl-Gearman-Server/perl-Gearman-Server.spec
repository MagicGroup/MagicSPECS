Name:           perl-Gearman-Server
Version:	1.12
Release:	1%{?dist}
Summary:        Function call "router" and load balancer
License:        GPL+ or Artistic
Group:          System Environment/Daemons
URL:            http://search.cpan.org/dist/Gearman-Server/
Source0:        http://search.cpan.org/CPAN/authors/id/D/DO/DORMANDO/Gearman-Server-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  perl(ExtUtils::MakeMaker)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
You run a Gearman server (or more likely, many of them for both high-
availability and load balancing), then have workers (using Gearman::Worker
from the Gearman module, or libraries for other languages) register their
ability to do certain functions to all of them, and then clients (using
Gearman::Client, Gearman::Client::Async, etc) request work to be done from
one of the Gearman servers.

%prep
%setup -q -n Gearman-Server-%{version}

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
%doc CHANGES
%{_bindir}/gearmand
%{perl_vendorlib}/Gearman
%{_mandir}/man1/gearmand.*
%{_mandir}/man3/Gearman::*.*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.12-1
- 更新到 1.12

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.11-8
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.11-7
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.11-6
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.11-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.11-2
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Jun 24 2010 Ruben Kerkhof <ruben@rubenkerkhof.com> 1.11-1
- Upstream released new version

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.09-6
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.09-5
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.09-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.09-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.09-2
- rebuild for new perl

* Sun May 20 2007 Ruben Kerkhof <ruben@rubenkerkhof.com> 1.09-1
- Initial import

