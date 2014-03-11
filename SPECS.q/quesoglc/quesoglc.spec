Name:           quesoglc
Version:        0.7.2
Release:        6%{?dist}
Summary:        The OpenGL Character Renderer

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://quesoglc.sourceforge.net/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}-free.tar.bz2
Patch0:         quesoglc-0.7.2-glew-mx.patch
Patch1:         quesoglc-0.7.2-doxyfile.patch

BuildRequires:  fontconfig-devel freeglut-devel
BuildRequires:  fribidi-devel glew-devel libSM-devel libXmu-devel
BuildRequires:  libXi-devel doxygen
BuildRequires:  pkgconfig 

%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       libGL-devel
Requires:       pkgconfig

%description
The OpenGL Character Renderer (GLC) is a state machine that provides OpenGL
programs with character rendering services via an application programming
interface (API).

%description devel
This package provides the libraries, include files, and other resources needed
for developing GLC applications.


%prep
%setup -q
%patch0 -p1
%patch1 -p1
rm -f include/GL/{glxew,wglew,glew}.h
ln -s %{_includedir}/GL/{glxew,wglew,glew}.h include/GL/
rm -rf src/fribidi/


%build
%configure --disable-static 
make %{?_smp_mflags}
cd docs
doxygen
cd ../


%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/libGLC.la


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%doc AUTHORS ChangeLog COPYING README THANKS
%{_libdir}/libGLC.so.*

%files devel
%doc docs/html
%{_includedir}/GL/glc.h
%{_libdir}/libGLC.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Thu May 02 2013 Liu Di <liudidi@gmail.com> - 0.7.2-6
- 为 Magic 3.0 重建

* Sat Jul 28 2012 Hans de Goede <hdegoede@redhat.com> - 0.7.2-5
- Fix FTBFS (rhbz#716030)
- Fix multilib conflict (rhbz#831438)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Aug 18 2010 Karol Trzcionka <karlikt at gmail.com> - 0.7.2-1
- Update to v0.7.2

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Apr 22 2008 Karol Trzcionka <karlikt at gmail.com> - 0.7.1-1
- Update to v0.7.1
- Using original tarball
* Sat Feb 23 2008 Karol Trzcionka <karlikt at gmail.com> - 0.7.0-1
- Update to v0.7.0
* Sat Feb 09 2008 Karol Trzcionka <karlikt at gmail.com> - 0.6.5-5
- Rebuild for gcc43
- Fix typo in patch
* Thu Dec 27 2007 Karol Trzcionka <karlikt at gmail.com> - 0.6.5-4
- Delete %%check
* Sun Dec 23 2007 Karol Trzcionka <karlikt at gmail.com> - 0.6.5-3
- Add %%check section
- Remove redundant BuildRequires
* Sat Dec 22 2007 Karol Trzcionka <karlikt at gmail.com> - 0.6.5-2
- Remove freeB and GLXPL files
- Add html docs
- Add Requires for subpackage -devel
- Fix BuildRequires
* Sat Dec 01 2007 Karol Trzcionka <karlikt at gmail.com> - 0.6.5-1
- Initial release
