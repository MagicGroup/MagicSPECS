Name:           perl-bioperl-run
Version:        1.6.1
Release:        26%{?dist}
Summary:        Modules to provide a Perl interface to various bioinformatics applications
Summary(zh_CN.UTF-8): 各种生物信息学应用的 Perl 接口模块

Group:          Development/Libraries
Group(zh_CN.UTF-8): 开发/库
License:        GPL+ or Artistic
URL:            http://bioperl.org
Source0:        http://bioperl.org/DIST/BioPerl-run-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(Bio::Root::Version) >= 1.5.9
BuildRequires:  perl(Algorithm::Diff) >= 1
BuildRequires:  perl(XML::Parser::PerlSAX)
BuildRequires:  perl(IPC::Run)
BuildRequires:  perl(HTML::Parser)
BuildRequires:  perl(Module::Build)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Bioperl-run contain modules that provide a Perl interface to various
bioinformatics applications. This allows various applications to be
used with common Bioperl objects.

%description -l zh_CN.UTF-8
各种生物信息学应用的 Perl 接口模块。

%prep
# note that archive and tarball version numbers don't quite match in this release
%setup -q -n BioPerl-run-1.6.0

# remove all execute bits from the doc stuff
chmod -x INSTALL INSTALL.PROGRAMS

%build
%{__perl} Build.PL --installdirs vendor << EOF
a
EOF

./Build

%install
rm -rf $RPM_BUILD_ROOT
perl Build pure_install --destdir=$RPM_BUILD_ROOT

# remove some spurious files
find $RPM_BUILD_ROOT -type f -a \( -name .packlist \
  -o \( -name '*.bs' -a -empty \) \) -exec rm -f {} ';'
# remove errant execute bit from the .pm's
find $RPM_BUILD_ROOT -type f -name '*.pm' -exec chmod -x {} 2>/dev/null ';'
# correct all binaries in /usr/bin to be 0755
find $RPM_BUILD_ROOT/%{_bindir} -type f -name '*.pl' -exec chmod 0755 {} 2>/dev/null ';'
magic_rpm_clean.sh

%check
%{?_with_check:./Build test || :}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
## don't distribute "doc" "scripts" subdirectories, they don't contain docs
%doc AUTHORS Changes INSTALL INSTALL.PROGRAMS README
%{perl_vendorlib}/*
%{_mandir}/man3/*.3*    
%{_bindir}/*
%{_mandir}/man1/*.1*

%changelog
* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.6.1-26
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.6.1-25
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.6.1-24
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.6.1-23
- 为 Magic 3.0 重建

* Mon Jun 16 2014 Liu Di <liudidi@gmail.com> - 1.6.1-22
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.6.1-21
- 为 Magic 3.0 重建

* Sun Jun 15 2014 Liu Di <liudidi@gmail.com> - 1.6.1-20
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.6.1-19
- 为 Magic 3.0 重建

* Sat Jun 14 2014 Liu Di <liudidi@gmail.com> - 1.6.1-18
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.6.1-17
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.6.1-16
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.6.1-15
- 为 Magic 3.0 重建

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.6.1-14
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 1.6.1-13
- 为 Magic 3.0 重建

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 04 2012 Petr Pisar <ppisar@redhat.com> - 1.6.1-11
- Perl 5.16 rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.6.1-9
- Perl mass rebuild

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.6.1-8
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.6.1-7
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.6.1-5
- 661697 rebuild for fixing problems with vendorach/lib

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.6.1-4
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.6.1-3
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Feb 28 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.6.1-1
- Update to final 1.6.1 release

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.9-0.3.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.5.9-0.2.2
- Update to release candidate 2 for 1.6.0 should fix file conflicts 
  with ConfigData (#484495)

* Tue Feb  3 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.5.9-0.1.1
- Update to release candidate 1 for 1.6.0 
- Remove examples subdirectory, no longer distributed
- Deprecated modules no longer need removing
- Add BR: perl(IPC::Run)

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.5.2_100-3
- rebuild for new perl

* Tue Apr 18 2007 Alex Lancaster <alexl@users.sourceforge.net> 1.5.2_100-2
- Remove deprecated modules that depend on non-existent
  Bio::Root::AccessorMaker

* Tue Apr 17 2007 Alex Lancaster <alexl@users.sourceforge.net> 1.5.2_100-1
- Initial Fedora package.
