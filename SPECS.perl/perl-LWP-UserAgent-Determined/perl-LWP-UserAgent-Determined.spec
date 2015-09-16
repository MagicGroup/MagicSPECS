Summary: A virtual browser that retries errors
Name: perl-LWP-UserAgent-Determined
Version:	1.07
Release:	1%{?dist}
License: GPL+ or Artistic
Group: Development/Libraries
URL: http://search.cpan.org/dist/%{pkg_name}/
Source0:        http://search.cpan.org/CPAN/authors/id/A/AL/ALEXMV/LWP-UserAgent-Determined-%{version}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch: noarch
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(LWP::UserAgent)
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))


%description
This class works just like LWP::UserAgent (and is based on it, by being a
subclass of it), except that when you use it to get a web page but run into
a possibly-temporary error (like a DNS lookup timeout), it'll wait a few
seconds and retry a few times.


%prep
%setup -q -n LWP-UserAgent-Determined-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
chmod -R u+w %{buildroot}/*


#%check
#


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc ChangeLog README
%dir %{perl_vendorlib}/LWP
%dir %{perl_vendorlib}/LWP/UserAgent
%{perl_vendorlib}/LWP/UserAgent/Determined.pm
%{_mandir}/man3/LWP::UserAgent::Determined.3pm*


%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.07-1
- 更新到 1.07

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.05-6
- 为 Magic 3.0 重建

* Mon Dec 10 2012 Liu Di <liudidi@gmail.com> - 1.05-5
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.05-4
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 1.05-2
- Perl mass rebuild

* Wed May 04 2011 Robert Rati <rrati@redhat> - 1.05-1
- Update to upstream version 1.05

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 08 2010 Lubomir Rintel <lkundrak@v3.sk> - 1.03-8
- We install into vendorlib, need proper perl version require

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.03-7
- Mass rebuild with perl-5.12.0

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.03-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar 11 2008 Robert Rati <rrati@redhat> - 1.03-3
- Package now owns all files/directories from LWP on down to
  conform with packaging standards

* Fri Mar  7 2008 Robert Rati <rrati@redhat> - 1.03-2
- Removed the %check tag because the tests attempt to access
  the internet

* Fri Mar  7 2008 Robert Rati <rrati@redhat> - 1.03-1
- Initial release
