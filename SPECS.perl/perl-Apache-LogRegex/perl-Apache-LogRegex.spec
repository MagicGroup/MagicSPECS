Name:           perl-Apache-LogRegex
Version:	1.71
Release:	2%{?dist}
Summary:        Parse a line from an Apache logfile into a hash
Summary(zh_CN.UTF-8): 解析 Apache 日志文件的一行到哈希
License:        GPL+ or Artistic
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
URL:            http://search.cpan.org/dist/Apache-LogRegex/
Source0:        http://www.cpan.org/authors/id/S/SP/SPACEBAT/Apache-LogRegex-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Designed as a simple class to parse Apache log files. 
It will construct a regex that will parse the given log 
file format and can then parse lines from the log file 
line by line returning a hash of each line.

%description -l zh_CN.UTF-8
解析 Apache 日志文件的一行到哈希。

%prep
%setup -q -n Apache-LogRegex-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*
magic_rpm_clean.sh


%check
# http://rt.perl.org/rt3//Public/Bug/Display.html?id=78008
# test broken by change of regexp
#

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.71-2
- 更新到 1.71

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.70-3
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.70-2
- 为 Magic 3.0 重建

* Thu Apr 23 2015 Liu Di <liudidi@gmail.com> - 1.70-1
- 更新到 1.70

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.5-13
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.5-12
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.5-11
- 为 Magic 3.0 重建

* Fri Jan 27 2012 Liu Di <liudidi@gmail.com> - 1.5-10
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.5-8
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 14 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.5-6
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.5-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.5-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec 12 2008 Steven Pritchard <steve@kspei.com> 1.5-1
- Update to 1.5.

* Thu Mar  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.4-4
- rebuild for new perl

* Tue Dec 11 2007 Steven Pritchard <steve@kspei.com> 1.4-3
- Update License tag.
- BR Test::More.

* Wed Apr 18 2007 Steven Pritchard <steve@kspei.com> 1.4-2
- BR ExtUtils::MakeMaker.

* Mon Oct 30 2006 Steven Pritchard <steve@kspei.com> 1.4-1
- Update to 1.4.
- Cleanup to more closely match cpanspec output.

* Tue Sep 26 2006 Steven Pritchard <steve@kspei.com> 1.3-1
- Update to 1.3.
- Fix find option order.

* Sat Aug 20 2005 Gavin Henry <ghenry[AT]suretecsystems.com> - 1.2-4
- Changed Licence names to COPYING and Artistic

* Fri Aug 19 2005 Gavin Henry <ghenry[AT]suretecsystems.com> - 1.2-3
- Added new perldoc commands for GPL and Artistic Licences

* Thu Aug 18 2005 Gavin Henry <ghenry[AT]suretecsystems.com> - 1.2-2
- Second build.

* Sun Jul 3 2005 Gavin Henry <ghenry[AT]suretecsystems.com> - 1.2-1
- First build.
