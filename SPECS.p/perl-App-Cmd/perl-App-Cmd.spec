Name:           perl-App-Cmd
Summary:        Write command line apps with less suffering
Version:        0.314
Release:        9%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/R/RJ/RJBS/App-Cmd-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/App-Cmd
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(Capture::Tiny)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Class::Load) >= 0.06
BuildRequires:  perl(constant)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Data::OptList)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.30
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(Getopt::Long::Descriptive) >= 0.084
BuildRequires:  perl(IO::TieCombine) >= 1
BuildRequires:  perl(IPC::Cmd)
BuildRequires:  perl(Module::Pluggable::Object)
BuildRequires:  perl(String::RewritePrefix)
BuildRequires:  perl(Sub::Exporter) >= 0.975
BuildRequires:  perl(Sub::Exporter::Util)
BuildRequires:  perl(Sub::Install)
BuildRequires:  perl(Test::Fatal)
BuildRequires:  perl(Test::More) >= 0.96
BuildRequires:  perl(Text::Abbrev)

Requires:       perl(Getopt::Long::Descriptive) >= 0.084
Requires:       perl(IO::TieCombine) >= 1
Requires:       perl(Sub::Exporter) >= 0.975

# obsolete/provide old tests subpackage
# can be removed during F19 development cycle
Obsoletes:      %{name}-tests < 0.314-2
Provides:       %{name}-tests = %{version}-%{release}

%{?perl_default_filter}

%description
App::Cmd is intended to make it easy to write complex command-line
applications without having to think about most of the annoying things
usually involved.

For information on how to start using App::Cmd, see App::Cmd::Tutorial.

%prep
%setup -q -n App-Cmd-%{version}

perl -pi -e 's|^#!perl|#!%{__perl}|' t/*.t

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

%check


%files
%doc Changes LICENSE README t/
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.314-9
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.314-8
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.314-7
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.314-6
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.314-5
- 为 Magic 3.0 重建

* Sat Jan 28 2012 Liu Di <liudidi@gmail.com> - 0.314-4
- 为 Magic 3.0 重建

* Fri Jan 27 2012 Liu Di <liudidi@gmail.com> - 0.314-3
- 为 Magic 3.0 重建

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> 0.314-2
- drop tests-subpackage; move tests to main package documentation

* Thu Jan 12 2012 Emmanuel Seyman <emmanuel.seyman@club-internet.fr> - 0.314-1
- Update to 0.314

* Sun Oct 02 2011 Iain Arnell <iarnell@gmail.com> 0.312-1
- update to latest upstream version

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.311-2
- Perl mass rebuild

* Fri Mar 18 2011 Iain Arnell <iarnell@gmail.com> 0.311-1
- update to latest upstream version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.309-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Nov 20 2010 Iain Arnell <iarnell@gmail.com> 0.309-1
- update by Fedora::App::MaintainerTools 0.006
- updating to latest GA CPAN version (0.309)
- added a new br on perl(Carp) (version 0)
- added a new br on perl(Data::Dumper) (version 0)
- added a new br on perl(Data::OptList) (version 0)
- altered br on perl(ExtUtils::MakeMaker) (6.42 => 6.31)
- added a new br on perl(File::Basename) (version 0)
- added a new br on perl(Sub::Exporter::Util) (version 0)
- added a new br on perl(Test::Fatal) (version 0)
- altered br on perl(Test::More) (0 => 0.96)
- added a new br on perl(Text::Abbrev) (version 0)
- added a new br on perl(constant) (version 0)
- clean up spec for modern rpmbuild

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.307-3
- Mass rebuild with perl-5.12.0

* Fri Apr 23 2010 Iain Arnell <iarnell@gmail.com> 0.307-2
- requires perl(IO::TieCombine)

* Thu Apr 08 2010 Iain Arnell <iarnell@gmail.com> 0.307-1
- update to latest upstream
- R/BR perl(String::RewritePrefix)
- Bump R/BR perl(Getopt::Long::Descriptive) >= 0.084

* Mon Mar 01 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.304-1
- update by Fedora::App::MaintainerTools 0.004
- PERL_INSTALL_ROOT => DESTDIR
- altered br on perl(Getopt::Long::Descriptive) (0.075 => 0.081)
- altered req on perl(Getopt::Long::Descriptive) (0.075 => 0.081)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.301-2
- rebuild against perl 5.10.1

* Sat Sep 19 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.301-1
- auto-update to 0.301 (by cpan-spec-update 0.01)

* Sat Aug 29 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.207-1
- switch filtering to perl_default_filter
- auto-update to 0.207 (by cpan-spec-update 0.01)

* Sun Aug 23 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.206-1
- auto-update to 0.206 (by cpan-spec-update 0.01)
- altered br on perl(Getopt::Long::Descriptive) (0.06 => 0.075)
- altered req on perl(Getopt::Long::Descriptive) (0.06 => 0.075)

* Sat Aug 08 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.204-1
- auto-update to 0.204 (by cpan-spec-update 0.01)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)
- added a new req on perl(Getopt::Long::Descriptive) (version 0.06)
- added a new req on perl(Module::Pluggable::Object) (version 0)
- added a new req on perl(Sub::Exporter) (version 0.975)
- added a new req on perl(Sub::Install) (version 0)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.203-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.203-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.203-1
- update to 0.203

* Mon Nov 17 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.202-3
- br Test::More; drink more coffee

* Mon Nov 17 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.202-2
- bump

* Tue Nov 04 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.202-1
- update for submission

* Mon Oct 27 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.202-0.1
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.5)
