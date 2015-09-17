%define		perl_vendorarch	%(eval "`perl -V:installvendorarch`"; echo $installvendorarch)

Summary:	Modular text mode IRC client with Perl scripting
Name:		irssi
Version:	0.8.16
Release:	2%{?dist}

License:	GPLv2+
Group:		Applications/Communications
URL:		http://irssi.org/
Source0:	http://irssi.org/files/irssi-%{version}.tar.bz2
Source1:	irssi-config.h
Patch0:		irssi-0.8.15-no-static-unload.patch
Patch1:		irssi-0.8.15-man-fix.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	ncurses-devel openssl-devel zlib-devel
BuildRequires:	pkgconfig glib2-devel perl-devel perl(ExtUtils::Embed)
BuildRequires:	autoconf automake libtool
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%package devel
Summary:	Development package for irssi
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description
Irssi is a modular IRC client with Perl scripting. Only text-mode
frontend is currently supported. The GTK/GNOME frontend is no longer
being maintained.

%description devel
This package contains headers needed to develop irssi plugins.

Irssi is a modular IRC client with Perl scripting. Only text-mode
frontend is currently supported. The GTK/GNOME frontend is no longer
being maintained.


%prep
%setup -q
%patch0 -p1 -b .no-static-unload
%patch1 -p1 -b .man-fix

%build
autoreconf -i
%configure --enable-ipv6 --with-textui	\
	--with-proxy			\
	--with-bot			\
	--with-perl=yes			\
	--with-perl-lib=vendor 

make %{_smp_mflags} CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
mv irssi-config.h irssi-config-$(getconf LONG_BIT).h
cp -p %{SOURCE1} irssi-config.h


%install
rm -rf $RPM_BUILD_ROOT
%makeinstall PERL_INSTALL_ROOT=$RPM_BUILD_ROOT INSTALL="%{__install} -p"
install -p irssi-config-$(getconf LONG_BIT).h $RPM_BUILD_ROOT%{_includedir}/%{name}/irssi-config-$(getconf LONG_BIT).h

rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/modules/lib*.*a
rm -Rf $RPM_BUILD_ROOT/%{_docdir}/%{name}
find $RPM_BUILD_ROOT%{perl_vendorarch} -type f -a -name '*.bs' -a -empty -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{perl_vendorarch} -type f -a -name .packlist -exec rm {} ';'
chmod -R u+w $RPM_BUILD_ROOT%{perl_vendorarch}



%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc docs/*.txt docs/*.html AUTHORS COPYING NEWS README TODO
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_bindir}/%{name}
%{_bindir}/botti
%{_datadir}/%{name}
%{_libdir}/%{name}
%{_mandir}/man1/%{name}.1*
%{perl_vendorarch}/Irssi*
%{perl_vendorarch}/auto/Irssi


%files devel
%defattr(-,root,root,-)
%{_includedir}/irssi/


%changelog
* Thu Sep 17 2015 Liu Di <liudidi@gmail.com> - 0.8.16-2
- 为 Magic 3.0 重建

* Tue Jun 10 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 0.8.16-1
- New version
  Resolves: rhbz#1107342
- Dropped format-security patch (not needed)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.16-0.4.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Dec  4 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 0.8.16-0.3.rc1
- Fixed change log

* Wed Dec  4 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 0.8.16-0.2.rc1
- Fixed compilation with -Werror=format-security
  Resolves: rhbz#1037139

* Mon Sep 16 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 0.8.16-0.1.rc1
- New version
- Dropped init-resize-crash-fix (upstreamed)
- Fixed bogus date in changelog (best effort)
- Disabled unloading static modules (by no-static-unload patch)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.15-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.8.15-14
- Perl 5.18 rebuild

* Mon Mar 25 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 0.8.15-13
- Added support for aarch64
  Resolves: rhbz#925598

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.15-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Aug  3 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 0.8.15-11
- Removed usage parameter from the man page (popt leftover)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.15-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 07 2012 Petr Pisar <ppisar@redhat.com> - 0.8.15-9
- Perl 5.16 rebuild

* Fri Feb 24 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 0.8.15-8
- Fixed crash that can occur if term is resized during irssi init
  (init-resize-crash-fix patch)
  Resolves: rhbz#796457

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.8.15-6
- Perl mass rebuild

* Thu Jun 09 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.8.15-5
- Perl 5.14 mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.8.15-3
- Mass rebuild with perl-5.12.0

* Mon May 31 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 0.8.15-2
- Rebuilt with -fno-strict-aliasing

* Tue Apr 13 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 0.8.15-1
- Update to new version: irssi-0.8.15

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.8.14-4
- rebuild against perl 5.10.1

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.8.14-3
- rebuilt with new openssl

* Tue Aug 11 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.8.14-2
- Use bzipped upstream tarball.

* Mon Aug  3 2009 Marek Mahut <mmahut@fedoraproject.org> - 0.8.14-1
- Upstream release 0.8.14

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 23 2009 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 0.8.13-2
- Resolve CVE-2009-1959

* Fri May  1 2009 Marek Mahut <mmahut@fedoraproject.org> - 0.8.13-1
- Upstream release

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.12-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 0.8.12-12
- rebuild with new openssl

* Fri Aug 29 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 0.8.12-11
- Don't include any C header files in main package.

* Fri Mar  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.8.12-10
- BR: perl(ExtUtils::Embed)

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.8.12-9
- Rebuild for new perl

* Sat Mar  1 2008 Marek Mahut <mmahut@fedoraproject.org> - 0.8.12-8
- Fix for multiarch conflict (BZ#341591)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.8.12-5
- Autorebuild for GCC 4.3

* Sun Nov 11 2007 Marek Mahut <mmahut fedoraproject.org> - 0.8.12-3
- Enabling perl build-in support as per request in BZ#375121

* Mon Oct 08 2007 Marek Mahut <mmahut fedoraproject.org> - 0.8.12-1
- New release
- Fixes bug from BZ#239511, dropping patch

* Sun Aug 19 2007 Marek Mahut <mmahut fedoraproject.org> - 0.8.11-5
- Fixing properly irssi-support-meta-cursor-xterm.patch

* Thu Aug 16 2007 Marek Mahut <mmahut redhat.com> - 0.8.11-4
- Added irssi-support-meta-cursor-xterm.patch (BZ#239511)

* Thu Aug 16 2007 Marek Mahut <mmahut redhat.com> - 0.8.11-2
- Updating license tag
- Rebuild for 0.8.11

* Wed May  2 2007 Dams <anvil[AT]livna.org> - 0.8.11-1
- Updated to 0.8.11
- Dropped patch0

* Sat Apr 21 2007 Dams <anvil[AT]livna.org> - 0.8.10-7.a
- Release bump

* Sun Sep 17 2006 Dams <anvil[AT]livna.org> - 0.8.10-6.a
- Bumped release 

* Sun Sep 17 2006 Dams <anvil[AT]livna.org> - 0.8.10-5.a
- Updated to 0.8.10a
- Fixed tarball name..
- Updated Patch0 still from Saleem

* Wed Mar 15 2006 Dams <anvil[AT]livna.org> - 0.8.10-4
- Added patch from Saleem Abdulrasool to fix invalid pointer.

* Sat Jan 28 2006 Dams <anvil[AT]livna.org> - 0.8.10-3
- Fixed changelog -_-

* Sat Jan 28 2006 Dams <anvil[AT]livna.org> - 0.8.10-2
- Disabled gc support

* Sun Dec 11 2005 Dams <anvil[AT]livna.org> - 0.8.10-1
- Updated to final 0.8.10

* Wed Dec  7 2005 Dams <anvil[AT]livna.org> - 0.8.10-0.2.rc8
- Updated to rc8

* Tue Nov 15 2005 Dams <anvil[AT]livna.org> - 0.8.10-0.1.rc7
- Dropped patch 2 (seems applied upstream) and 3 (no longer needed)
- Removed conditionnal build against glib1 parts

* Sun Nov 13 2005 Luke Macken <lmacken@redhat.com> 0.8.9-8
- Rebuild against new openssl

* Mon Apr 11 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 0.8.9-7
- Two patches to fix build for GCC4 and new Perl with config.h.

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Fri Dec 24 2004 Michael Schwendt <mschwendt[AT]users.sf.net> 0:0.8.9-5
- Reduce Perl dir ownership and add MODULE_COMPAT dependency.

* Fri Apr  2 2004 Dams <anvil[AT]livna.org> 0:0.8.9-0.fdr.4
- Rebuilt to use new perl to prevent random segmentation fault at load
  time

* Fri Feb  6 2004 Dams <anvil[AT]livna.org> 0:0.8.9-0.fdr.3
- Patch from Michael Schwendt to fix convert-replace-trigger script
  (bug #1120 comment #3)

* Sat Dec 20 2003 Dams <anvil[AT]livna.org> 0:0.8.9-0.fdr.2
- Fixed changelog typo
- Added trigger.pl as replace.pl wont be maintained anymore
- Updated replace.pl to 0.1.4 version
- Added replace.pl URL in Source tag
- Removed .packlist files
- Added as doc a script to convert pref from replace.pl to trigger.pl

* Thu Dec 11 2003 Dams <anvil[AT]livna.org> 0:0.8.9-0.fdr.1
- Updated to 0.8.9

* Mon Nov 24 2003 Dams <anvil[AT]livna.org> 0:0.8.8-0.fdr.1
- Updated to 0.8.8
- Enabled gc

* Sun Sep 14 2003 Dams <anvil[AT]livna.org> 0:0.8.6-0.fdr.13
- Rebuild

* Sun Sep 14 2003 Michael Schwendt <mschwendt[AT]users.sf.net> 0:0.8.6-0.fdr.12
- apply openssl patch only if openssl-devel supports pkgconfig

* Thu Sep 11 2003 Dams <anvil[AT]livna.org> 0:0.8.6-0.fdr.11
- Installing replace.pl in good directory

* Thu Sep 11 2003 Dams <anvil[AT]livna.org> 0:0.8.6-0.fdr.10
- Rebuild

* Thu Sep 11 2003 Dams <anvil[AT]livna.org> 0:0.8.6-0.fdr.9
- Using vendor perl directories

* Thu Sep 11 2003 Dams <anvil[AT]livna.org> 0:0.8.6-0.fdr.8
- Added missing unowned directories
- Added an additionnal useful perl script (replace.pl)

* Tue Aug  5 2003 Dams <anvil[AT]livna.org> 0:0.8.6-0.fdr.7
- Added zlib-devel buildrequires

* Sat Jul 12 2003 Dams <anvil[AT]livna.org> 0:0.8.6-0.fdr.6
- Applied Patches from Ville Skyttä (bug #277 comment #11 and
  comment #12)

* Mon Jun 23 2003 Dams <anvil[AT]livna.org> 0:0.8.6-0.fdr.5
- Modified BuildRequires for ssl

* Wed Jun 11 2003 Dams <anvil[AT]livna.org> 0:0.8.6-0.fdr.4
- Added another dir entry

* Sun Jun  8 2003 Dams <anvil[AT]livna.org> 0:0.8.6-0.fdr.3
- Added some dir entry in file section

* Tue May 20 2003 Dams <anvil[AT]livna.org> 0:0.8.6-0.fdr.2
- Exclude modules ".a" files
- Include more files as doc

* Sat May 10 2003 Dams <anvil[AT]livna.org>
- Initial build.
