# Only need manual requires for "use base XXX;" prior to rpm 4.9
%global rpm49 %(rpm --version | perl -pi -e 's/^.* (\\d+)\\.(\\d+).*/sprintf("%d.%03d",$1,$2) ge 4.009 ? 1 : 0/e')

Name:           perl-Array-Diff
Version:        0.07
Release:        16%{?dist}
# Because 0.07 compares newer than 0.05002 in Perl world
# but not in RPM world :-(
Epoch:          1
Summary:        Find the differences between two arrays
Summary(zh_CN.UTF-8): 在两个数组之间寻找不同
License:        GPL+ or Artistic
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
URL:            http://search.cpan.org/dist/Array-Diff/
Source0:        http://www.cpan.org/authors/id/T/TY/TYPESTER/Array-Diff-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:      noarch
BuildRequires:  perl(Algorithm::Diff)
BuildRequires:  perl(Class::Accessor::Fast)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
%if ! %{rpm49}
Requires:       perl(Class::Accessor::Fast)
%endif

%description
This module compares two arrays and returns the added or deleted elements in
two separate arrays. It's a simple wrapper around Algorithm::Diff.

If you need more complex array tools, check Array::Compare.

%description -l zh_CN.UTF-8
在两个数组之间寻找不同。

%prep
%setup -q -n Array-Diff-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT
magic_rpm_clean.sh

%check


%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc Changes LICENSE README
%dir %{perl_vendorlib}/Array/
%{perl_vendorlib}/Array/Diff.pm
%{_mandir}/man3/Array::Diff.3pm*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1:0.07-16
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1:0.07-15
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1:0.07-14
- 为 Magic 3.0 重建

* Thu Apr 23 2015 Liu Di <liudidi@gmail.com> - 1:0.07-13
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1:0.07-12
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1:0.07-11
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1:0.07-10
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.07-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 1:0.07-8
- Perl 5.16 rebuild

* Tue Mar  6 2012 Paul Howarth <paul@city-fan.org> - 1:0.07-7
- Explicitly require perl(Class::Accessor::Fast) unless we have rpm ≥ 4.9,
  which can auto-detect the dependency
- Drop buildreq perl(Module::Install) - Makefile.PL explicitly uses the one
  bundled in inc/
- Don't need to remove empty directories from buildroot
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Make %%files list more explicit
- Don't use macros for commands
- Drop %%defattr, redundant since rpm 4.4
- Improve %%description and %%summary

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.07-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1:0.07-5
- Perl mass rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1:0.07-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.07-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 25 2011 Daniel P. Berrange <berrange@redhat.com> - 1:0.07-2
- Bump epoch to ensure 0.07 is considered newer than 0.05002 (rhbz #672463)

* Fri Dec 17 2010 Daniel P. Berrange <berrange@redhat.com> - 0.07-1
- Update to 0.07 release

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.05002-6
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.05002-5
- Mass rebuild with perl-5.12.0

* Tue Jan 12 2010 Daniel P. Berrange <berrange@redhat.com> - 0.05002-4
- Fix source URL

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.05002-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05002-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Daniel P. Berrange <berrange@redhat.com> - 0.05002-1
- Update to new 0.05002 release

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.04-3
- rebuild for new perl

* Fri Dec 21 2007 Daniel P. Berrange <berrange@redhat.com> 0.04-2.fc9
- Added Test::Pod and Test::Pod::Coverage build requires

* Fri Dec 21 2007 Daniel P. Berrange <berrange@redhat.com> 0.04-1.fc9
- Specfile autogenerated by cpanspec 1.73.
