Name:         perl-NOCpulse-Utils
Version:      1.14.11
Release:      12%{?dist}
Summary:      NOCpulse utility packages
URL:          https://fedorahosted.org/spacewalk
Source0:      https://fedorahosted.org/releases/s/p/spacewalk/%{name}-%{version}.tar.gz
BuildArch:    noarch
Group:        Development/Libraries
License:      GPLv2
Buildroot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:     perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
NOCpulse provides application, network, systems and transaction monitoring,
coupled with a comprehensive reporting system including availability,
historical and trending reports in an easy-to-use browser interface.

This package provides miscellaneous utility modules.

%prep
%setup -q

%build
# Nothing to build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{perl_vendorlib}/NOCpulse/Utils/test

install -m 444 Module.pm          $RPM_BUILD_ROOT%{perl_vendorlib}/NOCpulse/Module.pm 
#install -m 444 TestRunner.pm      $RPM_BUILD_ROOT%{perl_vendorlib}/NOCpulse/Utils/TestRunner.pm
install -m 444 Error.pm           $RPM_BUILD_ROOT%{perl_vendorlib}/NOCpulse/Utils/Error.pm
#install -m 755 -D runtest.pl      $RPM_BUILD_ROOT/%{_bindir}/runtest.pl
install -m 444 XML.pm          $RPM_BUILD_ROOT%{perl_vendorlib}/NOCpulse/Utils/XML.pm
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man3/
/usr/bin/pod2man $RPM_BUILD_ROOT%{perl_vendorlib}/NOCpulse/Module.pm |gzip > $RPM_BUILD_ROOT%{_mandir}/man3/NOCpulse::Module.3pm.gz

%files 
%defattr(-,root,root)
%dir %{perl_vendorlib}/NOCpulse
%{perl_vendorlib}/NOCpulse/*
%{_mandir}/man3/*

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.14.11-12
- 为 Magic 3.0 重建

* Mon Jan 30 2012 Liu Di <liudidi@gmail.com> - 1.14.11-11
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14.11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.14.11-9
- Perl mass rebuild

* Fri Jun 10 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.14.11-8
- Perl 5.14 mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.14.11-6
- 661697 rebuild for fixing problems with vendorach/lib

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.14.11-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.14.11-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan  7 2009 Milan Zazrivec 1.14.11-1
- include documentation fixes

* Wed Dec  3 2008 Miroslav Suchý <msuchy@redhat.com> 1.14.10-1
- changed Source0 to point to fedorahosted.org

* Mon Oct 20 2008 Miroslav Suchý <msuchy@redhat.com> 1.14.9-1
- 467441 - fix namespace

* Mon Oct 20 2008 Miroslav Suchy <msuchy@redhat.com> 1.14.8-1
- 467443 - fix typo in module name

* Tue Oct 14 2008 Miroslav Suchy <msuchy@redhat.com> 1.14.7-1
- remove nocpulse-common from requires

* Thu Aug 20 2008 Miroslav Suchy <msuchy@redhat.com> 1.14.5-1
- edit spec to comply with Fedora guidelines

* Thu Jun 19 2008 Miroslav Suchy <msuchy@redhat.com>
- migrating nocpulse home dir (BZ 202614)

* Wed Jun  4 2008 Milan Zazrivec <mzazrivec@redhat.com> 1.14.2-9
- fixed file permissions

* Tue May 27 2008 Jan Pazdziora 1.14.2-8
- fixed bugzilla 438770
u rebuild in dist.cvs

