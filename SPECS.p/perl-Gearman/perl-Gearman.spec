Name:           perl-Gearman
Version:        1.11
Release:        7%{?dist}
Summary:        Distributed job system
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://danga.com/gearman/
Source0:        http://search.cpan.org/CPAN/authors/id/D/DO/DORMANDO/Gearman-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  perl(Test::More)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(String::CRC32)

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Gearman is a system to farm out work to other machines,
dispatching function calls to machines that are better suited to do work,
to do work in parallel, to load balance lots of function calls,
or to call functions between languages.

%prep
%setup -q -n Gearman-%{version}

# Filter double proved for Gearman::Client:
cat << \EOF > %{name}-prov
#!/bin/sh
%{__perl_provides} $* |\
  sed -e '/^perl(Gearman::Client)$/d'
EOF

%define __perl_provides %{_builddir}/Gearman-%{version}/%{name}-prov
chmod +x %{__perl_provides}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check


%files
%defattr(-,root,root,-)
%doc CHANGES HACKING TODO
%{perl_vendorlib}/Gearman
%{_mandir}/man3/Gearman::*.*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.11-7
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.11-6
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.11-4
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
- rebuild for new per

* Sat Jun 30 2007 Ruben Kerkhof <ruben@rubenkerkhof.com> 1.09-1
- Upstream released new version
- New version now includes license information
- Filter out just one of the two Provides for Gearman::Client
* Thu Jun 28 2007 Ruben Kerkhof <ruben@rubenkerkhof.com> 1.08-2
- Filter out double Provides for Gearman::Client
- Change Source0 url
* Mon May 21 2007 Ruben Kerkhof <ruben@rubenkerkhof.com> 1.08-1
- Initial import

