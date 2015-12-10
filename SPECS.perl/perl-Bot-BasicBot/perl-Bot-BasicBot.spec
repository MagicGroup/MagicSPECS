Name:           perl-Bot-BasicBot
Version:	0.89
Release:	4%{?dist}
Summary:        Simple irc bot baseclass
Summary(zh_CN.UTF-8): 简单的 irc 机器人
License:        GPL+ or Artistic
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
URL:            http://search.cpan.org/dist/Bot-BasicBot/
Source0:        http://www.cpan.org/authors/id/H/HI/HINRIK/Bot-BasicBot-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(base)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(IRC::Utils)
BuildRequires:  perl(POE)
BuildRequires:  perl(POE::Component::IRC) >= 6.62
BuildRequires:  perl(POE::Component::IRC::State)
BuildRequires:  perl(POE::Component::IRC::Plugin::Connector)
BuildRequires:  perl(POE::Filter::Line)
BuildRequires:  perl(POE::Kernel)
BuildRequires:  perl(POE::Session)
BuildRequires:  perl(POE::Wheel::Run)
BuildRequires:  perl(Text::Wrap)
# Tests
BuildRequires:  perl(IO::Socket)
BuildRequires:  perl(IO::Socket::INET)
BuildRequires:  perl(Test::More)
Requires:       perl(POE::Component::IRC) >= 6.62
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Basic bot system designed to make it easy to do simple bots, optionally
forking longer processes (like searches) concurrently in the background.

%description -l zh_CN.UTF-8
简单的 irc 机器人。

%prep
%setup -q -n Bot-BasicBot-%{version}
find examples -type f -exec chmod 644 {} \;
iconv -f latin1 -t utf8 README > README.utf8 && mv README.utf8 README

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;
%{_fixperms} %{buildroot}/*
magic_rpm_clean.sh

%check


%files
%doc Changes dist.ini examples LICENSE META.json README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.89-4
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 0.89-3
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.89-2
- 为 Magic 3.0 重建

* Mon Apr 27 2015 Liu Di <liudidi@gmail.com> - 0.89-1
- 更新到 0.89

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.87-8
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.87-7
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.87-6
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.87-5
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.87-4
- 为 Magic 3.0 重建

* Sat Jan 28 2012 Liu Di <liudidi@gmail.com> - 0.87-3
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.87-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 26 2011 Petr Sabata <contyk@redhat.com> 0.87-1
- Initial package.
