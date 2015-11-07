Name:		perl-Jcode
Version:	2.07
Release:	12%{?dist}
Summary:	Perl extension interface for converting Japanese text
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Jcode/
Source0:	http://www.cpan.org/authors/id/D/DA/DANKOGAI/Jcode-%{version}.tar.gz
Patch0:		Jcode-2.07-UTF-8.patch
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildRequires:	perl(Carp)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(MIME::Base64)
BuildRequires:	perl(Test::More)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	perl(MIME::Base64)

%description
%{summary}.

%prep
%setup -q -n Jcode-%{version}

# Fix character encoding of pod file
%patch0 -p1

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} ';' 2>/dev/null
%{_fixperms} %{buildroot}

%check
LC_ALL=C 

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes* README
%{perl_vendorlib}/Jcode.pm
%dir %{perl_vendorlib}/Jcode/
%doc %{perl_vendorlib}/Jcode/Nihongo.pod
%{_mandir}/man3/Jcode.3pm*
%{_mandir}/man3/Jcode::Nihongo.3pm*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 2.07-12
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 2.07-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.07-10
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.07-9
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 2.07-8
- 为 Magic 3.0 重建

* Thu Jan 12 2012 Paul Howarth <paul@city-fan.org> 2.07-7
- Add buildreqs for perl core modules that might be dual-lived
- Nobody else likes macros for commands
- Use patch rather than scripted edit to fix encoding of Nihongo.pod

* Wed Jun 15 2011 Marcela Mašláňová <mmaslano@redhat.com> 2.07-6
- Perl mass rebuild

* Tue Feb  8 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 2.07-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> 2.07-4
- Rebuild to fix problems with vendorarch/lib (#661697)

* Sun May  2 2010 Marcela Maslanova <mmaslano@redhat.com> 2.07-3
- Mass rebuild with perl 5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> 2.07-2
- Rebuild against perl 5.10.1

* Mon Aug 24 2009 Paul Howarth <paul@city-fan.org> 2.07-1
- Update to 2.07 (fix mime_encode, CPAN RT#29049)
- Run test suite in "C" locale to support build on old distributions
- Fix argument order for find with -depth
- Encode manpages in UTF-8
- Include old Changes file too
- Mark POD file as %%doc
- Add explicit perl(MIME::Base64) dependency for MIME header support

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 2.06-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 2.06-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 2.06-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.06-6
- Rebuild for new perl

* Thu Sep 27 2007 Aurelien Bompard <abompard@fedoraproject.org> 2.06-5
- Fix license (thanks Tom)

* Sun Aug 26 2007 Aurelien Bompard <abompard@fedoraproject.org> 2.06-4
- Fix license tag (like perl itself)

* Mon Aug 13 2007 Aurelien Bompard <abompard@fedoraproject.org> 2.06-3
- BR perl-Test-Simple

* Mon Aug 13 2007 Aurelien Bompard <abompard@fedoraproject.org> 2.06-2
- BR perl-devel

* Wed Aug 30 2006 Aurelien Bompard <abompard@fedoraproject.org> 2.06-1
- Update to 2.06

* Tue Feb 21 2006 Aurelien Bompard <gauret[AT]free.fr> 2.03-3
- Rebuild for FC5

* Thu Oct 27 2005 Aurelien Bompard <gauret[AT]free.fr> 2.03-2
- Build as noarch (#171916)

* Sat Sep 03 2005 Aurelien Bompard <gauret[AT]free.fr> 2.03-1
- Update to 2.03
- Be closer to perl spec template

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- Rebuilt

* Sat Dec 04 2004 Aurelien Bompard <gauret[AT]free.fr> 0:0.88-0.fdr.1
- Update to 0.88

* Sun Jul 25 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.87-0.fdr.1
- Update to 0.87
- Require perl(:MODULE_COMPAT_*)

* Mon Jun 21 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.86-0.fdr.1
- Update to 0.86

* Sat Jun 19 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.85-0.fdr.1
- Update to 0.85
- Bring up to date with current fedora.us Perl spec template

* Mon Feb  2 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.83-0.fdr.4
- Reduce directory ownership bloat

* Sat Oct 11 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.83-0.fdr.3
- Install into vendor dirs
- Specfile cleanup

* Sun Jul  6 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.83-0.fdr.2
- Regenerate %%install section with cpanflute2, omit spurious *.pl

* Wed May  7 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.83-0.fdr.1
- Update to 0.83 and to current Fedora guidelines

* Sun Mar  2 2003 Ville Skyttä <ville.skytta at iki.fi> - 0.82-1.fedora.1
- First Fedora release
