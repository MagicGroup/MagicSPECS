Name:           mousepad
Version:        0.3.0
Release:        0.1.20120827git88aba4%{?dist}
Summary:        Mousepad - A simple text editor for Xfce

Group:          Applications/Editors
License:        GPLv2+
URL:            http://xfce.org/
#Source0:        http://www.xfce.org/archive/xfce-4.6.0/src/mousepad-%{version}.tar.bz2
Source0:        http://git.xfce.org/apps/mousepad/snapshot/mousepad-88aba4e1f5272ea686cb34c5d6e349ef152d4701.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: libxfce4util-devel
BuildRequires: perl(XML::Parser)
BuildRequires: gettext intltool
BuildRequires: desktop-file-utils
BuildRequires: xfce4-dev-tools autoconf libtool 
BuildRequires: gtksourceview2-devel dbus-glib-devel glib2-devel
BuildRequires: exo-devel

%description
Mousepad is a text editor for Xfce based on Leafpad. The initial reason for
Mousepad was to provide printing support, which would have been difficult
for Leafpad for various reasons.

Although some features are under development, currently Mousepad has following
features:

    * Complete support for UTF-8 text
    * Cut/Copy/Paste and Select All text
    * Search and Replace
    * Font selecton
    * Word Wrap
    * Character coding selection
    * Auto character coding detection (UTF-8 and some codesets)
    * Manual codeset setting
    * Infinite Undo/Redo by word
    * Auto Indent
    * Multi-line Indent
    * Display line numbers
    * Drag and Drop
    * Printing

%prep
%setup -q -n mousepad-88aba4e1f5272ea686cb34c5d6e349ef152d4701


%build
xdt-autogen
%configure --enable-maintainer-mode
make 


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

rm -f ${RPM_BUILD_ROOT}%{_datadir}/applications/mousepad.desktop

desktop-file-install                                            \
        --dir ${RPM_BUILD_ROOT}%{_datadir}/applications         \
        Mousepad.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%post
update-desktop-database &> /dev/null ||:

%postun
update-desktop-database &> /dev/null ||:

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS* README NEWS* TODO COPYING THANKS
%{_bindir}/mousepad 
%{_datadir}/applications/Mousepad.desktop
%{_datadir}/icons/hicolor/*/*/*
%{_libdir}/xfce4/mousepad
%{_datadir}/doc/Mousepad

%changelog
* Mon Sep 03 2012 Kevin Fenzi <kevin@scrye.com> 0.3.0-0.1
- Update to pre-release git snapshot of 0.3.0

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.16-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 04 2012 Kevin Fenzi <kevin@scrye.com> - 0.2.16-7
- Rebuild for Xfce 4.10

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.2.16-5
- Rebuild for new libpng

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 01 2010 Kevin Fenzi <kevin@tummy.com> - 0.2.16-3
- Add patch to fix find bug (#648560)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Kevin Fenzi <kevin@tummy.com> - 0.2.16-1
- Update to 0.2.16

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Oct 27 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.14-1
- Update to 0.2.14
- BuildRequire intltool
- Drop category X-Fedora from desktop file

* Sun Feb 10 2008 Kevin Fenzi <kevin@tummy.com> - 0.2.13-2
- Rebuild for gcc43

* Sun Nov 18 2007 Kevin Fenzi <kevin@tummy.com> - 0.2.13-1
- Update to 0.2.13

* Mon Aug 27 2007 Kevin Fenzi <kevin@tummy.com> - 0.2.12-3
- Update License tag

* Mon May 14 2007 Kevin Fenzi <kevin@tummy.com> - 0.2.12-2
- Rebuild for ppc64

* Sun Jan 21 2007 Kevin Fenzi <kevin@tummy.com> - 0.2.12-1
- Update to 0.2.12

* Fri Nov 10 2006 Kevin Fenzi <kevin@tummy.com> - 0.2.10-1
- Update to 0.2.10

* Thu Oct  5 2006 Kevin Fenzi <kevin@tummy.com> - 0.2.8-2
- Fix typo in description 

* Sun Sep  3 2006 Kevin Fenzi <kevin@tummy.com> - 0.2.8-1
- Update to 0.2.8

* Thu Aug 31 2006 Kevin Fenzi <kevin@tummy.com> - 0.2.6-2
- Add update-desktop-database

* Sun Aug 27 2006 Kevin Fenzi <kevin@tummy.com> - 0.2.6-1
- Inital package for fedora extras

