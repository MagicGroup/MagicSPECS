Name:           perl-XML-Dumper
Version:        0.81
Release:        14%{dist}
Summary:        Perl module for dumping Perl objects from/to XML

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/XML-Dumper/
Source0:        http://www.cpan.org/authors/id/M/MI/MIKEWONG/XML-Dumper-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(XML::Parser) >= 2.30-7
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
Requires:       perl(XML::Parser) >= 2.30-7
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))


%description
XML::Dumper dumps Perl data to XML format. XML::Dumper can also read
XML data that was previously dumped by the module and convert it back
to Perl.  Perl objects are blessed back to their original packaging;
if the modules are installed on the system where the perl objects are
reconstituted from xml, they will behave as expected. Intuitively, if
the perl objects are converted and reconstituted in the same
environment, all should be well.


%prep
%setup -q -n XML-Dumper-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

for file in README; do
  iconv -f iso-8859-1 -t utf-8 < "$file" > "${file}_"
  mv -f "${file}_" "$file"
done


%check



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/XML/
%{_mandir}/man3/*.3*


%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.81-14
- 为 Magic 3.0 重建

* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.81-13
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.81-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.81-11
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.81-10
- 为 Magic 3.0 重建

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.81-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 15 2010 Marcela Mašláňová <mmaslano@redhat.com> - 0.81-8
- add missing requirement

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.81-7
- Mass rebuild with perl-5.12.0

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.81-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.81-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.81-4
- rebuild for new perl

* Thu Oct 25 2007 Robin Norwood <rnorwood@redhat.com> - 0.81-3
- fix various issues from package review:
- remove || : from %%check
- remove tabs and fix spacing
- fix encoding for README file

* Wed Oct 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.81-2.2
- add BR: perl(Test::More)

* Wed Oct 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.81-2.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.81-2
- rebuild

* Wed Apr 12 2006 Jason Vas Dias <jvdias@redhat.com> - 0.81-1
- upgrade to 0.81

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 0.79-1.2
- rebuild for new perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Sun Nov 06 2005 Florian La Roche <laroche@redhat.com>
- 0.79

* Tue Apr 26 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.71-4
- Specfile rewrite, fixes License, dir ownerships and dependencies (#112593).

* Wed Mar 30 2005 Warren Togami <wtogami@redhat.com>
- remove brp-compress

* Wed Sep 22 2004 Chip Turner <cturner@redhat.com> 0.71-2
- rebuild

* Fri Feb 13 2004 Chip Turner <cturner@redhat.com> 0.71-1
- update to 0.71

* Tue Aug  6 2002 Chip Turner <cturner@redhat.com>
- automated release bump and build

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Jul 23 2001 Crutcher Dunnavant <crutcher@redhat.com> 2.30-5
- got it to work.

* Thu Jul 18 2001 Crutcher Dunnavant <crutcher@redhat.com> 2.30-4
- imported from mandrake. tweaked man path.

* Thu Jun 21 2001 Christian Belisle <cbelisle@mandrakesoft.com> 0.4-3mdk
- Fixed an error in changelog.

* Thu Jun 21 2001 Christian Belisle <cbelisle@mandrakesoft.com> 0.4-2mdk
- Clean up spec.
- Fixed distribution tag.
- Needed by eGrail.

* Mon Jun 18 2001 Till Kamppeter <till@mandrakesoft.com> 0.4-1mdk
- Newly introduced for Foomatic.
