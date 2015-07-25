Name:		perl-Archive-Any
Version:	0.0942
Release:	1%{?dist}
Summary:	Single interface to deal with file archives
Summary(zh_CN.UTF-8): 与归档文件打交道的单一接口
License:	GPL+ or Artistic
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
URL:		http://search.cpan.org/dist/Archive-Any/
Source0:	http://search.cpan.org/CPAN/authors/id/O/OA/OALDERS/Archive-Any-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
# Build
BuildRequires:	perl(Module::Build)
# Module
BuildRequires:	perl(Archive::Tar) >= 0.22
BuildRequires:	perl(Archive::Zip) >= 1.07
BuildRequires:	perl(Cwd)
BuildRequires:	perl(File::MMagic) >= 1.27
BuildRequires:	perl(File::Spec::Functions)
BuildRequires:	perl(MIME::Types) >= 1.16
BuildRequires:	perl(Module::Find) >= 0.05
# Test suite
BuildRequires:	perl(Test::More) >= 0.4
BuildRequires:	perl(Test::Pod)
BuildRequires:	perl(Test::Pod::Coverage)
BuildRequires:	perl(Test::Warn)
# Runtime
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This module is a single interface for manipulating different archive
formats. Tarballs, zip files, etc.

%description -l zh_CN.UTF-8
与归档文件打交道的单一接口，支持 tar 包，zip 文件等。

%prep
%setup -q -n Archive-Any-%{version}

%build
perl Build.PL installdirs=vendor
./Build

%install
rm -rf %{buildroot}
./Build install destdir=%{buildroot} create_packlist=0
find %{buildroot} -depth -type d -exec rmdir {} \; 2>/dev/null
%{_fixperms} %{buildroot}
magic_rpm_clean.sh

%check
./Build test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes README t/
%{perl_vendorlib}/Archive/
%{_mandir}/man3/Archive::Any.3pm*
%{_mandir}/man3/Archive::Any::Plugin.3pm*
%{_mandir}/man3/Archive::Any::Plugin::Tar.3pm*
%{_mandir}/man3/Archive::Any::Plugin::Zip.3pm*
%{_mandir}/man3/Archive::Any::Tar.3pm*
%{_mandir}/man3/Archive::Any::Zip.3pm*

%changelog
* Thu Apr 23 2015 Liu Di <liudidi@gmail.com> - 0.0942-1
- 更新到 0.0942

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.0932-19
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.0932-18
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.0932-17
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.0932-16
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.0932-15
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.0932-14
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.0932-13
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.0932-12
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0932-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 0.0932-10
- Perl 5.16 rebuild

* Tue Jan 17 2012 Paul Howarth <paul@city-fan.org> - 0.0932-9
- Spec clean-up:
  - Drop redundant buildreq perl(Test::Perl::Critic)
  - Make %%files list more explicit
  - Group buildreqs by build/module/test
  - Don't use macros for commands
  - Use tabs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0932-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.0932-7
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0932-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.0932-5
- Rebuild to fix problems with vendorarch/lib (#661697)

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.0932-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.0932-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0932-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jun 07 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.0932-1
- auto-update to 0.0932 (by cpan-spec-update 0.01)
- altered br on perl(Test::More) (0 => 0.4)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.093-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 08 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.093-3
- rebuild for new perl

* Wed May 09 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.093-2
- bump

* Sat May 05 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.093-1
- Specfile autogenerated by cpanspec 1.71.