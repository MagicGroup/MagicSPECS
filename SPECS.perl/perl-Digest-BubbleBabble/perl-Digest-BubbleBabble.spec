Summary:	Create bubble-babble fingerprints
Name:		perl-Digest-BubbleBabble
Version:	0.02
Release:	8%{?dist}
License:	GPL+ or Artistic
Group:		Development/Libraries
Url:		http://search.cpan.org/dist/Digest-BubbleBabble/
Source0:	http://search.cpan.org/CPAN/authors/id/B/BT/BTROTT/Digest-BubbleBabble-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Test::Pod)
# Test::Synopsis requires Test::Builder::Module, available from Perl 5.8.8 (EL-5)
# Digest::SHA1 is only used in the Synopsis code to be tested by Test::Synopsis
%if %(perl -e 'print (($] >= 5.008008) ? 1 : 0);')
BuildRequires:	perl(Digest::SHA1), perl(Test::Synopsis)
%endif

%description
Digest::BubbleBabble takes a message digest (generated by either of the MD5 or
SHA-1 message digest algorithms) and creates a fingerprint of that digest in
"bubble babble" format. Bubble babble is a method of representing a message
digest as a string of "real" words, to make the fingerprint easier to remember.
The "words" are not necessarily real words, but they look more like words than
a string of hex characters.

Bubble babble fingerprinting is used by the SSH2 suite (and, consequently, by
Net::SSH::Perl, the Perl SSH implementation) to display easy-to-remember key
fingerprints. The key (a DSA or RSA key) is converted into a textual form,
digested using Digest::SHA1, and run through bubblebabble to create the key
fingerprint.

%prep
%setup -q -n Digest-BubbleBabble-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} ';' 2>/dev/null
%{_fixperms} %{buildroot}

%check

 TEST_FILES="xt/*.t"

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes
%{perl_vendorlib}/Digest/
%{_mandir}/man3/Digest::BubbleBabble.3pm*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.02-8
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.02-7
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.02-6
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.02-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.02-4
- Perl 5.16 rebuild

* Wed Jan 11 2012 Paul Howarth <paul@city-fan.org> - 0.02-3
- Fedora 17 mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.02-2
- Perl mass rebuild

* Thu Mar 24 2011 Paul Howarth <paul@city-fan.org> - 0.02-1
- Update to 0.02:
  - Fixed a bug affecting input strings with an odd number of characters
  - Cleaned up Makefile.PL
  - Removed magic svn keywords
  - Added author tests (xt/) and modified SYNOPSIS for all modules to make
    them pass the compilation test
- Nobody else likes macros for commands
- Use %%{_fixperms} macro instead of our own chmod incantation
- Add buildreqs perl(Digest::SHA1), perl(Test::Pod) and perl(Test::Synopsis)
  and run author tests

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.01-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.01-14
- Rebuild to fix problems with vendorarch/lib (#661697)

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.01-13
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.01-12
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.01-11
- Rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.01-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.01-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.01-8
- Rebuild for perl 5.10 (again)

* Thu Jan 31 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.01-7
- Rebuild for new perl

* Mon Aug 13 2007 Paul Howarth <paul@city-fan.org> 0.01-6
- Clarify license as GPL v1 or later, or Artistic (same as perl)

* Wed Apr 18 2007 Paul Howarth <paul@city-fan.org> 0.01-5
- Buildrequire perl(ExtUtils::MakeMaker)
- Fix argument order for find with -depth

* Tue Aug 29 2006 Paul Howarth <paul@city-fan.org> 0.01-4
- FE6 mass rebuild

* Wed Feb 15 2006 Paul Howarth <paul@city-fan.org> 0.01-3
- Rebuild for perl 5.8.8 (FC5)

* Tue Jan  3 2006 Paul Howarth <paul@city-fan.org> 0.01-2
- Don't include README, which contains only install instructions (#175280)

* Fri Nov 25 2005 Paul Howarth <paul@city-fan.org> 0.01-1
- Initial build