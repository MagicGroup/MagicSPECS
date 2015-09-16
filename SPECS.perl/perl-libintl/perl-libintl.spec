Summary: Internationalization library for Perl, compatible with gettext
Name: perl-libintl
Version:	1.24
Release:	1%{?dist}
License: LGPLv2+
Group: Development/Libraries
URL: http://search.cpan.org/dist/libintl-perl/
Source: http://search.cpan.org/CPAN/authors/id/G/GU/GUIDO/libintl-perl-%{version}.tar.gz
Requires: perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Provides: perl-libintl-perl = %{version}-%{release}
BuildRequires: perl(ExtUtils::MakeMaker)
# Run-time:
BuildRequires: perl(base)
BuildRequires: perl(Carp)
BuildRequires: perl(constant)
BuildRequires: perl(Cwd)
BuildRequires: perl(Encode)
BuildRequires: perl(Encode::Alias)
BuildRequires: perl(Exporter)
BuildRequires: perl(IO::Handle)
# Tests:
BuildRequires: perl(File::Spec)
BuildRequires: perl(Test)
BuildRequires: perl(Test::Harness)

%{?perl_default_filter}

%description
The package libintl-perl is an internationalization library for Perl that
aims to be compatible with the Uniforum message translations system as
implemented for example in GNU gettext.


%prep
%setup -q -n libintl-perl-%{version}
find -type f -exec chmod -x {} \;
find lib/Locale gettext_xs \( -name '*.pm' -o -name '*.pod' \) \
    -exec sed -i -e '/^#! \/bin\/false/d' {} \;

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f \( -name .packlist -o \
			-name '*.bs' -size 0 \) -exec rm -f {} ';'
chmod -R u+w %{buildroot}/*

%check
make test

%files
%doc ChangeLog COPYING* NEWS README THANKS TODO
%{perl_vendorlib}/Locale/
%{perl_vendorarch}/auto/Locale/
%{_mandir}/man?/*

%changelog
* Wed Sep 16 2015 Liu Di <liudidi@gmail.com> - 1.24-1
- 更新到 1.24

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.20-14
- 为 Magic 3.0 重建

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.20-12
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 20 2012 Petr Šabata <contyk@redhat.com> - 1.20-10
- Add some missing BRs
- Modernize the spec
- Drop command macros

* Thu Oct 11 2012 Petr Pisar <ppisar@redhat.com> - 1.20-9
- Do not provide private library
- Drop unneeded build-time dependencies
- Specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.20-7
- Perl 5.16 rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.20-5
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.20-3
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.20-2
- Mass rebuild with perl-5.12.0

* Fri Jan 15 2010 Stepan Kasal <skasal@redhat.com> - 1.20-1
- new upstream version
- better buildroot

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.16-11
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.16-8
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.16-7
- Autorebuild for GCC 4.3

* Tue Feb  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.16-6
- rebuild for new perl

* Wed Aug 22 2007 Matthias Saou <http://freshrpms.net/> 1.16-5
- Rebuild for new BuildID feature.

* Mon Aug  6 2007 Matthias Saou <http://freshrpms.net/> 1.16-4
- Update License field.
- Add perl(ExtUtils::MakeMaker) build requirement.

* Mon Aug 28 2006 Matthias Saou <http://freshrpms.net/> 1.16-3
- FC6 rebuild.
- Change spec file back to my own liking...

* Sat Feb 11 2006 Ralf Corsépius <rc040203@freenet.de>  1.16-2
- Rework spec (PR 180767).

* Thu Feb  9 2006 Matthias Saou <http://freshrpms.net/> 1.16-1
- Update to 1.16.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Tue Nov  9 2004 Matthias Saou <http://freshrpms.net/> 1.11-2
- Fix : Added perl(Locale::gettext_xs) provides.

* Thu Nov  4 2004 Matthias Saou <http://freshrpms.net/> 1.11-1
- Initial RPM release.
