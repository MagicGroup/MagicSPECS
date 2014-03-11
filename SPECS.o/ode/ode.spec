Name:           ode
Version:        0.11.1
Release:        8%{?dist}
Summary:        High performance library for simulating rigid body dynamics
Group:          System Environment/Libraries
License:        BSD or LGPLv2+
URL:            http://www.ode.org
Source0:        http://downloads.sourceforge.net/opende/ode-%{version}.tar.bz2
# This works around a bug in rpmbuild, where with localbuilds it will pass
# the machine being build on as host param to configure instead of the machine
# on which the code will run
Patch0:         ode-0.10.0-no-pentium-on-i386.patch
Patch1:         ode-0.11.1-multilib.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  libGL-devel libGLU-devel

%description
ODE is an open source, high performance library for simulating rigid body
dynamics. It is fully featured, stable, mature and platform independent with
an easy to use C/C++ API. It has advanced joint types and integrated collision
detection with friction. ODE is useful for simulating vehicles, objects in
virtual reality environments and virtual creatures. It is currently used in
many computer games, 3D authoring tools and simulation tools.


%package        double
Summary:        Ode physics library compiled with double precision
Group:          Development/Libraries

%description    double
The %{name}-double package contains a version of the ODE library for simulating
rigid body dynamics compiled with double precision.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-double = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name} or %{name}-double.


%prep
%setup -q
%patch0 -p1
%patch1 -p1
# to stop autoxxx from getting regenerated because of our configure patch
touch -r CHANGELOG.txt configure.in
# stop rpmlint from complaining about executable files in the debug package
chmod -x ode/src/stepfast.cpp include/ode/collision_trimesh.h \
  include/ode/odeconfig.h


%build
%configure --enable-shared --disable-static --enable-double-precision
make %{?_smp_mflags} X_LIBS=-lX11 \
    libode_la_LDFLAGS="-release double -version-info 2:1:1"
sed -i 's|-lode|-lode-double|g' ode-config ode.pc
mv ode-config ode-double-config
mv ode.pc ode-double.pc
mv ode/src/.libs/libode-double.so.1.1.1 .
make distclean

CFLAGS="%{optflags} -ffast-math"
CXXFLAGS="%{optflags} -ffast-math"
%configure --enable-shared --disable-static
make %{?_smp_mflags} X_LIBS=-lX11


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/libode.la
# DIY libode-double install
install -m 755 ode-double-config $RPM_BUILD_ROOT%{_bindir}
install -m 755 libode-double.so.1.1.1 $RPM_BUILD_ROOT%{_libdir}
ln -s libode-double.so.1.1.1 $RPM_BUILD_ROOT%{_libdir}/libode-double.so.1
ln -s libode-double.so.1.1.1 $RPM_BUILD_ROOT%{_libdir}/libode-double.so
install -m 644 ode-double.pc $RPM_BUILD_ROOT%{_libdir}/pkgconfig


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post double -p /sbin/ldconfig

%postun double -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc CHANGELOG.txt LICENSE*.TXT README.txt
%{_libdir}/libode.so.1*

%files double
%defattr(-,root,root,-)
%doc CHANGELOG.txt LICENSE*.TXT README.txt
%{_libdir}/libode-double.so.1*

%files devel
%defattr(-,root,root,-)
%{_bindir}/%{name}-config
%{_bindir}/%{name}-double-config
%{_includedir}/%{name}
%{_libdir}/libode.so
%{_libdir}/libode-double.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/%{name}-double.pc


%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 0.11.1-8
- 为 Magic 3.0 重建

* Thu Jan 19 2012 Liu Di <liudidi@gmail.com> - 0.11.1-7
- 为 Magic 3.0 重建

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov  8 2010 Hans de Goede <hdegoede@redhat.com> 0.11.1-5
- Add a -double subpackage providing a version of ode compiled with
  double precision (#574034)

* Tue Feb 16 2010 Hans de Goede <hdegoede@redhat.com> 0.11.1-4
- Fix FTBFS (#564642)

* Thu Nov 12 2009 Hans de Goede <hdegoede@redhat.com> 0.11.1-3
- Fix multilib conflict in -devel sub package (#507981)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 25 2009 Hans de Goede <hdegoede@redhat.com> 0.11.1-1
- New upstream release 0.11.1

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 30 2009 Hans de Goede <hdegoede@redhat.com> 0.11-1
- New upstream release 0.11

* Mon Sep 15 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.1-1
- New upstream release 0.10.1 (bz 460033)

* Thu Apr  3 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.9-4
- Force proper use of RPM_OPT_FLAGS during build

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9-3
- Autorebuild for GCC 4.3

* Thu Oct 18 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.9-2
- Drop workaround for stormbaancoureur crash, it is now fixed in
  stormbaancoureur

* Fri Oct 12 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.9-1
- New upstream release 0.9 (final)

* Fri Sep 28 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.9-0.1.rc1
- New upstream release 0.9-rc1

* Tue Sep 11 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.8.1-0.1.rc1
- New upstream release 0.8.1-rc1

* Wed Aug 15 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.8-2
- Update License tag for new Licensing Guidelines compliance

* Wed Feb 14 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.8-1
- New upstream release 0.8

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 0.7-2
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Fri Sep 22 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.7-1
- New upstream release 0.7

* Mon Aug 28 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.6-3
- FE6 Rebuild

* Wed Jul  5 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.6-2
- Change name from libode to ode
- Fix soname & /usr/lib64 usage
- Patch configure to accept our CFLAGS instead of always using its own
- Patch configure to never activate the generation of asm-code which is then
  used unconditionally, the build CPU may be very different from the CPU on
  which the package gets run.

* Sun Jun 18 2006 Hugo Cisneiros <hugo@devin.com.br> 0.6-1
- Initial RPM release
