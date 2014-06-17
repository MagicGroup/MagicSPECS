Name:           perl-Catalyst-Controller-FormBuilder
Version:        0.06
Release:        19%{?dist}
Summary:        Catalyst FormBuilder Base Controller
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Catalyst-Controller-FormBuilder/
Source0:        http://search.cpan.org/CPAN/authors/id/M/MS/MSTROUT/Catalyst-Controller-FormBuilder-%{version}.tar.gz
BuildArch:      noarch
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

BuildRequires:  perl(CGI::FormBuilder) >= 3.02
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::WWW::Mechanize::Catalyst) >= 0.37
BuildRequires:  perl(Tie::IxHash) >= 1.21

# not auto-picked up, or to keep rpmlint happy...
Requires:       perl(Catalyst)
Requires:       perl(warnings)
Requires:       perl(lib)

### auto-added brs!
BuildRequires:  perl(Class::Inspector) >= 1.13
BuildRequires:  perl(Catalyst::Runtime) >= 5.7
BuildRequires:  perl(Scalar::Util) >= 1.19
BuildRequires:  perl(Class::Data::Inheritable) >= 0.04
BuildRequires:  perl(MRO::Compat) >= 0.09

%description
This base controller merges the functionality of CGI::FormBuilder with
Catalyst and the following templating systems: Template Toolkit, Mason and
HTML::Template. This gives you access to all of FormBuilder's niceties,
such as controllablefield stickiness, multilingual support, and Javascript
generation. For more details, see CGI::FormBuilder or the website at:
http://www.formbuilder.org


%{?filter_setup:
%filter_from_requires /perl(FindBin)/d; /perl(Test::.*)/d
%filter_from_provides /perl(TestApp.*)/d
%{?perl_default_filter}
}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\((FindBin|Test::.*)\\)
%global __provides_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(TestApp.*\\)

%prep
%setup -q -n Catalyst-Controller-FormBuilder-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} +
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*

%check


%files
%defattr(-,root,root,-)
%doc Changes t/
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.06-19
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.06-18
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.06-17
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.06-16
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.06-15
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.06-14
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.06-13
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.06-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.06-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.06-10
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.06-9
- 为 Magic 3.0 重建

* Mon Dec 10 2012 Liu Di <liudidi@gmail.com> - 0.06-8
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.06-7
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.06-6
- 为 Magic 3.0 重建

* Sat Jan 28 2012 Liu Di <liudidi@gmail.com> - 0.06-5
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Iain Arnell <iarnell@gmail.com> 0.06-3
- update filtering macros for rpm 4.9

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.06-2
- Perl mass rebuild

* Fri Mar 18 2011 Iain Arnell <iarnell@gmail.com> 0.06-1
- update to latest upstream version

* Thu Mar 17 2011 Iain Arnell <iarnell@gmail.com> 0.05-9
- don't filter perl(Catalyst::View::HTML::Template) from requires
- drop obsolete no_scalar_util_0_19.patch
- clean up spec for modern rpmbuild

* Wed Feb 16 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.05-8
- fix filter for RPM4.9

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.05-6
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.05-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.05-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 30 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.05-2
- add br on CPAN

* Fri May 29 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.05-1
- auto-update to 0.05 (by cpan-spec-update 0.01)
- altered br on perl(Test::WWW::Mechanize::Catalyst) (0 => 0.37)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)
- added a new br on perl(Class::Inspector) (version 1.13)
- added a new br on perl(Catalyst::Runtime) (version 5.7)
- altered br on perl(Tie::IxHash) (0 => 1.21)
- added a new br on perl(Scalar::Util) (version 1.19)
- added a new br on perl(Class::Data::Inheritable) (version 0.04)
- altered br on perl(CGI::FormBuilder) (0 => 3.02)
- added a new br on perl(MRO::Compat) (version 0.09)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Mar 19 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.04-2
- bump

* Mon Mar 17 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.04-1
- Specfile autogenerated by cpanspec 1.74.
