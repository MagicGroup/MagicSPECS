Name:           perl-Catalyst-Devel
Summary:        Catalyst Development Tools
Summary(zh_CN.UTF-8): Catalyst 开发工具
Version:	1.39
Release:	2%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Source0:        http://search.cpan.org/CPAN/authors/id/I/IL/ILMARI/Catalyst-Devel-%{version}.tar.gz
URL:            http://search.cpan.org/dist/Catalyst-Devel/
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(Catalyst) >= 5.90001
BuildRequires:  perl(Catalyst::Action::RenderView) >= 0.10
BuildRequires:  perl(Catalyst::Plugin::ConfigLoader) >= 0.30
BuildRequires:  perl(Catalyst::Plugin::Static::Simple) >= 0.28
BuildRequires:  perl(Config::General) >= 2.42
BuildRequires:  perl(CPAN)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires:  perl(File::ChangeNotify) >= 0.07
BuildRequires:  perl(File::Copy::Recursive)
BuildRequires:  perl(File::ShareDir)
BuildRequires:  perl(Module::Install) >= 1.02
BuildRequires:  perl(Moose)
BuildRequires:  perl(MooseX::Daemonize)
BuildRequires:  perl(MooseX::Emulate::Class::Accessor::Fast)
BuildRequires:  perl(namespace::autoclean)
BuildRequires:  perl(namespace::clean)
BuildRequires:  perl(Path::Class) >= 0.09
BuildRequires:  perl(Starman)
BuildRequires:  perl(Template) >= 2.14
BuildRequires:  perl(Test::More) >= 0.94
BuildRequires:  perl(Test::Fatal)

BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(IPC::Run3)

Requires:       perl(Catalyst) >= 5.90001
Requires:       perl(Catalyst::Action::RenderView) >= 0.10
Requires:       perl(Catalyst::Plugin::ConfigLoader) >= 0.30
Requires:       perl(Catalyst::Plugin::Static::Simple) >= 0.28
Requires:       perl(Config::General) >= 2.42
Requires:       perl(File::ChangeNotify) >= 0.07
Requires:       perl(Module::Install) >= 1.02
Requires:       perl(MooseX::Daemonize)
Requires:       perl(MooseX::Emulate::Class::Accessor::Fast)
Requires:       perl(Path::Class) >= 0.09
Requires:       perl(Starman)
Requires:       perl(Template) >= 2.14
Requires:       perl-Catalyst-Runtime-scripts

# obsolete/provide old tests subpackage
# can be removed during F19 development cycle
Obsoletes:      %{name}-tests < 1.36-2
Provides:       %{name}-tests = %{version}-%{release}

%{?perl_default_filter}

%description
The Catalyst::Devel package includes a variety of modules useful for the
development of Catalyst applications, but not required to run them. This is
intended to make it easier to deploy Catalyst apps. The runtime parts of
Catalyst are now known as Catalyst::Runtime.

%description -l zh_CN.UTF-8
Catalyst 开发工具。

%prep
%setup -q -n Catalyst-Devel-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*
magic_rpm_clean.sh

%check



%files
%doc Changes t/
%{perl_vendorlib}/*
%{_mandir}/man[13]/*
# we don't need this, and it's causing dep problems.
%exclude %{perl_vendorlib}/Catalyst/Restarter/Win32.pm

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.39-2
- 为 Magic 3.0 重建

* Fri Jun 05 2015 Liu Di <liudidi@gmail.com> - 1.39-1
- 更新到 1.39

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.36-17
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.36-16
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.36-15
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.36-14
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.36-13
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.36-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.36-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.36-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.36-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.36-8
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.36-7
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.36-6
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.36-5
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.36-4
- 为 Magic 3.0 重建

* Sat Jan 28 2012 Liu Di <liudidi@gmail.com> - 1.36-3
- 为 Magic 3.0 重建

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> 1.36-2
- drop old tests subpackage; move tests to main package documentation

* Thu Jan 12 2012 Iain Arnell <iarnell@gmail.com> 1.36-1
- update to latest upstream version
- clean up spec for moderm rpmbuild

* Mon Aug 29 2011 Iain Arnell <iarnell@gmail.com> 1.34-1
- update to latest upstream version

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.31-4
- Perl mass rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.31-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 22 2011 Iain Arnell <iarnell@gmail.com> 1.31-1
- update to latest upstream version
- update R/BR perl(Catalyst::Plugin::ConfigLoader) >= 0.30
- remove unnecessary explicit requires

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.28-2
- 661697 rebuild for fixing problems with vendorach/lib

* Tue Aug 31 2010 Iain Arnell <iarnell@gmail.com> 1.28-1
- update to latest upstream

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.27-2
- Mass rebuild with perl-5.12.0

* Sat Mar 13 2010 Chris Weyl <cweyl@alumni.drew.edu> 1.27-1
- update by Fedora::App::MaintainerTools 0.006
- PERL_INSTALL_ROOT => DESTDIR
- updating to latest GA CPAN version (1.27)
- altered br on perl(Catalyst) (5.8000 => 5.80015)
- altered br on perl(Catalyst::Action::RenderView) (0.04 => 0.10)
- altered br on perl(Catalyst::Plugin::ConfigLoader) (0 => 0.23)
- altered br on perl(Catalyst::Plugin::Static::Simple) (0.16 => 0.28)
- added a new br on perl(File::ShareDir) (version 0)
- added a new br on perl(Moose) (version 0)
- added a new br on perl(MooseX::Emulate::Class::Accessor::Fast) (version 0)
- altered br on perl(Test::More) (0 => 0.94)
- added a new br on perl(namespace::autoclean) (version 0)
- added a new br on perl(namespace::clean) (version 0)
- dropped old BR on perl(Class::Accessor::Fast)
- dropped old BR on perl(parent)
- added manual BR on perl(Test::More) (or override to 0.92)
- altered req on perl(Catalyst) (5.8000 => 5.80015)
- altered req on perl(Catalyst::Action::RenderView) (0.04 => 0.10)
- altered req on perl(Catalyst::Plugin::ConfigLoader) (0 => 0.23)
- altered req on perl(Catalyst::Plugin::Static::Simple) (0.16 => 0.28)
- added a new req on perl(File::ShareDir) (version 0)
- added a new req on perl(Moose) (version 0)
- added a new req on perl(MooseX::Emulate::Class::Accessor::Fast) (version 0)
- added a new req on perl(namespace::autoclean) (version 0)
- added a new req on perl(namespace::clean) (version 0)
- dropped old requires on perl(Class::Accessor::Fast)
- dropped old requires on perl(YAML)
- dropped old requires on perl(parent)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.20-2
- rebuild against perl 5.10.1

* Tue Aug 18 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.20-1
- auto-update to 1.20 (by cpan-spec-update 0.01)
- altered br on perl(File::ChangeNotify) (0.03 => 0.07)
- altered req on perl(File::ChangeNotify) (0.03 => 0.07)

* Mon Jul 27 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.19-1
- auto-update to 1.19 (by cpan-spec-update 0.01)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 17 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.18-3
- exclude Catalyst::Restarter::Win32 (dep issues and unneeded on this
  platform)

* Sun Jun 14 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.18-2
- br CPAN until bundled M::I is updated

* Sun Jun 14 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.18-1
- auto-update to 1.18 (by cpan-spec-update 0.01)
- altered br on perl(Module::Install) (0.64 => 0.91)
- altered req on perl(Catalyst) (5.7000 => 5.8000)
- added a new req on perl(Config::General) (version 2.42)
- added a new req on perl(File::ChangeNotify) (version 0.03)
- added a new req on perl(File::Copy::Recursive) (version 0)
- altered req on perl(Module::Install) (0.64 => 0.91)
- added a new req on perl(Template) (version 2.14)

* Sun Jun 07 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.17-1
- auto-update to 1.17 (by cpan-spec-update 0.01)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)
- altered br on perl(Catalyst) (5.7000 => 5.8000)
- altered br on perl(Config::General) (0 => 2.42)
- added a new br on perl(File::ChangeNotify) (version 0.03)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.10-1
- update to 1.10

* Wed Sep 10 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.08-2
- add perl(parent) as a requires (BZ#461581)

* Thu Jul 31 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.08-1
- update to 1.08

* Thu Jul 31 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.07-2
- drop requires on Catalyst::Manual that should have been dropped in 1.06-1

* Sun Jun 22 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.07-1
- update to 1.07
- require perl-Catalyst-Runtime-scripts; catalyst.pl lives in there now.

* Wed May 28 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.06-1
- update to 1.06 (runtime to 5.7014)
- drop br on Catalyst::Manual; add br on parent

* Wed Mar 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.03-2
- rebuild for new perl

* Sat Mar 01 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.03-1
- update to 1.03 (runtime to 5.7012)

* Fri Aug 10 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.02-3
- bump

* Tue Jul 24 2007 Chris Weyl <cweyl@alumni.drew.edu>
- add t/ to doc

* Fri Apr 27 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.02-1
- Specfile autogenerated by cpanspec 1.71.
