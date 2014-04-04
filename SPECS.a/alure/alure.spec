Name:           alure
Version:        1.2
Release:        6%{?dist}
Summary:        Audio Library Tools REloaded
Group:          System Environment/Libraries
# ALURE code is LGPLv2+; note -devel subpackage has its own license tag
License:        LGPLv2+ 
URL:            http://kcat.strangesoft.net/alure.html
Source0:        http://kcat.strangesoft.net/%{name}-releases/%{name}-%{version}.tar.bz2
Patch0:         alure-gcc47.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  cmake, libvorbis-devel, libsndfile-devel, openal-soft-devel, flac-devel, dumb-devel, fluidsynth-devel


%description
ALURE is a utility library to help manage common tasks with OpenAL 
applications. This includes device enumeration and initialization, 
file loading, and streaming.  


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
# Devel doc includes some files under GPLv2+ from NaturalDocs
License:        LGPLv2+ and GPLv2+
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig


%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q 
%patch0


%build
%cmake . -DBUILD_STATIC:BOOL=OFF
make VERBOSE=1 %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -exec rm -f {} ';'
# strip installed html doc
rm -rf %{buildroot}%{_docdir}/alure/html


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/*.so.*
%{_bindir}/alure*


%files devel
%defattr(-,root,root,-)
%doc docs/html examples
%{_includedir}/AL/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jan 30 2012 Bruno Wolff III <bruno@wolff.to> - 1.2-3
- Fix for gcc 4.7

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 29 2011 Julian Aloofi <julian@fedoraproject.org> - 1.2-1
- update to latest upstream release

* Sat May 28 2011 Julian Aloofi <julian@fedoraproject.org> - 1.1-1
- update to latest upstream release
- enabled FLAC, DUMB and fluidsynth support

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 01 2009 Guido Grazioli <guido.grazioli@gmail.com> - 1.0-4
- Fixed license for -devel subpackage
- Included sample code in -devel subpackage
- Sanitized %%files

* Tue Sep 29 2009 Guido Grazioli <guido.grazioli@gmail.com> - 1.0-3
- Renamed from libalure to alure
- Fixed license

* Mon Sep 28 2009 Guido Grazioli <guido.grazioli@gmail.com> - 1.0-2
- Fix multilib pkgconfig path

* Sat Sep 26 2009 Guido Grazioli <guido.grazioli@gmail.com> - 1.0-1
- Initial packaging 
