Name:		perl-Shell
Version:	0.72_01
Release:	1%{?dist}
Summary:	Run shell commands transparently within perl

Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/Shell
Source0:	http://search.cpan.org/CPAN/authors/id/F/FE/FERREIRA/Shell-%{version}.tar.gz


BuildArch:	noarch
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(constant)
BuildRequires:	perl(File::Spec::Functions)


Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))


%description
This package is included as a show case, illustrating a few Perl features. It
shouldn't be used for production programs. Although it does provide a simple
interface for obtaining the standard output of arbitrary commands, there may be
better ways of achieving what you need.


%prep
%setup -q -n Shell-%{version}


%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}/*


%check
make test


%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*


%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.72_01-1
- 更新到 0.72_01

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.72-2
- 为 Magic 3.0 重建

* Tue Feb 05 2013 Normunds Neimanis <fedorapkg at rule.lv> 0.72-1
- Initial package for Fedora
