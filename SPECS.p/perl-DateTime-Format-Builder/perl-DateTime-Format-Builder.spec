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
%define real_version   0.80

Name:           perl-DateTime-Format-Builder
# 0.80 in reality, but rpm can't get it
Version:        0.8000
Release:        11%{?dist}
Summary:        Create DateTime parser classes and objects        

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/DateTime-Format-Builder            
Source0:        http://search.cpan.org/CPAN/authors/id/D/DR/DROLSKY/DateTime-Format-Builder-%{real_version}.tar.gz        

BuildArch: noarch
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

## core
BuildRequires:  perl(Test::More)
## non-core
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Class::ISA)
BuildRequires:  perl(Class::Factory::Util)
BuildRequires:  perl(DateTime)
BuildRequires:  perl(DateTime::Format::Strptime)
BuildRequires:  perl(Params::Validate) >= 0.73
# note -- listed as a BR but _not_ needed with Fedora perl
#BuildRequires:  perl(Task::Weaken)
BuildRequires:  perl(Test::Pod)
## For extended testing
BuildRequires:  perl(DateTime::Format::HTTP)
BuildRequires:  perl(DateTime::Format::Mail)
BuildRequires:  perl(DateTime::Format::IBeat)
Provides:       perl(DateTime::Format::Builder) = %{version}

# for signature checking
%{?_with_network_tests:BuildRequires: perl(Module::Signature) }

# not explicitly picked up
Requires:       perl(DateTime::Format::Strptime)

%{?perl_default_filter}

%description
DateTime::Format::Builder creates DateTime parsers. Many string formats of
dates and times are simple and just require a basic regular expression to
extract the relevant information. Builder provides a simple way to do this
without writing reams of structural code.

Builder provides a number of methods, most of which you'll never need, or at
least rarely need. They're provided more for exposing of the module's innards
to any subclasses, or for when you need to do something slightly beyond what
is expected.


%prep
%setup -q -n DateTime-Format-Builder-%{real_version}

cat << \EOF > %{name}-req
#!/bin/sh
%{__perl_requires} $* |\
   sed -e '/perl(DateTime::Format::HTTP)/d;/perl(DateTime::Format::IBeat)/d' \
       -e '/perl(DateTime::Format::Mail)/d'
EOF

%define __perl_requires %{_builddir}/DateTime-Format-Builder-%{real_version}/%{name}-req
chmod +x %{__perl_requires}

# digital signature checking.  Not essential, but nice
%{?_with_network_tests: cpansign -v }

# POD doesn't like E<copy> very much...
perl -pi -e 's/E<copy>/(C)/' `find lib/ -type f`

# American English
mv LICENCE LICENSE


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor 
make %{?_smp_mflags}


%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} +
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*


%check



%files
%defattr(-,root,root,-)
%doc COPYING Artistic Changes AUTHORS CREDITS LICENSE README examples/ t/
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.8000-11
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8000-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 0.8000-9
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8000-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.8000-7
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.8000-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8000-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.8000-4
- 661697 rebuild for fixing problems with vendorach/lib

* Sun Dec 12 2010 Iain Arnell <iarnell@gmail.com> 0.8000-3
- use perl_default_filter
- clean up spec for modern rpmbuild

* Fri May 14 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.8000-2
- add provides with rpm version for other packages

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.8000-1
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.7901-5
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7901-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7901-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.7901-2
- rebuild for new perl

* Sat Jan 26 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.7901-1
- update to 0.7901
- additional docs
- some spec rework

* Thu Aug 31 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.7807-4
- bump for mass rebuild

* Tue Aug 08 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.7807-3
- bump for release & build, not in that order

* Tue Aug 08 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.7807-2
- additional br's

* Fri Aug 04 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.7807-1
- Initial spec file for F-E
