Summary:	I/O on in-core objects like strings and arrays for Perl
Name:		perl-IO-stringy
Version:	2.110
Release:	22%{?dist}
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/IO-stringy/
Source0:	http://search.cpan.org/CPAN/authors/id/D/DS/DSKOLL/IO-stringy-%{version}.tar.gz
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildRequires:	perl(Carp)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(FileHandle)
BuildRequires:	perl(IO::File)
BuildRequires:	perl(IO::Handle)
BuildRequires:	perl(Symbol)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This toolkit primarily provides modules for performing both traditional
and object-oriented I/O) on things *other* than normal filehandles; in
particular, IO::Scalar, IO::ScalarArray, and IO::Lines.

In the more-traditional IO::Handle front, we have IO::AtomicFile, which
may be used to painlessly create files that are updated atomically.

And in the "this-may-prove-useful" corner, we have IO::Wrap, whose
exported wraphandle() function will clothe anything that's not a blessed
object in an IO::Handle-like wrapper... so you can just use OO syntax
and stop worrying about whether your function's caller handed you a
string, a globref, or a FileHandle.

%prep
%setup -q -n IO-stringy-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check


%clean
rm -rf %{buildroot}

%files
%doc README COPYING examples
%{perl_vendorlib}/IO/
%{_mandir}/man3/IO::AtomicFile.3pm*
%{_mandir}/man3/IO::InnerFile.3pm*
%{_mandir}/man3/IO::Lines.3pm*
%{_mandir}/man3/IO::Scalar.3pm*
%{_mandir}/man3/IO::ScalarArray.3pm*
%{_mandir}/man3/IO::Stringy.3pm*
%{_mandir}/man3/IO::Wrap.3pm*
%{_mandir}/man3/IO::WrapTie.3pm*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.110-22
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.110-21
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.110-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 2.110-19
- Perl 5.16 rebuild

* Fri Apr  6 2012 Paul Howarth <paul@city-fan.org> 2.110-18
- don't build-require modules that this package provides (problem stupidly
  introduced in previous release)
- don't need to remove empty directories from buildroot
- drop %%defattr, redundant since rpm 4.4

* Thu Jan 12 2012 Paul Howarth <paul@city-fan.org> 2.110-17
- spec clean-up:
  - nobody else likes macros for commands
  - use DESTDIR rather than PERL_INSTALL_ROOT
  - add buildreqs for core perl modules, which may be dual-lived

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> 2.110-16
- perl mass rebuild

* Tue Feb  8 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 2.110-15
- rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> 2.110-14
- rebuild to fix problems with vendorarch/lib (#661697)

* Sun May  2 2010 Marcela Maslanova <mmaslano@redhat.com> 2.110-13
- mass rebuild with perl-5.12.0

* Fri Jan 15 2010 Paul Howarth <paul@city-fan.org> 2.110-12
- spec cleanups (see also merge review #552564)

* Sun Dec 20 2009 Robert Scheck <robert@fedoraproject.org> 2.110-11
- rebuilt against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 2.110-10
- rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 2.110-9
- rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.110-8
- rebuild for perl 5.10 (again)

* Tue Jan 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.110-7
- rebuild for new perl

* Mon Aug 13 2007 Paul Howarth <paul@city-fan.org> 2.110-6
- clarify license as GPL v1 or later, or Artistic (same as perl)

* Wed Apr 18 2007 Paul Howarth <paul@city-fan.org> 2.110-5
- buildrequire perl(ExtUtils::MakeMaker)

* Sun Sep 17 2006 Paul Howarth <paul@city-fan.org> 2.110-4
- add dist tag
- fix argument order in find command with -depth

* Tue Aug 29 2006 Paul Howarth <paul@city-fan.org> 2.110-3
- use search.cpan.org download URL
- use full paths for all commands used in build
- assume rpm knows about %%check and %%{perl_vendorlib}
- cosmetic spec file changes

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Tue Feb 15 2005 Ville Skyttä <ville.skytta at iki.fi> 2.110-1
- 2.110
- some specfile cleanups, bringing it closer to spectemplate-perl.spec

* Wed Dec 31 2003 Ville Skyttä <ville.skytta at iki.fi> 2.109-0.fdr.1
- update to 2.109

* Thu Oct  2 2003 Michael Schwendt <rh0212ms[AT]arcor.de> 2.108-0.fdr.4
- package is now using vendor directories

* Sat Aug 16 2003 Dams <anvil[AT]livna.org> 2.108-0.fdr.3
- package is now noarch
- rm-ing perllocal.pod instead of excluding it

* Fri Jul 11 2003 Dams <anvil[AT]livna.org> 2.108-0.fdr.2
- changed Group tag value
- "" in build section
- added missing directory

* Sun Jun 15 2003 Dams <anvil[AT]livna.org> 2.108-0.fdr.1
- initial build
