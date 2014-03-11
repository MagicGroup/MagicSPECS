Name:           rpmlint
Version:        1.4
Release:        12%{?dist}
Summary:        Tool for checking common errors in RPM packages

Group:          Development/Tools
License:        GPLv2
URL:            http://rpmlint.zarb.org/
Source0:        http://rpmlint.zarb.org/download/%{name}-%{version}.tar.xz
Source1:        %{name}.config
Source2:        %{name}-CHANGES.package.old
Source3:        %{name}-etc.config
# EL-4 specific config
Source4:        %{name}.config.el4
# EL-5 specific config
Source5:        %{name}.config.el5
Patch0: rpmlint-1.4-encoding.patch
# http://sourceforge.net/p/rpmlint/code/ci/671bf6d21c6e878e6ee551ee4e2871df8947ac52/
Patch1: rpmlint-1.4-py3-magic-number-fix.patch
# Tighten macro regexp to min 3 chars, starting with a letter or underscore.
# http://sourceforge.net/p/rpmlint/code/ci/ae8a019e53784a45c59f23a7b09ad47ea7584795/
Patch2: rpmlint-1.4-tighten-macro-regexp.patch
# Fix handling of Ruby RI files as text files, they're always binary files.
# http://rpmlint.zarb.org/cgi-bin/trac.cgi/ticket/569
Patch3: rpmlint-1.4-ruby-ri-files-are-binary.patch
BuildArch:      noarch
BuildRequires:  python >= 2.4
BuildRequires:  rpm-python >= 4.4
BuildRequires:  sed >= 3.95
%if ! 0%{?rhel}
# no bash-completion for RHEL
BuildRequires:  bash-completion
%endif
Requires:       rpm-python >= 4.4.2.2
Requires:       python >= 2.4
%if ! 0%{?rhel}
# python-magic and python-enchant are actually optional dependencies, but
# they bring quite desirable features.  They're not available in RHEL/EPEL 5
# as of 2010-06-23 though.
Requires:       python-magic
Requires:       python-enchant
%endif
Requires:       cpio
Requires:       binutils
Requires:       desktop-file-utils
Requires:       gzip
Requires:       bzip2
Requires:       xz
# Needed for man page check in FilesCheck.py
Requires:	%{_bindir}/groff

%description
rpmlint is a tool for checking common errors in RPM packages.  Binary
and source packages as well as spec files can be checked.


%prep
%setup -q
%patch0 -p1 -b .enc
%patch1 -p1 -b .py3
%patch2 -p1 -b .tighten-regexp
%patch3 -p1 -b .ruby-ri-files
sed -i -e /MenuCheck/d Config.py
cp -p config config.example
install -pm 644 %{SOURCE2} CHANGES.package.old
install -pm 644 %{SOURCE3} config


%build
make COMPILE_PYC=1


%install
touch rpmlint.pyc rpmlint.pyo # just for the %%exclude to work everywhere
make install DESTDIR=$RPM_BUILD_ROOT ETCDIR=%{_sysconfdir} MANDIR=%{_mandir} \
  LIBDIR=%{_datadir}/rpmlint BINDIR=%{_bindir}
install -pm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/rpmlint/config

install -pm 644 %{SOURCE4} $RPM_BUILD_ROOT%{_datadir}/rpmlint/config.el4
install -pm 644 %{SOURCE5} $RPM_BUILD_ROOT%{_datadir}/rpmlint/config.el5
pushd $RPM_BUILD_ROOT%{_bindir}
ln -s rpmlint el4-rpmlint
ln -s rpmlint el5-rpmlint
popd
%if 0%{?rhel}
rm -rf %{buildroot}%{_sysconfdir}/bash_completion.d/
%endif


%check
make check


%files
%doc AUTHORS COPYING ChangeLog CHANGES.package.old README config.example
%config(noreplace) %{_sysconfdir}/rpmlint/
%if 0%{?fedora} >= 17
%{_datadir}/bash-completion/
%else
%if ! 0%{?rhel}
%{_sysconfdir}/bash_completion.d/
%endif
%endif
%{_bindir}/rpmdiff
%{_bindir}/el*-rpmlint
%{_bindir}/rpmlint
%{_datadir}/rpmlint/
%exclude %{_datadir}/rpmlint/rpmlint.py[co]
%{_mandir}/man1/rpmlint.1*


%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.4-12
- 为 Magic 3.0 重建

* Tue Nov  6 2012 Tom Callaway <spot@fedoraproject.org> - 1.4-11
- add Requires: %{_bindir}/groff for man page checks (bz 873448)

* Thu Sep  6 2012 Tom Callaway <spot@fedoraproject.org> - 1.4-10
- fix handling of ruby RI files as text files (they are binary files)
- apply upstream fix for macro regexp

* Tue Sep  4 2012 Thomas Woerner <twoerner@redhat.com> - 1.4-9
- fix build for RHEL: no bash-completion

* Tue Aug 14 2012 Tom Callaway <spot@fedoraproject.org> - 1.4-8
- add magic number fix for python 3 (bz845972)
- update license list

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jan 23 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 1.4-6
-  Patch to fix messages that contain unicode summaries
   https://bugzilla.redhat.com/show_bug.cgi?id=783912

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 15 2011 Tom Callaway <spot@fedoraproject.org> - 1.4-4
- Do not throw an error on .desktop files set +x. (bz 767978)

* Mon Dec  5 2011 Tom Callaway <spot@fedoraproject.org> - 1.4-3
- own %%{_datadir}/bash-completion/ (thanks Ville Skyttä)

* Mon Dec  5 2011 Tom Callaway <spot@fedoraproject.org> - 1.4-2
- add BR: bash-completion for the pc file

* Mon Dec  5 2011 Tom Callaway <spot@fedoraproject.org> - 1.4-1
- update to 1.4

* Wed Oct 12 2011 Tom Callaway <spot@fedoraproject.org> - 1.3-2
- apply upstream fix for false error on checking ghosted man pages for 
  encoding (bz745446)
- update config to reflect new licenses (bz741298)

* Tue Jul 12 2011 Tom Callaway <spot@fedoraproject.org> - 1.3-1
- update to 1.3

* Sun Apr 24 2011 Tom Callaway <spot@fedoraproject.org> - 1.2-1
- update to 1.2
- filter away files-attr-not-set for all targets except EL-4 (bz694579)

* Thu Mar  3 2011 Tom Callaway <spot@fedoraproject.org> - 1.1-3
- apply upstream fix for source url aborts (bz 680781)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb  4 2011 Tom Callaway <spot@fedoraproject.org> - 1.1-1
- update to 1.1

* Tue Dec  7 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0-3
- fix typo in changelog
- %% comment out item in changelog
- simplify el4/el5 config files (thanks to Ville Skyttä)

* Mon Dec  6 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0-2
- add support for el4-rpmlint, el5-rpmlint
- disable no-cleaning-of-buildroot checks for Fedora
- disable no-buildroot-tag check for Fedora
- disable no-%%clean-section check for Fedora

* Mon Nov  1 2010 Ville Skyttä <ville.skytta@iki.fi> - 1.0-1
- Update to 1.0; fixes #637956, and #639823.
- Sync Fedora license list with Wiki revision 1.85.
- Whitelist more expectedly setuid executables; fixes #646455.

* Thu Aug 19 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.99-1
- Update to 0.99; fixes #623607, helps work around #537430.
- Sync Fedora license list with Wiki revision 1.80.

* Wed Aug 11 2010 David Malcolm <dmalcolm@redhat.com> - 0.98-2
- recompiling .py files against Python 2.7 (rhbz#623355)

* Wed Jun 23 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.98-1
- Update to 0.98; fixes #599427 and #599516.
- Filter out all lib*-java and lib*-python explicit-lib-dependency messages.
- Sync Fedora license list with Wiki revision 1.75; fixes #600317.

* Tue May 18 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.97-1
- Update to 0.97; fixes #459452, #589432.
- Filter out explicit-lib-dep messages for libvirt(-python) (Dan Kenigsberg).
- Sync Fedora license list with Wiki revision 1.73.

* Thu Apr 22 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.96-1
- Update to 0.96; fixes #487974, #571375, #571386, #572090, #572097, #578390.
- Sync Fedora license list with Wiki revision 1.71.

* Sat Mar  6 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.95-2
- Patch to fix non-coherent-filename regression for source packages.

* Wed Mar  3 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.95-1
- Update to 0.95; fixes #564585, #567285, #568498, and #570086.

* Mon Feb  1 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.94-1
- Update to 0.94; rpm >= 4.8.0 spec file check fix included upstream.
- Sync Fedora license list with Wiki revision 1.65 (#559156).

* Tue Jan 26 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.93-2
- Apply upstream patch to fix spec file check with rpm >= 4.8.0.

* Mon Jan 25 2010 Ville Skyttä <ville.skytta@iki.fi> - 0.93-1
- Update to 0.93; fixes #531102 and #555284.
- Enable checks requiring network access in default config.
- Disallow kernel module packages in default config.
- Remove old X11R6 dirs from paths treated as system ones in default config.
- Sync Fedora license list with Wiki revision 1.64.
- Omit python-enchant and python-magic dependencies when built on EL.

* Mon Nov  2 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.92-1
- Update to 0.92; fixes #528535, and #531102 (partially).
- Python byte compile patch applied/superseded upstream.
- Add <lua> to list of valid scriptlet shells.
- Sync Fedora license list with Wiki revision 1.53.

* Mon Sep 14 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.91-1
- Update to 0.91; fixes #513811, #515185, #516492, #519694, and #521630.
- Add dependencies on gzip, bzip2, and xz.
- Sync Fedora license list with Wiki revision 1.49.
- Move pre-2008 %%changelog entries to CHANGES.package.old.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 29 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.90-1
- 0.90; fixes #508683.

* Sun Jun 21 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.89-1
- Update to 0.89; fixes #461610, #496735, #496737 (partially), #498107,
  #491188, and #506957.
- Sync Fedora license list with Wiki revision 1.44.
- Parse list of standard users and groups from the setup package's uidgid file.

* Thu Mar 19 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.87-1
- 0.87; fixes #480664, #483196, #483199, #486748, #488146, #488930, #489118.
- Sync Fedora license list with Wiki revision 1.38.
- Configs patch included upstream.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.85-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 20 2009 Ville Skyttä <ville.skytta@iki.fi>
- Sync Fedora license list with Wiki revision 1.34.
- Filter out filename-too-long-for-joliet and symlink-should-be-* warnings in
  default config.

* Mon Dec 01 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.85-3
- Rebuild for Python 2.6

* Thu Oct 30 2008 Ville Skyttä <ville.skytta@iki.fi> - 0.85-2
- Apply upstream patch to load all *config from /etc/rpmlint.

* Thu Oct 23 2008 Ville Skyttä <ville.skytta@iki.fi> - 0.85-1
- 0.85, fixes #355861, #450011, #455371, #456843, #461421, #461423, #461434.
- Mute some explicit-lib-dependency false positives (#458290).
- Sync Fedora license list with Wiki revision 1.19.
- Dist regex patch applied/superseded upstream.

* Fri Sep 12 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.84-3
- Sync Fedora license list with Wiki revision 1.09

* Sat Jul 26 2008 Ville Skyttä <ville.skytta@iki.fi> - 0.84-2
- 0.84, fixes #355861, #456304.
- Sync Fedora license list with Wiki revision "16:08, 18 July 2008".
- Rediff patches.

* Tue May 27 2008 Ville Skyttä <ville.skytta@iki.fi> - 0.83-1
- 0.83, fixes #237204, #428096, #430206, #433783, #434694, #444441.
- Fedora licensing patch applied upstream.
- Move pre-2007 changelog entries to CHANGES.package.old.
- Sync Fedora license list with Revision 0.88.

* Tue May 20 2008 Todd Zullinger <tmz@pobox.com> 
- Sync Fedora license list with Revision 0.83 (Wiki rev 131).

* Mon Mar  3 2008 Ville Skyttä <ville.skytta@iki.fi> - 0.82-3
- Sync Fedora license list with Revision 0.69 (Wiki rev 110) (#434690).
