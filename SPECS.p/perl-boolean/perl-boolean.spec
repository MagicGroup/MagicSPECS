Name:           perl-boolean
Version:        0.28
Release:        6%{?dist}
Summary:        Boolean support for Perl
Summary(zh_CN.UTF-8): Perl 的布尔值支持
License:        GPL+ or Artistic
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
URL:            http://search.cpan.org/dist/boolean/
Source0:        http://www.cpan.org/authors/id/I/IN/INGY/boolean-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl >= 0:5.005003
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Readonly)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(Readonly)

%description
Most programming languages have a native Boolean data type. Perl does not.

%description -l zh_CN.UTF-8
Perl 的布尔值支持。

%prep
%setup -q -n boolean-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*
magic_rpm_clean.sh

%check


%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.28-6
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.28-5
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.28-4
- 为 Magic 3.0 重建

* Sat Jan 28 2012 Liu Di <liudidi@gmail.com> - 0.28-3
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 22 2011 Iain Arnell <iarnell@gmail.com> 0.28-1
- update to latest upstream version

* Wed Jun 29 2011 Iain Arnell <iarnell@gmail.com> 0.27-1
- update to latest upstream version
- remove buildroot and defattr from spec file

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.26-3
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 22 2011 Iain Arnell <iarnell@gmail.com> 0.26-1
- update to latest upstream version

* Sun Jan 16 2011 Iain Arnell <iarnell@gmail.com> 0.25-1
- update to latest upstream version
- add new R/BR perl(Readonly)
- add new R perl(Exporter)

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.23-2
- 661697 rebuild for fixing problems with vendorach/lib

* Wed Sep 22 2010 Iain Arnell <iarnell@gmail.com> 0.23-1
- update to latest upstream version

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.20-6
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.20-5
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 19 2008 Iain Arnell <iarnell@gmail.com> 0.20-2
- BR Test::More

* Tue Nov 18 2008 Iain Arnell <iarnell@gmail.com> 0.20-1
- Specfile autogenerated by cpanspec 1.77.
