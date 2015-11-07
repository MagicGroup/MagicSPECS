Name:           perl-Catalyst-Plugin-Authentication
Summary:        Infrastructure plugin for the Catalyst authentication framework
Version:	0.10023
Release:	2%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/B/BO/BOBTFISH/Catalyst-Plugin-Authentication-%{version}.tar.gz
URL:            http://search.cpan.org/dist/Catalyst-Plugin-Authentication/
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(Catalyst::Plugin::Session) >= 0.10
BuildRequires:  perl(Catalyst::Plugin::Session::State::Cookie)
BuildRequires:  perl(Catalyst::Runtime)
BuildRequires:  perl(Class::Inspector)
BuildRequires:  perl(Class::MOP)
BuildRequires:  perl(CPAN)
BuildRequires:  perl(Digest::MD5)
BuildRequires:  perl(Digest::SHA1)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.42
BuildRequires:  perl(Moose)
BuildRequires:  perl(MRO::Compat)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::MockObject)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::WWW::Mechanize::Catalyst)

Requires:       perl(Catalyst::Plugin::Session) >= 0.10
Requires:       perl(Catalyst::Runtime)
Requires:       perl(Class::Inspector)
Requires:       perl(MRO::Compat)

# obsolete/provide old tests subpackage
# can be removed during F19 development cycle
Obsoletes:      %{name}-tests < 0.10018-3
Provides:       %{name}-tests = %{version}-%{release}

%{?perl_default_filter}

%description
The authentication plugin provides generic user support for Catalyst apps.
It is the basis for both authentication (checking the user is who they
claim to be), and authorization (allowing the user to do what the system
authorizes them to do).

%prep
%setup -q -n Catalyst-Plugin-Authentication-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*

%check
TEST_POD=1 

%files
%doc Changes README t/
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.10023-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.10023-1
- 更新到 0.10023

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.10018-18
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.10018-17
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.10018-16
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.10018-15
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.10018-14
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.10018-13
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.10018-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.10018-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.10018-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.10018-9
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.10018-8
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.10018-7
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.10018-6
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.10018-5
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.10018-4
- 为 Magic 3.0 重建

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> 0.10018-3
- drop tests subpackage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10018-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 01 2011 Iain Arnell <iarnell@gmail.com> 0.10018-1
- update to latest upstream version

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.10017-2
- Perl mass rebuild

* Sun Mar 13 2011 Iain Arnell <iarnell@gmail.com> 0.10017-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10016-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.10016-3
- 661697 rebuild for fixing problems with vendorach/lib

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.10016-2
- Mass rebuild with perl-5.12.0

* Tue Feb 23 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.10016-1
- update by Fedora::App::MaintainerTools 0.003
- PERL_INSTALL_ROOT => DESTDIR
- altered br on perl(Test::More) (0 => 0.88)

* Thu Sep 03 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.10015-1
- switch filtering systems...
- auto-update to 0.10015 (by cpan-spec-update 0.01)
- added a new br on perl(Class::MOP) (version 0)
- added a new br on perl(Moose) (version 0)

* Sat Aug 08 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.10013-2
- auto-update to 0.10013 (by cpan-spec-update 0.01)
- added a new br on CPAN (inc::Module::AutoInstall found)

* Sat Aug 08 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.10013-1
- auto-update to 0.10013 (by cpan-spec-update 0.01)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10012-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 15 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.10012-1
- switch fitering system to a cleaner one
- auto-update to 0.10012 (by cpan-spec-update 0.01)
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.42)
- added a new req on perl(Class::Inspector) (version 0)
- added a new req on perl(MRO::Compat) (version 0)

* Thu Apr 02 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.10011-1
- update to 0.10011

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10010-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.10010-1
- update to 0.10010

* Sun Jan 25 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.100092-1
- update to 0.100092

* Sun Oct 26 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.10008-1
- update to 0.10008

* Thu Sep 25 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.10007-1
- update to 0.10007

* Tue Jun 17 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.10006-4
- bump

* Mon Jun 16 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.10006-3
- add br on Test::Exception

* Mon Jun 02 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.10006-2
- drop buildroot references from prep

* Sat May 31 2008 Chris Weyl <cweyl@alumni.drew.edu> 0.10006-1
- Specfile autogenerated by cpanspec 1.75.
