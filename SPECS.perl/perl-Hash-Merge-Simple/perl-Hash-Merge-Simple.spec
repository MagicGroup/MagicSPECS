Name:       perl-Hash-Merge-Simple 
Version:    0.04 
Release:    16%{?dist}
# lib/Hash/Merge/Simple.pm -> GPL+ or Artistic
License:    GPL+ or Artistic 
Group:      Development/Libraries
Summary:    Recursively merge two or more hashes, simply 
Source:     http://search.cpan.org/CPAN/authors/id/R/RK/RKRIMEN/Hash-Merge-Simple-%{version}.tar.gz 
Url:        http://search.cpan.org/dist/Hash-Merge-Simple
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n) 
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:  noarch

BuildRequires: perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires: perl(Test::Deep)
BuildRequires: perl(Test::More)

%description
Hash::Merge::Simple will recursively merge two or more hashes and return
the result as a new hash reference. The merge function will descend and
merge hashes that exist under the same node in both the left and right
hash, but doesn't attempt to combine arrays, objects, scalars, or
anything else. The rightmost hash also takes precedence, replacing
whatever was in the left hash if a conflict occurs. This code was pretty
much taken straight from Catalyst::Utils, and modified to handle more 
than 2 hashes at the same time.

%prep
%setup -q -n Hash-Merge-Simple-%{version}

perl -pi -e 's/Test::Most/Test::More/g' `find . -type f`

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
%doc Changes README 
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.04-16
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.04-15
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.04-14
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.04-13
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.04-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.04-11
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.04-10
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.04-9
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.04-7
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.04-5
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.04-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.04-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Mar 05 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.04-1
- submission

* Thu Mar 05 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.04-0
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)

