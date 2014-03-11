
Name:	 ilmbase 
Version: 1.0.2
Release: 5%{?dist}
Summary: Abstraction/convenience libraries

Group:	 System Environment/Libraries
License: BSD
URL:	 http://www.openexr.com/
Source0: http://download.savannah.nongnu.org/releases/openexr/ilmbase-%{version}.tar.gz
Source1: http://download.savannah.nongnu.org/releases/openexr/ilmbase-%{version}.tar.gz.sig
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#BuildRequires: automake libtool
BuildRequires: pkgconfig

## upstreamable patches
# missing #include <cstring>
Patch50: ilmbase-1.0.2-cstring.patch
# explicitly add $(PTHREAD_LIBS) to libIlmThread linkage (helps workaround below)
Patch51: ilmbase-1.0.2-no_undefined.patch

%description
Half is a class that encapsulates the ilm 16-bit floating-point format.

IlmThread is a thread abstraction library for use with OpenEXR
and other software packages.

Imath implements 2D and 3D vectors, 3x3 and 4x4 matrices, quaternions
and other useful 2D and 3D math functions.

Iex is an exception-handling library.

%package devel
Summary: Headers and libraries for building apps that use %{name} 
Group:	 Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: libGL-devel libGLU-devel
Requires: pkgconfig
%description devel
%{summary}.


%prep
%setup -q

%patch50 -p1 -b .cstring
%patch51 -p1 -b .no_undefined


%build
%configure --disable-static

# manually set PTHREAD_LIBS to include -lpthread until libtool bogosity is fixed,
# https://bugzilla.redhat.com/show_bug.cgi?id=661333
make %{?_smp_mflags} PTHREAD_LIBS="-pthread -lpthread"


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

rm -f  $RPM_BUILD_ROOT%{_libdir}/lib*.la


%check
export PKG_CONFIG_PATH=%{buildroot}%{_datadir}/pkgconfig:%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion IlmBase)" = "%{version}"
%ifarch %{ix86}
make check ||:
%else
make check
%endif


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_libdir}/libHalf.so.6*
%{_libdir}/libIex.so.6*
%{_libdir}/libIlmThread.so.6*
%{_libdir}/libImath.so.6*

%files devel
%defattr(-,root,root,-)
%{_includedir}/OpenEXR/
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/IlmBase.pc


%changelog
* Fri Dec 07 2012 Liu Di <liudidi@gmail.com> - 1.0.2-5
- 为 Magic 3.0 重建

* Tue Dec 13 2011 Liu Di <liudidi@gmail.com> - 1.0.2-4
- 为 Magic 3.0 重建

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

