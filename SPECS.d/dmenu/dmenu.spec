Name:           dmenu
Version:        4.5
Release:        10.20140425git%{?dist}
Summary:        Generic menu for X
License:        MIT
URL:            http://tools.suckless.org/dmenu
Source0:        http://dl.suckless.org/tools/%{name}-%{version}.tar.gz
# git format-patch from upstream git repository:
# git://git.suckless.org/dmenu
Patch1:         0016-remove-_POSIX_C_SOURCE-cflag.patch
Patch2:         0017-add-G-escape-keybinding.patch
Patch3:         0018-listen-for-C-S-jm.patch
Patch4:         0019-_POSIX_C_SOURCE-200809L.patch
Patch5:         0020-ignore-prompt-if-it-is-empty-in-addition-to-NULL.patch
Patch6:         0021-dmenu_run-Split-cache-logic-to-dmenu_path-again.patch
Patch7:         0022-applied-multisel-patch-to-mainline.patch
Patch8:         0023-applied-Alex-Sedov-s-Tab-buffer-termination-patch-th.patch
Patch9:         0024-adopted-Alex-Sedov-s-config.h-revival-patch-to-tip.patch
Patch10:        0025-forgot-to-add-config.def.h-thanks-William.patch
Patch11:        0026-accepted-vi-is-exit-approach-suggested-by-Arkaduisz.patch
Patch12:        0027-applied-Martti-K-hne-s-dmenu-monitor-patch.patch
Patch13:        0028-applied-Martin-K-hl-s-inverse-matching-flag-to-stest.patch
BuildRequires:  libX11-devel
BuildRequires:  libXinerama-devel
Requires:       terminus-fonts
# dmenu-4.5 switched to a more generic tool, stest (f17 note)
Obsoletes:      lsx < 0.1-2
Provides:       lsx = 0.1-2

%description
Dynamic menu is a generic menu for X, originally designed for dwm. It manages
huge amounts (up to 10.000 and more) of user defined menu items efficiently.

%prep
%autosetup
# Nuke the silent build.
sed -i -e 's|\t@|\t|' Makefile
# Insert optflags.
sed -i -e 's|-Os|%{optflags}|' config.mk
# No strip for debuginfo, and insert ldflags to enhance the security.
sed -i -e 's|-s ${LIBS}|%{?__global_ldflags} ${LIBS}|' config.mk
# X includedir path fix
sed -i -e 's|X11INC = .*|X11INC = %{_includedir}|' config.mk
# libdir path fix
sed -i -e 's|X11LIB = .*|X11LIB = %{_libdir}|' config.mk

%build
make %{?_smp_mflags}

%install
%make_install PREFIX=%{_prefix}

%files
%doc LICENSE README
%{_bindir}/%{name}*
%{_bindir}/stest
%{_mandir}/man*/%{name}.*
%{_mandir}/man*/stest.*

%changelog
* Thu Oct 29 2015 Liu Di <liudidi@gmail.com> - 4.5-10.20140425git
- 为 Magic 3.0 重建

* Sat Oct 24 2015 Liu Di <liudidi@gmail.com> - 4.5-9.20140425git
- 为 Magic 3.0 重建

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5-8.20140425git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5-7.20140425git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5-6.20140425git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 25 2014 Christopher Meng <rpm@cicku.me> - 4.5-5.20140425git
- Fetch patches from upstream since 4.5 version.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jan 09 2012 Petr Šabata <contyk@redhat.com> - 4.5-1
- 4.5 bump
- Switching from lsx to stest

* Mon Sep 19 2011 Petr Sabata <contyk@redhat.com> - 4.4.1-1
- 4.4.1 bump

* Tue Aug 02 2011 Simon Wesp <cassmodiah@fedoraproject.org> - 4.4-2
- Rebuild against newest dependencies

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 4.4-1
- 4.4 bump
- This version integrates lsx, adding proper obsoletes/provides

* Mon Jun 13 2011 Petr Sabata <contyk@redhat.com> - 4.3.1-2
- dmenu no longer uses sselp at runtime, removing sselp dependency

* Thu May 19 2011 Petr Sabata <psabata@redhat.com> - 4.3.1-1
- 4.3.1 bugfix update

* Thu May 19 2011 Petr Sabata <psabata@redhat.com> - 4.3-1
- 4.3 released today
- Buildroot and defattr cleanup
- Use macros in URL and Source
- Use RPM_OPT_FLAGS in config.mk patch

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Nov 20 2010 Simon Wesp <cassmodiah@fedoraproject.org> - 4.2.1-1
- New upstrem version

* Mon Jun 28 2010 Simon Wesp <cassmodiah@fedoraproject.org> - 4.1.1-1
- New upstrem version

* Sat Dec 12 2009 Simon Wesp <cassmodiah@fedoraproject.org> - 4.0-2
- merged with the spec-file of Jan Blazek

* Thu Oct 15 2009 Simon Wesp <cassmodiah@fedoraproject.org> - 4.0-1
- Initial Package Build
