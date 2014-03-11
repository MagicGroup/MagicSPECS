Name:            polkit-qt-1
Version:         0.103.0
Release:         3%{?dist}
Summary:         Qt bindings for PolicyKit

Group:           System Environment/Libraries
License:         GPLv2+
URL:             https://projects.kde.org/projects/kdesupport/polkit-qt-1 
Source0:         ftp://ftp.kde.org/pub/kde/stable/apps/KDE4.x/admim/polkit-qt-1-%{version}.tar.bz2 
Source1:         Doxyfile
BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch0:          polkit-qt-0.95.1-install-cmake-find.patch

## upstream patches

Source10: macros.polkit-qt

BuildRequires:   automoc4
BuildRequires:   cmake
BuildRequires:   polkit-devel >= 0.98
BuildRequires:   qt4-devel
BuildRequires:   doxygen

%description
Polkit-qt is a library that lets developers use the PolicyKit API
through a nice Qt-styled API.

%package devel
Summary: Development files for PolicyKit Qt bindings
Group: Development/Libraries
Provides: polkit-qt-1-devel = %{version}-%{release}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
%{summary}.

%package doc
Summary: Doxygen documentation for the PolkitQt API
Group: Documentation
BuildArch: noarch
%description doc
%{summary}.


%prep
%setup -q -n %{name}-%{version}

# temporary patch - installs FindPolkitQt-1.cmake until we decide how to deal with cmake 
# module installation
%patch0 -p1 -b .install-cmake-find


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} \
  -DBUILD_EXAMPLES:BOOL=0 \
  -DDATA_INSTALL_DIR:PATH=%{_datadir} \
  ..
popd

make %{?_smp_mflags} -C %{_target_platform}

doxygen %{SOURCE1}
# Remove installdox file - it is not necessary here
rm -f html/installdox


%install
rm -rf %{buildroot}
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
install -p -m644 -D %{SOURCE10} %{buildroot}%{_sysconfdir}/rpm/macros.polkit-qt


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_libdir}/libpolkit-qt-core-1.so.1*
%{_libdir}/libpolkit-qt-gui-1.so.1*
%{_libdir}/libpolkit-qt-agent-1.so.1*

%files devel
%defattr(-,root,root,-)
%{_sysconfdir}/rpm/macros.polkit-qt
%{_includedir}/polkit-qt-1/
%{_libdir}/libpolkit-qt-core-1.so
%{_libdir}/libpolkit-qt-gui-1.so
%{_libdir}/libpolkit-qt-agent-1.so
%{_libdir}/pkgconfig/polkit-qt-1.pc
%{_libdir}/pkgconfig/polkit-qt-core-1.pc
%{_libdir}/pkgconfig/polkit-qt-gui-1.pc
%{_libdir}/pkgconfig/polkit-qt-agent-1.pc
%{_libdir}/cmake/PolkitQt-1/
%{_datadir}/cmake/Modules/*.cmake

%files doc
%defattr(-,root,root,-)
%doc html/*


%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.103.0-3
- 为 Magic 3.0 重建

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.103.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 15 2011 Jaroslav Reznik <jreznik@redhat.com> 0.103.0-1
- polkit-qt-1-0.103.0

* Mon Dec 12 2011 Rex Dieter <rdieter@fedoraproject.org> 0.99.0-3
- upstream crash patch (kde#258916,#684625)
- pull a couple more upstream patches
- -devel: drop Req: polkit-devel

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 09 2010 Jaroslav Reznik <jreznik@redhat.com> - 0.99.0-1
- polkit-qt-1-0.99.0

* Sat Nov 20 2010 Rex Dieter <rdieter@fedoraproject.org> -  0.98.1-1.20101120
- polkit-qt-1-0.98.1-20101120 snapshot

* Fri Oct 15 2010 Radek Novacek <rnovacek@redhat.com> - 0.96.1-4
- Next attempt of fix-deprecated-warnings patch

* Thu Oct 14 2010 Jaroslav Reznik <jreznik@redhat.com> - 0.96.1-3
- Revert fix-deprecated-warnings as it causes kde#254150

* Thu Oct 07 2010 Radek Novacek <rnovacek@redhat.com> 0.96.1-2
- Fixed deprecation warning with polkit-0.98
- Fixed typo in url
- Null checking patch (might be fix for #637064)

* Tue Sep 07 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.96.1-1
- polkit-qt-1-0.96.1

* Thu Jan 14 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.95.1-3
- macros.polkit-qt : %%_polkit_qt_policydir, %%_polkit_qt

* Thu Jan 14 2010 Jaroslav Reznik <jreznik@redhat.com> - 0.95.1-2
- Installs FindPolkitQt-1.cmake

* Tue Jan 05 2010 Jaroslav Reznik <jreznik@redhat.com> - 0.95.1-1
- Update to release version

* Sun Dec 27 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.95-0.3.20091119svn
- Provides: polkit-qt-1(-devel) ...
- doc: make noarch

* Wed Dec 09 2009 Kevin Kofler <Kevin@tigcc.ticalc.org>  - 0.95-0.2.20091119svn
- Obsoletes: polkit-qt-examples < 0.10 for upgrade path

* Mon Nov 23 2009 Radek Novacek <rnovacek@redhat.com> - 0.95-0.1.20091119svn
- Added -doc subpackage
- Added command to obtaining the source code

* Fri Nov 20 2009 Jaroslav Reznik <jreznik@redhat.com> - 0.95-0.1.20091119svn
- SPEC file fixes
- removed -examples subpackage

* Thu Nov 19 2009 Radek Novacek <rnovacek@redhat.com> - 0.1.20091119svn
- Initial build of snapshot from svn
