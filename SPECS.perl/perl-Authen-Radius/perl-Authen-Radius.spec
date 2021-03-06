Name:           perl-Authen-Radius
Version:	0.22
Release:	4%{?dist}
Summary:        Perl Authen::Radius modules
Summary(zh_CN.UTF-8): Perl Authen::Radius 模块
# See LICENSING.txt
License:        Artistic 2.0
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
URL:            http://search.cpan.org/dist/RadiusPerl/
Source0:        http://www.cpan.org/modules/by-module/Authen/RadiusPerl-%{version}.tar.gz
Source1:	LICENSING.txt
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(Data::HexDump) >= 0.02
BuildRequires:  perl(Digest::MD5) >= 2.20, perl(IO) >= 1.12, perl-devel
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
RadiusPerl is a Perl 5 module (Radius.pm) which allows you to 
communicate with a Radius server from Perl. You can just authenticate 
usernames/passwords via Radius, or completely imitate AAA requests and 
process server response.

%description -l zh_CN.UTF-8
这个模块允许你使用 Perl 与 Radius 认证服务器通信。

%prep
%setup -q -n Authen-Radius-%{version}
cp %{SOURCE1} .

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make pure_install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null \;

chmod -R u+rwX,go+rX,go-w %{buildroot}/*
magic_rpm_clean.sh

%check
# Disabled check, as a running Radius-server is needed
#

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes README LICENSING.txt
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.22-4
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.22-3
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.22-2
- 为 Magic 3.0 重建

* Fri Apr 24 2015 Liu Di <liudidi@gmail.com> - 0.22-1
- 更新到 0.22

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.13-15
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.13-14
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.13-13
- 为 Magic 3.0 重建

* Sat Jan 28 2012 Liu Di <liudidi@gmail.com> - 0.13-12
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.13-10
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.13-8
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.13-7
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.13-6
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Sep  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.13-3
- fix license tag (with permission from upstream)

* Thu Feb  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.13-2
- rebuild for new perl

* Sat Mar 10 2007 Andreas Thienemann <andreas@bawue.net> - 0.13-1
- Updated to 0.13
- Added perl-devel BuildReq

* Fri Sep 08 2006 Andreas Thienemann <andreas@bawue.net> - 0.12-3
- FE6 Rebuild

* Thu Apr 13 2006 Andreas Thienemann <andreas@bawue.net> 0.12-2
- Final cleanup for inclusion.

* Wed Mar 29 2006 Andreas Thienemann <andreas@bawue.net> 0.12-1
- Cleaned up for FE
- Specfile autogenerated by cpanspec 1.64.
