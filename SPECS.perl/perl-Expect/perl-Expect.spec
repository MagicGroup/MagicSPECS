Name:		perl-Expect
Version:	1.32
Release:	3%{?dist}
Summary:	Expect for Perl
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/Expect/
Source0:        http://search.cpan.org/CPAN/authors/id/S/SZ/SZABGAB/Expect-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
BuildRequires:	perl(Carp)
BuildRequires:	perl(Errno)
BuildRequires:	perl(Exporter)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Fcntl)
BuildRequires:	perl(IO::Handle)
BuildRequires:	perl(IO::Pty) >= 1.03
BuildRequires:	perl(IO::Tty) >= 1.03
BuildRequires:	perl(POSIX)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This module provides Expect-like functionality to Perl. Expect is
a tool for automating interactive applications such as telnet, ftp,
passwd, fsck, rlogin, tip, etc.


%prep
%setup -q -n Expect-%{version}
sed -i 's|^#!/usr/local/bin/perl|#!/usr/bin/perl|' examples/kibitz/kibitz tutorial/[2-6].*
chmod -c a-x examples/ssh.pl examples/kibitz/kibitz tutorial/[2-6].*

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
%{perl_vendorlib}/Expect.pm
%{_mandir}/man3/Expect.3pm*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.32-3
- 为 Magic 3.0 重建

* Mon Sep 14 2015 Liu Di <liudidi@gmail.com> - 1.32-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.32-1
- 更新到 1.32

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.21-15
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.21-14
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.21-13
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.21-12
- 为 Magic 3.0 重建

* Mon Jan 23 2012 Paul Howarth <paul@city-fan.org> - 1.21-11
- Spec clean-up
  - Run the test suite in %%check now that it no longer breaks in mock
  - BR: perl(Carp), perl(Errno), perl(Exporter), perl(Fcntl), perl(IO::Handle)
    and perl(POSIX)
  - Make %%files list more explicit
  - Use search.cpan.org source URL
  - Use DESTDIR rather than PERL_INSTALL_ROOT
  - Use %%{_fixperms} macro rather than our own chmod incantation
  - Don't use macros for commands
  - Use tabs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 23 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.21-9
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.21-7
- Rebuild to fix problems with vendorarch/lib (#661697)

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.21-6
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.21-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.21-4
- Rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Mar 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.21-1
- Update to 1.21

* Wed Mar 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.20-2
- Rebuild for new perl

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.20-1.1
- Correct license tag
- Add BR: perl(ExtUtils::MakeMaker)

* Fri Jul 21 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.20-1
- Update to 1.20

* Tue Jul 18 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.19-1
- Update to 1.19

* Tue Jul 11 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.18-1
- Update to 1.18

* Wed May 31 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.17-1
- Update to 1.17

* Tue May 16 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.16-2
- Description improved as suggested in #191622

* Mon May 08 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.16-1
- First build
