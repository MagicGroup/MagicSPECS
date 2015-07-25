Name:           perl-Getopt-Long-Descriptive
Summary:        Getopt::Long with usage text
Version:        0.093
Release:        2%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/R/RJ/RJBS/Getopt-Long-Descriptive-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/Getopt-Long-Descriptive/
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(Carp)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Getopt::Long) >= 2.33
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Params::Validate) >= 0.97
BuildRequires:  perl(Sub::Exporter) >= 0.972
BuildRequires:  perl(Sub::Exporter::Util)
BuildRequires:  perl(overload)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)

# obsolete/provide old tests subpackage
# can be removed during F19 development cycle
Obsoletes:      %{name}-tests < 0.090-4
Provides:       %{name}-tests = %{version}-%{release}

%{?perl_default_filter}

%description
Convenient wrapper for Getopt::Long and program usage output.

%prep
%setup -q -n Getopt-Long-Descriptive-%{version}

# silence rpmlint warnings
sed -i '1s,#!.*perl,#!%{__perl},' t/*.t

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \;

%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc Changes README t/
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.093-2
- 为 Magic 3.0 重建

* Fri Nov 02 2012 Iain Arnell <iarnell@gmail.com> 0.093-1
- update to latest upstream version

* Fri Aug 03 2012 Iain Arnell <iarnell@gmail.com> 0.092-1
- update to latest upstream version

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.091-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 0.091-2
- Perl 5.16 rebuild

* Thu Feb 23 2012 Iain Arnell <iarnell@gmail.com> 0.091-1
- update to latest upstream version

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> 0.090-4
- drop tests subpackage; move tests to main package documentation

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.090-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.090-2
- Perl mass rebuild

* Sat Jul 02 2011 Iain Arnell <iarnell@gmail.com> 0.090-1
- update to latest upstream version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.087-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 08 2011 Iain Arnell <iarnell@gmail.com> 0.087-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.084-3
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.084-2
- Mass rebuild with perl-5.12.0

* Sat Feb 27 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.084-1
- update by Fedora::App::MaintainerTools 0.004
- PERL_INSTALL_ROOT => DESTDIR
- added a new br on perl(Getopt::Long) (version 2.33)
- dropped old BR on perl(IO::Scalar)
- dropped old BR on perl(Test::Pod::Coverage)
- added a new req on perl(Getopt::Long) (version 2.33)
- dropped old requires on perl(IO::Scalar)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.077-2
- rebuild against perl 5.10.1

* Sun Aug 23 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.077-1
- auto-update to 0.077 (by cpan-spec-update 0.01)
- added a new br on perl(List::Util) (version 0)
- added a new br on perl(Sub::Exporter) (version 0)
- added a new req on perl(List::Util) (version 0)
- added a new req on perl(Params::Validate) (version 0.74)
- added a new req on perl(Sub::Exporter) (version 0)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.074-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.074-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul 09 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.074-2
- bump

* Tue Jul 08 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.074-1
- Specfile autogenerated by cpanspec 1.74.