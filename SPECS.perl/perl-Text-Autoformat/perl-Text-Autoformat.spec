Name:           perl-Text-Autoformat
# Maintain six-digit version number to ensure clean upgrade path
%global cpan_version 1.72
Version:	%{cpan_version}0000
Release:	2%{?dist}
Summary:        Automatic text wrapping and reformatting
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Text-Autoformat/
Source0:        http://www.cpan.org/authors/id/N/NE/NEILB/Text-Autoformat-%{cpan_version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Runtime
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(overload)
BuildRequires:  perl(Text::Reform) >= 1.11
BuildRequires:  perl(Text::Tabs)
BuildRequires:  perl(vars)
# Tests only
BuildRequires:  perl(Test::More)
BuildRequires:  perl(utf8)
Requires:       perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))

# Do not export private modules
%global __provides_exclude %{?__provides_exclude|%__provides_exclude|}^perl\\((Hang|NullHang)\\)

%description
Text::Autoformat provides intelligent formatting of plain text without the
need for any kind of embe%description -l zh_CN.UTF-8ed mark-up. The module recognizes Internet
quoting conventions, a wide range of bulleting and number schemes, centered
text, and block quotations, and reformats each appropriately. Other options
allow the user to adjust inter-word and inter-paragraph spacing, justify
text, and impose various capitalization schemes.

The module also supplies a re-entrant, highly configurable replacement for
the built-in Perl format() mechanism.

%prep
%setup -q -n Text-Autoformat-%{cpan_version}
chmod -c -x config.*

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}/*

%check
make test

%files
%license LICENSE
%doc Changes README config.emacs config.vim
%{perl_vendorlib}/Text/
%{_mandir}/man3/Text::Autoformat.3pm*

%changelog
* Wed Sep 16 2015 Liu Di <liudidi@gmail.com> - 1.720000-2
- 为 Magic 3.0 重建

* Wed Sep 16 2015 Liu Di <liudidi@gmail.com> - 1.72-1
- 更新到 1.72

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.72-1
- 更新到 1.72

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.669004-7
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.669004-6
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.669004-5
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.669004-4
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.669004-3
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.669004-2
- 为 Magic 3.0 重建

* Fri Oct 25 2013 Paul Howarth <paul@city-fan.org> - 1.669004-1
- Update to 1.669004
  - Tweaked widow handling to avoid a nasty edge case
- Specify all dependencies
- Replace provides filter with a patch that works right back to EL-5
- Don't need to remove empty directories from the buildroot
- Drop %%defattr, redundant since rpm 4.4
- Make %%files list more explicit
- Don't use macros for commands

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.669002-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Petr Pisar <ppisar@redhat.com> - 1.669002-8
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.669002-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.669002-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 1.669002-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.669002-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.669002-3
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.669002-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 08 2010 Steven Pritchard <steve@kspei.com> 1.669002-1
- Update to 1.669002.
- BR version and Module::Build (and build with that).
- Include config.emacs and config.vim in docs.

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.14.0-7
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.14.0-6
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.14.0-3
- Rebuild for perl 5.10 (again)

* Wed Jan 23 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.14.0-2
- add BR: Test::More

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.14.0-1
- rebuild for new perl
- upstream changed license to GPL+ or Artistic

* Wed Apr 18 2007 Steven Pritchard <steve@kspei.com> 1.13-5
- Use fixperms macro instead of our own chmod incantation.
- BR ExtUtils::MakeMaker.

* Fri Sep 01 2006 Steven Pritchard <steve@kspei.com> 1.13-4
- Rework spec to look more like current cpanspec output.

* Mon Sep 05 2005 Steven Pritchard <steve@kspei.com> 1.13-3
- Minor spec cleanup.
- Add Artistic.

* Sat Aug 20 2005 Steven Pritchard <steve@kspei.com> 1.13-2
- Fix permissions (#166406).

* Tue May 24 2005 Steven Pritchard <steve@kspei.com> 1.13-1
- Update to 1.13 final.
- Filter bogus perl(Hang) and perl(NullHang) auto-provides.

* Tue May 10 2005 Steven Pritchard <steve@kspei.com> 1.13-0.3.beta
- Drop Epoch and change Release for Fedora Extras.

* Wed Feb 09 2005 Steven Pritchard <steve@kspei.com> 0:1.13-0.fdr.0.2.beta
- Minor update to 0.13beta source, from
  http://rt.cpan.org/NoAuth/Bug.html?id=8018 (pointed out by jpo@di.uminho.pt)

* Wed Jun 09 2004 Steven Pritchard <steve@kspei.com> 0:1.13-0.fdr.0.1.beta
- Specfile regenerated.
- Update to 0.13beta, which includes the upstream fix for a bug reported to
  the author.
