Name:           perl-Inline
Version:        0.51
Release:        2%{?dist}
Summary:        Inline Perl module
Group:          Development/Libraries
License:        GPL+ or Artistic
Url:            http://search.cpan.org/dist/Inline/
Source0:        http://search.cpan.org/CPAN/authors/id/S/SI/SISYPHUS/Inline-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(base)
BuildRequires:  perl(lib)
BuildRequires:  perl(AutoLoader)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Digest::MD5)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Spec::Unix)
BuildRequires:  perl(Inline::Files)
BuildRequires:  perl(Parse::RecDescent)
BuildRequires:  perl(Socket)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Warn)
# Optional tests
#Optional, not yet in Fedora
#BuildRequires:  perl(Inline::Filters)
#BuildRequires:  perl(Inline::Struct)
BuildRequires:  perl(Time::HiRes)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
# not automatically detected
Requires:       perl(Digest::MD5)
Requires:       perl(Socket)

%{?perl_default_filter}
%global __provides_exclude %{?__provides_exclude}|perl\\(Inline\\)$

%description
The Inline module allows you to put source code from other programming
languages directly "inline" in a Perl script or module. The code is
automatically compiled as needed, and then loaded for immediate access
from Perl.

Inline saves you from the hassle of having to write and compile your
own glue code using facilities like XS or SWIG. Simply type the code
where you want it and run your Perl as normal. All the hairy details
are handled for you. The compilation and installation of your code
chunks all happen transparently; all you will notice is the delay of
compilation on the first run.

The Inline code only gets compiled the first time you run it (or
whenever it is modified) so you only take the performance hit
once. Code that is Inlined into distributed modules (like on the CPAN)
will get compiled when the module is installed, so the end user will
never notice the compilation time.

%prep
%setup -q -n Inline-%{version} 

%build
# trick avoiding installation other modules
perl Makefile.PL INSTALLDIRS=vendor < /dev/null
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w %{buildroot}/*

%check


%files
%doc Changes README
%{perl_vendorlib}/Inline*
%{perl_vendorlib}/auto/
%{_mandir}/man3/*.3*

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.51-2
- 为 Magic 3.0 重建

* Mon Oct 15 2012 Petr Šabata <contyk@redhat.com> - 0.51-1
- 0.51 bump

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.50-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 16 2012 Petr Pisar <ppisar@redhat.com> - 0.50-2
- Perl 5.16 rebuild

* Tue Feb 07 2012 Petr Šabata <contyk@redhat.com> - 0.50-1
- 0.50 bump
- Minor cleanup

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.49-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 13 2011 Marcela Mašláňová <mmaslano@redhat.com> 0.49-1
- bump to 0.49
- add BR: perl(Carp), perl(File::Spec), perl(Test::More)
- add R: perl(Data::Dumper)

* Wed Nov 09 2011 Iain Arnell <iarnell@gmail.com> 0.48-3
- R/BR perl(Digest::MD5)

* Wed Jun 28 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.48-2
- Perl mass rebuild
- fix filter macro

* Mon Mar  7 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.48-1
- update to 0.48
- add Test::Warn into BR

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.47-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 25 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.47-1
- 671863 update to 0.47

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.46-2
- 661697 rebuild for fixing problems with vendorach/lib

* Wed Jul 14 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 0.46-1
- update to 0.46

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.44-24
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.44-23
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.44-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.44-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.44-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.44-19
- rebuild for new perl

* Mon Nov 19 2007 Robin Norwood <rnorwood@redhat.com> - 0.44-18
- Add BR: perl(Inline::Files)

* Wed Oct 24 2007 Robin Norwood <rnorwood@redhat.com> - 0.44-17
- Various fixes from package review

* Tue Oct 16 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 0.44-16
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 0.44-15.2
- rebuild for new perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Thu Apr 21 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.44-15
- BuildArch correction (noarch). (#155811)
- Bring up to date with current Fedora.Extras perl spec template.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 19 2004 Chip Turner <cturner@redhat.com> 0.44-10
- rebuild

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun 17 2003 Chip Turner <cturner@redhat.com> 0.44-8
- rebuild

* Mon Jan 27 2003 Chip Turner <cturner@redhat.com>
- version bump and rebuild

* Wed Nov 20 2002 Chip Turner <cturner@redhat.com>
- rebuild
- update to 0.44

* Tue Aug  6 2002 Chip Turner <cturner@redhat.com>
- automated release bump and build

* Thu Jun 27 2002 Chip Turner <cturner@redhat.com>
- description update

* Fri Jun 07 2002 cturner@redhat.com
- Specfile autogenerated

