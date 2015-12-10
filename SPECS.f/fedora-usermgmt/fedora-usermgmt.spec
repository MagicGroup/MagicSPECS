%global pkgdatadir	%_datadir/%name
%global confdir		%_sysconfdir/fedora/usermgmt
%global alternatives	/usr/sbin/update-alternatives


Summary:	Fedora tools for user management
Name:		fedora-usermgmt
Version:	0.11
Release:	5%{?dist}

License:	GPLv2
BuildArch:	noarch
Group:		Applications/System
URL:		http://fedoraproject.org/wiki/PackageUserCreation
Requires(pre):	%name-core = %version-%release
Requires(pre):	instance(fedora-usermgmt)
Requires(pre):	setup(fedora-usermgmt)
BuildRoot:	%_tmppath/%name-%version-%release-root


%package core
Summary:	Core utilities for the fedora-usermgmt
Group:		Applications/System
Source0:	fedora-usermgmt-wrapper
Source1:	fedora-usermgmt-README
Requires:	%name = %version-%release
Requires:	util-linux-ng coreutils


%package default-fedora-setup
Summary:	Default values for baseuid/basegid
Group:		System Environment/Base
Provides:	setup(fedora-usermgmt)
Provides:	flavor(fedora-usermgmt-setup) = default
Conflicts:	flavor(fedora-usermgmt-setup) < default
Conflicts:	flavor(fedora-usermgmt-setup) > default
Source2:	fedora-usermgmt-baseid
Provides:	%name-setup = %version-%release
Obsoletes:	%name-setup < %version-%release


%package shadow-utils
Summary:	shadow-utils customization for fedora-usermgmt
Group:		Applications/System
Source10:	fedora-usermgmt-groupadd
Source11:	fedora-usermgmt-useradd
Source20:	fedora-usermgmt-groupadd.legacy
Source21:	fedora-usermgmt-useradd.legacy
Provides:	instance(fedora-usermgmt)
Requires:	%name = %version-%release
Requires(pre):		%confdir
Requires(postun):	%confdir
Requires(post):		%alternatives
Requires(preun):	%alternatives
Requires:		shadow-utils


%package devel
Summary:	Enhancements for fedora-usermgmt
Group:		Development/System
Source30:	macros.fedora-usermgmt
Conflicts:	%name < %version-%release
Conflicts:	%name > %version-%release
Requires(pre):		%_sysconfdir/rpm
Requires(postun):	%_sysconfdir/rpm


%description
This package provides wrapper around the useradd/-del and groupadd/-del
programs to allow predictable uids/gids.


%description core
This package provides wrapper around the useradd/-del and groupadd/-del
programs to allow predictable uids/gids.


%description devel
This package provides wrapper around the useradd/-del and groupadd/-del
programs to allow predictable uids/gids.


%description default-fedora-setup
This package contains default values for the base of relative UIDs. It
is designed to be overridden by local customizations; you should create
a package with

| Provides:	setup(fedora-usermgmt)
| Provides:	flavor(fedora-usermgmt-setup) = <one-word-description>

put it into your installation tree, remove the fedora-usermgmt-setup
package from there and update the package metainformation (e.g. with
genhdlist, yum-arch, or apt's genbasedir). A separate repository in
combination with apt pinning might be a solution also.


%description shadow-utils
This package provides the customization of fedora-usermgmt for the
traditional shadow-utils.

WARNING: The attribute "predictable" from "predicatable user-creation"
is turned off by default. It can be enabled by executing

  %alternatives --set %name %confdir/scripts.shadow-utils

as root.


%prep
%setup -q -T -c

%__install -p -m644 %SOURCE1 README


%install
rm -rf $RPM_BUILD_ROOT

%__install -d -m755 $RPM_BUILD_ROOT{%pkgdatadir,%confdir,%_sbindir}

## The base package
%__install -p -m755 %SOURCE0 ${RPM_BUILD_ROOT}%pkgdatadir/wrapper
%__install -p -m644 %SOURCE2 ${RPM_BUILD_ROOT}%confdir/baseuid
%__install -p -m644 %SOURCE2 ${RPM_BUILD_ROOT}%confdir/basegid
for i in {user,group}{del,add}; do
	ln -s %pkgdatadir/wrapper ${RPM_BUILD_ROOT}%_sbindir/fedora-$i
done

## The -shadow-utils installation
%__install -d -m755 ${RPM_BUILD_ROOT}%confdir/scripts.{shadow-utils,legacy}
%__install -p -m755 %SOURCE10 ${RPM_BUILD_ROOT}%confdir/scripts.shadow-utils/groupadd
%__install -p -m755 %SOURCE11 ${RPM_BUILD_ROOT}%confdir/scripts.shadow-utils/useradd

%__install -p -m755 %SOURCE20 ${RPM_BUILD_ROOT}%confdir/scripts.legacy/groupadd
%__install -p -m755 %SOURCE21 ${RPM_BUILD_ROOT}%confdir/scripts.legacy/useradd


## The -devel installation
%__install -d -m755           ${RPM_BUILD_ROOT}%_sysconfdir/rpm
%__install -p -m444 %SOURCE30 ${RPM_BUILD_ROOT}%_sysconfdir/rpm/

magic_rpm_clean.sh

%post shadow-utils
%alternatives --install %confdir/scripts %name %confdir/scripts.legacy 60
%alternatives --install %confdir/scripts %name %confdir/scripts.shadow-utils 50


%preun shadow-utils
test "$1" != 0 || %alternatives --remove %name %confdir/scripts.shadow-utils
test "$1" != 0 || %alternatives --remove %name %confdir/scripts.legacy


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README


%files core
%defattr(-,root,root,-)
%dir %_sysconfdir/fedora
%dir %confdir
%pkgdatadir
%_sbindir/*


%files default-fedora-setup
%defattr(-,root,root,-)
%config(noreplace) %confdir/base*


%files shadow-utils
%defattr(-,root,root,-)
%dir    %confdir/scripts.*
%config %confdir/scripts.*/*


%files devel
%defattr(-,root,root,-)
# do not add %config here; rpm does not ignore the generated
# *.rpmsave/rpmnew files
%_sysconfdir/rpm/macros.*


%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 0.11-5
- 为 Magic 3.0 重建

* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 0.11-4
- 为 Magic 3.0 重建

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 0.11-3
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-1406
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Mar  3 2010 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.11-1405
- obey packaging rules and made user/groupdel noops
- added sanity checks for proper baseuid/basegid setup

* Mon Nov 23 2009 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.10-1300
- require coreutils + util-linux-ng (#540352)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jul 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.10-2
- fix license tag

* Wed Jun 20 2007 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.10-1
- added basic checks that CLI is used correctly

* Wed Apr 25 2007 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.9-2
- fixed version in the Provides/Obsoletes of -default-fedora-setup (bz
  #237457)

* Thu Mar  8 2007 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.9-1
- fixed and updated the documentation; especially, added the '-r'
  option to the fedora-useradd example and mentioned the wiki page.

* Fri Sep 15 2006 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.8.91-1
- make 'id ...' succeed everytime in the wrapper
- append a '%%nil' in a new line to %%FE_USERADD_REQ

* Thu Apr 27 2006 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.8.90-2
- moved most content of the base package and used directories into a
  -core subpackage; this avoids dependencies loops.
- renamed -setup into the much longer -default-fedora-setup; because
  yum's depsolver is not very smart (and choses packages with smallest
  name) it might is more difficult to provide a custom -setup package
  else
- added -devel subpackages with a /etc/rpm/macros.fedora-usermgmt file

* Sat Feb 18 2006 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.8-2
- added the %%dist release-tag

* Sat Dec 10 2005 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0.8-1
- fixed URL metadata (bz #172758)
- execute 'nscd -i ...' before and after creating users/groups; this
  should workaround nscd caching problems
- minor cleanups and logging enhancements in the wrapper script

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sat Mar 20 2004 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0:0.7-0.fdr.2
- applied patch from https://bugzilla.fedora.us/show_bug.cgi?id=701#c10
  I should not defer such things but apply them immediatly...

* Sat Mar 20 2004 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0:0.7-0.fdr.1
- added some '(Pre)' modifiers to ensure correct installation when a
  package has 'Requires: fedora-usermgmt'
- removed the '%%dir %%confdir' from the main-package, it causes apt
  to fail because of dependency loops; this is not really correct
  since -setup (which owns %%confdir) is a virtual package and other
  instances might missing it
- split the double Requires(...,...): statements; see
  https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=118773
- added support for logging: when /etc/fedora/usermgmt/log exists, every
  output of the commands will be redirected into this file. Usually it
  is not a regular file but a symlink somewhere into /var/log

* Sat Nov  8 2003 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0:0.6-0.fdr.1
- removed duplicate '--help' handling in useradd script
- own /etc/fedora by the -setup subpackage, and require this dir in the
  main-package. This is a temporary hack to avoid orphaned directories
  and related problems; final solution will be that /etc/fedora is
  owned by a filesystem-like basepackage.

* Sun Nov  2 2003 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0:0.5-0.fdr.1
- added basic sanity checks and '--help' to wrapper-scripts
- tied -shadow-utils to main-package
- use %%_sysconfdir instead of /etc
- fixed typos in README (thanks to Michael Schwendt)

* Wed Sep 24 2003 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0:0.4-0.fdr.1
- added -setup subpackage to allow customization of baseuid/gid at
  installation-time

* Fri Sep 12 2003 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0:0.2-0.fdr.91
- moved the skin-scripts into /etc/fedora/usermgmt/scripts.$SKIN
- disable the new, predictable behavior by default
- use 'alternatives' concept

* Fri Sep 12 2003 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0:0.2-0.fdr.1
- fixed *del cases
- renamed spec-file to fedora-usermgmt.spec
- updated doc

* Fri Sep 12 2003 Enrico Scholz <enrico.scholz@informatik.tu-chemnitz.de> - 0:0.1-1
- Initial build.
