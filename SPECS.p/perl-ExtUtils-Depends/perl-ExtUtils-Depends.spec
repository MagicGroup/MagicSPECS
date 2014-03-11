Name:           perl-ExtUtils-Depends
Version:        0.304
Release:        2%{?dist}
Summary:        Easily build XS extensions that depend on XS extensions
Summary(zh_CN): 基于 XS 扩展简单建立 XS 扩展
License:        GPL+ or Artistic
Group:          Development/Libraries
Group(zh_CN):	开发/库
URL:            http://search.cpan.org/dist/ExtUtils-Depends/
Source0:        http://www.cpan.org/authors/id/T/TS/TSCH/ExtUtils-Depends-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This module tries to make it easy to build Perl extensions that use
functions and typemaps provided by other perl extensions. This means that a
perl extension is treated like a shared library that provides also a C and
an XS interface besides the perl one.

%description -l zh_CN
基于 XS 扩展简单建立 XS 扩展。

%prep
%setup -q -n ExtUtils-Depends-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.304-2
- 为 Magic 3.0 重建


