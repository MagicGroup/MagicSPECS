Name:           perl-Params-CallbackRequest
Version:        1.20
Release:        4%{?dist}
Summary:        Functional and object-oriented callback architecture
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Params-CallbackRequest/
Source0:        http://www.cpan.org/authors/id/D/DW/DWHEELER/Params-CallbackRequest-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:      noarch
# Module Build
BuildRequires:  perl(Module::Build)
# Module Runtime
BuildRequires:  perl(Attribute::Handlers) >= 0.77
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Class::ISA)
BuildRequires:  perl(Exception::Class) >= 1.10
BuildRequires:  perl(Params::Validate) >= 0.59
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
# Test Suite
BuildRequires:  perl(base)
BuildRequires:  perl(Test::More) >= 0.17
BuildRequires:  perl(Test::Pod)
# Runtime
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Attribute::Handlers) >= 0.77
Requires:       perl(Carp)
Requires:       perl(Class::ISA)
Requires:       perl(Exception::Class) >= 1.10
Requires:       perl(Params::Validate) >= 0.59

# Filter under-specified dependencies
%global __requires_exclude ^perl\\((Exception::Class|Params::Validate)\\)$

%description
Params::CallbackRequest provides functional and object-oriented callbacks
to method and function parameters. Callbacks may be either code references
provided to the new() constructor, or methods defined in subclasses of
Params::Callback. Callbacks are triggered either for every call to the
Params::CallbackRequest request() method, or by specially named keys in the
parameters to request().

%prep
%setup -q -n Params-CallbackRequest-%{version}

# Avoid spurious warning from Test::Pod
mkdir bin

%build
perl Build.PL installdirs=vendor
./Build

%install
rm -rf $RPM_BUILD_ROOT
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
%{_fixperms} $RPM_BUILD_ROOT

%check
./Build test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc Changes README.md
%{perl_vendorlib}/Params/
%{_mandir}/man3/Params::Callback.3pm*
%{_mandir}/man3/Params::CallbackRequest.3pm*
%{_mandir}/man3/Params::CallbackRequest::Exceptions.3pm*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.20-4
- 为 Magic 3.0 重建

* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 1.20-3
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Oct 14 2013 Paul Howarth <paul@city-fan.org> - 1.20-1
- Update to 1.20
  - Moved repository to https://github.com/theory/params-callbackrequest/
  - Switched to a "traditional" Makefile.PL
- Specify all dependencies
- Don't need to remove empty directories from the buildroot
- Drop %%defattr, redundant since rpm 4.4
- Make %%files list more explicit
- Don't use macros for commands

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 25 2013 Petr Pisar <ppisar@redhat.com> - 1.19-13
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 1.19-10
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 1.19-8
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 08 2010 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.19-6
- Add BR: perl(Class::ISA) (Fix FTBFS: BZ 660995).

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.19-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.19-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 01 2008 Steven Pritchard <steve@kspei.com> 1.19-1
- Update to 1.19.
- BR Test::Simple.

* Fri May 16 2008 Steven Pritchard <steve@kspei.com> 1.18-1
- Update to 1.18.

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.17-2
- rebuild for new perl

* Mon Jul 16 2007 Steven Pritchard <steve@kspei.com> 1.17-1
- Specfile autogenerated by cpanspec 1.73.
- Remove redundant explicit perl BR.
- BR Test::More and Test::Pod.
