Name:           perl-CGI-Session
Version:	4.48
Release:	2%{?dist}
Summary:        Persistent session data in CGI applications
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/CGI-Session/
Source0:        http://www.cpan.org/modules/by-module/CGI/CGI-Session-%{version}.tar.gz
# Fix deprecated use of qw//, RHBZ #754689, CPAN RT #69048
Patch0:         CGI-Session-4.35-qw.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(CGI)

BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Carp)
BuildRequires:  perl(CGI)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(DBD::Pg)
BuildRequires:  perl(DB_File)
BuildRequires:  perl(DBI)
BuildRequires:  perl(Digest::MD5)
BuildRequires:  perl(encoding)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(FreezeThaw)
BuildRequires:  perl(Safe)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Storable)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Text::Abbrev)
BuildRequires:  perl(Text::Wrap)

%description
CGI-Session is a Perl5 library that provides an easy, reliable and modular
session management system across HTTP requests. Persistency is a key
feature for such applications as shopping carts, login/authentication
routines, and application that need to carry data across HTTP requests.
CGI::Session does that and many more.

%prep
%setup -q -n CGI-Session-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}
chmod 644 examples/*

%install
rm -rf %{buildroot}

make pure_install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*
magic_rpm_clean.sh

%check


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes examples README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 4.48-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 4.48-1
- 更新到 4.48

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 4.35-26
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 4.35-25
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 4.35-24
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 4.35-23
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 4.35-22
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 4.35-21
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 4.35-20
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 4.35-19
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 4.35-18
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 4.35-17
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 4.35-16
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 4.35-15
- 为 Magic 3.0 重建

* Tue Aug 21 2012 Petr Pisar <ppisar@redhat.com> - 4.35-14
- Fix deprecated use of qw// (bug #754689)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.35-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 4.35-12
- Perl 5.16 rebuild
- Specify all dependencies

* Tue Jan 17 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 4.35-11
- Add BR: perl(Digest::MD5) (Fix mass rebuild FTBS).

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.35-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4.35-9
- Perl mass rebuild

* Sun May 29 2011 Iain Arnell <iarnell@gmail.com> 4.35-8
- explicitly require perl(CGI)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.35-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 4.35-6
- 661697 rebuild for fixing problems with vendorach/lib
- add BR CGI

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 4.35-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 4.35-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.35-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.35-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Aug  1 2008 Andreas Thienemann <athienem@redhat.com> 4.35-1
- update to current 4.35, 4.31 release was broken.

* Fri Aug  1 2008 Andreas Thienemann <athienem@redhat.com> 4.31-1
- update to 4.31

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4.20-4
- rebuild for new perl

* Sun Jan 27 2008 Andreas Thienemann <andreas@bawue.net> 4.20-3
- Added Test::More to the BuildReqs

* Sat Mar 17 2007 Andreas Thienemann <andreas@bawue.net> 4.20-2
- Fixed perl-devel req

* Sat Mar 10 2007 Andreas Thienemann <andreas@bawue.net> 4.20-1
- Cleaned up for FE
- Specfile autogenerated by cpanspec 1.69.1.
