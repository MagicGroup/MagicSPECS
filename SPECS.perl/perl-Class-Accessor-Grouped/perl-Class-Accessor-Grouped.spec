Name:           perl-Class-Accessor-Grouped
Version:	0.10012
Release:	2%{?dist}
Summary:        Build groups of accessors
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Class-Accessor-Grouped/
Source0:        http://search.cpan.org/CPAN/authors/id/R/RI/RIBASUSHI/Class-Accessor-Grouped-%{version}.tar.gz
BuildArch:      noarch
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.62
BuildRequires:  perl(Carp)
BuildRequires:  perl(Class::XSAccessor) >= 1.13
BuildRequires:  perl(Devel::Hide)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Class::Inspector)
BuildRequires:  perl(Sub::Name) >= 0.05
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Exception) >= 0.31
BuildRequires:  perl(CPAN)

Requires:       perl(Class::XSAccessor) >= 1.13
Requires:       perl(Class::Inspector)
Requires:       perl(Sub::Name) >= 0.05

# obsolete/provide old tests subpackage
# can be removed during F19 development cycle
Obsoletes:      %{name}-tests < 0.10006-3
Provides:       %{name}-tests = %{version}-%{release}

%{?perl_default_filter}

%description
This class lets you build groups of accessors that will call different
getters and setters.

%prep
%setup -q -n Class-Accessor-Grouped-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*

%check


%files
%doc Changes README t/
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Mon Sep 14 2015 Liu Di <liudidi@gmail.com> - 0.10012-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.10012-1
- 更新到 0.10012

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.10006-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.10006-7
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.10006-6
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.10006-5
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.10006-4
- 为 Magic 3.0 重建

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> 0.10006-3
- drop tests subpackage; move tests to main package documentation

* Tue Jan 17 2012 Iain Arnell <iarnell@gmail.com> - 0.10006-2
- rebuilt again for F17 mass rebuild

* Fri Jan 13 2012 Iain Arnell <iarnell@gmail.com> 0.10006-1
- update to latest upstream version

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10002-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 28 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.10002-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10002-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 08 2011 Iain Arnell <iarnell@gmail.com> 0.10002-1
- update to latest upstream version
- update R/BR perl(Sub::Name) >= 0.05
- update BR perl(Test::Exception) >= 0.31
- new BR perl(Devel::Hide)

* Wed Nov 03 2010 Iain Arnell <iarnell@gmail.com> 0.09008-1
- update to latest upstream version
- clean up spec for modern rpmbuild
- new BR perl(Test::Exception)
- new BR perl(Class::XSAccessor)
- remove BR perl(Sub::Identify)
- new req perl(Class::XSAccessor)
- remove explicit req perl(Carp)
- remove explicit req perl(MRO::Compat)
- remove explicit req perl(Scalar::Util)

* Thu Sep 02 2010 Iain Arnell <iarnell@gmail.com> 0.09005-1
- update to latest upstream version

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.09002-2
- Mass rebuild with perl-5.12.0

* Sun Feb 07 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.09002-1
- subpackage tests, drop t/ from doc
- update filtering (perl_default_filter)
- PERL_INSTALL_ROOT => DESTDIR in make install
- auto-update to 0.09002 (by cpan-spec-update 0.01)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.09000-2
- rebuild against perl 5.10.1

* Tue Aug 25 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.09000-1
- auto-update to 0.09000 (by cpan-spec-update 0.01)
- added a new br on perl(Carp) (version 0)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)
- added a new br on perl(Scalar::Util) (version 0)
- added a new br on perl(Sub::Identify) (version 0)
- added a new br on perl(Sub::Name) (version 0.04)
- added a new br on CPAN (inc::Module::AutoInstall found)
- added a new req on perl(Carp) (version 0)
- added a new req on perl(Class::Inspector) (version 0)
- added a new req on perl(MRO::Compat) (version 0)
- added a new req on perl(Scalar::Util) (version 0)
- added a new req on perl(Sub::Name) (version 0.04)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08003-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 02 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.08003-1
- update to 0.08003

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08002-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 02 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.08002-1
- update to 0.08002

* Wed May 21 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.08001-1
- update to 0.08001

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.07000-4
Rebuild for new perl

* Wed Mar 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.07000-3
- rebuild for new perl

* Sat Dec 08 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.07000-2
- bump

* Tue Sep 18 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.07000-1
- Specfile autogenerated by cpanspec 1.71.
