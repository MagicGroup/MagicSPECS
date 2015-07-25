Name:           perl-Class-InsideOut
Version:        1.10
Release:        10%{?dist}
Summary:        A safe, simple inside-out object construction kit 

Group:          Development/Libraries
License:        ASL 2.0
URL:            http://search.cpan.org/dist/Class-InsideOut            
Source0: http://search.cpan.org/CPAN/authors/id/D/DA/DAGOLDEN/Class-InsideOut-%{version}.tar.gz 
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  dos2unix
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Class::ISA)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This is a simple, safe and streamlined toolkit for building inside-out
objects. Unlike most other inside-out object building modules already on CPAN,
this module aims for minimalism and robustness:

* Does not require derived classes to subclass it
* Uses no source filters, attributes or CHECK blocks
* Supports any underlying object type including foreign
  inheritance
* Does not leak memory on object destruction
* Overloading-safe
* Thread-safe for Perl 5.8 or better
* mod_perl compatible
* Makes no assumption about inheritance or initializer needs

It provides the minimal support necessary for creating safe inside-out 
objects and generating flexible accessors.

%prep
%setup -q -n Class-InsideOut-%{version}

# fix encoding
dos2unix Todo

# make sure doc/tests don't generate provides
# note we first filter out the bits in _docdir...
cat << \EOF > %{name}-prov
#!/bin/sh
%{__perl_provides} `perl -p -e 's|\S+%{_docdir}/%{name}-%{version}\S+||'`
EOF

%define __perl_provides %{_builddir}/Class-InsideOut-%{version}/%{name}-prov
chmod +x %{__perl_provides}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

%check



%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
# note that perl(base) ends up as a dep from the code under t/Object; however
# perl(base) is provided by perl, which is already a dep of this package, so
# no big deal.
%doc README Todo Changes LICENSE examples/ t/Object/
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%changelog
* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.10-10
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.10-9
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.10-8
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.10-7
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.10-5
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 06 2010 Ralf Corsépius <corsepiu@fedora.org> - 1.10-3
- Remove BR: perl.
- Add BR: perl(Class::ISA) (Fix FTBS).

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.10-2
- Mass rebuild with perl-5.12.0

* Fri Jan 15 2010 Ralf Corsépius <corsepiu@fedora.org> - 1.10-1
- Upstream update (BZ #539136)

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.09-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.09-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.09-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Oct 21 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.09-1
- update to 1.09
- filter provides
- note license change: perl -> ASL 2.0

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.06-2.2
Rebuild for new perl

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.06-1.2
- add BR: perl(Test::More)

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.06-1.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Mon Feb 19 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.06-1
- update to 1.06
- drop br's on modules required for skipped "author tests"

* Tue Nov 07 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.03-1
- update to 1.03
- minor spec tweaks

* Thu Aug 31 2006 Chris Weyl <cweyl.drew.edu> 1.02-3
- bump for mass rebuild

* Wed Aug 16 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.02-2
- *sigh* tagging issues, so bump

* Wed Aug 16 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.02-1
- update to 1.02
- dropped some depreciated spec bits

* Fri Jul 28 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.01-0
- update to 1.01

* Thu Jul  6 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.00-1
- bump for F-E release

* Sat Jul 01 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.00-0
- Initial spec file for F-E
