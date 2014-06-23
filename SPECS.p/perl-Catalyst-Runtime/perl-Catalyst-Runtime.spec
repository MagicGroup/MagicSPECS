Name:           perl-Catalyst-Runtime
Summary:        Catalyst Framework Runtime
Version:        5.90019
Release:        6%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/B/BO/BOBTFISH/Catalyst-Runtime-%{version}.tar.gz
URL:            http://search.cpan.org/dist/Catalyst-Runtime/
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  groff
BuildRequires:  /usr/bin/perldoc
BuildRequires:  perl(Carp)
BuildRequires:  perl(CGI::Simple::Cookie) >= 1.109
BuildRequires:  perl(Class::C3::Adopt::NEXT) >= 0.07
BuildRequires:  perl(Class::Data::Inheritable)
BuildRequires:  perl(Class::Load) >= 0.12
BuildRequires:  perl(Class::MOP) >= 0.95
BuildRequires:  perl(CPAN)
BuildRequires:  perl(Data::Dump)
BuildRequires:  perl(Data::OptList)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires:  perl(HTML::Entities)
BuildRequires:  perl(HTML::HeadParser)
BuildRequires:  perl(HTTP::Body) >= 1.06
BuildRequires:  perl(HTTP::Headers) >= 1.64
BuildRequires:  perl(HTTP::Request) >= 5.814
BuildRequires:  perl(HTTP::Request::AsCGI) >= 1.0
BuildRequires:  perl(HTTP::Request::Common)
BuildRequires:  perl(HTTP::Response) >= 5.813
BuildRequires:  perl(List::MoreUtils)
BuildRequires:  perl(LWP::UserAgent)
BuildRequires:  perl(Module::Pluggable) >= 3.9
BuildRequires:  perl(Moose) >= 1.03
BuildRequires:  perl(MooseX::Emulate::Class::Accessor::Fast) >= 0.00903
BuildRequires:  perl(MooseX::Getopt) >= 0.30
BuildRequires:  perl(MooseX::MethodAttributes::Inheritable) >= 0.24
BuildRequires:  perl(MooseX::Role::WithOverloading) >= 0.09
BuildRequires:  perl(MRO::Compat)
BuildRequires:  perl(namespace::autoclean) >= 0.09
BuildRequires:  perl(namespace::clean) >= 0.23
BuildRequires:  perl(Path::Class) >= 0.09
BuildRequires:  perl(Plack) >= 0.9991
BuildRequires:  perl(Plack::Middleware::ReverseProxy) >= 0.04
BuildRequires:  perl(Plack::Test::ExternalServer)
BuildRequires:  perl(Safe::Isa)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(String::RewritePrefix) >= 0.004
BuildRequires:  perl(Sub::Exporter)
BuildRequires:  perl(Task::Weaken)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Text::Balanced)
BuildRequires:  perl(Text::SimpleTable) >= 0.03
BuildRequires:  perl(Time::HiRes)
BuildRequires:  perl(Tree::Simple) >= 1.15
BuildRequires:  perl(Tree::Simple::Visitor::FindByPath)
BuildRequires:  perl(Try::Tiny)
BuildRequires:  perl(URI) >= 1.35

BuildRequires:  perl(Class::Accessor::Fast)
BuildRequires:  perl(Class::C3)
BuildRequires:  perl(Class::Inspector)
BuildRequires:  perl(FCGI)
BuildRequires:  perl(File::Copy::Recursive)
BuildRequires:  perl(File::Modified)
BuildRequires:  perl(Proc::ProcessTable)
BuildRequires:  perl(Test::Harness)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Spelling)
BuildRequires:  perl(Test::Without::Module)
BuildRequires:  perl(YAML)


Requires:       perl(B::Hooks::EndOfScope) >= 0.08
Requires:       perl(CGI::Simple::Cookie) >= 1.109
Requires:       perl(Class::C3::Adopt::NEXT) >= 0.07
Requires:       perl(Class::Load) >= 0.12
Requires:       perl(Class::MOP) >= 0.95
Requires:       perl(HTML::HeadParser)
Requires:       perl(HTTP::Body) >= 1.06
Requires:       perl(HTTP::Headers) >= 1.64
Requires:       perl(HTTP::Request) >= 5.814
Requires:       perl(HTTP::Request::AsCGI) >= 1.0
Requires:       perl(HTTP::Response) >= 5.813
Requires:       perl(LWP::UserAgent)
Requires:       perl(Module::Pluggable) >= 3.9
Requires:       perl(Moose) >= 1.03
Requires:       perl(MooseX::Emulate::Class::Accessor::Fast) >= 0.00903
Requires:       perl(MooseX::Getopt) >= 0.30
Requires:       perl(MooseX::MethodAttributes::Inheritable) >= 0.24
Requires:       perl(MooseX::Role::WithOverloading) >= 0.09
Requires:       perl(namespace::autoclean) >= 0.09
Requires:       perl(namespace::clean) >= 0.23
Requires:       perl(Path::Class) >= 0.09
Requires:       perl(Plack) >= 0.9991
Requires:       perl(Plack::Middleware::ReverseProxy) >= 0.04
Requires:       perl(Plack::Test::ExternalServer)
Requires:       perl(String::RewritePrefix) >= 0.004
Requires:       perl(Task::Weaken)
Requires:       perl(Text::SimpleTable) >= 0.03
Requires:       perl(Tree::Simple) >= 1.15
Requires:       perl(URI) >= 1.35

# obolete/provide old tests subpackage
# can be removed during F19 development cycle
Obsoletes:      %{name}-tests < 5.90007-2
Provides:       %{name}-tests = %{version}-%{release}

%{?perl_default_filter}

%description
This is the primary class for the Catalyst-Runtime distribution.  It provides
the core of any runtime Catalyst instance.
 
%package        scripts
Summary:        Scripts for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    scripts

The %{name}-scripts package contains scripts distributed with
%{name} but generally used for developing Catalyst applications.


%prep
%setup -q -n Catalyst-Runtime-%{version}

# something like this seems to beg for explicitness
perldoc perlgpl      > COPYING.gpl
perldoc perlartistic > COPYING.artistic

find .  -type f -exec chmod -c -x {} +
find t/ -type f -exec perl -pi -e 's|^#!perl|#!%{__perl}|' {} +

%build
PERL5_CPANPLUS_IS_RUNNING=1 %{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \;

%{_fixperms} %{buildroot}/*

%check
# note that some of the optional tests we're enabling here will be skipped
# anyways, due to deps on Catalyst::Devel, etc.  We cannot depend on
# Catalyst::Devel, however, as it depends on us, and circular dep loops are
# never fun.  (Well, maybe to Zeno.)
#
# See also http://rt.cpan.org/Public/Bug/Display.html?id=27123

export TEST_LIGHTTPD=1
export TEST_HTTP=1

# see https://rt.cpan.org/Public/Bug/Display.html?id=42540
#export TEST_MEMLEAK=1

export TEST_POD=1
export TEST_STRESS=1

make test
make clean

%files
%doc Changes COPYING* README t/
%{perl_vendorlib}/*
%{_mandir}/man3/*

%files scripts
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 5.90019-6
- 为 Magic 3.0 重建

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.90019-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Aug 05 2013 Petr Pisar <ppisar@redhat.com> - 5.90019-4
- Perl 5.18 rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.90019-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.90019-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 07 2012 Iain Arnell <iarnell@gmail.com> 5.90019-1
- update to latest upstream version

* Sat Oct 27 2012 Iain Arnell <iarnell@gmail.com> 5.90018-1
- update to latest upstream version

* Sat Oct 20 2012 Iain Arnell <iarnell@gmail.com> 5.90017-1
- update to latest upstream version

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.90015-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 03 2012 Petr Pisar <ppisar@redhat.com> - 5.90015-2
- Perl 5.16 rebuild

* Tue Jul 03 2012 Iain Arnell <iarnell@gmail.com> 5.90015-1
- update to latest upstream version

* Sun Jul 01 2012 Petr Pisar <ppisar@redhat.com> - 5.90012-2
- Perl 5.16 rebuild

* Sat May 19 2012 Iain Arnell <iarnell@gmail.com> 5.90012-1
- update to latest upstream version

* Fri Mar 09 2012 Iain Arnell <iarnell@gmail.com> 5.90011-1
- update to latest upstream version
- resolves RHBZ#800241

* Sat Feb 18 2012 Iain Arnell <iarnell@gmail.com> 5.90010-1
- update to latest upstream version

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> 5.90007-2
- drop tests subpackage; move tests to main package documentation

* Thu Jan 12 2012 Iain Arnell <iarnell@gmail.com> 5.90007-1
- update to latest upstream version
- BR perldoc

* Sun Oct 30 2011 Iain Arnell <iarnell@gmail.com> 5.90006-1
- update to latest upstream version
- remove unnecessary explicit requires

* Mon Aug 29 2011 Iain Arnell <iarnell@gmail.com> 5.90002-1
- update to latest upstream version

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 5.80032-2
- Perl mass rebuild

* Mon Mar 07 2011 Iain Arnell <iarnell@gmail.com> 5.80032-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.80030-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 08 2011 Iain Arnell <iarnell@gmail.com> 5.80030-1
- update to latest upstream version
- update R/BR perl(MooseX::MethodAttributes::Inheritable) >= 0.24
- drop R perl(Class::Data::Inheritable)

* Sat Oct 09 2010 Iain Arnell <iarnell@gmail.com> 5.80029-1
- update by Fedora::App::MaintainerTools 0.006
- updating to latest GA CPAN version (5.80029)
- added a new br on perl(HTML::HeadParser) (version 0)
- altered br on perl(MooseX::Getopt) (0.25 => 0.30)
- added a new req on perl(HTML::HeadParser) (version 0)
- altered req on perl(MooseX::Getopt) (0.25 => 0.30)
- disable auto_install

* Sat Aug 28 2010 Iain Arnell <iarnell@gmail.com> 5.80025-1
- update by Fedora::App::MaintainerTools 0.006
- updating to latest GA CPAN version (5.80025)
- altered br on perl(CGI::Simple::Cookie) (0 => 1.109)
- added a new br on perl(Data::OptList) (version 0)
- altered br on perl(HTTP::Body) (1.04 => 1.06)
- altered br on perl(Moose) (0.93 => 1.03)
- altered req on perl(CGI::Simple::Cookie) (0 => 1.109)
- added a new req on perl(Class::Data::Inheritable) (version 0)
- added a new req on perl(Data::OptList) (version 0)
- altered req on perl(HTTP::Body) (1.04 => 1.06)
- altered req on perl(Moose) (0.93 => 1.03)
- dropped br on perl(Test::MockObject)

* Fri Jul  9 2010 Marcela Mašláňová <mmaslano@redhat.com> - 5.80021-3
- 590961 add missing BR (warnings about nroff in buil log)

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 5.80021-2
- Mass rebuild with perl-5.12.0

* Sun Mar 07 2010 Chris Weyl <cweyl@alumni.drew.edu> 5.80021-1
- update by Fedora::App::MaintainerTools 0.004
- PERL_INSTALL_ROOT => DESTDIR
- updating to latest GA CPAN version (5.80021)
- altered br on perl(Class::MOP) (0.83 => 0.95)
- altered br on perl(HTTP::Request) (0 => 5.814)
- altered br on perl(HTTP::Request::AsCGI) (0.8 => 1.0)
- altered br on perl(HTTP::Response) (0 => 5.813)
- altered br on perl(Moose) (0.90 => 0.93)
- added a new br on perl(MooseX::Getopt) (version 0.25)
- altered br on perl(MooseX::MethodAttributes::Inheritable) (0.16 => 0.19)
- added a new br on perl(MooseX::Role::WithOverloading) (version 0.05)
- added a new br on perl(MooseX::Types) (version 0)
- added a new br on perl(MooseX::Types::Common::Numeric) (version 0)
- altered br on perl(Test::More) (0 => 0.88)
- altered br on perl(namespace::clean) (0 => 0.13)
- dropped old BR on perl(Test::Pod::Coverage)
- altered req on perl(Class::MOP) (0.83 => 0.95)
- altered req on perl(HTTP::Request) (0 => 5.814)
- altered req on perl(HTTP::Request::AsCGI) (0.8 => 1.0)
- altered req on perl(HTTP::Response) (0 => 5.813)
- altered req on perl(Moose) (0.90 => 0.93)
- added a new req on perl(MooseX::Getopt) (version 0.25)
- altered req on perl(MooseX::MethodAttributes::Inheritable) (0.16 => 0.19)
- added a new req on perl(MooseX::Role::WithOverloading) (version 0.05)
- added a new req on perl(MooseX::Types) (version 0)
- added a new req on perl(MooseX::Types::Common::Numeric) (version 0)
- altered req on perl(namespace::clean) (0 => 0.13)
- dropped old requires on perl(Class::Accessor::Fast)
- dropped old requires on perl(Class::Data::Inheritable)
- dropped old requires on perl(File::Modified)

* Sat Sep 26 2009 Chris Weyl <cweyl@alumni.drew.edu> 5.80013-2
- dis-enable certain optional tests until a couple RT tix are resolved

* Sat Sep 26 2009 Chris Weyl <cweyl@alumni.drew.edu> 5.80013-1
- auto-update to 5.80013 (by cpan-spec-update 0.01)
- altered br on perl(Moose) (0.78 => 0.90)
- altered br on perl(MooseX::Emulate::Class::Accessor::Fast) (0.00801 => 0.00903)
- altered br on perl(MooseX::MethodAttributes::Inheritable) (0.15 => 0.16)
- altered br on perl(namespace::autoclean) (0 => 0.09)
- altered req on perl(Moose) (0.78 => 0.90)
- altered req on perl(MooseX::Emulate::Class::Accessor::Fast) (0.00801 => 0.00903)
- altered req on perl(MooseX::MethodAttributes::Inheritable) (0.15 => 0.16)
- altered req on perl(namespace::autoclean) (0 => 0.09)

* Tue Aug 25 2009 Chris Weyl <cweyl@alumni.drew.edu> 5.80011-1
- switch filtering system
- auto-update to 5.80011 (by cpan-spec-update 0.01)
- added a new br on perl(List::MoreUtils) (version 0)
- altered br on perl(Module::Pluggable) (3.01 => 3.9)
- altered br on perl(MooseX::MethodAttributes::Inheritable) (0.12 => 0.15)
- added a new req on perl(List::MoreUtils) (version 0)
- altered req on perl(Module::Pluggable) (3.01 => 3.9)
- altered req on perl(MooseX::MethodAttributes::Inheritable) (0.12 => 0.15)

* Mon Jul 27 2009 Chris Weyl <cweyl@alumni.drew.edu> 5.80007-1
- auto-update to 5.80007 (by cpan-spec-update 0.01)
- added a new br on perl(String::RewritePrefix) (version 0.004)
- added a new br on perl(Task::Weaken) (version 0)
- added a new br on perl(namespace::autoclean) (version 0)
- added a new req on perl(String::RewritePrefix) (version 0.004)
- added a new req on perl(Task::Weaken) (version 0)
- added a new req on perl(namespace::autoclean) (version 0)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.80005-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jun 14 2009 Chris Weyl <cweyl@alumni.drew.edu> 5.80005-3
- flesh out to full requires list (from upstream metadata)
- auto-update to 5.80005 (by cpan-spec-update 0.01)
- added a new req on perl(Text::Balanced) (version 0)
- added a new req on perl(HTTP::Response) (version 0)
- added a new req on perl(LWP::UserAgent) (version 0)
- added a new req on perl(Scalar::Util) (version 0)
- added a new req on perl(CGI::Simple::Cookie) (version 0)
- added a new req on perl(Class::C3::Adopt::NEXT) (version 0.07)
- added a new req on perl(Class::MOP) (version 0.83)
- added a new req on perl(Time::HiRes) (version 0)
- added a new req on perl(MRO::Compat) (version 0)
- added a new req on perl(File::Modified) (version 0)
- added a new req on perl(HTTP::Headers) (version 1.64)
- added a new req on perl(Sub::Exporter) (version 0)
- added a new req on perl(Tree::Simple) (version 1.15)
- added a new req on perl(B::Hooks::EndOfScope) (version 0.08)
- added a new req on perl(namespace::clean) (version 0)
- added a new req on perl(HTML::Entities) (version 0)
- added a new req on perl(Moose) (version 0.78)
- added a new req on perl(Data::Dump) (version 0)
- added a new req on perl(Tree::Simple::Visitor::FindByPath) (version 0)
- added a new req on perl(Module::Pluggable) (version 3.01)
- added a new req on perl(Text::SimpleTable) (version 0.03)
- altered req on perl(HTTP::Request::AsCGI) (0.5 => 0.8)
- added a new req on perl(HTTP::Request) (version 0)
- added a new req on perl(HTTP::Body) (version 1.04)
- added a new req on perl(Path::Class) (version 0.09)
- added a new req on perl(MooseX::MethodAttributes::Inheritable) (version 0.12)
- added a new req on perl(URI) (version 1.35)
- added a new req on perl(Carp) (version 0)

* Sat Jun 13 2009 Iain Arnell <iarnell@gmail.com> 5.80005-2
- requires perl(MooseX::Emulate::Class::Accessor::Fast)

* Tue Jun 09 2009 Chris Weyl <cweyl@alumni.drew.edu> 5.80005-1
- auto-update to 5.80005 (by cpan-spec-update 0.01)
- altered br on perl(MooseX::MethodAttributes::Inheritable) (0.10 => 0.12)

* Fri May 29 2009 Chris Weyl <cweyl@alumni.drew.edu> 5.80004-1
- drop Catalyst::Manual exclusions (no longer present)
- streamline req/prov filtering
- auto-update to 5.80004 (by cpan-spec-update 0.01)
- added a new br on perl(Scalar::Util) (version 0)
- added a new br on perl(Class::MOP) (version 0.83)
- added a new br on perl(Time::HiRes) (version 0)
- added a new br on perl(MRO::Compat) (version 0)
- added a new br on perl(Sub::Exporter) (version 0)
- added a new br on perl(B::Hooks::EndOfScope) (version 0.08)
- added a new br on perl(namespace::clean) (version 0)
- added a new br on perl(Moose) (version 0.78)
- added a new br on perl(MooseX::MethodAttributes::Inheritable) (version 0.10)
- added a new br on perl(Carp) (version 0)
- added a new br on perl(Text::Balanced) (version 0)
- added a new br on perl(Class::C3::Adopt::NEXT) (version 0.07)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)
- added a new br on perl(Test::MockObject) (version 1.07)
- altered br on perl(HTTP::Request::AsCGI) (0.5 => 0.8)
- added a new br on perl(MooseX::Emulate::Class::Accessor::Fast) (version 0.00801)

* Sat Apr 11 2009 Chris Weyl <cweyl@alumni.drew.edu> 5.71001-2
- return Catalyst::Manual perl-Catalyst-Manual

* Thu Apr 02 2009 Chris Weyl <cweyl@alumni.drew.edu> 5.71001-1
- update to 5.71001

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.71000-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 25 2009 Chris Weyl <cweyl@alumni.drew.edu> 5.71000-1
- update to 5.71000

* Thu Oct 23 2008 Chris Weyl <cweyl@alumni.drew.edu> 5.7015-1
- update to 5.7015

* Mon Jun 23 2008 Chris Weyl <cweyl@alumni.drew.edu> 5.7014-3
- Quiet STDERR somewhat on build

* Sat May 31 2008 Chris Weyl <cweyl@alumni.drew.edu> 5.7014-2
- pull catalyst.pl back from perl-Catalyst-Devel, put into subpackage: too
  much of a headache to keep this bit of -Runtime in -Devel
- pull in tests
- deal with perl-Catalyst-Manual issues

* Sat May 31 2008 Chris Weyl <cweyl@alumni.drew.edu> 5.7014-1
- update to 5.7014

* Thu Mar 27 2008 Chris Weyl <cweyl@alumni.drew.edu> 5.7012-3
- nuke Catalyst/Manual.pm from this dist -- handled in perl-Catalyst-Manual

* Wed Mar 05 2008 Tom "spot" Callaway <tcallawa@redhat.com> 5.7012-2
- rebuild for new perl

* Sat Mar 01 2008 Chris Weyl <cweyl@alumni.drew.edu> 5.7012-1
- update to 5.7012

* Sun Oct 28 2007 Chris Weyl <cweyl@alumni.drew.edu> 5.7011-1
- update to 5.7011

* Mon May 14 2007 Chris Weyl <cweyl@alumni.drew.edu> 5.7007-4
- bump

* Mon May 14 2007 Chris Weyl <cweyl@alumni.drew.edu> 5.7007-3
- additional br's

* Fri Apr 27 2007 Chris Weyl <cweyl@alumni.drew.edu> 5.7007-2
- exclude catalyst.pl from this package -- it depends on
  perl(Catalyst::Helper), which is provided by perl-Catalyst-Devel (but which
  has a buildreq on this package).  We will provide catalyst.pl in
  perl-Catalyst-Devel instead.

* Tue Apr 10 2007 Chris Weyl <cweyl@alumni.drew.edu> 5.7007-1
- Specfile autogenerated by cpanspec 1.70.
