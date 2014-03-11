Name:           perl-Catalyst-Plugin-Static-Simple
Version:        0.29
Release:        9%{?dist}
Summary:        Make serving static pages painless
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Catalyst-Plugin-Static-Simple/
Source0:        http://search.cpan.org/CPAN/authors/id/M/MS/MSTROUT/Catalyst-Plugin-Static-Simple-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Catalyst) >= 5.30
BuildRequires:  perl(HTTP::Request::AsCGI)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(MIME::Types) >= 1.25
BuildRequires:  perl(Catalyst::Plugin::SubRequest)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(CPAN)
BuildRequires:  perl(MRO::Compat)
BuildRequires:  perl(Catalyst::Runtime) >= 5.80008
BuildRequires:  perl(Moose)
BuildRequires:  perl(MooseX::Types)
BuildRequires:  perl(namespace::autoclean)

Requires:       perl(Catalyst) >= 5.30
Requires:       perl(Catalyst::Runtime) >= 5.80008
Requires:       perl(MIME::Types) >= 1.25
Requires:       perl(MRO::Compat)
Requires:       perl(Moose)
Requires:       perl(MooseX::Types)
Requires:       perl(namespace::autoclean)

%{?perl_default_filter}
%{?perl_default_subpackage_tests}

%description
The Static::Simple plugin is designed to make serving static content in
your application during development quick and easy, without requiring a
single line of code from you.

%prep
%setup -q -n Catalyst-Plugin-Static-Simple-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} +
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

%check
TEST_POD=1 

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.29-9
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.29-8
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.29-7
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.29-5
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.29-3
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.29-2
- Mass rebuild with perl-5.12.0

* Sun Feb 07 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.29-1
- add perl_default_filter
- add perl_default_subpackage_tests, drop t/ from doc
- PERL_INSTALL_ROOT => DESTDIR
- auto-update to 0.29 (by cpan-spec-update 0.01)
- added a new br on perl(Moose) (version 0)
- added a new br on perl(MooseX::Types) (version 0)
- added a new br on perl(namespace::autoclean) (version 0)
- added a new req on perl(Moose) (version 0)
- added a new req on perl(MooseX::Types) (version 0)
- added a new req on perl(namespace::autoclean) (version 0)

* Sun Aug 23 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.22-1
- switch to new filtering system
- auto-update to 0.22 (by cpan-spec-update 0.01)
- altered br on perl(Catalyst::Runtime) (5.30 => 5.80008)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)
- added a new br on CPAN (inc::Module::Install::AutoInstall found)
- added a new req on perl(Catalyst::Runtime) (version 5.80008)
- added a new req on perl(MIME::Types) (version 1.25)
- added a new req on perl(MRO::Compat) (version 0)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 25 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.21-1
- auto-update to 0.21 (by cpan-spec-update 0.01)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.50)
- added a new br on perl(MRO::Compat) (version 0)
- added a new br on perl(Catalyst::Runtime) (version 5.30)
- altered br on perl(MIME::Types) (1.15 => 1.25)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Mar 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.20-2
- rebuild for new perl

* Sat Mar 01 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.20-1
- update to 0.20

* Thu Aug 09 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.19-1
- update to 0.19

* Fri Jun 08 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.17-1
- update to 0.17
- switch build/install incantations; module switched to Module::Install

* Tue Jun 05 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.15-3
- bump

* Tue Jun 05 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.15-2
- add perl(HTTP::Request::AsCGI) as br
- include all of t/, not just t/lib/TestApp/

* Fri Apr 27 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.15-1
- Specfile autogenerated by cpanspec 1.71.
