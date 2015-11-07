Name:           perl-Exception-Base
Version:	0.25
Release:	2%{?dist}
Summary:        Lightweight exceptions
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Exception-Base/
Source0:        http://www.cpan.org/authors/id/D/DE/DEXTER/Exception-Base-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Test::Unit::Lite)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
This class implements a fully OO exception mechanism similar to
Exception::Class or Class::Throwable. It provides a simple interface
allowing programmers to declare exception classes. These classes can be
thrown and caught. Each uncaught exception prints full stack trace if the
default verbosity is uppered for debugging purposes.

%prep
%setup -q -n Exception-Base-%{version}

%build
%{__perl} Build.PL installdirs=vendor
./Build

%install
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
./Build test

%files
%doc Changes Incompatibilities README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.25-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.25-1
- 更新到 0.25

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.2401-15
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.2401-14
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.2401-13
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.2401-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.2401-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.2401-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.2401-9
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.2401-8
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2401-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 0.2401-6
- Perl 5.16 rebuild

* Wed May 30 2012 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 0.2401-5
- Clean up spec file
- Add perl default filter

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2401-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.2401-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2401-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Oct 03 2010 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 0.2401-1
- Update to 0.2401

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.24-3
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.24-2
- Mass rebuild with perl-5.12.0

* Sun Apr  4 2010 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 0.24-1
- Update to 0.24
- Add perl(Test::Unit::Lite) to BuildRequires.

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.21-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 29 2009 Allisson Azevedo <allisson@gmail.com> 0.21-1
- Initial rpm release.
