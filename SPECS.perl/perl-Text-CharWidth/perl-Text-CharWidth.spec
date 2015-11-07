Summary: Get number of occupied columns of a string on terminal
Name: perl-Text-CharWidth
Version: 0.04
Release: 22%{?dist}
License: GPL+ or Artistic
Group: Development/Libraries
URL: http://search.cpan.org/dist/Text-CharWidth/
Source0: http://search.cpan.org/CPAN/authors/id/K/KU/KUBOTA/Text-CharWidth-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: perl(Exporter)
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(Test::Simple)
BuildRequires: perl(XSLoader)
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
This is a module to provide equivalent feature as wcwidth(3) and
wcswidth(3).  This also provides mblen(3) equivalent subroutine.

%prep
%setup -q -n Text-CharWidth-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
find %{buildroot} -type f \( -name .packlist -or -name perllocal.pod \
  -or \( -name '*.bs' -a -empty \) \) -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} \;
chmod -R u+w %{buildroot}

%check
make test

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc README Changes
%{perl_vendorarch}/Text
%{perl_vendorarch}/auto/Text
%{_mandir}/man3/Text::CharWidth.3pm*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.04-22
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.04-21
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.04-20
- 为 Magic 3.0 重建

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.04-18
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Oct 26 2012 Jitka Plesnikova <jplesnik@redhat.com> - 0.04-16
- Specify all dependencies.
- Add default filter.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.04-14
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.04-12
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.04-10
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.04-9
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.04-8
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Aug 24 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.04-5
- %%check || : does not work anymore.

* Wed Oct 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.04-2.2
- add BR: perl(Test::Simple)

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.04-2.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Sat Dec 30 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.04-2
- Add ownership of some perl folders.

* Thu Dec 28 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.04-1
- Initial build.

