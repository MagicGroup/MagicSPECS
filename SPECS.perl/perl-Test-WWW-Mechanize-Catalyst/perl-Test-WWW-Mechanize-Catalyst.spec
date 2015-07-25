Name:           perl-Test-WWW-Mechanize-Catalyst
Summary:        Test::WWW::Mechanize for Catalyst
Summary(zh_CN.UTF-8): Catalyst 的 Test::WWW::Mechanize 模块
Version:        0.60
Release:        2%{?dist}
License:        GPL+ or Artistic

Source0:        http://search.cpan.org/CPAN/authors/id/I/IL/ILMARI/Test-WWW-Mechanize-Catalyst-%{version}.tar.gz
URL:            http://search.cpan.org/dist/Test-WWW-Mechanize-Catalyst/
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(Catalyst) >= 5.00
# Catalyst::Plugin::Session::State::Cookie and Test::WWW::Mechanize::Catalyst
# use each other in their test suites
%if !0%{?perl_bootstrap}
BuildRequires:  perl(Catalyst::Plugin::Session::State::Cookie)
%endif
BuildRequires:  perl(Catalyst::Plugin::Session::Store::Dummy)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires:  perl(LWP) >= 5.816
BuildRequires:  perl(Moose) >= 0.67
BuildRequires:  perl(namespace::clean) >= 0.09
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::utf8)
BuildRequires:  perl(Test::WWW::Mechanize) >= 1.14
BuildRequires:  perl(WWW::Mechanize) >= 1.54

Requires:       perl(Catalyst) >= 5.00
Requires:       perl(LWP) >= 5.816
Requires:       perl(Moose) >= 0.67
Requires:       perl(namespace::clean) >= 0.09
Requires:       perl(Test::WWW::Mechanize) >= 1.14
Requires:       perl(WWW::Mechanize) >= 1.54

# obsolete/provide old tests subpackage
# can be removed during F19 development cycle
Obsoletes:      %{name}-tests < 0.56-3
Provides:       %{name}-tests = %{version}-%{release}

%{?perl_default_filter}

%description
Catalyst is an elegant MVC Web Application Framework. Test::WWW::Mechanize
is a subclass of WWW::Mechanize that incorporates features for web
application testing. The Test::WWW::Mechanize::Catalyst module meshes the
two to allow easy testing of Catalyst applications without starting up a
web server.

%description -l zh_CN.UTF-8
Catalyst 的 Test::WWW::Mechanize 模块。

%prep
%setup -q -n Test-WWW-Mechanize-Catalyst-%{version}

# silence rpmlint warning
sed -i '1s,#!.*perl,#!%{__perl},' t/*.t

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} +
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*
magic_rpm_clean.sh

%check
make test

%files
%doc CHANGES README t/
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri Jun 05 2015 Liu Di <liudidi@gmail.com> - 0.60-2
- 为 Magic 3.0 重建

* Mon Dec 29 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 0.60-1
- Update to 0.60

* Thu Nov 13 2014 Emmanuel Seyman <emmanuel@seyman.fr> - 0.59-1
- Update to 0.59

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.58-8
- Perl 5.20 re-rebuild of bootstrapped packages

* Tue Sep 02 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.58-7
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.58-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug 14 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.58-5
- Perl 5.18 re-rebuild of bootstrapped packages

* Tue Aug 06 2013 Petr Pisar <ppisar@redhat.com> - 0.58-4
- Perl 5.18 rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.58-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.58-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Iain Arnell <iarnell@gmail.com> 0.58-1
- update to latest upstream version

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.57-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 0.57-3
- Perl 5.16 re-rebuild of bootstrapped packages

* Mon Jul 02 2012 Petr Pisar <ppisar@redhat.com> - 0.57-2
- Perl 5.16 rebuild

* Thu Apr 05 2012 Iain Arnell <iarnell@gmail.com> 0.57-1
- update to latest upstream version
- avoid circular build dependencies (patch from Paul Howarth rhbz#810721)

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> 0.56-3
- drop tests subpackage; move tests to main package documentation

* Tue Jan 17 2012 Iain Arnell <iarnell@gmail.com> - 0.56-2
- rebuilt again for F17 mass rebuild

* Sat Jan 14 2012 Iain Arnell <iarnell@gmail.com> 0.56-1
- update to latest upstream version

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.55-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 02 2011 Iain Arnell <iarnell@gmail.com> 0.55-1
- update to latest upstream version

* Mon Aug 29 2011 Iain Arnell <iarnell@epo.org> 0.54-1
- update to latest upstream version

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.53-3
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.53-2
- Perl mass rebuild

* Fri Mar 18 2011 Iain Arnell <iarnell@gmail.com> 0.53-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.52-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.52-3
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.52-2
- Mass rebuild with perl-5.12.0

* Fri Apr 16 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.52-1
- update by Fedora::App::MaintainerTools 0.006
- PERL_INSTALL_ROOT => DESTDIR
- updating to latest GA CPAN version (0.52)
- added a new br on perl(Catalyst::Plugin::Session::Store::Dummy) (version 0)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)
- added a new br on perl(LWP) (version 5.816)
- altered br on perl(Moose) (0 => 0.67)
- added a new br on perl(Test::More) (version 0)
- altered br on perl(WWW::Mechanize) (1.30 => 1.54)
- altered br on perl(namespace::clean) (0 => 0.09)
- dropped old BR on perl(Test::Pod::Coverage)
- added a new req on perl(LWP) (version 5.816)
- added a new req on perl(Moose) (version 0.67)
- added a new req on perl(Test::WWW::Mechanize) (version 1.14)
- added a new req on perl(WWW::Mechanize) (version 1.54)
- added a new req on perl(namespace::clean) (version 0.09)

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.51-3
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.51-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 09 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.51-1
- update to 0.51

* Sun Mar 22 2009 Robert Scheck <robert@fedoraproject.org> 0.50-2
- Buildrequire perl(Catalyst::Plugin::Session::State::Cookie)

* Mon Mar 09 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.50-1
- update to 0.50

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.43-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Oct 26 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.43-1
- update to 0.43

* Tue Jul 01 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.42-1
- update to 0.42

* Tue Mar 18 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.41-2
- bump

* Mon Mar 17 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.41-1
- Specfile autogenerated by cpanspec 1.74.
