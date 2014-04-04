%global spectemplatedir %{_sysconfdir}/rpmdevtools/
%global ftcgtemplatedir %{_datadir}/fontconfig/templates/
%global rpmmacrodir     %{_sysconfdir}/rpm/

Name:    fontpackages
Version: 1.44
Release: 5%{?dist}
Summary: Common directory and macro definitions used by font packages
Summary(zh_CN.UTF-8): 字体包使用的通用目录和宏定义

Group:     Development/System
Group(zh_CN.UTF): 开发/系统
# Mostly means the scriptlets inserted via this package do not change the
# license of the packages they're inserted in
License:   LGPLv3+
URL:       http://fedoraproject.org/wiki/fontpackages
Source0:   http://fedorahosted.org/releases/f/o/%{name}/%{name}-%{version}.tar.xz

BuildArch: noarch


%description
This package contains the basic directory layout, spec templates, rpm macros
and other materials used to create font packages.

%description -l zh_CN.UTF-8
这个包包含了创建字体包使用的基本目录结构，spec 模板，rpm 宏和其它资料。

%package filesystem
Summary: Directories used by font packages
Summary(zh_CN.UTF-8): 字体包使用的目录
License: Public Domain

%description filesystem
This package contains the basic directory layout used by font packages,
including the correct permissions for the directories.

%description filesystem -l zh_CN.UTF-8
字体包使用的基本目录结构。

%package devel
Summary: Templates and macros used to create font packages
Summary(zh_CN.UTF-8): %{name} 的开发包
Requires: rpmdevtools, %{name}-filesystem = %{version}-%{release}
Requires: fontconfig

%description devel
This package contains spec templates, rpm macros and other materials used to
create font packages.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%package tools
Summary: Tools used to check fonts and font packages
Summary(zh_CN.UTF-8): 检查字体和字体包的工具

Requires: fontconfig, fontforge
Requires: curl, make, mutt
Requires: rpmlint, yum-utils

%description tools
This package contains tools used to check fonts and font packages

%description tools -l zh_CN.UTF-8
检查字体和字体包的工具。

%prep
%setup -q


%build

for file in bin/repo-font-audit bin/compare-repo-font-audit ; do
sed -i "s|^DATADIR\([[:space:]]*\)\?=\(.*\)$|DATADIR=%{_datadir}/%{name}|g" \
  $file
done

%install
rm -fr %{buildroot}

# Pull macros out of macros.fonts and emulate them during install
for dir in fontbasedir        fontconfig_masterdir \
           fontconfig_confdir fontconfig_templatedir ; do
  export _${dir}=$(rpm --eval $(%{__grep} -E "^%_${dir}\b" \
    rpm/macros.fonts | %{__awk} '{ print $2 }'))
done

install -m 0755 -d %{buildroot}${_fontbasedir} \
                   %{buildroot}${_fontconfig_masterdir} \
                   %{buildroot}${_fontconfig_confdir} \
                   %{buildroot}${_fontconfig_templatedir} \
                   %{buildroot}%{spectemplatedir} \
                   %{buildroot}%{rpmmacrodir} \
                   %{buildroot}%{_datadir}/fontconfig/templates \
                   %{buildroot}/%_datadir/%{name} \
                   %{buildroot}%{_bindir}
install -m 0644 -p spec-templates/*.spec       %{buildroot}%{spectemplatedir}
install -m 0644 -p fontconfig-templates/*      %{buildroot}%{ftcgtemplatedir}
install -m 0644 -p rpm/macros*                 %{buildroot}%{rpmmacrodir}
install -m 0644 -p private/repo-font-audit.mk  %{buildroot}/%{_datadir}/%{name}
install -m 0755 -p private/core-fonts-report \
                   private/font-links-report \
                   private/fonts-report \
                   private/process-fc-query \
                   private/test-info           %{buildroot}/%{_datadir}/%{name}
install -m 0755 -p bin/*                       %{buildroot}%{_bindir}

cat <<EOF > %{name}-%{version}.files
%defattr(0644,root,root,0755)
%dir ${_fontbasedir}
%dir ${_fontconfig_masterdir}
%dir ${_fontconfig_confdir}
%dir ${_fontconfig_templatedir}
EOF
magic_rpm_clean.sh

%clean
rm -fr %{buildroot}


%files filesystem -f %{name}-%{version}.files
%defattr(0644,root,root,0755)
%dir %{_datadir}/fontconfig

%files devel
%defattr(0644,root,root,0755)
%doc license.txt readme.txt
%config(noreplace) %{spectemplatedir}/*.spec
%config(noreplace) %{rpmmacrodir}/macros*
%dir %{ftcgtemplatedir}
%{ftcgtemplatedir}/*conf
%{ftcgtemplatedir}/*txt

%files tools
%defattr(0644,root,root,0755)
%doc license.txt readme.txt
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/repo-font-audit.mk
%defattr(0755,root,root,0755)
%{_datadir}/%{name}/core-fonts-report
%{_datadir}/%{name}/font-links-report
%{_datadir}/%{name}/fonts-report
%{_datadir}/%{name}/process-fc-query
%{_datadir}/%{name}/test-info
%{_bindir}/*

%changelog
* Thu Dec 06 2012 Liu Di <liudidi@gmail.com> - 1.44-5
- 为 Magic 3.0 重建

* Fri Nov 23 2012 Liu Di <liudidi@gmail.com> - 1.44-4
- 为 Magic 3.0 重建

* Thu Nov 24 2011 Liu Di <liudidi@gmail.com> - 1.44-3
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.44-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jun 13 2010 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.44-1
— Cleanup release

* Fri May 28 2010 Akira TAGOH <tagoh@redhat.com>
- 1.42-2
— Get rid of binding="same" from l10n-font-template.conf (#578015)

* Sat Feb 13 2010 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.42-1
— Update mailing list references

* Tue Dec 01 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.41-1
— Bugfix release

* Sat Nov 28 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.40-1
— Bugfix release

* Mon Nov 23 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.35-1

* Sun Nov 22 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.34-1
— compare-repo-font-audit: make output more comprehensive

* Sat Nov 21 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.33-1
— repo-font-audit: add ancilliary script to compare the results of two
  different runs
- 1.32-1
— repo-font-audit: add test for core fonts direct use
— repo-font-audit: replace font naming tests by a more comprehensive one
  (in a separate utility)
— repo-font-audit: add fedora packager detection
— repo-font-audit: parallelize (at the cost of more filesystem space use)
— repo-font-audit: misc output and reliability fixes

* Sun Nov 1 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.31-2
— add yum-utils to deps
- 1.31-1
— Rework repo-font-audit messages based on packager feedback

* Thu Oct 29 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.30-1
— Bugfix release

* Tue Oct 27 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.29-1
— Split out tools as repo-font-audit requirements grow

* Mon Oct 19 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.28-1
— Rework repo-font-audit to also generate individual packager nagmails

* Mon Sep 28 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.27-1
— Brownpaper bag release ×2

* Sun Sep 27 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.26-1
— Brownpaper bag release
- 1.25-1
– Add short test summary to repo-font-audit

* Sat Sep 26 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.24-1
– improve repo-font-audit (make WWS check more accurate, support file://
  local repositories…)

* Sun Sep 13 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.23-1
— cleanups + add merging/remapping templates

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- 1.22-2
— Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jun 20 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.22-1
– workaround rpm eating end-of-line after %%_font_pkg calls
– add script to audit font sanity of yum repositories

* Tue Jun 2 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.21-1
— try to handle more corner naming cases in lua macro – expect some fallout
  if your spec uses weird naming

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- 1.20-2
— Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.20-1
— global-ization

* Mon Feb 16 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.19-3
— remove workaround and explicit version checks
- 1.19-2
— workaround the fact koji is not ready yet
- 1.19-1
— Add a fontconfig dep to -devel so font autoprovides work (bz#485702)
— Drop duplicated group declarations, rpm has been fixed (bz#470714)
— Add partial templates for fonts subpackages of non-font source packages
— Make them noarch (http://fedoraproject.org/wiki/Features/NoarchSubpackages)

* Thu Feb 5 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.18-1
✓ Panu wants autoprovides in rpm proper, drop it
✓ Guidelines people are ok with multiple ownership of directories, make the
  fonts macro auto-own the directory font files are put into

* Sat Jan 31 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.17-1
⁇ Tweak and complete documentation
☤ Merge the autoprovides stuff and try to make it actually work

* Tue Jan 27 2009 Richard Hughes <rhughes@redhat.com>
- 1.16-2
- Add fontconfig.prov and macros.fontconfig so that we can automatically
  generate font provides for packages at build time.
  This lets us do some cool things with PackageKit in the future.

* Wed Jan 22 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.16-1

* Thu Jan 15 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.15-1
➜ lua-ize the main macro

* Wed Jan 14 2009 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.14-1
➽ Update for subpackage naming changes requested by FPC

* Mon Dec 22 2008 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.13-1
⟃ Add another directory to avoid depending on unowned stuff
❤ use it to put the fontconfig examples in a better place

* Sun Dec 21 2008 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.12-2
⌂ Change homepage

* Fri Dec 19 2008 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.12-1
☺ Add another macro to allow building fontconfig without cycling

* Wed Dec 10 2008 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.11-1
☺ Add actual fedorahosted references

* Sun Nov 23 2008 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.10-1
☺ renamed to “fontpackages”

* Fri Nov 14 2008 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.9-1
☺ fix and complete fontconfig doc
- 1.8-1
☺ simplify multi spec template: codify general case
- 1.7-1
☺ split fontconfig template documentation is separate files
- 1.6-1
☺ simplify spec templates
- 1.5-1
☺ use ".conf" extension for fontconfig templates
- 1.4-1
☺ small multi spec template fix

* Wed Nov 12 2008 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.3-1
☺ remove trailing slashes in directory macros

* Tue Nov 11 2008 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.2-1
☺ add fontconfig templates
☺ fix a few typos

* Mon Nov 10 2008 Nicolas Mailhot <nim at fedoraproject dot org>
- 1.0-1
☺ initial release
