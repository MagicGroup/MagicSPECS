Name:           perl-File-Tail
Version:	1.3
Release:	3%{?dist}
Summary:        Perl extension for reading from continously updated files

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/File-Tail/
Source0:        http://www.cpan.org/authors/id/M/MG/MGRABNAR/File-Tail-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(Time::HiRes)
BuildRequires:  perl(ExtUtils::MakeMaker)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
The primary purpose of File::Tail is reading and analysing log files
while they are being written, which is especially useful if you are
monitoring the logging process with a tool like Tobias Oetiker's MRTG.

%prep
%setup -q -n File-Tail-%{version}


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



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/File/
%{_mandir}/man3/File::Tail.3*


%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.3-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.3-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.3-1
- 更新到 1.3

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.99.3-23
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.99.3-22
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.99.3-21
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.99.3-20
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.99.3-19
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.99.3-18
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.99.3-17
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.99.3-16
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.99.3-15
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.99.3-13
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.99.3-11
- 661697 rebuild for fixing problems with vendorach/lib

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.99.3-10
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.99.3-9
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.99.3-6
- rebuild for new perl

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.99.3-5.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Fri Jun  9 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.99.3-5
- Added the requirement perl(:MODULE_COMPAT_x.x.x).

* Mon Feb 20 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.99.3-4
- Rebuild for FC5 (perl 5.8.8).

* Fri Jan  6 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.99.3-3
- Another typo corrected.

* Wed Jan  4 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.99.3-2
- Correction of spelling error in the description.

* Thu Sep 15 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.99.3-1
- 0.99.3.
- Specfile cleanups.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.98-4
- rebuilt

* Sun Feb  8 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.98-0.fdr.3
- BuildRequire Time::HiRes (bug 731).
- Run tests in the %%check section.
- Reduce directory ownership bloat.

* Mon Nov 17 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.98-0.fdr.2
- Specfile rewrite.

* Tue Sep 17 2003 Warren Togami <warren@togami.com> - 0.98-0.fdr.1
- Specfile autogenerated.
