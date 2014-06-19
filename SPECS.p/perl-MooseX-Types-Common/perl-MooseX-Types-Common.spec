Name:           perl-MooseX-Types-Common 
Summary:        A library of commonly used type constraints 
Version:        0.001008
Release:        6%{?dist}
License:        GPL+ or Artistic 
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/MooseX-Types-Common-%{version}.tar.gz
URL:            http://search.cpan.org/dist/MooseX-Types-Common
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(Capture::Tiny)
BuildRequires:  perl(inc::Module::Install)
BuildRequires:  perl(Moose) >= 0.39
BuildRequires:  perl(MooseX::Types) >= 0.04
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::More) >= 0.62

# obsolete/provide old tests subpackage
# can be removed during F19 development cycle
Obsoletes:      %{name}-tests < 0.001004-2
Provides:       %{name}-tests = %{version}-%{release}

%{?perl_default_filter}

%description
A set of commonly-used type constraints that do not ship with Moose
by default.


%prep
%setup -q -n MooseX-Types-Common-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'

%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc README Changes t/
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.001008-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 0.001008-5
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.001008-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.001008-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.001008-2
- Perl 5.16 rebuild

* Sun Jun 17 2012 Iain Arnell <iarnell@gmail.com> 0.001008-1
- update to latest upstream version
- BR inc::Module::Install instead of EU::MM

* Sun Feb 26 2012 Iain Arnell <iarnell@gmail.com> 0.001007-1
- update to latest upstream version
- drop Test::Exception build requirement again

* Thu Feb 23 2012 Iain Arnell <iarnell@gmail.com> 0.001006-1
- update to latest upstream version

* Tue Feb 21 2012 Iain Arnell <iarnell@gmail.com> 0.001005-1
- update to latest upstream version

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> 0.001004-2
- drop tests subpackage; move tests to main package documentation

* Thu Jan 12 2012 Iain Arnell <iarnell@gmail.com> 0.001004-1
- update to latest upstream version
- remove unnecessary explicit requires

* Sat Oct 01 2011 Iain Arnell <iarnell@gmail.com> 0.001003-1
- update to latest upstream version
- clean up spec for modern rpmbuild
- BR Capture::Tiny for improved test coverage

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.001002-5
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.001002-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.001002-3
- 661697 rebuild for fixing problems with vendorach/lib

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.001002-2
- Mass rebuild with perl-5.12.0

* Sun Mar 14 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.001002-1
- update by Fedora::App::MaintainerTools 0.006
- PERL_INSTALL_ROOT => DESTDIR
- updating to latest GA CPAN version (0.001002)
- added a new req on perl(Moose) (version 0.39)
- added a new req on perl(MooseX::Types) (version 0.04)

* Sat Feb 06 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.001001-1
- submission

* Sat Feb 06 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.001001-0
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)
