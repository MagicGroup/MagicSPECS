Name:           perl-MooseX-Types-Path-Class 
Summary:        A Path::Class type library for Moose 
Version:	0.08
Release:	1%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/MooseX-Types-Path-Class-%{version}.tar.gz
URL:            http://search.cpan.org/dist/MooseX-Types-Path-Class
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(Class::MOP)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Moose) >= 0.39
BuildRequires:  perl(MooseX::Getopt) >= 0.05
BuildRequires:  perl(MooseX::Types) >= 0.04
BuildRequires:  perl(Path::Class) >= 0.16
BuildRequires:  perl(Test::More) >= 0.88

Requires:       perl(Class::MOP)
Requires:       perl(Moose) >= 0.39
Requires:       perl(MooseX::Types) >= 0.04
Requires:       perl(Path::Class) >= 0.16

# obsolete/provide old tests subpackage
Obsoletes:      %{name}-tests < 0.06-1
Provides:       %{name}-tests = %{version}-%{release}

%{?perl_default_filter}

%description
MooseX::Types::Path::Class creates common Moose types, coercions and option
specifications useful for dealing with Path::Class objects as Moose attributes.  

Coercions (see Moose::Util::TypeConstraints) are made from both 'Str' and 
'ArrayRef' to both Path::Class::Dir and Path::Class::File objects.  If you
have MooseX::Getopt installed, the Getopt option type ("=s") will be added
for both Path::Class::Dir and Path::Class::File.

%prep
%setup -q -n MooseX-Types-Path-Class-%{version}

sed -i '1s:^#!.*perl:#!%{__perl}:' t/*.t

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc Changes README t/
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.08-1
- 更新到 0.08

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.06-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.06-2
- Perl 5.16 rebuild

* Fri Mar 30 2012 Iain Arnell <iarnell@gmail.com> 0.06-1
- update to latest upstream version
- clean up spec for modern rpmbuild
- drop tests subpackage; move tests to main package documentation
- silence rpmlint wrong-script-interpreter error

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.05-11
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.05-9
- 661697 rebuild for fixing problems with vendorach/lib

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.05-8
- Mass rebuild with perl-5.12.0

* Tue Feb 23 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.05-7
- massive spec cleanups, etc.
- update by Fedora::App::MaintainerTools 0.003
- PERL_INSTALL_ROOT => DESTDIR
- added a new br on perl(Class::MOP) (version 0)
- added a new br on perl(Moose) (version 0.39)
- dropped old BR on perl(Test::Pod)
- dropped old BR on perl(Test::Pod::Coverage)
- added a new req on perl(Class::MOP) (version 0)
- added a new req on perl(Moose) (version 0.39)
- added a new req on perl(MooseX::Types) (version 0.04)
- added a new req on perl(Path::Class) (version 0.16)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.05-6
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Nov 16 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.05-3
- bump

* Fri Nov 07 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.05-2
- filter _docdir prov/req's

* Sat Nov 01 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.05-1
- update to 0.05
- brush up for submission

* Tue Oct 07 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.04-1
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.1)
