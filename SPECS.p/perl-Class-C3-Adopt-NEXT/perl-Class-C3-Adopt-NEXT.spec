Name:       perl-Class-C3-Adopt-NEXT
Version:    0.13
Release:    7%{?dist}
# lib/Class/C3/Adopt/NEXT.pm -> GPL+ or Artistic
License:    GPL+ or Artistic
Group:      Development/Libraries
Summary:    Reduce one's dependency on NEXT
Source:     http://search.cpan.org/CPAN/authors/id/F/FL/FLORA/Class-C3-Adopt-NEXT-%{version}.tar.gz
Url:        http://search.cpan.org/dist/Class-C3-Adopt-NEXT
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:  noarch

BuildRequires: perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires: perl(List::MoreUtils)
BuildRequires: perl(MRO::Compat)
BuildRequires: perl(NEXT)
# test
BuildRequires: perl(Test::More)
BuildRequires: perl(Test::Exception) >= 0.27

%description
NEXT was a good solution a few years ago, but isn't any more. It's
slow, and the order in which it re-dispatches methods appears random
at times. It also encourages bad programming practices, as you end up
with code to redispatch methods when all you really wanted to do was
run some code before or after a method fired.  However, if you have a large
application, then weaning yourself off 'NEXT' isn't easy.This module is
intended as a drop-in replacement for NEXT, supporting the same interface,
but using Class::C3 to do the hard work. You can then write new code
without 'NEXT', and migrate individual source files to use 'Class::C3'
or method modifiers as appropriate, at whatever pace you're comfortable with.



%prep
%setup -q -n Class-C3-Adopt-NEXT-%{version}

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
%doc Changes
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.13-7
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.13-6
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.13-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.13-2
- 661697 rebuild for fixing problems with vendorach/lib

* Tue Jun  1 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.13-1
- update

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.12-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.12-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 16 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.12-1
- auto-update to 0.12 (by cpan-spec-update 0.01)

* Sat May 23 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.11-2
- README no longer present

* Sat May 23 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.11-1
- auto-update to 0.11 (by cpan-spec-update 0.01)

* Sun May 17 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.10-1
- auto-update to 0.10 (by cpan-spec-update 0.01)
- altered br on perl(Test::Exception) (0 => 0.27)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 22 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.07-1
- update to 0.07

* Tue Feb 10 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.06-1
- brush up for submission

* Tue Feb 10 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.06-0
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)
