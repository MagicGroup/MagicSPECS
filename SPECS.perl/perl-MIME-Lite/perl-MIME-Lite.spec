Name:           perl-MIME-Lite
Version:	3.030
Release:	2%{?dist}
Summary:        MIME::Lite - low-calorie MIME generator
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/MIME-Lite/
Source0:        http://www.cpan.org/authors/id/R/RJ/RJBS/MIME-Lite-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(lib)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Email::Date::Format)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Mail::Address)
BuildRequires:  perl(MIME::Types) >= 1.28
BuildRequires:  perl(Net::SMTP)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
# not detected by automated find-requires:
Requires:       perl(Email::Date::Format)
Requires:       perl(MIME::Types) >= 1.28

%description
MIME::Lite is intended as a simple, standalone module for generating (not 
parsing!) MIME messages... Specifically, it allows you to output a simple,
decent single- or multi-part message with text or binary attachments.  It does
not require that you have the Mail:: or MIME:: modules installed.

%prep
%setup -q -n MIME-Lite-%{version}
sed -i 's/\r//' examples/*
sed -i 's/\r//' contrib/*
sed -i 's/\r//' COPYING README
chmod a-x examples/* contrib/*

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -empty -exec rmdir ';'
magic_rpm_clean.sh

%check


%files
%doc changes.pod README examples contrib COPYING LICENSE
%exclude %{perl_vendorlib}/MIME/changes.pod
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 3.030-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 3.030-1
- 更新到 3.030

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 3.029-3
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 3.029-2
- 为 Magic 3.0 重建

* Wed Aug 22 2012 Petr Šabata <contyk@redhat.com> - 3.029-1
- 3.029 bump
- Fix deps, drop command macros
- Correct line-endings and file permissions

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.028-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Petr Pisar <ppisar@redhat.com> - 3.028-3
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.028-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 09 2011 Petr Sabata <contyk@redhat.com> - 3.028-1
- 3.028 bump
- Remove now obsolete BuildRoot and defattr

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 3.027-7
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.027-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 3.027-5
- 661697 rebuild for fixing problems with vendorach/lib

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 3.027-4
- Mass rebuild with perl-5.12.0

* Wed Jan 27 2010 Marcela Mašláňová <mmaslano@redhat.com> - 3.027-3
- make rpmlint happy 

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 3.027-2
- rebuild against perl 5.10.1

* Mon Nov  2 2009 Stepan Kasal <skasal@redhat.com> - 3.027-1
- new upstream version

* Wed Oct  7 2009 Stepan Kasal <skasal@redhat.com> - 3.26-2
- no need to search for *.bs files in noarch rpm

* Wed Oct  7 2009 Stepan Kasal <skasal@redhat.com> - 3.26-1
- new upstream version
- fix buildrequires
- add requires not detected automatically

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.01-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.01-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.01-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Sep  2 2008 Paul Howarth <paul@city-fan.org> 3.01-7
- fix FTBFS (#449558)

* Sat Feb  2 2008 Tom "spot" Callaway <tcallawa@redhat.com> 3.01-6
- rebuild for new perl

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> 3.01-5.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Sun Sep 10 2006 Mike McGrath <imlinux@gmail.com> 3.01-5
- Rebuild

* Thu Mar 30 2006 Mike McGrath <imlinux@gmail.com> 3.01-4
- New maintainer

* Thu Jun 23 2005 Ralf Corsepius <ralf@links2linux.de> 3.01-3
- Add %%{dist}.

* Wed Apr 06 2005 Hunter Matthews <thm@duke.edu> 3.01-2
- Review suggestions from José Pedro Oliveira

* Fri Mar 18 2005 Hunter Matthews <thm@duke.edu> 3.01-1
- Initial packageing.
