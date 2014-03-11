Name: 		perl-Date-Pcalc
Version:	6.1
Release:	4%{?dist}
Summary:	Gregorian calendar date calculations
License:	GPL+ or Artistic
Group:		Development/Libraries
URL: 		http://search.cpan.org/dist/Date-Pcalc/
Source0: 	http://search.cpan.org/CPAN/authors/id/S/ST/STBEY/Date-Pcalc-%{version}.tar.gz

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildRequires:  %{_bindir}/iconv
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Bit::Vector) >= 7.1
BuildRequires:  perl(Carp::Clan) >= 5.3

%description
This package consists of a Perl module for all kinds of date calculations based
on the Gregorian calendar (the one used in all western countries today), 
thereby complying with all relevant norms and standards: ISO/R 2015-1971, 
DIN 1355 and, to some extent, ISO 8601 (where applicable).

%prep
%setup -q -n Date-Pcalc-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
%{_bindir}/iconv --from-code=ISO-8859-1 --to-code=UTF-8 blib/man3/Date::Pcalc.3pm -o blib/man3/Date::Pcalc.3pm-utf8
mv blib/man3/Date::Pcalc.3pm-utf8 blib/man3/Date::Pcalc.3pm 
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check


# Interactive build, prompts if binary of PP version should be built
# Defaults to binary if gcc is found (default Fedora buildroot contains gcc)
# There's No option available to specify explicitly
%files
%defattr(-,root,root,-)
%doc CHANGES.txt README.txt EXAMPLES.txt CREDITS.txt GNU_GPL.txt Artistic.txt
%{perl_vendorarch}/auto/Date
%{perl_vendorarch}/Date
%{_mandir}/man3/*

%changelog
* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 6.1-4
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 6.1-2
- Perl mass rebuild

* Tue Apr 05 2011 Petr Sabata <psabata@redhat.com> - 6.1-1
- 6.1 bump
- Removing obsolete Buildroot stuff

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.2-10
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.2-9
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.2-8
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.2-5.1
Rebuild for new perl

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.2-4.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Thu Sep 07 2006 Mike McGrath <imlinux@gmail.com> - 1.2-4
- Release bump

* Mon Mar 20 2006 Mike McGrath <imlinux@gmail.com> - 1.2-3
- Minor fixes and formatting in spec file

* Sun Mar 19 2006 Mike McGrath <imlinux@gmail.com> - 1.2-2
- Include license and credits
- Convert manpage to utf-8

* Sat Mar 18 2006 Mike McGrath <imlinux@gmail.com> - 1.2-1
- First attempt at a Fedora friendly spec file
