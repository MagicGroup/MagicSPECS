Name:           perl-Bit-Vector
Version:	7.4
Release:	3%{?dist}
Summary:        Efficient bit vector, set of integers and "big int" math library
Summary(zh_CN.UTF-8): 高效位向量，整数和大整数集合的数学库

Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
# Clarified by a private mail from the author:
License:        (GPLv2+ or Artistic) and LGPLv2+
URL:            http://search.cpan.org/dist/Bit-Vector/
Source0:        http://www.cpan.org/authors/id/S/ST/STBEY/Bit-Vector-%{version}.tar.gz

BuildRequires:  perl(Carp::Clan) >= 5.4
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Storable)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%{?perl_default_filter}

%description
Bit::Vector is an efficient C library which allows you to handle bit
vectors, sets (of integers), "big integer arithmetic" and boolean
matrices, all of arbitrary sizes.

The library is efficient (in terms of algorithmical complexity) and
therefore fast (in terms of execution speed) for instance through the
widespread use of divide-and-conquer algorithms.

%description -l zh_CN.UTF-8
高效位向量，整数和大整数集合的数学库。

%prep
%setup -q -n Bit-Vector-%{version} 
chmod 644 examples/*.pl
perl -pi -e 's|^#!/usr/local/bin/perl\b|#!%{__perl}|' examples/benchmk1.pl
perl -pi -e 's|^#!perl\b|#!%{__perl}|' \
    examples/{benchmk{2,3},primes,SetObject}.pl

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'
%{_fixperms} %{buildroot}/*
magic_rpm_clean.sh

%check


%files
%doc Artistic.txt GNU_GPL.txt GNU_LGPL.txt
%doc CHANGES.txt CREDITS.txt README.txt examples/
%{perl_vendorarch}/Bit/
%{perl_vendorarch}/auto/Bit/
%{_mandir}/man3/*.3*


%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 7.4-3
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 7.4-2
- 为 Magic 3.0 重建

* Sat Apr 25 2015 Liu Di <liudidi@gmail.com> - 7.4-1
- 更新到 7.4

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 7.2-12
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 7.2-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 7.2-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 7.2-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 7.2-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 7.2-7
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 7.2-6
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 7.2-5
- 为 Magic 3.0 重建

* Wed Sep 19 2012 Jitka Plesnikova <jplesnik@redhat.com> - 7.2-4
- Use latest version of Bit-Vector-7.2.tar.gz from CPAN

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 7.2-2
- Perl 5.16 rebuild

* Wed Mar 14 2012 Petr Šabata <contyk@redhat.com> - 7.2-1
- 7.2 bumpity
- Remove command macros

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug  2 2011 Marcela Mašláňová <mmaslano@redhat.com> - 7.1-7
- filter *.so library incorectly provided by package
- clean spec file

* Wed Jun 29 2011 Marcela Mašláňová <mmaslano@redhat.com> - 7.1-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 7.1-4
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 7.1-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 7.1-2
- rebuild against perl 5.10.1

* Fri Oct  2 2009 Stepan Kasal <skasal@redhat.com> - 7.1-2
- fixed the license tag

* Thu Oct  1 2009 Stepan Kasal <skasal@redhat.com> - 7.1-1
- new upstream release

* Tue Aug  4 2009 Stepan Kasal <skasal@redhat.com> - 6.6-1
- new upstream release

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 6.4-8
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 6.4-7
- Autorebuild for GCC 4.3

* Tue Feb  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 6.4-6
- fix license tag, rebuild for new perl

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 6.4-5
- Rebuild for selinux ppc32 issue.

* Fri Jul 06 2007 Robin Norwood <rnorwood@redhat.com> 6.4-4
- Resolves: rhbz#247212
- Fix broken perl_provides script - it was removing both the versioned
  and unversioned Provides: perl(Bit::Vector)

* Sat Jun 30 2007 Steven Pritchard <steve@kspei.com> 6.4-3
- Fix find option order.
- Use fixperms macro instead of our own chmod incantation.
- Remove check macro cruft.
- Improve Summary.
- Remove redundant perl build dependency.
- BR ExtUtils::MakeMaker.
- Set OPTIMIZE when we run Makefile.PL, not make.
- BR perl(Carp::Clan) instead of perl-Carp-Clan.
- Remove redundant Carp::Clan dependency.
- Filter unversioned Provides: perl(Bit::Vector)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 6.4-2.2.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 6.4-2.2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 6.4-2.2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 6.4-2.2
- rebuild for new perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Sat Apr  2 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 6.4-1
- Update to 6.4.
- Bring up to date with current Fedora.Extras perl spec template.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Chip Turner <cturner@redhat.com> 6.3-1
- update to 6.3

* Wed Jul 16 2003 Elliot Lee <sopwith@redhat.com> 
- Rebuild, remove unpackaged files

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Aug 15 2002 Chip Turner <cturner@redhat.com>
- file list fix for Clan stuff

* Tue Aug  6 2002 Chip Turner <cturner@redhat.com>
- automated release bump and build

* Wed Jan 30 2002 cturner@redhat.com
- Specfile autogenerated

