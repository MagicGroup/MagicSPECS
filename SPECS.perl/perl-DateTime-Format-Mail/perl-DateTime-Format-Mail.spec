Name:           perl-DateTime-Format-Mail
Version:	0.4020
Release:	1%{?dist}
Summary:        Convert between DateTime and RFC2822/822 formats

Group:          Development/Libraries
License:        GPL+ or Artistic        
URL:            http://search.cpan.org/dist/DateTime-Format-Mail            
%define cpan_version 0.402
Source0:        http://search.cpan.org/CPAN/authors/id/B/BO/BOOK/DateTime-Format-Mail-%{cpan_version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(Class::ISA)
BuildRequires:  perl(Module::Build), perl(DateTime) 
BuildRequires:  perl(Params::Validate) >= 0.67, perl(Test::More) >= 0.47
BuildRequires:  perl(File::Find::Rule)

Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# DateTime >= 0.1705 plays havoc with rpm's versioning system
Requires:       perl(DateTime) >= 0.18
%{?filter_setup:
%filter_from_requires s/^perl(DateTime).*/d
%{?perl_default_filter}
}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(DateTime\\)

%description
RFCs 2822 and 822 specify date formats to be used by email. This module parses
and emits such dates.

RFC2822 (April 2001) introduces a slightly different format of date than that
used by RFC822 (August 1982). The main correction is that the preferred format
is more limited, and thus easier to parse programmatically.

Despite the ease of generating and parsing perfectly valid RFC822 and RFC2822
people still get it wrong. This module aims to correct that.


%prep
%setup -q -n DateTime-Format-Mail-%{cpan_version}

# POD doesn't like E<copy> very much...
perl -pi -e 's/E<copy>/(C)/' `find lib/ -type f`


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w %{buildroot}/*


%check
# we don't have a SIGNATURE, regardless of perl(Test::Signature) being around
rm t/00signature.t




%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc t/sample_dates t/invalid.t
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%changelog
* Tue Sep 15 2015 Liu Di <liudidi@gmail.com> - 0.4020-1
- 更新到 0.4020

* Tue Sep 15 2015 Liu Di <liudidi@gmail.com> - 0.402-3
- 为 Magic 3.0 重建

* Tue Sep 15 2015 Liu Di <liudidi@gmail.com> - 0.402-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.402-1
- 更新到 0.402

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.3001-21
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.3001-20
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.3001-19
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.3001-18
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.3001-17
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.3001-16
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.3001-15
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.3001-14
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3001-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Iain Arnell <iarnell@gmail.com> - 0.3001-12
- update filtering macros for rpm 4.9

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.3001-11
- Perl mass rebuild

* Mon Feb 14 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.3001-10
- Switch to using perl-filters/Abandon filter-requires.sh 
  (Work around mass rebuild breakdown).

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3001-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.3001-8
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.3001-7
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.3001-6
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3001-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3001-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.3001-3
- Rebuild for perl 5.10 (again)

* Fri Jan 25 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.3001-2
- no more notes/ directory

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.3001-1
- 0.3001
- fix license tag
- rebuild against new perl

* Thu Aug 31 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.30-4
- bump for mass rebuild

* Sun Aug 06 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.30-3
- bump for build and release

* Sun Aug 06 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.30-2
- add missing br: perl(File::Find::Rule)
- additional files from the test suite added to %%doc

* Fri Aug 04 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.30-1
- Initial spec file for F-E
