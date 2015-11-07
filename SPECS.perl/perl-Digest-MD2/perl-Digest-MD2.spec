Summary:	Perl interface to the MD2 Algorithm
Name:		perl-Digest-MD2
Version:	2.04
Release:	2%{?dist}
License:	GPL+ or Artistic
Group:		Development/Libraries
Url:		http://search.cpan.org/dist/Digest-MD2/
Source0:	http://search.cpan.org/CPAN/authors/id/G/GA/GAAS/Digest-MD2-%{version}.tar.gz
Patch0:		Digest-MD2-2.03-utf8.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildRequires:	perl(ExtUtils::MakeMaker)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

# Don't "provide" private Perl libs
%{?perl_default_filter}

%description
The Digest::MD2 module allows you to use the RSA Data Security Inc. MD2 Message
Digest algorithm from within Perl programs. The algorithm takes as input a
message of arbitrary length and produces as output a 128-bit "fingerprint" or
"message digest" of the input.

The Digest::MD2 programming interface is identical to the interface of
Digest::MD5.

%prep
%setup -q -n Digest-MD2-%{version}

# Convert docs to UTF-8 encoding
%patch0 -p1

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} ';' 2>/dev/null
%{_fixperms} %{buildroot}

%check


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README Changes rfc1319.txt 
%{perl_vendorarch}/Digest/
%{perl_vendorarch}/auto/Digest/
%{_mandir}/man3/Digest::MD2.3pm*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 2.04-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 2.04-1
- 更新到 2.04

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.03-22
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 2.03-21
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.03-20
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 2.03-19
- 为 Magic 3.0 重建

* Wed Jan 11 2012 Paul Howarth <paul@city-fan.org> 2.03-18
- Spec clean-up:
  - Nobody else likes macros for commands
  - Use a patch rather than scripted iconv to fix character encoding
  - Use DESTDIR rather than PERL_INSTALL_ROOT
  - Use %%{_fixperms} macro rather than our own chmod incantation

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> 2.03-17
- Perl mass rebuild

* Tue Feb  8 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 2.03-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> 2.03-15
- Rebuild to fix problems with vendorarch/lib (#661697)

* Tue May 11 2010 Paul Howarth <paul@city-fan.org> 2.03-14
- Use %%{?perl_default_filter} for provides filter

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> 2.03-13
- Mass rebuild with perl 5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> 2.03-12
- Mass rebuild with perl 5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> 2.03-11
- Rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 2.03-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Mar  7 2009 Paul Howarth <paul@city-fan.org> 2.03-9
- Filter out unwanted provides for perl shared objects
- Recode docs as UTF-8

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 2.03-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.03-7
- Rebuild for new perl

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> 2.03-6
- Autorebuild for GCC 4.3

* Mon Aug 13 2007 Paul Howarth <paul@city-fan.org> 2.03-5
- Clarify license as GPL v1 or later, or Artistic (same as perl)

* Wed Apr 18 2007 Paul Howarth <paul@city-fan.org> 2.03-4
- Buildrequire perl(ExtUtils::MakeMaker)
- Fix argument order for find with -depth

* Tue Aug 29 2006 Paul Howarth <paul@city-fan.org> 2.03-3
- FE6 mass rebuild

* Wed Feb 15 2006 Paul Howarth <paul@city-fan.org> 2.03-2
- Rebuild for perl 5.8.8 (FC5)

* Mon Dec  5 2005 Paul Howarth <paul@city-fan.org> 2.03-1
- Initial build
