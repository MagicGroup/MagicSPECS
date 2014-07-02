Name:		libprojectM
Version:	2.0.1
Release:	23%{?dist}
Summary:	The libraries for the projectM music visualization plugin
Group:		Applications/Multimedia
License:	LGPLv2+
URL:		http://projectm.sourceforge.net/
Source0:	http://downloads.sourceforge.net/projectm/%{name}-%{version}.tar.bz2
#Remove fonts from package
#Change default fonts
Patch0:		libprojectM-fonts.patch
#Bump soname
Patch1:		libprojectM-soname.patch
#Turn off USE_THREADS until the bug is fixed upstream
Patch2:		libprojectM-USE_THREADS.patch
#Patches for clementine
Patch3:		01-change-texture-size.patch
Patch4:		04-change-preset-duration.patch

Patch5:		libprojectM-2.0.1-freetype253.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	ftgl-devel, cmake, glew-devel

BuildRequires:	dejavu-sans-mono-fonts, dejavu-sans-fonts
Requires:	dejavu-sans-mono-fonts, dejavu-sans-fonts
%global titlefont /share/fonts/dejavu/DejaVuSans.ttf
%global menufont /share/fonts/dejavu/DejaVuSansMono.ttf


%description
projectM is an awesome music visualizer. There is nothing better in the world
of Unix. projectM's greatness comes from the hard work of the community. Users
like you can create presets that connect music with incredible visuals.
projectM is an LGPL'ed reimplementation of Milkdrop under OpenGL. All projectM
requires is a video card with 3D acceleration and your favorite music.

%package	devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}, pkgconfig

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%patch0 -p1 -b .font-changes
for f in config.inp.in projectM.cpp
do
    sed -i -e 's!__FEDORA_TITLE_FONT__!%{titlefont}!g' $f
    sed -i -e 's!__FEDORA_MENU_FONT__!%{menufont}!g' $f
    grep -q -s __FEDORA_ $f && exit 1
done
[ -e %{_prefix}%{titlefont} ] || exit 1
[ -e %{_prefix}%{menufont} ] || exit 1

%patch1 -p1
%patch2 -p1
%patch3 -p0
%patch4 -p0
%patch5 -p1
sed -i 's/\r//' ChangeLog


%build
%cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} -DLIB_INSTALL_DIR=%{_libdir} .
make %{?_smp_mflags} VERBOSE=1


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING
%{_libdir}/*.so.*
%{_datadir}/projectM/

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Tue May 27 2014 Liu Di <liudidi@gmail.com> - 2.0.1-23
- 为 Magic 3.0 重建

* Tue May 27 2014 Liu Di <liudidi@gmail.com> - 2.0.1-22
- 为 Magic 3.0 重建

* Mon Nov 18 2013 Dave Airlie <airlied@redhat.com> - 2.0.1-21
- rebuilt for GLEW 1.10

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 13 2012 Adam Jackson <ajax@redhat.com> - 2.0.1-18
- Rebuild for glew 1.9.0

* Thu Jul 26 2012 Rex Dieter <rdieter@fedoraproject.org> 2.0.1-17
- rebuild (glew)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun  1 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 2.0.1-15
- Enhancement of the patch in 2.0.1-11: also override invalid font paths
  passed in by applications as these lead to an immediate crash. (#664088)
- Make -devel base pkg dep arch-specific.

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-14
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 ajax@redhat.com - 2.0.1-12
- Rebuild for new glew soname

* Sat May  7 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 2.0.1-11
- Also BuildRequires the desired font packages for the safety-checks.
- Drop obsolete README.fedora file since users need not modify their
  config file manually anymore to prevent projectM from crashing.
- Revise fonts patch: check that user's configured font files exist,
  fall back to our defaults, add safety-check in spec file, replace
  font paths in prep section. (#698404, #698381)

* Mon Apr 25 2011 Jameson Pugh <imntreal@gmail.com> - 2.0.1-10
- Fixed fonts patch

* Wed Mar 23 2011 Jameson Pugh <imntreal@gmail.com> - 2.0.1-9
- Correct typo in requirements

* Tue Mar 15 2011 Jameson Pugh <imntreal@gmail.com> - 2.0.1-8
- Replace obsolete bitstream-vera font requirements with dejavu

* Sat Jul 17 2010 Jameson Pugh (imntreal@gmail.com) - 2.0.1-7
- Updated font patch with Orcan's changes

* Sat Jul 10 2010 Jameson Pugh (imntreal@gmail.com) - 2.0.1-6
- Added patches so clementine can be built against it

* Fri May 21 2010 Jameson Pugh (imntreal@gmail.com) - 2.0.1-5
- Don't create fonts directory
- Add a README.fedora for instructions on upgrading from -3

* Mon Apr 05 2010 Jameson Pugh (imntreal@gmail.com) - 2.0.1-4
- Got rid of font symlinks

* Mon Feb 08 2010 Jameson Pugh (imntreal@gmail.com) - 2.0.1-3
- Patch to remove the USE_THREADS option pending an update from upstream

* Sun Jan 10 2010 Jameson Pugh (imntreal@gmail.com) - 2.0.1-2
- Made needed soname bump

* Sun Dec 13 2009 Jameson Pugh (imntreal@gmail.com) - 2.0.1-1
- New release

* Mon Oct 12 2009 Jameson Pugh (imntreal@gmail.com) - 1.2.0r1300-1
- SVN Release to prepare for v2

* Wed Feb 25 2009 Jameson Pugh (imntreal@gmail.com) - 1.2.0-9
- Aparently stdio.h didn't need to be included in BuiltinParams.cpp before, but is now

* Tue Feb 24 2009 Jameson Pugh (imntreal@gmail.com) - 1.2.0-8
- Font packages renamed

* Fri Jan 01 2009 Jameson Pugh (imntreal@gmail.com) - 1.2.0-7
- Per recommendation, switched font packages from bitstream to dejavu

* Mon Dec 22 2008 Jameson Pugh (imntreal@gmail.com) - 1.2.0-6
- Updated font package names

* Tue Nov 04 2008 Jameson Pugh (imntreal@gmail.com) - 1.2.0-5
- Moved sed command from prep to install
- Correct libprojectM.pc patch

* Thu Oct 30 2008 Jameson Pugh (imntreal@gmail.com) - 1.2.0-4
- Removed patch for ChangeLog, and used sed command in the spec
- Added VERBOSE=1 to the make line
- Added patch to correct libprojectM.pc

* Wed Oct 29 2008 Jameson Pugh (imntreal@gmail.com) - 1.2.0-3
- Added a patch to correct ChangeLog EOL encoding
- Cleaned up all Requires and BuildRequires
- Corrected ownership of include/libprojectM and data/projectM
- Removed unnecessary cmake arguments

* Wed Sep 24 2008 Jameson Pugh (imntreal@gmail.com) - 1.2.0-2
- Removed fonts from package
- Added symlinks to the fonts due to hard coded programing

* Tue Sep 02 2008 Jameson Pugh (imntreal@gmail.com) - 1.2.0-1
- New release
- 64-bit patch no longer needed

* Mon Mar 31 2008 Jameson Pugh (imntreal@gmail.com) - 1.1-1
- New release

* Wed Dec 05 2007 Jameson Pugh <imntreal@gmail.com> - 1.01-1
- Initial public release of the package
