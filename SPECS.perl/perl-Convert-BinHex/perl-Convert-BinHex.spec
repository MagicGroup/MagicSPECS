Name:		perl-Convert-BinHex
Version:	1.119
Release:	21%{?dist}
Summary:	Convert to/from RFC1741 HQX7 (Mac BinHex)
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/Convert-BinHex/
Source0:	http://search.cpan.org/CPAN/authors/id/E/ER/ERYQ/Convert-BinHex-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
BuildRequires:	perl(Carp)
BuildRequires:	perl(ExtUtils::MakeMaker)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
Convert::BinHex extracts data from Macintosh BinHex files.

%prep
%setup -q -n Convert-BinHex-%{version}
chmod -c -x bin/*.pl docs/Convert/BinHex/redapple.gif
cp -a bin examples
perl -pi -e 's/^use lib .*$//' bin/*.pl
perl -pi -e 's/^(\@ISA.*)/require Exporter; $1/' t/Checker.pm

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} ';' 2>/dev/null
%{_fixperms} %{buildroot}

%check


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING README docs examples
%{perl_vendorlib}/Convert/
%{_mandir}/man3/Convert::BinHex.3pm*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.119-21
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.119-20
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.119-19
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.119-18
- 为 Magic 3.0 重建

* Tue Jan 10 2012 Paul Howarth <paul@city-fan.org> 1.119-17
- nobody else likes macros for commands
- BR: perl(Carp)

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> 1.119-16
- perl mass rebuild

* Tue Feb  8 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1.119-15
- rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> 1.119-14
- rebuild to fix problems with vendorarch/lib (#661697)

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> 1.119-13
- mass rebuild with perl-5.12.0

* Thu Jan 14 2010 Paul Howarth <paul@city-fan.org> 1.119-12
- minor spec issues from merge review (#552554)

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> 1.119-11
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1.119-10
- rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 1.119-9
- rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.119-8
- rebuild for perl 5.10 (again)

* Mon Jan 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.119-7
- rebuild for new perl

* Sat Aug 11 2007 Paul Howarth <paul@city-fan.org> 1.119-6
- clarify license as GPL version 1 or later, or Artistic (same as perl)

* Thu Mar  8 2007 Paul Howarth <paul@city-fan.org> 1.119-5
- add perl(ExtUtils::MakeMaker) buildreq
- use tabs rather than spaces

* Sun Sep 17 2006 Paul Howarth <paul@city-fan.org> 1.119-4
- add dist tag
- fix argument order in find command with -depth

* Tue Aug 29 2006 Paul Howarth <paul@city-fan.org> 1.119-3
- use full paths for all commands used in build
- use search.cpan.org download URL
- assume rpm knows about %%check and %%{perl_vendorlib}
- cosmetic spec file changes

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 1.119-2
- rebuilt

* Wed Sep 15 2004 Ville Skyttä <ville.skytta at iki.fi> 1.119-1
- first build
