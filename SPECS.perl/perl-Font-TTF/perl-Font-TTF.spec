Name:          perl-Font-TTF
Version:	1.05
Release:	1%{?dist}
Summary:       Perl library for modifying TTF font files
Group:         Development/Libraries
License:       Artistic 2.0
URL:           http://search.cpan.org/dist/Font-TTF/
Source0:       http://cpan.org/authors/id/M/MH/MHOSKEN/Font-TTF-%{version}.tar.gz
BuildArch:     noarch
BuildRequires: perl(Compress::Zlib)
BuildRequires: perl(Data::Dumper)
BuildRequires: perl(Exporter)
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(File::Spec)
BuildRequires: perl(IO::File)
BuildRequires: perl(IO::String)
BuildRequires: perl(Test::Simple)
BuildRequires: perl(XML::Parser::Expat)
Requires: perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
Perl module for TrueType font hacking. Supports reading, processing and writing
of the following tables: GDEF, GPOS, GSUB, LTSH, OS/2, PCLT, bsln, cmap, cvt,
fdsc, feat, fpgm, glyf, hdmx, head, hhea, hmtx, kern, loca, maxp, mort, name,
post, prep, prop, vhea, vmtx and the reading and writing of all other table
types.

In short, you can do almost anything with a standard TrueType font with this
module.

%prep
%setup -q -n Font-TTF-%{version}
#dos2unix README.TXT COPYING lib/Font/TTF/Changes

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'
%{_fixperms} %{buildroot}/*

%check


%files
%doc README.TXT LICENSE CONTRIBUTORS Changes TODO
%dir %{perl_vendorlib}/Font
%dir %{perl_vendorlib}/Font/TTF
%{perl_vendorlib}/ttfmod.pl
%{perl_vendorlib}/Font/TTF.pm
%{perl_vendorlib}/Font/TTF/*
%{_mandir}/man3/*.3*
# We really don't want to use this perl package in a Win32 env
# or poke in the windows registry to resolve fonts
# (upstream makefile needs to get smarter)
%exclude %{perl_vendorlib}/Font/TTF/Win32.pm

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.05-1
- 更新到 1.05

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.02-5
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.02-4
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.02-3
- 为 Magic 3.0 重建

* Tue Nov 06 2012 Petr Šabata <contyk@redhat.com> - 1.02-2
- Add missing dependencies

* Fri Aug 31 2012 Petr Šabata <contyk@redhat.com> - 1.02-1
- 1.02 bump (a lettercase fix)

* Thu Aug 30 2012 Petr Šabata <contyk@redhat.com> - 1.01-1
- 1.01 bump (Makefile/META changes only)

* Wed Aug 29 2012 Petr Šabata <contyk@redhat.com> - 1.00-1
- 1.00 bump
- Modernize the spec file

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.48-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.48-4
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.48-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.48-2
- Perl mass rebuild

* Wed Mar 09 2011 Parag Nemade <panemade AT fedoraproject DOT org> - 0.48-1
- new upstream release 0.48

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.45-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.45-8
- 661697 rebuild for fixing problems with vendorach/lib

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.45-7
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.45-6
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.45-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.45-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.45-3
— global-ization

* Thu Sep 4 2008 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.45-2
⚖ ⇒ Artistic 2.0

* Fri Jul 11 2008 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.45-1
⌖ Fedora 10 alpha general package cleanup
⚖ Upstream needs to relicense fast to avoid culling

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com>
- 0.43-3
Rebuild for new perl

* Sat Feb 09 2008  Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.43-2

* Fri May 18 2007 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.41-1

* Tue Mar 20 2007 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.40.0-3
- small packaging fixes

* Sat Sep 02 2006  Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.40.0-2
- FE6 Rebuild

* Mon Jul 31 2006 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.40.0-1

* Sat Feb 18 2006 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.38.1-1
- new version with COPYING file as requested from upstream
  many thanks to Martin Hosken for quick action!

* Mon Feb 13 2006 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.37-4
- rebuilt for new gcc4.1 snapshot and glibc changes

* Sun Feb 5 2006 Nicolas Mailhot <nicolas.mailhot (at) laposte.net>
- 0.37-3
- spec cleanups #2

* Sun Feb 5 2006 Nicolas Mailhot <nicolas.mailhot (at) laposte.net>
- 0.37-2
- spec cleanups

* Sat Feb 4 2006 Nicolas Mailhot <nicolas.mailhot (at) laposte.net>
- 0.37-1
- Initial release
