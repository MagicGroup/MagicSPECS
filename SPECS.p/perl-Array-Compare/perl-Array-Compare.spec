Name:           perl-Array-Compare
Version:	2.11
Release:	1%{?dist}
Summary:        Perl extension for comparing arrays
Summary(zh_CN.UTF-8): 比较数组的 Perl 扩展

Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Array-Compare/
Source0:        http://www.cpan.org/authors/id/D/DA/DAVECROSS/Array-Compare-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(Module::Build), perl(Moose)
BuildRequires:  perl(Test::Pod), perl(Test::Pod::Coverage)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
If you have two arrays and you want to know if they are the same or
different, then Array::Compare will be useful to you.

%description -l zh_CN.UTF-8
比较数组的 Perl 扩展。

%prep
%setup -q -n Array-Compare-%{version}
chmod -c a-x lib/Array/*.pm


%build
%{__perl} Build.PL installdirs=vendor
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
%doc Changes README
%{perl_vendorlib}/Array/
%{_mandir}/man3/*.3pm*


%changelog
* Thu Apr 23 2015 Liu Di <liudidi@gmail.com> - 2.11-1
- 更新到 2.11

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 2.01-18
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 2.01-17
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.01-16
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.01-15
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 2.01-14
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 2.01-13
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 2.01-12
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 2.01-11
- 为 Magic 3.0 重建

* Sat Jan 28 2012 Liu Di <liudidi@gmail.com> - 2.01-10
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.01-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 2.01-8
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 2.01-7
- Perl mass rebuild

* Thu Jun 29 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.01-6
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.01-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.01-4
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.01-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.01-2
- rebuild against perl 5.10.1

* Mon Oct  5 2009 Stepan Kasal <skasal@redhat.com> - 2.01-1
- new upstream version, BR perl(Moose)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Feb 27 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.17-1
- Upstream update.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jul 10 2008 Ralf Corsépius <rc040203@freenet.de> - 1.16-1
- Upstream update.

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.14-3
- Rebuild for perl 5.10 (again)

* Thu Jan 31 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.14-2
- rebuild for new perl

* Thu Apr  5 2007 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.14-1
- Update to 1.14.

* Thu Sep  7 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.13-3
- Rebuild for FC6.

* Mon Feb 20 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.13-2
- Rebuild for FC5 (perl 5.8.8).

* Thu Oct  6 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.13-1
- Update to 1.13.

* Fri Jul  1 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.12-3
- Dist tag.

* Wed Apr 20 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.12-0.fdr.2
- Avoid .packlist creation with Module::Build >= 0.2609.

* Tue Mar  1 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.12-0.fdr.1
- Update to 1.12.

* Fri Nov  5 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.11-0.fdr.1
- Update to 1.11.

* Sun Jul 04 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:1.09-0.fdr.1
- First build.
