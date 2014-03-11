%define DisableOffensiveFortunes 1
%define CookieDir %{_datadir}/games/fortune

Summary: A program which will display a fortune
Name: fortune-mod
Version: 1.99.1
Release: 16%{?dist}
URL: http://www.redellipse.net/code/fortune
License: BSD
Group: Amusements/Games
Source: http://www.redellipse.net/code/downloads/fortune-mod-1.99.1.tar.gz
Source1: kernelnewbies-fortunes.tar.gz
Source2: bofh-excuses.tar.bz2
Source3: http://www.aboleo.net/software/misc/fortune-tao.tar.gz
Source4: http://www.splitbrain.org/Fortunes/hitchhiker/fortune-hitchhiker.tgz
Source5: http://www.dibona.com/opensources/osfortune.tar.gz
Source6: http://humorix.org/downloads/humorixfortunes-1.4.tar.gz
Patch0: fortune-mod-offense.patch
Patch1: fortune-mod-1.99-remove-offensive-option.patch
Patch2: fortune-mod-cflags.patch
Patch3: fortune-mod-1.99-move-offensive.patch
BuildRequires: recode-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Fortune-mod contains the ever-popular fortune program, which will
display quotes or witticisms. Fun-loving system administrators can add
fortune to users' .login files, so that the users get their dose of
wisdom each time they log in.

%prep
%setup -q

# disable offensive fortunes completely
%if %{DisableOffensiveFortunes}
%patch0 -p1 -b .disable-offensive1
%patch1 -p0 -b .remove-offensive-option
%endif

# use CFLAGS from rpmbuld
%patch2 -p1 -b .cflags
# move possibly offensive fortunes into the offensive directory
%patch3 -p0 -b .move-offensive

%build
make COOKIEDIR=%{CookieDir} \
	FORTDIR=%{_bindir} BINDIR=%{_sbindir}

%install
rm -rf $RPM_BUILD_ROOT

make    COOKIEDIR=%{CookieDir} fortune/fortune.man
make	FORTDIR=$RPM_BUILD_ROOT/%{_bindir} \
	COOKIEDIR=$RPM_BUILD_ROOT%{CookieDir} \
	LOCALDIR=$RPM_BUILD_ROOT%{CookieDir} \
	BINDIR=$RPM_BUILD_ROOT/%{_sbindir} \
	BINMANDIR=$RPM_BUILD_ROOT/%{_mandir}/man1 \
	FORTMANDIR=$RPM_BUILD_ROOT/%{_mandir}/man6 \
	install

tar zxvf %{SOURCE1} -C $RPM_BUILD_ROOT%{CookieDir}
%if %{DisableOffensiveFortunes}
rm -f $RPM_BUILD_ROOT%{CookieDir}/men-women*
%endif

# this isn't debian
rm -f $RPM_BUILD_ROOT%{CookieDir}/debian*
rm -f $RPM_BUILD_ROOT%{CookieDir}/off/debian*

# Using bzcat for portability because tar keeps changing the switch
bzcat %{SOURCE2} | tar xvf - -C $RPM_BUILD_ROOT%{CookieDir}

# Non-standard source files, need to move things around
tar zxvf %{SOURCE3} -C $RPM_BUILD_ROOT%{CookieDir}/ fortune-tao/tao*
mv $RPM_BUILD_ROOT%{CookieDir}/fortune-tao/* $RPM_BUILD_ROOT%{CookieDir}/
rmdir $RPM_BUILD_ROOT%{CookieDir}/fortune-tao

tar zxvf %{SOURCE4} -C $RPM_BUILD_ROOT%{CookieDir}/ fortune-hitchhiker/hitch*
mv $RPM_BUILD_ROOT%{CookieDir}/fortune-hitchhiker/* $RPM_BUILD_ROOT%{CookieDir}/
rmdir $RPM_BUILD_ROOT%{CookieDir}/fortune-hitchhiker

tar zxvf %{SOURCE5} -C $RPM_BUILD_ROOT%{CookieDir}/
chmod 644 $RPM_BUILD_ROOT%{CookieDir}/osfortune*

tar zxvf %{SOURCE6} -C $RPM_BUILD_ROOT%{CookieDir}/ humorixfortunes-1.4/*
mv $RPM_BUILD_ROOT%{CookieDir}/humorixfortunes-1.4/* $RPM_BUILD_ROOT%{CookieDir}/
rmdir $RPM_BUILD_ROOT%{CookieDir}/humorixfortunes-1.4

# Recreate random access files for the added fortune files.
for i in \
    kernelnewbies bofh-excuses tao hitchhiker \
    osfortune humorix-misc humorix-stories \
; do util/strfile $RPM_BUILD_ROOT%{CookieDir}/$i ; done


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README ChangeLog TODO
%{_bindir}/fortune
%{_sbindir}/strfile
%{_sbindir}/unstr
%{CookieDir}
%{_mandir}/man*/*

%changelog
* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 1.99.1-16
- 为 Magic 3.0 重建

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.99.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.99.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.99.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.99.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.99.1-11
- Autorebuild for GCC 4.3

* Fri Jan 11 2008 Jeff Sheltren <jeff@osuosl.org> 1.99.1-10
- Rebuild for F9

* Tue Jun  5 2007 Jeff Sheltren <sheltren@cs.ucsb.edu> 1.99.1-9
- Rebuild

* Mon Apr  9 2007 Jeff Sheltren <sheltren@cs.ucsb.edu> 1.99.1-8
- Rebuild for Fedora 7

* Sat Sep  9 2006 Jeff Sheltren <sheltren@cs.ucsb.edu> 1.99.1-7
- bump release for buildsystem

* Sat Sep  9 2006 Jeff Sheltren <sheltren@cs.ucsb.edu> 1.99.1-6
- Rebuild for FE6

* Mon Feb 20 2006 Jeff Sheltren <sheltren@cs.ucsb.edu> 1.99.1-5
- Rebuild for Fedora Extras 5

* Tue Oct  4 2005 Jeff Sheltren <sheltren@cs.ucsb.edu> 1.99.1-4
- Move fortunes into _datadir/games/fortune

* Mon Mar 21 2005 Jeff Sheltren <sheltren@cs.ucsb.edu> 1.99.1-3
- Bump version to 3 for fc4 package

* Mon Mar 14 2005 Jeff Sheltren <sheltren@cs.ucsb.edu> 1.99.1-2
- Add patch for moving fortunes into offensive directory

* Sun Mar 13 2005 Jeff Sheltren <sheltren@cs.ucsb.edu> 1.99.1-1
- Update to newer source (see URL)
- Update patches as necessary, separate cflags patch as it was only applied if applying offensive patches
- New source has recode-devel buildreq
- Remove debian fortunes which are included in new source

* Sat Nov 13 2004 Michael Schwendt <mschwendt[AT]users.sf.net> 1.0-25
- Recreate .dat files at build-time to fix x86_64 fedora.us bug #2279.
- Use %%CookieDir everywhere.
- Bump release to 25, drop Epoch.

* Sun Jun 08 2003 Michel Alexandre Salim <salimma[AT]users.sourceforge.net> 1.0-24.fdr.4
- Added Humorix fortunes
- Used $RPM_BUILD_ROOT

* Sun May 04 2003 Michel Alexandre Salim <salimma[AT]users.sourceforge.net> 1.0-24.fdr.3
- Added Tao Te Ching (fortune-tao), O'Reilly (osfortune) and H2G2 (fortune-hitchhiker) cookies
- Fixed BuildRoot
- Added Epoch
- Reverted to .tar.gz for main source, .tar.bz2 not available upstream

* Fri May 02 2003 Michel Alexandre Salim <salimma[AT]users.sourceforge.net> 1.0-24.fdr.2
- Modified installation paths to conform with Red Hat-packaged games, i.e. binaries in /usr and data files under /usr/games

* Fri May 02 2003 Michel Alexandre Salim <salimma[AT]users.sourceforge.net> 1.0-24.fdr.1
- Converted from fortune-mod-1.0-24 from RH8.0
- Updated package naming, added URL

* Thu Aug 22 2002 Mike A. Harris <mharris@redhat.com> 1.0-24
- Removed -o option from fortune, the manpage and --help message, as
  we do not provide or support the offensive fortunes for obvious
  reasons.  (#54713)
