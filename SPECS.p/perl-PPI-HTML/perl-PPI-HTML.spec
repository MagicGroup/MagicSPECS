Name:           perl-PPI-HTML
Version:        1.08
Release:        3%{?dist}
Summary:        Generate syntax-highlighted HTML for Perl using PPI
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/PPI-HTML/
Source0:        http://www.cpan.org/authors/id/A/AD/ADAMK/PPI-HTML-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(inc::Module::Install)
# Run-time:
BuildRequires:  perl(CSS::Tiny) >= 1.10
BuildRequires:  perl(Params::Util) => 0.05
BuildRequires:  perl(PPI) >= 0.990
BuildRequires:  perl(PPI::Document)
# Tests:
BuildRequires:  perl(File::Spec) >= 0.80
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test::More) >= 0.47
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(CSS::Tiny) >= 1.10
Requires:       perl(Params::Util) => 0.05
Requires:       perl(PPI) >= 0.990

# Filter under specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(CSS::Tiny|Params::Util|PPI\\)$

%description
PPI::HTML converts Perl documents into syntax highlighted HTML pages.

%prep
%setup -q -n PPI-HTML-%{version}
# Remove bundled modules
rm -r inc/*
sed -i '/^\/inc\//d' MANIFEST

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes LICENSE README
%{_bindir}/*
%{perl_vendorlib}/PPI/
%{_mandir}/man3/*.3pm*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.08-3
- 为 Magic 3.0 重建

* Thu Oct 25 2012 Petr Pisar <ppisar@redhat.com> - 1.08-2
- Unbundle inc::Module::Install

* Thu Oct 25 2012 Petr Pisar <ppisar@redhat.com> - 1.08-1
- 1.08 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 19 2012 Petr Pisar <ppisar@redhat.com> - 1.07-12
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 29 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.07-10
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.07-8
- 661697 rebuild for fixing problems with vendorach/lib

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.07-7
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.07-6
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.07-3
- Rebuild for perl 5.10 (again)

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.07-2
- rebuild for new perl

* Sat May 13 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.07-1
- First build.
