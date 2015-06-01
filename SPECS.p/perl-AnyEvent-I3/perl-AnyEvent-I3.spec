%define srcname AnyEvent-I3

Name:           perl-AnyEvent-I3
Version:	0.16
Release:	1%{?dist}
Summary:        Communicate with the i3 window manager
Summary(zh_CN.UTF-8): 与 I3 窗口管理器通信

Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/anyevent-i3/
Source0:        http://search.cpan.org/CPAN/authors/id/M/MS/MSTPLBG/%{srcname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Module::Install)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}


%description
This module connects to the i3 window manager using the UNIX socket based
IPC interface it provides (if enabled in the configuration file). You can
then subscribe to events or send messages and receive their replies.

%description -l zh_CN.UTF-8
与 I3 窗口管理器通信。

%prep
%setup -q -n %{srcname}-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}/*
magic_rpm_clean.sh

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc README Changes
%{perl_vendorlib}/AnyEvent/I3.pm
%{_mandir}/man3/*.3*


%changelog
* Wed Apr 22 2015 Liu Di <liudidi@gmail.com> - 0.16-1
- 更新到 0.16

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.06-10
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.06-9
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.06-8
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Petr Pisar <ppisar@redhat.com> - 0.06-6
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 0.06-4
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.06-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 14 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.06-2
- 661697 rebuild for fixing problems with vendorach/lib

* Wed Jun 23 2010 Simon Wesp <cassmodiah@fedoraproject.org> - 0.06-1
- New Upstream Release

* Tue Jun 15 2010 Simon Wesp <cassmodiah@fedoraproject.org> - 0.05-1
- New Upstream Release

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.04-2
- Mass rebuild with perl-5.12.0

* Wed Apr 14 2010 Simon Wesp <cassmodiah@fedoraproject.org> - 0.04-1
- Initial package release
