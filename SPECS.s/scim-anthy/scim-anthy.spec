Name:           scim-anthy
Version:        1.2.7
Release:        10%{?dist}

License:        GPLv2+
URL:            http://scim-imengine.sourceforge.jp/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  scim-devel
BuildRequires:  anthy-devel >= 6700b-1 gettext-devel automake autoconf libtool
Source0:        http://osdn.dl.sourceforge.jp/scim-imengine/37309/%{name}-%{version}.tar.gz

Summary:        SCIM IMEngine for anthy for Japanese input
Summary(zh_CN.UTF-8): 日语输入法的 SCIM 引擎
Group:          System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Requires:       scim, kasumi
# This was necessary for the upgrade path from IIIMF
# and ensure the installation of future version of IIIMF.
# No Provides line for iiimf-le-canna is intentional because
# This package doesn't really provide the Language Engine for IIIMF.
# This just works on only SCIM.
Obsoletes:      iiimf-le-canna <= 1:12.2
%description
Scim-anthy is a SCIM IMEngine module for anthy to support Japanese input.
%description -l zh_CN.UTF-8
日语输入法的 SCIM 引擎。


%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -p"

rm $RPM_BUILD_ROOT%{_libdir}/scim-1.0/*/*/*.la
magic_rpm_clean.sh
#find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README
%{_libdir}/scim-1.0/*/Helper/anthy-imengine-helper.so
%{_libdir}/scim-1.0/*/IMEngine/anthy.so
%{_libdir}/scim-1.0/*/SetupUI/anthy-imengine-setup.so
%{_datadir}/scim/Anthy
%{_datadir}/scim/icons/*png


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.2.7-10
- 为 Magic 3.0 重建

* Sat Sep 26 2015 Liu Di <liudidi@gmail.com> - 1.2.7-9
- 为 Magic 3.0 重建

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-7
- Rebuilt for c++ ABI breakage

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1.2.7-5
- Rebuild for new libpng

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 29 2009 Akira TAGOH <tagoh@redhat.com> - 1.2.7-1
- New upstream release.

* Fri Nov 21 2008 Akira TAGOH <tagoh@redhat.com> - 1.2.6-2
- Fix a source URL.

* Tue Oct  7 2008 Akira TAGOH <tagoh@redhat.com> - 1.2.6-1
- New upstream release.

* Tue Mar  4 2008 Akira TAGOH <tagoh@redhat.com> - 1.2.5-1
- New upstream release.

* Thu Jan 31 2008 Akira TAGOH <tagoh@redhat.com> - 1.2.4-4
- scim-anthy-1.2.4-gcc43.patch: Fix a build fail with gcc-4.3.

* Wed Oct 31 2007 Akira TAGOH <tagoh@redhat.com>
- Update the source url.

* Thu Aug 23 2007 Akira TAGOH <tagoh@redhat.com> - 1.2.4-2
- Rebuild

* Fri Aug 10 2007 Akira TAGOH <tagoh@redhat.com>
- Update License tag.

* Wed Jul  4 2007 Jens Petersen <petersen@redhat.com>
- remove with_libstdc_preview macro

* Wed May 30 2007 Akira TAGOH <tagoh@redhat.com> - 1.2.4-1
- New upstream release.
  - we don't need the below patches anymore:
    - scim-anthy-helper-moduledir.patch
    - scim-anthy-1.2.2-gettextize.patch
    - scim-anthy-1.2.0-fix-no-n-candidates.patch

* Tue Mar 13 2007 Akira TAGOH <tagoh@redhat.com> - 1.2.2-3
- Invoke autoheader. (#226390)
- Fix no the number of candidates on the candidate window with focus out/in.

* Mon Mar 12 2007 Akira TAGOH <tagoh@redhat.com> - 1.2.2-2
- clean up a spec file. (#226390)

* Tue Nov 14 2006 Akira TAGOH <tagoh@redhat.com> - 1.2.2-1
- New upstream release.
  - removed unnecessary patches:
    - scim-anthy-libtool-export.patch
    - scim-anthy-fix-pending-state.patch
    - scim-anthy-dict-encoding.patch
- scim-anthy-1.2.2-gettextize.patch: fix a build issue on the latest autotools.

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 1.2.0-3
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 26 2006 Akira TAGOH <tagoh@redhat.com> - 1.2.0-2
- scim-anthy-libtool-export.patch: fix a typo.
- scim-anthy-fix-pending-state.patch: fix not composing roman character
  properly when any characters are still in pending queue after deleting.
  (#208074)
- scim-anthy-dict-encoding.patch: revert the default dictionary encoding to
  EUC-JP.

* Mon Jul 31 2006 Akira TAGOH <tagoh@redhat.com> - 1.2.0-1
- New upstream release.
- scim-anthy-1.0.0-pseudo-ascii*.patch: merged into upstream.
  removed from srpm.

* Fri Jul 14 2006 Akira TAGOH <tagohr@edhat.com> - 1.0.0-4
- scim-anthy-1.0.0-pseudo-ascii.patch,
  scim-anthy-1.0.0-pseudo-ascii-insert-space.patch: applied to allow the ASCII
  characters with the capital letter without even turning off the IME. (#187721)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.0.0-3
- rebuild
- Add missing br automake

* Thu Jul  6 2006 Akira TAGOH <tagoh@redhat.com>
- use dist tag.

* Fri Mar 31 2006 Jens Petersen <petersen@redhat.com> - 1.0.0-2
- rebuild without libstdc++so7

* Thu Mar 30 2006 Akira TAGOH <tagoh@redhat.com> - 1.0.0-1
- New upstream release.
  - can input numerals when the candidate window doesn't appear. (#185934)
- scim-anthy-symbol-style.patch: removed.
- add Requires: gettext-devel
- run aclocal and autoconf as well to regenerate Makefile properly.

* Fri Mar 17 2006 Akira TAGOH <tagoh@redhat.com> - 0.9.0-3
- scim-anthy-symbol-style.patch: applied a backport patch from upstream CVS to
  add an UI for the symbol style. (#178400)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.9.0-2.fc5.1
- bump again for double-long bug on ppc(64)

* Thu Feb  9 2006 Jens Petersen <petersen@redhat.com>
- list .so modules explicitly in filelist

* Thu Feb  9 2006 Jens Petersen <petersen@redhat.com> - 0.9.0-2
- build conditionally with libstdc++so7 preview library (#166041)
  - add with_libstdc_preview switch and tweak libtool to link against newer lib
- add scim-anthy-helper-moduledir.patch to tweak the helper module install dir,
  since scim.pc now returns moduledir with api-version
- remove anthy-imengine-helper.la

* Mon Jan 30 2006 Akira TAGOH <tagoh@redhat.com> - 0.9.0-1
- New upstream release.
- scim-anthy-wide-latin.diff: removed.

* Mon Jan 23 2006 Akira TAGOH <tagoh@redhat.com> - 0.8.0-2
- scim-anthy-wide-latin.diff: applied to fix a problem that the input character
  appears twice with the full size alphanumeric mode.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Dec  1 2005 Akira TAGOH <tagoh@redhat.com> - 0.8.0-1
- New upstream release.

* Mon Nov 14 2005 Akira TAGOH <tagoh@redhat.com> - 0.7.1-2
- added Obsoletes: iiimf-le-canna <= 12.2 to ensure the upgrade path.

* Mon Oct 17 2005 Akira TAGOH <tagoh@redhat.com> - 0.7.1-1
- New upstream release.
- scim-0.7.0-fix_crash_bug.diff: removed.

* Fri Oct  7 2005 Akira TAGOH <tagoh@redhat.com> - 0.7.0-4
- scim-0.7.0-fix_crash_bug.diff: a patch to fix a crash issue.

* Thu Oct  6 2005 Jens Petersen <petersen@redhat.com> - 0.7.0-3
- require scim

* Thu Oct  6 2005 Akira TAGOH <tagoh@redhat.com> - 0.7.0-2
- added Requires: kasumi.

* Thu Sep 29 2005 Akira TAGOH <tagoh@redhat.com> - 0.7.0-1
- New upstream release.

* Tue Aug 16 2005 Akira TAGOH <tagoh@redhat.com> - 0.6.1-1
- New upstream release.

* Tue Aug  9 2005 Akira TAGOH <tagoh@redhat.com>
- added dist tag in Release.

* Tue Aug  2 2005 Akira TAGOH <tagoh@redhat.com> - 0.5.3-6
- removed PreReq as well.

* Tue Aug  2 2005 Akira TAGOH <tagoh@redhat.com> - 0.5.3-5
- removed %%post and %%postun for now.

* Tue Aug  2 2005 Akira TAGOH <tagoh@redhat.com> - 0.5.3-4
- Import into Core.
- relying the file dependencies instead of the explicit package dependency
  of anthy since anthy-libs was gone.
- clean up the spec file.

* Sat Jul 30 2005 Jens Petersen <petersen@redhat.com> - 0.5.3-2
- prereq scim xinput.d script

* Fri Jul 29 2005 Ryo Dairiki <ryo-dairiki@mbm.nifty.com>
- add xinput.d alternatives setup in %%post and %%postun
- provide scim-ja_JP and only uninstall xinput.d-ja_JP alternative if
  no scim-ja_JP left

* Fri Jul 29 2005 Jens Petersen <petersen@redhat.com> - 0.5.3-1
- update to 0.5.3 release

* Tue Jul 26 2005 Ryo Dairiki <ryo-dairiki@mbm.nifty.com> - 0.5.2-1
- update to 0.5.2 release

* Sat Jul  9 2005 Jens Petersen <petersen@redhat.com> - 0.5.1-2
- update to 0.5.1 release

* Thu Jun 30 2005 Jens Petersen <petersen@redhat.com> - 0.5.0-1
- update to 0.5.0 release

* Wed Jun 29 2005 Jens Petersen <petersen@redhat.com> - 0.4.3-1
- use find_lang for translations (Ryo Dairiki)

* Tue Jun 28 2005 Jens Petersen <petersen@redhat.com>
- Initial packaging for Fedora Extras

* Fri May 27 2005 Jens Petersen <petersen@redhat.com> - 0.4.2-1
- Initial packaging.
