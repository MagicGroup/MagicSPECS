Name:		perl-Devel-EnforceEncapsulation
Version:	0.50
Release:	8%{?dist}
Summary:	Find access violations to blessed objects
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/Devel-EnforceEncapsulation/
Source0:	http://search.cpan.org/CPAN/authors/id/C/CL/CLOTHO/Devel-EnforceEncapsulation-%{version}.tgz
BuildArch:	noarch
BuildRequires:	perl(Carp)
BuildRequires:	perl(English)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Test::Pod)
BuildRequires:	perl(Test::Pod::Coverage)
Requires:	perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
Encapsulation is the practice of creating subroutines to access the properties
of a class instead of accessing those properties directly. The advantage of
good encapsulation is that the author is permitted to change the internal
implementation of a class without breaking its usage.

Object-oriented programming in Perl is most commonly implemented via blessed
hashes. This practice makes it easy for users of a class to violate
encapsulation by simply accessing the hash values directly. Although less
common, the same applies to classes implemented via blessed arrays, scalars,
filehandles, etc.

This module is a hack to block those direct accesses. If you try to access a
hash value of an object from its own class, or a superclass or subclass, all
goes well. If you try to access a hash value from any other package, an
exception is thrown. The same applies to the scalar value of a blessed scalar,
entry in a blessed array, etc.

To be clear: this class is NOT intended for strict enforcement of
encapsulation. If you want bullet-proof encapsulation, use inside-out objects
or the like. Instead, this module is intended to be a development or debugging
aid in catching places where direct access is used against classes implemented
as blessed hashes.

To repeat: the encapsulation enforced here is a hack and is easily
circumvented. Please use this module for good (finding bugs), not evil (making
life harder for downstream developers).

%prep
%setup -q -n Devel-EnforceEncapsulation-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} \; 2>/dev/null
%{_fixperms} %{buildroot}

%check
 AUTHOR_TEST=1 AUTHOR_TEST_CDOLAN=1

%files
%defattr(-,root,root,-)
%doc CHANGES LICENSE README index.html
%{perl_vendorlib}/Devel/
%{_mandir}/man3/Devel::EnforceEncapsulation.3pm*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.50-8
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.50-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.50-6
- Perl 5.16 rebuild

* Wed Jan 11 2012 Paul Howarth <paul@city-fan.org> - 0.50-5
- BR: perl(Carp) and perl(English)

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.50-4
- Perl mass rebuild

* Mon Apr 11 2011 Paul Howarth <paul@city-fan.org> - 0.50-3
- Clean up for modern rpmbuild

* Mon Apr 11 2011 Paul Howarth <paul@city-fan.org> - 0.50-2
- Nobody else likes macros for commands

* Fri Mar 18 2011 Paul Howarth <paul@city-fan.org> - 0.50-1
- Initial RPM version
