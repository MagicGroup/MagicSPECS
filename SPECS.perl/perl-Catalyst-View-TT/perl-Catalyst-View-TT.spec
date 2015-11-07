Name:           perl-Catalyst-View-TT
Summary:        Template Toolkit View Class
Version:	0.44
Release:	2%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/Catalyst-View-TT-%{version}.tar.gz
URL:            http://search.cpan.org/dist/Catalyst-View-TT/
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(Catalyst) >= 5.7
BuildRequires:  perl(Class::Accessor)
BuildRequires:  perl(CPAN)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires:  perl(MRO::Compat)
BuildRequires:  perl(Path::Class)
BuildRequires:  perl(Template)
BuildRequires:  perl(Template::Timer)
BuildRequires:  perl(Template::Provider::Encoding)
BuildRequires:  perl(Test::More)

Requires:       perl(Catalyst) >= 5.7
Requires:       perl(Class::Accessor)
Requires:       perl(MRO::Compat)
Requires:       perl(Path::Class)
Requires:       perl(Template)
Requires:       perl(Template::Timer)

# obsolete/provide old tests subpackage
# can be removed during F19 development cycle
Obsoletes:      %{name}-tests < 0.37-3
Provides:       %{name}-tests = %{version}-%{release}

%{?perl_default_filter}

%description
This is the Catalyst view base class for the Template Toolkit.

%prep
%setup -q -n Catalyst-View-TT-%{version}

find . -type f -exec chmod -x -c {} +

# silence rpmlint warnings
sed -i 's/\r//' t/lib/TestApp/Template/Any.pm

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} +
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*

%check


%files
%doc Changes README t/
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.44-2
- 更新到 0.44

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.43-1
- 更新到 0.43

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.37-17
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.37-16
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.37-15
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.37-14
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.37-13
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.37-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.37-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.37-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.37-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.37-8
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.37-7
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.37-6
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.37-5
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.37-4
- 为 Magic 3.0 重建

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> 0.37-3
- drop tests subpackage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 01 2011 Iain Arnell <iarnell@gmail.com> 0.37-1
- update to latest upstream version

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.36-2
- Perl mass rebuild

* Sun Mar 13 2011 Iain Arnell <iarnell@gmail.com> 0.36-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.34-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.34-2
- 661697 rebuild for fixing problems with vendorach/lib

* Sat Jul 17 2010 Iain Arnell <iarnell@gmail.com> 0.34-1
- update to latest upstream version
- BR perl(Template::Provider::Encoding)

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.32-2
- Mass rebuild with perl-5.12.0

* Sat Feb 20 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.32-1
- update by Fedora::App::MaintainerTools 0.003
- PERL_INSTALL_ROOT => DESTDIR
- dropped old BR on perl(Test::Pod)
- dropped old BR on perl(Test::Pod::Coverage)
- dropped old requires on perl(warnings)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.31-2
- rebuild against perl 5.10.1

* Sun Dec 06 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.31-1
- auto-update to 0.31 (by cpan-spec-update 0.01)

* Sat Sep 26 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.30-1
- update filtering
- auto-update to 0.30 (by cpan-spec-update 0.01)
- altered br on perl(Catalyst) (5.5 => 5.7)
- added a new br on perl(Class::Accessor) (version 0)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)
- added a new br on CPAN (inc::Module::AutoInstall found)
- altered req on perl(Catalyst) (0 => 5.7)
- added a new req on perl(Class::Accessor) (version 0)
- added a new req on perl(MRO::Compat) (version 0)
- added a new req on perl(Template) (version 0)
- added a new req on perl(Template::Timer) (version 0)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Feb 27 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.29-1
- update to 0.29

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed May 28 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.27-1
- update to 0.27

* Wed Mar 19 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.26-2
- bump

* Mon Mar 17 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.26-1
- Specfile autogenerated by cpanspec 1.74.
