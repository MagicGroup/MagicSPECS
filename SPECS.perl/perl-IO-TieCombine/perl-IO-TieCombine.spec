Name:       perl-IO-TieCombine 
Version:	1.005
Release:	2%{?dist}
# see lib/IO/TieCombine.pm
License:    GPL+ or Artistic
Group:      Development/Libraries
Summary:    Produce tied (and other) separate but combined variables 
Source:     http://search.cpan.org/CPAN/authors/id/R/RJ/RJBS/IO-TieCombine-%{version}.tar.gz 
Url:        http://search.cpan.org/dist/IO-TieCombine
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:  noarch

BuildRequires: perl(ExtUtils::MakeMaker) 
BuildRequires: perl(Test::More)

# a weak description, I know, but upstream didn't have one and it's an
# App::Cmd prereq.
%description
This package allows you to tie separate variables into a combined whole, using
ties and other magic.  This can be very useful when, say, you want a unified
output from various different things that return data in different ways
(STDIN/ERR, scalars, handles, etc).

%prep
%setup -q -n IO-TieCombine-%{version}

perl -pi -e 's|^#!perl|#!%{__perl}|' t/*.t

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

%check


%clean
rm -rf %{buildroot} 

%files
%defattr(-,root,root,-)
%doc Changes LICENSE README t/
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.005-2
- 更新到 1.005

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.004-1
- 更新到 1.004

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.000-13
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.000-12
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.000-11
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.000-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.000-9
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.000-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.000-7
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.000-6
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.000-5
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.000-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.000-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.000-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 01 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.000-1
- cleanup for submission

* Mon Oct 27 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.000-0.1
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.5)

