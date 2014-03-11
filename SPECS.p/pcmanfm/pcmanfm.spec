# Upstream git:
# git://pcmanfm.git.sourceforge.net/gitroot/pcmanfm/pcmanfm

%global         usegit      0
%global         mainrel     1

%global         usegtk3     0
%if 0%{?fedora} >= 18
%global         usegtk3     1
%endif

%global         githash     07ddaf9cdeedc5f86a03b28b3d686aa82c59b38e
%global         shorthash   %(TMP=%githash ; echo ${TMP:0:10})
%global         gitdate    	Wed Aug 3 22:28:07 2011 +0200
%global         gitdate_num 20110803

%if 0%{?usegit} >= 1
%global         fedorarel   %{mainrel}.D%{gitdate_num}git%{shorthash}
%else
%global         fedorarel   %{mainrel}
%endif

%global	libfm_minver	1.1.0

Name:		pcmanfm
Version:	1.1.0
Release:	%{fedorarel}%{?dist}
Summary:	Extremly fast and lightweight file manager

Group:		User Interface/Desktops
License:	GPLv2+
URL:		http://pcmanfm.sourceforge.net/
%if 0%{?usegit} >= 1
Source0:        %{name}-%{version}-D%{gitdate_num}git%{shorthash}.tar.gz
%else
Source0:	http://downloads.sourceforge.net/pcmanfm/%{name}-%{version}.tar.gz
%endif
## Missing in the tarball, taken from git tree
#Source1:	pcmanfm.conf

BuildRequires:	libfm-gtk-devel >= %{libfm_minver}
BuildRequires:	menu-cache-devel

BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	intltool

# Still needed for removable media - still now really?
%if 0%{?fedora} < 16
Requires:	hal-storage-addon
%endif
# Write explicitly
Requires:	libfm >= %{libfm_minver}

%description
PCMan File Manager is an extremly fast and lightweight file manager 
which features tabbed browsing and user-friendly interface.

%prep
%setup -q
#install -cpm 644 %{SOURCE1} data/

#sh autogen.sh

# permission fix
chmod 0644 [A-Z]*

%build
# src/desktop.c
export LDFLAGS="-lm"
%configure \
%if %{usegtk3}
	--with-gtk=3
%endif

make -C po -j1 GMSGFMT="msgfmt --statistics"
make  %{?_smp_mflags} -k

%install
make install \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALL="install -p"

desktop-file-install \
	--delete-original \
	--dir $RPM_BUILD_ROOT%{_datadir}/applications \
	--remove-category 'Application' \
	--vendor 'fedora' \
	$RPM_BUILD_ROOT%{_datadir}/applications/%{name}*.desktop

%find_lang %{name}

%{_prefix}/lib/rpm/check-rpaths

%post
update-desktop-database &> /dev/null
exit 0

%postun
update-desktop-database &> /dev/null
exit 0

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc	AUTHORS
%doc	COPYING
%doc	README

%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%{_datadir}/%{name}/
%{_datadir}/applications/fedora-%{name}*.desktop
%config(noreplace) %{_sysconfdir}/xdg/%{name}/

%changelog
* Sun Nov  4 2012 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.1.0-1
- 1.1.0

* Wed Sep 27 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.0.1-1
- 1.0.1

* Wed Aug 15 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.0-1
- 1.0 release

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.10-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan  5 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.9.10-2
- F-17: rebuild against gcc47

* Fri Oct 28 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.9.10-1
- 0.9.10

* Sun Aug 28 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.9.9-8
- 0.9.9 release

* Sun Aug  7 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.9.9-7
- Update to the latest git

* Mon May 30 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.9.9-6
- Update to the latest git on "tab-rework" branch

* Sun Apr 24 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.9.9-5
- Update to the latest git

* Fri Apr 22 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.9.9-4
- Just kill hal dependency on F-16+

* Sat Apr 09 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.9.9-3
- Update to the latest git

* Sun Feb 20 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 0.9.9-2
- Update to the latest git

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9-1.git0f075cf5ba.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec  5 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- Update to the latest git

* Wed Oct 13 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.9.8-1
- Update to 0.9.8

* Sat May 29 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.9.7-1
- Update to 0.9.7

* Sun May  9 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.9.5-2
- Translation update from git

* Thu Apr 29 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.9.5-1
- Update to 0.9.5

* Sun Apr 18 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.9.4-1
- Update to 0.9.4
- Require hal-storage-addon
- Fix Source0 URL

* Mon Mar 22 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.9.3-1
- Update to 0.9.3
- Install %%name.png for compatibility on <= F-13

* Sun Feb 14 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.5.2-2
- Fix F-13 DSO linkage issue

* Fri Oct 30 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.5.2-1
- Update tp 0.5.2 (fixes sourceforge bug 2883172)

* Sat Jul 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.5.1-2
- F-12: Mass rebuild

* Thu Jun  4 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.5.1-1
- Update to 0.5.1
- Remove icon name fallback hack
- Still enable 2 patches

* Mon Apr  6 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.5-7
- Fix the issue when application cannot be lauched from desktop menu
  (sourceforge bug 2313286)

* Tue Feb 24 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.5-6
- F-11: Mass rebuild

* Fri Aug  8 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.5-5
- More fallback

* Wed Jul 30 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.5-4
- More fallback for gnome-icon-theme 2.23.X (F-10)

* Tue Jul 29 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.5-2
- F-10+: Use more generic icon name due to gnome-icon-theme 2.23.X change
  First try (need more fix)

* Thu Jul 17 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.5-1
- 0.5

* Wed Jul 16 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.4.6.2-1
- 0.4.6.2

* Tue Jul 15 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.4.6.1-1
- 0.4.6
- 0.4.6.1
- -Werror-implicit-function-declaration is added upstream

* Sat Jun 28 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.4.5-1
- 0.4.5 (remote server access function temporally removed)
- BR: intltool

* Sun May 25 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.4.4.2-1
- 0.4.4.2

* Mon May 19 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.4.4.0-1
- 0.4.4.0

* Sun May 11 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.4.1.1-1
- 0.4.1
- 0.4.1.1

* Mon May  5 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.4.0-1
- 0.4.0

* Sun Apr 13 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.3.9.98-2
- First trial to suppress compilation warning (containing fix for
  crash on an occasion)

* Wed Apr  9 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.3.9.98-1
- 0.3.9.98

* Thu Mar 20 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.3.9.10-1
- 0.3.9.10

* Sat Mar 15 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.3.9.5-1
- 0.3.9.5

* Wed Mar  5 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.3.9-1
- 0.3.9

* Fri Feb 29 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.3.6.1-1
- 0.3.6.1

* Sat Feb 23 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.3.6-1
- 0.3.6

* Wed Feb 20 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.3.5.99-1
- 0.3.6 RC
- 2 patches dropped (applied by upstream)

* Tue Feb 19 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.3.5.23-3
- Fix crash on mounting removable devices

* Mon Feb 18 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.3.5.23-2
- Apply patch to fix crash on 64bits arch as suggested by Hans
  (bug 433182)
- Disable to mount removable devices for now

* Sun Feb 17 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.3.5.23-1
- Initial draft
- Disable inotify support, too buggy (also default is no currently)


