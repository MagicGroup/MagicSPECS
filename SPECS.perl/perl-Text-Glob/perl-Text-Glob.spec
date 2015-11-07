Name: 		perl-Text-Glob
Version: 	0.09
Release: 	10%{?dist}
Summary: 	Perl module to match globbing patterns against text
License: 	GPL+ or Artistic
Group: 		Development/Libraries
URL: 		http://search.cpan.org/dist/Text-Glob/
Source0: 	http://www.cpan.org/authors/id/R/RC/RCLAMP/Text-Glob-%{version}.tar.gz

BuildArch: noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(constant)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Test::More)
Requires:  perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
Text::Glob implements glob(3) style matching that can be used to match
against text, rather than fetching names from a file-system.  If you
want to do full file globbing use the File::Glob module instead.

%prep
%setup -q -n Text-Glob-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check


%files
%doc Changes
%{perl_vendorlib}/Text
%{_mandir}/man3/*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.09-10
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.09-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.09-8
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.09-7
- 为 Magic 3.0 重建

* Fri Aug 10 2012 Jitka Plesnikova <jplesnik@redhat.com> - 0.09-6
- Update BRs and remove %%defattr.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 0.09-4
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.09-2
- Perl mass rebuild

* Wed Mar 02 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.09-1
- Upstream update.
- Spec cleanup.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.08-10
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.08-9
- Mass rebuild with perl-5.12.0

* Thu Feb 25 2010 Marcela Mašláňová <mmaslano@redhat.com> - 0.08-8
- add readme

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.08-7
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.08-4
- Rebuild for perl 5.10 (again)

* Fri Jan 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.08-3
- rebuild for new perl

* Sat Aug 18 2007 Ralf Corsépius <rc040203@freenet.de> - 0.08-2
- Update license tag.

* Tue May 08 2007 Ralf Corsépius <rc040203@freenet.de> - 0.08-1
- Upstream update.

* Tue Sep 05 2006 Ralf Corsépius <rc040203@freenet.de> - 0.07-2
- Mass rebuild.

* Thu Jul 20 2006 Ralf Corsépius <rc040203@freenet.de> - 0.07-1
- Upstream update.

* Tue Feb 28 2006 Ralf Corsépius <rc040203@freenet.de> - 0.06-4
- Rebuild for perl-5.8.8.

* Wed Aug 10 2005 Ralf Corsepius <ralf@links2linux.de> - 0.06-3
- Spec cleanup.

* Wed Aug 10 2005 Ralf Corsepius <ralf@links2linux.de> - 0.06-2
- FE resubmission.

* Fri Jul 01 2005 Ralf Corsepius <ralf@links2linux.de> - 0.06-1
- FE submission.
