Name:           environment-modules
Version:	3.2.10
Release:        5%{?dist}
Summary:        Provides dynamic modification of a user's environment

Group:          System Environment/Base
License:        GPLv2+
URL:            http://modules.sourceforge.net/
Source0:        http://downloads.sourceforge.net/modules/modules-%{version}.tar.bz2
Source1:        modules.sh
Source2:        createmodule.sh
Patch0:         environment-modules-3.2.7-bindir.patch
# Patch to fix segfault in module unload due to Tcl RegExp handling
# https://bugzilla.redhat.com/show_bug.cgi?id=834580
Patch1:         environment-modules-regex.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  tcl-devel, tclx-devel, libX11-devel
BuildRequires:  dejagnu
BuildRequires:  man
#For ps in startup script
Requires:       procps

%description
The Environment Modules package provides for the dynamic modification of
a user's environment via modulefiles.

Each modulefile contains the information needed to configure the shell
for an application. Once the Modules package is initialized, the
environment can be modified on a per-module basis using the module
command which interprets modulefiles. Typically modulefiles instruct
the module command to alter or set shell environment variables such as
PATH, MANPATH, etc. modulefiles may be shared by many users on a system
and users may have their own collection to supplement or replace the
shared modulefiles.

Modules can be loaded and unloaded dynamically and atomically, in an
clean fashion. All popular shells are supported, including bash, ksh,
zsh, sh, csh, tcsh, as well as some scripting languages such as perl.

Modules are useful in managing different versions of applications.
Modules can also be bundled into metamodules that will load an entire
suite of different applications.

NOTE: You will need to get a new shell after installing this package to
have access to the module alias.


%prep
%setup -q -n modules-%{version}
%patch0 -p1 -b .bindir
#%patch1 -p1 -b .regex

%build
export CFLAGS=" $RPM_OPT_FLAGS -DUSE_INTERP_ERRORLINE "
export CXXFLAGS=" $RPM_OPT_FLAGS -DUSE_INTERP_ERRORLINE "
%configure --disable-versioning \
           --prefix=%{_datadir} \
           --exec-prefix=%{_datadir}/Modules \
           --with-man-path=$(manpath) \
           --with-module-path=%{_sysconfdir}/modulefiles
#           --with-debug=42 --with-log-facility-debug=stderr
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
cp -p %SOURCE1 $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/modules.sh
cp -p %SOURCE2 $RPM_BUILD_ROOT%{_datadir}/Modules/bin
ln -s %{_datadir}/Modules/init/csh $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/modules.csh
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/modulefiles
magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%check
make test


%files
%defattr(-,root,root,-)
%doc LICENSE.GPL README TODO
%{_sysconfdir}/modulefiles
%{_sysconfdir}/profile.d/*
%{_bindir}/modulecmd
%dir %{_datadir}/Modules
%{_datadir}/Modules/bin/
%dir %{_datadir}/Modules/init
%{_datadir}/Modules/init/*
%config(noreplace) %{_datadir}/Modules/init/.modulespath
%{_datadir}/Modules/modulefiles
%{_mandir}/man1/module.1.gz
%{_mandir}/man4/modulefile.4.gz


%changelog
* Tue Apr 01 2014 Liu Di <liudidi@gmail.com> - 3.2.10-5
- 更新到 3.2.10

* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 3.2.9c-5
- 为 Magic 3.0 重建

* Fri Aug 24 2012 Orion Poplawski <orion@cora.nwra.com> - 3.2.9c-4
- Add patch to fix segfault from Tcl RexExp handling (bug 834580)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.9c-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.9c-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 29 2011 Orion Poplawski <orion@cora.nwra.com> - 3.2.9c-1
- Update to 3.2.9c (fixes bug 753760)

* Tue Nov 22 2011 Orion Poplawski <orion@cora.nwra.com> - 3.2.9b-2
- Make .modulespath a config file

* Tue Nov 15 2011 Orion Poplawski <orion@cora.nwra.com> - 3.2.9b-1
- Update to 3.2.9b

* Fri Nov 11 2011 Orion Poplawski <orion@cora.nwra.com> - 3.2.9a-2
- Add %%check section

* Fri Nov 11 2011 Orion Poplawski <orion@cora.nwra.com> - 3.2.9a-1
- Update to 3.2.9a
- Drop strcpy patch

* Thu Sep 22 2011 Orion Poplawski <orion@cora.nwra.com> - 3.2.8a-3
- Add patch to fix overlapping strcpy() in Remove_Path, hopefully fixes
  bug 737043

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.8a-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 4 2010 Orion Poplawski <orion@cora.nwra.com> - 3.2.8a-1
- Update to 3.2.8a, changes --with-def-man-path to --with-man-path

* Mon Oct 4 2010 Orion Poplawski <orion@cora.nwra.com> - 3.2.8-1
- Update to 3.2.8
- Drop mandir patch, use --with-def-man-path

* Thu Jan 7 2010 Orion Poplawski <orion@cora.nwra.com> - 3.2.7b-7
- Add patch to set a sane default MANPATH
- Add createmodule.sh utility script for creating modulefiles
 
* Mon Nov 30 2009 Orion Poplawski <orion@cora.nwra.com> - 3.2.7b-6
- Add Requires: propcs (bug #54272)

* Mon Oct 26 2009 Orion Poplawski <orion@cora.nwra.com> - 3.2.7b-5
- Don't assume different shell init scripts exist (bug #530770)

* Fri Oct 23 2009 Orion Poplawski <orion@cora.nwra.com> - 3.2.7b-4
- Don't load bash init script when bash is running as "sh" (bug #529745)

* Mon Oct 19 2009 Orion Poplawski <orion@cora.nwra.com> - 3.2.7b-3
- Support different flavors of "sh" (bug #529493)

* Wed Sep 23 2009 Orion Poplawski <orion@cora.nwra.com> - 3.2.7b-2
- Add patch to fix modulecmd path in init files

* Wed Sep 23 2009 Orion Poplawski <orion@cora.nwra.com> - 3.2.7b-1
- Update to 3.2.7b

* Mon Sep 21 2009 Orion Poplawski <orion@cora.nwra.com> - 3.2.7-1
- Update to 3.2.7, fixes bug #524475
- Drop versioning patch fixed upstream

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Sep 3 2008 - Orion Poplawski <orion@cora.nwra.com> - 3.2.6-6
- Change %%patch -> %%patch0

* Fri Mar 14 2008 - Orion Poplawski <orion@cora.nwra.com> - 3.2.6-5
- Add BR libX11-devel so modulecmd can handle X resources

* Wed Mar  5 2008 - Orion Poplawski <orion@cora.nwra.com> - 3.2.6-4
- Add patch to fix extraneous version path entry properly
- Use --with-module-path to point to /etc/modulefiles for local modules,
  this also fixes bug #436041

* Sat Feb  9 2008 - Orion Poplawski <orion@cora.nwra.com> - 3.2.6-3
- Rebuild for gcc 3.4

* Thu Jan 03 2008 - Alex Lancaster <alexlan at fedoraproject.org> - 3.2.6-2
- Rebuild for new Tcl (8.5).

* Fri Nov  2 2007 - Orion Poplawski <orion@cora.nwra.com> - 3.2.6-1
- Update to 3.2.6

* Tue Aug 21 2007 - Orion Poplawski <orion@cora.nwra.com> - 3.2.5-2
- Update license tag to GPLv2

* Fri Feb 16 2007 - Orion Poplawski <orion@cora.nwra.com> - 3.2.5-1
- Update to 3.2.5

* Wed Feb 14 2007 - Orion Poplawski <orion@cora.nwra.com> - 3.2.4-2
- Rebuild for Tcl downgrade

* Fri Feb 09 2007 - Orion Poplawski <orion@cora.nwra.com> - 3.2.4-1
- Update to 3.2.4

* Wed Dec 20 2006 - Orion Poplawski <orion@cora.nwra.com> - 3.2.3-3
- Add --with-version-path to set VERSIONPATH (bug 220260)

* Tue Aug 28 2006 - Orion Poplawski <orion@cora.nwra.com> - 3.2.3-2
- Rebuild for FC6

* Fri Jun  2 2006 - Orion Poplawski <orion@cora.nwra.com> - 3.2.3-1
- Update to 3.2.3

* Fri May  5 2006 - Orion Poplawski <orion@cora.nwra.com> - 3.2.2-1
- Update to 3.2.2

* Fri Mar 24 2006 - Orion Poplawski <orion@cora.nwra.com> - 3.2.1-1
- Update to 3.2.1

* Thu Feb  9 2006 - Orion Poplawski <orion@cora.nwra.com> - 3.2.0p1-1
- Update to 3.2.0p1

* Fri Jan 27 2006 - Orion Poplawski <orion@cora.nwra.com> - 3.2.0-2
- Add profile.d links

* Tue Jan 24 2006 - Orion Poplawski <orion@cora.nwra.com> - 3.2.0-1
- Fedora Extras packaging
