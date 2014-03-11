Name:           perl-Compress-Bzip2
Version:        2.09
Release:        16%{?dist}
Summary:        Interface to Bzip2 compression library

Group:          Development/Libraries
License:        GPL+
URL:            http://search.cpan.org/dist/Compress-Bzip2/
Source0:        http://www.cpan.org/authors/id/A/AR/ARJAY/Compress-Bzip2-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  perl(Test::More)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  bzip2-devel
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
The Compress::Bzip2 module provides a Perl interface to the Bzip2
compression library.  A relevant subset of the functionality provided
by Bzip2 is available in Compress::Bzip2.


%prep
%setup -q -n Compress-Bzip2-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -empty -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc ANNOUNCE Changes COPYING NEWS README
%{perl_vendorarch}/Compress/
%{perl_vendorarch}/auto/Compress/
%{_mandir}/man3/*.3pm*


%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.09-16
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 2.09-15
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.09-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 16 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.09-13
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.09-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.09-11
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.09-10
- Mass rebuild with perl-5.12.0

* Fri Jan 15 2010 Stepan Kasal <skasal@redhat.com> - 2.09-9
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.09-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.09-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.09-6.2
Rebuild for new perl

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.09-5.2
- Autorebuild for GCC 4.3

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.09-4.2
- add BR: perl(Test::More)

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 2.09-4.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Thu Sep  7 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.09-4
- Rebuild for FC6.

* Mon Feb 20 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.09-3
- Rebuild for FC5 (perl 5.8.8).

* Mon Jan  9 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.09-2
- Applied two of the Ville's suggestions (#177166): trimmed down
  the description to the first paragraph and added the file ANNOUNCE
  as documentation.

* Thu Aug 11 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.09-1
- Update to 2.09.

* Mon May 02 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.07-1
- Update to 2.07.

* Mon Apr 25 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.04-1
- Update to 2.04.

* Sun Apr 24 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.03-1
- Update to 2.03.

* Sun Apr 24 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 2.00-1
- Update to 2.00.

* Thu Apr 21 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.03-1
- First build.
