Name:           perl-LDAP
Version:	0.65
Release:	3%{?dist}
Epoch:          1
Summary:        LDAP Perl module

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/perl-ldap/
Source0:        http://search.cpan.org/CPAN/authors/id/M/MA/MARSCHAP/perl-ldap-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(Convert::ASN1)
BuildRequires:  perl(IO::Socket::SSL)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(IO::Socket::SSL)
Requires:       perl(Authen::SASL)

%description
Net::LDAP is a collection of modules that implements a LDAP services API
for Perl programs. The module may be used to search directories or perform
maintenance functions such as adding, deleting or modifying entries.


%prep
%setup -q -n perl-ldap-%{version}
chmod -c 644 bin/* contrib/* lib/Net/LDAP/DSML.pm
%{__perl} -pi -e 's|^#!/usr/local/bin/perl\b|#!%{__perl}|' contrib/*

# Filter unwanted Provides:
cat << \EOF > %{name}-prov
#!/bin/sh
%{__perl_provides} $* |\
  sed -e '/perl(Net::LDAP::Filter)$/d'
EOF

%define __perl_provides %{_builddir}/perl-ldap-%{version}/%{name}-prov
chmod +x %{__perl_provides}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor < /dev/null
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check

 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes CREDITS
%doc contrib/ bin/
%{perl_vendorlib}/Bundle/
%{perl_vendorlib}/LWP/
%{perl_vendorlib}/Net/
%{_mandir}/man3/*.3pm*


%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1:0.65-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1:0.65-2
- 为 Magic 3.0 重建

* Wed Sep 16 2015 Liu Di <liudidi@gmail.com> - 1:0.65-1
- 更新到 0.65

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1:0.40-14
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1:0.40-13
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1:0.40-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1:0.40-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1:0.40-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1:0.40-9
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1:0.40-8
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1:0.40-7
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.40-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1:0.40-5
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.40-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:0.40-3
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:0.40-2
- Mass rebuild with perl-5.12.0

* Mon Apr 12 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1:0.40-1
- update

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1:0.34-7
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.34-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.34-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:0.34-4
- rebuild for new perl

* Mon Apr 09 2007 Robin Norwood <rnorwood@redhat.com> - 1:0.34-3
- Resolves: bz#226267
- Only filter out the unversioned Provides: perl(Net::LDAP::Filter) to
  avoid breaking dependencies.

* Thu Apr 05 2007 Robin Norwood <rnorwood@redhat.com> - 1:0.34-2
- Resolves: bz#226267
- Filter out provides perl(Net::LDAP::Filter) per package review.

* Tue Feb 13 2007 Robin Norwood <rnorwood@redhat.com> - 1:0.34-1
- New version: 0.34

* Wed Sep 27 2006 Robin Norwood <rnorwood@redhat.com> - 1:0.33-3
- Bugzilla: 207430
- Incorporate fixes from Jose Oliveira's patch
- Add perl(IO::Socket::SSL) as a BuildRequires as well
- Other cleanups from Jose

* Wed Sep 27 2006 Robin Norwood <rnorwood@redhat.com> - 0.33-1.3
- Add a requirement for IO::Socket::SSL, per bug #122066

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 0.33-1.2
- rebuild for new perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Tue Apr 26 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.33-1
- Update to 0.33.

* Sat Apr 02 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.3202-1
- Update to 0.3202.
- Specfile cleanup. (#153766)

* Wed Sep 22 2004 Chip Turner <cturner@redhat.com> 0.31-5
- rebuild

* Wed Mar 10 2004 Chip Turner <cturner@redhat.com> - 0.31-1
- Specfile autogenerated.

