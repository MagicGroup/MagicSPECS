Name:           perl-Unicode-String
Version:        2.09
Release:        30%{?dist}

Summary:        Perl modules to handle various Unicode issues

Group:          Development/Libraries
# in CharName.pm is mentioned use of Unicode table, but fonts are not used
# so here can't be UCD license
# in String.xs is mentioned "same terms as Perl itself" which is this
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Unicode-String/
Source0:        http://www.cpan.org/authors/id/G/GA/GAAS/Unicode-String-2.09.tar.gz
Patch0:         perl-Unicode-String-2.09-utf8doc.patch
Patch1:         perl-Unicode-String-2.09-undefined.patch

BuildRequires:  perl(ExtUtils::MakeMaker), perl(MIME::Base64)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
# not detected by auto provide scripts:
Requires:       perl(MIME::Base64)

%{?perl_default_filter}

%description
%{summary}.


%prep
%setup -q -n Unicode-String-%{version}

# Recode documentation as UTF-8
# Can't just use iconv because README includes an example of
# character code conversion that would be wrong if simply recoded
%patch0 -p1

# Suppress warnings in newer versions of Perl
# Patch is upstreamed as RT #74354
%patch1 -p1

%build
CFLAGS="$RPM_OPT_FLAGS" %{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags} OPTIMIZE="$RPM_OPT_FLAGS"


%install
make install \
  DESTDIR=$RPM_BUILD_ROOT \
  INSTALLARCHLIB=$RPM_BUILD_ROOT%{perl_archlib}
find $RPM_BUILD_ROOT -type f \( -name perllocal.pod -o -name .packlist \
  -o \( -name '*.bs' -empty \) \) -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -empty -exec rmdir {} ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check



%files
%doc Changes README
%{perl_vendorarch}/auto/Unicode
%{perl_vendorarch}/Unicode
%{_mandir}/man3/*.3*


%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 2.09-30
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 2.09-29
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.09-28
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.09-27
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.09-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 2.09-25
- Perl 5.16 rebuild

* Sun Jun 24 2012 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 2.09-24
- Really add the patch

* Sun Jun 24 2012 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 2.09-23
- Add patch to suppress warnings (#834867)
- Clean up spec file

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 2.09-22
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.09-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jul 24 2011 Iain Arnell <iarnell@gmail.com> 2.09-20
- use perl_default_filter

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.09-19
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.09-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.09-17
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Jul 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.09-16
- apply ppisar hints from 558743

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.09-15
- Mass rebuild with perl-5.12.0

* Thu Feb 18 2010 Paul Howarth <paul@city-fan.org> - 2.09-14
- carefully convert documentation to UTF-8 encoding
- add :MODULE_COMPAT_* dependency

* Wed Feb 17 2010 Marcela Mašláňová <mmaslano@redhat.com> - 2.09-13
- fix license

* Tue Jan 26 2010 Stepan Kasal <skasal@redhat.com> - 2.09-12
- better buildroot
- no need to define perl_vendorarch

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.09-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.09-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jun 05 2008 Aurelien Bompard <abompard@fedoraproject.org> 2.09-9
- fix build

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.09-8
- Rebuild for perl 5.10 (again)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.09-7
- Autorebuild for GCC 4.3

* Mon Jan 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.09-6
- rebuild for new perl

* Thu Sep 27 2007 Aurelien Bompard <abompard@fedoraproject.org> 2.09-5
- fix license tag again (thanks Tom)

* Sun Aug 26 2007 Aurelien Bompard <abompard@fedoraproject.org> 2.09-4
- fix license tag (like perl itself)

* Mon Aug 13 2007 Aurelien Bompard <abompard@fedoraproject.org> 2.09-3
- BR: perl-devel

* Wed Aug 30 2006 Aurelien Bompard <abompard@fedoraproject.org> 2.09-2
- rebuild

* Tue Feb 21 2006 Aurelien Bompard <gauret[AT]free.fr> 2.09-1
- version 2.09

* Tue Feb 21 2006 Aurelien Bompard <gauret[AT]free.fr> 2.07-6
- rebuild for FC5

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Mon Feb  2 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:2.07-0.fdr.4
- Reduce directory ownership bloat.

* Sat Oct 11 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.07-0.fdr.3
- Install into vendor dirs.
- Spec cleanup.

* Mon Jul  7 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.07-0.fdr.2
- Regenerate %%install section with cpanflute2.

* Wed May  7 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:2.07-0.fdr.1
- Update to 2.07 and to current Fedora guidelines.

* Sun Mar  2 2003 Ville Skyttä <ville.skytta at iki.fi> - 2.06-1.fedora.1
- First Fedora release.
