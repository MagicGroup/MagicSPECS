%{!?perl_vendorarch: %define perl_vendorarch %(eval "`%{__perl} -V:installvendorarch`"; echo $installvendorarch)}

Name:           perl-Unicode-Map8
Version:        0.13
Release:        14%{?dist}

Summary:        Mapping table between 8-bit chars and Unicode for Perl

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Unicode-Map8/
Source0:        http://www.cpan.org/authors/id/G/GA/GAAS/Unicode-Map8-%{version}.tar.gz
Patch0:         perl-Unicode-Map8-0.12-declaration.patch
Patch1:         perl-Unicode-Map8-0.12-type.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  perl(ExtUtils::MakeMaker), perl(Unicode::String)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))


%description
The Unicode::Map8 class implements efficient mapping tables between
8-bit character sets and 16 bit character sets like Unicode.  About
170 different mapping tables between various known character sets and
Unicode is distributed with this package.  The source of these tables
is the vendor mapping tables provided by Unicode, Inc. and the code
tables in RFC 1345.  New maps can easily be installed.


%prep
%setup -q -n Unicode-Map8-%{version}
%patch0 -p0 -b .declaration
%patch1 -p0 -b .type

for i in README Changes; do
  iconv --from=ISO-8859-1 --to=UTF-8 $i > $i.UTF-8
  mv $i.UTF-8 $i
done


%build
CFLAGS="$RPM_OPT_FLAGS" %{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags} OPTIMIZE="$RPM_OPT_FLAGS"


%install
rm -rf $RPM_BUILD_ROOT
make install \
  PERL_INSTALL_ROOT=$RPM_BUILD_ROOT \
  INSTALLARCHLIB=$RPM_BUILD_ROOT%{perl_archlib}
find $RPM_BUILD_ROOT -type f -a \( -name perllocal.pod -o -name .packlist \
  -o \( -name '*.bs' -a -empty \) \) -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes README
%{_bindir}/umap
%{perl_vendorarch}/auto/Unicode
%{perl_vendorarch}/Unicode
%{_mandir}/man[13]/*.[13]*


%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.13-14
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.13-13
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.13-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.13-11
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.13-10
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.13-8
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.13-6
- Perl mass rebuild

* Fri Jul  8 2011 Paul Howarth <paul@city-fan.org> - 0.13-5
- Add perl(:MODULE_COMPAT_*) dependency

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.13-3
- Rebuild to fix problems with vendorarch/lib (#661697)

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.13-2
- Mass rebuild with perl-5.12.0

* Tue Jan 19 2010 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 0.13-1
- Update to 0.13.
- Convert ISO8858-1 files to UTF-8.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jun 05 2008 Aurelien Bompard <abompard@fedoraproject.org> 0.12-18
- fix build

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.12-17
- Rebuild for perl 5.10 (again)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.12-16
- Autorebuild for GCC 4.3

* Mon Jan 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.12-15
- rebuild for new perl

* Thu Sep 27 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.12-14
- fix license tag again (thanks Tom)

* Sun Aug 26 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.12-13
- fix license tag (like perl itself)

* Mon Aug 13 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.12-12
- BR: perl-devel

* Sun Oct 29 2006 Aurelien Bompard <abompard@fedoraproject.org> 0.12-11
- actually apply the patches

* Sat Oct 28 2006 Aurelien Bompard <abompard@fedoraproject.org> 0.12-10
- add patches for x86_64

* Wed Aug 30 2006 Aurelien Bompard <abompard@fedoraproject.org> 0.12-9
- rebuild

* Wed Feb 22 2006 Aurelien Bompard <gauret[AT]free.fr> 0.12-8
- ExcludeArch x86_64

* Wed Feb 22 2006 Aurelien Bompard <gauret[AT]free.fr> 0.12-7
- disable unit tests (map8.t fails on x86_64)

* Tue Feb 21 2006 Aurelien Bompard <gauret[AT]free.fr> 0.12-6
- rebuild for FC5

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Mon Feb  2 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.12-0.fdr.4
- Reduce directory ownership bloat.

* Sat Oct 11 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.12-0.fdr.3
- Install into vendor dirs.
- Specfile cleanup.

* Mon Jul  7 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.12-0.fdr.2
- Regenerate %%install section with cpanflute2.

* Wed May  7 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.12-0.fdr.1
- Update to current Fedora guidelines.

* Sun Mar  2 2003 Ville Skyttä <ville.skytta at iki.fi> - 0.12-1.fedora.1
- First Fedora release.
