
Name:    kwebkitpart
Summary: A KPart based on QtWebKit
Version: 1.3.0
Release: 2%{?dist}

License: LGPLv2+
URL:     https://projects.kde.org/projects/extragear/base/kwebkitpart
# git clone git://anongit.kde.org/kwebkitpart
# git archive --prefix=kwebkitpart-%{version}/ v1.3.0 | xz > ../kwebkitpart-%{version}.tar.xz
Source0: kwebkitpart-%{version}.tar.xz

## upstream patches
Patch101: 0001-Removed-unnecessary-debug-statements.patch
Patch102: 0002-Do-not-crash-when-QWebHitTestResult-frame-returns-NU.patch
Patch103: 0003-Added-the-applet-tag-to-the-ondemand-plugin-loader-l.patch
Patch104: 0004-Fix-search-shortcuts.patch
Patch105: 0005-Removed-no-longer-necessary-namespace-use.patch
Patch106: 0006-On-view-frame-or-document-source-open-the-actual-fil.patch

BuildRequires: gettext
BuildRequires: git-core
BuildRequires: kdelibs4-devel >= 4.8.3
BuildRequires: pkgconfig(QtWebKit)

%{?_kde4_version:Requires: kdelibs4%{?_isa} >= %{_kde4_version}}
Obsoletes: kwebkitpart-devel < 1.1
Obsoletes: webkitpart < 0.0.6
Provides:  webkitpart = %{version}-%{release}

%description
KWebKitPart is a web browser component for KDE (KPart)
based on (Qt)WebKit. You can use it for example for
browsing the web in Konqueror.


%prep
%setup -q

git init
if [ -z "$GIT_COMMITTER_NAME" ]; then
git config user.email "kde@lists.fedoraproject.org"
git config user.name "Fedora KDE SIG"
fi
git add .
git commit -a -q -m "%{version} baseline."

# Apply all the patches
git am -p1 %{patches} < /dev/null

%if 0%{?fedora} < 18
# revert commit that gives kwebkitpart higher priority than khtml
# https://projects.kde.org/projects/extragear/base/kwebkitpart/repository/revisions/49ea6284cc46e8a24d04a564d4c8680ebd2b0f74
sed -i.InitialPreference \
  -e 's|^InitialPreference=.*|-InitialPreference=9|g' \
  src/kwebkitpart.desktop
%endif


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=$RPM_BUILD_ROOT -C %{_target_platform}
magic_rpm_clean.sh

%post
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null ||:

%posttrans
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null ||:

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null ||:
  gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null ||:
fi

%files
%doc README COPYING.LIB TODO
%{_kde4_libdir}/kde4/kwebkitpart.so
%{_kde4_iconsdir}/hicolor/*/apps/webkit.*
%{_kde4_datadir}/kde4/services/kwebkitpart.desktop
%{_kde4_appsdir}/kwebkitpart/


%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.3.0-2
- 为 Magic 3.0 重建

* Thu Oct 04 2012 Rex Dieter <rdieter@fedoraproject.org> 1.3.0-1
- generate tarball from v1.3.0 tag
- include a few post v1.3.0 patches
- default web browsing KPart unexpectedly changed to WebKitPart (#862601)
- BR: pkgconfig(QtWebKit)
- .spec cosmetics

* Thu Jul 26 2012 Rex Dieter <rdieter@fedoraproject.org> 1.3-0.1.20120726git
- 1.3 branch 20120726 snapshot

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-0.5.20120715
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jul 15 2012 Rex Dieter <rdieter@fedoraproject.org> 1.2-0.4.20120715
- 20120715 snapshot (master branch, 1.2 is broken atm)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-0.3.20111030
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 30 2011 Alexey Kurov <nucleo@fedoraproject.org> - 1.2-0.2.20111030
- kwebkitpart 1.2 20111030 snapshot

* Thu Jul 21 2011 Alexey Kurov <nucleo@fedoraproject.org> - 1.2-0.1.20110720
- kwebkitpart 1.2 20110720 snapshot
- drop kwebkitpart-devel

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 0.9.6-2
- Rebuilt for gcc bug 634757

* Sun Jul 25 2010 Alexey Kurov <nucleo@fedoraproject.org> - 0.9.6-1
- kwebkitpart 0.9.6

* Sat May 08 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.0.5-0.4.svn1088283
- revert BR: qt4-webkit-devel, rebuild against newer kdelibs-devel that includes it

* Sat May 08 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.0.5-0.3.svn1088283
- BR: qt4-webkit-devel

* Wed Mar 24 2010 Alexey Kurov <nucleo@fedoraproject.org> - 0.0.5-0.2.svn1088283
- drop webkitkde package
- removed Requires: webkitkde from webkitpart

* Wed Feb 10 2010 Alexey Kurov <nucleo@fedoraproject.org> - 0.0.5-0.1.svn1088283
- update to kwebkitpart snapshot from kdereview

* Wed Feb 10 2010 Alexey Kurov <nucleo@fedoraproject.org> - 0.0.4-0.3.svn1079265
- build only for kdelibs >= 4.4.0

* Sun Jan 24 2010 Alexey Kurov <nucleo@fedoraproject.org> - 0.0.4-0.2.svn1079265
- svn 1079265. Fixed the library and header file names.

* Sat Jan 23 2010 Alexey Kurov <nucleo@fedoraproject.org> - 0.0.4-0.1.svn1078162
- svn 1078162

* Thu Dec  3 2009 Alexey Kurov <nucleo@fedoraproject.org> - 0.0.3-0.2.svn1057318
- svn 1057318

* Tue Nov 24 2009 Alexey Kurov <nucleo@fedoraproject.org> - 0.0.3-0.1.svn1049337
- version changed to 0.0.3 (kdewebkit moved to kdelibs 4.4)
- drop webkitkde-devel subpackage for KDE 4.4

* Wed Nov 18 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.0.2-0.2.20091109svn
- rebuild (qt-4.6.0-rc1, fc13+)

* Mon Nov  9 2009 Alexey Kurov <nucleo@fedoraproject.org> - 0.0.2-0.1.20091109svn
- version changed to 0.0.2 for new API

* Mon Nov  9 2009 Alexey Kurov <nucleo@fedoraproject.org> - 0.0.1-0.6.20091109svn
- removed kdelauncher from CMakeLists because it not installs

* Mon Nov  9 2009 Alexey Kurov <nucleo@fedoraproject.org> - 0.0.1-0.5.20091109svn
- snapshot 1046552 with new API

* Sun Sep 27 2009 Alexey Kurov <nucleo@fedoraproject.org> - 0.0.1-0.2.20090924svn
- webkitpart should owns kpartplugins in webkitpart apps dir

* Thu Sep 24 2009 Alexey Kurov <nucleo@fedoraproject.org> - 0.0.1-0.1.20090924svn
- Initial RPM release
