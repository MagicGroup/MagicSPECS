# Note:  Some tests for this package are disabled by default, as they
# require network access and would thus fail in the buildsys' mock
# environments.  To build locally while enabling tests, either:
#
#   rpmbuild ... --define '_with_network_tests 1' ...
#   rpmbuild ... --with network_tests ...
#   define _with_network_tests 1 in your ~/.rpmmacros
#
# Note that right now, the only way to run tests locally from a cvs sandbox
# "make noarch" type scenario is the third one.


Name:           perl-DateTime-Format-MySQL
Version:        0.04        
Release:        18%{?dist}
Summary:        Parse and format MySQL dates and times 

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/DateTime-Format-MySQL            
Source0: http://search.cpan.org/CPAN/authors/id/D/DR/DROLSKY/DateTime-Format-MySQL-%{version}.tar.gz        
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch 
BuildRequires:  perl(Module::Build), perl(DateTime)
BuildRequires:  perl(DateTime::Format::Builder)
BuildRequires:  perl(Test::More)

# not picked up explicitly, for whatever reason...
Requires:  perl(DateTime::Format::Builder)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# for signature checking
%{?_with_network_tests:BuildRequires: perl(Module::Signature) }


%description
This module understands the formats used by MySQL for its DATE, DATETIME,
TIME, and TIMESTAMP data types. It can be used to parse these formats in order
to create DateTime objects, and it can take a DateTime object and produce a
string representing it in the MySQL format.


%prep
%setup -q -n DateTime-Format-MySQL-%{version}

# digital signature checking.  Not essential, but nice
%{?_with_network_tests: cpansign -v }


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*


%check



%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc Changes LICENSE README
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.04-18
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 0.04-16
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.04-14
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.04-13
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.04-11
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.04-10
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.04-9
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar 04 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.04-6
- rebuild for new perl

* Tue Jan 01 2008 Ralf Corsépius <rc040203@freenet.de> 0.04-5
- Adjust License-tag.
- Add BR: perl(Test::More) (BZ 419631).
- Minor spec cosmetics.

* Fri Sep 08 2006 Chris Weyl <cweyl@alumni.drew.edu>
- add missing explicit requires on perl(DateTime::Format::Builder)
- misc spec tweaks

* Thu Aug 31 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.04-3
- bump for mass rebuild

* Thu Aug 10 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.04-2
- bump for build & release

* Fri Aug 04 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.04-1
- Initial spec file for F-E
