Name:           perl-Catalyst-Plugin-Session-State-Cookie
Summary:        Maintain session IDs using cookies
Version:        0.17
Release:        29%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/M/MS/MSTROUT/Catalyst-Plugin-Session-State-Cookie-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/Catalyst-Plugin-Session-State-Cookie/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(Catalyst) >= 5.80005
BuildRequires:  perl(Catalyst::Plugin::Session) >= 0.27
BuildRequires:  perl(CPAN)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires:  perl(Moose)
BuildRequires:  perl(MRO::Compat)
BuildRequires:  perl(namespace::autoclean)
BuildRequires:  perl(Test::MockObject) >= 1.01
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::WWW::Mechanize::Catalyst)

Requires:       perl(Catalyst) >= 5.80005
Requires:       perl(Catalyst::Plugin::Session) >= 0.27
Requires:       perl(Moose)
Requires:       perl(MRO::Compat)
Requires:       perl(namespace::autoclean)


%{?perl_default_filter}
#{?perl_default_subpackage_tests}

%description
In order for Catalyst::Plugin::Session to work the session ID needs to
be stored on the client, and the session data needs to be stored on
the server.  This plugin provides a way to store the session ID on the
client, through a cookie.

%prep
%setup -q -n Catalyst-Plugin-Session-State-Cookie-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make pure_install DESTDIR=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*

%check
TEST_POD=1 

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes README t/
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.17-29
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.17-28
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.17-27
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.17-26
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.17-25
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.17-24
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.17-23
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.17-22
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.17-21
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.17-20
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.17-19
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.17-18
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.17-17
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.17-16
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.17-15
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.17-14
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.17-13
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.17-12
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.17-11
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.17-10
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.17-9
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.17-7
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.17-5
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.17-4
- Mass rebuild with perl-5.12.0

* Sat Feb 27 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.17-3
- update by Fedora::App::MaintainerTools 0.004
- PERL_INSTALL_ROOT => DESTDIR
- dropped old BR on perl(Test::Pod::Coverage)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.17-2
- rebuild against perl 5.10.1

* Sun Dec 06 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.17-1
- auto-update to 0.17 (by cpan-spec-update 0.01)
- altered br on perl(Catalyst::Plugin::Session) (0.19 => 0.27)
- altered req on perl(Catalyst::Plugin::Session) (0.19 => 0.27)

* Sun Aug 23 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.14-1
- switch req/prov filtering systems...
- auto-update to 0.14 (by cpan-spec-update 0.01)
- added a new br on perl(Moose) (version 0)
- added a new br on perl(namespace::autoclean) (version 0)
- added a new req on perl(Moose) (version 0)
- added a new req on perl(namespace::autoclean) (version 0)

* Sat Aug 08 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.12-1
- auto-update to 0.12 (by cpan-spec-update 0.01)
- altered br on perl(Catalyst) (5.7010 => 5.80005)
- added a new req on perl(Catalyst) (version 5.80005)
- added a new req on perl(MRO::Compat) (version 0)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 29 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.11-2
- add br on CPAN

* Fri May 29 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.11-1
- auto-update to 0.11 (by cpan-spec-update 0.01)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)
- added a new br on perl(Catalyst) (version 5.7010)
- altered br on perl(Test::MockObject) (0 => 1.01)

* Mon Mar 09 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.10-1
- update to 0.10

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jun 01 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.09-2
- bump

* Thu May 29 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.09-1
- Specfile autogenerated by cpanspec 1.74.
