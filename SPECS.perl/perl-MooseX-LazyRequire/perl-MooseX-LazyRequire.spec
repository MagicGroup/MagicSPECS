Name:           perl-MooseX-LazyRequire
Version:	0.11
Release:	3%{?dist}
Summary:        Required attributes which fail only when trying to use them
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/MooseX-LazyRequire/
Source0:        http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/MooseX-LazyRequire-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(aliased) >= 0.30
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Moose)
BuildRequires:  perl(Moose::Exporter)
BuildRequires:  perl(Moose::Role)
BuildRequires:  perl(namespace::autoclean)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(warnings)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
This module adds a lazy_required option to Moose attribute declarations.

%prep
%setup -q -n MooseX-LazyRequire-%{version}

# we don't have Test::CheckDeps in Fedora yet
rm -f t/00-check-deps.t

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \;

%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc Changes LICENSE README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.11-3
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.11-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.11-1
- 更新到 0.11

* Fri Jun 20 2014 Liu Di <liudidi@gmail.com> - 0.09-5
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 0.09-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jan 05 2013 Iain Arnell <iarnell@gmail.com> 0.09-1
- update to latest upstream version

* Sat Jul 21 2012 Iain Arnell <iarnell@gmail.com> 0.08-1
- update to latest upstream version

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.07-4
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.07-2
- Perl mass rebuild

* Sat Apr 09 2011 Iain Arnell <iarnell@gmail.com> 0.07-1
- update to latest upstream version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.06-2
- 661697 rebuild for fixing problems with vendorach/lib

* Sun Jul 25 2010 Iain Arnell <iarnell@gmail.com> 0.06-1
- update to latest upstream
- update spec for modern rpmbuild

* Mon Jun 07 2010 Iain Arnell 0.05-1
- Specfile autogenerated by cpanspec 1.78.
