Name:           perl-Alien-wxWidgets
Version:	0.67
Release:	2%{?dist}
Summary:        Building, finding and using wxWidgets binaries
Summary(zh_CN.UTF-8): 构建、查找和使用二进制的 wx 部件

Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Alien-wxWidgets/
Source0:        http://search.cpan.org/CPAN/authors/id/M/MD/MDOOTSON/Alien-wxWidgets-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  wx-gtk2-unicode-devel
# A lot of stuff used by inc/My/Build/Base.pm.
BuildRequires:  perl
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Fatal)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Glob)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec) >= 1.50
BuildRequires:  perl(Module::Build) >= 0.28
BuildRequires:  perl(Module::Pluggable)
BuildRequires:  perl(strict)
# Tests:
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# No binaries in this package
%define debug_package %{nil}

%description
"Alien::wxWidgets" can be used to detect and get configuration
settings from an installed wxWidgets.

%description -l zh_CN.UTF-8
构建、查找和使用二进制的 wx 部件。

%prep
%setup -q -n Alien-wxWidgets-%{version}


%build
%{__perl} Build.PL installdirs=vendor < /dev/null
./Build


%install
rm -rf $RPM_BUILD_ROOT
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
chmod -R u+w $RPM_BUILD_ROOT/*
magic_rpm_clean.sh

%check
./Build test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes
%{perl_vendorarch}/Alien/
%{_mandir}/man3/*.3pm*


%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.67-2
- 为 Magic 3.0 重建

* Wed Apr 22 2015 Liu Di <liudidi@gmail.com> - 0.67-1
- 更新到 0.67

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.51-15
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.51-14
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.51-13
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.51-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.51-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Petr Pisar <ppisar@redhat.com> - 0.51-10
- Perl 5.18 rebuild
- Specify some dependencies

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.51-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.51-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.51-7
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.51-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.51-5
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.51-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 14 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.51-3
- 661697 rebuild for fixing problems with vendorach/lib

* Wed Jul 14 2010 Dan Horák <dan@danny.cz> - 0.51-2
- rebuilt against wxGTK-2.8.11-2

* Mon May 17 2010 Petr Pisar <ppisar@redhat.com> - 0.51-1
- Version bump
- Remove perl-Alien-wxWidgets-SONAME.patch

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.44-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.44-3
- rebuild against perl 5.10.1

* Mon Aug 24 2009 Stepan Kasal <skasal@redhat.com> - 0.44-2
- fix the soname patch

* Thu Aug 20 2009 Stepan Kasal <skasal@redhat.com> - 0.44-1
- new upstream version
- add patch to remember the canonical sonames of libraries, so that
  perl-Wx runs without wxGTK-devel

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.42-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.42-1
- 0.42

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.32-4
- Rebuild for perl 5.10 (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.32-3
- Autorebuild for GCC 4.3

* Tue Feb  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.32-2
- rebuild for new perl

* Wed Nov 28 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.32-1
- Update to 0.32

* Sat Mar 31 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.31-1
- Update to 0.31.

* Fri Mar 23 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.30-1
- Update to 0.30.

* Sun Mar 18 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.29-1
- Update to 0.29.

* Wed Dec 20 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.27-1
- Update to 0.27.

* Sat Dec 16 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.26-1
- Update to 0.26.

* Sat Dec 16 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.25-2
- Rebuild (wxGTK 2.8.0).

* Sat Nov 11 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.25-1
- Update to 0.25.

* Sat Oct 21 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.24-1
- Update to 0.24.

* Thu Oct 19 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.23-1
- Update to 0.23.

* Tue Oct  3 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.22-1
- Update to 0.22.
- Avoid creation of the debuginfo package (#209180).
- Dropped patch Alien-wxWidgets-0.21-Any_wx_config.pm.patch
  (http://rt.cpan.org/Public/Bug/Display.html?id=21854).

* Sun Oct  1 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.21-3
- Patch to add /usr/lib64 to the library search path.

* Thu Sep 28 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.21-2
- This is a binary RPM (see bug #208007 comment #2).

* Sun Sep 24 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.21-1
- First build.
