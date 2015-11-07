Name:           perl-constant-boolean
Version:        0.02
Release:        19%{?dist}
Summary:        Define TRUE and FALSE constants
Summary(zh_CN.UTF-8): 定义 TRUE 和 FALSE 常量
License:        GPL+ or Artistic
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
URL:            http://search.cpan.org/dist/constant-boolean/
Source0:        http://www.cpan.org/authors/id/D/DE/DEXTER/constant-boolean-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Symbol::Util)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
Defines TRUE and FALSE constants in caller's namespace. You could use
simple values like empty string or zero for false, or any non-empty and non-
zero string value as true, but the TRUE and FALSE constants are more
descriptive.

%description -l zh_CN.UTF-8
定义 TRUE 和 FALSE 常量。

%prep
%setup -q -n constant-boolean-%{version}

%build
%{__perl} Build.PL installdirs=vendor
./Build

%install
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*
magic_rpm_clean.sh

%check
./Build test

%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.02-19
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.02-18
- 为 Magic 3.0 重建

* Fri May 08 2015 Liu Di <liudidi@gmail.com> - 0.02-17
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.02-16
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.02-15
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.02-14
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.02-13
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.02-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.02-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.02-10
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.02-9
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.02-7
- Perl 5.16 rebuild

* Sun Mar 11 2012 Emmanuel Seyman <emmanuel.seyman@club-internet.fr - 0.02-6
- Add perl default filter
- Clean up spec file

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.02-4
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.02-2
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 0.02-1
- Update to 0.02.

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.01-6
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.01-5
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.01-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.01-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 01 2009 Allisson Azevedo <allisson@gmail.com> 0.01-2
- Rebuild.

* Thu Jan 29 2009 Allisson Azevedo <allisson@gmail.com> 0.01-1
- Initial rpm release.
