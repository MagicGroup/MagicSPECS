Name:           perl-XML-Writer
Version:        0.612
Release:        5%{?dist}
Summary:        A simple Perl module for writing XML documents

Group:          Development/Libraries
License:        MIT
URL:            http://search.cpan.org/dist/XML-Writer/
Source0:        http://www.cpan.org/authors/id/J/JO/JOSEPHW/XML-Writer-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  perl(Carp)
BuildRequires:  perl(Encode)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(ExtUtils::MakeMaker)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
XML::Writer is a simple Perl module for writing XML documents: it
takes care of constructing markup and escaping data correctly, and by
default, it also performs a significant amount of well-formedness
checking on the output, to make certain (for example) that start and
end tags match, that there is exactly one document element, and that
there are not duplicate attribute names.


%prep
%setup -q -n XML-Writer-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags} 


%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -a \( -name .packlist \
  -o \( -name '*.bs' -a -empty \) \) -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'


%check
make test


%files
%doc Changes README TODO LICENSE
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%changelog
* Fri Aug 17 2012 Jitka Plesnikova <jplesnik@redhat.com> - 0.612-5
- Specify all dependencies.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.612-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.612-3
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.612-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct  2 2011 Tom Callaway <spot@fedoraproject.org> - 0.612-1
- update to 0.612

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.606-9
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.606-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.606-7
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.606-6
- Mass rebuild with perl-5.12.0

* Wed Feb 25 2010 Marcela Mašláňová <mmaslano@redhat.com> - 0.606-6
- make rpmlint happy

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.606-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.606-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.606-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb  2 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.606-1
- Update to upstream 0.606
- Clarify license is MIT

* Tue Mar 18 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.604-1
- New upstream release (0.604)

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.603-4
- Rebuild for perl 5.10 (again)

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.603-3
- rebuild for new perl

* Thu Aug 23 2007 Alex Lancaster <alexl@users.sourceforge.net> 0.603-2
- License tag to "GPL+ or Artistic" as per new guidelines.

* Sat Aug 18 2007 Alex Lancaster <alexl@users.sourceforge.net> 0.603-1
- Update to latest upstream

* Mon Mar 26 2007 Alex Lancaster <alexl@users.sourceforge.net> 0.602-3
- Fixed %check

* Wed Mar 23 2007 Alex Lancaster <alexl@users.sourceforge.net> 0.602-2
- Update BR as per suggestions from review by Ralf Corsepius

* Wed Mar 23 2007 Alex Lancaster <alexl@users.sourceforge.net> 0.602-1
- Update to 0.602

* Wed Apr 06 2005 Hunter Matthews <thm@duke.edu> 0.531-1
- Review suggestions from José Pedro Oliveira

* Tue Mar 22 2005 Hunter Matthews <thm@duke.edu> 0.531-1
- Initial build.
