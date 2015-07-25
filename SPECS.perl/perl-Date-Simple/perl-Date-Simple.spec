Summary:	Simple date object for perl
Name:		perl-Date-Simple
Version:	3.03
Release:	14%{?dist}
License:	GPL+ or Artistic
Group:		Development/Libraries
Url:		http://search.cpan.org/dist/Date-Simple/
Source0:	http://search.cpan.org/CPAN/authors/id/I/IZ/IZUT/Date-Simple-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildRequires:	perl(Carp)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Test::More)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# Don't "provide" private Perl libs
%{?perl_default_filter}

%description
Simple date object for perl.

%prep
%setup -q -n Date-Simple-%{version}

# Spurious exec permissions in files from tarball
find lib -type f -exec chmod -c -x {} ';'
chmod -c -x ChangeLog COPYING README Simple.xs

# The NoXS.pm file provides a pure-perl alternative to the C implementation
# of the module. This results in duplicate "Provides:" entries, which rpmlint
# whinges about. This kludge removes the redundant file, which has the added
# benefit of shutting up rpmlint.
rm -f lib/Date/Simple/NoXS.pm
sed -i -e '/^lib\/Date\/Simple\/NoXS\.pm$/d' MANIFEST

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} ';' 2>/dev/null
%{_fixperms} %{buildroot}

%check


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING README
%{perl_vendorarch}/Date/
%{perl_vendorarch}/auto/Date/
%{_mandir}/man3/Date::Simple*.3pm*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 3.03-14
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 3.03-13
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 3.03-12
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 3.03-11
- 为 Magic 3.0 重建

* Wed Jan 11 2012 Paul Howarth <paul@city-fan.org> 3.03-10
- Spec file clean-up:
  - Nobody else likes macros for commands
  - Use %%{?perl_default_filter} rather than our own dep filter implementation
  - Use %%{_fixperms} macro rather than our own chmod incantation
  - Use DESTDIR rather than PERL_INSTALL_ROOT
  - BR: perl(Carp)

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> 3.03-9
- Perl mass rebuild

* Tue Feb  8 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 3.03-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> 3.03-7
- Rebuild to fix problems with vendorarch/lib (#661697)

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> 3.03-6
- Mass rebuild with perl 5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> 3.03-5
- Rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 3.03-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar  6 2009 Paul Howarth <paul@city-fan.org> 3.03-3
- Filter out unwanted provides for perl shared objects

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 3.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 22 2009 Paul Howarth <paul@city-fan.org> 3.03-1
- Update to 3.03
- Don't package Artistic license text, not included in upstream release
- New upstream maintainer -> new source URL

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> 3.02-9
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> 3.02-8
- Autorebuild for GCC 4.3

* Tue Jan 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> 3.02-7
- Rebuild for new perl

* Mon Aug 13 2007 Paul Howarth <paul@city-fan.org> 3.02-6
- Clarify license as GPL v1 or later, or Artistic (same as perl)
- Add buildreq perl(Test::More)

* Wed Apr 18 2007 Paul Howarth <paul@city-fan.org> 3.02-5
- Buildrequire perl(ExtUtils::MakeMaker)
- Fix argument order for find with -depth
- Fix permissions in debuginfo

* Tue Aug 29 2006 Paul Howarth <paul@city-fan.org> 3.02-4
- FE6 mass rebuild

* Thu Feb 16 2006 Paul Howarth <paul@city-fan.org> 3.02-3
- Don't use macros in command paths, hardcode them instead

* Tue Aug 23 2005 Paul Howarth <paul@city-fan.org> 3.02-2
- Point URLs at search.cpan.org instead of cpan.uwinnipeg.ca

* Tue Aug 23 2005 Paul Howarth <paul@city-fan.org> 3.02-1
- Initial package build
