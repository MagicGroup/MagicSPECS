Name:           perl-Config-Any
Summary:        Load configuration from different file formats, transparently
Version:        0.23
Release:        20%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/B/BR/BRICAS/Config-Any-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/Config-Any/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(Config::General)
BuildRequires:  perl(Config::Tiny)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires:  perl(JSON::XS)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Module::Pluggable) >= 3.01
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(version)
BuildRequires:  perl(XML::LibXML)
BuildRequires:  perl(XML::Simple)
BuildRequires:  perl(YAML::XS)

Requires:       perl(Config::General)
Requires:       perl(Config::Tiny)
Requires:       perl(JSON::XS)
Requires:       perl(Module::Pluggable) >= 3.01
Requires:       perl(XML::Simple)
Requires:       perl(YAML::XS)


%{?perl_default_filter}
#{?perl_default_subpackage_tests}

%description
Config::Any provides a facility for Perl applications and libraries to
load configuration data from multiple different file formats. It supports
XML, YAML, JSON, Apache-style configuration, Windows INI files, and even
Perl code.

%prep
%setup -q -n Config-Any-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

%check


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
# conf/ for examples of different config types
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.23-20
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.23-19
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.23-18
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.23-17
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.23-16
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.23-15
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.23-14
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.23-13
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.23-12
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.23-11
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.23-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.23-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.23-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.23-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.23-6
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.23-5
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.23-4
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.23-3
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.23-2
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Robin Lee <cheeselee@fedoraproject.org> - 0.23-1
- Update to 0.23
- BR: add perl(Test::Pod::Coverage)

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.20-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.20-2
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Aug 27 2010 Iain Arnell <iarnell@gmail.com> 0.20-1
- update to latest upstream

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.19-2
- Mass rebuild with perl-5.12.0

* Mon Mar 01 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.19-1
- update by Fedora::App::MaintainerTools 0.004
- PERL_INSTALL_ROOT => DESTDIR
- added a new br on perl(ExtUtils::MakeMaker) (version 6.42)
- dropped old BR on perl(JSON::Syck)
- added manual BR on perl(JSON::XS)
- added a new req on perl(Module::Pluggable) (version 3.01)
- dropped old requires on perl(JSON::Syck)
- added manual requires on perl(JSON::XS)

* Mon Jan 11 2010 Iain Arnell <iarnell@gmail.com> 0.18-1
- update to latest upstream version
- prefer YAML::XS over YAML::Syck

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.17-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 22 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.17-1
- update to 0.17

* Sat Dec 06 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.16-1
- update to 0.16

* Thu Sep 25 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.14-1
- update to 0.14
- add XML::LibXML to br's

* Wed May 21 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.12-1
- update to 0.12

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.08-2
- rebuild for new perl

* Tue Oct 23 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.08-1
- update to 0.08
- license tag update: GPL -> GPL+
- Module::Build -> Module::Install

* Fri May 04 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.07-4
- bump

* Fri May 04 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.07-3
- add entirety of t/ to %%doc

* Tue Apr 10 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.07-2
- Additional requires not documented added

* Tue Apr 10 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.07-1
- Specfile autogenerated by cpanspec 1.70.