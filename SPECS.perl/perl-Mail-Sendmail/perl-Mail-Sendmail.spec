Name:           perl-Mail-Sendmail
Version:	0.79_16
Release:	3%{?dist}
Summary:        Simple platform independent mailer for Perl

License:        Copyright only
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Mail-Sendmail/
Source0:        http://www.cpan.org/authors/id/M/MI/MIVKOVIC/Mail-Sendmail-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
# Not picked up automatically.
Requires:       perl(MIME::QuotedPrint)

%description
Mail::Sendmail is a simple platform independent library for sending
e-mail from your perl script.  It only requires Perl 5 and a network
connection.  Mail::Sendmail contains mainly &sendmail, which takes a
hash with the message to send and sends it. It is intended to be very
easy to setup and use.


%prep
%setup -q -n Mail-Sendmail-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check
# We don't want to send the test mail -> no 


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes README Sendmail.html Todo
%{perl_vendorlib}/Mail/
%{_mandir}/man3/*.3pm*


%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.79_16-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.79_16-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.79_16-1
- 更新到 0.79_16

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.79-22
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.79-21
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.79-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.79-19
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.79-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 16 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.79-17
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.79-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.79-15
- 661697 rebuild for fixing problems with vendorach/lib

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.79-14
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.79-13
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.79-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.79-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.79-10
- rebuild for new perl

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.79-9.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Fri Sep  8 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.79-9
- Rebuild for FC6.

* Fri Feb 17 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.79-8
- Rebuild for FC5 (perl 5.8.8).
- Dist tag and specfile cleanup.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.79-7
- rebuilt

* Thu Dec 16 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.79-6
- Sync with fedora-rpmdevtools' Perl spec template to fix x86_64 build.

* Tue Jan 13 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.79-0.fdr.5
- Fix License and %%description (#65).

* Wed Oct 29 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.79-0.fdr.4
- Specfile cleanup.

* Sun Aug 31 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.79-0.fdr.3
- Install into vendor dirs.

* Sun May  4 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.79-0.fdr.2
- Own more dirs.
- Save .spec in UTF-8.

* Sat Mar 22 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.79-0.fdr.1
- Update to current Fedora guidelines.

* Sun Feb  9 2003 Ville Skyttä <ville.skytta at iki.fi> - 0.79-1.fedora.1
- First Fedora release.
