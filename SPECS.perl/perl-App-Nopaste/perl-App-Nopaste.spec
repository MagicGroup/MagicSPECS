Name:           perl-App-Nopaste
Version:	1.004
Release:	2%{?dist}
Summary:        Easy access to any pastebin
Summary(zh_CN.UTF-8): 简单访问任何 pastebin
License:        GPL+ or Artistic
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
URL:            http://search.cpan.org/dist/App-Nopaste/
Source0:        http://www.cpan.org/authors/id/E/ET/ETHER/App-Nopaste-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(inc::Module::Install)
BuildRequires:  perl(Browser::Open)
BuildRequires:  perl(Class::Load)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Getopt::Long::Descriptive) >= 0.090
BuildRequires:  perl(JSON)
BuildRequires:  perl(Module::Pluggable)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(WWW::Mechanize)
# necessary for optional modules
BuildRequires:  perl(Clipboard)
BuildRequires:  perl(Config::GitLike)
BuildRequires:  perl(WWW::Pastebin::PastebinCom::Create)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
# autoreq doesn't catch this
Requires:       perl(Browser::Open)
# necessary for optional modules
Requires:       perl(Clipboard)
Requires:       perl(Config::GitLike)
Requires:       perl(WWW::Pastebin::PastebinCom::Create)
# for ssh plugin
Requires:       /usr/bin/scp

%description
Pastebins (also known as nopaste sites) let you post text, usually code,
for public viewing. They're used a lot in IRC channels to show code that
would normally be too long to give directly in the channel (hence the
name nopaste).

%description -l zh_CN.UTF-8
简单访问任何 pastebin。

%package -n nopaste
# needs to beat old nopaste-2835-3
Epoch:          1
License:        GPL+ or Artistic
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Summary:        Access pastebins from the command line
Summary(zh_CN.UTF-8): 从命令行访问 pastebin
Requires:       %{name} = 0:%{version}-%{release}

%description -n nopaste
This application lets you post text to pastebins from the command line.

Pastebins (also known as nopaste sites) let you post text, usually code, for
public viewing. They're used a lot in IRC channels to show code that would
normally be too long to give directly in the channel (hence the name nopaste).

%description -n nopaste -l zh_CN.UTF-8
从命令行访问 pastebin。

%prep
%setup -q -n App-Nopaste-%{version}
find lib -type f | xargs chmod -x

%build
echo "y\n" | PERL5_CPANPLUS_IS_RUNNING=1 %{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*
magic_rpm_clean.sh

%check
make test

%files
%doc Changes
%{perl_vendorlib}/*
%{_mandir}/man3/*

%files -n nopaste
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.004-2
- 为 Magic 3.0 重建

* Thu Apr 23 2015 Liu Di <liudidi@gmail.com> - 1.004-1
- 更新到 1.004

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.90-3
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.90-2
- 为 Magic 3.0 重建

* Fri Nov 02 2012 Iain Arnell <iarnell@gmail.com> 1:0.90-1
- update to latest upstream version

* Sat Jul 21 2012 Iain Arnell <iarnell@gmail.com> 1:0.35-1
- update to latest upstream version
- BR inc::Module::Install

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.33-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 23 2012 Petr Pisar <ppisar@redhat.com> - 0.33-2
- Perl 5.16 rebuild

* Thu Jan 05 2012 Iain Arnell <iarnell@gmail.com> 0.33-1
- update to latest upstream version

* Sat Oct 22 2011 Iain Arnell <iarnell@gmail.com> 0.32-1
- update to latest upstream version

* Fri Sep 23 2011 Iain Arnell <iarnell@gmail.com> 1:0.31-1
- update to latest upstream version
- drop defattr in files sections

* Sat Aug 27 2011 Iain Arnell <iarnell@gmail.com> 1:0.30-1
- update to latest upstream version

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.28-2
- Perl mass rebuild

* Sat Apr 09 2011 Iain Arnell <iarnell@gmail.com> 1:0.28-1
- update to latest upstream version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 15 2011 Iain Arnell <iarnell@gmail.com> 0.25-1
- update to latest upstream version

* Sun Jan 02 2011 Iain Arnell <iarnell@gmail.com> 0.24-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Fri Dec 03 2010 Iain Arnell <iarnell@gmail.com> 0.23-1
- update to latest upstream version

* Tue Jun 15 2010 Iain Arnell <iarnell@gmail.com> 0.22-1
- update to latest upstream

* Sat May 08 2010 Iain Arnell - 0.21-2
- bump for rebuild with perl-5.12.0

* Sat May 01 2010 Iain Arnell <iarnell@gmail.com> 0.21-1
- update to latest upstream

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.20-2
- Mass rebuild with perl-5.12.0

* Sun Apr 18 2010 Iain Arnell <iarnell@gmail.com> 0.20-1
- update to latest upstream version

* Thu Feb 25 2010 Iain Arnell <iarnell@gmail.com> 0.19-1
- update to latest upstream version

* Mon Jan 04 2010 Iain Arnell <iarnell@gmail.com> 0.18-1
- update to latest upstream version (adds ssh support)

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.17-2
- rebuild against perl 5.10.1

* Sat Nov 07 2009 Iain Arnell <iarnell@gmail.com> 0.17-1
- update to latest upstream version (fixes Gist support better)

* Sun Oct 18 2009 Iain Arnell <iarnell@gmail.com> 0.16-1
- update to latest upstream version (fixes rt#50500 Gist support)

* Fri Jul 31 2009 Iain Arnell <iarnell@gmail.com> 0.15-1
- update to latest upstream version

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jun 21 2009 Iain Arnell <iarnell@gmail.com> 0.11-2
- pretend that CPANPLUS is running

* Sun Jun 21 2009 Iain Arnell <iarnell@gmail.com> 0.11-1
- update to latest upstream version

* Thu Jun 18 2009 Iain Arnell <iarnell@gmail.com> 0.10-4
- don't require Git since Config::INI::Reader is sufficient
- don't require WWW::Pastebin::RafbNet::Create since rafb.net is gone

* Sat Jun 06 2009 Iain Arnell <iarnell@gmail.com> 0.10-3
- nopaste gets its own subpackage (to replace existing nopaste pacakge now that
  rafb.net has gone)

* Sun May 03 2009 Iain Arnell <iarnell@gmail.com> 0.10-2
- rename nopaste command to avoid conflict with existing nopaste rpm

* Sun Apr 19 2009 Iain Arnell <iarnell@gmail.com> 0.10-1
- Specfile autogenerated by cpanspec 1.77.
- add requires for optional modules
- add bindir and man1 to files
