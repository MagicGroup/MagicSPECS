Name:           perl-CGI-Simple
Version:	1.115
Release:	3%{?dist}
Summary:        Simple totally OO CGI interface that is CGI.pm compliant
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/CGI-Simple/
Source0:        http://search.cpan.org/CPAN/authors/id/S/SZ/SZABGAB/CGI-Simple-%{version}.tar.gz
# https://github.com/markstos/CGI--Simple/commit/e811ab874a5e0ac8a99e76b645a0e537d8f714da
Patch0:		perl-CGI-Simple-CVE-2010-4411.patch
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker), perl(Test::More), perl(IO::Scalar)
# For perldoc
BuildRequires:	perl(Pod::Perldoc)
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
%{summary}.

%prep
%setup -q -n CGI-Simple-%{version}
%patch0 -p1 -b .CVE-2010-4411
chmod -x Changes README
perldoc -t perlartistic > Artistic
perldoc -t perlgpl > COPYING

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make 

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check


%files
%doc Artistic COPYING Changes README
%{perl_vendorlib}/CGI
%{_mandir}/man3/*.3*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.115-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.115-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.115-1
- 更新到 1.115

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.113-10
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.113-9
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.113-8
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.113-7
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.113-6
- 为 Magic 3.0 重建

* Sun Jan 22 2012 Tom Callaway <spot@fedoraproject.org> - 1.113-5
- rebuild with fixed perldoc BR

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.113-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jun 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.113-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.113-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 21 2011 Tom Callaway <spot@fedoraproject.org> - 1.113-1
- Update to 1.113, apply additional patch to fully resolve CVE-2010-4411

* Wed Dec  1 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.112-2
- patch for randomizing boundary (bz 658973)

* Mon Jul 12 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.112-1
- update to 1.112

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.108-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.108-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.108-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> 1.108-1
- update to 1.108

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.103-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.103-3
- rebuild for new perl

* Wed Nov 28 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.103-2
- BR Test::More

* Wed Nov 28 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.103-1
- bump to 1.103

* Mon Oct 15 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.077-8
- add BR: perl(ExtUtils::MakeMaker)

* Fri Aug 24 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.077-7
- license fix

* Thu Sep 14 2006 Tom "spot" Callaway <tcallawa@redhat.com> 0.077-6
- rebuild for FC-6

* Sun Sep  4 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.077-5
- remove BR: perl
- add license texts

* Fri Jul 29 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.077-4
- cleanup chmod -x

* Wed Jul 27 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.077-3
- add missing documentation
- fix URL

* Fri Jul  8 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.077-2
- cleanups

* Wed Jul  6 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.077-1
- Initial package for Fedora Extras
