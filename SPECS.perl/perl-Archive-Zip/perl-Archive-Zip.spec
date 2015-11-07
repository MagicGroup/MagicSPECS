Name:           perl-Archive-Zip
Version:	1.53
Release:	2%{?dist}
Summary:        Perl library for accessing Zip archives
Summary(zh_CN.UTF-8): 访问 Zip 归档的 Perl 库

Group:          Development/Libraries
Group(zh_CN.UTF-8):	开发/库
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Archive-Zip/
Source0:        http://search.cpan.org/CPAN/authors/id/P/PH/PHRED/Archive-Zip-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  perl(Compress::Zlib) >= 1.14
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Which) >= 0.05
BuildRequires:  perl(Test::More)
BuildRequires:  unzip
BuildRequires:  zip

Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
The Archive::Zip module allows a Perl program to create, manipulate,
read, and write Zip archive files.
Zip archives can be created, or you can read from existing zip files.
Once created, they can be written to files, streams, or strings.
Members can be added, removed, extracted, replaced, rearranged, and
enumerated.  They can also be renamed or have their dates, comments,
or other attributes queried or modified.  Their data can be compressed
or uncompressed as needed.  Members can be created from members in
existing Zip files, or from existing directories, files, or strings.

%description -l zh_CN.UTF-8
这个包允许 Perl 程序建立，处理，读取和写入 Zip 归档文件。

%prep
%setup -q -n Archive-Zip-%{version}
%{__perl} -pi -e 's|^#!/bin/perl|#!%{__perl}|' examples/*.pl
%{__perl} -pi -e 's|^#!/usr/local/bin/perl|#!%{__perl}|' examples/selfex.pl


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
%{_fixperms} $RPM_BUILD_ROOT/*
magic_rpm_clean.sh

%check



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/crc32
%{perl_vendorlib}/Archive/
%{_mandir}/man3/Archive*.3*


%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.53-2
- 更新到 1.53

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.50-1
- 更新到 1.50

* Thu Apr 23 2015 Liu Di <liudidi@gmail.com> - 1.46-1
- 更新到 1.46

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.31_04-4
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.31_04-3
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.31_04-2
- 为 Magic 3.0 重建


