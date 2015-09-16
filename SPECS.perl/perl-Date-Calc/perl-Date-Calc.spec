Name:           perl-Date-Calc
Version:	6.4
Release:	1%{?dist}
Summary:        Gregorian calendar date calculations

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Date-Calc/
Source0:        http://www.cpan.org/authors/id/S/ST/STBEY/Date-Calc-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Carp::Clan) >= 6.3
BuildRequires:  perl(Bit::Vector) >= 7.1
Requires:       perl(Bit::Vector) >= 7.1
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

%description
The library provides all sorts of date calculations based on the
Gregorian calendar (the one used in all western countries today),
thereby complying with all relevant norms and standards: ISO/R
2015-1971, DIN 1355 and, to some extent, ISO 8601 (where applicable).


%prep
%setup -q -n Date-Calc-%{version} 
%{__perl} -pi -e 's|^#!perl\b|#!%{__perl}|' examples/*.{pl,cgi} tools/*.pl

# Filter unwanted Provides:
cat << \EOF > %{name}-prov
#!/bin/sh
%{__perl_provides} $* |\
  sed -e '/^perl(Date::Calc)$/d'
EOF

%define __perl_provides %{_builddir}/Date-Calc-%{version}/%{name}-prov
chmod +x %{__perl_provides}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

for file in $RPM_BUILD_ROOT%{_mandir}/man3/Date::Calc.3pm \
            CREDITS.txt; do
  iconv -f iso-8859-1 -t utf-8 < "$file" > "${file}_"
  mv -f "${file}_" "$file"
done

%check



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc license/Artistic.txt license/GNU_GPL.txt license/GNU_LGPL.txt
%doc CHANGES.txt CREDITS.txt README.txt
%{perl_vendorlib}/Date/
%{_mandir}/man3/*.3*


%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 6.4-1
- 更新到 6.4

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 6.3-14
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 6.3-13
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 6.3-12
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 6.3-10
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 6.3-8
- Perl mass rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 6.3-7
- Perl mass rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 6.3-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 6.3-4
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 6.3-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 6.3-2
- rebuild against perl 5.10.1

* Wed Nov 18 2009 Marcela Mašláňová <mmaslano@redhat.com> - 6.3-1
- new upstream version - noarch, because since 6.0 there were bigger
 changes like stripping this module into more of them

* Mon Oct 19 2009 Marcela Mašláňová <mmaslano@redhat.com> - 6.2-1
- new upstream version

* Tue Aug  4 2009 Stepan Kasal <skasal@redhat.com> - 5.6-1
- new upstream version

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 5.4-6
- rebuild for new perl

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 5.4-5
- Autorebuild for GCC 4.3

* Mon Nov 12 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 5.4-4
- filtered out too many provides

* Wed Oct 24 2007 Robin Norwood <rnorwood@redhat.com> - 5.4-3
- various specfile fixes

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 5.4-2.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Mon Aug 27 2007 Robin Norwood <rnorwood@redhat.com> - 5.4-2
- Update License tag
- Clean up minor specfile issues

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 5.4-1.2.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 5.4-1.2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 5.4-1.2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 5.4-1.2
- rebuild for new perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Sat Apr  2 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 5.4-1
- Update to 5.4.
- Bring up to date with current Fedora.Extras perl spec template.

* Thu Nov 25 2004 Miloslav Trmac <mitr@redhat.com> - 5.3-10
- Convert man page to UTF-8

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Chip Turner <cturner@redhat.com> 5.3-5
- rebuilt

* Thu Jun 05 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Dec 10 2002 Chip Turner <cturner@redhat.com>
- update to latest version from CPAN

* Tue Aug  6 2002 Chip Turner <cturner@redhat.com>
- automated release bump and build

* Wed Jan 30 2002 cturner@redhat.com
- Specfile autogenerated

