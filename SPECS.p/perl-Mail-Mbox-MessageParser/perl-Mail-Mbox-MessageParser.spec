Summary:	A fast and simple mbox folder reader
Name:		perl-Mail-Mbox-MessageParser
Version:	1.5002
Release:	12%{?dist}
License:	GPL+
Group:		Development/Libraries
Url:		http://search.cpan.org/dist/Mail-Mbox-MessageParser/
Source0:	http://search.cpan.org/CPAN/authors/id/D/DC/DCOPPIT/Mail-Mbox-MessageParser-%{version}.tar.gz
Source1:	perl-module-version-filter
Patch0:		Mail-Mbox-MessageParser-1.5002-warning.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
BuildRequires:	grep, gzip, bzip2, /usr/bin/diff
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(FileHandle::Unget)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Text::Diff)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:	grep, gzip, bzip2, /usr/bin/diff

%description
Mail::Mbox::MessageParser is a feature-poor but very fast mbox parser. It uses
the best of three strategies for parsing a mailbox: either using cached folder
information, GNU grep, or highly optimized Perl.

%prep
%setup -q -n Mail-Mbox-MessageParser-%{version}

# Fix used-only-once warning that breaks grepmail with perl 5.12.0
%patch0 -p1

# Auto provides aren't clever enough for what Mail::Mbox::MessageParser does
%if 0%{?__perllib_provides:1}
%global provfilt /bin/sh -c "%{__perllib_provides} | perl -n -s %{SOURCE1} -lib=%{_builddir}/%{buildsubdir}/lib"
%define __perllib_provides %{provfilt}
%else
%global provfilt /bin/sh -c "%{__perl_provides} | perl -n -s %{SOURCE1} -lib=%{_builddir}/%{buildsubdir}/lib"
%define __perl_provides %{provfilt}
%endif

%build
perl Makefile.PL INSTALLDIRS=vendor \
	DIFF=/usr/bin/diff \
	BZIP=/usr/bin/bzip2 \
	BZIP2=/usr/bin/bzip2 \
	GREP=/bin/grep \
	GZIP=/bin/gzip \
	--default
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} ';' 2>/dev/null
%{_fixperms} %{buildroot}

%check


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README CHANGES anonymize_mailbox LICENSE
%{perl_vendorlib}/Mail/
%{_mandir}/man3/Mail::Mbox::MessageParser.3pm*
%{_mandir}/man3/Mail::Mbox::MessageParser::Cache.3pm*
%{_mandir}/man3/Mail::Mbox::MessageParser::Grep.3pm*
%{_mandir}/man3/Mail::Mbox::MessageParser::MetaInfo.3pm*
%{_mandir}/man3/Mail::Mbox::MessageParser::Perl.3pm*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.5002-12
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.5002-11
- 为 Magic 3.0 重建

* Sat Jan  7 2012 Paul Howarth <paul@city-fan.org> - 1.5002-10
- Fedora 17 Mass Rebuild

* Tue Jun 28 2011 Paul Howarth <paul@city-fan.org> - 1.5002-9
- Fix provides filter to work with rpm 4.9 onwards
- Nobody else likes macros for commands

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.5002-8
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5002-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.5002-6
- Rebuild to fix problems with vendorarch/lib (#661697)

* Tue Jun  1 2010 Paul Howarth <paul@city-fan.org> 1.5002-5
- Fix used-only-once warning that breaks grepmail with perl 5.12.0

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.5002-4
- Mass rebuild with perl-5.12.0

* Fri Feb 19 2010 Paul Howarth <paul@city-fan.org> 1.5002-3
- Fix versioned provides for perl modules
- Use %%{_fixperms} macro instead of our own %%{__chmod} incantation

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> 1.5002-2
- Rebuild against perl 5.10.1

* Wed Sep  2 2009 Paul Howarth <paul@city-fan.org> 1.5002-1 
- Update to 1.5002 
  - perl 5.10 patch upstreamed 
  - disable the grep interface, known to be buggy 
  - fix infinite loop in emails of less than 200 characters (CPAN RT#33493) 
  - update Makefile.PL for versions of Module::Install > 0.88 
  - instead of returning an error for an empty mailbox, a valid mailbox is 
    returned that immediately fails the end_of_mailbox check (CPAN RT#43665) 
  - fix missing "m" modifier issue exposed by Perl 5.10 (CPAN RT#33004) 
  - added some debugging information for the "cache data not validated" error 
  - fix an off-by-one error that could cause warnings about undefined values 
- BuildRequire perl(Test::More) and perl(Text::Diff) 

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5000-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5000-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Nov 20 2008 Paul Howarth <paul@city-fan.org> 1.5000-6
- Project upstream has moved from Sourceforge to Google Code but Google Code
  site is content-free so use standard CPAN URLs instead

* Sat Feb  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.5000-5
- Fix for perl 5.10 (Andreas König)

* Thu Feb  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.5000-4
- Rebuild for new perl

* Mon Aug 13 2007 Paul Howarth <paul@city-fan.org> 1.5000-3
- Clarify license as GPL (unspecified version)

* Thu Mar  8 2007 Paul Howarth <paul@city-fan.org> 1.5000-2
- Buildrequire perl(ExtUtils::MakeMaker)

* Tue Feb 27 2007 Paul Howarth <paul@city-fan.org> 1.5000-1
- Update to 1.5000
- Fix argument order for find with -depth
- Permission fixes no longer needed in %%prep
- Buildreq various utils for running test suite

* Fri Aug 25 2006 Paul Howarth <paul@city-fan.org> 1.4005-1
- Update to 1.4005

* Wed Jul 12 2006 Paul Howarth <paul@city-fan.org> 1.4004-1
- Update to 1.4004

* Mon May 22 2006 Paul Howarth <paul@city-fan.org> 1.4003-1
- Update to 1.4003

* Thu Feb 16 2006 Paul Howarth <paul@city-fan.org> 1.4002-2
- Rebuild

* Fri Feb 10 2006 Paul Howarth <paul@city-fan.org> 1.4002-1
- Update to 1.4002
- Don't use macros in build-time command paths, hardcode them instead
- Add dependency on /usr/bin/diff
- Tzip support removed upstream

* Wed Oct 12 2005 Paul Howarth <paul@city-fan.org> 1.4001-1
- Fedora Extras submission
