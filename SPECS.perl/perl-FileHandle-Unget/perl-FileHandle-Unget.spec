# Need to tweak provides filter differently if we have rpm 4.9 onwards
%global rpm49 %(rpm --version | perl -pi -e 's/^.* (\\d+)\\.(\\d+)\\.(\\d+).*/sprintf("%d.%03d%03d",$1,$2,$3) ge 4.009 ? 1 : 0/e')

Summary:	A FileHandle that supports ungetting of multiple bytes
Name:		perl-FileHandle-Unget
Version:	0.1623
Release:	14%{?dist}
License:	GPL+
Group:		Development/Libraries
Url:		http://search.cpan.org/dist/FileHandle-Unget/
Source0:	http://search.cpan.org/CPAN/authors/id/D/DC/DCOPPIT/FileHandle-Unget-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
BuildRequires:	perl(Scalar::Util) >= 1.14
BuildRequires:	perl(Devel::Leak), perl(ExtUtils::MakeMaker), perl(Test::More)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Provides:	perl(FileHandle::Unget) = %{version}

%description
FileHandle::Unget is a drop-in replacement for FileHandle that allows more
than one byte to be placed back on the input. It supports an ungetc(ORD), which
can be called more than once in a row, and an ungets(SCALAR), which places a
string of bytes back on the input.

%prep
%setup -q -n FileHandle-Unget-%{version}

# Drop bogus autodetected provide
%if %{rpm49}
%global __provides_exclude ^perl\\(FileHandle::Unget\\)
%else
%global provfilt /bin/sh -c "%{__perl_provides} | grep -v '^perl(FileHandle::Unget)'"
%define __perl_provides %{provfilt}
%endif

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
%doc README CHANGES LICENSE
%{perl_vendorlib}/FileHandle/
%{_mandir}/man3/FileHandle::Unget.3pm*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.1623-14
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.1623-13
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.1623-12
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.1623-11
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.1623-10
- 为 Magic 3.0 重建

* Sat Jan  7 2012 Paul Howarth <paul@city-fan.org> 0.1623-9
- Rebuilt for Fedora 17 Mass Rebuild

* Thu Jul 28 2011 Paul Howarth <paul@city-fan.org> 0.1623-8
- Tweak provides filter for rpm 4.9 compatibility
- Nobody else likes macros for commands
- Use DESTDIR rather than PERL_INSTALL_ROOT

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.1623-7
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1623-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.1623-5
- Rebuild to fix problems with vendorarch/lib (#661697)

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.1623-4
- Mass rebuild with perl-5.12.0

* Fri Feb 19 2010 Paul Howarth <paul@city-fan.org> 0.1623-3
- Fix versioned provide for perl(FileHandle::Unget)
- Add buildreq perl(Devel::Leak) for additional test coverage
- Use %%{_fixperms} macro instead of our own %%{__chmod} incantation

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> 0.1623-2
- Rebuild against perl 5.10.1

* Tue Sep  1 2009 Paul Howarth <paul@city-fan.org> 0.1623-1
- Update to 0.1623
  - fix uninitialized value warning and incorrect behaviour (CPAN RT#48528)
  - remove reference to obsolete ExtUtils::MakeMaker::bytes (CPAN RT#48984)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1622-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1622-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jul 17 2008 Paul Howarth <paul@city-fan.org> 0.1622-1
- Update to 0.1622
- BuildRequire perl(Test::More)
- Unget.pm permissions no longer need fixing

* Thu Feb  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.1621-6
- rebuild for new perl

* Mon Aug 13 2007 Paul Howarth <paul@city-fan.org> 0.1621-5
- Clarify license as GPL (unspecified version)

* Wed Apr 18 2007 Paul Howarth <paul@city-fan.org> 0.1621-4
- Buildrequire perl(ExtUtils::MakeMaker)
- Fix argument order for find with -depth

* Tue Aug 29 2006 Paul Howarth <paul@city-fan.org> 0.1621-3
- FE6 mass rebuild

* Thu Feb 16 2006 Paul Howarth <paul@city-fan.org> 0.1621-2
- Don't use macros in command paths, hardcode them instead

* Wed Oct 12 2005 Paul Howarth <paul@city-fan.org> 0.1621-1
- Fedora Extras submission
