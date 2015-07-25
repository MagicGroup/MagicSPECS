%define short_name	Algorithm-FastPermute

Name:		perl-%{short_name}           
Version:	0.999
Release:	15%{?dist}
Summary:	Rapid generation of permutations
Summary(zh_CN.UTF-8): 快速的生成排列

Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/%{short_name}/
Source0:	http://www.cpan.org/authors/id/R/RO/ROBIN/%{short_name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	perl(ExtUtils::MakeMaker)
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Algorithm::FastPermute generates all the permutations of an array. You pass
a block of code, which will be executed for each permutation. The array
will be changed in place, and then changed back again before "permute"
returns. During the execution of the callback, the array is read-only and
you'll get an error if you try to change its length.

%description -l zh_CN.UTF-8
快速的生成排列。

%prep
%setup -q -n %{short_name}-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*
magic_rpm_clean.sh

%check



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes README perms.pl
%dir %{perl_vendorarch}/Algorithm
%{perl_vendorarch}/Algorithm/FastPermute.pm
%{perl_vendorarch}/auto/*
%{_mandir}/man3/*.3*
%exclude %{perl_vendorarch}/Algorithm/perms.pl

%changelog
* Mon Apr 20 2015 Liu Di <liudidi@gmail.com> - 0.999-15
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.999-14
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.999-13
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.999-12
- 为 Magic 3.0 重建

* Fri Jan 27 2012 Liu Di <liudidi@gmail.com> - 0.999-11
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.999-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.999-9
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.999-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 14 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.999-7
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.999-6
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.999-5
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.999-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.999-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Apr 04 2008 Milos Jakubicek <xjakub@fi.muni.cz> - 0.999-2
- License changed to "GPL+ or Artistic".

* Sat Mar 08 2008 Milos Jakubicek <xjakub@fi.muni.cz> - 0.999-1
- Initial release based on SRPM from Marius Feraru (reb00t.com).
- Modified according to the default perl spec file template.
