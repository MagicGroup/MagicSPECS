Name:           perl-MooseX-AttributeHelpers
Version:	0.24
Release:	2%{?dist}
Summary:        Extended Moose attribute interfaces
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/MooseX-AttributeHelpers/
Source0:        http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/MooseX-AttributeHelpers-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires:  perl(Moose)           >= 0.56
BuildRequires:  perl(Test::Exception) >= 0.21
BuildRequires:  perl(Test::Moose)
BuildRequires:  perl(Test::More)      >= 0.62

### auto-added reqs!
Requires:  perl(Moose) >= 0.56

%description
While Moose attributes provide you with a way to name your accessors,
readers, writers, clearers and predicates, this library provides commonly
used attribute helper methods for more specific types of data.

%prep
%setup -q -n MooseX-AttributeHelpers-%{version}

# first filter out the bits in _docdir...
cat << \EOF > %{name}-prov
#!/bin/sh
FOO=`perl -p -e 's|%{buildroot}%{_docdir}/%{name}-%{version}\S+||'`
%{__perl_provides} $FOO
EOF

%define __perl_provides %{_builddir}/MooseX-AttributeHelpers-%{version}/%{name}-prov
chmod +x %{__perl_provides}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} +
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*

%check
make test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Mon Sep 14 2015 Liu Di <liudidi@gmail.com> - 0.24-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.24-1
- 更新到 0.24

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.23-9
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.23-7
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.23-5
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.23-3
- 661697 rebuild for fixing problems with vendorach/lib

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.23-2
- Mass rebuild with perl-5.12.0

* Wed Jan 20 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.23-1
- auto-update to 0.23 (by cpan-spec-update 0.01)

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.22-2
- rebuild against perl 5.10.1

* Sat Sep 19 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.22-1
- auto-update to 0.22 (by cpan-spec-update 0.01)

* Tue Jul 28 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.21-1
- auto-update to 0.21 (by cpan-spec-update 0.01)
- added a new br on perl(Test::Moose) (version 0)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 16 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.19-1
- drop br on CPAN
- auto-update to 0.19 (by cpan-spec-update 0.01)
- added a new req on perl(Moose) (version 0.56)

* Wed May 27 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.17-1
- auto-update to 0.17 (by cpan-spec-update 0.01)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)

* Tue May 26 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.16-2
- add br on CPAN until M::I bundled version is updated

* Mon Apr 06 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.16-1
- update to 0.16

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 08 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.14-1
- updating to 0.14
- POD tests are now explicitly for author/maintainers only; removing deps

* Sat Sep 06 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.13-1
- update to 0.13
- note BR on Moose is now at 0.56 and is not optional :)

* Mon Jun 30 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.12-2
- ...and fix filtering.  heh.

* Mon Jun 30 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.12-1
- update to 0.12
- switch to Module::Install incantations
- update BR's
- update provides filtering

* Wed May 28 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.09-1
- update to 0.09

* Wed Mar 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.07-2
- rebuild for new perl

* Sat Jan 05 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.07-1
- update to 0.07

* Fri Dec 14 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.06-1
- update to 0.06

* Mon Nov 26 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.05-2
- bump

* Sun Nov 25 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.05-1
- update to 0.05

* Sun Oct 28 2007 Chris Weyl <cweyl@alumni.drew.edu> 0.03-1
- Specfile autogenerated by cpanspec 1.73.
