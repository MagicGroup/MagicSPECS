# Provides/Requires filtering is different from rpm 4.9 onwards
%global rpm49 %(rpm --version | perl -p -e 's/^.* (\\d+)\\.(\\d+).*/sprintf("%d.%03d",$1,$2) ge 4.009 ? 1 : 0/e')

Name:           perl-Module-Info
Version:        0.35
Release:        4%{?dist}
Summary:        Information about Perl modules
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Module-Info/
Source0:        http://www.cpan.org/authors/id/M/MB/MBARBON/Module-Info-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:      noarch
BuildRequires:  perl(Carp)
BuildRequires:  perl(Class::Struct)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(lib)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Safe)
BuildRequires:  perl(Test::Pod) >= 1.00
BuildRequires:  perl(Test::Pod::Coverage) >= 1.00
BuildRequires:  perl(version)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Safe)
Requires:       perl(version)

# We don't really provide perl(B::Utils)
%global __provides_exclude ^perl\\(B::Utils\\)

%description
Module::Info gives you information about Perl modules without actually loading
the module. It isn't actually specific to modules and should work on any perl
code.

%prep
%setup -q -n Module-Info-%{version}

# We don't really provide perl(B::Utils) [filter for rpm < 4.9]
%if ! %{rpm49}
%global provfilt /bin/sh -c "%{__perl_provides} | grep -Ev '^perl\\(B::Utils\\)'"
%define __perl_provides %{provfilt}
%endif

%build
perl Build.PL installdirs=vendor
./Build

%install
rm -rf $RPM_BUILD_ROOT
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
%{_fixperms} $RPM_BUILD_ROOT

%check
./Build test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc Changes
%{_bindir}/*
%{perl_vendorlib}/*
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.35-4
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.35-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jan 21 2014 Paul Howarth <paul@city-fan.org> - 0.35-2
- Drop pointless in-place edit flag from perl filter invocation

* Sun Sep  8 2013 Paul Howarth <paul@city-fan.org> - 0.35-1
- Update to 0.35
  - Handle 'package NAME VERSION' syntax
  - Added repository and license info to metadata
  - Tweaked format of Changes (this file) to match CPAN::Changes::Spec

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.34-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Petr Pisar <ppisar@redhat.com> - 0.34-2
- Perl 5.18 rebuild

* Tue May 21 2013 Paul Howarth <paul@city-fan.org> - 0.34-1
- Update to 0.34
  - Replace Text::Soundex in tests with Class::Struct, since Text::Soundex will
    not be in core in Perl 5.19 and up
  - Replace ExtUtils::MY_Metafile with META_MERGE in Makefile.PL

* Sun Feb 10 2013 Paul Howarth <paul@city-fan.org> - 0.33-1
- Update to 0.33
  - Fix tests under Perl 5.6.2 when some core modules have been upgraded
- Add provides filter that works with rpm ≥ 4.10
- Simplify provides filter for rpm < 4.10
- BR: perl(Carp), perl(Cwd), perl(File::Spec), perl(lib) and
  perl(Text::Soundex)
- BR:/R: perl(Safe)
- BR: at least version 1.00 of perl(Test::Pod) and perl(Test::Pod::Coverage)
- Don't use macros for commands
- Don't need to remove empty directories from the buildroot
- Drop %%defattr, redundant since rpm 4.4

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.32-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.32-5
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.32-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.32-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.32-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 28 2010 Steven Pritchard <steve@kspei.com> 0.32-1
- Update to 0.32.

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.31-9
- Rebuild to fix problems with vendorarch/lib (#661697)

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.31-8
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.31-7
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 17 2008 Steven Pritchard <steve@kspei.com> 0.31-4
- BR Test::Pod::Coverage.
- Filter B::Utils auto-provides.

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.31-3
- Rebuild for perl 5.10 (again)

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.31-2
- rebuild for new perl

* Wed May 30 2007 Steven Pritchard <steve@kspei.com> 0.31-1
- Update to 0.31.

* Wed Apr 18 2007 Steven Pritchard <steve@kspei.com> 0.30-5
- Use fixperms macro instead of our own chmod incantation.

* Sun Sep 17 2006 Steven Pritchard <steve@kspei.com> 0.30-4
- Rebuild.

* Wed May 24 2006 Steven Pritchard <steve@kspei.com> 0.30-3
- Rebuild.

* Sat May 06 2006 Steven Pritchard <steve@kspei.com> 0.30-2
- Add BR: perl(Test::Pod) and perl(version).
- Add Requires: perl(version).

* Fri Apr 21 2006 Steven Pritchard <steve@kspei.com> 0.30-1
- Update to 0.30.
- Use perl macro.
- Drop extra find.

* Fri Mar 24 2006 Steven Pritchard <steve@kspei.com> 0.290-1
- Specfile autogenerated by cpanspec 1.64.
- Add bindir and man1 files.
