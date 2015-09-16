Name:           perl-CPAN-Mini
Summary:        Create a minimal mirror of CPAN
Version:	1.111016
Release:	1%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/R/RJ/RJBS/CPAN-Mini-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/CPAN-Mini/
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(Carp)
BuildRequires:  perl(Compress::Zlib) >= 1.20
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.30
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::HomeDir) >= 0.57
BuildRequires:  perl(File::Path) >= 2.04
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(LWP::UserAgent) >= 5
BuildRequires:  perl(Pod::Usage) >= 1.00
BuildRequires:  perl(Test::More) >= 0.96
BuildRequires:  perl(URI) >= 1

# obsolete/provide old tests subpackage
# can be removed during F19 development cycle
Obsoletes:      %{name}-tests < 1.111007-3
Provides:       %{name}-tests = %{version}-%{release}

%{?perl_default_filter}

%description
CPAN::Mini provides a simple mechanism to build and update a minimal 
mirror of the CPAN on your local disk containing only those files 
needed to install the newest version of every distribution. 

%prep
%setup -q -n CPAN-Mini-%{version}

perl -pi -e 's|^#!perl|#!/usr/bin/perl|' t/*

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
%doc Changes LICENSE README t/
%{_bindir}/*
%{perl_vendorlib}/*
%{_mandir}/man[13]/*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.111016-1
- 更新到 1.111016

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.111007-8
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.111007-7
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.111007-6
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.111007-5
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.111007-4
- 为 Magic 3.0 重建

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> 1.111007-3
- drop tests subpackage; move tests to main package documentation

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.111007-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 02 2011 Iain Arnell <iarnell@gmail.com> 1.111007-1
- update to latest upstream version
- clean up spec for modern rpmbuild
- don't package tests as doc
- remove explicit requires

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.100630-5
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.100630-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.100630-3
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.100630-2
- Mass rebuild with perl-5.12.0

* Tue Mar 23 2010 Chris Weyl <cweyl@alumni.drew.edu> 1.100630-1
- update by Fedora::App::MaintainerTools 0.006
- PERL_INSTALL_ROOT => DESTDIR
- updating to latest GA CPAN version (1.100630)
- added a new br on perl(Carp) (version 0)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.11)
- added a new br on perl(File::Basename) (version 0)
- added a new br on perl(File::Copy) (version 0)
- added a new br on perl(File::Find) (version 0)
- added a new br on perl(File::Spec) (version 0)
- added a new br on perl(File::Temp) (version 0)
- added a new br on perl(Getopt::Long) (version 0)
- added a new br on perl(LWP::UserAgent) (version 5)
- added a new br on perl(Pod::Usage) (version 1.00)
- dropped old BR on perl(LWP)
- added a new req on perl(Carp) (version 0)
- added a new req on perl(Compress::Zlib) (version 1.20)
- added a new req on perl(File::Basename) (version 0)
- added a new req on perl(File::Copy) (version 0)
- added a new req on perl(File::Find) (version 0)
- added a new req on perl(File::HomeDir) (version 0.57)
- added a new req on perl(File::Path) (version 2.04)
- added a new req on perl(File::Spec) (version 0)
- added a new req on perl(File::Temp) (version 0)
- added a new req on perl(Getopt::Long) (version 0)
- added a new req on perl(LWP::UserAgent) (version 5)
- added a new req on perl(Pod::Usage) (version 1.00)
- added a new req on perl(URI) (version 1)

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.576-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.576-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.576-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 25 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.576-1
- update to 0.576

* Fri May 30 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.571-2
- bump

* Thu May 29 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.571-1
- update to 0.571

* Wed Apr 23 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.568-2
- additional br 

* Wed Apr 23 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.568-1
- Specfile autogenerated by cpanspec 1.74.
