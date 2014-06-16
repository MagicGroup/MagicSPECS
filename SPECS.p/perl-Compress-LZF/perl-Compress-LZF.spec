Name:           perl-Compress-LZF
Version:        3.7
Release:        2%{?dist}
Summary:        Extremely light-weight Lempel-Ziv-Free compression
License:        GPL+ or Artistic
# patch to address https://fedoraproject.org/wiki/Common_Rpmlint_issues#incorrect-fsf-address has been sent upstream at https://rt.cpan.org/Ticket/Display.html?id=93643
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Compress-LZF/
Source0:        http://www.cpan.org/modules/by-module/Compress/Compress-LZF-%{version}.tar.gz
Patch1:         compress_lzf_unbundle.patch
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

%patch1 -p1

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
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Mar 8 2014 David Dick <ddick@cpan.org> - 3.7-1
- Initial release
