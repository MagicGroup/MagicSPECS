Name:           perl-File-ChangeNotify
Summary:        Watch for changes to files, cross-platform style
Version:	0.24
Release:	3%{?dist}
License:        Artistic 2.0
Group:          Development/Libraries
Source0:        http://search.cpan.org/CPAN/authors/id/D/DR/DROLSKY/File-ChangeNotify-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/File-ChangeNotify
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(Carp)
BuildRequires:  perl(Class::MOP)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Module::Build) >= 0.3601
BuildRequires:  perl(Module::Pluggable::Object)
BuildRequires:  perl(Moose)
BuildRequires:  perl(MooseX::Params::Validate) >= 0.08
BuildRequires:  perl(MooseX::SemiAffordanceAccessor)
BuildRequires:  perl(namespace::autoclean)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(Test::Without::Module)
BuildRequires:  perl(Time::HiRes)
BuildRequires:  perl(Test::Exception)
BuildRequires:  perl(Linux::Inotify2)

Requires:       perl(Carp)
Requires:       perl(Class::MOP)
Requires:       perl(File::Find)
Requires:       perl(File::Spec)
Requires:       perl(Module::Pluggable::Object)
Requires:       perl(Moose)
Requires:       perl(MooseX::Params::Validate) >= 0.08
Requires:       perl(MooseX::SemiAffordanceAccessor)
Requires:       perl(namespace::autoclean)
Requires:       perl(Time::HiRes)

%{?filter_setup:
%filter_from_requires /^perl(IO::KQueue)/d
%?perl_default_filter
}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(IO::KQueue\\)
#{?perl_default_subpackage_tests}

%description
Watch for changes to files, easily, cleanly, and across different platforms.


%prep
%setup -q -n File-ChangeNotify-%{version}

%build
perl Build.PL --installdirs vendor
./Build

%install
rm -rf %{buildroot}

./Build install --destdir %{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'

%{_fixperms} %{buildroot}/*

%check
./Build test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes README LICENSE
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.24-3
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.24-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.24-1
- 更新到 0.24

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.20-19
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.20-18
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.20-17
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.20-16
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.20-15
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.20-14
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.20-13
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.20-12
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.20-11
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.20-10
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.20-9
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.20-8
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.20-7
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.20-6
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.20-5
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.20-4
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.20-3
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.20-2
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Robin Lee <cheeselee@fedoraproject.org> - 0.20-1
- Update to 0.20
- Changed to Build.PL style
- BR: add perl(Test::Exception), perl(Linux::Inotify2)

* Fri Jul 22 2011 Iain Arnell <iarnell@gmail.com> 0.16-6
- update filtering for rpm 4.9

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.16-5
- Perl mass rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 0.16-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.16-2
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Aug 26 2010 Iain Arnell <iarnell@gmail.com> 0.16-1
- update by Fedora::App::MaintainerTools 0.006
- updating to latest GA CPAN version (0.16)
- new license Artistic 2.0
- altered br on perl(ExtUtils::MakeMaker) (0 => 6.31)
- altered br on perl(Module::Build) (0 => 0.3601)
- altered br on perl(Test::More) (0 => 0.88)
- added a new br on perl(namespace::autoclean) (version 0)
- added a new req on perl(namespace::autoclean) (version 0)
- BR perl(Test::Exception), perl(Test::Without::Module) to enable tests

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.13-1
- update

* Sat May 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.12-4
- Mass rebuild with perl-5.12.0

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.12-3
- Mass rebuild with perl-5.12.0

* Mon Mar 15 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.12-2
- update by Fedora::App::MaintainerTools 0.006

* Sat Mar 13 2010 Chris Weyl <cweyl@alumni.drew.edu> 0.12-1
- update by Fedora::App::MaintainerTools 0.006
- PERL_INSTALL_ROOT => DESTDIR
- updating to latest GA CPAN version (0.12)
- added a new br on perl(Module::Build)
- dropped old BR on perl(Module::Build::Compat)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.07-2
- rebuild against perl 5.10.1

* Tue Aug 11 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.07-1
- auto-update to 0.07 (by cpan-spec-update 0.01)
- added a new req on perl(Carp) (version 0)
- added a new req on perl(Class::MOP) (version 0)
- added a new req on perl(File::Find) (version 0)
- added a new req on perl(File::Spec) (version 0)
- added a new req on perl(Module::Pluggable::Object) (version 0)
- added a new req on perl(Moose) (version 0)
- added a new req on perl(MooseX::Params::Validate) (version 0.08)
- added a new req on perl(MooseX::SemiAffordanceAccessor) (version 0)
- added a new req on perl(Time::HiRes) (version 0)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 08 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.06-1
- submission

* Sun Jun 07 2009 Chris Weyl <cweyl@alumni.drew.edu> 0.06-0
- initial RPM packaging
- generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)
