Name:           perl-File-Find-Rule-PPI
Version:	1.06
Release:	2%{?dist}
Summary:        Add support for PPI queries to File::Find::Rule

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/File-Find-Rule-PPI/
Source0:        http://www.cpan.org/authors/id/A/AD/ADAMK/File-Find-Rule-PPI-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(File::Find::Rule) >= 0.20
BuildRequires:  perl(Params::Util) >= 0.10
BuildRequires:  perl(PPI) >= 1.000
BuildRequires:  perl(Test::Pod) >= 1.00
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
File::Find::Rule::PPI allows you to integrate PPI content queries into
your File::Find::Rule searches.


%prep
%setup -q -n File-Find-Rule-PPI-%{version}
%{__sed} -i  's|\r||' Changes


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes LICENSE README
%{perl_vendorlib}/File/
%{_mandir}/man3/*.3pm*


%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.06-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.06-1
- 更新到 1.06

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.05-16
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.05-15
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.05-14
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 19 2012 Petr Pisar <ppisar@redhat.com> - 0.05-12
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 29 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.05-10
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.05-8
- 661697 rebuild for fixing problems with vendorach/lib

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.05-7
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.05-6
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.05-5
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.05-2
Rebuild for new perl

* Sun Sep 10 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.05-1
- Update to 0.05.

* Tue Sep  5 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.04-1
- Update to 0.04.

* Tue Apr 25 2006 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.03-1
- First build.
