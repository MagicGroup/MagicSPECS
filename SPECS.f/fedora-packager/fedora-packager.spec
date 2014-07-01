%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

Name:           fedora-packager
Version:        0.5.10.4
Release:        2%{?dist}
Summary:        Tools for setting up a fedora maintainer environment

Group:          Applications/Productivity
License:        GPLv2+
URL:            https://fedorahosted.org/fedora-packager
Source0:        https://fedorahosted.org/releases/f/e/fedora-packager/fedora-packager-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel
Requires:       koji bodhi-client packagedb-cli
Requires:       rpm-build rpmdevtools rpmlint
Requires:       mock curl openssh-clients
Requires:       pyOpenSSL
Requires:       redhat-rpm-config
Requires:       fedpkg >= 1.0
Requires:       fedora-cert = %{version}-%{release}
Requires:       ykpers

BuildArch:      noarch

%description
Set of utilities useful for a fedora packager in setting up their environment.


%package     -n fedora-cert
Summary:        Fedora certificate tool and python library
Group:          Applications/Databases
Requires:       pyOpenSSL
Requires:       python-pycurl
%if 0%{?rhel} == 5 || 0%{?rhel} == 4
Requires:       python-kitchen
%endif

%description -n fedora-cert
Provides fedora-cert and the fedora_cert python library


%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libexecdir}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING TODO AUTHORS ChangeLog
%{_bindir}/*
%{_sbindir}/*
%dir %{_sysconfdir}/koji
%config(noreplace) %{_sysconfdir}/koji/*
%exclude %{_bindir}/fedora-cert

%files -n fedora-cert
%defattr(-,root,root,-)
%doc COPYING TODO AUTHORS ChangeLog
%{_bindir}/fedora-cert
%{python_sitelib}/fedora_cert


%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.10.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Mar 23 2014 Nick Bebout <nb@fedoraproject.org> - 0.5.10.4-1
- fix fedora-burn-yubikey script to add -oserial-api-visible

* Tue Mar 18 2014 Nick Bebout <nb@fedoraproject.org> - 0.5.10.3-1
- fix fedora-burn-yubikey script to work with slot 2

* Thu Dec 05 2013 Denis Gilmore <dennis@ausil.us> - 0.5.10.2-1
- update to 0.5.10.2
- drop sparc support

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 03 2013 Adam Jackson <ajax@redhat.com> 0.5.10.1-2
- Requires: packagedb-cli (which also pulls in python-bugzilla)

* Mon Dec 03 2012 Nick Bebout <nb@fedoraproject.org> - 0.5.10.1-1
- fix fedora-burn-yubikey to allow specifying what slot to use

* Fri Aug 03 2012 Dennis Gilmore <dennis@ausil.us> - 0.5.10.0-1
- fix up secondary arch configs for newer koji
- clean up message for browser import

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.9.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 08 2011 Jesse Keating <jkeating@redhat.com> - 0.5.9.6-1
- Install secondary-arch files correctly

* Mon Nov 07 2011 Jesse Keating <jkeating@redhat.com> - 0.5.9.5-1
- Move fedpkg to it's own package, no longer part of fedora-packager

* Fri Oct 28 2011 Jesse Keating <jkeating@redhat.com> - 0.5.9.4-1
- Overload curl stuff (jkeating)
- Hardcode fedpkg version requires (jkeating)
- Fix up changelog date (jkeating)

* Thu Oct 27 2011 Jesse Keating <jkeating@redhat.com> - 0.5.9.3-1
- Use the new plugin setup with rpkg
- Change fedpkg version number to 1.0

* Sat Aug 27 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.5.9.2-2
- Fix operating URL of fedoradev-pkgowners (BZ #575517).

* Sun May 22 2011 Jesse Keating <jkeating@redhat.com> - 0.5.9.2-1
- Strip the .py off of fixbranches (jkeating)
- Unconditionally check for new branch style (jkeating)
- Stop setting push.default (#705468) (jkeating)
- Make sure packages are built before lint (#702893) (jkeating)
- Except more build submission errors (#702235) (jkeating)
- Move the fixbranches.py script out of the $PATH (#698646) (jkeating)
- fedpkg: Support branch completion on non-default remotes (tmz)
- fedpkg: Update bash completion for new branch names (tmz)
- Fix retiring a package with a provided message (#701626) (jkeating)
- add arm specific and s390 specific packages so they get sent to the right
  place (dennis)
- initial go at using consistent targets across all targets dist-rawhide is
  still used for master branch (dennis)
- only pass in a target arch to local builds when specified on the command line
  some arches notably x86, arm and sparc dont build for the base arch you end
  up with .i386 .arm or .sparc rpms when you really want something else
  (dennis)

* Thu Apr 14 2011 Jesse Keating <jkeating@redhat.com> - 0.5.9.0-1
- Add a check for new-style branches (jkeating)
- Add a force option (jkeating)
- Add ability to check status of conversion (jkeating)
- Add a dry-run option (jkeating)
- Add a client side script to fix branch data (jkeating)

* Sat Apr 09 2011 Jesse Keating <jkeating@redhat.com> - 0.5.8.1-1
- Man page comment syntax fix. (ville.skytta)
- Make sure the bodhi.template file got written out (#683602) (jkeating)
- Wrap the diff in a try (#681789) (jkeating)
- Don't try to upload directories. (#689947) (jkeating)
- Fix tag-request (#684418) (jkeating)

* Fri Mar 04 2011 Jesse Keating <jkeating@redhat.com> - 0.5.7.0-1
- If chain has sets, handle them right (#679126) (jkeating)
- Fix "fedpkg help" command (make it work again) (#681242) (hun)
- Always generate a new srpm (#681359) (jkeating)
- Fix up uses of path (ticket #96) (jkeating)
- Clean up hardcoded "origin" (ticket #95) (jkeating)
- Fix obvious error in definition of curl command (pebolle)

* Wed Feb 23 2011 Jesse Keating <jkeating@redhat.com> - 0.5.6.0-1
- Fix improper use of strip() (jkeating)
- Improve the way we detect branch data (jkeating)
- Fix clone to work with old/new branch styles (jkeating)
- Add new and old support to switch_branches (jkeating)
- Update the regexes used for finding branches (jkeating)
- Don't use temporary editor files for spec (#677121) (jkeating)
- fedpkg requires rpm-build (#676973) (jkeating)
- Don't error out just from stderr from rpm (jkeating)

* Wed Feb 09 2011 Jesse Keating <jkeating@redhat.com> - 0.5.5.0-1
- Re-add 'lint' command hookup into argparse magic (hun)
- Catch errors parsing spec to get name. (#676383) (jkeating)

* Wed Feb 09 2011 Jesse Keating <jkeating@redhat.com> - 0.5.4.0-1
- Re-arrange verify-files and slight fixups (jkeating)
- Add "fedpkg verify-files" command (hun)
- Provide feedback about new-ticket. (ticket 91) (jkeating)
- Add the new pull options to bash completion (jkeating)
- Add a --rebase and --no-rebase option to pull (jkeating)
- Update the documentation for a lot of commands (jkeating)
- Handle working from a non-existent path (#675398) (jkeating)
- Fix an traceback when failing to watch a build. (jkeating)
- Handle arches argument for scratch builds (#675285) (jkeating)
- Trim the "- " out of clogs.  (#675892) (jkeating)
- Exit with an error when appropriate (jkeating)
- Add build time man page generator (hun)
- Add help text for global --user option (hun)
- Move argparse setup into parse_cmdline function (hun)
- Require python-hashlib on EL5 and 4 (jkeating)
- Catch a traceback when trying to build from local branch (jkeating)

* Mon Jan 31 2011 Jesse Keating <jkeating@redhat.com> 0.5.3.0-1
- Catch the case where there is no branch merge point (#622592) (jkeating)
- Fix whitespace (jkeating)
- Add an argument to override the "distribution" (jkeating)
- upload to lookaside cache tgz files (dennis)
- Handle traceback if koji is down or unreachable. (jkeating)
- If we don't have a remote branch, query koji (#619979) (jkeating)
- Add a method to create an anonymous koji session (jkeating)
- Make sure we have sources for mockbuild (#665555) (jwboyer) (jkeating)
- Revert "Make sure we have an srpm when doing a mockbuild (#665555)" (jkeating)
- Regenerate the srpm if spec file is newer (ticket #84) (jkeating)
- Improve cert failure message (Ticket 90) (jkeating)
- Get package name from the specfile. (Ticket 75) (jkeating)
- Handle anonymous clones in clone_with_dirs. (#660183) (ricky)
- Make sure we have an srpm when doing a mockbuild (#665555) (jkeating)
- Catch all errors from watching tasks. (#670305) (jkeating)
- Fix a traceback when koji goes offline (#668889) (jkeating)
- Fix traceback with lint (ticket 89) (jkeating)

* Wed Jan 05 2011 Dennis Gilmore <dennis@ausil.us> - 0.5.2.0-1
- new release see ChangeLog

* Tue Aug 24 2010 Jesse Keating <jkeating@redhat.com> - 0.5.1.4-1
- Fix setting push.default when cloning with dirs
- Remove build --test option in bash completion

* Mon Aug 23 2010 Jesse Keating <jkeating@redhat.com> - 0.5.1.3-1
- Error check the update call.  #625679
- Use the correct remote when listing revs
- Add the bash completion file
- make fedora-cvs only do anonymous chackouts since cvs is read only now.
- re-fix dist defines.
- Short cut the failure on repeated builds
- Allow passing srpms to the build command
- clone: set repo's push.default to tracking
- pull the username from fedora_cert to pass to bodhi
- Catch double ^c's from build.  RHBZ #620465
- Fix up chain building
- Add missing process call for non-pipe no tty.

* Thu Aug 12 2010 Dennis Gilmore <dennis@asuil.us> - 0.5.1.2-1
- fix rh bz 619733 619879 619935 620254 620465 620595 620648
- 620653 620750 621148 621808 622291 622716

* Fri Jul 30 2010 Dennis Gilmore <dennis@ausil.us> -0.5.1.0-2
- split fedpkg out on its own

* Thu Jul 29 2010 Dennis Gilmore <dennis@ausil.us> - 0.5.1.0-1
- wrap fedora-cert in try except 
- fedpkg fixes
- require python-kitchen on EL-4 and 5

* Wed Jul 28 2010 Dennis Gilmore <dennis@ausil.us> - 0.5.0.1-1
- Fix checking for unpushed changes on a branch

* Wed Jul 28 2010 Dennis Gilmore <dennis@ausil.us> - 0.5.0-1
- update to 0.5.0 with the switch to dist-git

* Thu Jul 08 2010 Dennis Gilmore <dennis@ausil.us> - 0.4.2.2-1
- new release with lost of fedpkg fixes

* Mon Jun 14 2010 Dennis Gilmore <dennis@ausil.us> - 0.4.2.1-1
- set devel for F-14
- point builds to koji.stg
- correctly create a git url for koji

* Tue Mar 23 2010 Dennis Gilmore <dennis@ausil.us> - 0.4.2-1
- update to 0.4.2
- adds missing fedora_cert. in fedora-packager-setup bz#573941
- Require python-argparse for fedpkg bz#574206
- Require make and openssh-clients bz#542209
- Patch to make cvs checkouts more robust bz#569954

* Wed Mar 03 2010 Dennis Gilmore <dennis@ausil.us> - 0.4.1-1
- update to 0.4.1 
- adds a missing "import sys" from fedora-cert bz#570370
- Require GitPython for fedpkg

* Fri Feb 26 2010 Dennis Gilmore <dennis@ausil.us> - 0.4.0-1
- update to 0.4.0 adds fedpkg 
- make a fedora_cert python library 
- add basic date check for certs 

* Tue Aug 04 2009 Jesse Keating <jkeating@redhat.com> - 0.3.8-1
- Add fedora-hosted and require offtrac

* Thu Jul 30 2009 Dennis Gilmore <dennis@ausil.us> - 0.3.7-1
- define user_cert in fedora-cvs before refrencing it 

* Tue Jul 28 2009 Dennis Gilmore <dennis@ausil.us> - 0.3.6-1
- use anon checkout when a fedora cert doesnt exist bz#514108
- quote arguments passed onto rpmbuild bz#513269

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Dennis Gilmore <dennis@ausil.us> - 0.3.5-1
- add new rpmbuild-md5 script to build old style hash srpms
- it is a wrapper around rpmbuild

* Mon Jul  6 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 0.3.4-3
- add Requires: redhat-rpm-config to be sure fedora packagers are using all available macros

* Wed Jun 24 2009 Dennis Gilmore <dennis@ausil.us> - 0.3.4-2
- minor bump

* Mon Jun 22 2009 Dennis Gilmore <dennis@ausil.us> - 0.3.4-1
- update to 0.3.4 
- bugfix release with some new scripts

* Mon Mar 02 2009 Dennis Gilmore <dennis@ausil.us> - 0.3.3-1
- update to 0.3.3

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Aug 18 2008 Dennis Gilmore <dennis@ausil.us> - 0.3.1-1
- update to 0.3.1 fedora-cvs allows anonymous checkout
- fix some Requires  add cvs curl and wget 

* Sun Mar 30 2008 Dennis Gilmore <dennis@ausil.us> - 0.3.0-1
- update to 0.3.0 fedora-cvs uses pyOpenSSL to work out username
- remove Requires on RCS's for fedora-hosted
- rename fedora-packager-setup.sh to fedora-packager-setup

* Fri Feb 22 2008 Dennis Gilmore <dennis@ausil.us> - 0.2.0-1
- new upstream release
- update for fas2
- fedora-cvs  can now check out multiple modules at once
- only require git-core

* Mon Dec 03 2007 Dennis Gilmore <dennis@ausil.us> - 0.1.1-1
- fix typo in description 
- update to 0.1.1  fixes typo in fedora-cvs

* Sun Nov 11 2007 Dennis Gilmore <dennis@ausil.us> - 0.1-1
- initial build
