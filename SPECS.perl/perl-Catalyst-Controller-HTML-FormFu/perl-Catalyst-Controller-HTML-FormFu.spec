Name:           perl-Catalyst-Controller-HTML-FormFu
Version:	1.00
Release:	1%{?dist}
Summary:        HTML::FormFu controller for Catalyst
Summary(zh_CN.UTF-8): Catalyst 的 HTML::FormFu 控制器
License:        GPL+ or Artistic
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
URL:            http://search.cpan.org/dist/Catalyst-Controller-HTML-FormFu/
Source0:        http://search.cpan.org/CPAN/authors/id/C/CF/CFRANKS/Catalyst-Controller-HTML-FormFu-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(Catalyst::Action::RenderView)
BuildRequires:  perl(Catalyst::Component::InstancePerContext)
BuildRequires:  perl(Catalyst::Plugin::ConfigLoader)
BuildRequires:  perl(Catalyst::Plugin::Session::State::Cookie)
BuildRequires:  perl(Catalyst::Plugin::Session::Store::File)
BuildRequires:  perl(Catalyst::Runtime) >= 5.70
BuildRequires:  perl(Catalyst::View::TT)
BuildRequires:  perl(Config::Any)
BuildRequires:  perl(Config::General)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(HTML::FormFu) >= 0.09000
BuildRequires:  perl(Moose)
BuildRequires:  perl(MooseX::ChainedAccessors) >= 0.02
BuildRequires:  perl(namespace::autoclean)
BuildRequires:  perl(Regexp::Assemble)
BuildRequires:  perl(Task::Weaken)
BuildRequires:  perl(Template)
BuildRequires:  perl(Test::WWW::Mechanize) >= 1.16
BuildRequires:  perl(Test::WWW::Mechanize::Catalyst)
Requires:       perl(Catalyst::Component::InstancePerContext)
Requires:       perl(Catalyst::Runtime) >= 5.70
Requires:       perl(HTML::FormFu) >= 0.09000
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This base controller merges the functionality of HTML::FormFu with Catalyst.

%description -l zh_CN.UTF-8
Catalyst 的 HTML::FormFu 控制器。

%prep
%setup -q -n Catalyst-Controller-HTML-FormFu-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*
magic_rpm_clean.sh

%check


%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri Jun 05 2015 Liu Di <liudidi@gmail.com> - 1.00-1
- 更新到 1.00

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.09003-18
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 0.09003-17
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.09003-16
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 0.09003-15
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.09003-14
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 0.09003-13
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.09003-12
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.09003-11
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.09003-10
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.09003-9
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.09003-8
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.09003-7
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.09003-6
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.09003-5
- 为 Magic 3.0 重建

* Sat Jan 28 2012 Liu Di <liudidi@gmail.com> - 0.09003-4
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.09003-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.09003-2
- Perl mass rebuild

* Wed May 18 2011 Iain Arnell <iarnell@gmail.com> 0.09003-1
- update to latest upstream version

* Sat Apr 09 2011 Iain Arnell <iarnell@gmail.com> 0.09000-1
- update to latest upstream version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.08002-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.08002-2
- 661697 rebuild for fixing problems with vendorach/lib

* Sat Sep 25 2010 Iain Arnell <iarnell@gmail.com> 0.08002-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Fri Apr 30 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.06001-2
- Mass rebuild with perl-5.12.0

* Fri Dec 18 2009 Iain Arnell <iarnell@gmail.com> 0.06001-1
- update to latest upstream version

* Wed Dec 09 2009 Iain Arnell <iarnell@gmail.com> 0.06000-1
- update to latest upstream version

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.05000-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05000-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 08 2009 Iain Arnell <iarnell@gmail.com> 0.05000-1
- update to latest upstream version
- BR perl(namespace::autoclean)

* Wed Apr 22 2009 Iain Arnell <iarnell@gmail.com> 0.04003-1
- update to 0.04003
- BR perl(MRO::Compat)

* Fri Apr 17 2009 Iain Arnell <iarnell@gmail.com> 0.04001-1
- update to latest upstream version

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.03007-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 10 2008 Iain Arnell <iarnell@gmail.com> 0.03007-2
- temporarily change source url to use search.cpan.org

* Mon Dec 08 2008 Iain Arnell 0.03007-1
- Specfile autogenerated by cpanspec 1.77.
