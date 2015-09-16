Name:           perl-CSS-DOM
Version:	0.15
Release:	1%{?dist}
Summary:        Document Object Model for Cascading Style Sheets

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/CSS-DOM/
Source0:        http://www.cpan.org/authors/id/S/SP/SPROUT/CSS-DOM-%{version}.tar.gz
# to avoid false "perl()" and "perl(#)" dependencies with rpmbuild < 4.9.0-rc1
Patch0:         %{name}-0.14-rpmdeps.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(Clone) >= 0.09
BuildRequires:  perl(Encode) >= 2.10
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
# Dependencies not detected automatically:
Requires:       perl(Clone) >= 0.09
Requires:       perl(Encode) >= 2.10
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This set of modules provides the CSS-specific interfaces described in
the W3C DOM recommendation.


%prep
%setup -q -n CSS-DOM-%{version}
%patch0 -p1


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;
%{_fixperms} $RPM_BUILD_ROOT/*


%check



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes LICENSE README
%{perl_vendorlib}/CSS/
%{_mandir}/man3/CSS::DOM*.3*


%changelog
* Sun Sep 13 2015 Liu Di <liudidi@gmail.com> - 0.15-1
- 更新到 0.15

* Fri Jun 13 2014 Liu Di <liudidi@gmail.com> - 0.14-11
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 0.14-10
- 为 Magic 3.0 重建

* Wed Dec 12 2012 Liu Di <liudidi@gmail.com> - 0.14-9
- 为 Magic 3.0 重建

* Sun Jan 29 2012 Liu Di <liudidi@gmail.com> - 0.14-8
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.14-6
- Perl mass rebuild

* Thu Feb 17 2011 Ville Skyttä <ville.skytta@iki.fi> - 0.14-5
- Patch to avoid incorrect automatic dependencies with rpmbuild < 4.9.0-rc1.
- Bring back BuildRoot lost in previous commit.
- Fix perl(Encode) build dependency.

* Tue Feb 15 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.14-4
- remove filter, which is now useless with RPM4.9

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.14-2
- 661697 rebuild for fixing problems with vendorach/lib

* Mon Dec 13 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.14-1
- Update to 0.14.

* Thu Aug 26 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.13-2
- Add explicit dependency on perl(Encode), not detected automatically.

* Tue Aug 24 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.13-1
- Update to 0.13.

* Fri Aug 20 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.11-1
- Update to 0.11.

* Fri Apr  2 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.10-1
- Update to 0.10.

* Sun Feb 21 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.09-1
- 0.09.

* Sun Jan 24 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.08-1
- First build.
