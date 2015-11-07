Name:           perl-Cflow
Version:        1.053
Release:        34%{?dist}
Summary:        Find flows in raw IP flow files
Group:          Development/Libraries
License:        GPLv2+
URL:            http://net.doit.wisc.edu/~plonka/Cflow/
Source0:        http://net.doit.wisc.edu/~plonka/Cflow/Cflow-%{version}.tar.gz
# http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=628522
Patch0:         perl-Cflow-ccflags.patch

BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  flow-tools-devel
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
Cflow with flow-tools support.  This module implements an API for
processing IP flow accounting information which as been collected from
routers and written into flow files.

%prep
%setup -q -n Cflow-%{version}
%patch0 -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"

make %{?_smp_mflags}


%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check


%files
%doc COPYING README Changes
%{_bindir}/flowdumper
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Cflow.pm
%{_mandir}/man1/flowdumper.1.gz
%{_mandir}/man3/*.3*


%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.053-34
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.053-33
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.053-32
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.053-31
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.053-30
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.053-29
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.053-28
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.053-27
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.053-26
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.053-25
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.053-24
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.053-23
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.053-22
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.053-21
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.053-20
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.053-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Jun 18 2011 Iain Arnell <iarnell@gmail.com> 1.053-18
- rename patch and clarify that it's EU::MM related, not EU::CB

* Fri Jun 17 2011 Iain Arnell <iarnell@gmail.com> 1.053-17
- patch to workaround ExtUtils::CBuilder behavior change
  see http://rt.perl.org/rt3/Public/Bug/Display.html?id=89478
- clean up spec for modern rpmbuild
- use perl_default_filter

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.053-16
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.053-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.053-14
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.053-13
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.053-12
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.053-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.053-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.053-9
Rebuild for new perl

* Sat Feb  9 2008 - Orion Poplawski <orion@cora.nwra.com> - 1.053-8
- Rebuild for gcc 3.4

* Thu Aug 23 2007 - Orion Poplawski <orion@cora.nwra.com> - 1.053-7
- Rebuild for BuildID

* Wed Aug 15 2007 - Orion Poplawski <orion@cora.nwra.com> - 1.053-6
- Update License tag
- Add BR perl(ExtUtils::MakeMaker)

* Thu Sep  7 2006 - Orion Poplawski <orion@cora.nwra.com> - 1.053-5
- Rebuild for FC6

* Fri Feb 24 2006 - Orion Poplawski <orion@cora.nwra.com> - 1.053-4
- Rebuild for FC5 gcc/glibc changes

* Fri Oct 21 2005 - Orion Poplawski <orion@cora.nwra.com> - 1.053-3
- Remove BR zlib-devel (Bug #171206 resolved)

* Wed Oct 19 2005 - Orion Poplawski <orion@cora.nwra.com> - 1.053-2
- Add BR zlib-devel because flow-tools-devel does not properly
  include it (Bug #171206)

* Tue Oct 11 2005 - Orion Poplawski <orion@cora.nwra.com> - 1.053-1
- Initial version
