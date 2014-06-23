Name:           perl-Devel-DProf
Version:        20110802.00
Release:        8%{?dist}
Summary:        Deprecated Perl code profiler
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Devel-DProf/
Source0:        http://www.cpan.org/authors/id/F/FL/FLORA/Devel-DProf-%{version}.tar.gz
# Perl 5.16 compatibility, CPAN RT #70629
Patch0:         Devel-DProf-20110802.00-Work-around-static-XS_Devel__DProf_END-mismatch.patch
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.30
# Run-time
BuildRequires:  perl(if)
BuildRequires:  perl(XSLoader)
# Tests:
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
The Devel::DProf package is a Perl code profiler. This will collect
information on the execution time of a Perl script and of the subs in that
script. This information can be used to determine which subroutines are
using the most time and which subroutines are being called most often. This
information can also be used to create an execution graph of the script,
showing subroutine relationships.

This module is deprecated and new users are advised to use Devel::NYTProf
instead.

%prep
%setup -q -n Devel-DProf-%{version}
%patch0 -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes LICENSE README Todo
%{_bindir}/*
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Devel*
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 20110802.00-8
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20110802.00-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20110802.00-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 20110802.00-5
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20110802.00-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20110802.00-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 20110802.00-2
- Perl 5.16 rebuild

* Mon Jun 25 2012 Petr Pisar <ppisar@redhat.com> 20110802.00-1
- Restore perl 5.16 compatibility (CPAN RT #70629)
