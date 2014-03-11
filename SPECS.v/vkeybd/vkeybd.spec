Summary:      Virtual MIDI keyboard
Name:         vkeybd
Version:      0.1.17a
Release:      14%{?dist}
License:      GPLv2+
Group:        Applications/Multimedia
URL:          http://www.alsa-project.org/~iwai/alsa.html
Source0:      http://www.alsa-project.org/~iwai/vkeybd-0.1.17a.tar.bz2
Source1:      vkeybd.png
Source2:      vkeybd.desktop
Patch0:       vkeybd-lash.patch
Patch1:       vkeybd-CFLAGS.patch
Patch2:       vkeybd-lash-2.patch
Patch3:       vkeybd-no-OSS.patch
Patch4:	      vkeybd-tcl8.5.patch
BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: tk-devel >= 1:8.5, tk-devel < 1:8.6
BuildRequires: lash-devel

BuildRequires: desktop-file-utils

Requires: tk >= 1:8.5, tk > 1:8.5, lash
Requires: hicolor-icon-theme

%description
This is a virtual keyboard for AWE, MIDI and ALSA drivers.
It's a simple fake of a MIDI keyboard on X-windows system.
Enjoy a music with your mouse and "computer" keyboard :-)

%prep
%setup -q -n vkeybd
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0

%build
make %{?_smp_mflags} USE_LADCCA=1 TCL_VERSION=8.5 PREFIX=%{_prefix}

%install
rm -rf $RPM_BUILD_ROOT
make USE_LADCCA=1 PREFIX=%{_prefix} DESTDIR=$RPM_BUILD_ROOT install
make USE_LADCCA=1 PREFIX=%{_prefix} DESTDIR=$RPM_BUILD_ROOT install-man
chmod 644 $RPM_BUILD_ROOT/%{_mandir}/man1/*
chmod 755 $RPM_BUILD_ROOT/%{_datadir}/vkeybd/vkeybd.tcl

mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/64x64/apps
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/64x64/apps/vkeybd.png

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install --vendor fedora            \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --add-category X-Fedora                       \
  %{SOURCE2}

%clean
rm -rf $RPM_BUILD_ROOT

%post
# update icon themes
touch --no-create %{_datadir}/icons/hicolor || :
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :

%postun
# update icon themes
touch --no-create %{_datadir}/icons/hicolor || :
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :

%files
%defattr(-,root,root,-)
%doc README ChangeLog
%{_bindir}/vkeybd
%{_bindir}/sftovkb
%{_datadir}/vkeybd/
%{_mandir}/man1/*
%{_datadir}/applications/*%{name}.desktop
%{_datadir}/icons/hicolor/64x64/apps/vkeybd.png

%changelog
* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.17a-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.17a-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.17a-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 23 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 0.1.17a-11
- Update desktop file according to F-12 FedoraStudio feature

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.17a-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.17a-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.1.17a-8
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.1.17a-7
- Autorebuild for GCC 4.3

* Sat Jan 05 2008 Marcela Maslanova <mmaslano@redhat.com> 0.1.17a-6
- Upgrade to tcl8.5. 

* Mon Oct 07 2007 Anthony Green <green@redhat.com> 0.1.17a-5
- Add -no-OSS patch.

* Mon Oct 07 2007 Anthony Green <green@redhat.com> 0.1.17a-4
- Rebuild for new lash.

* Mon Feb 19 2007 Anthony Green <green@redhat.com> 0.1.17a-3
- Track tcl/tk in rawhide.  Now using 1:8.4.

* Thu Feb 01 2007 Anthony Green <green@redhat.com> 0.1.17a-2
- Update tcl/tk dependency to 8.5.

* Thu Oct 19 2006 Anthony Green <green@redhat.com> 0.1.17a-1
- Update sources.
- Remove jack-audio-connection-kit dependency, which is implied by
  lash dependency.

* Mon Sep 25 2006 Anthony Green <green@redhat.com> 0.1.17-8
- Tweak vkeybd.desktop file.
- Package ChangeLog.
- Clean up %%files.
- Move Categories to .desktop file.
- More LADCCA to LASH patching.
- Fix man page permissions.

* Tue Sep 19 2006 Anthony Green <green@redhat.com> 0.1.17-7
- Remove Require(post,postun) for gtk2, as per the packaging
  guidelines.

* Tue Sep 19 2006 Anthony Green <green@redhat.com> 0.1.17-6
- Remove my COPYING file.
- Don't use update-desktop-database.
- Clean up BuildRequires.
- Install the icon in the hicolor tree.
- Require hicolor-icon-theme.
- Don't Require tcl, since tk does that.
- Collar tk version requirements.
- Make vkeybd.tcl executable.
- Require(post,postun) gtk2 for gtk-update-icon-cache.

* Thu Jun  1 2006 Anthony Green <green@redhat.com> 0.1.17-5
- Add dist tag to Release.
- Build with _smp_mflags.
- Add GPL license file (COPYING).

* Tue Apr 25 2006 Anthony Green <green@redhat.com> 0.1.17-4
- Add Fernando Lopez-Lezcano's icon and related changes.
- Clean up macro usage.

* Tue Apr 25 2006 Anthony Green <green@redhat.com> 0.1.17-3
- Build with RPM_OPT_FLAGS with vkeybd-CFLAGS.patch.

* Sat Apr 22 2006 Anthony Green <green@redhat.com> 0.1.17-2
- Build for Fedora Extras.
- Port from ladcca to lash.
- Update description.

* Mon Dec 27 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.1.17-1
- updated to 0.1.17
- spec file cleanup
* Mon May 10 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 
- added buildrequires, detect tcl version
* Tue Feb 24 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.1.15-1
- updated to 0.1.15
* Sat Jul 26 2003 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.1.13a-1
- updated to 0.1.13a
- added menu entries
* Mon Dec 30 2002 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.1.12-1
- Initial build.
