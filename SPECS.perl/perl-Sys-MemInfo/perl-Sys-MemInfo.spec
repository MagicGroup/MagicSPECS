Name:           perl-Sys-MemInfo
Version:	0.98
Release:	1%{?dist}
Summary:        Memory information as Perl module
# README:       GPLv1+ or Artistic
# MemInfo.pm    LGPLv2+
# <https://rt.cpan.org/Public/Bug/Display.html?id=80636>
License:        (GPLv1+ or Artistic) and LGPLv2+
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Sys-MemInfo/
Source0:        http://search.cpan.org/CPAN/authors/id/S/SC/SCRESTO/Sys-MemInfo-%{version}.tar.gz
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Copy)
# Run-time:
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Exporter)
# Tests:
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Data::Dumper)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
Sys::MemInfo returns the total amount of free and used physical memory in
bytes in totalmem and freemem variables.

%prep
%setup -q -n Sys-MemInfo-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Sys*
%{_mandir}/man3/*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.98-1
- 更新到 0.98

* Thu Jul 03 2014 Liu Di <liudidi@gmail.com> - 0.91-10
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.91-7
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 05 2012 Petr Pisar <ppisar@redhat.com> - 0.91-5
- Change license from (LGPLv2+) to ((GPLv1+ or Artistic) and LGPLv2+)
  (CPAN RT #80636)

* Mon Nov 05 2012 Petr Pisar <ppisar@redhat.com> - 0.91-4
- Improve description
- Specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.91-2
- Perl 5.16 rebuild

* Fri May 04 2012 jsynacek@redhat.com 0.91-1
- Initial release
