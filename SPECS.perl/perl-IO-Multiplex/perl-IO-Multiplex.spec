Summary:	Manage IO on many file handles
Name:		perl-IO-Multiplex
Version:	1.16
Release:	3%{?dist}
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/IO-Multiplex/
Source0:        http://search.cpan.org/CPAN/authors/id/B/BB/BBB/IO-Multiplex-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
BuildRequires:	perl(Carp)
BuildRequires:	perl(Fcntl)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(FileHandle)
BuildRequires:	perl(IO::Handle)
BuildRequires:	perl(POSIX)
BuildRequires:	perl(Socket)
BuildRequires:	perl(Tie::Handle)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
IO::Multiplex is designed to take the effort out of managing multiple file
handles. It is essentially a really fancy front end to the select system call.
In addition to maintaining the select loop, it buffers all input and output
to/from the file handles. It can also accept incoming connections on one or
more listen sockets.

%prep
%setup -q -n IO-Multiplex-%{version}

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
%doc Changes README TODO
%{perl_vendorlib}/IO/
%{_mandir}/man3/IO::Multiplex.3pm*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.16-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.16-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.16-1
- 更新到 1.16

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.13-6
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.13-5
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.13-4
- 为 Magic 3.0 重建

* Thu Jan 12 2012 Paul Howarth <paul@city-fan.org> - 1.13-2
- Add buildreqs for core modules, which may be dual-lived

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.13-2
- Perl mass rebuild

* Fri Apr 15 2011 Paul Howarth <paul@city-fan.org> - 1.13-1
- Update to 1.13
  - Fix handling of outbuf that contains '0' (CPAN RT#67458)
- Nobody else likes macros for commands

* Thu Feb 24 2011 Paul Howarth <paul@city-fan.org> - 1.12-1
- Update to 1.12
  - Fixes for Windows (CPAN RT#66096)

* Mon Feb 21 2011 Paul Howarth <paul@city-fan.org> - 1.11-1
- Update to 1.11
  - Avoid warning while adding pipe (CPAN RT#16259, CPAN RT#60068)
  - Add EWOULDBLOCK and non-blocking mode for windows (CPAN RT#23982)
  - Fix typo in documentation (CPAN RT#21085)
  - Avoid shutdown after close (CPAN RT#5885, CPAN RT#5715)
  - Use length of outbuf, not exists to see if it is empty
  - Turn "use warnings" on
- This release by MARKOV -> update source URL
- Use %%{_fixperms} rather than our own chmod incantation
- Tidy up %%summary and %%description

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.10-8
- Rebuild to fix problems with vendorarch/lib (#661697)

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.10-7
- Mass rebuild with perl 5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.10-6
- Rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 11 2009 Paul Howarth <paul@city-fan.org> - 1.10-4
- Fix argument order for find with -depth
- Include TODO
- Cosmetic changes

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.10-1
- Update to 1.10, upstream found and relicensing has happened!

* Thu Mar  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.09-1
- Rebuild for new perl
- 1.09

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.08-5.1
- Add BR: perl(ExtUtils::MakeMaker)

* Fri Sep 15 2006 Leif O M Bergman <lmb@biosci.ki.se> - 1.08-5
- Add dist tag

* Tue Dec 13 2005 Leif O M Bergman <lmb@biosci.ki.se> - 1.08-4
- Changes for fedora xtras compliance

* Mon Dec 12 2005 Leif O M Bergman <lmb@biosci.ki.se> - 1.08-3
- Cosmetic changes for fedora xtras

* Sun Feb 20 2005 Dag Wieers <dag@wieers.com> - 1.08-2
- Cosmetic changes

* Thu Mar 18 2004 Dag Wieers <dag@wieers.com> - 1.08-1
- Updated to release 1.08

* Mon Jul 14 2003 Dag Wieers <dag@wieers.com> - 1.04-0
- Initial package (using DAR)
