Name:           perl-Hook-LexWrap
Version:        0.24
Release:        3%{?dist}
Summary:        Lexically scoped subroutine wrappers
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Hook-LexWrap/
Source0:        http://search.cpan.org/CPAN/authors/id/C/CH/CHORNY/Hook-LexWrap-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:      noarch
BuildRequires:  perl(Carp)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
Hook::LexWrap allows you to install a pre- or post-wrapper (or both)
around an existing subroutine. Unlike other modules that provide this
capacity (e.g. Hook::PreAndPost and Hook::WrapSub), Hook::LexWrap
implements wrappers in such a way that the standard `caller' function
works correctly within the wrapped subroutine.

%prep
%setup -q -n Hook-LexWrap-%{version}

# Fix line endings
sed -i -e 's/\r$//' Changes README demo/*

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check


%clean
rm -rf %{buildroot}

%files
%doc Changes README demo/
%{perl_vendorlib}/Hook/
%{_mandir}/man3/Hook::LexWrap.3pm*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.24-3
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.24-2
- 为 Magic 3.0 重建

* Tue Jul 24 2012 Paul Howarth <paul@city-fan.org> - 0.24-1
- Update to 0.24
  - Add Build.PL
  - Better support for debugger
  - Makefile.PL fixed
  - New test added
- BR: perl(Carp)
- Include demo files as %%doc
- Fix line endings on documentation
- Upstream release is now a tarball rather than a zipfile
- Drop %%defattr, redundant since rpm 4.4
- Don't need to remove empty directories from the buildroot
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Use %%{_fixperms} macro rather than our own chmod incantation
- Don't use macros for commands
- Make %%files list more explicit

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.22-10
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.22-8
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.22-6
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.22-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.22-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 21 2009 Ralf Corsepius <corsepiu@fedoraproject.org> - 0.22-1
- Upstream update.
- Reflect upstream having fixed CPAN RT#38892:
  Remove Hook-LexWrap-0.21-cpan-rt-38892.diff.
- Reflect upstream having fixed permissions.

* Mon Nov 10 2008 Paul Howarth <paul@city-fan.org> - 0.21-1
- Update to 0.21
- New upstream maintainer => new source URL
- Add buildreqs perl(Test::More) and perl(Test::Pod)
- Update patch for CPAN RT#38892 to apply without fuzz
- Fix argument order for find with -depth

* Mon Oct 06 2008 Ralf Corsepius <corsepiu@fedoraproject.org> - 0.20-6
- Add Hook-LexWrap-0.20-cpan-rt-38892.diff to fix
  http://rt.cpan.org/Public/Bug/Display.html?id=38892
  (Bugs shows while building rt3).

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.20-5
- Rebuild for perl 5.10 (again)

* Sat Jan 12 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.20-4.2
- rebuild for new perl

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.20-4.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Fri Sep  8 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.20-4
- Rebuild for FC6.

* Fri Feb 17 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.20-3
- Rebuild for FC5 (perl 5.8.8).

* Fri Sep  9 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.20-2
- Comment about license files location.

* Fri Aug 26 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.20-1
- First build.
