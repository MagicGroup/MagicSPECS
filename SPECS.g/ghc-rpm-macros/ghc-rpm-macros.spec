%global debug_package %{nil}

%global macros_dir %{_rpmconfigdir}/macros.d

# uncomment to bootstrap without hscolour
#%%global without_hscolour 1

Name:           ghc-rpm-macros
Version:        1.4.15
Release:        4%{?dist}
Summary:        RPM macros for building packages for GHC

License:        GPLv3+
URL:            https://fedoraproject.org/wiki/Packaging:Haskell

# This is a Fedora maintained package, originally made for
# the distribution.  Hence the source is currently only available
# from this package.  But it could be hosted on fedorahosted.org
# for example if other rpm distros would prefer that.
Source0:        macros.ghc
Source1:        COPYING
Source2:        AUTHORS
Source3:        ghc-deps.sh
Source4:        cabal-tweak-dep-ver
Source5:        cabal-tweak-flag
Source6:        macros.ghc-extra
Source7:        ghc_bin.attr
Source8:        ghc_lib.attr
Requires:       ghc-srpm-macros
# macros.ghc-srpm moved out from redhat-rpm-config-21
Requires:       redhat-rpm-config > 20-1.fc21
# for ghc_version
Requires:       ghc-compiler
%if %{undefined without_hscolour}
# could use ghc_arches here
%ifarch %{ix86} %{ix86} x86_64 ppc ppc64 alpha sparcv9 armv7hl armv5tel s390 s390x ppc64le aarch64
Requires:       hscolour
%endif
%endif

%description
A set of macros for building GHC packages following the Haskell Guidelines
of the Fedora Haskell SIG.  ghc needs to be installed in order to make use of
these macros.


%package extra
Summary:        Extra RPM macros for building Haskell library subpackages
Requires:       %{name} = %{version}-%{release}

%description extra
Extra macros used for subpackaging of Haskell libraries,
for example in ghc and haskell-platform.


# ideally packages should be obsoletes by some relevant package
# this is a last resort when there is no such appropriate package
%package -n ghc-obsoletes
Summary:        Dummy package to obsolete deprecated Haskell packages
# these 3 no longer build with ghc-7.8 (F22)
Obsoletes:      ghc-ForSyDe < 3.1.2, ghc-ForSyDe-devel < 3.1.2
Obsoletes:      ghc-parameterized-data < 0.1.6
Obsoletes:      ghc-parameterized-data-devel < 0.1.6
Obsoletes:      ghc-type-level < 0.2.5, ghc-type-level-devel < 0.2.5
Obsoletes:      leksah < 0.14, ghc-leksah < 0.14, ghc-leksah-devel < 0.14
# dropped from HP 2014.2 (F22)
Obsoletes:      ghc-cgi < 3001.1.8,  ghc-cgi-devel < 3001.1.8

%description -n ghc-obsoletes
Meta package for obsoleting deprecated Haskell packages.

This package can safely be removed.


%prep
%setup -c -T
cp %{SOURCE1} %{SOURCE2} .


%build
echo no build stage needed


%install
install -p -D -m 0644 %{SOURCE0} %{buildroot}/%{macros_dir}/macros.ghc
install -p -D -m 0644 %{SOURCE6} %{buildroot}/%{macros_dir}/macros.ghc-extra

install -p -D -m 0755 %{SOURCE3} %{buildroot}/%{_prefix}/lib/rpm/ghc-deps.sh
install -p -D -m 0644 %{SOURCE7} %{buildroot}/%{_prefix}/lib/rpm/fileattrs/ghc_bin.attr
install -p -D -m 0644 %{SOURCE8} %{buildroot}/%{_prefix}/lib/rpm/fileattrs/ghc_lib.attr

install -p -D -m 0755 %{SOURCE4} %{buildroot}/%{_bindir}/cabal-tweak-dep-ver
install -p -D -m 0755 %{SOURCE5} %{buildroot}/%{_bindir}/cabal-tweak-flag


%files
%doc COPYING AUTHORS
%{macros_dir}/macros.ghc
%{_prefix}/lib/rpm/fileattrs/ghc_bin.attr
%{_prefix}/lib/rpm/fileattrs/ghc_lib.attr
%{_prefix}/lib/rpm/ghc-deps.sh
%{_bindir}/cabal-tweak-dep-ver
%{_bindir}/cabal-tweak-flag


%files extra
%{macros_dir}/macros.ghc-extra


%if 0%{?fedora} >= 22
%files -n ghc-obsoletes
%endif


%changelog
* Sun Sep 20 2015 Liu Di <liudidi@gmail.com> - 1.4.15-4
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Jens Petersen <petersen@redhat.com> - 1.4.15-3
- reenable dynamic linking for aarch64 (#1195231)

* Mon May 25 2015 Jens Petersen <petersen@redhat.com> - 1.4.15-2
- add leksah to ghc-obsoletes

* Thu May  7 2015 Jens Petersen <petersen@redhat.com> - 1.4.15-1
- cabal macro now sets utf8 locale
- disable dynamic linking on aarch64 as a workaround (#1195231)

* Thu Apr  2 2015 Jens Petersen <petersen@redhat.com> - 1.4.14-1
- add explicit --enable-shared again for arm64

* Mon Mar 23 2015 Jens Petersen <petersen@redhat.com> - 1.4.13-1
- fix ghc-deps.sh for ghc builds:
- use .a files again instead of .conf for devel deps
- extract pkg-ver from library filename rather than directory
  (should also work for 7.10)
- introduce ghc_pkgdocdir since no _pkgdocdir in RHEL 7 and earlier

* Sat Mar  7 2015 Jens Petersen <petersen@fedoraproject.org> - 1.4.12-1
- allow overriding ghc- prefix with ghc_name (for ghc784 etc)

* Fri Mar  6 2015 Jens Petersen <petersen@redhat.com> - 1.4.11-2
- add ghc-obsoletes dummy subpackage for obsoleting deprecated packages
- initially: ForSyDe, parameterized-data, type-level, and cgi for F22

* Mon Mar  2 2015 Jens Petersen <petersen@redhat.com> - 1.4.11-1
- fix ghc-deps.sh to handle meta-packages
- configure --disable-shared if ghc_without_shared

* Fri Feb 27 2015 Jens Petersen <petersen@fedoraproject.org> - 1.4.10-1
- have to turn off hardening in cabal_configure: set _hardened_ldflags to nil

* Fri Feb 27 2015 Jens Petersen <petersen@fedoraproject.org> - 1.4.9-1
- turn off _hardened_build for libraries since it breaks linking
  <https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code>

* Sun Feb  1 2015 Jens Petersen <petersen@redhat.com> - 1.4.8-1
- drop cabal_tests_not_working since not all tests failing on ARMv7

* Sat Jan 31 2015 Jens Petersen <petersen@redhat.com> - 1.4.7-1
- fix arch for cabal_tests_not_working
- add cabal_test macro which uses it

* Sat Jan 31 2015 Jens Petersen <petersen@redhat.com> - 1.4.6-1
- disable Cabal tests on armv7 since they give an internal error
  https://ghc.haskell.org/trac/ghc/ticket/10029
- fix building of meta packages:
- only run cabal haddock for real libraries with modules
- make sure basepkg.files is also created for meta packages

* Sat Jan 31 2015 Jens Petersen <petersen@redhat.com> - 1.4.5-1
- fix the R*PATH regexp

* Sat Jan 31 2015 Jens Petersen <petersen@redhat.com> - 1.4.4-1
- ghc_fix_dynamic_rpath: on ARMv7 RPATH is RUNPATH

* Thu Jan 22 2015 Jens Petersen <petersen@redhat.com> - 1.4.3-1
- version ghcpkgdocdir
- add new names ghc_html_dir, ghc_html_libraries_dir, and ghc_html_pkg_dir

* Thu Jan 22 2015 Jens Petersen <petersen@redhat.com> - 1.4.2-1
- correct cabal-tweak-flag error message for missing flag (#1184508)

* Sat Jan 17 2015 Jens Petersen <petersen@redhat.com> - 1.4.1-1
- revert to versioned doc htmldirs

* Sat Jan 17 2015 Jens Petersen <petersen@redhat.com> - 1.4.0-1
- enable shared libraries and dynamic linking on all arch's
  since ghc-7.8 now supports that
- disable debuginfo until ghc-7.10 which will support dwarf debugging output
  (#1138982)

* Fri Nov 14 2014 Jens Petersen <petersen@redhat.com> - 1.3.10-1
- split ghc.attr into ghc_lib.attr and ghc_bin.attr for finer grained handling
- require ghc-compiler for ghc_version

* Mon Oct 27 2014 Jens Petersen <petersen@redhat.com> - 1.3.9-1
- macros.ghc: cabal_configure now passes CFLAGS and LDFLAGS to ghc (#1138982)
  (thanks to Sergei Trofimovich and Ville Skyttä)

* Thu Oct 23 2014 Jens Petersen <petersen@redhat.com> - 1.3.8-1
- ghc-deps.sh: support ghc-pkg for ghc builds <= 7.4.2 as well

* Thu Oct 16 2014 Jens Petersen <petersen@redhat.com> - 1.3.7-1
- ghc.attr needs to handle requires for /usr/bin files too

* Wed Sep 10 2014 Jens Petersen <petersen@redhat.com> - 1.3.6-1
- improve ghc_fix_dynamic_rpath not to assume cwd = pkg_name

* Fri Aug 29 2014 Jens Petersen <petersen@redhat.com> - 1.3.5-1
- no longer disable debuginfo by default:
  packages now need to explicitly opt out of debuginfo if appropriate

* Thu Aug 28 2014 Jens Petersen <petersen@redhat.com> - 1.3.4-1
- drop -O2 for ghc-7.8: it uses too much build mem

* Fri Aug 22 2014 Jens Petersen <petersen@redhat.com> - 1.3.3-1
- temporarily revert to ghc-7.6 config for shared libs
  until we move to ghc-7.8

* Thu Aug 21 2014 Jens Petersen <petersen@redhat.com> - 1.3.2-1
- add an rpm .attr file for ghc-deps.sh rather than running it
  as an external dep generator (#1132275)
  (see http://rpm.org/wiki/PackagerDocs/DependencyGenerator)

* Wed Aug 20 2014 Jens Petersen <petersen@redhat.com> - 1.3.1-1
- fix warning in macros.ghc-extra about unused pkgnamever

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Aug  2 2014 Jens Petersen <petersen@redhat.com> - 1.3.0-1
- shared libs available for all archs in ghc-7.8
- cabal_configure --disable-shared with ghc_without_shared
- ghc_clear_execstack no longer needed

* Fri Jun 27 2014 Jens Petersen <petersen@redhat.com> - 1.2.13-2
- ghc-srpm-macros is now a separate source package

* Fri Jun  6 2014 Jens Petersen <petersen@redhat.com> - 1.2.13-1
- add aarch64

* Sun Jun  1 2014 Jens Petersen <petersen@redhat.com> - 1.2.12-1
- add missing ppc64, s390, and s390x to ghc_arches
- add new ppc64le to ghc_arches

* Fri May 30 2014 Jens Petersen <petersen@redhat.com> - 1.2.11-1
- condition use of execstack since no prelink on ppc64le or arm64

* Wed May 21 2014 Dennis Gilmore <dennis@ausil.us> - 1.2.10-2
- add %%ghc_arches back to macros.ghc-srpm to maintain compatability with
- existing specs

* Fri May 16 2014 Jens Petersen <petersen@redhat.com> - 1.2.10-1
- do bcond cabal configure --enable-tests also for Bin packages

* Fri May 16 2014 Jens Petersen <petersen@redhat.com> - 1.2.9-1
- enable configure bcond check for tests

* Tue May 13 2014 Jens Petersen <petersen@redhat.com> - 1.2.8-1
- use -O2 also for executable (Bin) packages and allow it to be overrided

* Wed Apr 30 2014 Jens Petersen <petersen@redhat.com> - 1.2.7-1
- ghc-rpm-macros requires ghc-srpm-macros
- ghc-srpm-macros does not require ghc-rpm-macros
- drop ExclusiveArch and make hscolour requires arch conditional
- make ghc-srpm-macros subpackage noarch
- set Url field when generating subpackages

* Mon Apr 28 2014 Jens Petersen <petersen@redhat.com> - 1.2.6-1
- move macros.ghc-srpm from redhat-rpm-config to new ghc-srpm-macros subpackage:
  defines ghc_arches_with_ghci and drops no longer used ghc_arches (#1089102)
- update license tag to GPLv3+

* Fri Mar 28 2014 Jens Petersen <petersen@redhat.com> - 1.2.5-1
- handle no _pkgdocdir in RHEL7 and docdir path different to F20+

* Mon Mar 17 2014 Jens Petersen <petersen@redhat.com> - 1.2.4-1
- abort ghc_fix_dynamic_rpath if no chrpath

* Thu Feb 13 2014 Ville Skyttä <ville.skytta@iki.fi> - 1.2.3-2
- Install macros to %%{_rpmconfigdir}/macros.d.

* Mon Feb 10 2014 Jens Petersen <petersen@redhat.com> - 1.2.3-1
- set datasubdir in cabal_configure for ghc-7.8

* Fri Jan 10 2014 Jens Petersen <petersen@redhat.com> - 1.2.2-1
- quote the ghc_fix_dynamic_rpath error message

* Fri Jan 10 2014 Jens Petersen <petersen@redhat.com> - 1.2.1-1
- ghc_fix_dynamic_rpath: abort for non-existent executable name
- cabal-tweak-flag: add manual field to enforce flag changes

* Tue Oct 15 2013 Jens Petersen <petersen@redhat.com> - 1.2-1
- add ghcpkgdocdir, which like _pkgdocdir allows for unversioned haddock dirs

* Tue Sep 10 2013 Jens Petersen <petersen@redhat.com> - 1.1.3-1
- ghc-deps.sh: fix ghc-pkg path when bootstrapping new ghc version

* Mon Sep  9 2013 Jens Petersen <petersen@redhat.com> - 1.1.2-1
- fix ghc-deps.sh when bootstrapping a new ghc version

* Mon Sep  9 2013 Jens Petersen <petersen@redhat.com> - 1.1.1-1
- use objdump -p instead of ldd to read executable dependencies

* Sat Sep  7 2013 Jens Petersen <petersen@redhat.com> - 1.1-1
- update ghc-deps.sh to handling ghc-7.8 rts

* Tue Aug 27 2013 Jens Petersen <petersen@redhat.com> - 1.0.8-1
- drop ghc_docdir in favor of _pkgdocdir
- no longer version package htmldirs

* Fri Jul 26 2013 Jens Petersen <petersen@redhat.com> - 1.0.7-1
- add ghc_docdir for package's docdir since not provided by standard macros

* Fri Jul 26 2013 Jens Petersen <petersen@redhat.com> - 1.0.6-1
- also make %%ghc_lib_build docdir unversioned
- require redhat-rpm-config >= 9.1.0-50.fc20 for unversioned docdir

* Fri Jul 26 2013 Jens Petersen <petersen@redhat.com> - 1.0.5-1
- F20 Change: docdir's are now unversioned

* Thu Jul 11 2013 Jens Petersen <petersen@redhat.com> - 1.0.4-1
- check for bindir before looking for executables in ghc_clear_execstack

* Wed Jul 10 2013 Jens Petersen <petersen@redhat.com> - 1.0.3-1
- add ghc_clear_execstack and use it also in ghc_lib_install (#973512)
  and require prelink for execstack

* Tue Jul  9 2013 Jens Petersen <petersen@redhat.com> - 1.0.2-1
- drop doc and prof obsoletes and provides from ghc_lib_subpackage
- clear executable stack flag when installing package executables (#973512)

* Thu Jun 20 2013 Jens Petersen <petersen@redhat.com> - 1.0.1-1
- only configure with --global if not subpackaging libs

* Thu Jun 20 2013 Jens Petersen <petersen@redhat.com> - 1.0-3
- reenable hscolour

* Thu Jun 20 2013 Jens Petersen <petersen@redhat.com> - 1.0-2
- turn off hscolour for bootstrap

* Wed Jun 19 2013 Jens Petersen <petersen@redhat.com> - 1.0-1
- add --global to cabal_configure

* Mon Jun 17 2013 Jens Petersen <petersen@redhat.com> - 0.99.4-1
- merge remaining extra macros into ghc_lib_subpackage

* Thu Jun  6 2013 Jens Petersen <petersen@redhat.com> - 0.99.3-1
- configure builds with ghc -O2 (#880135)

* Wed Jun  5 2013 Jens Petersen <petersen@redhat.com> - 0.99.2-1
- drop -h option from extra macros and make -m work again

* Fri May 17 2013 Jens Petersen <petersen@redhat.com> - 0.99.1-1
- drop new ghc_compiler macro since it is not good for koji
- ghc_fix_dynamic_rpath: do not assume first RPATH

* Tue Apr 23 2013 Jens Petersen <petersen@redhat.com> - 0.99-1
- update for simplified revised Haskell Packaging Guidelines
  (https://fedorahosted.org/fpc/ticket/194)
- packaging for without_shared is now done the same way as shared
  to make non-shared arch packages same as shared ones:
  so all archs will now have base library binary packages
- move spec section metamacros and multiple library packaging macros still
  needed for ghc and haskell-platform to new extra subpackage
- drop ghc_add_basepkg_file macro and ghc_exclude_docdir
- for ghc-7.6 --global-package-db replaces --global-conf and
  --no-user-package-db deprecates --no-user-package-conf

* Wed Mar 20 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.98.1-4
- Remove %%config from %%{_sysconfdir}/rpm/macros.*
  (https://fedorahosted.org/fpc/ticket/259).

* Tue Feb 26 2013 Jens Petersen <petersen@redhat.com> - 0.98.1-3
- only add lib pkgdir to filelist if it exists
  to fix haskell-platform build on secondary archs (no shared libs)
- add ghc_with_lib_for_ghci which re-enables ghci library .o files
  (should not normally be necessary since ghci can load .a files)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 22 2013 Jens Petersen <petersen@redhat.com> - 0.98.1-1
- simplify cabal-tweak-flag script to take one flag value

* Mon Jan 21 2013 Jens Petersen <petersen@redhat.com> - 0.98-1
- new ghc_fix_dynamic_rpath macro for cleaning up package executables
  linked against their own libraries

* Fri Jan 18 2013 Jens Petersen <petersen@redhat.com> - 0.97.6-1
- be more careful about library pkgdir ownership (#893777)

* Mon Dec  3 2012 Jens Petersen <petersen@redhat.com> - 0.97.5-1
- add cabal-tweak-flag script for toggling flag default

* Sat Nov 17 2012 Jens Petersen <petersen@redhat.com> - 0.97.4-1
- enable hscolour again

* Sat Nov 17 2012 Jens Petersen <petersen@redhat.com> - 0.97.3.1-1
- bootstrap hscolour

* Thu Oct 25 2012 Jens Petersen <petersen@redhat.com> - 0.97.3-1
- BR redhat-rpm-config instead of ghc-rpm-macros
- no longer set without_hscolour in macros.ghc for bootstrapping

* Tue Oct  9 2012 Jens Petersen <petersen@redhat.com> - 0.97.2-1
- "cabal haddock" needs --html option with --hoogle to output html

* Thu Sep 20 2012 Jens Petersen <petersen@redhat.com> - 0.97.1-2
- no need to BR hscolour

* Wed Sep 19 2012 Jens Petersen <petersen@redhat.com> - 0.97.1-1
- fix broken duplicate hash output for haskell-platform binaries buildhack
  when haskell-platform locally installed

* Sat Sep  8 2012 Jens Petersen <petersen@redhat.com> - 0.97-1
- ghc-rpm-macros now requires hscolour so packages no longer need to BR it
- this can be disabled for bootstrapping by setting without_hscolour

* Fri Aug 24 2012 Jens Petersen <petersen@redhat.com> - 0.96-1
- make haddock build hoogle files
- Fedora ghc-7.4.2 Cabal will not build ghci lib files by default

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.95.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 25 2012 Jens Petersen <petersen@redhat.com> - 0.95.6-1
- provide doc from devel a little longer to silence rpmlint

* Fri Jun 22 2012 Jens Petersen <petersen@redhat.com> - 0.95.5.1-1
- cabal-tweak-dep-ver: be careful only to match complete dep name and
  do not match beyond ","

* Fri Jun 22 2012 Jens Petersen <petersen@redhat.com> - 0.95.5-1
- some cabal-tweak-dep-ver improvements:
- show file name when no match
- backslash quote . and * in the match string
- create a backup file if none exists

* Fri Jun 22 2012 Jens Petersen <petersen@redhat.com> - 0.95.4-1
- new cabal-tweak-dep-ver script to tweak depends version bounds in .cabal

* Sat Jun  9 2012 Jens Petersen <petersen@redhat.com> - 0.95.3-1
- ghc-dep.sh: only use buildroot package.conf.d if it exists

* Fri Jun  8 2012 Jens Petersen <petersen@redhat.com> - 0.95.2-1
- ghc-deps.sh: look in buildroot package.conf.d for program deps

* Fri Jun  8 2012 Jens Petersen <petersen@redhat.com> - 0.95.1-1
- add a meta-package option to ghc_devel_package and use in ghc_devel_requires

* Thu Jun  7 2012 Jens Petersen <petersen@redhat.com> - 0.95-1
- let ghc_bin_install take an arg to disable implicit stripping for subpackages

* Thu Jun  7 2012 Jens Petersen <petersen@redhat.com> - 0.94-1
- allow ghc_description, ghc_devel_description, ghc_devel_post_postun
  to take args

* Thu Jun  7 2012 Jens Petersen <petersen@redhat.com> - 0.93-1
- fix doc handling of subpackages for ghc_without_shared

* Thu Jun  7 2012 Jens Petersen <petersen@redhat.com> - 0.92-1
- move --disable-library-for-ghci to ghc_lib_build
- revert back to fallback behaviour for common_summary and common_description
  since it is needed for ghc and haskell-platform subpackaging
- without ghc_exclude_docdir include doc dir also for subpackages

* Tue Jun  5 2012 Jens Petersen <petersen@redhat.com> - 0.91-1
- no longer build redundant ghci .o library files
- support meta packages like haskell-platform without base lib files
- make it possible not to have to use common_summary and common_description
- rename ghc_binlib_package to ghc_lib_subpackage
- add ghc_lib_build_without_haddock
- no longer drop into package dirs when subpackaging with ghc_lib_build and
  ghc_lib_install
- add shell variable cabal_configure_extra_options to cabal_configure for
  local configuration

* Mon Mar 19 2012 Jens Petersen <petersen@redhat.com> - 0.90-1
- use new rpm metadata hash format for ghc-7.4
- drop prof meta hash data
- no longer include doc files automatically by default
- no longer provide doc subpackage
- do not provide prof when without_prof set

* Thu Feb 23 2012 Jens Petersen <petersen@redhat.com> - 0.15.5-1
- fix handling of devel docdir for non-shared builds
- simplify ghc_bootstrap

* Thu Jan 19 2012 Jens Petersen <petersen@redhat.com> - 0.15.4-1
- allow dynamic linking of Setup with ghc_without_shared set

* Fri Jan  6 2012 Jens Petersen <petersen@redhat.com> - 0.15.3-1
- new ghc_add_basepkg_file to add a path to base lib package filelist

* Wed Dec 28 2011 Jens Petersen <petersen@redhat.com> - 0.15.2-1
- add ghc_devel_post_postun to help koji/mock with new macros

* Tue Dec 27 2011 Jens Petersen <petersen@redhat.com> - 0.15.1-1
- add ghc_package, ghc_description, ghc_devel_package, ghc_devel_description

* Tue Dec 27 2011 Jens Petersen <petersen@redhat.com> - 0.15-1
- new ghc_files wrapper macro for files which takes base doc files as args
  and uses new ghc_shared_files and ghc_devel_files macros
- when building for non-shared archs move installed docfiles to devel docdir

* Fri Dec  2 2011 Jens Petersen <petersen@redhat.com> - 0.14.3-1
- do not use ghc user config by default when compiling Setup
- do not setup hscolour if without_hscolour defined

* Thu Nov 17 2011 Jens Petersen <petersen@redhat.com> - 0.14.2-1
- test for HsColour directly when running "cabal haddock" instead of
  check hscolour is available (reported by Giam Teck Choon, #753833)

* Sat Nov 12 2011 Jens Petersen <petersen@redhat.com> - 0.14.1-1
- fix double listing of docdir in base lib package

* Tue Nov  1 2011 Jens Petersen <petersen@redhat.com> - 0.14-1
- replace devel ghc requires with ghc-compiler
- disable testsuite in ghc_bootstrap

* Mon Oct 17 2011 Jens Petersen <petersen@redhat.com> - 0.13.13-1
- add ghc_bootstrapping to ghc_bootstrap for packages other than ghc
- make ghc-deps.sh also work when bootstrapping a new ghc version

* Sat Oct 15 2011 Jens Petersen <petersen@redhat.com> - 0.13.12-1
- add ghc_exclude_docdir to exclude docdir from filelists

* Fri Sep 30 2011 Jens Petersen <petersen@redhat.com> - 0.13.11-1
- fix devel subpackage's prof and doc obsoletes and provides versions
  for multiple lib packages like ghc (reported by Henrik Nordström)

* Tue Sep 13 2011 Jens Petersen <petersen@redhat.com> - 0.13.10-1
- do not setup ghc-deps.sh when ghc_bootstrapping
- add ghc_test build config

* Wed Aug  3 2011 Jens Petersen <petersen@redhat.com> - 0.13.9-1
- drop without_testsuite from ghc_bootstrap since it breaks koji

* Fri Jul  1 2011 Jens Petersen <petersen@redhat.com> - 0.13.8-1
- drop redundant defattr from filelists
- move dependency generator setup from ghc_package_devel to ghc_lib_install
  in line with ghc_bin_install

* Mon Jun 27 2011 Jens Petersen <petersen@redhat.com> - 0.13.7-1
- add requires for redhat-rpm-config for ghc_arches
- drop ghc_bootstrapping from ghc_bootstrap: doesn't work for koji

* Fri Jun 17 2011 Jens Petersen <petersen@redhat.com> - 0.13.6-1
- also set ghc_without_dynamic for ghc_bootstrap
- drop without_hscolour from ghc_bootstrap: doesn't work for koji

* Fri Jun 17 2011 Jens Petersen <petersen@redhat.com> - 0.13.5-1
- ghc_bootstrap is now a macro which sets ghc_bootstrapping,
  ghc_without_shared, without_prof, without_haddock, without_hscolour,
  without_manual, without_testsuite
- tweaks to ghc_check_bootstrap

* Fri Jun 17 2011 Jens Petersen <petersen@redhat.com> - 0.13.4-1
- add ghc_check_bootstrap

* Thu Jun  2 2011 Jens Petersen <petersen@redhat.com> - 0.13.3-1
- rename macros.ghc-pkg back to macros.ghc
- move the devel summary prefix back to a suffix

* Sat May 28 2011 Jens Petersen <petersen@redhat.com> - 0.13.2-1
- macros need to live in /etc/rpm
- use macro_file for macros.ghc filepath

* Sat May 28 2011 Jens Petersen <petersen@redhat.com> - 0.13.1-1
- move macros.ghc to /usr/lib/rpm to avoid conflict with redhat-rpm-config

* Wed May 11 2011 Jens Petersen <petersen@redhat.com> - 0.13-1
- merge prof subpackages into devel to simplify packaging

* Mon May  9 2011 Jens Petersen <petersen@redhat.com> - 0.12.1-1
- include ghc_pkg_c_deps even when -c option used

* Sat May  7 2011 Jens Petersen <petersen@redhat.com> - 0.12.0-1
- drop ghc_pkg_deps from ghc_package_devel and ghc_package_prof since
  ghc-deps.sh generates better inter-package dependencies already
- condition --htmldir on pkg_name

* Fri Apr  1 2011 Jens Petersen <petersen@redhat.com> - 0.11.14-1
- provides ghc-*-doc still needed for current lib templates

* Mon Mar 28 2011 Jens Petersen <petersen@redhat.com> - 0.11.13-1
- ghc-deps.sh: check PKGBASEDIR exists to avoid warning for bin package
- abort cabal_configure if ghc is not self-bootstrapped
- make ghc_reindex_haddock a safe no-op
- no longer provide ghc-*-doc
- no longer run ghc_reindex_haddock in ghc-*-devel scripts

* Thu Mar 10 2011 Jens Petersen <petersen@redhat.com> - 0.11.12-1
- add ghc_pkg_obsoletes to binlib base lib package too

* Wed Mar  9 2011 Jens Petersen <petersen@redhat.com> - 0.11.11-1
- add docdir when subpackaging packages too

* Sun Feb 13 2011 Jens Petersen <petersen@redhat.com> - 0.11.10-1
- this package is now arch-dependent
- rename without_shared to ghc_without_shared and without_dynamic
  to ghc_without_dynamic so that they can be globally defined for
  secondary archs without shared libs
- use %%undefined macro
- disable debug_package in ghc_bin_build and ghc_lib_build
- set ghc_without_shared and ghc_without_dynamic on secondary
  (ie non main intel) archs
- disable debuginfo for self

* Fri Feb 11 2011 Jens Petersen <petersen@redhat.com> - 0.11.9-1
- revert "set without_shared and without_dynamic by default on secondary archs
  in cabal_bin_build and cabal_lib_build" change, since happening for all archs

* Thu Feb 10 2011 Jens Petersen <petersen@redhat.com> - 0.11.8-1
- only link Setup dynamically if without_shared and without_dynamic not set
- set without_shared and without_dynamic by default on secondary archs
  in cabal_bin_build and cabal_lib_build
- add cabal_configure_options to pass extra options to cabal_configure

* Thu Feb 10 2011 Jens Petersen <petersen@redhat.com> - 0.11.7-1
- fix ghc-deps.sh for without_shared libraries

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 29 2011 Jens Petersen <petersen@redhat.com> - 0.11.6-1
- simplify adding shared subpackage license file
- own ghc-deps.sh not /usr/lib/rpm

* Sun Jan 23 2011 Jens Petersen <petersen@redhat.com> - 0.11.5-1
- add rpm hash requires for dynamic executables in ghc-deps.sh
- compile Setup in cabal macro
- use _rpmconfigdir

* Sat Jan 22 2011 Jens Petersen <petersen@redhat.com> - 0.11.4-1
- drop deprecated ghcdocdir and ghcpkgdir
- new ghclibdocdir
- replace some missed RPM_BUILD_ROOT's
- bring back ghc requires in ghc_devel_requires
- improve prof summary and description
- add without_prof and without_haddock option macros

* Fri Jan 21 2011 Jens Petersen <petersen@redhat.com> - 0.11.3-1
- compile Setup to help speed up builds

* Thu Jan 20 2011 Jens Petersen <petersen@redhat.com> - 0.11.2-1
- put docdir (license) also into shared lib subpackage
- add ghc_binlib_package option to exclude package from ghc_packages_list
- condition lib base package additional description for srpm

* Mon Jan  3 2011 Jens Petersen <petersen@redhat.com> - 0.11.1-1
- use buildroot instead of RPM_BUILD_ROOT
- rename ghcpkgbasedir to ghclibdir
- split "[name-version]" args into "[name] [version]" args
- move remaining name and version macro options (-n and -v) to args
- drop deprecated -o options

* Thu Dec 30 2010 Jens Petersen <petersen@redhat.com> - 0.11.0-1
- add support for subpackaging ghc's libraries:
- deprecate ghcpkgdir and ghcdocdir from now on
- ghc_gen_filelists optional arg is now name-version
- ghc_lib_build, ghc_lib_install, cabal_pkg_conf now take optional
  name-version arg

* Mon Dec 20 2010 Jens Petersen <petersen@redhat.com> - 0.10.3-1
- revert disabling debug_package, since with redhat-rpm-config installed
  the behaviour depended on the position of ghc_lib_package in the spec file
  (reported by narasim)

* Fri Nov 26 2010 Jens Petersen <petersen@redhat.com>
- drop with_devhelp since --html-help option gone from haddock-2.8.0

* Tue Nov 23 2010 Jens Petersen <petersen@redhat.com> - 0.10.2-1
- ignore ghc's builtin pseudo-libs

* Tue Nov 23 2010 Jens Petersen <petersen@redhat.com> - 0.10.1-1
- bring back the explicit n-v-r internal package requires for devel and prof packages

* Mon Nov 22 2010 Jens Petersen <petersen@redhat.com> - 0.10.0-1
- turn on pkg hash metadata (for ghc-7 builds)
- ghc-deps.sh now requires an extra buildroot/ghcpkgbasedir arg
- automatic internal package deps from prof to devel to base
- rename ghc_requires to ghc_devel_requires
- drop ghc_doc_requires
- ghc_reindex_haddock is deprecated and now a no-op

* Thu Sep 30 2010 Jens Petersen <petersen@redhat.com> - 0.9.1-1
- fix without_shared build so it actually works

* Thu Sep 30 2010 Jens Petersen <petersen@redhat.com> - 0.9.0-1
- add rpm provides and requires script ghc-deps.sh for package hash metadata
- turn on hash provides and disable debuginfo by default
- make shared and hscolour default
- use without_shared and without_hscolour to disable them
- add ghc_pkg_obsoletes for obsoleting old packages
- use ghcpkgbasedir
- always obsolete -doc packages, but keep -o for now for backward compatibility

* Fri Jul 16 2010 Jens Petersen <petersen@redhat.com> - 0.8.1-1
- fix ghc_strip_dynlinked when no dynlinked files
- devel should provide doc also when not obsoleting

* Fri Jul 16 2010 Jens Petersen <petersen@redhat.com> - 0.8.0-1
- merge -doc into -devel and provide -o obsoletes doc subpackage option

* Mon Jun 28 2010 Jens Petersen <petersen@redhat.com> - 0.7.1-1
- support hscolour'ing of src from haddock
- really remove redundant summary and description option flags

* Sat Jun 26 2010 Jens Petersen <petersen@redhat.com> - 0.7.0-1
- new ghc_bin_build, ghc_bin_install, ghc_lib_build, ghc_lib_install

* Thu Jun 24 2010 Jens Petersen <petersen@redhat.com> - 0.6.2-1
- a couple more fallback summary tweaks

* Thu Jun 24 2010 Jens Petersen <petersen@redhat.com> - 0.6.1-1
- drop the summary -s and description -d package options since rpm does not
  seem to allow white\ space in macro option args anyway

* Wed Jun 23 2010 Jens Petersen <petersen@redhat.com> - 0.6.0-1
- make ghc_strip_dynlinked conditional on no debug_package

* Wed Jun 23 2010 Jens Petersen <petersen@redhat.com> - 0.5.9-1
- replace ghc_strip_shared with ghc_strip_dynlinked

* Sun Jun 20 2010 Jens Petersen <petersen@redhat.com> - 0.5.8-1
- add ghc_strip_shared to strip shared libraries

* Sun Jun 20 2010 Jens Petersen <petersen@redhat.com> - 0.5.7-1
- add comments over macros
- drop unused cabal_makefile

* Mon Apr 12 2010 Jens Petersen <petersen@redhat.com> - 0.5.6-1
- drop unused ghc_pkg_ver macro
- add ghc_pkg_recache macro

* Fri Jan 15 2010 Jens Petersen <petersen@redhat.com> - 0.5.5-1
- drop optional 2nd version arg from ghcdocdir, ghcpkgdir, and
  ghc_gen_filelists: multiversion subpackages are not supported
- add ghcpkgbasedir
- bring back some shared conditions which were dropped temporarily
- test for ghcpkgdir and ghcdocdir in ghc_gen_filelists
- allow optional pkgname arg for cabal_pkg_conf
- can now package gtk2hs

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 0.5.4-1
- use -v in ghc_requires and ghc_prof_requires for version

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 0.5.3-1
- drop "Library for" from base lib summary

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 0.5.2-1
- use -n in ghc_requires and ghc_prof_requires for when no pkg_name

* Mon Jan 11 2010 Jens Petersen <petersen@redhat.com> - 0.5.1-1
- add ghcdocbasedir
- revert ghcdocdir to match upstream ghc
- ghcdocdir and ghcpkgdir now take optional name version args
- update ghc_gen_filelists to new optional name version args
- handle docdir in ghc_gen_filelists
- ghc_reindex_haddock uses ghcdocbasedir
- summary and description options to ghc_binlib_package, ghc_package_devel,
  ghc_package_doc, and ghc_package_prof

* Sun Jan 10 2010 Jens Petersen <petersen@redhat.com> - 0.5.0-1
- pkg_name must be set now for binlib packages too
- new ghc_lib_package and ghc_binlib_package macros make packaging too easy
- ghc_package_devel, ghc_package_doc, and ghc_package_prof helper macros
- ghc_gen_filelists now defaults to ghc-%%{pkg_name}
- add dynamic bcond to cabal_configure instead of cabal_configure_dynamic

* Thu Dec 24 2009 Jens Petersen <petersen@redhat.com> - 0.4.0-1
- add cabal_configure_dynamic
- add ghc_requires, ghc_doc_requires, ghc_prof_requires

* Tue Dec 15 2009 Jens Petersen <petersen@redhat.com> - 0.3.1-1
- use ghc_version_override to override ghc_version
- fix pkg .conf filelist match

* Sat Dec 12 2009 Jens Petersen <petersen@redhat.com> - 0.3.0-1
- major updates for ghc-6.12, package.conf.d, and shared libraries
- add shared support to cabal_configure, ghc_gen_filelists
- version ghcdocdir
- replace ghc_gen_scripts, ghc_install_scripts, ghc_register_pkg, ghc_unregister_pkg
  with cabal_pkg_conf
- allow (ghc to) override ghc_version

* Mon Nov 16 2009 Jens Petersen <petersen@redhat.com> - 0.2.5-1
- make ghc_pkg_ver only return pkg version

* Mon Nov 16 2009 Jens Petersen <petersen@redhat.com> - 0.2.4-1
- change GHCRequires to ghc_pkg_ver

* Mon Nov 16 2009 Jens Petersen <petersen@redhat.com> - 0.2.3-1
- use the latest installed pkg version for %%GHCRequires

* Mon Nov 16 2009 Jens Petersen <petersen@redhat.com> - 0.2.2-1
- add %%GHCRequires for automatically versioned library deps

* Tue Sep 22 2009 Jens Petersen <petersen@redhat.com> - 0.2.1-2
- no, revert versioned ghcdocdir again!

* Tue Sep 22 2009 Jens Petersen <petersen@redhat.com> - 0.2.1-1
- version ghcdocdir to allow multiple doc versions like ghcpkgdir

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun  9 2009 Jens Petersen <petersen@redhat.com> - 0.2-1
- drop version from ghcdocdir since it breaks haddock indexing

* Wed May 13 2009 Yaakov M. Nemoy <ynemoy@fedoraproject.org> - 0.1-7
- specifies the macros file as a %%conf

* Sat May  9 2009 Yaakov M. Nemoy <ynemoy@fedoraproject.org> - 0.1-6
- removes archs and replaces with noarch
- bumps to avoid conflicts with jens

* Fri May  8 2009 Jens Petersen <petersen@redhat.com> - 0.1-5
- make it arch specific to fedora ghc archs
- setup a build dir so it can build from the current working dir

* Wed May  6 2009 Yaakov M. Nemoy <ynemoy@fedoraproject.org> - 0.1-4
- renamed license file
- removed some extraneous comments needed only at review time

* Wed May  6 2009 Yaakov M. Nemoy <ynemoy@fedoraproject.org> - 0.1-3
- updated license to GPLv3
- added AUTHORS file

* Tue May  5 2009 Yaakov M. Nemoy <ghc@hexago.nl> - 0.1-2
- moved copying license from %%build to %%prep

* Mon May  4 2009 Yaakov M. Nemoy <ghc@hexago.nl> - 0.1-1
- creation of package

