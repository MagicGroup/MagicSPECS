Summary: PolicyKit integration for the GNOME desktop
Summary(zh_CN.UTF-8): GNOME 桌面的 PolicyKit 集成
Name: polkit-gnome
Version: 0.105
Release: 6%{?dist}
License: LGPLv2+
URL: http://www.freedesktop.org/wiki/Software/PolicyKit
Group: Applications/System
Group(zh_CN.UTF-8): 应用程序/系统
Source0: http://hal.freedesktop.org/releases/%{name}-%{version}.tar.xz

BuildRequires: gtk3-devel
BuildRequires: glib2-devel >= 2.25.11
BuildRequires: polkit-devel >= 0.97-1
BuildRequires: desktop-file-utils
BuildRequires: intltool
BuildRequires: gobject-introspection-devel
BuildRequires: gtk-doc

Obsoletes: PolicyKit-gnome <= 0.10
Provides: PolicyKit-gnome = 0.11
Obsoletes: PolicyKit-gnome-libs <= 0.10
Provides: PolicyKit-gnome-libs = 0.11
Obsoletes: polkit-gnome-devel < 0.102-2
Provides: polkit-gnome-devel = 0.102-2
Obsoletes: polkit-gnome-docs < 0.102-2
Provides: polkit-gnome-docs = 0.102-2

Provides: PolicyKit-authentication-agent

Requires: polkit >= 0.97

%description
polkit-gnome provides an authentication agent for PolicyKit
that matches the look and feel of the GNOME desktop.

%description -l zh_CN.UTF-8
GNOME 桌面的 PolicyKit 集成。

%prep
%setup -q

%build
%configure
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
magic_rpm_clean.sh
%find_lang polkit-gnome-1

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f polkit-gnome-1.lang
%doc COPYING AUTHORS README
%{_libexecdir}/*


%changelog
* Thu Nov 12 2015 Liu Di <liudidi@gmail.com> - 0.105-6
- 为 Magic 3.0 重建

* Sun Nov 01 2015 Liu Di <liudidi@gmail.com> - 0.105-5
- 为 Magic 3.0 重建

* Sat Jul 25 2015 Liu Di <liudidi@gmail.com> - 0.105-4
- 为 Magic 3.0 重建

* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.105-3
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.105-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov  2 2011 Matthias Clasen <mclasen@redhat.com> - 0.105-1
- Update to 0.105

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.104-2
- Rebuilt for glibc bug#747377

* Tue Oct 18 2011 Matthias Clasen <mclasen@redhat.com> - 0.104-1
- Update to 0.104

* Tue Oct 11 2011 Matthias Clasen <mclasen@redhat.com> - 0.103-2
- Try to fix Obsoletes/Provides

* Mon Sep 19 2011 Matthias Clasen <mclasen@redhat.com> - 0.103-1
- Update to 0.103
- Build against gtk3
- Drop no-longer-needed subpackages

* Tue Aug 16 2011 Matthias Clasen <mclasen@redhat.com> - 0.102-1
- Update to 0.102

* Thu Mar 03 2011 David Zeuthen <davidz@redhat.com> - 0.101-1
- New upstream version

* Mon Feb 21 2011 David Zeuthen <davidz@redhat.com> - 0.100-1
- New upstream version
- Note: The auto-start desktop file for the authentication agent is no
  longer shipped with this package. This is now the responsibility of
  each desktop environment.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.97-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 10 2010 Dan Horák <dan[at]danny.cz> - 0.97-7
- Add gtk-doc as BR

* Mon Aug 23 2010 Matthias Clasen <mclasen@redhat.com> - 0.97-6
- Co-own /usr/share/gtk-doc (#604411)

* Wed Aug 18 2010 Matthias Clasen <mclasen@redhat.com> - 0.97-5
- Rebuild to work around bodhi limitations

* Mon Aug 09 2010 David Zeuthen <davidz@redhat.com> - 0.97-4
- Bump polkit req to 0.97 since we have to chainbuild anyway. Sigh.

* Mon Aug 09 2010 David Zeuthen <davidz@redhat.com> - 0.97-3
- Nuke patch that was committed upstream

* Mon Aug 09 2010 David Zeuthen <davidz@redhat.com> - 0.97-2
- Fix up BRs

* Mon Aug 09 2010 David Zeuthen <davidz@redhat.com> - 0.97-1
- Update to 0.97

* Mon Jun 14 2010 Matthias Clasen <mclasen@redhat.com> - 0.96-2
- Use lock icons that exist in current icon theme
- Minor spec file fixes

* Fri Jan 15 2010 David Zeuthen <davidz@redhat.com> - 0.96-1
- Update to release 0.96
- Disable introspection support for the time being

* Tue Jan  5 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.95-2
- Don't autostart in KDE on F13+

* Fri Nov 13 2009 David Zeuthen <davidz@redhat.com> - 0.95-1
- Update to release 0.95
- Drop upstreamed patches

* Wed Oct  7 2009 Matthias Clasen <mclasen@redhat.com> - 0.95.0.git20090913.6
- Prevent the statusicon from eating whitespace

* Mon Sep 14 2009 David Zeuthen <davidz@redhat.com> - 0.95-0.git20090913.5
- add Provides: PolicyKit-authentication-agent to satify what PolicyKit-gnome
  also provided

* Mon Sep 14 2009 David Zeuthen <davidz@redhat.com> - 0.95-0.git20090913.4
- Refine how Obsolete: is used and also add Provides: (thanks Jesse
  Keating and nim-nim)

* Mon Sep 14 2009 David Zeuthen <davidz@redhat.com> - 0.95-0.git20090913.3
- Obsolete old PolicyKit-gnome packages

* Sun Sep 13 2009 David Zeuthen <davidz@redhat.com> - 0.95-0.git20090913.2
- Update BR

* Sun Sep 13 2009 David Zeuthen <davidz@redhat.com> - 0.95-0.git20090913.1
- Update BR

* Sun Sep 13 2009 David Zeuthen <davidz@redhat.com> - 0.95-0.git20090913
- Update to git snapshot
- Turn on GObject introspection

* Wed Sep  2 2009 Matthias Clasen <mclasen@redhat.com> - 0.94-4
- Just remove the OnlyShowIn, it turns out everybody wants this

* Sat Aug 29 2009 Matthias Clasen <mclasen@redhat.com> - 0.94-3
- Require a new enough polkit (#517479)

* Sat Aug 29 2009 Matthias Clasen <mclasen@redhat.com> - 0.94-2
- Show in KDE, too (#519674)

* Wed Aug 12 2009 David Zeuthen <davidz@redhat.com> - 0.94-1
- Update to upstream release 0.94

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.93-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 David Zeuthen <davidz@redhat.com> - 0.93-2
- Rebuild

* Mon Jul 20 2009 David Zeuthen <davidz@redhat.com> - 0.93-1
- Update to 0.93

* Tue Jun  9 2009 Matthias Clasen <mclasen@redhat.com> - 0.9.2-3
- Fix BuildRequires

* Tue Jun 09 2009 David Zeuthen <davidz@redhat.com> - 0.92-2
- Change license to LGPLv2+
- Remove Requires: gnome-session

* Mon Jun 08 2009 David Zeuthen <davidz@redhat.com> - 0.92-1
- Update to 0.92 release

* Wed May 27 2009 David Zeuthen <davidz@redhat.com> - 0.92-0.git20090527
- Update to 0.92 snapshot

* Mon Feb  9 2009 David Zeuthen <davidz@redhat.com> - 0.91-1
- Initial spec file.
