Name:           perl-POE-Component-Child
Version:        1.39        
Release:        16%{?dist}
Summary:        Child management component for POE 

Group:          Development/Libraries
License:        GPLv2+
URL:            http://search.cpan.org/dist/POE-Component-Child            
Source0: http://search.cpan.org/CPAN/authors/id/E/EC/ECALDER/POE-Component-Child-%{version}.tar.gz        
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch 
BuildRequires:  perl(POE) >= 0.23
BuildRequires:  perl(Test::Simple)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This POE component serves as a wrapper for POE::Wheel::Run, obviating 
the need to create a session to receive the events it dishes out.

%prep
%setup -q -n POE-Component-Child-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w %{buildroot}/*


%check
# hangs after last test, switch off
##


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*



%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.39-16
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.39-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 1.39-14
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.39-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.39-12
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.39-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.39-10
- 661697 rebuild for fixing problems with vendorach/lib

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.39-9
- Mass rebuild with perl-5.12.0

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.39-8
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.39-7
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.39-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.39-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.39-4
- rebuild for new perl

* Thu Jan 10 2008 Ralf Corsépius <rc040203@freenet.de> 1.39-3
- Update License-tag.
- BR: perl(Test::Simple) (BZ 419631).

* Thu Aug 31 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.39-2
- bump for mass rebuild

* Sun Jul  9 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.39-1
- bump for build & release

* Sat Jul  8 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.39-0.1
- fix changlog version plus licensing

* Fri Jul 07 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.39-0
- Initial spec file for F-E
