%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
Summary:        Generic Programming for Computer Vision
Name:           vigra
Version:        1.10.0
Release:        2%{?dist}
License:        MIT
Group:          Development/Libraries
Source0:        http://hci.iwr.uni-heidelberg.de/%{name}/%{name}-%{version}-src.tar.gz
Source1:        vigra-config.sh
URL:            http://hci.iwr.uni-heidelberg.de/vigra/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  zlib-devel libjpeg-devel libpng-devel libtiff-devel fftw-devel >= 3
BuildRequires:  cmake boost-devel doxygen
%if ! 0%{?rhel}
BuildRequires:  hdf5-devel python-sphinx numpy-f2py boost-python OpenEXR-devel
%endif
Patch0: vigra.rhbz987048.shebang.patch

%description
VIGRA stands for "Vision with Generic Algorithms". It's a novel computer vision
library that puts its main emphasis on customizable algorithms and data
structures. By using template techniques similar to those in the C++ Standard
Template Library, you can easily adapt any VIGRA component to the needs of your
application without thereby giving up execution speed.

%package devel
Summary: Development tools for programs which will use the vigra library
Group: Development/Libraries
Requires: vigra = %{version}-%{release}
Requires: libjpeg-devel libtiff-devel libpng-devel zlib-devel fftw-devel >= 3
Requires: boost-devel
%if ! 0%{?rhel}
Requires: hdf5-devel numpy-f2py boost-python OpenEXR-devel
%endif

%description devel
The vigra-devel package includes the header files necessary for developing
programs that use the vigra library.

%if ! 0%{?rhel}
%package python
Summary: Python interface for the vigra computer vision library
Requires: vigra = %{version}-%{release}
Requires: numpy numpy-f2py

%description python
The vigra-python package provides python bindings for vigra
%endif

%prep
%setup -q
%patch0 -p1 -b .rhbz987048.shebang.patch

%build
%if ! 0%{?rhel}
%cmake . -DWITH_OPENEXR=1 -DWITH_HDF5=1 -DWITH_VIGRANUMPY=1 -DWITH_VALGRIND=0
%else
%cmake . -DWITH_OPENEXR=0 -DWITH_HDF5=0 -DWITH_VIGRANUMPY=0 -DWITH_VALGRIND=0
%endif
make VERBOSE=1 %{?_smp_mflags}
# cleanup
rm -f doc/vigranumpy/.buildinfo
find ./doc/ -type f | xargs chmod -x

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}/usr/doc
(
 cd $RPM_BUILD_ROOT%{_bindir}
 mv vigra-config vigra-config-%{__isa_bits}
)
install -p -m755 -D %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/vigra-config

#fixme: this fails,
#%check
#make VERBOSE=1 check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root,-)
%doc LICENSE.txt
%{_libdir}/libvigraimpex.so.*

%files devel
%defattr(-, root, root,-)
%{_includedir}/vigra
%{_bindir}/vigra-config*
%{_libdir}/libvigraimpex.so
%{_libdir}/vigra
%doc doc/vigra doc/vigranumpy

%if ! 0%{?rhel}
%files python
%defattr(-, root, root,-)
%{python_sitearch}/vigra
%{_libdir}/vigranumpy
%endif

%changelog
* Wed Apr 30 2014 Liu Di <liudidi@gmail.com> - 1.10.0-2
- 为 Magic 3.0 重建

* Fri Dec 13 2013 Bruno Postle <bruno@postle.net> - 1.10.0-1
- upstream release

* Wed Nov 27 2013 Rex Dieter <rdieter@fedoraproject.org> - 1.9.0-14
- rebuild (openexr)

* Sat Sep 21 2013 David Tardon <dtardon@redhat.com> - 1.9.0-13
- rebuild for atlas 3.10

* Thu Sep 12 2013 Caolán McNamara <caolanm@redhat.com> - 1.9.0-12
- bump n-v-r

* Thu Aug 29 2013 Caolán McNamara <caolanm@redhat.com> - 1.9.0-11
- Resolves: rhbz#884207 multi-lib vigra-config

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 27 2013 pmachata@redhat.com - 1.9.0-9
- Rebuild for boost 1.54.0

* Wed Jul 24 2013 Caolán McNamara <caolanm@redhat.com> - 1.9.0-8
- Resolves: rhbz#987048 explicit python path in shebang

* Tue Jun 04 2013 Caolán McNamara <caolanm@redhat.com> - 1.9.0-7
- Resolves: rhbz#970561 no hdf5-devel in RHEL-7

* Thu May 16 2013 Orion Poplawski <orion@cora.nwra.com> - 1.9.0-6
- Rebuild for hdf5 1.8.11

* Sun Mar 10 2013 Rex Dieter <rdieter@fedoraproject.org> - 1.9.0-5
- rebuild (OpenEXR)

* Thu Feb 14 2013 Caolán McNamara <caolanm@redhat.com> - 1.9.0-4
- no hdf5-devel in RHEL-7

* Sat Feb 09 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.9.0-3
- Rebuild for Boost-1.53.0

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 1.9.0-2
- rebuild due to "jpeg8-ABI" feature drop

* Tue Nov 06 2012 Bruno Postle <bruno@postle.net> 1.9.0-1
- upstream release, support impex OpenEXR

* Tue Nov 06 2012 Caolán McNamara <caolanm@redhat.com> - 1.8.0-7
- document that there is a test suite, but it fails

* Wed Oct 31 2012 Tom Callaway <spot@fedoraproject.org> - 1.8.0-6
- rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 27 2012 Bruno Postle <bruno@postle.net> 1.8.0-4
- patch to build with gcc-4.7.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1.8.0-2
- Rebuild for new libpng

* Sat Sep 24 2011 Bruno Postle <bruno@postle.net> 1.8.0-1
- upstream release

* Fri Aug 26 2011 Tom Callaway <spot@fedoraproject.org> - 1.7.1-4
- rebuild against boost

* Tue May 17 2011 Orion Poplawski <orion@cora.nwra.com> - 1.7.1-3
- Rebuild for hdf5 1.8.7

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 23 2011 Bruno Postle <bruno@postle.net> 1.7.1-1
- upstream release

* Fri Jul 30 2010 Toshio Kuratomi <toshio@fedoraproject.org> 1.7.0-2
- Rebuild for new python release

* Tue Apr 20 2010 Bruno Postle <bruno@postle.net> 1.7.0-1
- new upstream with cmake replacing autotools.
- patch for x86_64 systems.
- add vigra-python sub-package.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 08 2009 Bruno Postle - 1.6.0-1
- Update to latest release

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.5.0-4
- Autorebuild for GCC 4.3

* Tue Aug 21 2007 Bruno Postle <bruno@postle.net> 1.5.0-3
  - Bumping for Jesse

* Mon Feb 19 2007 Bruno Postle <bruno@postle.net> 1.5.0-2
  - update to 1.5.0 release
  - fix bug 228926: vigra: $RPM_OPT_FLAGS not used

* Sun Nov 23 2003 Bruno Postle <bruno@postle.net>
  - initial package


