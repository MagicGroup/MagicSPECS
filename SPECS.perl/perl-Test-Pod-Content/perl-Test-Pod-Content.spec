Name:           perl-Test-Pod-Content
Version:	0.0.6
Release:	14%{?dist}
Summary:        Test a Pod's content
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Test-Pod-Content/
Source0:        http://search.cpan.org/CPAN/authors/id/M/MK/MKUTTER/Test-Pod-Content-v%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Pod::Simple)
BuildRequires:  perl(Test::Kwalitee)
BuildRequires:  perl(Test::Perl::Critic)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(version)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
This is a very simple module for testing a Pod's content. It is mainly intended
for testing the content of generated Pod - that is, the Pod included in perl
modules generated by some mechanism. Another usage example is to test whether
all files contain the same copyright notice.

%prep
%setup -q -n Test-Pod-Content-v%{version}

%build
%{__perl} Build.PL installdirs=vendor
./Build

%install
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
RELEASE_TESTING=1 ./Build test

%files
%doc Changes HACKING README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.0.6-14
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.0.6-13
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.0.6-11
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.0.6-10
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.0.6-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.0.6-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.0.6-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.0.6-6
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.0.6-5
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 23 2012 Petr Pisar <ppisar@redhat.com> - 0.0.6-3
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 26 2011 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> 0.0.6-1
- Update to 0.0.6
- Add perl default filter
- Add BuildRequires for the tests

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.0.5-3
- Perl mass rebuild

* Thu Jun 09 2011 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> 0.0.5-2
- Enable all tests.

* Mon May 16 2011 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> 0.0.5-1
- Specfile autogenerated by cpanspec 1.78.
