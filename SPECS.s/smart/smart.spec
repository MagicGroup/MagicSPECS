# This is not defined on Fedora buildsystems
%{!?python_sitearch:%global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%bcond_with ksmarttray
%bcond_without pygtk
%bcond_with qt
%bcond_without qt4

Summary: Next generation package handling tool
Summary(zh_CN.UTF-8): 下一代包处理工具
Name: smart
Version: 1.4.1
Release: 4%{?dist}
License: GPLv2+
Group: Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
URL: http://labix.org/smart/
Source0: http://labix.org/download/smart/%{name}-%{version}.tar.bz2
Source1: smart.console
Source2: smart.pam
Source3: smart.desktop
Source4: distro.py
Source5: ksmarttray.desktop
Source6: smart-qt.desktop
# http://bazaar.launchpad.net/%7Esmartpm/smart/qt/diff/885
Patch0: 885.diff
Patch1: https://bugs.launchpad.net/smart/+bug/592503/+attachment/1423240/+files/smart-gtk-progress-nothread.diff
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: python-devel >= 2.3
BuildRequires: desktop-file-utils
BuildRequires: gettext
%if %{with ksmarttray}
BuildRequires: autoconf, automake, gcc-c++
BuildRequires: libXt-devel, libXext-devel
BuildRequires: tdelibs-devel
BuildRequires: zlib-devel
%endif
#Requires: python-abi = %(python -c "import sys ; print sys.version[:3]")
Requires: rpm-python >= 4.4
%{!?with_pygtk:Requires: usermode}
Requires: smart-config

%description
Smart Package Manager is a next generation package handling tool.

%description -l zh_CN.UTF-8
下一代包处理工具。

%package update
Summary: Allows execution of 'smart update' by normal users (suid)
Summary(zh_CN.UTF-8): 允许普通用户执行 'smart update'
Group: Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
Requires: smart = %{version}-%{release}

%description update
Allows execution of 'smart update' by normal users through a
special suid command.

%description update -l zh_CN.UTF-8
允许普通用户执行 'smart update'。

%if %{with pygtk}
%package gui
Summary: Graphical user interface for the smart package manager
Summary(zh_CN.UTF-8): smart 包管理器的图形用户界面
Group: Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
Requires: smart = %{version}-%{release}
Requires: pygtk2 >= 2.4
Requires: usermode
Provides: smart-gtk = %{version}-%{release}
%if %{with qt}
Requires: PyQt
%endif
%if %{with qt4}
Requires: PyQt4
%endif

%description gui
Graphical user interface for the smart package manager.
%description gui -l zh_CN.UTF-8
smart 包管理器的图形用户界面。
%endif

%if %{with ksmarttray}
%package -n ksmarttray
Summary: KDE tray program for watching updates with Smart Package Manager
Summary(zh_CN.UTF-8): smart 包管理器用来监视更新的 KDE 系统栏程序 
Group: Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
Requires: %{_bindir}/kdesu
Requires: smart-update = %{version}-%{release}
Requires: smart-gui = %{version}-%{release}

%description -n ksmarttray
KDE tray program for watching updates with Smart Package Manager.
%description -n ksmarttray -l zh_CN.UTF-8
smart 包管理器用来监视更新的 KDE 系统栏程序。
%endif

%prep
%setup -q
%patch0 -p0 -b .eventscallback
#%patch1 -p0 -b .gtknothread
# /usr/lib is hardcoded 
perl -pi -e's,/usr/lib/,%{_libdir}/,' smart/const.py
install -p -m 644 %{SOURCE2} .
# Detect whether the system is using pam_stack
if test -f /%{_lib}/security/pam_stack.so \
   && ! grep "Deprecated pam_stack module" /%{_lib}/security/pam_stack.so \
      2>&1 > /dev/null; then
  perl -pi -e's,include(\s*)(.*),required\1pam_stack.so service=\2,' smart.pam
  touch -r %{SOURCE2} smart.pam
fi

%build
CFLAGS="%{optflags}"
export CFLAGS
python setup.py build

%if %{with ksmarttray}
# ksmarttray
pushd contrib/ksmarttray
make -f admin/Makefile.common
%configure --disable-rpath --disable-dependency-tracking
make
popd
%endif

# smart-update
make -C contrib/smart-update

%install
rm -rf %{buildroot}
python setup.py install -O1 --root=%{buildroot}

mkdir -p %{buildroot}%{_libdir}/smart/plugins
mkdir -p %{buildroot}%{_sysconfdir}/smart/channels
mkdir -p %{buildroot}%{_localstatedir}/lib/smart{/packages,/channels}

%if %{with ksmarttray}
# ksmarttray
make -C contrib/ksmarttray install DESTDIR=%{buildroot} \
  iconsdir=%{_datadir}/icons/hicolor/48x48/apps
desktop-file-install --vendor=""             \
  --dir %{buildroot}%{_datadir}/applications \
  %{SOURCE5}
%endif

# usermode support
ln -sf consolehelper %{buildroot}%{_bindir}/smart-root

mkdir -p %{buildroot}/etc/security/console.apps
mkdir -p %{buildroot}/etc/pam.d
install -p -m 644 %{SOURCE1} %{buildroot}/etc/security/console.apps/smart-root
install -p -m 644 smart.pam %{buildroot}/etc/pam.d/smart-root

# smart-update
install -p -m 4755 contrib/smart-update/smart-update %{buildroot}%{_bindir}

mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install --vendor=""             \
  --dir %{buildroot}%{_datadir}/applications \
  %{SOURCE3}

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/48x48/apps
install -p -m 644 smart/interfaces/images/smart.png \
  %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/smart.png

# distro.py and distro.d support
install -p -m 644 %{SOURCE4} %{buildroot}%{_libdir}/smart/
mkdir -p %{buildroot}%{_sysconfdir}/smart/distro.d
magic_rpm_clean.sh
%find_lang %{name}

# Create a list w/o smart/interfaces/{gtk,qt} to avoid warning of duplicate
# in the %files section (otherwise including all and %excluding works,
# too

%if ! %{with qt}
rm -rf %{buildroot}%{python_sitearch}/smart/interfaces/qt
%endif 

%if ! %{with qt4}
rm -rf %{buildroot}%{python_sitearch}/smart/interfaces/qt4
%endif

echo "%%defattr(-,root,root,-)" > %{name}.fileslist
find %{buildroot}%{python_sitearch}/smart* -type d \
  | grep -v %{python_sitearch}/smart/interfaces/gtk \
  | grep -v %{python_sitearch}/smart/interfaces/qt \
  | grep -v %{python_sitearch}/smart/interfaces/qt4 \
  | sed -e's,%{buildroot},%%dir ,' \
  >> %{name}.fileslist
find %{buildroot}%{python_sitearch}/smart* \! -type d \
  | grep -v %{python_sitearch}/smart/interfaces/gtk \
  | grep -v %{python_sitearch}/smart/interfaces/qt \
  | grep -v %{python_sitearch}/smart/interfaces/qt4 \
  | sed -e's,%{buildroot},,' \
  >> %{name}.fileslist

# %files does not take two -f arguments
cat %{name}.lang >> %{name}.fileslist

%clean
rm -rf %{buildroot}

%files -f %{name}.fileslist
%defattr(-,root,root,-)
%doc HACKING README LICENSE TODO IDEAS
%{_bindir}/smart
%{_libdir}/smart
%{_sysconfdir}/smart
%{_localstatedir}/lib/smart
%{_mandir}/man8/smart.8*

%files update
%defattr(-,root,root,-)
%{_bindir}/smart-update

%if %{with pygtk}
%files gui
%defattr(-,root,root,-)
%{python_sitearch}/smart/interfaces/gtk
%if %{with qt}
%{python_sitearch}/smart/interfaces/qt
%endif
%if %{with qt4}
%{python_sitearch}/smart/interfaces/qt4
%endif
%{_datadir}/applications/smart.desktop
%{_datadir}/icons/hicolor/48x48/apps/smart.png
%else
%exclude %{python_sitearch}/smart/interfaces/gtk
%exclude %{python_sitearch}/smart/interfaces/qt
%exclude %{_datadir}/applications/smart.desktop
%exclude %{_datadir}/icons/hicolor/48x48/apps/smart.png
%endif

%{_bindir}/smart-root
%config %{_sysconfdir}/security/console.apps/smart-root
%config %{_sysconfdir}/pam.d/smart-root

%if %{with ksmarttray}
%files -n ksmarttray
%defattr(-,root,root,-)
%{_bindir}/ksmarttray
%{_datadir}/apps/ksmarttray
%{_datadir}/applications/ksmarttray.desktop
%{_datadir}/icons/hicolor/48x48/apps/ksmarttray.png
%endif

%changelog
* Fri Nov 13 2015 Liu Di <liudidi@gmail.com> - 1.4.1-4
- 为 Magic 3.0 重建

* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 1.4.1-3
- 为 Magic 3.0 重建

* Mon Sep 28 2015 Liu Di <liudidi@gmail.com> - 1.4.1-2
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.3.1-69
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-68
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-67
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov  3 2010 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.3.1-66
- Update to 1.3.1.
- Apply fixes for bug #592503 (launchpad) (John Bray).

* Sun Feb 14 2010 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.3-65
- Update to 1.3.

* Thu Apr 16 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.2-64
- Fix premature returns in sha256 patch.

* Wed Apr 15 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.2-62
- Fix sha256 and mdclean patches.

* Sun Mar 22 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.2-60
- Update to 1.2.

* Sat Feb 14 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.1-59.0.1
- launchpad changed the from/to rev order in patches, patch now
  properly recreated.

* Sat Feb 14 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.1-59
- Add some more fixes from the bugfix branch.
- Fixes Fedora bug #476808 (getPathList on newer rpms not working
  properly making the content pane apearing empty).
- Fixes unerased accumulated old repomd metadata bug.

* Sun Dec 21 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.1-58
- Use bugfix branch, remove already included patches.

* Sat Dec 13 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.1-57
- Fix rpm loop reordering.

* Sun Oct  5 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.1-56
- Update to 1.1.

* Sat Sep 13 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.0-55
- Fix bad smart.pam commit.

* Wed Aug 27 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.0-54
- omit (broken) BR: qt-devel (Rex Dieter).
- fix comment typo (Ville Skyttä).
- Configure ksmarttray with dependency tracking disabled (Ville Skyttä).

* Sun Aug 24 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.0-53
- Rebase patch to 1.0 to avoid fuzz=0 rejection on recent rpm.

* Fri Aug 15 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.0-52
- Update to 1.0.
- Remove automake version patch.

* Sun Oct  7 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.52-50
- Update to 0.52.
- Fix pam stack type detection.

* Sat Sep 22 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.51-49
- 0.51; autofs, ccache, and autotools (partially) patches addressed upstream.

* Sat Sep  8 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.50-48
- KSmartTray desktop entry fixes.
- License: GPLv2+

* Thu Aug  2 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.50-47
- Add kernel-tuxonice series support.

* Sun Jun  3 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.50-46
- Autodetect pam_stack module at build time.

* Mon Feb  5 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.50-45
- Adjust checks for autotools.

* Mon Jan 22 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.50-44
- Add ccache fix from svn trunk.

* Sun Jan 21 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.50-43
- gettext is BR'd outside of ksmarttray.

* Thu Jan 18 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.50-42
- Update to 0.50.

* Fri Dec  8 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.50-41_rc1
- Update to 0.50rc1.

* Sat Nov 25 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.42-40
- Start preparing virtual provides for upcoming qt gui.

* Sat Nov 25 2006 Ville Skyttä <ville.skytta at iki.fi>
- Flag -xen and -PAE kernels as multi-version.
- Update desktop entry categories and icon installation paths.
- Avoid lib64 RPATHs in ksmarttray, fix menu icon.

* Sat Sep 30 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.42-39
- Fix the autofs5 patch.

* Sat Sep 16 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.42-38
- Un%%ghost pyo files.

* Sat Sep  2 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.42-37
- Add ksmarttray.desktop from ensc.
- Add missing dependency from ksmarttray on smart-gui.
- Ignore new autofs5 solaris-like NIS lookup syntax.

* Wed Aug  9 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.42-36
- Make smart-update suid.

* Mon Aug  7 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.42-35
- Add ksmarttray dependency to kdesu.

* Sat Aug  5 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.42-34
- Merge back ksmarttray package.

* Mon Jun 26 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.42-33
- Update to 0.42.
- Remove unneeded patched that have been applied upstream.

* Thu Apr 20 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.41-31
- Add virtual smart-config dependency (#175630 comment 13).

* Tue Apr 11 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.41-30
- Move the disttag to the Release: tag.

* Mon Apr 10 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.41-29
- Fix typos in distro.py, there were %% missing.
- /usr/bin/smart-root should had been %%{_bindir}/smart-root ...
- Make dependent on fedora-package-config-smart.

* Sun Apr  2 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.41-28
- Move usermode support to the gui package.
- Add cluster/gfs *-kernel variants.

* Fri Mar 31 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.41-27
- Sync with specfile from Ville Skyttä <ville.skytta at iki.fi>
- Add empty-description patch (upstream issue 64).
- Update multi-version to include more kernel-* variants.
- Add distro.d support.
- Make owner of %%{_sysconfdir}/smart and %%{_localstatedir}/lib/smart{,/packages,/channels}.

* Wed Dec 21 2005 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.41-26
- Update to 0.41.

* Tue Dec 13 2005 Axel Thimm <Axel.Thimm@ATrpms.net> - 0.40-23
- Adapted to Fedora Extras guidelines for submission.

* Sun Oct  9 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.40.

* Thu Sep 15 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.39.

* Fri Aug 19 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.37.

* Sat Jun 18 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.35.

* Fri Jun 10 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.35.

* Fri Apr  1 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.30.2.

* Fri Mar 25 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.30.

* Wed Mar 16 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.29.2.

* Sat Mar  5 2005 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.29.1.

* Wed Dec 29 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Merge smart and smart-gui src.rpm back together again.
  (all dependencies resolved for all supported platforms)

* Mon Dec 13 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Split out smart-gui and ksmarttray to manage build dependencies better.

* Wed Dec  8 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.28.

* Sun Dec  5 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 0.27.1

* Fri Dec  3 2004 Axel Thimm <Axel.Thimm@ATrpms.net>
- Initial specfile from Guilherme Manika <guilherme@zorked.net>.
- Some reordering and cleanups.
- Remove binary rpmmodule.so lib.
- Split the gui into a separate package, so the non-gui packages have
  lower requirements.
