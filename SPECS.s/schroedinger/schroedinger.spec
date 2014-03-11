%define abi 1.0

Name:           schroedinger
Version:        1.0.11
Release:        3%{?dist}
Summary:        Portable libraries for the high quality Dirac video codec

Group:          System Environment/Libraries
# No version is given for the GPL or the LGPL
License:        GPL+ or LGPLv2+ or MIT or MPLv1.1
URL:            http://www.diracvideo.org/
Source0:        http://www.diracvideo.org/download/schroedinger/schroedinger-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  orc-devel >= 0.4.10
BuildRequires:  glew-devel >= 1.5.1
BuildRequires:  gtk-doc


%description
The Schrödinger project will implement portable libraries for the high
quality Dirac video codec created by BBC Research and
Development. Dirac is a free and open source codec producing very high
image quality video.

The Schrödinger project is a project done by BBC R&D and Fluendo in
order to create a set of high quality decoder and encoder libraries
for the Dirac video codec.

%package devel
Group:          Development/Libraries
Summary:        Development files for schroedinger
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
Requires:       orc-devel >= 0.4.10

%description devel
Development files for schroedinger


%prep
%setup -q


%build
%configure --disable-static --enable-gtk-doc

# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
find %{buildroot} -name \*.la -delete


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING* NEWS TODO
%{_libdir}/libschroedinger-%{abi}.so.*


%files devel
%defattr(-,root,root,-)
%doc %{_datadir}/gtk-doc/html/schroedinger
%{_includedir}/schroedinger-%{abi}
%{_libdir}/*.so
%{_libdir}/pkgconfig/schroedinger-%{abi}.pc


%changelog
* Sat Dec 08 2012 Liu Di <liudidi@gmail.com> - 1.0.11-3
- 为 Magic 3.0 重建

* Tue Nov 13 2012 Liu Di <liudidi@gmail.com> - 1.0.11-2
- 为 Magic 3.0 重建

* Mon Jan 23 2012 Fabian Deutsch <fabiand@fedoraproject.org> - 1.0.11-1
- Update to 1.0.11

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Oct 24 2010 Fabian Deutsch <fabiand@fedoraproject.org> - 1.0.10-1
- Update to 1.0.10

* Tue Apr 22 2010 Fabian Deutsch <fabiand@fedoraproject.org> - 1.0.9-2
- Added dependency on gtk-doc

* Fri Mar 05 2010 Fabian Deutsch <fabiand@fedoraproject.org> - 1.0.9-1
- Update to 1.0.9
- Dropped dependency on liboil
- Added dependency on orc

* Mon Feb  1 2010 Nicolas CHauvet <kwizart@fedoraproject.org> - 1.0.8-4
- Remove gstreamer-plugins-schroedinger 
  Obsoleted by gst-plugins-bad-free introduction in Fedora.

* Sun Oct 25 2009 kwizart < kwizart at gmail.com > - 1.0.8-3
- Re-introduce gstreamer sub-package until seen in -good

* Tue Oct 20 2009 kwizart < kwizart at gmail.com > - 1.0.8-2
- Update to 1.0.8
- gstreamer-plugins-schroedinger is now in bad.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Apr 24 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.0.7-1
- Update to 1.0.7

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Oct 29 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.0.5-4
- Fix some typos [BZ#469133]

* Fri Sep 12 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.0.5-3
- Bump release and rebuild against latest gstreamer-* packages to pick
- up special gstreamer codec provides.

* Thu Sep  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0.5-2
- fix license tag

* Wed Aug 27 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.0.5-1
- Update to 1.0.5

* Fri Jul  2 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.0.3-2
- Devel subpackage needs to require liboil-devel.

* Fri Jun 27 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.0.3-1
- Update to 1.0.3.
- Update URLs.

* Fri Feb 22 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.0.0-1
- Update to 1.0.0

* Mon Feb 11 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9.0-2
- Rebuild for GCC 4.3

* Mon Nov 12 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.9.0-1
- Update to 0.9.0

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.6.1-3
- Rebuild for selinux ppc32 issue.

* Wed Jun 20 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.6.1-2
- Fix license field
- Add pkgconfig as a requirement for the devel subpackage

* Sun Jun 10 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.6.1-1
- First version for Fedora
