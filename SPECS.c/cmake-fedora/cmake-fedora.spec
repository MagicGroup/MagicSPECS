Name:       cmake-fedora
Version:    0.8.3
Release:    2%{?dist}
Summary:    CMake helper modules for fedora developers
Summary(zh_CN.UTF-8): fedora 开发人员用的 cmake 模块
License:    BSD
Group:      System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
URL:        https://fedorahosted.org/%{name}/
Source0:    https://fedorahosted.org/releases/c/m/%{name}/%{name}-%{version}-Source.tar.gz

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

BuildRequires:  cmake >= 2.4

Requires:   cmake >= 2.4

%description
cmake-fedora consist a set of cmake modules that provides
helper macros and targets for fedora developers.

%description -l zh_CN.UTF-8
fedora 开发人员用的 cmake 模块。

%prep
%setup -q -n %{name}-%{version}-Source

%build
# $RPM_OPT_FLAGS should be  loaded from cmake macro.
%cmake -DCMAKE_BUILD_TYPE:STRING=RelWithDebInfo .
%__make VERBOSE=1  %{?_smp_mflags}

%install
%__rm -rf $RPM_BUILD_ROOT
%__make install DESTDIR=$RPM_BUILD_ROOT
# We install document using doc
(cd $RPM_BUILD_ROOT//usr/share/doc/cmake-fedora-0.8.3
    %__rm -rf RELEASE-NOTES.txt AUTHORS README ChangeLog COPYING TODO
)

%clean
%__rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc RELEASE-NOTES.txt AUTHORS README ChangeLog COPYING TODO
%{_bindir}/cmake-fedora-newprj.sh
%{_bindir}/koji-build-scratch.sh
%{_datadir}/cmake/Modules/CMakeVersion.cmake
%{_datadir}/cmake/Modules/DateTimeFormat.cmake
%{_datadir}/cmake/Modules/ManageEnvironment.cmake
%{_datadir}/cmake/Modules/ManageMaintainerTargets.cmake
%{_datadir}/cmake/Modules/ManageMessage.cmake
%{_datadir}/cmake/Modules/ManageRelease.cmake
%{_datadir}/cmake/Modules/ManageReleaseOnFedora.cmake
%{_datadir}/cmake/Modules/ManageSourceVersionControl.cmake
%{_datadir}/cmake/Modules/ManageString.cmake
%{_datadir}/cmake/Modules/ManageTranslation.cmake
%{_datadir}/cmake/Modules/ManageUninstall.cmake
%{_datadir}/cmake/Modules/ManageVariable.cmake
%{_datadir}/cmake/Modules/ManageVersion.cmake
%{_datadir}/cmake/Modules/PackRPM.cmake
%{_datadir}/cmake/Modules/PackSource.cmake
%{_datadir}/cmake/Modules/UseDoxygen.cmake
%{_datadir}/cmake/Modules/UseGConf.cmake
%{_datadir}/cmake/Modules/cmake_uninstall.cmake.in
%{_datadir}/cmake/Templates/fedora
%config %{_sysconfdir}/cmake-fedora.conf

%changelog
* Wed Mar 12 2014 Liu Di <liudidi@gmail.com> - 0.8.3-2
- 更新到

* Wed Dec 05 2012 Liu Di <liudidi@gmail.com> - 0.8.3-2
- 为 Magic 3.0 重建

* Mon Feb 27 2012 Ding-Yi Chen <dchen at redhat.com> - 0.8.3-1
- New command: koji-build-scratch.sh for scratch build on all supported
  releases.
- Release versions are now defined in configuration file for easy
  maintenance.
- RELEASE_ON_FEDORA: support new tags: "fedora" for current fedora,
  and "epel" for current epel.
- Variable Removed:
  FEDORA_NEXT_RELEASE
  FEDORA_NEXT_RELEASE_TAGS
  FEDORA_LATEST_RELEASE
  FEDORA_PREVIOUS_RELEASE

* Tue Sep 20 2011 Ding-Yi Chen <dchen at redhat.com> - 0.8.1-1
- Fixed Bug 738958 - cmake-fedora: remove excessive quotation marks for Precompile definition
- Fixed Bug 733540 - cmake-fedora: "" should be read as empty string
- ManageEnvironment: Now defined cmake_policy won't get overridden.
- ManageString: STRING_UNQUOTE is now merely remove quote marks in the beginning and
    end of string. The string will not be changed otherwise.
- UseUninstall has renamed as ManageUninstall
- ManageMaintainerTargets: Reveal MAINTAINER_UPLOAD_COMMAND
- ManageTranslation: Adopt zanata python client 1.3, arguments are redesigned.
  + Change target: from "translations" to "gmo_files"
  + Add targets: zanata_push, zanata_push_trans, zanata_pull_trans
  + Add argument: ALL_FOR_PUSH, ALL_FOR_PUSH_TRANS and ALL_FOR_PULL
  + Add argument: OPTIONS for passing arguments.
- ManageReleaseOnFedora: Now default to build against candidate repos,
  unless _CANDIDATE_PREFERRED is set to "0".

* Thu Aug 18 2011 Ding-Yi Chen <dchen at redhat.com> - 0.7.994-1
- Fixed Bug 725615 - cmake-fedora: Use UTC for changelog
- Fixed Bug 725617 - cmake-fedora: target 'tag' should stop when tag file exists.
- Module CompileEnv.cmake is obsoleted by ManageEnvironment.cmake
  because it is what the variable actually store.
- Revised ManageTranslation, now zanata.xml.in can be put to either
  CMAKE_SOURCE_DIR or CMAKE_CURRENT_SOURCE_DIR.
- ManageReleaseOnFedora:
  + New Constants: FEDORA_NEXT_RELEASE_TAGS, FEDORA_SUPPORTED_RELEASE_TAGS.
  + Remove NORAWHIDE, as user can use TAGS to achieve the same.
  + Actually mkdir and clone project if the FedPkg directory is missing.
- ManageTranslation:
  + Fixed zanata.xml path problem
  + Fixed zanata related targets.
- New Variable: CMAKE_FEDORA_TMP_DIR for holding cmake-fedora files.
  + ChangeLog temporary files have moved to this directory.

* Fri Jul 08 2011 Ding-Yi Chen <dchen at redhat.com> - 0.7.1-1
- Target release now depends on upload.

* Fri Jul 08 2011 Ding-Yi Chen <dchen at redhat.com> - 0.7.0-1
- Fixed target: after_release_commit.
- Add "INCLUDE(ManageRelease)" in template
  so new project will not get CMake command "MANAGE_RELEASE"
- Corrected TODO.
- Corrected ChangeLog.prev and SPECS/RPM-ChangeLog.prev.
- By default, the CMAKE_INSTALL_PREFIX is set as '/usr'.

* Wed Jul 06 2011 Ding-Yi Chen <dchen at redhat.com> - 0.6.1-1
- Remove f13 from FEDORA_CURRENT_RELEASE_TAGS, as Fedora 13 is end of life.
- ManageMessage: New module.
  + M_MSG: Controllable verbose output
- ManageRelease: New module.
  + MANAGE_RELEASE: Make release by uploading files to hosting services
- Now ManageReleaseOnFedora includes ManageMaintainerTargets
- Modules are shown what they include and included by.
- Now tag depends on koji_scratch_build, while fedpkg_commit master
  (or other primary branch) depends directly on tag.
- MAINTAINER_SETTING_READ_FILE now can either use MAINTAINER_SETTING, or take
  one argument that define maintainer setting file.
- MANAGE_MAINTAINER_TARGETS_UPLOAD no longer require argument hostService,
  It now relies on HOSTING_SERVICES from maintainer setting file.
- Minimum cmake requirement is now raise to 2.6.
- Targets which perform after release now have the prefix "after_release".

* Wed Jul 06 2011 Ding-Yi Chen <dchen at redhat.com> - 0.6.1-1
- Remove f13 from FEDORA_CURRENT_RELEASE_TAGS, as Fedora 13 is end of life.
- ManageMessage: New module.
  + M_MSG: Controllable verbose output
- ManageRelease: New module.
  + MANAGE_RELEASE: Make release by uploading files to hosting services
- Now ManageReleaseOnFedora includes ManageMaintainerTargets
- Modules are shown what they include and included by.
- Now tag depends on koji_scratch_build, while fedpkg_commit master
  (or other primary branch) depends directly on tag.
- MAINTAINER_SETTING_READ_FILE now can either use MAINTAINER_SETTING, or take
  one argument that define maintainer setting file.
- MANAGE_MAINTAINER_TARGETS_UPLOAD no longer require argument hostService,
  It now relies on HOSTING_SERVICES from maintainer setting file.
- Minimum cmake requirement is now raise to 2.6

* Wed Jun 08 2011 Ding-Yi Chen <dchen at redhat.com> - 0.6.0-1
- Fixed Bug 684107 - [cmake-fedora] TAGS in USE_FEDPKG is ineffective.
- ManageTranslation:
  + Renamed from UseGettext
  + New Macro: USE_ZANATA() - Zanata support (experiential).
  + New Macro: USE_GETTEXT() - Gettext support.
    This macro merges GETTEXT_CREATE_POT and GETTEXT_CREATE_TRANSLATIONS,
    to simplified the usage and make the macro names more consistent.
- ManageReleaseOnFedora:
  + New Variable: FEDORA_EPEL_RELEASE_TAGS
- Clean up Modules: No unrelated files under Modules/
- Removed debug messages of:
  CMAKE_MAJOR_VERSION, CMAKE_MINOR_VERSION. CMAKE_PATCH_VERSION,
  _cmake_uninstall_in, _koji_tags, _tags.

* Sun Feb 27 2011 Ding-Yi Chen <dchen at redhat.com> - 0.5.0-1
- Macro: RELEASE_ON_FEDORA added.
- Target: release_on_fedora added.
- Now has more informative error message, when cmake-fedora is not installed.
- Fixed UseUninstall
- Fixed Bug 670079 - [cmake-fedora] target "release"
  will not stop when koji build failed
- Fixed Bug 671063 - [cmake-fedora] target "rpmlint"
  should not depend on "koji_scratch_build"
- Protocol for hosting server should now be specified as "[Hosting]_PROTOCOL".
- Refactoring ManageMaintainerTargets.
- fedpkg and koji build for every tags are revealed.
- Now set rawhide as f16, release dists are f15,f14,f13.
- rpm build process is now refined, no unnecessary build.
- Renamed target push_svc_tag to push_post_release.
- Renamed module UseFedpkg to ManageReleaseOnFedora

* Fri Jan 07 2011 Ding-Yi Chen <dchen at redhat.com> - 0.4.0-1
- New target: release
- New target: install_rpms
- ./Module should precedes /usr/share/cmake/Modules, so
  it always use latest modules.
- Fixed Reading a file that contains '\'.
- Added Macro PACK_RPM_GET_ARCH
- Added target install_rpms for bulk rpms installation.
- Target rpm now uses -bb instead of -ba.
- Target rpm now depends on srpm.
- Source version control logic is split out as ManageSourceVersionControl
- Module UseHostingService is renamed as ManageMaintainerTarget
- Macro USE_HOSTING_SERVICE_READ_SETTING_FILE is renamed as
  MAINTAINER_SETTING_READ_FILE

* Sun Dec 19 2010 Ding-Yi Chen <dchen at redhat.com> - 0.3.3-1
- Fixed: Support for out-of-source build.
- Fixed: Join the next line if ended with back slash '\'.
- ChangeLog: Now generate from "cmake ." directly.
- changelog: target removed. So it won't do unnecessary rebuild.

* Tue Nov 09 2010 Ding-Yi Chen <dchen at redhat.com> - 0.3.2-1
- Fixed: Macro invoked with incorrect arguments for macro named STRING_ESCAPE
  Caused by give and empty string from STRING_TRIM
- Removed: f12 from FEDORA_CURRENT_RELEASE_TAGS

* Mon Nov 08 2010 Ding-Yi Chen <dchen at redhat.com> - 0.3.1-1
- SETTING_FILE_GET_VARIABLES_PATTERN:
  Fixed: unable to use relative path problem.
  Fixed: UNQUOTE and NOESCAPE_SEMICOLON can now used together.

* Wed Nov 03 2010 Ding-Yi Chen <dchen at redhat.com> - 0.3.0-1
- New macro: SETTING_FILE_GET_VARIABLES_PATTERN
- New macro: PACK_SOURCE_FILES
- Fixed: Variable lost in SETTING_FILE_GET_ALL_VARIABLES and
  SETTING_FILE_GET_VARABLE.
- Fixed: Variable values won't apply in SETTING_FILE_GET_ALL_VARIABLES
- UseUninstall finds cmake_uninstall.in in additional paths:
  /usr/share/cmake/Modules and /usr/share/cmake/Modules
- Minor improvements in CMakeLists.txt and project.spec.in templates.

* Wed Oct 20 2010 Ding-Yi Chen <dchen at redhat.com> - 0.2.4-1
- cmake-fedora-newprj.sh: New option "-e" that extract value from specified
  spec or spec.in.
- Now usage is printed instead of junk output when project_name is not given.
- Source code (whatever is packed) and tarball dependency now checked.

* Sat Oct 16 2010 Ding-Yi Chen <dchen at redhat.com> - 0.2.3-1
- Inserted git pull for each fedpkg targets. Reduce the chance of conflict.
- Fixed target: bodhi_new. So it will actually run this command instead of
just showing it.

* Fri Oct 15 2010 Ding-Yi Chen <dchen at redhat.com> - 0.2.2-1
- Add new project building script.
- Build for EL-5, EL-6
- Add el5, el6 build.
- Fixed errors in UseFedpkg.
- Fixed target: tag
- Fixed target: bodhi_new

* Fri Oct 08 2010 Ding-Yi Chen <dchen at redhat.com> - 0.1.4-1
- Fixed error in UseFedpkg.

* Mon Oct 04 2010 Ding-Yi Chen <dchen at redhat.com> - 0.1.2-1
- Removed excess spaces.

* Mon Oct 04 2010 Ding-Yi Chen <dchen at redhat.com> - 0.1.1-1
- Added koji scratch build target.
- Fixed changelog_update.

* Mon Oct 04 2010 Ding-Yi Chen <dchen at redhat.com> - 0.1.0-1
- Initial package.

