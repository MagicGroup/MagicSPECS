Name:           perl-HTTP-Request-AsCGI
Summary:        Setup a CGI enviroment from a HTTP::Request
Version:        1.2
Release:        26%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/F/FL/FLORA/HTTP-Request-AsCGI-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/HTTP-Request-AsCGI/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(Carp)
BuildRequires:  perl(Class::Accessor)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(HTTP::Request)
BuildRequires:  perl(HTTP::Response) >= 1.53
BuildRequires:  perl(IO::File)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(URI::Escape)

Requires:       perl(Carp)
Requires:       perl(Class::Accessor)
Requires:       perl(HTTP::Request)
Requires:       perl(HTTP::Response) >= 1.53
Requires:       perl(IO::File)
Requires:       perl(URI::Escape)


%{?perl_default_filter}
#{?perl_default_subpackage_tests}

%description
Provides a convenient way of setting up an CGI environment from a
HTTP::Request.

%prep
%setup -q -n HTTP-Request-AsCGI-%{version}

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


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes README examples/
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.2-26
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.2-25
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.2-24
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.2-23
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.2-22
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.2-21
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.2-20
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.2-19
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.2-18
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.2-17
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.2-16
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.2-15
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.2-14
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.2-13
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.2-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.2-11
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.2-10
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.2-9
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.2-7
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.2-5
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.2-4
- Mass rebuild with perl-5.12.0

* Sun Mar 07 2010 Chris Weyl <cweyl@alumni.drew.edu> 1.2-3
- update by Fedora::App::MaintainerTools 0.004
- PERL_INSTALL_ROOT => DESTDIR
- dropped old requires on perl(Class::Accessor::Fast)

* Fri Feb 05 2010 Chris Weyl <cweyl@alumni.drew.edu> 1.2-2
- drop errant req on Test::More

* Fri Feb 05 2010 Chris Weyl <cweyl@alumni.drew.edu> 1.2-1
- add perl_default_filter
- auto-update to 1.2 (by cpan-spec-update 0.01)
- added a new req on perl(Carp) (version 0)
- added a new req on perl(Class::Accessor) (version 0)
- added a new req on perl(HTTP::Request) (version 0)
- added a new req on perl(HTTP::Response) (version 1.53)
- added a new req on perl(IO::File) (version 0)
- added a new req on perl(Test::More) (version 0)
- added a new req on perl(URI::Escape) (version 0)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.9-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue May 19 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.9-1
- auto-update to 0.9 (by cpan-spec-update 0.01)
- added a new br on perl(IO::File) (version 0)
- added a new br on perl(URI::Escape) (version 0)
- added a new br on perl(Carp) (version 0)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.5-3
- rebuild for new perl

* Fri Apr 27 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.5-2
- bump

* Tue Apr 10 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.5-1
- Specfile autogenerated by cpanspec 1.70.
