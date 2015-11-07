Name:           perl-CGI-Emulate-PSGI
Version:	0.21
Release:	2%{?dist}
Summary:        PSGI adapter for CGI applications
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/CGI-Emulate-PSGI
Source0:        http://www.cpan.org/authors/id/M/MI/MIYAGAWA/CGI-Emulate-PSGI-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  perl(CGI)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires:  perl(HTTP::Response)
BuildRequires:  perl(Test::Builder::Module)
BuildRequires:  perl(Plack::Test)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
This module allows an application designed for the CGI environment to run
in a PSGI environment, and thus on any of the backends that PSGI supports.

%prep
%setup -q -n CGI-Emulate-PSGI-%{version}

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
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.21-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.21-1
- 更新到 0.21

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.14-15
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.14-14
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.14-13
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.14-12
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.14-11
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.14-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.14-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.14-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.14-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.14-6
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.14-5
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.14-4
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.14-3
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 26 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.14-1
- Upstream update.

* Mon Sep 19 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.13-1
- Upstream update.

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.12-2
- Perl mass rebuild

* Mon Jun 20 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.12-1
- Upstream update.
- Remove BuildRoot.

* Thu Mar 03 2011 Ralf Corsépius <corsepiu@fedoraproject.org> 0.11-1
- Upstream update.
- Spec cleanup.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 29 2010 Ralf Corsépius <corsepiu@fedoraproject.org> 0.10-1
- Merge-in *.spec from BZ 664815.
- Update to 0.10.
- Remove *-tests subpackage.

* Sat Mar 20 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.06-1
- specfile by Fedora::App::MaintainerTools 0.006
