Summary:	Utilities for alternative packaging
Name:		scl-utils
Version:	20140127
Release:	2%{?dist}
License:	GPLv2+
Group:		Applications/File
URL:		https://fedorahosted.org/SoftwareCollections/
Source0:	https://fedorahosted.org/released/scl-utils/%{name}-%{version}.tar.gz
Source1:	macros.scl-filesystem
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Run-time utility for alternative packaging.

%package build
Summary:	RPM build macros for alternative packaging
Group:		Applications/File
Requires:	iso-codes
Requires:	magic-rpm-config

%description build
Essential RPM build macros for alternative packaging.

%prep
%setup -q

%build
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="$RPM_LD_FLAGS"

%install
rm -rf %buildroot
mkdir -p %buildroot%{_sysconfdir}/rpm
mkdir -p %buildroot%{_sysconfdir}/scl/prefixes
pushd %buildroot%{_sysconfdir}/scl
ln -s prefixes conf
popd
mkdir -p %buildroot/opt/rh
install -d -m 755 %buildroot%{_mandir}/man1
make install DESTDIR=%buildroot
cat %SOURCE1 >> %buildroot%{_sysconfdir}/rpm/macros.scl

# remove brp-python-hardlink invocation as it is not present in RHEL5
%if 0%{?rhel} == 5
  sed -i -e '/^.*brp-python-hardlink.*/d' %buildroot%{_sysconfdir}/rpm/macros.scl
%endif

%clean
rm -rf %buildroot

%files
%defattr(-,root,root,-)
%dir /opt/rh
%{_sysconfdir}/scl/conf
%dir %{_sysconfdir}/scl/prefixes
%{_bindir}/scl
%{_bindir}/scl_enabled
%{_bindir}/scl_source
%{_mandir}/man1/*
%{_sysconfdir}/bash_completion.d/scl.bash
%doc LICENSE

%{!?_rpmconfigdir:%global _rpmconfigdir /usr/lib/rpm}
%files build
%defattr(-,root,root,-)
%{_bindir}/sclbuild
%{_sysconfdir}/rpm/macros.scl
%{_rpmconfigdir}/scldeps.sh
%{_rpmconfigdir}/fileattrs/scl.attr
%{_rpmconfigdir}/brp-scl-compress
%{_rpmconfigdir}/brp-scl-python-bytecompile

%changelog
* Sat May 03 2014 Liu Di <liudidi@gmail.com> - 20140127-2
- 为 Magic 3.0 重建

* Mon Jan 27 2014 Jan Zeleny <jzeleny@redhat.com> - 20140127-1
- don't exclude provides from SCLs (#1056183)
- don't generate scl-package(%scl) in macros.scl, it's already
  handled in dependency generator
- add automatic Requires: %scl_runtime to every SCL package (#1054711)

* Wed Jan 08 2014 Jan Zeleny <jzeleny@redhat.com> - 20140108-1
- split _scl_prefix macro in two parts: scl_basedir and scl_vendor (#985233)
- check if temp file is created (#1032666)
- don't split command arguments containing white space (#1032666)
- rename some attr rpm macros to stop confusing rpm (#1023625)

* Thu Oct 17 2013 Jan Zeleny <jzeleny@redhat.com> - 20131017-1
- fixed one issue in scl_source script

* Wed Oct 16 2013 Jan Zeleny <jzeleny@redhat.com> - 20131016-1
- fixed the -- separator behavior

* Wed Oct 09 2013 Jan Zeleny <jzeleny@redhat.com> - 20131015-1
- Correct the %_sharedstatedir and %_root_sharedstatedir macros
- Don't install /%{_lib} when not necessary
- Add LICENSE file
- Add scl_source script
- Don't change directory in %scl_install
- Don't generate provides from sonames in the SCL root
- Add the SCL prefix to virtual provides of SCL-based packages
- Implement "--" as a command separator
- Removed binary file scl from git tracking
- Fixed typo
- Added example wrapper script.

* Mon Aug 26 2013 Jan Zeleny <jzeleny@redhat.com> - 20130529-3
- updated the file list to handle /etc/scl/conf correctly

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130529-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed May 29 2013 Jan Zeleny <jzeleny@redhat.com> - 20130529-1
- changed the upstream tarball location
- update to 20130529

* Fri Feb 01 2013 Jindrich Novy <jnovy@redhat.com> 20121110-2
- add build compatibility fixes

* Wed Dec 19 2012 Jindrich Novy <jnovy@redhat.com> 20121110-1
- introduce sclbuild utility
- fix exporting of env. variables when mutiple collections are
  enabled at the same time
- better bash completion
- fix changelog

* Thu Sep 27 2012 Jindrich Novy <jnovy@redhat.com> 20120927-1
- update to 20120927
- better BUILDROOT processing
- bash completition for scl command
- debuginfo package now has SCL-specific provide
- non-SCL builds are without warning in build log
- improved help

* Thu Aug 09 2012 Jindrich Novy <jnovy@redhat.com> 20120809-1
- update to 20120809
- processes the SCL buildroot correctly now

* Thu Aug 02 2012 Jindrich Novy <jnovy@redhat.com> 20120802-1
- update to 20120802

* Tue Jul 31 2012 Jindrich Novy <jnovy@redhat.com> 20120731-1
- add functionality that allows to list all packages in a collection
- add dependency generators

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120613-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Jindrich Novy <jnovy@redhat.com> 20120613-1
- Requires: iso-codes for basic filesystem in build subpackage
- add scl_require_package() macro to depend on a particular package
  from the collection
- fix filesystem file list
- tighten runtime package dependency via scl_require()
- fix _localstatedir to point to the correct path according to redhat-rpm-config
- thanks to Bohuslav Kabrda for feature proposals/QA/fixes

* Thu May 03 2012 Jindrich Novy <jnovy@redhat.com> 20120503-1
- avoid doublefree corruption when reading commands from stdin

* Sun Apr 22 2012 Jindrich Novy <jnovy@redhat.com> 20120423-1
- keep filesystem macros out of the main sources as
  it is distro-dependent

* Fri Apr 13 2012 Jindrich Novy <jnovy@redhat.com> 20120413-1
- filesystem ownership by meta package
- add man page
- fix memory leak when parsing commands from stdin
- use more descriptive error message if /etc/prefixes is missing

* Wed Feb 29 2012 Jindrich Novy <jnovy@redhat.com> 20120229-1
- do not prepend scl_* prefix to package names
- unify package naming to <SCL>-package-version
- add scl --list functionality to list available SCLs

* Thu Feb 09 2012 Jindrich Novy <jnovy@redhat.com> 20120209-1
- fix minor bugs (#788194)
  - clear temp files
  - handle commands from stdin properly
  - run command even if ran as "scl enable SCL command" from already
    enabled SCL

* Wed Jan 25 2012 Jindrich Novy <jnovy@redhat.com> 20120125-1
- remove dsc macros
- trigger scl-utils-build BR inclusion while using scl macros

* Wed Jan 11 2012 Jindrich Novy <jnovy@redhat.com> 20120111-1
- add "dsc" alias to "scl" utility

* Wed Dec 14 2011 Jindrich Novy <jnovy@redhat.com> 20111214-1
- initial review fixes (#767556)

* Fri Dec  9 2011 Jindrich Novy <jnovy@redhat.com> 20111209-1
- allow to use dsc_* macros and dsc* package naming

* Wed Nov 16 2011 Jindrich Novy <jnovy@redhat.com> 20111116-1
- package is now named scl-utils

* Mon Oct 17 2011 Jindrich Novy <jnovy@redhat.com> 20111017-1
- initial packaging for upstream

* Wed Sep 21 2011 Jindrich Novy <jnovy@redhat.com> 0.1-14
- define %%_defaultdocdir to properly relocate docs into
  a stack
- document a way how to pass command to stack via stdin

* Wed Jun 22 2011 Jindrich Novy <jnovy@redhat.com> 0.1-13
- fix Stack meta config configuration

* Fri Jun 17 2011 Jindrich Novy <jnovy@redhat.com> 0.1-12
- use own Stack path configuration mechanism

* Fri Jun 17 2011 Jindrich Novy <jnovy@redhat.com> 0.1-11
- avoid redefinition of %%_root* macros by multiple
  occurence of %%stack_package
- make the Stack root path configurable

* Tue Jun 14 2011 Jindrich Novy <jnovy@redhat.com> 0.1-10
- stack utility allows to read command from stdin

* Mon Jun 13 2011 Jindrich Novy <jnovy@redhat.com> 0.1-9
- introduce stack enablement tracking
- introduce "stack_enabled" helper utility to let a stack
  application figure out which stacks are actually enabled
- disallow running stacks recursively

* Mon Jun 13 2011 Jindrich Novy <jnovy@redhat.com> 0.1-8
- stack utility returns executed commands' exit value

* Fri Jun 10 2011 Jindrich Novy <jnovy@redhat.com> 0.1-7
- fix possible segfault in the stack utility

* Fri Jun 10 2011 Jindrich Novy <jnovy@redhat.com> 0.1-6
- %%stack_name: initial part of stack prefix and name of
  meta package providing scriptlets
- %%stack_prefix: stack namespacing part to be prepended to
  original non-stack package name, can be used for Provides
  namespacing as well
- %%stack_runtime: run-time package name providing scriptlets
- %%stack_require: macro to define dependency to other stacks

* Thu Jun 09 2011 Jindrich Novy <jnovy@redhat.com> 0.1-5
- split the package into two - runtime and build part
- decrease verbosity when enabling a stack

* Wed Jun 08 2011 Jindrich Novy <jnovy@redhat.com> 0.1-4
- prepend stack package with stack_* to prevent namespace
  conflicts with core packages

* Thu Jun 02 2011 Jindrich Novy <jnovy@redhat.com> 0.1-3
- introduce metapackage concept

* Wed Jun 01 2011 Jindrich Novy <jnovy@redhat.com> 0.1-2
- modify macros so that they don't change preamble tags

* Sun May 08 2011 Jindrich Novy <jnovy@redhat.com> 0.1-1
- initial packaging
