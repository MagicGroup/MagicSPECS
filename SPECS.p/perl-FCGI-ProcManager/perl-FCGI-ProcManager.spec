Name:       perl-FCGI-ProcManager
Version:    0.24
Release:    6%{?dist}
# ProcManager.pm -> LGPLv2, LGPLv3
License:    LGPLv2+
Group:      Development/Libraries
Summary:    A FastCGI process manager
Source:     http://search.cpan.org/CPAN/authors/id/B/BO/BOBTFISH/FCGI-ProcManager-%{version}.tar.gz
Url:        http://search.cpan.org/dist/FCGI-ProcManager
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:  noarch

BuildRequires: perl(ExtUtils::MakeMaker)
# testing...
BuildRequires: perl(Test)

%{?perl_default_filter}

%description
FCGI::ProcManager is used to serve as a FastCGI process manager. By
re-implementing it in perl, developers can more finely tune performance
in their web applications, and can take advantage of copy-on-write
semantics prevalent in UNIX kernel process management.


%prep
%setup -q -n FCGI-ProcManager-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

%check


%files
%doc README ChangeLog COPYING
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.24-6
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.24-5
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.24-4
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 07 2012 Petr Pisar <ppisar@redhat.com> - 0.24-2
- Perl 5.16 rebuild

* Thu Jan 12 2012 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 0.24-1
- Update to 0.24
- Clean up spec file
- Add perl default filter

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.19-8
- Perl mass rebuild

* Thu Jun 09 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.19-7
- Perl 5.14 mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.19-5
- 661697 rebuild for fixing problems with vendorach/lib

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.19-4
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.19-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.19-2
- rebuild against perl 5.10.1

* Tue Aug 11 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.19-1
- auto-update to 0.19 (by cpan-spec-update 0.01)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 15 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.18-1
- update for submission

* Sat Feb 14 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.18-0
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)
