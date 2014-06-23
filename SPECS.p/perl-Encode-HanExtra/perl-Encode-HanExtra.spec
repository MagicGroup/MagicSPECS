Name:           perl-Encode-HanExtra
Version:        0.23
Release:        9%{?dist}
Summary:        Extra sets of Chinese encodings
License:        MIT
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Encode-HanExtra/
Source0:        http://www.cpan.org/modules/by-module/Encode/Encode-HanExtra-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
Perl 5.7.3 and later ships with an adequate set of Chinese encodings,
including the commonly used CP950, CP936 (also known as GBK), Big5 (alias
for Big5-Eten), Big5-HKSCS, EUC-CN, HZ, and ISO-IR-165.
However, the numbers of Chinese encodings are staggering, and a complete
coverage will easily increase the size of perl distribution by several
megabytes; hence, this CPAN module tries to provide the rest of them.
If you are using Perl 5.8 or later, Encode::CN and Encode::TW will
automatically load the extra encodings for you, so there's no need to
explicitly write use Encode::HanExtra if you are using one of them already.

%prep
%setup -q -n Encode-HanExtra-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
# Remove the next line from noarch packages (unneeded)
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
%{_fixperms} $RPM_BUILD_ROOT/*

%check


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorarch}/*
%exclude %dir %{perl_vendorarch}/auto/
%{_mandir}/man3/*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.23-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.23-8
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.23-7
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.23-6
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.23-5
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 21 2011 Xavier Bachelot <xavier@bachelot.org> 0.23-3
- Fix bad copy/paste.

* Tue Dec 20 2011 Xavier Bachelot <xavier@bachelot.org> 0.23-2
- Follow the rpmdevtools perl spec template to fix packaging bugs.

* Tue Nov 29 2011 Xavier Bachelot <xavier@bachelot.org> 0.23-1
- Initial Fedora release.
