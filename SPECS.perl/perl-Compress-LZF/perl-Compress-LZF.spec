Name:           perl-Compress-LZF
Version:	3.8
Release:	1%{?dist}
Summary:        Extremely light-weight Lempel-Ziv-Free compression
License:        GPL+ or Artistic
# patch to address https://fedoraproject.org/wiki/Common_Rpmlint_issues#incorrect-fsf-address has been sent upstream at https://rt.cpan.org/Ticket/Display.html?id=93643
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Compress-LZF/
Source0:        http://www.cpan.org/modules/by-module/Compress/Compress-LZF-%{version}.tar.gz
BuildRequires:  liblzf-devel
BuildRequires:  perl
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Storable)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This is Perl binding to the LZF compression library.

%prep
%setup -q -n Compress-LZF-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes COPYING COPYING.Artistic COPYING.GNU README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Compress*
%{_mandir}/man3/*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 3.8-1
- 更新到 3.8

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 3.7-4
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 3.7-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Mar 8 2014 David Dick <ddick@cpan.org> - 3.7-1
- Initial release
