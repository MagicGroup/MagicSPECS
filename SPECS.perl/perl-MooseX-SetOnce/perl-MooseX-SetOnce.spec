Name:           perl-MooseX-SetOnce
Version:	0.200002
Release:	3%{?dist}
Summary:        Write-once, read-many attributes for Moose
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/MooseX-SetOnce/
Source0:        http://www.cpan.org/authors/id/R/RJ/RJBS/MooseX-SetOnce-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.30
BuildRequires:  perl(Moose)
BuildRequires:  perl(Moose::Role) >= 0.90
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::Moose)
BuildRequires:  perl(Test::More)
Requires:       perl(Moose)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
The 'SetOnce' attribute lets your class have attributes that are not lazy
and not set, but that cannot be altered once set.

%prep
%setup -q -n MooseX-SetOnce-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes LICENSE README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.200002-3
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.200002-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.200002-1
- 更新到 0.200002

* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 0.200001-9
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.200001-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.200001-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Aug 02 2013 Petr Pisar <ppisar@redhat.com> - 0.200001-6
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.200001-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.200001-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.200001-3
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.200001-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 08 2011 Iain Arnell <iarnell@gmail.com> 0.200001-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.200000-2
- Perl mass rebuild

* Sat Apr 09 2011 Iain Arnell <iarnell@gmail.com> 0.200000-1
- update to latest upstream version

* Mon Feb 28 2011 Iain Arnell <iarnell@gmail.com> 0.100473-1
- update to latest upstream version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.100472-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov 19 2010 Iain Arnell <iarnell@gmail.com> 0.100472-1
- update to latest upstream version

* Mon Jun 07 2010 Iain Arnell 0.100471-1
- Specfile autogenerated by cpanspec 1.78.
