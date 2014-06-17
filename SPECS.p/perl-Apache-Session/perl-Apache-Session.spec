Name:           perl-Apache-Session
Version:        1.89
Release:        14%{?dist}
Summary:        Persistence framework for session data
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Apache-Session/
Source0:        http://www.cpan.org/authors/id/C/CH/CHORNY/Apache-Session-%{version}.tar.gz
# https://bugzilla.redhat.com/bugzilla/attachment.cgi?id=118577, from Chris Grau
Patch0:         Apache-Session-mp2.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(DBI)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Test::Deep) >= 0.082
BuildRequires:  perl(Test::Exception) >= 0.15
BuildRequires:  perl(Test::More) >= 0.47
BuildRequires:  perl(Test::Pod)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Apache::Session is a persistence framework which is particularly useful for
tracking session data between httpd requests. Apache::Session is designed
to work with Apache and mod_perl, but it should work under CGI and other
web servers, and it also works outside of a web server altogether.

%prep
%setup -q -n Apache-Session-%{version}

find -type f -exec perl -pi -e 's/\r\n/\n/g' {} \;

%patch0 -p1

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
%doc CHANGES Contributing.txt README TODO
%doc eg/
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.89-14
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.89-13
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.89-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.89-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.89-10
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.89-9
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.89-8
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.89-7
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.89-6
- 为 Magic 3.0 重建

* Sat Jan 28 2012 Liu Di <liudidi@gmail.com> - 1.89-5
- 为 Magic 3.0 重建

* Fri Jan 27 2012 Liu Di <liudidi@gmail.com> - 1.89-4
- 为 Magic 3.0 重建

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.89-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.89-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 08 2010 Steven Pritchard <steve@kspei.com> 1.89-1
- Update to 1.89.
- Build with Module::Build.
- Add examples in eg/.
- Convert everything to Unix line endings and patch afterwards.

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.88-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.88-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.88-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 04 2009 Steven Pritchard <steve@kspei.com> 1.88-1
- Update to 1.88.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.87-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Aug 29 2008 Steven Pritchard <steve@kspei.com> 1.87-1
- Update to 1.87.
- Explicitly BR Test::More.
- Get rid of DOS line endings in Contributing.txt.

* Tue Feb 05 2008 Steven Pritchard <steve@kspei.com> 1.86-1
- Update to 1.86.

* Sat Feb 02 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.85-2
- rebuild for new perl

* Mon Jan 07 2008 Steven Pritchard <steve@kspei.com> 1.85-1
- Update to 1.85.
- BR Test::Pod.

* Mon Oct 15 2007 Steven Pritchard <steve@kspei.com> 1.84-1
- Update to 1.84.
- License changed to GPL+ or Artistic.
- Package Contributing.txt doc.

* Mon May 28 2007 Steven Pritchard <steve@kspei.com> 1.83-1
- Update to 1.83.

* Wed Apr 18 2007 Steven Pritchard <steve@kspei.com> 1.82-2
- BR ExtUtils::MakeMaker.

* Thu Feb 22 2007 Steven Pritchard <steve@kspei.com> 1.82-1
- Update to 1.82.
- Use fixperms macro instead of our own chmod incantation.
- Minor spec cleanup to more closely resemble current cpanspec output.

* Sat Sep 16 2006 Steven Pritchard <steve@kspei.com> 1.81-2
- Fix find option order.

* Wed May 24 2006 Steven Pritchard <steve@kspei.com> 1.81-1
- Update to 1.81.

* Tue Apr 11 2006 Steven Pritchard <steve@kspei.com> 1.80-1
- Update to 1.80.
- Spec cleanup.

* Thu Sep 08 2005 Steven Pritchard <steve@kspei.com> 1.6-2
- Add patch for mod_perl2 compatibility from Chris Grau (#167753, comment #3).
- Re-enable "".

* Wed Aug 31 2005 Steven Pritchard <steve@kspei.com> 1.6-1
- Specfile autogenerated.
