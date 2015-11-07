Name:           perl-Crypt-Blowfish_PP
Version:        1.12
Release:        9%{?dist}
Summary:        Blowfish encryption algorithm implemented purely in Perl
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/~mattbm/Crypt-Blowfish_PP-1.12/Blowfish_PP.pm
Source0:        http://search.cpan.org/CPAN/authors/id/M/MA/MATTBM/Crypt-Blowfish_PP-1.12.tar.gz
BuildArch:      noarch

BuildRequires:  perl(ExtUtils::MakeMaker)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
The Crypt::Blowfish_PP module provides for users to use the Blowfish
encryption algorithm in perl. The implementation is entirely Object
Oriented, as there is quite a lot of context inherent in making blowfish
as fast as it is. The key is anywhere between 64 and 448 bits (8 and 56
bytes), and should be passed as a packed string. The transformation itself
is a 16-round Feistel Network, and operates on a 64 bit block.


%prep
%setup -q -n Crypt-Blowfish_PP-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%check



%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
%{_fixperms} $RPM_BUILD_ROOT/*


%files
%doc README CHANGELOG
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.12-9
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.12-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.12-7
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.12-6
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.12-5
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 1.12-3
- Perl 5.16 rebuild

* Thu Feb 23 2012 Alec Leamas <alec@nowhere.com>             1.12-2
- Fixing review remarks
* Wed Feb 22 2012 Alec Leamas <alec@nowhere.com>             1.12-2
- Re-enabling Requires: perl(:MODULE_COMPAT...)
* Tue Feb 21 2012 Alec Leamas <alec@nowhere.com>             1.12-2
- Removing defattr
* Sat Jan 31 2012 Alec Leamas <alec@nowhere.com>             1.12-1
- Intial packaging
