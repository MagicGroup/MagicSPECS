Name:           perl-Log-Any
Version:	1.032
Release:	4%{?dist}
Summary:        Bringing loggers and listeners together
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Log-Any/
Source0:        http://search.cpan.org/CPAN/authors/id/D/DA/DAGOLDEN/Log-Any-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::Simple)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# Log::Any::Adapter* merged into Log::Any in 1.00
Obsoletes:      perl-Log-Any-Adapter < 0.11-7
Provides:       perl-Log-Any-Adapter = %{version}-%{release}%{?dist}

%{?perl_default_filter:
%filter_from_provides /perl(Log::Any::Adapter)\s*$/d
%perl_default_filter}
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}perl\\(Log::Any::Adapter\\)


%description
Log::Any allows CPAN modules to safely and efficiently log messages, while
letting the application choose (or decline to choose) a logging mechanism
such as Log::Dispatch or Log::Log4perl.

%prep
%setup -q -n Log-Any-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor --skipdeps
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.032-4
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.032-3
- 为 Magic 3.0 重建

* Thu Sep 17 2015 Liu Di <liudidi@gmail.com> - 1.032-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.032-1
- 更新到 1.032

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.11-9
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.11-8
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.11-7
- 为 Magic 3.0 重建

* Wed Jul 20 2011 Iain Arnell <iarnell@gmail.com> 0.11-6
- add __provides_exclude macro for rpm 4.9

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.11-5
- Perl mass rebuild

* Thu Jun 09 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.11-4
- Perl 5.14 mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Feb 06 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.11-2
- Add %%perl_default_filter.
- Filter out bogus Provides: perl(Log::Any::Adapter).

* Sat Feb 13 2010 Steven Pritchard <steve@kspei.com> 0.11-1
- Specfile autogenerated by cpanspec 1.79.
- Add --skipdeps to Makefile.PL to avoid attempting to download dependencies.
