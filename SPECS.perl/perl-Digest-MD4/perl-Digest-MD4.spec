Name:		perl-Digest-MD4
Version:	1.9
Release:	3%{?dist}
Summary:	Perl interface to the MD4 Algorithm
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/Digest-MD4/
Source0:	http://search.cpan.org/CPAN/authors/id/M/MI/MIKEM/DigestMD4/Digest-MD4-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildRequires:	perl(ExtUtils::MakeMaker), db4-devel, gdbm-devel
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# Don't "provide" private Perl libs
%{?perl_default_filter}

%description
The Digest::MD4 module allows you to use the RSA Data Security Inc. MD4 Message
Digest algorithm from within Perl programs. The algorithm takes as input a
message of arbitrary length and produces as output a 128-bit "fingerprint" or
"message digest" of the input.

%prep
%setup -q -n Digest-MD4-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -empty -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} ';' 2>/dev/null
%{_fixperms} %{buildroot}

%check


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes README rfc1320.txt
%{perl_vendorarch}/Digest/
%{perl_vendorarch}/auto/Digest/
%{_mandir}/man3/Digest::MD4.3pm*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.9-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.9-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.9-1
- 更新到 1.9

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.5-30
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.5-29
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.5-28
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.5-27
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.5-26
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.5-25
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.5-24
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.5-23
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.5-22
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.5-21
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.5-20
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.5-19
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.5-18
- 为 Magic 3.0 重建

* Wed Jan 11 2012 Paul Howarth - 1.5-17
- spec clean-up:
  - nobody else likes macros for commands
  - use DESTDIR rather than PERL_INSTALL_ROOT
  - use %%{_fixperms} macro rather than our own chmod incantation

* Thu Jun 16 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.5-16
- perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-15
- rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.5-14
- rebuild to fix problems with vendorarch/lib (#661697)

* Sat May  1 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.5-13
- mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.5-12
- mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.5-11
- rebuild against perl 5.10.1

* Wed Nov 25 2009 Paul Howarth <paul@city-fan.org> - 1.5-10
- use %%{?perl_default_filter} for provides filter
- make %%files list more explicit

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-9
- rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Mar  7 2009 Paul Howarth <paul@city-fan.org> - 1.5-8
- filter out unwanted provides for perl shared objects

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-7
- rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.5-6
- rebuild for new perl

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.5-5
- autorebuild for GCC 4.3

* Wed Nov 28 2007 Paul Howarth <paul@city-fan.org> - 1.5-4
- cosmetic spec changes for new maintainer's preferences
- fix argument order for find with -depth
- add buildreqs db4-devel and gdbm-devel for alignment optimization

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.5-3.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Thu Sep  7 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.5-3
- rebuild for FC6

* Fri Feb 17 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.5-2
- rebuild for FC5 (perl 5.8.8)

* Sat Sep 10 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.5-1
- first build
