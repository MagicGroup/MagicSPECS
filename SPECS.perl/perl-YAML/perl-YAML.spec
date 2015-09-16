Name:           perl-YAML
Version:	1.15
Release:	1%{?dist}
Summary:        YAML Ain't Markup Language (tm)
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/YAML/
Source0:	http://search.cpan.org/CPAN/authors/id/I/IN/INGY/YAML-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(lib)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Carp)
Requires:       perl(Data::Dumper)

# Filter private provides:
# perl(yaml_mapping) perl(yaml_scalar) perl(yaml_sequence)
%global __provides_exclude ^perl\\(yaml_

%description
The YAML.pm module implements a YAML Loader and Dumper based on the
YAML 1.0 specification. http://www.yaml.org/spec/
YAML is a generic data serialization language that is optimized for
human readability. It can be used to express the data structures of
most modern programming languages, including Perl.
For information on the YAML syntax, please refer to the YAML
specification.

%prep
%setup -q -n YAML-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor < /dev/null
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

# Removing Test::YAML (at least temporarily) due
# to security concerns and questionable value.
# https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=197539
rm -f %{buildroot}%{perl_vendorlib}/Test/YAML* \
    %{buildroot}%{_mandir}/man3/Test::YAML*.3*

%check


%files
%doc Changes README LICENSE
%{perl_vendorlib}/YAML*
%{_mandir}/man3/YAML*.3*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.15-1
- 更新到 1.15

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.84-6
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.84-5
- 为 Magic 3.0 重建

* Tue Aug 28 2012 Jitka Plesnikova <jplesnik@redhat.com> - 0.84-4
- Specify all dependencies.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.84-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Paul Howarth <paul@city-fan.org> - 0.84-2
- Haven't needed to fix documentation character encoding since 0.79
- Drop Test::Base build dependency again to avoid a BR loop (#215637)
- Filter private provides perl(yaml_mapping), perl(yaml_scalar) and
  perl(yaml_sequence)
- Don't need to remove empty directories from the buildroot
- This release by MSTROUT -> update source URL

* Mon Jul 16 2012 Petr Šabata <contyk@redhat.com> - 0.84-1
- 0.84 bump
- Drop command macros
- Drop previously added patch (included in 0.82)

* Fri Jun 22 2012 Jitka Plesnikova <jplesnik@redhat.com> 0.81-4
- apply patch to for YAML::Any RT#74226

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 0.81-3
- Perl 5.16 rebuild

* Mon Apr 23 2012 Paul Howarth <paul@city-fan.org> - 0.81-2
- R: perl(Carp) and perl(Data::Dumper)
- BR: perl(Carp), perl(constant) and perl(Exporter)
- Release tests no longer shipped, so drop buildreqs for them and don't bother
  setting AUTOMATED_TESTING; run tests even when bootstrapping

* Mon Apr 23 2012 Marcela Mašláňová <mmaslano@redhat.com> - 0.81-1
- Update to 0.81
- Add BR Data::Dumper

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.73-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.73-2
- Perl mass rebuild
- add perl_bootstrap macro

* Sat May 14 2011 Iain Arnell <iarnell@gmail.com> 0.73-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.72-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 08 2010 Steven Pritchard <steve@kspei.com> 0.72-1
- Update to 0.72.

* Wed Aug 18 2010 Paul Howarth <paul@city-fan.org> - 0.71-1
- Update to 0.71 (use UTF-8 encoding in LoadFile/DumpFile: CPAN RT#25434)
- Enable AUTOMATED_TESTING
- BR: perl(Test::CPAN::Meta), perl(Test::MinimumVersion), perl(Test::Pod)
- This release by ADAMK -> update source URL
- Re-code docs as UTF-8

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.70-5
- Mass rebuild with perl-5.12.0

* Thu Feb 25 2010 Marcela Mašláňová <mmaslano@redhat.com> - 0.70-4
- add license

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.70-3
- rebuild against perl 5.10.1

* Wed Oct  7 2009 Marcela Mašláňová <mmaslano@redhat.com> - 0.70-2
- rebuild for push

* Tue Oct 6  2009 Marcela Mašláňová <mmaslano@redhat.com> - 0.70-1
- new upstream version

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.68-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.68-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 10 2008 Steven Pritchard <steve@kspei.com> 0.68-1
- Update to 0.68.
- COMPATIBILITY went away.
- ysh moved to YAML::Shell.

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.66-3
- Rebuild for perl 5.10 (again)

* Fri Jan 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.66-2
- rebuild for new perl

* Tue Oct 16 2007 Steven Pritchard <steve@kspei.com> 0.66-1
- Update to 0.66.
- Update License tag.

* Wed Jun 27 2007 Steven Pritchard <steve@kspei.com> 0.65-1
- Update to 0.65.

* Tue Mar 13 2007 Steven Pritchard <steve@kspei.com> 0.62-3
- Use fixperms macro instead of our own chmod incantation.
- Drop Test::Base build dependency to avoid a BR loop (#215637).
- BR ExtUtils::MakeMaker.

* Sat Sep 16 2006 Steven Pritchard <steve@kspei.com> 0.62-2
- Fix find option order.

* Fri Jul 07 2006 Steven Pritchard <steve@kspei.com> 0.62-1
- Update to 0.62.
- Removed Test::YAML (bug #197539).

* Mon Jul 03 2006 Steven Pritchard <steve@kspei.com> 0.61-1
- Update to 0.61.

* Sat May 20 2006 Steven Pritchard <steve@kspei.com> 0.58-3
- Rebuild.

* Tue May 09 2006 Steven Pritchard <steve@kspei.com> 0.58-2
- Drop testmore patch.
- Catch Test::YAML module and man page in file list.

* Thu May 04 2006 Steven Pritchard <steve@kspei.com> 0.58-1
- Update to 0.58.
- Small spec cleanups.

* Thu Apr 14 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.39-2
- 0.39.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sat May 15 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.35-0.fdr.5
- Avoid creation of the perllocal.pod file (make pure_install).

* Sun Apr 25 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.35-0.fdr.4
- Require perl(:MODULE_COMPAT_*).
- Cosmetic tweaks (bug 1383).

* Sun Mar 14 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.35-0.fdr.3
- Reduce directory ownership bloat.

* Tue Nov 18 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.35-0.fdr.2
- Use INSTALLARCHLIB workaround in %%install.

* Wed Sep  3 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.35-0.fdr.1
- First build.
