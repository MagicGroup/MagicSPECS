Summary: Line wrapping with support for several locale setups
Name: perl-Text-WrapI18N
Version: 0.06
Release: 22%{?dist}
License: GPL+ or Artistic
Group: Development/Libraries
URL: http://search.cpan.org/dist/Text-WrapI18N/
Source0: http://search.cpan.org/CPAN/authors/id/K/KU/KUBOTA/Text-WrapI18N-%{version}.tar.gz
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: perl(Exporter)
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(Test::Simple)
BuildRequires: perl(Text::CharWidth) >= 0.02
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires: perl(Text::CharWidth) >= 0.02

%description
This is a module which intends to substitute Text::Wrap,
which supports internationalized texts including:
 - multi-byte encodings such as UTF-8, EUC-JP, EUC-KR, GB2312, and Big5,
 - full width characters like east Asian characters which appear in
   UTF-8, EUC-JP, EUC-KR, GB2312, Big5, and so on,
 - combining characters like diacritical marks which appear in UTF-8,
   ISO-8859-11 (aka TIS-620), and so on, and
 - languages which don't use white spaces between words, like Chinese
   and Japanese.

%prep
%setup -q -n Text-WrapI18N-%{version}

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
%{perl_vendorlib}/Text
%{_mandir}/man3/Text::WrapI18N.3pm*

%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.06-22
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.06-21
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.06-20
- 为 Magic 3.0 重建

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 0.06-18
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 23 2012 Jitka Plesnikova <jplesnik@redhat.com> - 0.06-16
- Update dependencies and description

* Mon Oct 29 2012 Jitka Plesnikova <jplesnik@redhat.com> - 0.06-15
- Add BR perl(Exporter)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.06-13
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.06-11
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.06-9
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.06-8
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.06-7
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Aug 24 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.06-4
- %%check || : does not work anymore.

* Wed Oct 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.06-2.2
- add BR: perl(Test::Simple)

* Wed Oct 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.06-2.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Sat Dec 30 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.06-2
- Add ownership of some perl folders.

* Thu Dec 28 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.06-1
- Initial build.

