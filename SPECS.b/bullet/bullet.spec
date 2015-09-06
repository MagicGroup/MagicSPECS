%global svnrev 2704

Name: bullet
Version: 2.82
Release: 6%{?dist}
Summary: 3D Collision Detection and Rigid Body Dynamics Library
Group: Development/Libraries
License: zlib and MIT and BSD
URL: http://www.bulletphysics.com

Source0: %{name}-%{version}-r%{svnrev}-free.tar.gz
# bullet contains non-free code that we cannot ship.  Therefore we use
# this script to remove the non-free code before shipping it.
# Download the upstream tarball and invoke this script while in the
# tarball's directory:
# ./generate-tarball.sh 2.82-r2704
Source1: generate-tarball.sh

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: cmake
BuildRequires: freeglut-devel
BuildRequires: libICE-devel


%description
Bullet is a 3D Collision Detection and Rigid Body Dynamics Library for games
and animation.


%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: cmake
%description devel
Development headers and libraries for %{name}.


%package extras
Summary: Extra libraries for %{name}
Group: Development/Libraries
License: zlib and LGPLv2+

%description extras
Extra libraries for %{name}.


%package extras-devel
Summary: Development files for %{name} extras
Group: Development/Libraries
License: zlib and LGPLv2+
Requires: %{name}-extras%{?_isa} = %{version}-%{release}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}

%description extras-devel
Development headers and libraries for %{name} extra libraries.


%prep
%setup -q -n %{name}-%{version}-r%{svnrev}

# Set these files to right permission
chmod 644 src/LinearMath/btPoolAllocator.h
chmod 644 src/BulletDynamics/ConstraintSolver/btSliderConstraint.cpp
chmod 644 src/BulletDynamics/ConstraintSolver/btSliderConstraint.h

iconv -f ISO-8859-1 -t UTF-8 -o ChangeLog.utf8 ChangeLog
mv ChangeLog.utf8 ChangeLog
# Don't build bundled glui
rm -fr Extras/glui/*

%build
mkdir build
pushd build
%cmake .. \
  -DBUILD_DEMOS=OFF \
  -DBUILD_EXTRAS=ON \
  -DINSTALL_EXTRA_LIBS=ON \
  -DCMAKE_BUILD_TYPE=NONE \
  -DCMAKE_SKIP_BUILD_RPATH=ON \
  -DINCLUDE_INSTALL_DIR=%{_includedir}/bullet

make %{?_smp_mflags}
popd

%install
rm -rf $RPM_BUILD_ROOT
pushd build
make install DESTDIR=$RPM_BUILD_ROOT
popd

# Create symlinks for .so.X
pushd $RPM_BUILD_ROOT%{_libdir}
for f in lib*.so.*.*
do
  ln -sf $f ${f%\.*}
done
popd


%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post extras -p /sbin/ldconfig

%postun extras -p /sbin/ldconfig


%files
%doc README AUTHORS COPYING NEWS ChangeLog
%{_libdir}/libBulletCollision.so.*
%{_libdir}/libBulletDynamics.so.*
%{_libdir}/libBulletSoftBody.so.*
%{_libdir}/libLinearMath.so.*

%files devel
%doc Bullet_User_Manual.pdf
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_includedir}/%{name}/BulletCollision
%{_includedir}/%{name}/BulletDynamics
%{_includedir}/%{name}/BulletSoftBody
%{_includedir}/%{name}/LinearMath
%{_includedir}/%{name}/vectormath
%{_libdir}/libBulletCollision.so
%{_libdir}/libBulletDynamics.so
%{_libdir}/libBulletSoftBody.so
%{_libdir}/libLinearMath.so
%{_libdir}/pkgconfig/bullet.pc
%{_libdir}/cmake/%{name}

%files extras
%{_libdir}/libConvexDecomposition.so.*
%{_libdir}/libGIMPACTUtils.so.*
%{_libdir}/libHACD.so.*
%{_libdir}/libBulletFileLoader.so.*
%{_libdir}/libBulletWorldImporter.so.*
%{_libdir}/libBulletXmlWorldImporter.so.*

%files extras-devel
%{_includedir}/%{name}/ConvexDecomposition
%{_includedir}/%{name}/GIMPACTUtils
%{_includedir}/%{name}/HACD
%{_includedir}/%{name}/BulletFileLoader
%{_includedir}/%{name}/BulletWorldImporter
%{_includedir}/%{name}/BulletXmlWorldImporter
%{_libdir}/libConvexDecomposition.so
%{_libdir}/libGIMPACTUtils.so
%{_libdir}/libHACD.so
%{_libdir}/libBulletFileLoader.so
%{_libdir}/libBulletWorldImporter.so
%{_libdir}/libBulletXmlWorldImporter.so

%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.82-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.82-5
- Rebuilt for GCC 5 C++11 ABI change

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.82-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.82-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 16 2014 Rich Mattes <richmattes@gmail.com> - 2.82-2
- Install all of the bullet extras (rhbz#1097452)
- Spec file cleanup

* Sun Feb 09 2014 Rich Mattes <richmattes@gmail.com> - 2.82-1
- Update to version 2.82

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.81-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.81-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Oct 13 2012 Rich Mattes <richmattes@gmail.com> - 2.81-1
- Update to version 2.81

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.80-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 25 2012 Rich Mattes <richmattes@gmail.com> - 2.80-1
- Update to version 2.80

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.79-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Dec 18 2011 Rich Mattes <richmattes@gmail.com> - 2.79-1
- Update to version 2.79

* Wed May 11 2011 Rich Mattes <richmattes@gmail.com> - 2.78-1
- Update to version 2.78
- Remove upstreamed patches

* Sat Feb 19 2011 Rich Mattes <richmattes@gmail.com> - 2.77-4
- Fix gcc 4.6 build error

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.77-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 20 2010 Dan Horák <dan[at]danny.cz> - 2.77-3
- add extras subpackage with additional libs
- install headers into /usr/include/bullet

* Wed Sep 29 2010 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 2.77-2
- Added LibSuffix patch

* Wed Sep 29 2010 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 2.77-1
- Updatet to version 2.77
- Droped all patches because they are all in upstream

* Sat Aug 21 2010 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 2.75-4
- Hope fix (#599495)

* Sat Aug 21 2010 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 2.75-3
- Hope fix (#619885)

* Tue Mar 09 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.75-2
- pkgconfig file not installed (#549051)

* Sat Oct 03 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 2.75-1
- Updatet to new upstream version 2.75
- Updatet the patch file to work agian

* Thu Jun 25 2009 Thomas Kowaliczek <linuxdonald@linuxdonald.de> - 2.74-1
- Updatet to version 2.74
- Updatet the patch file to work agian

* Sun Feb 22 2009 Bruno Mahé <bruno at gnoll.org> - 2.73-5
- Shortened the description
- Fix directory ownership for directories BulletCollision and BulletDynamics
- Convert ChangeLog to UTF-8
- chmod generate-tarball.sh to 644

* Fri Feb 20 2009 Bruno Mahé <bruno at gnoll.org> - 2.73-4
- Remove gcc-g++ in BuildRequires
- Add option -DCMAKE_BUILD_TYPE=NONE to %%cmake. This will make CMake using default compiler flags
- Use %% instead of single % in %%changelog to prevent macros from being expanded
- Specify we are not shipping pristine source because of some non-free parts
- Change licence to "zlib and MIT and BSD"
- Make include directory being owned by this package
- Remove duplicate documents
- Convert spec file to UTF8
- Set some files permission to 644

* Sun Feb 15 2009 Bruno Mahé <bruno at gnoll.org> - 2.73-3
- Remove non-free directories Demos/, Extras/ and Glut/ from the source

* Sun Jan 18 2009 Bruno Mahé <bruno at gnoll.org> - 2.73-2
- Add "rm -rf $RPM_BUILD_ROOT" to the install target
- Moved unversioned shared libraries (e.g. libfoo.so) to the -devel package
- Update %%post and %%postrun
- Change %%description
- Reduce length of %%summary
- Changed %%group to Development/Libraries
- Changed Zlib licence to lowercase zlib
- %%description kept below 80 characters wide

* Sat Dec 13 2008 Bruno Mahé <bruno at gnoll.org> - 2.73-1
- Initial build.
