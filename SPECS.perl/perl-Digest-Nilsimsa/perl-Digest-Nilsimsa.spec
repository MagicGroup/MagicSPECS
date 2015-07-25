Name:           perl-Digest-Nilsimsa
Version:        0.06
Release:        23%{?dist}

Summary:        Perl interface to the Nilsima Algorithm

Group:          Development/Libraries
License:        GPLv2+
Source0:        http://www.cpan.org/authors/id/V/VI/VIPUL/Digest-Nilsimsa-%{version}.tar.gz
URL:            http://search.cpan.org/dist/Digest-Nilsimsa/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  perl(ExtUtils::MakeMaker)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
%{summary}.


%prep
%setup -q -n Digest-Nilsimsa-%{version}


%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING README
%{perl_vendorarch}/Digest/
%{perl_vendorarch}/auto/Digest/
%{_mandir}/man3/*.3*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.06-23
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.06-22
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.06-21
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.06-20
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 15 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.06-18
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.06-16
- 661697 rebuild for fixing problems with vendorach/lib

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.06-15
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.06-14
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.06-13
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul  1 2008 Paul Howarth <paul@city-fan.org> 0.06-10
- Add perl(:MODULE_COMPAT...) dependency (#453564)
- Remove redundant buildreq perl
- Clean buildroot at start of %%install
- Move "" to %%check
- Install into %%{perl_vendorarch} and use "make pure_install"
- Fix argument order for find with -depth
- Only specify compiler flags once
- Only specify version number once

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> 0.06-9.1
- Autorebuild for GCC 4.3

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.06-8.1
- add BR: perl(ExtUtils::MakeMaker)

* Tue Aug 21 2007 Warren Togami <wtogami@redhat.com> 0.06-8
- rebuild

* Thu Sep 14 2006 Warren Togami <wtogami@redhat.com> 0.06-7
- rebuild for FC6

* Thu Mar 16 2006 Warren Togami <wtogami@redhat.com> 0.06-6
- rebuild for FC5

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun Nov 23 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.06-0.fdr.4
- Specfile rewrite.
- Fix license (GPL only).

* Fri Jul 04 2003 Warren Togami <warren@togami.com> 0.06-0.fdr.3
- prep build install clean files from cpanflute2
- Development/Libraries
- 
- Change to upstream .gz
- Drop Mandrake .spec
- A few cosmetic changes

* Sun Jun 15 2003 Warren Togami <warren@togami.com> 0.06-0.fdr.2
- Apply anvil's spec patch

* Sat Jun 14 2003 Warren Togami <warren@togami.com> 0.06-0.fdr.1
- Initial Fedora conversion attempt

* Tue May 27 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.06-4mdk
- rebuild for new auto{prov,req}
