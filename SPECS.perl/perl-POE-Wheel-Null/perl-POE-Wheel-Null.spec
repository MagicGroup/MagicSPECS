Name:           perl-POE-Wheel-Null
Version:        0.01        
Release:        18%{?dist}
Summary:        POE Wheel that does puts data nowhere, and sends nothing

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/POE-Wheel-Null            
Source0: http://search.cpan.org/CPAN/authors/id/H/HA/HACHI/POE-Wheel-Null-%{version}.tar.gz        
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(POE)
BuildRequires:  perl(Test::More)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# I'm not sure why this isn't automagically found, but...
Requires:       perl(POE)

%description
POE::Wheel::Null creates a wheel which doesn't do anything upon put(), and
doesn't send any events to the current session.

Its function is the same as those pipes in the Enterprise's engine room 
marked "GNDN".


%prep
%setup -q -n POE-Wheel-Null-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w %{buildroot}/*


%check



%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.01-18
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.01-17
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.01-16
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.01-15
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.01-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 0.01-13
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.01-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.01-11
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.01-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.01-9
- 661697 rebuild for fixing problems with vendorach/lib

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.01-8
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.01-7
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.01-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.01-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.01-4
- rebuild for new perl

* Thu Jan 10 2008 Ralf Corsépius <rc040203@freenet.de> 0.01-3
- Update License-tag.
- BR perl(Test::More) (BZ 419631).
- Minor spec cleanup.

* Thu Aug 31 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.01-2
- bump for mass rebuild

* Wed Jul 26 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.01-1
- bump and build

* Mon Jul 17 2006 Chris Weyl <cweyl@alumni.drew.edu> 0.01-0
- Initial spec file for F-E
