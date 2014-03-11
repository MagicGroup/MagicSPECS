%define pcscver 1.3.0
%define pcsclib libpcsclite.so.1
%ifarch x86_64 ppc64 ia64 sparc64 s390x
%define mark64  ()(64bit)
%endif

Name:           pcsc-perl
Version:        1.4.12
Release:        6%{?dist}
Summary:        Perl interface to the PC/SC smart card library

Group:          Development/Libraries
License:        GPLv2+
URL:            http://ludovic.rousseau.free.fr/softwares/pcsc-perl/
Source0:        http://ludovic.rousseau.free.fr/softwares/pcsc-perl/%{name}-%{version}.tar.bz2
Source1:        http://ludovic.rousseau.free.fr/softwares/pcsc-perl/%{name}-%{version}.tar.bz2.asc
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  pcsc-lite-devel >= %{pcscver}
Requires:       %{pcsclib}%{?mark64}
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Provides:       perl-pcsc = %{version}-%{release}

%description
This library allows to communicate with a smart card using PC/SC
interface (pcsc-lite) from a Perl script.

%prep
%setup -q
chmod 644 examples/* # avoid dependencies
f=Changelog ; iconv -f iso-8859-1 -t utf-8 $f > $f.utf8 ; mv $f.utf8 $f


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS" DEFINE=-Wall
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check
# tests need configured readers etc
if ! grep -qF 'dlopen("%{pcsclib}"' PCSCperl.h ; then # sanity check
    echo "ERROR: pcsc lib name mismatch in PCSCperl.h/dependencies" ; exit 1
fi


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changelog LICENCE README examples/
%{perl_vendorarch}/auto/Chipcard/
%{perl_vendorarch}/Chipcard/
%{_mandir}/man3/Chipcard::PCSC*.3*


%changelog
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 1.4.12-4
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.4.12-2
- Perl mass rebuild

* Tue Jun  7 2011 Tomas Mraz <tmraz@redhat.com> - 1.4.12-1
- New upstream version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep  7 2010 Tomas Mraz <tmraz@redhat.com> - 1.4.10-1
- New upstream version

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.4.8-3
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.4.8-2
- rebuild against perl 5.10.1

* Fri Sep 25 2009 Tomas Mraz <tmraz@redhat.com> - 1.4.8-1
- New upstream version

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 27 2008 Ville Skyttä <ville.skytta at iki.fi> - 1.4.7-1
- 1.4.7.

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.4.6-4
- Rebuild for new perl

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.4.6-3
- Autorebuild for GCC 4.3

* Tue Aug  7 2007 Ville Skyttä <ville.skytta at iki.fi> - 1.4.6-2
- Apply #defines patch only when building with pcsc-lite < 1.4.0.
- License: GPLv2+

* Tue Apr 17 2007 Ville Skyttä <ville.skytta at iki.fi> - 1.4.6-1
- 1.4.6 + PCSCperl.h #defines fixes.
- BuildRequire perl(ExtUtils::MakeMaker).

* Sun Dec 24 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.4.4-3
- Eliminate file based dependencies.

* Thu Nov  2 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.4.4-2
- Rebuild with pcsc-lite 1.3.2 for extended APDU support.

* Tue Aug 15 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.4.4-1
- 1.4.4.

* Wed May 17 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.4.3-1
- 1.4.3.

* Mon Mar  6 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.4.1-1
- 1.4.1.
- Don't hardcode required pcsc-lite-libs version, use shared lib file instead.
- Convert docs to UTF-8.

* Wed Feb 15 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.3.1-8
- Rebuild, cosmetics.

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 1.3.1-7
- rebuild on all arches

* Thu May 19 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.3.1-6
- Provide perl-pcsc, fixate required pcsc-lite version to 1.2.0.

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.3.1-5
- rebuilt

* Fri Jan  7 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:1.3.1-4
- Honor $RPM_OPT_FLAGS, remove (some) extra include dirs from build (#1281).
- Improve summary and description.

* Wed May 12 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.3.1-0.fdr.3
- BuildRequire perl >= 1:5.6.1 for vendor install dir support.
- Use pure_install to avoid perllocal.pod workarounds.

* Sun Apr 25 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.3.1-0.fdr.2
- Require perl(:MODULE_COMPAT_*).

* Fri Apr  2 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.3.1-0.fdr.1
- Update to 1.3.1.

* Sun Feb  8 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.3.0-0.fdr.2
- Reduce directory ownership bloat.

* Wed Dec 17 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.3.0-0.fdr.1
- Update to 1.3.0.

* Sun Sep 14 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.2.2-0.fdr.4
- More spec cleanups.

* Wed Aug 27 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.2.2-0.fdr.3
- Spec cleanups, install into vendor dirs.

* Fri Jul  4 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.2.2-0.fdr.2
- Fix dir ownerships, non-root strip during build.

* Thu May 29 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.2.2-0.fdr.1
- Update to 1.2.2.
- Drop patch and hacks, already applied/fixed upstream.

* Sun May 25 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.2.1-0.fdr.1
- Update to 1.2.1.
- Fix build and runtime dependencies.

* Thu May 22 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.2.0-0.fdr.1
- First build.
