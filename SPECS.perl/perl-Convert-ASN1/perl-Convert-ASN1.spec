Summary:        ASN.1 Encode/Decode library
Name:           perl-Convert-ASN1
Version:        0.22
Release:        11%{?dist}

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Convert-ASN1/
Source0:        http://www.cpan.org/authors/id/G/GB/GBARR/Convert-ASN1-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Convert::ASN1 encodes and decodes ASN.1 data structures using BER/DER rules.


%prep
%setup -q -n Convert-ASN1-%{version}

# Provides: exclude perl(Convert::ASN1)
cat <<__EOF__ > %{name}-perl.prov
#!/bin/sh
/usr/lib/rpm/perl.prov \$* | grep -v '^perl(Convert::ASN1)$'
__EOF__
%define __perl_provides %{_builddir}/Convert-ASN1-%{version}/%{name}-perl.prov
chmod +x %{__perl_provides}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc ChangeLog README examples/
%{perl_vendorlib}/Convert/
%{_mandir}/man3/*.3pm*


%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.22-11
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.22-10
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.22-9
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.22-8
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.22-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.22-4
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.22-3
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.22-2
- rebuild against perl 5.10.1

* Mon Jul 27 2009 Marcela Mašláňová <mmaslano@redhat.com> - 0.22-1
- update to 0.22

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.21-3
- rebuild for new perl

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.21-2.1
- add BR: perl(ExtUtils::MakeMaker)

* Fri Aug 24 2007 Robin Norwood <rnorwood@redhat.com> - 0.21-2
- Fix license tag.

* Sat Feb  3 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.21-1
- Update to 0.21.
- Corrected several changelog entries.
- Removed an explicit perl(Convert::ASN1) provides.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.20-1.1
- rebuild

* Thu Mar 09 2006 Jason Vas Dias <jvdias@redhat.com> - 0.20-1
- upgrade to upstream version 0.20

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 0.19-1.2
- rebuild for new perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Wed Apr 20 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.19-1
- Update to 0.19. (#155458)
- Bring up to date with current Fedora.Extras perl spec template.

* Wed Sep 22 2004 Chip Turner <cturner@redhat.com> 0.18-3
- rebuild

* Wed Mar 10 2004 Chip Turner <cturner@redhat.com> - 0.18-1
- Specfile autogenerated.