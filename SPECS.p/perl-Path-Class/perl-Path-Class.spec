Name:		perl-Path-Class
Version:	0.26
Release:	4%{?dist}
Summary:	Cross-platform path specification manipulation
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Path-Class/
Source0:	http://search.cpan.org/CPAN/authors/id/K/KW/KWILLIAMS/Path-Class-%{version}.tar.gz
Patch0:		Path-Class-0.25-old-M::B.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
BuildRequires:	perl(base)
BuildRequires:	perl(Carp)
BuildRequires:	perl(Cwd)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(File::Path)
BuildRequires:	perl(File::Spec) >= 0.87
BuildRequires:	perl(File::stat)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(IO::Dir)
BuildRequires:	perl(IO::File)
BuildRequires:	perl(Module::Build)
BuildRequires:	perl(Test::More)
# We need Perl::Perl::Critic ≥ 1.080 for a fix to
# Variables::ProhibitConditionalDeclarations, and the EPEL-5 version is too old
%if "%{?rhel}" != "5"
BuildRequires:	perl(Test::Perl::Critic)
%endif
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
Path::Class is a module for manipulation of file and directory specifications
(strings describing their locations, like '/home/ken/foo.txt' or
'C:\Windows\Foo.txt') in a cross-platform manner. It supports pretty much every
platform Perl runs on, including Unix, Windows, Mac, VMS, Epoc, Cygwin, OS/2,
and NetWare.

%prep
%setup -q -n Path-Class-%{version}

# Don't really need Module::Build ≥ 0.3601
%patch0 -p1

%build
perl Build.PL installdirs=vendor
./Build

%install
rm -rf %{buildroot}
./Build install destdir=%{buildroot} create_packlist=0
%{_fixperms} %{buildroot}

%check
AUTHOR_TESTING=1 ./Build test

%clean
rm -rf %{buildroot}

%files
%doc Changes README
%{perl_vendorlib}/Path/
%{_mandir}/man3/Path::Class.3pm*
%{_mandir}/man3/Path::Class::Dir.3pm*
%{_mandir}/man3/Path::Class::Entity.3pm*
%{_mandir}/man3/Path::Class::File.3pm*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.26-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 0.26-2
- Perl 5.16 rebuild

* Fri Jun 15 2012 Paul Howarth <paul@city-fan.org> - 0.26-1
- Update to 0.26:
  - resolve() now includes the name of the non-existent file in the error
    message
  - New shortcut opena(), to open a file for appending
  - New spew() method that does the inverse of the slurp() method
  - Fixed a typo in a class name in the docs for Path::Class::Entity
- Drop %%defattr, redundant since rpm 4.4
- Drop conditional for EPEL-4 support (EL-4 now EOL-ed)

* Thu Feb 16 2012 Paul Howarth <paul@city-fan.org> - 0.25-1
- Update to 0.25:
  - resolve() now croak()s instead of die()s on non-existent file
  - Added a traverse() method for directories, based on the fmap_cont() method
    of Forest::Tree::Pure; it's an alternative to ->recurse, which allows for
    more control over how the recursion happens
  - Fixed a grammar error in the docs
  - Added a tempfile() method for Dir objects, which provides an interface to
    File::Temp (CPAN RT#60485)
  - Fixed a non-helpful fatal error message when calling resolve() on a path
    that doesn't exist; now dies with the proper "No such file or directory"
    message and exit status
- BR: perl(Test::Perl::Critic) and run author tests where possible
- Add patch to support building with Module::Build < 0.3601

* Thu Feb 16 2012 Paul Howarth <paul@city-fan.org> - 0.23-4
- Spec clean-up:
  - Add buildreqs for Perl core modules that might be dual-lived
  - Tidy %%description
  - Make %%files list more explicit
  - Don't use macros for commands
  - Use search.cpan.org source URL
  - BR: at least version 0.87 of File::Spec

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.23-2
- Perl mass rebuild

* Thu Apr 14 2011 Ian Burrell <ianburrell@gmail.com> - 0.23-1
- Update to 0.23

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.18-3
- Rebuild to fix problems with vendorarch/lib (#661697)

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.18-2
- Mass rebuild with perl-5.12.0

* Mon Feb 22 2010 Chris Weyl <cweyl@alumni.drew.edu> - 0.18-1
- Update to 0.18 (for latest DBIx::Class)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.16-6
- Rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.16-3
- Rebuild for new perl

* Thu Aug 16 2007 Ian Burrell <ianburrell@gmail.com> - 0.16-2
- Fix BuildRequires

* Mon Jan 29 2007 Ian Burrell <ianburrell@gmail.com> - 0.16-1
- Specfile autogenerated by cpanspec 1.69.1
