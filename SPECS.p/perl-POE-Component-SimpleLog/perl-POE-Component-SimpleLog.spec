Name:           perl-POE-Component-SimpleLog
Version:        1.05
Release:        12%{?dist}
Summary:        A simple logging system for POE 

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/POE-Component-SimpleLog            
Source0: http://search.cpan.org/CPAN/authors/id/A/AP/APOCAL/POE-Component-SimpleLog-%{version}.tar.gz        
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch 
BuildRequires:  perl(POE)
BuildRequires:  perl(Test::More)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This module is a vastly simplified logging system that can do nice stuff.
Think of this module as a dispatcher for various logs.

This module *DOES NOT* do anything significant with logs, it simply routes
them to the appropriate place ( Events )

You register a log that you are interested in, by telling SimpleLog the target
session and target event. Once that is done, any log messages your program
generates ( sent to SimpleLog of course ) will be massaged, then sent to the
target session / target event for processing.

This enables an interesting logging system that can be changed during runtime
and allow pluggable interpretation of messages.


%prep
%setup -q -n POE-Component-SimpleLog-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
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
%doc README Changes examples/
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*


%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.05-12
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 1.05-10
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.05-8
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.05-6
- 661697 rebuild for fixing problems with vendorach/lib

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.05-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.05-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Oct 26 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.05-1
- update to 1.05

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.04-3
Rebuild for new perl

* Thu Jan 10 2008 Ralf Corsépius <rc040203@freenet.de> 1.04-2
- Update License-tag.
- BR: perl(Test::More) (BZ 419631).
- Minor spec cleanup.

* Wed Oct 04 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.04-1
- update to 1.04
- misc spec cleanup 
- add Changes, examples/ to %%doc

* Thu Aug 31 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.03-2
- bump for mass rebuild

* Sun Jul  9 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.03-1
- bump for build/release

* Fri Jul 07 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.03-0
- Initial spec file for F-E
