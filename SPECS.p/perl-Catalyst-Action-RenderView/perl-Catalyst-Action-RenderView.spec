Name:           perl-Catalyst-Action-RenderView
Summary:        Sensible default end action for view rendering
Version:        0.16
Release:        25%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/B/BO/BOBTFISH/Catalyst-Action-RenderView-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/Catalyst-Action-RenderView/
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(Catalyst::Runtime) >= 5.80030
BuildRequires:  perl(CPAN)
BuildRequires:  perl(Data::Visitor) >= 0.24
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires:  perl(HTTP::Request::AsCGI)
BuildRequires:  perl(MRO::Compat)
BuildRequires:  perl(Test::More) >= 0.88

Requires:       perl(Catalyst::Action)
Requires:       perl(Catalyst::Runtime) >= 5.70
Requires:       perl(Data::Visitor) >= 0.24
Requires:       perl(MRO::Compat)

%{?perl_default_filter}
#{?perl_default_subpackage_tests}

%description
This action implements a sensible default end action, which will forward to
the first available view, unless status is set to 3xx, or there is a
response body. It also allows you to pass dump_info=1 to the url in order
to force a debug screen, while in debug mode.

%prep
%setup -q -n Catalyst-Action-RenderView-%{version}

# correct line encoding and an errant interperter setting
find t/ -type f -exec perl -pi -e 's|^#!perl|#!%{__perl}|; s/\r//' {} +

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} +
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

%check


%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.16-25
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.16-24
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.16-23
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.16-22
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.16-21
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.16-20
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.16-19
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.16-18
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.16-17
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.16-16
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.16-15
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.16-14
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.16-13
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.16-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.16-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.16-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.16-9
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.16-8
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.16-7
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.16-6
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.16-5
- 为 Magic 3.0 重建

* Sat Jan 28 2012 Liu Di <liudidi@gmail.com> - 0.16-4
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.16-2
- Perl mass rebuild

* Sun Mar 13 2011 Iain Arnell <iarnell@gmail.com> 0.16-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.14-3
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.14-2
- Mass rebuild with perl-5.12.0

* Sun Feb 21 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.14-1
- update by Fedora::App::MaintainerTools 0.003
- PERL_INSTALL_ROOT => DESTDIR
- dropped old BR on perl(Catalyst)
- dropped old BR on perl(Module::Build)
- dropped old BR on perl(Test::Pod)
- dropped old BR on perl(Test::Pod::Coverage)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.13-2
- rebuild against perl 5.10.1

* Sun Dec 06 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.13-1
- auto-update to 0.13 (by cpan-spec-update 0.01)

* Sat Aug 08 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.11-2
- drop req on Test::More; open RT#48537
- switch to more compact filtering (until we have perl_default_filter)
- auto-update to 0.11 (by cpan-spec-update 0.01)
- added a new br on CPAN (inc::Module::AutoInstall found)

* Sat Aug 08 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.11-1
- auto-update to 0.11 (by cpan-spec-update 0.01)
- added a new req on perl(Catalyst::Runtime) (version 5.70)
- added a new req on perl(Data::Visitor) (version 0.24)
- added a new req on perl(MRO::Compat) (version 0)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May 28 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.10-2
- add a br on CPAN (for now)

* Mon May 25 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.10-1
- auto-update to 0.10 (by cpan-spec-update 0.01)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)
- added a new br on perl(Catalyst::Runtime) (version 5.70)
- altered br on perl(Data::Visitor) (0.08 => 0.24)

* Mon Mar 09 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.09-1
- update to 0.09

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed May 21 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.08-1
- update to 0.08

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.07-2
- rebuild for new perl

* Sun Oct 21 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.07-1
- update to 0.07
- update license tag: GPL -> GPL+
- switch build invocations due to switchover to Module::Install

* Tue Jul 24 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.04-3
- bump

* Tue Jun 05 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.04-2
- add t/ to doc
- fix pod syntax (patch0)
- allow pod coverage test to be skipped independently of pod syntax test

* Fri Apr 27 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.04-1
- Specfile autogenerated by cpanspec 1.71.
