Name:  perl-Geo-IP
Version:	1.45
Release:	4%{?dist}
Summary: Efficient Perl bindings for the GeoIP location database       

Group: Development/Libraries
License: GPL+ or Artistic
URL: http://search.cpan.org/dist/Geo-IP/            
Source0:        http://search.cpan.org/CPAN/authors/id/M/MA/MAXMIND/Geo-IP-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: GeoIP-devel perl(ExtUtils::MakeMaker)
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This package contains Perl bindings for the GeoIP IP/hostname to
country/location/organization database.

This package requires Maxmind's GeoIP libraries but is often faster than other,
similar modules.  

%prep
%setup -q -n Geo-IP-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}
# Avoid uneeded dependencies in the docs.
find example/ -type f | xargs chmod -x

%check


%install
rm -rf %{buildroot}
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w %{buildroot}/*

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc Changes INSTALL example
%{perl_vendorarch}/Geo
%{perl_vendorarch}/auto/Geo
%{_mandir}/man3/Geo::IP*.3*
%{_mandir}/man3/Geo::Mirror.3*

%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 1.45-4
- 为 Magic 3.0 重建

* Mon Nov 02 2015 Liu Di <liudidi@gmail.com> - 1.45-3
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.45-2
- 为 Magic 3.0 重建

* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 1.45-1
- 更新到 1.45

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 1.38-11
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 1.38-10
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 1.38-9
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.38-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.38-7
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.38-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.38-5
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.38-4
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.38-3
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 15 2009 Michael Fleming <mfleming+rpm@thatfleminggent.com> 1.38-1
- New upstream update (fixes some segfaults and .au timezone breakage)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Aug 28 2008 Michael Fleming <mfleming+rpm@enlartenment.com> 1.36-1
- New upstream update

* Thu Aug 28 2008 Michael Fleming <mfleming+rpm@enlartenment.com> 1.34-1
- New upstream update
- Source0 updated (new upstream maintainer)

* Sun Apr 13 2008 Michael Fleming <mfleming+rpm@enlartenment.com> 1.31-1
- New upstream update

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.30-3
- Rebuild for new perl

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.30-2
- Autorebuild for GCC 4.3

* Mon Jan 28 2008 Michael Fleming <mfleming+rpm@enlartenment.com> 1.30-1
- Update to 1.30. This pulls in much of the PurePerl module for those
  using it (via third party repositories)

* Mon Sep 3 2007 Michael Fleming <mfleming+rpm@enlartenment.com> 1.28-4
- Fix %%patch invocation to help avoid a bogus interpreter issue
- First build for Extras

* Sun Aug 26 2007 Michael Fleming <mfleming+rpm@enlartenment.com> 1.28-3
- Actually apply the patch :-)
- Apply consistency in macro usage
- Remove explicit GeoIP dependency as it should be pulled in automagically
- Patch to example/netspeed to avoid bogus interpreter
- Update License to match current Fedora guidelines.

* Fri Jul 20 2007 Michael Fleming <mfleming+rpm@enlartenment.com> 1.28-2
- Patch out mysterious and ephemeral test failure

* Sun Jul 8 2007 Michael Fleming <mfleming+rpm@enlartenment.com> 1.28-1
- Update to 1.28

* Sun Jun 17 2007 Michael Fleming <mfleming+rpm@enlartenment.com> 1.27-4.mf
- New URLs
- Fix MakeMaker build requirement
- Include test suite check
- Add examples directory in documentation

* Sat Nov 4 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.27-3.mf
- Fix version tag to go with my conventions
- Bump for FC6

* Sun Feb 19 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.27-2
- Spin a version for Extras, removing the braindamage from my previous
  releases.

* Fri Sep 9 2005 mfleming@enlartenment.com - 1.27-1.fc4.mf
- 1.27

* Wed Aug 3 2005 mfleming@enlartenment.com - 1.26-2.fc4.mf
- Rebuilt against new geoip version

* Sun Jun 12 2005 mfleming@enlartenment.com - 1.26-1.fc4.mf
- Initial release

