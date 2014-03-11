Name:           perl-Encode-EUCJPASCII
Version:        0.03
Release:        4%{?dist}
Summary:        EucJP-ascii - An eucJP-open mapping
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Encode-EUCJPASCII/
Source0:        http://www.cpan.org/modules/by-module/Encode/Encode-EUCJPASCII-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Encode)
BuildRequires:  perl(XSLoader)
BuildRequires:  perl(base)
BuildRequires:  perl(Encode::CJKConstants)
BuildRequires:  perl(Encode::JP::JIS7)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
This module provides eucJP-ascii, one of eucJP-open mappings, and its
derivative.

%prep
%setup -q -n Encode-EUCJPASCII-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
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

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.03-4
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.03-3
- 为 Magic 3.0 重建

* Thu Jan 05 2012 Xavier Bachelot <xavier@bachelot.org> 0.03-2
- Follow the rpmdevtools perl spec template to fix packaging bugs.
- Add missing implicit BuildRequires.

* Tue Nov 29 2011 Xavier Bachelot <xavier@bachelot.org> 0.03-1
- Initial Fedora release.
