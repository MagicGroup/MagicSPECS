Name:           perl-QWizard
Version:        3.15
Release:        17%{?dist}
Summary:        A very portable graphical question and answer wizard system
License:        GPL+ or Artistic 
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/QWizard/
Source0:        http://www.cpan.org/authors/id/H/HA/HARDAKER/QWizard-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(CGI)
# These are not auto-detected since they're technically optional
# (they're the best of the alternative choices available on linux)
Requires:       perl(CGI)
Requires:       perl(Gtk2)
Requires:       perl(Chart::Lines)

# neither are picked up automagically.
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
The QWizard module allows script authors to concentrate on the
content of the forms they want their users to fill in without
worrying about the display.  It allows "Question Wizard" like
interfaces to be very easily created and the results of the input
easily acted upon.  Scripts written which are entirely based on
QWizard inputs are able to be run from the command line which will
show a Gtk2, Tk window or as a ReadLine interactive session or as a
CGI script without modification.  Script writers do not need to know
which interface is being used to display the resulting form(s) as it
should be transparent to the script itself.

Other wizard interfaces exist for perl, but this one strives very
hard to be both extensible and easy to code with requiring as little
work by script authors as possible.  It is also one of the only ones
that supports both web environments and windowing environments
without code modification required by the script author.

%prep
%setup -q -n QWizard-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make pure_install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

# rpm doc examples shouldn't be executable
chmod a-x examples/*.pl
# not needed perl script that is actually just a pod generator from dist
rm -f %{buildroot}%{perl_vendorlib}/QWizard_Widgets.pl

%{_fixperms} %{buildroot}/*

%check
make test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc examples/
%doc README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Jun 19 2014 Liu Di <liudidi@gmail.com> - 3.15-17
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.15-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.15-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 3.15-14
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.15-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.15-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 3.15-11
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.15-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 3.15-9
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.15-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 13 2011 Wes Hardaker <wjhns174@hardakers.net> - 3.15-7
- require CGI to ensure all sub-components work

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 3.15-6
- 661697 rebuild for fixing problems with vendorach/lib

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 3.15-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 3.15-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Sep 17 2008 Wes Hardaker <wjhns174@hardakers.net> - 3.15-1
- Update to latest upstream bug fixes

* Fri Jul 18 2008 Wes Hardaker <wjhns174@hardakers.net> - 3.14-2
- Version bump for build issues

* Tue Apr 29 2008 Wes Hardaker <wjhns174@hardakers.net> - 3.14-1
- Update to latest upstream for bug fixes and minor new features

* Sat Dec 22 2007 Wes Hardaker <wjhns174@hardakers.net> - 3.13-2
- remove patch now in base

* Fri Dec 21 2007 Wes Hardaker <wjhns174@hardakers.net> - 3.13-1
- Sync with parent 3.13 version

* Wed Dec 19 2007 Wes Hardaker <wjhns174@hardakers.net> - 3.12-2
- Changed Chart requirement to Chart::Lines to pick up proper dependencies

* Sat Dec  1 2007  Wes Hardaker <wjhns174@hardakers.net> - 3.12-1
- Initial version
