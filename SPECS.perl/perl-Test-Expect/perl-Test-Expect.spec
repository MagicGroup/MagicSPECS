Name:           perl-Test-Expect
Version:	0.33
Release:	3%{?dist}
Summary:        Automated driving and testing of terminal-based programs
Summary(zh_CN.UTF-8): 自动驱动和测试基于命令行的程序

Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Test-Expect/
Source0:        http://www.cpan.org/authors/id/B/BP/BPS/Test-Expect-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Class::Accessor::Chained::Fast)
BuildRequires:  perl(Expect::Simple)
BuildRequires:	perl(Test::More)
BuildRequires:	perl(Test::Builder)

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Test::Expect is a module for automated driving and testing of
terminal-based programs. It is handy for testing interactive programs
which have a prompt, and is based on the same concepts as the Tcl Expect
tool. As in Expect::Simple, the Expect object is made available for
tweaking.

Test::Expect is intended for use in a test script.

%description -l zh_CN.UTF-8
自动驱动和测试基于命令行的程序。

%prep
%setup -q -n Test-Expect-%{version}


%build
%{__perl} Build.PL installdirs=vendor
./Build


%install
rm -rf $RPM_BUILD_ROOT
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
chmod -R u+w $RPM_BUILD_ROOT/*
magic_rpm_clean.sh

%check
# switch off because of broken mock
##./Build test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc CHANGES README
%{perl_vendorlib}/Test/
%{_mandir}/man3/*.3pm*


%changelog
* Tue Nov 03 2015 Liu Di <liudidi@gmail.com> - 0.33-3
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.33-2
- 为 Magic 3.0 重建

* Fri Jun 05 2015 Liu Di <liudidi@gmail.com> - 0.33-1
- 更新到 0.33

* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.31-16
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Petr Pisar <ppisar@redhat.com> - 0.31-13
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.31-10
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 24 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.31-8
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.31-6
- 661697 rebuild for fixing problems with vendorach/lib

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.31-5
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.31-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Sep 16 2008 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.31-1
- Upgrade to 0.31 (Required by rt3's testsuite, BZ 462440).

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.30-3
Rebuild for new perl

* Tue Dec 11 2007 Ralf Corsépius <rc040203@freenet.de> - 0.30-2
- BR: perl(Test::More), perl(Test::Builder) (BZ 419631).

* Wed May 10 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.30-1
- First build.
