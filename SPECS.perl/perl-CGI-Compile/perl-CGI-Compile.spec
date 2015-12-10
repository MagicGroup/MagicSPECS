Name:           perl-CGI-Compile
Summary:        Compile .cgi scripts to a code reference like ModPerl::Registry
Version:	0.20
Release:	3%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/M/MI/MIYAGAWA/CGI-Compile-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/CGI-Compile
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(CGI)
BuildRequires:  perl(CGI::Emulate::PSGI)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires:  perl(File::pushd)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::NoWarnings)
BuildRequires:  perl(Test::Requires)

# obsolete/provide tests subpackage
# can be removed during F19 development cycle
Obsoletes:      %{name}-tests < 0.15-3
Provides:       %{name}-tests = %{version}-%{release}

%{?perl_default_filter}

%description
CGI::Compile is an utility to compile CGI scripts into a code reference
that can run many times on its own namespace, as long as the script is
ready to run on a persistent environment.

%prep
%setup -q -n CGI-Compile-%{version}
sed -i 's/\r//' t/data_crlf.cgi t/end_crlf.cgi
sed -i -e '1s,#!.*perl,#!%{__perl},' t/*.t


%build
%{__perl} Build.PL --installdirs vendor
./Build

%install
./Build install --destdir $RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'

%{_fixperms} %{buildroot}/*

%check
./Build test


%files
%doc Changes README t/
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.20-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.20-2
- 更新到 0.20

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.19-1
- 更新到 0.19

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.15-17
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.15-16
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.15-15
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.15-14
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.15-13
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.15-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.15-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.15-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.15-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.15-8
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.15-7
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.15-6
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.15-5
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.15-4
- 为 Magic 3.0 重建

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> 0.15-3
- drop tests subpackage; move tests to main package documentation

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 02 2011 Iain Arnell <iarnell@gmail.com> 0.15-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Fri Jun 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.11-5
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 08 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.11-3
- Add BR: perl(CGI) (Fix FTBFS: BZ 660891).

* Tue Jun 22 2010 Petr Pisar <ppisar@redhat.com> - 0.11-2
- Rebuild against perl-5.12

* Sat Mar 20 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.11-1
- specfile by Fedora::App::MaintainerTools 0.006


