Name:           perl-Math-Round
Version:        0.06
Release:        15%{?dist}
Summary:        Perl extension for rounding numbers
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Math-Round
Source0:        http://search.cpan.org/CPAN/authors/id/G/GR/GROMMEL/Math-Round-%{version}.tar.gz
Patch0:         Math-Round-0.06-utf8.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:      noarch
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(POSIX)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
Math::Round supplies functions that will round numbers in different ways. The
functions round and nearest are exported by default; others are available as
described below. "use ... qw(:all)" exports all functions.

%prep
%setup -q -n Math-Round-%{version}

# Recode docs as UTF-8
%patch0 -p1

# remove errant execute bits
find . -type f -exec chmod -c -x {} ';'

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'
%{_fixperms} %{buildroot}

%check


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/auto/Math/
%{perl_vendorlib}/Math/
%{_mandir}/man3/Math::Round.3pm*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.06-15
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.06-13
- Perl 5.16 rebuild

* Fri Jan 20 2012 Paul Howarth <paul@city-fan.org> - 0.06-12
- BR: perl(Exporter) and perl(POSIX)
- Make %%files list more specific
- Don't use macros for commands
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Recode README as UTF-8

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.06-10
- Perl mass rebuild

* Tue Jun 14 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.06-9
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.06-7
- Rebuild to fix problems with vendorarch/lib (#661697)

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.06-6
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.06-5
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.06-2
- rebuild for new perl

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.06-1.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Tue Dec 05 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.06-1
- update to 0.06
- minor spec file tweaks

* Thu Aug 31 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.05-2
- bump for mass rebuild

* Mon Jul  3 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.05-1
- bump for F-E release

* Thu Jun 29 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.05-0
- Initial spec file for F-E
