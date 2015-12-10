Name:           perl-JavaScript-Beautifier
Version:	0.18
Release:	3%{?dist}
Summary:        Beautify Javascript (beautifier for javascript)
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/JavaScript-Beautifier/
Source0:        http://www.cpan.org/authors/id/F/FA/FAYLAND/JavaScript-Beautifier-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(IO::File)
BuildRequires:  perl(Module::Build) >= 0.35
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::Pod) >= 1.22
BuildRequires:  dos2unix
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This module is mostly a Perl-rewrite of
http://github.com/einars/js-beautify/tree/master/beautify.js

%prep
%setup -q -n JavaScript-Beautifier-%{version}
dos2unix Changes
dos2unix README

%build
%{__perl} Build.PL installdirs=vendor
./Build

%install
rm -rf $RPM_BUILD_ROOT

./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
./Build test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/*
%{_bindir}/js_beautify.pl
%{_mandir}/man1/js_beautify.pl.1.gz
%{_mandir}/man3/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.18-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.18-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.18-1
- 更新到 0.18

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.17-14
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.17-13
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.17-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.17-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.17-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.17-9
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.17-8
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.17-7
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.17-5
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.17-3
- 661697 rebuild for fixing problems with vendorach/lib

* Wed Sep 15 2010 Petr Pisar <ppisar@redhat.com> - 0.17-2
- Add perl(Test::Pod) BuildRequires to proceed POD tests

* Wed Sep 15 2010 Petr Pisar <ppisar@redhat.com> - 0.17-1
- 0.17 bump

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.13-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.13-2
- rebuild against perl 5.10.1

* Tue Aug 11 2009 Marcela Mašláňová <mmaslano@redhat.com> 0.13-1
- fix source url, update

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 29 2009 Marcela Mašláňová <mmaslano@redhat.com> 0.04-1
- Specfile autogenerated by cpanspec 1.78.
