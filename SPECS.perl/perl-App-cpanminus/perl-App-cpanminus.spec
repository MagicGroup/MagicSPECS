Name:           perl-App-cpanminus
Version:	1.7039
Release:	4%{?dist}
Summary:        Library for get, unpack, build and install CPAN modules
Summary(zh_CN.UTF-8): 获取、编译和安装 CPAN 模块的库
License:        GPL+ or Artistic
Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
URL:            http://search.cpan.org/dist/App-cpanminus/
Source0:        http://www.cpan.org/authors/id/M/MI/MIYAGAWA/App-cpanminus-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
# Required by bin/cpanm
Requires:       perl(Cwd)
Requires:       perl(ExtUtils::Install) >= 1.46
Requires:       perl(ExtUtils::MakeMaker) >= 6.31
Requires:       perl(File::Path)
Requires:       perl(File::Spec)
Requires:       perl(Getopt::Long)
Requires:       perl(IO::File)
Requires:       perl(IO::Socket)
Requires:       perl(JSON)
Requires:       perl(Module::Build)
Requires:       perl(Parse::CPAN::Meta)
Requires:       perl(Time::Local)
Requires:       perl(YAML)
# XXX: Keep Provides: cpanminus to allow `yum install cpanminus' instead of
# longer `yum install perl-App-cpanminus'.
Provides:       cpanminus = %{version}-%{release}
Obsoletes:      cpanminus <= 1.2002

# RPM 4.8 style
%{?filter_setup:
%filter_from_requires /^perl(App::cpanminus::script)$/d
%?perl_default_filter
}
# RPM 4.9 style
%global __requires_exclude %{?__requires_exclude:__requires_exclude|}^perl\\(App::cpanminus::script\\)$

%description
Why? It's dependency free, requires zero configuration, and stands alone 
but it's maintainable and extensible with plug-ins and friendly to shell 
scripting. When running, it requires only 10 MB of RAM.

%description -l zh_CN.UTF-8
获取、编译和安装 CPAN 模块的库。

%prep
%setup -q -n App-cpanminus-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;
%{_fixperms} %{buildroot}/*
magic_rpm_clean.sh

%check


%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*
%{_mandir}/man1/*
%{_bindir}/cpanm

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.7039-4
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.7039-3
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.7039-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.7039-1
- 更新到 1.7039

* Thu Apr 23 2015 Liu Di <liudidi@gmail.com> - 1.7031-1
- 更新到 1.7031

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.5007-6
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.5007-5
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.5007-4
- 为 Magic 3.0 重建

* Fri Jan 27 2012 Liu Di <liudidi@gmail.com> - 1.5007-3
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5007-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 21 2011 Marcela Mašláňová <mmaslano@redhat.com> 1.5007-1
- 1.5007 bump

* Wed Nov 30 2011 Petr Šabata <contyk@redhat.com> - 1.5006-1
- 1.5006 bump

* Wed Nov 23 2011 Petr Šabata <contyk@redhat.com> - 1.5005-1
- 1.5005 bump
- defattr removed

* Wed Nov 09 2011 Petr Sabata <contyk@redhat.com> - 1.5004-1
- 1.5004 bump

* Wed Oct 19 2011 Petr Sabata <contyk@redhat.com> - 1.5003-1
- 1.5003 bump

* Tue Oct 18 2011 Petr Sabata <contyk@redhat.com> - 1.5002-1
- 1.5002 bump

* Fri Oct 14 2011 Petr Sabata <contyk@redhat.com> - 1.5001-1
- 1.5001 bump

* Thu Oct 13 2011 Petr Sabata <contyk@redhat.com> - 1.5000-1
- 1.5000 bump

* Fri Jul 22 2011 Petr Pisar <ppisar@redhat.com> - 1.4008-3
- RPM 4.9 dependency filtering added

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.4008-2
- Perl mass rebuild

* Thu Jun 16 2011 Petr Pisar <ppisar@redhat.com> - 1.4008-1
- 1.4008 bump

* Wed May 18 2011 Petr Pisar <ppisar@redhat.com> - 1.4007-1
- 1.4007 bump
- LWP is optional since this package bundles HTTP::Tiny. Upstream recognized
  LWP being heavy. Follow upstream decision in RPM package dependencies.

* Tue May 17 2011 Petr Pisar <ppisar@redhat.com> - 1.4006-1
- 1.4006 bump
- Fix obsoleted version string

* Thu May 12 2011 Petr Sabata <psabata@redhat.com> - 1.4005-1
- 1.4005 bump

* Fri Mar 11 2011 Petr Sabata <psabata@redhat.com> - 1.4004-1
- 1.4004 bump

* Thu Mar 10 2011 Petr Pisar <ppisar@redhat.com> - 1.4003-1
- 1.4003 bump

* Tue Mar 08 2011 Petr Pisar <ppisar@redhat.com> - 1.4000-1
- 1.4000 bump

* Fri Mar 04 2011 Petr Pisar <ppisar@redhat.com> - 1.3001-1
- 1.3001 bump

* Thu Mar 03 2011 Petr Pisar <ppisar@redhat.com> - 1.3000-1
- 1.3000 bump
- Clean up spec file
- Require modules needed by cpanm
- Merge cpanminus into main package as cpanminus required main package and
  main package did not contain any code (i.e. was useless).

* Thu Feb 17 2011 Petr Sabata <psabata@redhat.com> - 1.2001-1
- 1.2001 bump

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1008-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 27 2011 Petr Pisar <ppisar@redhat.com> - 1.1008-1
- 1.1008 bump

* Mon Jan 24 2011 Petr Pisar <ppisar@redhat.com> - 1.1007-1
- 1.1007 bump

* Mon Jan  3 2011 Petr Sabata <psabata@redhat.com> - 1.1006-1
- 1.1006 bump

* Thu Dec  2 2010 Petr Sabata <psabata@redhat.com> - 1.1004-1
- 1.1004 bump

* Fri Nov 19 2010 Petr Pisar <ppisar@redhat.com> - 1.1002-1
- 1.1002 bump

* Mon Sep 27 2010 Petr Pisar <ppisar@redhat.com> - 1.0015-1
- 1.0015 bump

* Thu Sep 23 2010 Petr Pisar <ppisar@redhat.com> - 1.0014-1
- 1.0014 bump

* Tue Sep 14 2010 Petr Pisar <ppisar@redhat.com> - 1.0013-1
- 1.0013 bump
- Correct description spelling

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.9935-3
- Mass rebuild with perl-5.12.0

* Tue Mar 16 2010 Marcela Mašláňová <mmaslano@redhat.com> 0.9935-2
- filter unwanted requires

* Tue Mar 16 2010 Marcela Mašláňová <mmaslano@redhat.com> 0.9935-1
- update

* Tue Mar 16 2010 Marcela Mašláňová <mmaslano@redhat.com> 0.9923-1
- update
- create sub-package

* Tue Mar  2 2010 Marcela Mašláňová <mmaslano@redhat.com> 0.9911-1
- new version & fix description

* Tue Feb 23 2010 Marcela Mašláňová <mmaslano@redhat.com> 0.09-1
- Specfile autogenerated by cpanspec 1.78.
