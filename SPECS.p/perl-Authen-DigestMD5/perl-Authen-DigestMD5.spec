Summary:	SASL DIGEST-MD5 authentication (RFC2831)
Summary(zh_CN.UTF-8): SASL DIGEST-MD5 认证 (RFC2831)
Name:		perl-Authen-DigestMD5
Version:	0.04
Release:	18%{?dist}
License:	GPL+ or Artistic
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Url:		http://search.cpan.org/dist/Authen-DigestMD5/
Source0:	http://search.cpan.org/CPAN/authors/id/S/SA/SALVA/Authen-DigestMD5-%{version}.tar.gz
Patch0:		Authen-DigestMD5-0.04-UTF8.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
BuildRequires:	perl(Carp)
BuildRequires:	perl(Digest::MD5)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Test::More)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This module supports DIGEST-MD5 SASL authentication as defined in RFC-2831.

%description -l zh_CN.UTF-8
这个模块支持 RFC-2831 定义的 DIGEST-MD5 SASL 认证。

%prep
%setup -q -n Authen-DigestMD5-%{version}

# Fix wrong script interpreter, and set permissions to avoid extra deps
sed -i -e 's,/usr/local/bin/perl,%{__perl},' digest-md5-auth.pl
chmod -c 644 digest-md5-auth.pl

# Fix character encoding
%patch0 -p1

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} ';' 2>/dev/null
%{_fixperms} %{buildroot}

# Get rid of sample code that introduces additional dep on perl(OpenLDAP)
rm -f %{buildroot}%{perl_vendorlib}/Authen/digest-md5-auth.pl
magic_rpm_clean.sh

%check


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes README digest-md5-auth.pl
%{perl_vendorlib}/Authen/
%{_mandir}/man3/Authen::DigestMD5.3pm*

%changelog
* Thu Apr 23 2015 Liu Di <liudidi@gmail.com> - 0.04-18
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.04-17
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.04-16
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.04-15
- 为 Magic 3.0 重建

* Sat Jan 28 2012 Liu Di <liudidi@gmail.com> - 0.04-14
- 为 Magic 3.0 重建

* Tue Jan 10 2012 Paul Howarth <paul@city-fan.org> 0.04-13
- Nobody else likes macros for commands
- Use a patch rather than scripted iconv to fix character encoding
- BR: perl(Carp) and perl(Digest::MD5)

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> 0.04-12
- Perl mass rebuild

* Tue Feb  8 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 0.04-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> 0.04-10
- Rebuild to fix problems with vendorarch/lib (#661697)

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> 0.04-9
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> 0.04-8
- Rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 0.04-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 0.04-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.04-5
- Rebuild for new perl

* Fri Aug 10 2007 Paul Howarth <paul@city-fan.org> 0.04-4
- Clarify license as GPL v1 or later, or Artistic (same as perl)
- Add buildreq perl(Test::More)

* Wed Apr 18 2007 Paul Howarth <paul@city-fan.org> 0.04-3
- Add buildreq of perl(ExtUtils::MakeMaker)
- Fix argument order for find with -depth

* Tue Aug 29 2006 Paul Howarth <paul@city-fan.org> 0.04-2
- FE6 mass rebuild

* Fri May 12 2006 Paul Howarth <paul@city-fan.org> 0.04-1
- Initial build
