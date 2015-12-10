Name:    ilmbase
Version:	2.2.0
Release: 3%{?dist}
Summary: Abstraction/convenience libraries

License: BSD
URL:	 http://www.openexr.com/
Source0: http://download.savannah.nongnu.org/releases/openexr/ilmbase-%{version}.tar.gz

#BuildRequires: automake libtool
BuildRequires: pkgconfig
# silly rpm, won't pick up rpm dependencies for items not in it's buildroot
# see http://bugzilla.redhat.com/866302
BuildRequires: pkgconfig(gl) pkgconfig(glu)

## upstreamable patches
# explicitly add $(PTHREAD_LIBS) to libIlmThread linkage (helps workaround below)
Patch51: ilmbase-2.0.1-no_undefined.patch
# add Requires.private: gl glu to IlmBase.pc
Patch53:  ilmbase-1.0.3-pkgconfig.patch

## upstream patches

%description
Half is a class that encapsulates the ilm 16-bit floating-point format.

IlmThread is a thread abstraction library for use with OpenEXR
and other software packages.

Imath implements 2D and 3D vectors, 3x3 and 4x4 matrices, quaternions
and other useful 2D and 3D math functions.

Iex is an exception-handling library.

%package devel
Summary: Headers and libraries for building apps that use %{name} 
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
%{summary}.


%prep
%setup -q

%patch51 -p1 -b .no_undefined
%patch53 -p1 -b .pkgconfig

#/bootstrap


%build
%configure --disable-static

# manually set PTHREAD_LIBS to include -lpthread until libtool bogosity is fixed,
# https://bugzilla.redhat.com/show_bug.cgi?id=661333
make %{?_smp_mflags} PTHREAD_LIBS="-pthread -lpthread"


%install
make install DESTDIR=%{buildroot}

rm -fv %{buildroot}%{_libdir}/lib*.la


%check
export PKG_CONFIG_PATH=%{buildroot}%{_datadir}/pkgconfig:%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion IlmBase)" = "%{version}"
# is the known-failure ix86-specific or 32bit specific? guess we'll find out -- rex
%ifarch %{ix86}
make check ||:
%else
make check
%endif


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/libHalf.so.1*
%{_libdir}/libIex-2_*.so.1*
%{_libdir}/libIexMath-2_*.so.1*
%{_libdir}/libIlmThread-2_*.so.1*
%{_libdir}/libImath-2_*.so.1*

%files devel
%{_includedir}/OpenEXR/
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/IlmBase.pc


%changelog
* Sun Nov 08 2015 Liu Di <liudidi@gmail.com> - 2.2.0-3
- 为 Magic 3.0 重建

* Fri Oct 30 2015 Liu Di <liudidi@gmail.com> - 2.2.0-2
- 为 Magic 3.0 重建

* Sun Mar 01 2015 Liu Di <liudidi@gmail.com> - 2.2.0-1
- 更新到 2.2.0

* Wed Nov 27 2013 Rex Dieter <rdieter@fedoraproject.org> 2.1.0-1
- 2.1.0

* Thu Aug 29 2013 Rex Dieter <rdieter@fedoraproject.org>  2.0.1-1
- 2.0.1

* Thu Aug 29 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.3-7
- Fix spec issues, modernise spec

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 15 2012 Rex Dieter <rdieter@fedoraproject.org> 1.0.3-4
- ilmbase-devel missing dependency on libGLU-devel (#866302)

* Sat Sep 08 2012 Rex Dieter <rdieter@fedoraproject.org> - 1.0.3-3
- IlmBase.pc: +Requires.private: gl glu
- -devel: drop hard-coded libGL/pkgconfig deps, let rpm autodetect now

* Tue Sep 04 2012 Dan Horák <dan[at]danny.cz> 1.0.3-2
- fix build on non-x86 arches

* Sun Aug 05 2012 Rex Dieter <rdieter@fedoraproject.org> 1.0.3-1
- ilmbase-1.0.3
- ix86 fix courtesy of Nicolas Chauvet <kwizart@gmail.com>

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 08 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.0.2-2
- libIlmThread missing -pthread linkage (#661115)
- %%install: INSTALL="install -p"
- -devel: tighten dep using %%?_isa

* Wed Jul 28 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.0.2-1
- ilmbase-1.0.2

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May  4 2009 Ville Skyttä <ville.skytta at iki.fi> - 1.0.1-5
- Fix spelling error in summary.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec 12 2008 Rex Dieter <rdieter@fedoraproject.org> 1.0.1-3
- rebuild for pkgconfig deps

* Fri Feb 08 2008 Rex Dieter <rdieter@fedoraproject.org> 1.0.1-2
- respin (gcc43)

* Mon Jan 07 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.1-1
- ilmbase-1.0.1

* Fri Oct 12 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.0-3
- include *.tar.sig in sources

* Mon Oct 08 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.0-2
- update %%summary
- -devel: +Requires: libGL-devel libGLU-devel
- make install ... INSTALL="install -p" to preserve timestamps


* Thu Aug 09 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.0-1
- ilmbase-1.0.0 (first try)

