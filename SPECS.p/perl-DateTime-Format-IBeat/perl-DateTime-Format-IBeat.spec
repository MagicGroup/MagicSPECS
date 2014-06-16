Name:           perl-DateTime-Format-IBeat
Version:        0.161
Release:        20%{?dist}
Summary:        Format times in .beat notation 

Group:          Development/Libraries
License:        GPL+ or Artistic 
URL:            http://search.cpan.org/dist/DateTime-Format-IBeat            
Source0:        http://backpan.perl.org/authors/id/E/EM/EMARTIN/DateTime-Format-IBeat-0.161.tar.gz

BuildArch:      noarch 
BuildRequires:  perl(Class::ISA)
BuildRequires:  perl(DateTime) >= 0.18, perl(Test::More) >= 0.47
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::Pod) >= 1.00
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
No Time Zones, No Geographical Borders 

How long is a Swatch .beat? In short, we have divided up the virtual and real 
day into 1000 beats. One Swatch beat is the equivalent of 1 minute 26.4 
seconds. That means that 12 noon in the old time system is the equivalent of 
500 Swatch .beats.


%prep
%setup -q -n DateTime-Format-IBeat-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

# American English...
mv LICENCE LICENSE

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
chmod -R u+w %{buildroot}/*


%check
make test


%files
%doc Artistic COPYING LICENSE Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.161-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.161-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 31 2013 Petr Pisar <ppisar@redhat.com> - 0.161-18
- Perl 5.18 rebuild

* Sun Feb 17 2013 Iain Arnell <iarnell@gmail.com> 0.161-17
- update spec for modern rpmbuild
- BR ExtUtils::MakeMaker
- change source link to backpan - it's no longer in cpan

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.161-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.161-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 0.161-14
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.161-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.161-12
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.161-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.161-10
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.161-9
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.161-8
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.161-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.161-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar 04 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.161-5
- rebuild for new perl

* Thu Aug 31 2006 Chris Weyl <cweyl.drew.edu> 0.161-4
- bump for mass rebuild

* Sun Aug 06 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.161-3
- add br for test phase: perl(Test::Pod)

* Sun Aug 06 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.161-2
- bump for build & release
- dropped extra template bits not needed for noarch packages

* Fri Aug 04 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.161-1
- Initial spec file for F-E
